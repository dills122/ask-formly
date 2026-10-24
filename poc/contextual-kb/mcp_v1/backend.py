"""Own persistent resources around the unchanged advisory lookup implementation."""
import os
import json
import time
from contextlib import ExitStack
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
POC = HERE.parent
sys.path.insert(0,str(POC))
from agent_contract.advisory_lookup_v1.lookup import AdvisoryLookup
from agent_contract.advisory_lookup_v1.transport import ProcessExtractor
from agent_contract.advisory_lookup_v1.runtime import IntegrityError, digest
from agent_contract.retrieval_integration_v1.bridge import readonly
from kbcompiler.question_pilot import PilotIndex

class Backend:
    def __init__(self, seed=1701):
        self.seed = seed
        self.stack = ExitStack()
        self.extractors = []
        self.closed = False
        self.dbpath = POC/'build/knowledge.sqlite'
        self.dbhash = digest(self.dbpath)
        # Reuse the frozen offline model cache read-only; no corpus/index rebuild.
        os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(POC/'agent_contract/advisory_lookup_v1/test-output/embed-cache'),
                          HF_HUB_OFFLINE='1')
        try:
            db = self.stack.enter_context(readonly(self.dbpath))
            self.db = db
            started = time.perf_counter()
            self.index = PilotIndex(db)
            self.setup_seconds = time.perf_counter()-started
            self.lookup_service = AdvisoryLookup(self.index, self._extractor)
        except BaseException:
            self.stack.close()
            raise

    def _extractor(self):
        value = ProcessExtractor(self.seed)
        self.extractors.append(value)
        return value

    def lookup(self, request, core):
        if self.closed: raise RuntimeError('Backend closed')
        if digest(self.dbpath)!=self.dbhash: raise IntegrityError('Knowledge DB changed')
        result = self.lookup_service.lookup(request, core)
        checks = []
        for extractor in self.extractors:
            try: checks.append(extractor.verify_unchanged())
            except IntegrityError: raise
            except Exception as exc:
                checks.append({'parameters_unchanged':None,'error':type(exc).__name__})
                result['advisory']['status']='degraded'
                result['advisory']['diagnostics'].append('extractor_verification: '+str(exc))
        if digest(self.dbpath)!=self.dbhash: raise IntegrityError('Knowledge DB changed')
        result['citations']=citations_for(self.db, result['retrieval']['ids'])
        result['runtime']={'extractor_seed':self.seed,'model_checks':checks,
                           'db_unchanged':True,'index_setup_seconds':self.setup_seconds}
        return result

    def close(self):
        if self.closed: return
        self.closed = True
        try:
            for extractor in self.extractors: extractor.close()
        finally:
            self.stack.close()


def citations_for(db, fact_ids):
    """Attach stored provenance without modifying or certifying candidate facts."""
    result = {}
    for fact_id in fact_ids:
        row = db.execute(
            'SELECT d.source_path,d.source_sha256,f.source_quote,'
            'f.source_start_offset,f.source_end_offset,f.status '
            'FROM facts f JOIN documents d ON d.id=f.doc_id WHERE f.id=?',
            (fact_id,)).fetchone()
        if row is None:
            raise IntegrityError('Selected fact has no stored provenance')
        path, sha, quote, start, end, status = row
        evidence = [json.loads(r[0]) for r in db.execute(
            'SELECT e.record_json FROM fact_evidence fe JOIN evidence e ON e.id=fe.evidence_id '
            'WHERE fe.fact_id=? ORDER BY e.id', (fact_id,))]
        result[fact_id] = {'authored_source':{'path':path,'sha256':sha,'quote':quote,
                           'start_offset':start,'end_offset':end,'status':status},
                           'evidence':evidence}
    return result

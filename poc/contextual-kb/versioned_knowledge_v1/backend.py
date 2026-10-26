"""Explicit candidate DB composition; the installed launcher is unchanged."""
import os
import time
from contextlib import ExitStack
from pathlib import Path
from retrieval_repair_v1.integration import Backend as SelectedBackend
from retrieval_repair_v1.selector import Selector
from agent_contract.advisory_lookup_v1.lookup import AdvisoryLookup
from agent_contract.advisory_lookup_v1.runtime import digest
from agent_contract.retrieval_integration_v1.bridge import readonly
from versioned_knowledge_v1.index import Index

POC=Path(__file__).resolve().parent.parent

class Backend(SelectedBackend):
    def __init__(self,database,seed=1701,adapter=None,selector=None):
        self.seed=seed;self.stack=ExitStack();self.extractors=[];self.closed=False
        self.selector=selector if selector is not None else Selector()
        self.dbpath=Path(database).resolve()
        self.validate_database()
        self.dbhash=digest(self.dbpath)
        os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(POC/'agent_contract/advisory_lookup_v1/test-output/embed-cache'),HF_HUB_OFFLINE='1')
        try:
            self.db=self.stack.enter_context(readonly(self.dbpath))
            started=time.perf_counter()
            self.shared_index=Index(self.db)
            self.index=self.shared_index.for_scope('6.3.12',adapter)
            self.setup_seconds=time.perf_counter()-started
            self.lookup_service=AdvisoryLookup(self.index,self._extractor)
        except BaseException:
            self.stack.close();raise

    def validate_database(self):
        if self.dbpath==(POC/'build/knowledge.sqlite').resolve():raise ValueError('Candidate backend requires a separate database')

    def source_quote(self,fact_id):
        self.index.require([fact_id])
        return super().source_quote(fact_id)

    def lookup(self,request,core):
        result=super().lookup(request,core)
        result['citations']=self.index.citations(result['retrieval']['ids'])
        return result

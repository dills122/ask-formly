"""Reusable foundation + advisory extraction + unchanged full-question lookup."""
import copy,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent_contract.qualification_v3.candidate import build_plan
from agent_contract.advisory_lookup_v1.runtime import IntegrityError
from agent_contract.gliner_integration_v1.integration import integrate
from agent_contract.retrieval_integration_v1.bridge import retrieve

class AdvisoryLookup:
    """Load an optional extractor once. Advisory failures never disable search."""
    def __init__(self,index,extractor_factory=None):
        self.index=index
        self.extractor_factory=extractor_factory
        self.extractor=None
        self.load_error=None
        self.integrity_failure=None
        self.load_attempted=False
        self.load_seconds=0.0

    def lookup(self,request,question_plan):
        build_plan(request,question_plan)  # Invalid core fails before loading or I/O.
        if self.integrity_failure is not None:raise IntegrityError(self.integrity_failure)
        needed=bool(question_plan['formly_questions'])
        if needed and self.extractor_factory is not None and not self.load_attempted:
            self.load_attempted=True;started=time.perf_counter()
            try:
                self.extractor=self.extractor_factory()
                if not callable(self.extractor):raise TypeError('extractor must be callable')
            except IntegrityError as exc:
                self.integrity_failure=str(exc)
                raise
            except Exception as exc:
                self.extractor=None;self.load_error=type(exc).__name__+': '+str(exc)
            self.load_seconds=time.perf_counter()-started
        integrity_errors=[]
        def guarded_extract(text):
            try:return self.extractor(text)
            except IntegrityError as exc:
                integrity_errors.append(exc)
                raise
        result=integrate(request,question_plan,guarded_extract if needed and self.extractor is not None else None)
        if integrity_errors:
            self.integrity_failure=str(integrity_errors[0])
            raise integrity_errors[0]
        # Deliberately pass ONLY the search projection, not hints or other annotations.
        retrieval=retrieve(self.index,{'search_requests':result['plan']['search_requests']},enhanced=False)
        diagnostics=[]
        if needed and self.load_error:diagnostics.append('extractor_load: '+self.load_error)
        diagnostics.extend(f'question {r["question_index"]}: {r["error"]}' for r in result['extractions'] if r['error'])
        diagnostics.extend(result['plan']['hint_warnings'])
        status=('not_needed' if not needed else 'disabled' if self.extractor_factory is None else 'degraded' if diagnostics else 'available')
        return dict(**result,retrieval=retrieval,facts=[copy.deepcopy(self.index.facts[f]) for f in retrieval['ids']],
                    evidence_status='candidate_only',advisory=dict(status=status,policy='advisory_only',diagnostics=diagnostics,load_seconds=self.load_seconds))

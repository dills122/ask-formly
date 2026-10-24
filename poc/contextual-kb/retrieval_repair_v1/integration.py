"""New opt-in backend: unchanged foundation/extractor, bounded selected-fact repair."""
import copy,sys
from pathlib import Path
POC=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(POC))
from mcp_v1.backend import Backend as OriginalBackend,citations_for
from agent_contract.advisory_lookup_v1.runtime import digest,IntegrityError
from retrieval_repair_v1.policy import repair
from retrieval_repair_v1.selector import Selector

class Backend(OriginalBackend):
    def __init__(self,seed=1701,selector=None):
        self.selector=selector if selector is not None else Selector()
        super().__init__(seed)
    def source_quote(self,fact_id):
        row=self.db.execute('SELECT source_quote FROM facts WHERE id=?',(fact_id,)).fetchone()
        if row is None:raise IntegrityError('Candidate source record missing')
        return row[0]
    def lookup(self,request,core):
        result=copy.deepcopy(super().lookup(request,core))
        baseline=list(result['retrieval']['ids'])
        selection=repair(self.index,core,baseline,self.source_quote,self.selector)
        if digest(self.dbpath)!=self.dbhash:raise IntegrityError('Knowledge DB changed during selection')
        result['selection']=selection
        result['retrieval']['foundation_ids']=baseline
        result['retrieval']['ids']=selection['ids']
        result['facts']=[copy.deepcopy(self.index.facts[f]) for f in selection['ids']]
        result['citations']=citations_for(self.db,selection['ids'])
        return result

import copy,json,sys,unittest
from pathlib import Path
POC=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(POC))
from wording_candidate_v1.serve import make_service
from agent_contract.qualification_v3.candidate import build_plan

class Backend:
    def __init__(self):self.cores=[]
    def lookup(self,request,core):
        plan=build_plan(request,core);self.cores.append(copy.deepcopy(core))
        return {'plan':plan}
    def close(self):pass

class ServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_normalized_plan_crosses_existing_strict_service_boundary(self):
        row=json.loads((POC/'retrieval_repair_v1/test-output/fresh/F01.json').read_text())
        backend=Backend()
        service=make_service(planner=lambda _: (row['core'],{'attempt_id':'saved-F01'}),backend_factory=lambda:backend)
        try:
            result=await service.lookup(row['request'])
            self.assertEqual(len(backend.cores),1)
            self.assertEqual(result['generation']['wording_normalization']['original_plan'],row['core'])
            self.assertEqual(result['plan']['search_requests'][0]['query'],'In Formly, how can I configure props.disabled to track model.isLocked?')
            self.assertEqual(result['generation']['attempt_id'],'saved-F01')
        finally:await service.close()
    async def test_lost_condition_stops_before_backend(self):
        row=json.loads((POC/'retrieval_repair_v1/test-output/fresh/F01.json').read_text())
        row['core']['formly_questions'][0]['question']=row['core']['formly_questions'][0]['question'].replace('model.isLocked','model.other')
        def forbidden():raise AssertionError('Backend should not initialize')
        service=make_service(planner=lambda _: (row['core'],{}),backend_factory=forbidden)
        try:
            with self.assertRaises(ValueError):await service.lookup(row['request'])
        finally:await service.close()

if __name__=='__main__':unittest.main()

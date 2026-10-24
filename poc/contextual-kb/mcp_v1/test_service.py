import asyncio, copy, json, tempfile, unittest
from pathlib import Path
from service import LookupService
from planner import decode_plan, planner_command, PlannerError

CORE={'formly_questions':[],'library_constraints':{'formly_version':None,'ui_adapter':None},'condition_bindings':[]}
class Planner:
    def __init__(self, core=None):self.calls=[];self.core=CORE if core is None else core
    def __call__(self, request):self.calls.append(request);return copy.deepcopy(self.core),{'model':'test'}
class Backend:
    def __init__(self):self.calls=[];self.closed=False;self.failure=None
    def lookup(self, request, core):
        self.calls.append((request,core))
        if self.failure:raise self.failure
        return {'plan':{'question_plan':core},'facts':[],'advisory':{'status':'not_needed'},'evidence_status':'candidate_only'}
    def close(self):self.closed=True
class ServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_raw_request_and_core_are_preserved_and_backend_reused(self):
        p=Planner();b=Backend();s=LookupService(p,lambda:b)
        r=await s.lookup('  Formly question  ');await s.lookup('another')
        self.assertEqual(p.calls,['  Formly question  ','another']);self.assertEqual(b.calls[0],('  Formly question  ',CORE))
        self.assertEqual(r['evidence_status'],'candidate_only');self.assertEqual(r['knowledge_scope']['version'],'6.3.12')
        await s.close();self.assertTrue(b.closed)
    async def test_invalid_input_does_no_planning_or_loading(self):
        p=Planner();s=LookupService(p,lambda:self.fail('loaded'))
        for x in ['', '  ',None,4,'a'*12001]:
            with self.assertRaises(ValueError):await s.lookup(x)
        self.assertEqual(p.calls,[])
    async def test_invalid_plan_never_loads_backend(self):
        s=LookupService(Planner({'wrong':'shape'}),lambda:self.fail('loaded'))
        with self.assertRaises(ValueError):await s.lookup('Formly')
    async def test_integrity_failure_stays_fatal_before_later_planning(self):
        from agent_contract.advisory_lookup_v1.runtime import IntegrityError
        p=Planner();b=Backend();b.failure=IntegrityError('drift');s=LookupService(p,lambda:b)
        for _ in range(2):
            with self.assertRaises(IntegrityError):await s.lookup('Formly')
        self.assertEqual(len(p.calls),1);self.assertTrue(b.closed)
    async def test_closed_service_cannot_reopen(self):
        s=LookupService(Planner(),lambda:self.fail('loaded'));await s.close()
        with self.assertRaises(RuntimeError):await s.lookup('Formly')
    async def test_concurrent_calls_are_serialized(self):
        import time
        class Slow(Planner):
            active=0;peak=0
            def __call__(self,request):
                self.active+=1;self.peak=max(self.peak,self.active);time.sleep(.02);self.active-=1
                return super().__call__(request)
        p=Slow();s=LookupService(p,Backend)
        await asyncio.gather(s.lookup('one'),s.lookup('two'))
        self.assertEqual(p.peak,1)
    async def test_cancelled_call_finishes_before_backend_closes(self):
        import threading
        entered=threading.Event();release=threading.Event();b=Backend()
        class Slow(Planner):
            def __call__(self,request):entered.set();release.wait(2);return super().__call__(request)
        s=LookupService(Slow(),lambda:b);task=asyncio.create_task(s.lookup('Formly'))
        await asyncio.to_thread(entered.wait,1);task.cancel();closing=asyncio.create_task(s.close())
        await asyncio.sleep(.02);self.assertFalse(closing.done());release.set()
        with self.assertRaises(asyncio.CancelledError):await task
        await closing;self.assertTrue(b.closed)
class PlannerTests(unittest.TestCase):
    def test_strict_json_only_and_no_duplicate_keys(self):
        self.assertEqual(decode_plan(json.dumps(CORE)),CORE)
        for x in ['```json\n{}\n```','{"x":1,"x":2}','{"x":NaN}','[]']:
            with self.assertRaises(PlannerError):decode_plan(x)
    def test_command_keeps_request_out_of_shell_and_disables_tools(self):
        cmd=planner_command('codex',Path('/poc/contract.md'),Path('/poc/schema.json'),Path('/poc/job'))
        self.assertIn('--ignore-user-config',cmd);self.assertIn('--ephemeral',cmd)
        self.assertIn('features.shell_tool=false',cmd);self.assertIn('read-only',cmd)
        self.assertIn('model_instructions_file="/poc/contract.md"',cmd)
        self.assertEqual(cmd[-1],'-')
if __name__=='__main__':unittest.main()

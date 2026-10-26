import json
from pathlib import Path
import sys
import tempfile
import unittest
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'model_free_v1'))
from test_candidate import fixture,plan
from candidate import digest
HERE=Path(__file__).resolve().parent

class RepairTransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_feedback_error_and_text_survive_real_stdio(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);db=root/'db.sqlite';fixture(db)
            args=['-B',str(HERE.parent/'model_free_v1/offline_guard.py'),str(HERE/'serve.py'),'--database',str(db),'--sha256',digest(db),'--settings',str(root/'settings.sqlite')]
            env={'HOME':tmp,'PATH':'','HF_HOME':str(root/'empty'),'XDG_CACHE_HOME':str(root/'cache'),'PYTHONDONTWRITEBYTECODE':'1'}
            with (root/'stderr').open('w') as stderr:
                async with stdio_client(StdioServerParameters(command=sys.executable,args=args,env=env),errlog=stderr) as (r,w):
                    async with ClientSession(r,w) as session:
                        await session.initialize()
                        result=await session.call_tool('lookup_formly',{'request':'alpha'})
                        self.assertFalse(result.isError);self.assertEqual('PLAN_REQUIRED',result.structuredContent['issues'][0]['code'])
                        p=plan('alpha','without beta')
                        result=await session.call_tool('lookup_formly',{'request':'alpha without beta','plan':p})
                        self.assertTrue(result.isError)
                        self.assertEqual('MISSING_DECLARED_CONDITION',result.structuredContent['issues'][0]['code'])
                        self.assertEqual(result.structuredContent,json.loads(result.content[0].text))
                        p['formly_questions'][0]['question']='alpha without beta'
                        result=await session.call_tool('lookup_formly',{'request':'alpha without beta','plan':p})
                        self.assertFalse(result.isError);self.assertEqual('ok',result.structuredContent['status'])
                        self.assertEqual(result.structuredContent,json.loads(result.content[0].text))
                        result=await session.call_tool('lookup_formly',{'request':'alpha','plan':{'bad':'shape'}})
                        self.assertTrue(result.isError)
            self.assertIn('OFFLINE_GUARDS_ACTIVE',(root/'stderr').read_text())

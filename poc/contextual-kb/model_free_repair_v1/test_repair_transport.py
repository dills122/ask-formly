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
from model_free_v1.response import MAX_TRANSPORT_BYTES, encoded_size
HERE=Path(__file__).resolve().parent

def unpack(result):
    return result.structuredContent or json.loads(result.content[0].text)

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
                        self.assertFalse(result.isError);self.assertEqual('PLAN_REQUIRED',unpack(result)['issues'][0]['code'])
                        p=plan('alpha','without beta')
                        result=await session.call_tool('lookup_formly',{'request':'alpha without beta','plan':p})
                        self.assertTrue(result.isError)
                        self.assertEqual('MISSING_DECLARED_CONDITION',unpack(result)['issues'][0]['code'])
                        self.assertIsNone(result.structuredContent)
                        self.assertEqual(1,len(result.content))
                        self.assertLessEqual(encoded_size(result.model_dump(mode='json')),MAX_TRANSPORT_BYTES)
                        self.assertEqual(encoded_size(result.model_dump(mode='json')),unpack(result)['response']['transport_bytes'])
                        p['formly_questions'][0]['question']='alpha without beta'
                        result=await session.call_tool('lookup_formly',{'request':'alpha without beta','plan':p})
                        self.assertFalse(result.isError);self.assertEqual('ok',unpack(result)['status'])
                        self.assertIsNone(result.structuredContent)
                        self.assertEqual(1,len(result.content))
                        self.assertLessEqual(encoded_size(result.model_dump(mode='json')),MAX_TRANSPORT_BYTES)
                        self.assertEqual(encoded_size(result.model_dump(mode='json')),unpack(result)['response']['transport_bytes'])
                        result=await session.call_tool('lookup_formly',{'request':'alpha','plan':{'bad':'shape'}})
                        self.assertTrue(result.isError)
                        request='For Formly 6.3.12 with Material, explain alpha.'
                        p=plan('alpha')
                        result=await session.call_tool('lookup_formly',{'request':request,'plan':p})
                        self.assertTrue(result.isError)
                        self.assertEqual(['MISSING_SCOPE_METADATA']*2,[i['code'] for i in unpack(result)['issues']])
                        self.assertIsNone(result.structuredContent)
                        self.assertEqual(1,len(result.content))
                        self.assertLessEqual(encoded_size(result.model_dump(mode='json')),MAX_TRANSPORT_BYTES)
                        self.assertEqual(encoded_size(result.model_dump(mode='json')),unpack(result)['response']['transport_bytes'])
                        self.assertTrue(unpack(result)['next_action']['preserve_original_request'])
                        p['library_constraints']={'formly_version':'6.3.12','ui_adapter':'material'}
                        result=await session.call_tool('lookup_formly',{'request':request,'plan':p})
                        self.assertFalse(result.isError)
                        self.assertEqual(request,unpack(result)['request'])
                        self.assertEqual('material',unpack(result)['ui_adapter'])
            self.assertIn('OFFLINE_GUARDS_ACTIVE',(root/'stderr').read_text())

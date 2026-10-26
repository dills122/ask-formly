import sys
from pathlib import Path
POC=Path(__file__).resolve().parent.parent
sys.path[:0]=[str(POC),str(POC/'mcp_v1')]
import tempfile
import unittest
from pathlib import Path
from mcp_v1.project_settings import ProjectSettings
from versioned_knowledge_v1.context import Context

class FakeService:
    def __init__(self,adapter):self.adapter=adapter;self.calls=[];self.closed=False
    async def lookup(self,request):self.calls.append(request);return {'facts':[],'adapter_seen':self.adapter}
    async def close(self):self.closed=True

class ContextTests(unittest.IsolatedAsyncioTestCase):
    async def test_legacy_explicit_saved_and_unsupported_routing(self):
        with tempfile.TemporaryDirectory() as tmp:
            services=[]
            def factory(adapter):
                s=FakeService(adapter);services.append(s);return s
            context=Context(factory,ProjectSettings(Path(tmp)/'settings.sqlite'))
            legacy=await context.lookup('Formly defaults')
            self.assertEqual('6.3.12',legacy['version_context']['selected'])
            self.assertIsNone(legacy['adapter_seen'])
            core=await context.lookup('Formly defaults',project_id='p',formly_version='v6',ui_adapter='core')
            self.assertEqual('core',core['adapter_seen'])
            saved=await context.lookup('Formly defaultValue',project_id='p')
            self.assertEqual('core',saved['adapter_seen'])
            no=await context.lookup('Formly defaultValue',formly_version='7')
            self.assertEqual('unsupported_version',no['status']);self.assertEqual(2,len(services))
            self.assertEqual([1,2],[len(s.calls) for s in services])
            await context.close();self.assertTrue(all(s.closed for s in services))

if __name__=='__main__':unittest.main()

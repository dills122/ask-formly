import json,sys,tempfile,unittest
from datetime import timedelta
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
HERE=Path(__file__).resolve().parent
class TransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_stdio_schema_failures_noise_and_reuse(self):
        with tempfile.TemporaryDirectory(dir=HERE/'test-output') as tmp:
            script=Path(tmp)/'fake_server.py'
            script.write_text('''import sys
sys.path.insert(0,''' + repr(str(HERE)) + ''')
from server import create_server
class Service:
    n=0
    async def lookup(self,request):
        print('native diagnostic noise')
        if not request.strip():raise ValueError('empty request')
        self.n+=1
        return {'request':request,'count':self.n,'evidence_status':'candidate_only'}
    async def close(self):pass
create_server(Service()).run(transport='stdio')
''')
            with (Path(tmp)/'stderr.txt').open('w') as err:
                async with stdio_client(StdioServerParameters(command=sys.executable,args=['-B',str(script)]),errlog=err) as (r,w):
                    async with ClientSession(r,w) as session:
                        await session.initialize();tools=await session.list_tools()
                        self.assertEqual([t.name for t in tools.tools],['lookup_formly'])
                        for i in (1,2):
                            result=await session.call_tool('lookup_formly',{'request':'Formly'},read_timeout_seconds=timedelta(seconds=10))
                            self.assertFalse(result.isError);self.assertEqual(result.structuredContent['count'],i)
                        for arguments in [{},{'request':''},{'request':4}]:
                            bad=await session.call_tool('lookup_formly',arguments)
                            self.assertTrue(bad.isError)
                self.assertIn('native diagnostic noise',(Path(tmp)/'stderr.txt').read_text())
if __name__=='__main__':unittest.main()

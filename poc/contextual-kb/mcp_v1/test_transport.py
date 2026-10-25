import json,sys,tempfile,unittest
from datetime import timedelta
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
HERE=Path(__file__).resolve().parent
class TransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_stdio_schema_failures_noise_and_reuse(self):
        (HERE/'test-output').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=HERE/'test-output') as tmp:
            script=Path(tmp)/'fake_server.py'
            script.write_text('''import sys
sys.path.insert(0,''' + repr(str(HERE)) + ''')
from server import create_server
from project_settings import ProjectSettings
class Service:
    n=0
    async def lookup(self,request):
        print('native diagnostic noise')
        if not request.strip():raise ValueError('empty request')
        self.n+=1
        return {'request':request,'count':self.n,'evidence_status':'candidate_only'}
    async def close(self):pass
create_server(Service(),settings=ProjectSettings(__file__+'.sqlite')).run(transport='stdio')
''')
            with (Path(tmp)/'stderr.txt').open('w') as err:
                async with stdio_client(StdioServerParameters(command=sys.executable,args=['-B',str(script)]),errlog=err) as (r,w):
                    async with ClientSession(r,w) as session:
                        await session.initialize();tools=await session.list_tools()
                        self.assertEqual([t.name for t in tools.tools],
                                         ['lookup_formly','get_formly_project_settings','set_formly_project_settings'])
                        lookup = tools.tools[0]
                        self.assertEqual(lookup.inputSchema['required'], ['request'])
                        self.assertFalse(lookup.annotations.readOnlyHint)
                        for i in (1,2):
                            result=await session.call_tool('lookup_formly',{'request':'Formly'},read_timeout_seconds=timedelta(seconds=10))
                            self.assertFalse(result.isError);self.assertEqual(result.structuredContent['count'],i)
                        for arguments in [{},{'request':''},{'request':4}]:
                            bad=await session.call_tool('lookup_formly',arguments)
                            self.assertTrue(bad.isError)
                        saved = await session.call_tool('set_formly_project_settings',
                            {'project_id':'project-a','formly_version':'v6','ui_adapter':'Material'})
                        self.assertFalse(saved.isError)
                        self.assertEqual(saved.structuredContent['formly_version'],'v6')
                        matched = await session.call_tool('lookup_formly',
                            {'request':'follow-up','project_id':'project-a'})
                        self.assertEqual(matched.structuredContent['version_context']['selected'],'6.3.12')
                        self.assertEqual(matched.structuredContent['count'],3)
                        unsupported = await session.call_tool('lookup_formly',
                            {'request':'upgrade','project_id':'project-a','worktree_id':'upgrade','formly_version':'7'})
                        self.assertEqual(unsupported.structuredContent['status'],'unsupported_version')
                        self.assertNotIn('count',unsupported.structuredContent)
                        read = await session.call_tool('get_formly_project_settings',
                            {'project_id':'project-a','worktree_id':'upgrade'})
                        self.assertEqual(read.structuredContent['formly_version'],'7')
                        self.assertEqual(read.structuredContent['ui_adapter'],'material')
                        parent = await session.call_tool('lookup_formly',
                            {'request':'parent','project_id':'project-a'})
                        self.assertEqual(parent.structuredContent['count'],4)
                        bad = await session.call_tool('lookup_formly',
                            {'request':'question','worktree_id':'orphan'})
                        self.assertTrue(bad.isError)
                        bad = await session.call_tool('set_formly_project_settings',
                            {'project_id':'project-a','formly_version':'latest'})
                        self.assertTrue(bad.isError)
                # A second server process reads the same persistent project store.
                async with stdio_client(StdioServerParameters(command=sys.executable,args=['-B',str(script)]),errlog=err) as (r,w):
                    async with ClientSession(r,w) as session:
                        await session.initialize()
                        result = await session.call_tool('lookup_formly',
                            {'request':'restart','project_id':'project-a'})
                        self.assertEqual(result.structuredContent['version_context']['requested'],'v6')
                        self.assertEqual(result.structuredContent['count'],1)
                        result = await session.call_tool('lookup_formly',
                            {'request':'restart','project_id':'project-a','worktree_id':'upgrade'})
                        self.assertEqual(result.structuredContent['status'],'unsupported_version')
                self.assertIn('native diagnostic noise',(Path(tmp)/'stderr.txt').read_text())
if __name__=='__main__':unittest.main()

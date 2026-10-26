import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from test_candidate import fixture
from candidate import digest

HERE=Path(__file__).resolve().parent

class TransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_offline_stdio_with_guarded_empty_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);db=root/'db.sqlite';fixture(db)
            command=[str(HERE/'server.py'),'--database',str(db),'--sha256',digest(db),'--settings',str(root/'settings.sqlite')]
            env={'HOME':str(root),'PATH':'','XDG_CACHE_HOME':str(root/'cache'),'HF_HOME':str(root/'hf'),'HF_HUB_OFFLINE':'1','PYTHONDONTWRITEBYTECODE':'1'}
            with (root/'stderr').open('w') as stderr:
                async with stdio_client(StdioServerParameters(command=sys.executable,args=['-B',str(HERE/'offline_guard.py'),*command],env=env),errlog=stderr) as (read,write):
                    async with ClientSession(read,write) as session:
                        init=await session.initialize();tools=await session.list_tools()
                        lookup=next(t for t in tools.tools if t.name=='lookup_formly')
                        self.assertIn('plan',lookup.inputSchema['properties'])
                        result=await session.call_tool('lookup_formly',{'request':'alpha beta'})
                        self.assertFalse(result.isError)
                        packet=result.structuredContent
                        self.assertEqual('not_decomposed',packet['planning']['status'])
                        self.assertIn('and',[f['id'] for f in packet['facts']])
                        self.assertEqual(packet,json.loads(result.content[0].text))
                        result=await session.call_tool('get_formly_facts',{'fact_ids':['target']})
                        self.assertFalse(result.isError);self.assertEqual('target',result.structuredContent['facts'][0]['id'])
                        result=await session.call_tool('lookup_formly',{'request':'alpha','plan':{'wrong':True}})
                        self.assertTrue(result.isError)
                        result=await session.call_tool('lookup_formly',{'request':'alpha','formly_version':'7'})
                        self.assertEqual('unsupported_version',result.structuredContent['status'])
            self.assertIn('OFFLINE_GUARDS_ACTIVE', (root/'stderr').read_text())

if __name__=='__main__':unittest.main()

"""Asset-free real stdio checks for the opt-in candidate and unchanged baseline."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

POC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(POC))
sys.path.insert(0, str(POC / 'model_free_v1'))
from test_candidate import fixture, plan
from candidate import digest
from linked_examples_v1.test_catalog import example
from model_free_v1.response import encoded_size


class TransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_candidate_real_stdio_and_baseline_isolation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db = root / 'facts.sqlite'; fixture(db)
            catalog = root / 'examples/demo'; catalog.mkdir(parents=True)
            record = example(facts=['target'])
            record['provenance'] = [dict(kind='authored_fact', reference='target')]
            (catalog / 'manifest.json').write_text(json.dumps(record))
            (catalog / 'demo.ts').write_text('export const field = {resetOnHide: false};')
            runner = root / 'runner.py'
            runner.write_text('''import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from linked_examples_v1.serve import create_server, Catalog, RepairService, Service, Store
db, sha, settings, examples = sys.argv[2:]
store = Store(Path(db), sha)
create_server(RepairService(Service(store, Path(settings))), Catalog(Path(examples), set(store.facts))).run(transport='stdio')
''')
            for candidate in (False, True):
                if candidate:
                    args = [str(runner), str(POC), str(db), digest(db), str(root/'candidate-settings.sqlite'), str(root/'examples')]
                else:
                    args = [str(POC/'model_free_repair_v1/serve.py'), '--database', str(db), '--sha256', digest(db), '--settings', str(root/'baseline-settings.sqlite')]
                with (root/'stderr').open('w') as stderr:
                    async with stdio_client(StdioServerParameters(command=sys.executable, args=args), errlog=stderr) as (read, write):
                        async with ClientSession(read, write) as session:
                            init = await session.initialize()
                            names = {t.name for t in (await session.list_tools()).tools}
                            self.assertEqual(candidate, 'get_formly_examples' in names)
                            if not candidate: continue
                            self.assertIn('Isolated linked examples', init.instructions)
                            async def call(name, args):
                                result = await session.call_tool(name, args)
                                self.assertFalse(result.isError, result)
                                self.assertIsNone(result.structuredContent)
                                self.assertEqual(1, len(result.content))
                                self.assertLessEqual(encoded_size(result.model_dump(mode='json')), 30000)
                                return json.loads(result.content[0].text)
                            question = 'How does resetOnHide false preserve the model?'
                            p = plan(question)
                            p['library_constraints'] = dict(formly_version='6.3.12', ui_adapter='material')
                            packet = await call('lookup_formly', dict(request=question, plan=p))
                            self.assertEqual('demo', packet['example_references'][0]['id'])
                            facts = await call('get_formly_facts', dict(fact_ids=['target'], formly_version='6.3.12', ui_adapter='material'))
                            self.assertEqual('demo', facts['example_references'][0]['id'])
                            page = await call('get_formly_examples', dict(fact_ids=['target']))
                            self.assertNotIn('files', page['examples'][0])
                            full = await call('get_formly_examples', dict(example_ids=['demo']))
                            self.assertIn('resetOnHide', full['examples'][0]['files'][0]['content'])
                            stopped = await call('get_formly_examples', dict(fact_ids=['target'], formly_version='7'))
                            self.assertEqual('unsupported_scope', stopped['status'])
                            invalid = await session.call_tool('get_formly_examples', dict(example_ids=['missing']))
                            self.assertTrue(invalid.isError)


if __name__ == '__main__': unittest.main()

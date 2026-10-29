import asyncio
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discovery import catalog_page, discover


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.packet = dict(status='ok', facts=[dict(id='a')], questions=[
            dict(fact_ids=['a'], omitted_ids=['b', 'c']),
            dict(fact_ids=['a'], omitted_ids=['d', 'b'])])
        self.facts = {k: dict(id=k, claim='claim ' + k, context='context',
            conditions=['only when enabled'], limits=['not universal'], title=k,
            version='6.3.12', adapter='core', applicability=[{'scope': 'exact'}])
            for k in 'abcd'}
        self.reads = []

    def records(self, ids):
        self.reads.extend(ids)
        return [copy.deepcopy(self.facts[k]) for k in ids]

    def test_pages_are_fair_unique_and_exclude_already_delivered(self):
        first = catalog_page(self.packet, self.records, limit=2)
        second = catalog_page(self.packet, self.records, offset=first['next_offset'], limit=2)
        self.assertEqual([f['id'] for f in first['candidates']], ['b', 'd'])
        self.assertEqual([f['id'] for f in second['candidates']], ['c'])
        self.assertIsNone(second['next_offset'])

    def test_preserves_full_conditions_limits_and_scope_without_mutation(self):
        before = copy.deepcopy(self.packet)
        page = catalog_page(self.packet, self.records)
        self.assertEqual(page['candidates'][0], self.facts['b'])
        self.assertEqual(self.packet, before)
        self.assertEqual(page['evidence_status'], 'discovery_only_fetch_full_citations')
        self.assertEqual(page['record_kind'], 'claims_without_provenance')
        self.assertNotIn('citations', page)

    def test_byte_boundary_does_not_skip_the_next_candidate(self):
        size = len(json.dumps([self.facts['b']], ensure_ascii=False).encode())
        page = catalog_page(self.packet, self.records, byte_budget=size)
        self.assertEqual([f['id'] for f in page['candidates']], ['b'])
        self.assertEqual(page['next_offset'], 1)
        self.assertLessEqual(page['candidate_bytes'], size)

    def test_oversized_single_record_fails_instead_of_clipping_or_looping(self):
        with self.assertRaisesRegex(ValueError, 'complete candidate'):
            catalog_page(self.packet, self.records, byte_budget=2)

    def test_invalid_pagination_rejected(self):
        for kwargs in [dict(offset=-1), dict(offset=True), dict(limit=0), dict(limit=33), dict(byte_budget=24001)]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                catalog_page(self.packet, self.records, **kwargs)

    def test_scope_or_repair_feedback_does_not_read_records(self):
        packet = dict(status='unsupported_scope', next_action={'type':'stop'})
        self.assertEqual(catalog_page(packet, self.records), packet)
        self.assertEqual(self.reads, [])


class TargetedDiscoveryTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.searches = []
        self.reads = []
        self.packet = dict(status='ok', facts=[dict(id='a')],
                           version_context={'selected': '6.3.12'}, ui_adapter='core')
        self.plan = dict(formly_questions=[dict(question='alpha', reason='First facet'),
                                          dict(question='beta', reason='Second facet')],
                        library_constraints=dict(formly_version='6.3.12', ui_adapter='core'),
                        condition_bindings=[])
        outer = self
        class Store:
            facts = {fid: dict(id=fid, claim=claim, context='', title='',
                     conditions=['when enabled'], limits=['bounded'])
                     for fid, claim in [('a', 'already delivered fallback'),
                         ('b', 'general alpha configuration'), ('c', 'initial model fallback'),
                         ('d', 'beta control configuration'), ('e', 'outside scope fallback')]}
            def search(self, question, *scope):
                outer.searches.append((question, scope))
                return ['a', 'b', 'c'] if question == 'alpha' else ['d', 'a', 'b']
            def records(self, ids, *scope):
                outer.reads.extend(ids)
                return ([dict(copy.deepcopy(self.facts[fid]), applicability=[{'scope': 'exact'}])
                         for fid in ids], {})
        class Service:
            store = Store()
            async def lookup(self, request, plan=None, **scope):
                return copy.deepcopy(outer.packet), outer.packet.get('status') == 'needs_refinement'
        self.service = Service()

    async def test_targeted_pages_keep_question_order_and_exclude_global_delivery(self):
        page, error = await discover(self.service, 'alpha and beta', self.plan,
                                     question_index=1, limit=1)
        self.assertFalse(error)
        self.assertEqual(['d'], [r['id'] for r in page['candidates']])
        self.assertEqual(1, page['question_index'])
        self.assertEqual(4, page['question_ref']['characters'])
        self.assertEqual(2, page['total_omitted_candidates'])
        second, _ = await discover(self.service, 'alpha and beta', self.plan,
                                   question_index=1, offset=page['next_offset'], limit=1)
        self.assertEqual(['b'], [r['id'] for r in second['candidates']])
        self.assertIsNone(second['next_offset'])
        self.assertTrue(all(q == 'beta' for q, scope in self.searches))
        self.assertEqual(['when enabled'], second['candidates'][0]['conditions'])

    async def test_no_selector_preserves_global_interleaving(self):
        page, _ = await discover(self.service, 'alpha and beta', self.plan)
        self.assertEqual(['b', 'd', 'c'], [r['id'] for r in page['candidates']])
        self.assertIsNone(page['question_index'])
        self.assertNotIn('question_ref', page)

    async def test_focus_reranks_only_original_omissions_and_pages_stably(self):
        before = copy.deepcopy(self.plan)
        args = dict(question_index=0, focus='initial model fallback', limit=1)
        page, error = await discover(self.service, 'alpha and beta', self.plan, **args)
        repeated, _ = await discover(self.service, 'alpha and beta', self.plan, **args)
        self.assertFalse(error)
        self.assertEqual(page, repeated)
        self.assertEqual(['c'], [r['id'] for r in page['candidates']])
        self.assertEqual(2, page['total_omitted_candidates'])
        self.assertEqual('not_assessed', page['focus_matching']['semantic_relevance'])
        self.assertIn('restart offset at zero', page['next_action']['message'])
        second, _ = await discover(self.service, 'alpha and beta', self.plan,
                                   offset=page['next_offset'], **args)
        self.assertEqual(['b'], [r['id'] for r in second['candidates']])
        self.assertEqual(['when enabled'], page['candidates'][0]['conditions'])
        self.assertEqual(before, self.plan)
        self.assertTrue(all(question == 'alpha' for question, scope in self.searches))
        self.assertNotIn('e', self.reads)
        self.assertNotIn('a', self.reads)

    async def test_focus_without_selector_preserves_fair_interleaving(self):
        page, _ = await discover(self.service, 'alpha and beta', self.plan,
                                 focus='initial model fallback')
        self.assertEqual(['c', 'd', 'b'], [r['id'] for r in page['candidates']])

    async def test_unmatched_focus_keeps_candidates_without_claiming_absence(self):
        page, _ = await discover(self.service, 'alpha and beta', self.plan,
                                 question_index=0, focus='unrecognizedWidget')
        self.assertEqual(['b', 'c'], [r['id'] for r in page['candidates']])
        self.assertEqual('no_recognized_identifier', page['focus_matching']['signal'])
        self.assertEqual('not_assessed', page['focus_matching']['semantic_relevance'])
        self.assertIn('prove absence', page['next_action']['message'])

    async def test_invalid_focus_rejected_before_reads(self):
        for focus in (True, 2, [], {}, '', '   ', 'x' * 501):
            with self.subTest(focus=focus), self.assertRaisesRegex(ValueError, 'focus'):
                await discover(self.service, 'alpha and beta', self.plan, focus=focus)
        self.assertFalse(self.searches)
        self.assertFalse(self.reads)

    async def test_invalid_indices_reject_without_reading_records(self):
        for index in (True, False, -1, 2, 1.0, '1'):
            with self.subTest(index=index), self.assertRaises(ValueError):
                await discover(self.service, 'alpha and beta', self.plan, question_index=index)
        self.assertFalse(self.reads)

    async def test_scope_and_repair_gate_precede_targeted_discovery(self):
        for status in ('unsupported_scope', 'needs_refinement'):
            self.packet = dict(status=status, issues=[{'code': 'MISSING_DECLARED_CONDITION'}])
            page, error = await discover(self.service, 'alpha and beta', self.plan,
                                         question_index=1, focus='bypass attempt')
            self.assertEqual(status, page['status'])
            self.assertEqual(status == 'needs_refinement', error)
        self.assertFalse(self.searches)
        self.assertFalse(self.reads)


class DiscoveryTransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_target_selector_and_gates_survive_real_stdio(self):
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        from model_free_v1.response import encoded_size, MAX_TRANSPORT_BYTES
        poc = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runner = root / 'serve_fixture.py'
            runner.write_text('''import sys
from pathlib import Path
poc=Path(sys.argv[1])
sys.path[:0]=[str(poc),str(poc/'model_free_v1'),str(poc/'parity_v1')]
from test_response_contract import FakeStore
from parity_v1.serve_discovery import create_discovery_server,RepairService,Service
store=FakeStore();store.close=lambda:None
create_discovery_server(RepairService(Service(store,Path(sys.argv[2])))).run(transport='stdio')
''')
            with (root / 'stderr').open('w') as stderr:
                async with stdio_client(StdioServerParameters(command=sys.executable,
                        args=['-B', str(runner), str(poc), str(root / 'settings.sqlite')]), errlog=stderr) as (r, w):
                    async with ClientSession(r, w) as session:
                        await session.initialize()
                        tools = await session.list_tools()
                        schema = next(t.inputSchema for t in tools.tools if t.name == 'discover_formly_candidates')
                        self.assertIn('question_index', schema['properties'])
                        self.assertIn('focus', schema['properties'])
                        plan = dict(formly_questions=[dict(question='alpha', reason='First facet'),
                                                      dict(question='beta', reason='Second facet')],
                                    library_constraints=dict(formly_version='6.3.12', ui_adapter='core'),
                                    condition_bindings=[])
                        args = dict(request='alpha and beta', plan=plan, formly_version='6.3.12', ui_adapter='core')
                        lookup = await session.call_tool('lookup_formly', args)
                        self.assertFalse(lookup.isError)
                        delivered = {f['id'] for f in json.loads(lookup.content[0].text)['facts']}
                        result = await session.call_tool('discover_formly_candidates', dict(args, question_index=1, limit=3))
                        self.assertFalse(result.isError)
                        page = json.loads(result.content[0].text)
                        expected = [str(i) for i in reversed(range(40)) if str(i) not in delivered][:3]
                        self.assertEqual(expected, [f['id'] for f in page['candidates']])
                        self.assertEqual(1, page['question_index'])
                        self.assertIsNone(result.structuredContent)
                        self.assertEqual(1, len(result.content))
                        self.assertLessEqual(encoded_size(result.model_dump(mode='json')), MAX_TRANSPORT_BYTES)
                        self.assertEqual(encoded_size(result.model_dump(mode='json')), page['response']['transport_bytes'])
                        focused = await session.call_tool('discover_formly_candidates',
                            dict(args, question_index=1, focus='claim', limit=3))
                        self.assertFalse(focused.isError)
                        focused_page = json.loads(focused.content[0].text)
                        self.assertEqual(expected, [f['id'] for f in focused_page['candidates']])
                        self.assertIn('focus_ref', focused_page)
                        self.assertLessEqual(encoded_size(focused.model_dump(mode='json')), MAX_TRANSPORT_BYTES)
                        for focus in (True, 2, '', 'x' * 501):
                            rejected = await session.call_tool('discover_formly_candidates', dict(args, focus=focus))
                            self.assertTrue(rejected.isError)
                        for index in (True, -1, 2):
                            rejected = await session.call_tool('discover_formly_candidates', dict(args, question_index=index))
                            self.assertTrue(rejected.isError)
                        broken = copy.deepcopy(plan)
                        broken['condition_bindings'] = [dict(condition='without beta', question_indexes=[0])]
                        result = await session.call_tool('discover_formly_candidates', dict(args,
                            request='alpha without beta', plan=broken, question_index=0))
                        self.assertTrue(result.isError)
                        self.assertEqual('needs_refinement', json.loads(result.content[0].text)['status'])
                        unsupported = copy.deepcopy(plan)
                        unsupported['library_constraints']['formly_version'] = '7.0.0'
                        result = await session.call_tool('discover_formly_candidates', dict(args,
                            plan=unsupported, formly_version='7.0.0', question_index=0))
                        packet = json.loads(result.content[0].text)
                        self.assertEqual('unsupported_scope', packet['status'])
                        self.assertNotIn('candidates', packet)


if __name__ == '__main__': unittest.main()

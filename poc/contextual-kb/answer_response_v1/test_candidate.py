"""Disposable fixture checks; never builds or modifies installed knowledge."""
import asyncio
import copy
import hashlib
import json
from pathlib import Path
import sqlite3
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

POC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(POC))
sys.path.insert(0, str(POC / 'model_free_v1'))
from model_free_v1.test_candidate import fixture, plan
from model_free_v1.candidate import Service, Store
from model_free_v1.response import encoded_size, transport_size, fits_packet
from model_free_repair_v1.feedback import RepairService
from answer_response_v1.candidate import AnswerService, bounded_packet, identity, answer_packet, excerpt_availability, stored_text_status
from answer_response_v1.serve import create_server, discover_with_repair


class AnswerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.path = self.root / 'db.sqlite'
        fixture(self.path)
        db = sqlite3.connect(self.path)
        self.record = dict(id='K1', kind='implementation', path='src/fixture.ts', lines=[3, 12],
                           url='https://example.invalid/pinned/src/fixture.ts#L3-L12',
                           sha256='original-sha', excerpt='full original excerpt', status='source-read')
        db.execute('INSERT INTO evidence VALUES (?,?)', ('K1', json.dumps(self.record)))
        db.execute('INSERT INTO fact_evidence VALUES (?,?)', ('target', 'K1'))
        db.commit(); db.close()
        self.sha = hashlib.sha256(self.path.read_bytes()).hexdigest()
        self.store = Store(self.path, self.sha)
        self.base = Service(self.store, self.root / 'baseline.sqlite')
        self.answer = AnswerService(self.store, self.root / 'candidate.sqlite')

    def tearDown(self):
        self.store.close()
        self.assertEqual(self.sha, hashlib.sha256(self.path.read_bytes()).hexdigest())
        self.temp.cleanup()

    def run_async(self, call):
        return asyncio.run(call)

    def test_answer_facts_lossless_and_citations_usable(self):
        base = self.run_async(self.base.get_facts(['target'], '6.3.12', 'core', 'full'))
        answer = self.run_async(self.answer.get_facts(['target'], '6.3.12', 'core'))
        self.assertEqual(base['facts'], answer['facts'])
        self.assertEqual('answer_facts', answer['record_kind'])
        self.assertEqual(self.record['url'], answer['citations']['target'][0]['url'])
        self.assertNotIn('excerpt', answer['citations']['target'][0])
        self.assertNotIn('sha256', answer['citations']['target'][0])
        self.assertTrue(answer['detailed_provenance']['facts_complete'])
        self.assertEqual('deferred', answer['detailed_provenance']['status'])

    def test_full_provenance_rejoins_exactly(self):
        base = self.run_async(self.base.get_facts(['target'], '6.3.12', 'core', 'full'))
        answer = self.run_async(self.answer.get_facts(['target'], '6.3.12', 'core'))
        details = self.run_async(self.answer.get_provenance(**answer['detailed_provenance']['arguments']))
        self.assertEqual(base['citations'], details['citations'])
        self.assertNotIn('facts', details)
        self.assertTrue(details['details_complete'])

    def test_lookup_selection_and_facts_unchanged(self):
        request = 'resetOnHide preserves model value'
        base = self.run_async(self.base.lookup(request, plan=plan(request)))
        answer = self.run_async(self.answer.lookup(request, plan=plan(request)))
        for key in ('facts', 'questions', 'omitted_candidates', 'omitted_count', 'truncated', 'retrieval'):
            self.assertEqual(base[key], answer[key], key)
        self.assertEqual('answer_facts', answer['record_kind'])

    def test_unknown_or_ineligible_id_rejects_entire_set(self):
        for ids in (['target', 'unknown'], ['target', 'material']):
            with self.assertRaises(ValueError):
                self.run_async(self.answer.get_facts(ids, '6.3.12', 'core'))
            with self.assertRaises(ValueError):
                self.run_async(self.answer.get_provenance(ids, '6.3.12', 'core'))

    def test_scope_must_repeat_resolved_exact_version(self):
        with self.assertRaises(ValueError):
            self.run_async(self.answer.get_provenance(['target'], '6', 'core'))
        packet = self.run_async(self.answer.get_provenance(['target'], '7', 'core'))
        self.assertEqual('unsupported_version', packet['status'])
        self.assertNotIn('citations', packet)

    def test_null_adapter_roundtrips_and_duplicates_deduplicate(self):
        answer = self.run_async(self.answer.get_facts(['target', 'target'], '6.3.12'))
        details = self.run_async(self.answer.get_provenance(**answer['detailed_provenance']['arguments']))
        self.assertEqual(['target'], details['fact_ids'])

    def test_explicit_baseline_formats_unchanged(self):
        for fmt in ('compact', 'full'):
            self.assertEqual(self.run_async(self.base.get_facts(['target'], '6.3.12', 'core', fmt)),
                             self.run_async(self.answer.get_facts(['target'], '6.3.12', 'core', fmt)))

    def test_budget_retries_deliver_all_without_partial_records(self):
        context = dict(version_context={'selected': '6.3.12'}, ui_adapter='core')
        def factory(ids, ctx):
            return dict(citations={fid: 'x' * 15000 for fid in ids}, **ctx)
        packet = bounded_packet(['a', 'b', 'a'], context, factory, 'get_formly_provenance')
        self.assertEqual('batch_required', packet['status'])
        self.assertEqual([], packet['facts'])
        self.assertEqual([['a'], ['b']], [row['arguments']['fact_ids'] for row in packet['retry_batches']])
        for row in packet['retry_batches']:
            value = bounded_packet(row['arguments']['fact_ids'], context, factory, row['tool'])
            self.assertEqual(row['response_bytes'], encoded_size(value))
            self.assertEqual(row['transport_bytes'], transport_size(value))
        huge = bounded_packet(['a'], context, lambda ids, ctx: {'huge': 'x' * 35000, **ctx}, 'get_formly_provenance')
        self.assertEqual('response_too_large', huge['status'])
        self.assertEqual(['a'], huge['unbatchable_fact_ids'])
        self.assertEqual([], huge['retry_batches'])

    def test_no_automatic_provenance_fetch(self):
        with patch.object(self.answer, 'get_provenance', side_effect=AssertionError('unexpected fetch')):
            self.run_async(self.answer.get_facts(['target'], '6.3.12', 'core'))

    def test_transport_schema_and_identity(self):
        server = create_server(RepairService(self.answer))
        tools = {tool.name: tool for tool in self.run_async(server.list_tools())}
        self.assertEqual({'lookup_formly', 'get_formly_facts', 'get_formly_provenance', 'discover_formly_candidates', 'help_formly'}, set(tools))
        schema = tools['get_formly_provenance'].inputSchema
        self.assertEqual(['fact_ids', 'formly_version', 'ui_adapter'], schema['required'])
        self.assertEqual('answer', tools['get_formly_facts'].inputSchema['properties']['response_format']['default'])
        self.assertTrue(identity()['build_id'].startswith('answer-response-v1+'))
        self.assertEqual(identity()['build_id'], server._mcp_server.version)


    def test_excerpt_presence_distinguishes_stored_text_and_authored_summary(self):
        for value in (None, '', ' ', '\n\t', 4, False):
            self.assertEqual('absent', stored_text_status(value))
        self.assertEqual('available', stored_text_status('  exact text\n'))
        _, citations = self.store.records(['target'], '6.3.12', 'core')
        records = [dict(self.record, id='available', excerpt=' source line '),
                   {k: v for k, v in dict(self.record, id='missing').items() if k != 'excerpt'},
                   dict(self.record, id='null', excerpt=None),
                   dict(self.record, id='blank', excerpt='  '),
                   dict(self.record, id='guide', kind='guide', excerpt='documentation text')]
        citations['target']['evidence'] = records
        original = copy.deepcopy(citations)
        facts, _ = self.store.records(['target'], '6.3.12', 'core')
        packet = dict(facts=facts, version_context={'selected': '6.3.12'}, ui_adapter='core')
        answer = answer_packet(packet, citations)
        self.assertEqual(['available', 'absent', 'absent', 'absent', 'available'],
                         [row['stored_excerpt'] for row in answer['citations']['target']])
        self.assertEqual('guide', answer['citations']['target'][-1]['kind'])
        availability = excerpt_availability(citations)['target']
        self.assertEqual('available', availability['authored_summary_quote'])
        self.assertEqual('implementation', availability['evidence'][0]['kind'])
        self.assertEqual(original, citations)
        self.assertEqual(packet['facts'], answer['facts'])

    def test_provenance_preserves_original_and_explains_absent_excerpt(self):
        _, original = self.store.records(['target', 'generic'], '6.3.12', 'core')
        details = self.run_async(self.answer.get_provenance(['target', 'generic'], '6.3.12', 'core'))
        self.assertEqual(original, details['citations'])
        self.assertEqual('available', details['excerpt_availability']['target']['evidence'][0]['stored_excerpt'])
        self.assertEqual([], details['excerpt_availability']['generic']['evidence'])
        self.assertIn('same IDs cannot add', details['excerpt_guidance'])
        self.assertIn('different relevant facts', details['excerpt_guidance'])
        self.assertIn('not proof that source text does not exist', details['excerpt_guidance'])

    def test_provenance_metadata_is_measured_in_retry_budget(self):
        facts, citations = self.store.records(['target', 'generic'], '6.3.12', 'core')
        for citation in citations.values():
            citation['authored_source']['quote'] = 'x' * 15000
        def records(ids, version, adapter):
            return [f for f in facts if f['id'] in ids], {fid: citations[fid] for fid in dict.fromkeys(ids)}
        with patch.object(self.store, 'records', side_effect=records):
            initial = self.run_async(self.answer.get_provenance(['target', 'generic'], '6.3.12', 'core'))
            self.assertEqual('batch_required', initial['status'])
            self.assertEqual([], initial['facts'])
            delivered = {}
            for row in initial['retry_batches']:
                retry = self.run_async(self.answer.get_provenance(**row['arguments']))
                self.assertEqual(row['response_bytes'], encoded_size(retry))
                self.assertEqual(row['transport_bytes'], transport_size(retry))
                delivered.update(retry['citations'])
            self.assertEqual(citations, delivered)


    def test_discovery_schema_requires_nonnull_plan(self):
        server = create_server(RepairService(self.answer))
        tools = {tool.name: tool for tool in self.run_async(server.list_tools())}
        schema = tools['discover_formly_candidates'].inputSchema
        self.assertIn('plan', schema['required'])
        self.assertNotIn('anyOf', schema['properties']['plan'])
        for arguments in ({'request': 'alpha'}, {'request': 'alpha', 'plan': None}):
            with self.assertRaises(Exception) as caught:
                self.run_async(server.call_tool('discover_formly_candidates', arguments))
            self.assertIn('plan', str(caught.exception))

    def test_legacy_missing_plan_feedback_stays_on_discovery(self):
        arguments = dict(formly_version='6.3.12', ui_adapter='core', offset=0,
                         limit=12, question_index=0, focus='alpha')
        preserved = copy.deepcopy(arguments)
        packet, error = self.run_async(discover_with_repair(
            RepairService(self.answer), 'alpha', None, **arguments))
        self.assertEqual('PLAN_REQUIRED', packet['issues'][0]['code'])
        self.assertEqual('discover_formly_candidates', packet['next_action']['tool'])
        self.assertEqual(['request', 'formly_version', 'ui_adapter', 'offset', 'limit',
                          'question_index', 'focus'], packet['next_action']['preserve_arguments'])
        self.assertEqual(preserved, arguments)
        repaired, error = self.run_async(discover_with_repair(
            RepairService(self.answer), 'alpha', plan('alpha'), **arguments))
        self.assertFalse(error)
        self.assertIn(repaired['status'], ('candidates', 'exhausted'))

    def test_valid_discovery_unchanged_and_plan_errors_keep_selectors(self):
        from parity_v1.discovery import discover
        service = RepairService(self.answer)
        arguments = dict(formly_version='6.3.12', ui_adapter='core', offset=0,
                         limit=16, question_index=0, focus='alpha')
        expected = self.run_async(discover(service, 'alpha', plan('alpha'), **arguments))
        actual = self.run_async(discover_with_repair(service, 'alpha', plan('alpha'), **arguments))
        self.assertEqual(expected, actual)
        invalid = plan('alpha', 'without beta')
        packet, error = self.run_async(discover_with_repair(service,
            'alpha without beta', invalid, **arguments))
        self.assertTrue(error)
        self.assertEqual('needs_refinement', packet['status'])
        self.assertEqual('discover_formly_candidates', packet['next_action']['tool'])
        self.assertIn('question_index', packet['next_action']['preserve_arguments'])
        self.assertEqual('MISSING_DECLARED_CONDITION', packet['issues'][0]['code'])

    def test_shared_source_still_allows_distinct_fact_provenance(self):
        _, citations = self.store.records(['target', 'generic'], '6.3.12', 'core')
        citations['generic']['evidence'] = copy.deepcopy(citations['target']['evidence'])
        def records(ids, version, adapter):
            return [], {fid: copy.deepcopy(citations[fid]) for fid in ids}
        with patch.object(self.store, 'records', side_effect=records):
            first = self.run_async(self.answer.get_provenance(['target'], '6.3.12', 'core'))
            second = self.run_async(self.answer.get_provenance(['generic'], '6.3.12', 'core'))
            self.assertEqual(first['citations']['target']['evidence'], second['citations']['generic']['evidence'])
            self.assertNotEqual(first['citations']['target']['authored_source']['quote'],
                                second['citations']['generic']['authored_source']['quote'])
            self.assertEqual(citations['generic'], second['citations']['generic'])


    def test_selection_first_preserves_real_ordered_discovery(self):
        from parity_v1.discovery import discover
        service = RepairService(self.answer)
        original_lookup = self.answer.lookup
        async def limited_lookup(*args, **kwargs):
            return await original_lookup(*args, max_facts=1, **kwargs)
        arguments = dict(formly_version='6.3.12', ui_adapter='core', offset=0,
                         limit=1, question_index=0, focus='alpha')
        with patch.object(self.answer, 'lookup', side_effect=limited_lookup):
            baseline, baseline_error = self.run_async(discover(service, 'alpha', plan('alpha'), **arguments))
            result, error = self.run_async(discover_with_repair(service, 'alpha', plan('alpha'), **arguments))
        self.assertFalse(error)
        self.assertEqual(baseline_error, error)
        self.assertTrue(result['candidates'])
        for key in baseline:
            if key not in ('next_action', 'response'):
                self.assertEqual(baseline[key], result[key], key)
        self.assertEqual(set(baseline), set(result))
        self.assertEqual(set(baseline['next_action']), set(result['next_action']))
        self.assertEqual('get_formly_facts', result['next_action']['tool'])
        self.assertIn('map unmet decisions', result['next_action']['message'])
        self.assertIn('examples support only demonstrated behavior', result['next_action']['message'])
        self.assertEqual(encoded_size(result), result['response']['bytes'])
        self.assertEqual(transport_size(result), result['response']['transport_bytes'])

    def test_selection_guidance_preserves_near_budget_packet(self):
        for focused in (False, True):
            message = ('candidates include claims/conditions/limits, not citation provenance. Fetch only relevant IDs not already fully delivered, in batches. Reuse known IDs without rediscovery. Page with the same request/plan/scope/selector; restart offset at zero when the selector changes.')
            if focused:
                message += (' Keep focus unchanged while paging; restart offset at zero when changing focus. Focus only reranks omissions, not scope/support; no match does not prove absence.')
            packet = dict(status='candidates', candidates=[dict(id='fixture', claim='',
                conditions=['Keep this condition'], limits=['Keep this limit'])],
                offset=3, next_offset=4, question_index=0,
                version_context={'selected': '6.3.12'}, ui_adapter='core',
                next_action=dict(type='assess_candidates_then_fetch', tool='get_formly_facts', message=message))
            if focused:
                packet['focus_ref'] = dict(sha256='fixed', characters=5)
            low, high = 0, 30000
            while low < high:
                mid = (low + high + 1) // 2
                packet['candidates'][0]['claim'] = 'x' * mid
                if fits_packet(packet): low = mid
                else: high = mid - 1
            packet['candidates'][0]['claim'] = 'x' * low
            self.assertTrue(fits_packet(packet))
            baseline = copy.deepcopy(packet)
            with patch('answer_response_v1.serve.discover', return_value=(packet, False)):
                result, error = self.run_async(discover_with_repair(None, 'request', {}))
            self.assertFalse(error)
            self.assertEqual(baseline['candidates'], result['candidates'])
            self.assertEqual(baseline['offset'], result['offset'])
            self.assertEqual(baseline['next_offset'], result['next_offset'])
            self.assertLessEqual(encoded_size(result), encoded_size(baseline))
            self.assertEqual(encoded_size(result), result['response']['bytes'])
            self.assertEqual(transport_size(result), result['response']['transport_bytes'])
            self.assertTrue(fits_packet(result))

    def test_selection_guidance_leaves_empty_exhausted_and_scope_errors_unchanged(self):
        for packet, error in [
                ({'status': 'exhausted', 'candidates': [], 'next_offset': None}, False),
                ({'status': 'candidates', 'candidates': [], 'next_action': {'message': 'unchanged'}}, False),
                ({'status': 'unsupported_scope', 'scope_status': 'unsupported_version'}, False)]:
            original = copy.deepcopy(packet)
            with patch('answer_response_v1.serve.discover', return_value=(packet, error)):
                result = self.run_async(discover_with_repair(None, 'request', {}))
            self.assertEqual((original, error), result)
        with patch('answer_response_v1.serve.discover', side_effect=ValueError('invalid selector')):
            with self.assertRaisesRegex(ValueError, 'invalid selector'):
                self.run_async(discover_with_repair(None, 'request', {}))


class IdentityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = identity()
        for relative in self.source['files']:
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(POC / relative, destination)

    def tearDown(self):
        self.temp.cleanup()

    def test_source_and_minimal_staged_identity_match(self):
        staged = identity(self.root)
        self.assertEqual(self.source, staged)
        self.assertIn('mcp_foundation/capitalization.py', staged['first_party_import_closure'])
        self.assertNotIn('build/knowledge.sqlite', staged['files'])
        self.assertFalse(any('/PLAN' in name for name in staged['files']))
        self.assertEqual('1.26.0', staged['expected_server_packages']['mcp'])

    def test_previously_omitted_dependency_mutation_fails_closed(self):
        path = self.root / 'mcp_foundation/capitalization.py'
        path.write_text(path.read_text() + '\n# changed dependency\n')
        with self.assertRaisesRegex(ValueError, 'Pinned runtime dependency changed'):
            identity(self.root)

    def test_missing_pinned_or_candidate_dependency_fails_closed(self):
        for relative in ('mcp_foundation/capitalization.py', 'answer_response_v1/identity.py'):
            path = self.root / relative
            original = path.read_bytes()
            path.unlink()
            with self.assertRaisesRegex(ValueError, 'Missing runtime|Unresolved runtime'):
                identity(self.root)
            path.write_bytes(original)

    def test_new_transitive_local_dependency_is_hashed(self):
        server = self.root / 'answer_response_v1/serve.py'
        server.write_text(server.read_text() + '\nimport added_helper\n')
        helper = self.root / 'added_helper.py'
        helper.write_text('VALUE = 1\n')
        first = identity(self.root)
        self.assertIn('added_helper.py', first['files'])
        helper.write_text('VALUE = 2\n')
        self.assertNotEqual(first['build_id'], identity(self.root)['build_id'])
        helper.unlink()
        with self.assertRaisesRegex(ValueError, 'Unresolved runtime import'):
            identity(self.root)

    def test_version_catalog_resource_is_hashed_and_required(self):
        self.assertIn('mcp_v1/versions.json', self.source['files'])
        self.assertEqual(['mcp_v1/versions.json'], self.source['runtime_resources'])
        path = self.root / 'mcp_v1/versions.json'
        original = path.read_bytes()
        path.write_bytes(original + b'\n')
        self.assertNotEqual(self.source['build_id'], identity(self.root)['build_id'])
        path.unlink()
        with self.assertRaisesRegex(ValueError, 'Missing runtime identity dependency'):
            identity(self.root)

    def test_minimal_stage_constructs_real_version_resolver(self):
        command = [sys.executable, '-I', '-c',
                   'import sys; sys.path.insert(0, sys.argv[1]); '
                   'from mcp_v1.versioning import VersionResolver; '
                   'print(VersionResolver().resolve("6.3.12")["selected"])', str(self.root)]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        self.assertEqual('6.3.12', result.stdout.strip())
        (self.root / 'mcp_v1/versions.json').unlink()
        failed = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(0, failed.returncode)
        self.assertIn('versions.json', failed.stderr)

    def test_dynamic_dependency_loading_requires_review(self):
        server = self.root / 'answer_response_v1/serve.py'
        server.write_text(server.read_text() + '\n__import__("new_module")\n')
        with self.assertRaisesRegex(ValueError, 'Dynamic runtime loading'):
            identity(self.root)


if __name__ == '__main__':
    unittest.main()

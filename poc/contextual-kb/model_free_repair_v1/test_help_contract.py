import asyncio
import json
from pathlib import Path
import sys
import unittest

POC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(POC))
sys.path.insert(0, str(POC / 'model_free_v1'))
from model_free_v1.help import EXAMPLE, help_packet
from model_free_v1.server import QuestionPlan, create_server as original_server
from model_free_repair_v1.feedback import plan_issues
from model_free_repair_v1.serve import create_server
from parity_v1.serve_discovery import create_discovery_server
from mcp.server.fastmcp.exceptions import ToolError
from model_free_v1.response import MAX_RESPONSE_BYTES, MAX_TRANSPORT_BYTES, encoded_size


class Store:
    def __init__(self):
        self.verified = 0
        self.facts = {'core/a': {'title': 'Core'}, 'core/b': {'title': 'Core'},
                      'material/a': {'title': 'Material'}}
    def verify(self): self.verified += 1
    def close(self): pass
    def scopes(self, version, adapter):
        return {fid: [] for fid in self.facts if adapter != 'core' or fid.startswith('core/')}


class Gate:
    def __init__(self): self.calls = 0
    async def lookup(self, request, formly_version=None, ui_adapter=None):
        self.calls += 1
        if formly_version == '7': return {'status': 'unsupported_version'}
        return {'version_context': {'selected': '6.3.12'}, 'ui_adapter': ui_adapter}


class Service:
    def __init__(self):
        self.store = Store()
        self.gate = Gate()
        self.base = self


class HelpContractTests(unittest.TestCase):
    def test_handshake_and_help_report_same_runtime_build_not_sdk_version(self):
        server = create_server(Service())
        initialized = server._mcp_server.create_initialization_options()
        result = asyncio.run(server.call_tool('help_formly', {}))
        packet = json.loads(result.content[0].text)
        identity = packet['build_identity']
        self.assertEqual(identity['build_id'], initialized.server_version)
        self.assertTrue(identity['runtime_id'].startswith('formly-model-free-'))
        self.assertIsNone(identity['release'])
        unsupported = asyncio.run(server.call_tool('help_formly', {'formly_version': '7'}))
        self.assertEqual(identity, json.loads(unsupported.content[0].text)['build_identity'])

    def test_example_has_required_fields_and_exact_bindings(self):
        QuestionPlan.model_validate(EXAMPLE['plan'])
        self.assertEqual([], plan_issues(EXAMPLE['request'], EXAMPLE['plan']))

    def test_schema_exposes_copy_rule_and_fetch_count(self):
        for factory in (create_server, original_server):
            with self.subTest(factory=factory.__module__):
                schemas = {tool.name: tool for tool in asyncio.run(factory(Service()).list_tools())}
                binding = schemas['lookup_formly'].inputSchema['$defs']['Binding']['properties']['condition']
                self.assertIn('exact excerpt', binding['description'])
                fetch = schemas['get_formly_facts'].inputSchema['properties']['fact_ids']
                self.assertEqual((1, 16), (fetch['minItems'], fetch['maxItems']))
                self.assertIn('help_formly', schemas)
                self.assertIn('response_format', schemas['get_formly_facts'].inputSchema['properties'])

    def test_help_schema_advertises_enforced_bounds_on_all_model_free_servers(self):
        for factory in (original_server, create_server, create_discovery_server):
            with self.subTest(factory=factory.__module__):
                tool = next(t for t in asyncio.run(factory(Service()).list_tools()) if t.name == 'help_formly')
                props = tool.inputSchema['properties']
                self.assertEqual((0, 0), (props['offset']['minimum'], props['offset']['default']))
                self.assertEqual((1, 32, 16), (props['limit']['minimum'], props['limit']['maximum'], props['limit']['default']))
                topic = next(branch for branch in props['topic']['anyOf'] if branch.get('type') == 'string')
                self.assertEqual((1, 300), (topic['minLength'], topic['maxLength']))
                self.assertIn('next_offset', props['limit']['description'])

    def test_mcp_help_rejects_invalid_pages_before_service_and_accepts_boundaries(self):
        invalid = ({'offset': -1}, {'limit': 0}, {'limit': 33}, {'limit': 40},
                   {'limit': 50}, {'limit': 100}, {'limit': True}, {'offset': 1.5},
                   {'topic': ''}, {'topic': 'x' * 301})
        for factory in (original_server, create_server, create_discovery_server):
            service = Service()
            server = factory(service)
            for args in invalid:
                with self.subTest(factory=factory.__module__, args=args), self.assertRaises(ToolError):
                    asyncio.run(server.call_tool('help_formly', args))
            self.assertEqual(0, service.gate.calls)
            self.assertEqual(0, service.store.verified)
            for args in ({'offset': 0, 'limit': 1}, {'limit': 32}, {'offset': 300}):
                asyncio.run(server.call_tool('help_formly', args))
            self.assertEqual(3, service.gate.calls)
            self.assertEqual(6, service.store.verified)

    def test_topic_inventory_is_scoped_and_pages_complete_ids(self):
        service = Service()
        packet = asyncio.run(help_packet(service, ui_adapter='core'))
        self.assertEqual([{'topic': 'core', 'fact_count': 2}], packet['topics'])
        packet = asyncio.run(help_packet(service, 'core', ui_adapter='core', limit=1))
        self.assertEqual(['core/a'], [f['id'] for f in packet['facts']])
        self.assertEqual(1, packet['next_offset'])
        packet = asyncio.run(help_packet(service, 'core', ui_adapter='core', offset=1, limit=1))
        self.assertEqual(['core/b'], [f['id'] for f in packet['facts']])
        self.assertIsNone(packet['next_offset'])
        self.assertEqual(6, service.store.verified)

    def test_full_help_guidance_keeps_catalogue_pages_complete_within_transport_budget(self):
        service = Service()
        service.store.facts = {f'topic-{i:02}/fact': {'title': 'Synthetic topic'} for i in range(40)}
        server = create_discovery_server(service)
        seen = []
        offset = 0
        while offset is not None:
            result = asyncio.run(server.call_tool('help_formly', {'offset': offset, 'limit': 32}))
            self.assertFalse(result.isError)
            packet = json.loads(result.content[0].text)
            self.assertLessEqual(encoded_size(packet), MAX_RESPONSE_BYTES)
            self.assertLessEqual(encoded_size(result.model_dump(mode='json')), MAX_TRANSPORT_BYTES)
            self.assertTrue(packet['workflow'])
            self.assertEqual(40, packet['total_topics'])
            seen.extend(row['topic'] for row in packet['topics'])
            offset = packet['next_offset']
        self.assertEqual([f'topic-{i:02}' for i in range(40)], seen)
        self.assertEqual(2, service.gate.calls)

    def test_unknown_topic_does_not_expand_scope(self):
        packet = asyncio.run(help_packet(Service(), 'material', ui_adapter='core'))
        self.assertEqual('unknown_topic', packet['status'])
        self.assertEqual([], packet['facts'])
        packet = asyncio.run(help_packet(Service(), formly_version='7'))
        self.assertEqual({'status': 'unsupported_version'}, packet)

    def test_missing_condition_shows_comparison(self):
        plan = {'formly_questions': [{'question': 'alpha', 'reason': 'test'}],
                'library_constraints': {'formly_version': None, 'ui_adapter': None},
                'condition_bindings': [{'condition': 'without beta', 'question_indexes': [0]}]}
        error = plan_issues('alpha without beta', plan)[0]
        self.assertEqual('alpha', error['question'])
        self.assertEqual('without beta', error['condition'])
        self.assertIn('Copy this condition exactly', error['message'])

    def test_help_bounds_before_retrieval(self):
        for kwargs in ({'offset': -1}, {'limit': 0}, {'limit': 33}, {'topic': ''}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                asyncio.run(help_packet(Service(), **kwargs))


if __name__ == '__main__': unittest.main()

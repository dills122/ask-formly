import asyncio
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
    async def lookup(self, request, formly_version=None, ui_adapter=None):
        if formly_version == '7': return {'status': 'unsupported_version'}
        return {'version_context': {'selected': '6.3.12'}, 'ui_adapter': ui_adapter}


class Service:
    def __init__(self):
        self.store = Store()
        self.gate = Gate()
        self.base = self


class HelpContractTests(unittest.TestCase):
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

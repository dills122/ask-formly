import copy
import tempfile
import unittest
from pathlib import Path

from probe import load_development, validate_spans, check_access, observe


class ProbeTests(unittest.TestCase):
    def test_source_offsets_preserve_unicode_and_code(self):
        question = '🧭 use options.formState'
        span = {'text': 'options.formState', 'start': 6, 'end': 23}
        result = {'entities': {'identifier': [span]}, 'relation_extraction': {
            'context_for': [{'head': span, 'tail': span}]}}
        original = copy.deepcopy(result)
        self.assertEqual(validate_spans(question, result), 3)
        self.assertEqual(result, original)

    def test_bad_offsets_or_rewritten_text_rejected(self):
        for span in [{'text': 'foo', 'start': -1, 'end': 3},
                     {'text': 'bar', 'start': 0, 'end': 3},
                     {'text': 'foo', 'start': 0, 'end': 4},
                     {'text': 'foo'}, {'text': 'foo', 'start': False, 'end': 3}]:
            with self.subTest(span=span), self.assertRaises(ValueError):
                validate_spans('foo', {'entities': {'identifier': [span]}})

    def test_relation_endpoints_must_have_source_spans(self):
        with self.assertRaises(ValueError):
            validate_spans('foo', {'relation_extraction': {
                'context_for': [{'head': {'text': 'foo'}, 'tail': 'foo'}]}})

    def test_only_frozen_development_file_is_accepted(self):
        cases = load_development()
        self.assertEqual([c['id'] for c in cases], [f'D{i:02}' for i in range(1,13)])
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                load_development(Path(d)/'heldout.json')

    def test_network_and_protected_reads_rejected(self):
        for event, args in [('socket.connect', (None, ('localhost', 80))),
                            ('sqlite3.connect', ('memory',)),
                            ('open', ('poc/contextual-kb/authored/a.json', 'r', 0)),
                            ('open', ('poc/contextual-kb/planner_cases/sealed/a.json', 'r', 0))]:
            with self.subTest(event=event,args=args), self.assertRaises(PermissionError):
                check_access(event,args)

    def test_probe_can_read_its_model(self):
        check_access('open', ('poc/contextual-kb/gliner_feasibility/models/config.json','r',0))

    def test_native_result_is_retained_when_validation_fails(self):
        result = {'entities': {'identifier': [{'text': 'changed', 'start': 0, 'end': 3}]}}
        row = observe('foo', lambda: result)
        self.assertEqual(row['native'], result)
        self.assertEqual(row['error']['type'], 'ValueError')
        self.assertGreaterEqual(row['seconds'], 0)

    def test_backend_error_retained_without_retry(self):
        calls = []
        def fail():
            calls.append(1)
            raise RuntimeError('backend failed')
        row = observe('foo', fail)
        self.assertEqual(len(calls), 1)
        self.assertEqual(row['error']['message'], 'backend failed')
        self.assertNotIn('native', row)


if __name__ == '__main__':
    unittest.main()

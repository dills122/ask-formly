import json
from pathlib import Path
import tempfile
import unittest
import execution


class ExecutionTests(unittest.TestCase):
    def test_short_duplicate_reordered_or_wrong_ids_fail_all_slots(self):
        packet = {'requests': [{'id': 'a'}, {'id': 'b'}]}
        for rows in ([], [{'id': 'a', 'output': {}}],
                     [{'id': 'a', 'output': {}}, {'id': 'a', 'output': {}}],
                     [{'id': 'b', 'output': {}}, {'id': 'a', 'output': {}}],
                     [{'id': 'a', 'output': {}}, {'id': 'c', 'output': {}}]):
            with self.subTest(rows=rows):
                records, error = execution.account(packet, json.dumps(rows))
                self.assertIsNotNone(error)
                self.assertEqual(records, [{'id': 'a', 'output': None}, {'id': 'b', 'output': None}])

    def test_malformed_duplicate_key_missing_and_extra_fields_fail_whole_packet(self):
        packet = {'requests': [{'id': 'a'}]}
        for text in (None, '[', '[{"id":"a","id":"a","output":{}}]',
                     '[{"id":"a"}]', '[{"id":"a","output":{},"extra":1}]',
                     '[{"id":"a","output":NaN}]'):
            with self.subTest(text=text):
                rows, error = execution.account(packet, text)
                self.assertIsNotNone(error)
                self.assertEqual(rows, [{'id': 'a', 'output': None}])

    def test_semantic_defects_survive_valid_envelope(self):
        packet = {'requests': [{'id': 'a'}]}
        rows = [{'id': 'a', 'output': {'condition_bindings': []}}]
        self.assertEqual(execution.account(packet, json.dumps(rows)), (rows, None))

    def test_load_attempt_checks_receipts_and_whole_packet(self):
        for failure in ('none', 'source', 'output', 'receipt', 'short'):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                packet, source, attempt = root / 'packet.json', root / 'first.literal', root / 'attempt'
                packet.write_text('{"requests":[{"id":"a"},{"id":"b"}]}')
                source.write_text("[{'id':'a','output':{}}]" if failure == 'short' else "[{'id':'a','output':{}},{'id':'b','output':{}}]")
                execution.execute(packet, source, attempt)
                if failure == 'source':
                    source.write_text('[]')
                elif failure == 'output':
                    (attempt / 'output.json').write_text('[]')
                elif failure == 'receipt':
                    (attempt / 'first-save.json').unlink()
                rows, error = execution.load_attempt(packet, source, attempt)
                if failure == 'none':
                    self.assertIsNone(error)
                    self.assertEqual([r['output'] for r in rows], [{}, {}])
                else:
                    self.assertIsNotNone(error)
                    self.assertEqual(rows, [{'id': 'a', 'output': None}, {'id': 'b', 'output': None}])

    def test_one_shot_success_records_original_hashes_and_blocks_rerun(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            packet = root / 'packet.json'
            source = root / 'first.literal'
            attempt = root / 'attempt'
            packet.write_text('{"requests":[{"id":"a"}]}')
            source.write_text("[{'id':'a','output':{}}]")
            result = execution.execute(packet, source, attempt)
            self.assertEqual(result['returncode'], 0)
            self.assertEqual(result['source_before'], result['source_after'])
            self.assertEqual(json.loads((attempt / 'output.json').read_text()), [{'id': 'a', 'output': {}}])
            initial = (attempt / 'first-save.json').read_bytes()
            output = (attempt / 'output.json').read_bytes()
            with self.assertRaises(FileExistsError):
                execution.execute(packet, source, attempt)
            self.assertEqual((attempt / 'first-save.json').read_bytes(), initial)
            self.assertEqual((attempt / 'output.json').read_bytes(), output)

    def test_failed_execution_retains_error_and_cannot_be_retried(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            packet = root / 'packet.json'
            source = root / 'first.literal'
            attempt = root / 'attempt'
            packet.write_text('{"requests":[{"id":"a"}]}')
            source.write_text('[')
            result = execution.execute(packet, source, attempt)
            self.assertNotEqual(result['returncode'], 0)
            self.assertTrue((attempt / 'stderr.txt').read_text())
            self.assertFalse((attempt / 'output.json').exists())
            self.assertEqual(source.read_text(), '[')
            with self.assertRaises(FileExistsError):
                execution.execute(packet, source, attempt)


if __name__ == '__main__':
    unittest.main()

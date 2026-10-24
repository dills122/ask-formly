"""Exercise the actual fixed runner from an unrelated working directory."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

RUNNER = Path(__file__).with_name('runner.py').resolve()


class RunnerTests(unittest.TestCase):
    def run_literal(self, folder, literal, output='result.json'):
        source = folder / 'first.literal'
        source.write_text(literal, encoding='utf-8')
        before = source.read_bytes()
        result = subprocess.run(
            [sys.executable, '-B', str(RUNNER), str(source), str(folder / output)],
            cwd=folder, capture_output=True, text=True,
        )
        self.assertEqual(source.read_bytes(), before)
        return result, folder / output

    def test_absolute_cli_from_unrelated_cwd_preserves_first_object(self):
        rows = [{'id': 'example', 'output': {'quoted': '"\\\n☃', 'flag': False, 'value': None}}]
        with tempfile.TemporaryDirectory() as directory:
            result, output = self.run_literal(Path(directory), repr(rows))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(output.read_text()), rows)

    def test_semantic_defects_are_not_filtered_or_fixed(self):
        rows = [{'id': 'wrong', 'output': {'condition_bindings': []}}, {'id': 'wrong', 'output': None}]
        with tempfile.TemporaryDirectory() as directory:
            result, output = self.run_literal(Path(directory), repr(rows))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(output.read_text()), rows)

    def test_existing_output_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            (folder / 'result.json').write_text('first retained bytes')
            result, output = self.run_literal(folder, '[]')
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_text(), 'first retained bytes')

    def test_python_expression_is_never_executed(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            marker = folder / 'executed'
            result, output = self.run_literal(folder, f"__import__('pathlib').Path({str(marker)!r}).touch()")
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(marker.exists())
            self.assertFalse(output.exists())

    def test_malformed_nonlist_and_nonjson_values_fail_without_output(self):
        for literal in ('[', '{}', '[{1, 2}]', '[1e999]'):
            with self.subTest(literal=literal), tempfile.TemporaryDirectory() as directory:
                result, output = self.run_literal(Path(directory), literal)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(output.exists())

    def test_first_literal_can_never_be_used_as_output_path(self):
        with tempfile.TemporaryDirectory() as directory:
            result, source = self.run_literal(Path(directory), '[]', output='first.literal')
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(source.read_text(), '[]')


if __name__ == '__main__':
    unittest.main()

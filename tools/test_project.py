import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('project', ROOT / 'tools/project.py')
project = importlib.util.module_from_spec(spec)
spec.loader.exec_module(project)

class SourceGuardTests(unittest.TestCase):
    def test_unchanged_files_pass_but_drift_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / 'fact.json'
            path.write_bytes(b'original')
            manifest = {'fact.json': hashlib.sha256(b'original').hexdigest()}
            project.verify_files(root, manifest)
            path.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'fact.json'):
                project.verify_files(root, manifest)

    def test_missing_file_cannot_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'missing.json'):
                project.verify_files(Path(tmp), {'missing.json': '0' * 64})

    def test_manifest_cannot_escape_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ('../outside', '/tmp/outside'):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    project.verify_files(Path(tmp), {name: '0' * 64})

class SourceSuiteWiringTests(unittest.TestCase):
    def test_source_checks_schedule_admission_and_promotion_fixture_suites_only(self):
        # Keep real source validation and command construction. Intercept only
        # subprocess execution to avoid recursively invoking this very suite.
        with patch.object(project.subprocess, 'run') as execution:
            project.source_checks()
        commands = [call.args[0] for call in execution.call_args_list]
        expected = [
            ('tools', 'test_project.py'),
            ('poc/contextual-kb/tests', 'test_pipeline.py'),
            ('poc/contextual-kb/tests', 'test_structured_source.py'),
            ('poc/contextual-kb/packaging', 'test_bundle.py'),
            ('poc/contextual-kb/knowledge-expansion/admission', 'test_*.py'),
            ('poc/contextual-kb/knowledge-expansion/promotion-v3', 'test_*.py'),
            ('poc/contextual-kb/knowledge-expansion/promotion-v4', 'test_*.py'),
            ('poc/contextual-kb/knowledge-expansion/promotion-v5', 'test_*.py'),
            ('poc/contextual-kb/knowledge-expansion/promotion-v6', 'test_*.py'),
            ('poc/contextual-kb/knowledge-expansion/validation-v1', 'test_candidate.py'),
            ('poc/contextual-kb/knowledge-expansion/validation-v1', 'test_evaluate.py'),
            ('poc/contextual-kb/knowledge-expansion/combined-v2', 'test_run.py'),
            ('poc/contextual-kb/mcp_v1', 'test_project_context.py'),
        ]
        self.assertEqual(len(commands), len(expected))
        for command, (folder, pattern) in zip(commands, expected):
            self.assertEqual(command[1:], ['-B', '-m', 'unittest', 'discover',
                '-s', str(ROOT / folder), '-p', pattern])
        for call in execution.call_args_list:
            self.assertEqual(call.kwargs, {'cwd': project.POC, 'check': True})


if __name__ == '__main__':
    unittest.main()

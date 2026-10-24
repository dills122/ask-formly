import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

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

if __name__ == '__main__':
    unittest.main()

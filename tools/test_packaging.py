import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile
from project import ROOT,build,digest

class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        shutil.copytree(ROOT/'skill',self.root/'skill');shutil.copy2(ROOT/'package.json',self.root/'package.json')
    def test_bundle_determinism_inventory_and_hashes(self):
        archive=build(self.root);first=archive.read_bytes();self.assertEqual(first,build(self.root).read_bytes())
        manifest=json.loads(archive.with_suffix('.manifest.json').read_text())
        with zipfile.ZipFile(archive) as bundle:
            self.assertEqual(set(bundle.namelist()),set(manifest['files']))
            for name in bundle.namelist():self.assertEqual(digest(bundle.read(name)),manifest['files'][name])
        self.assertEqual(digest(first),manifest['archive_sha256'])
        self.assertFalse(any('/qualification/' in p or '/node_modules/' in p for p in manifest['files']))
    def test_symlink_input_refused(self):
        (self.root/'skill/ask-formly/outside').symlink_to(ROOT/'tests',target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'Symlinks'):build(self.root)
    def test_missing_entrypoint_refused(self):
        (self.root/'skill/ask-formly/SKILL.md').unlink()
        with self.assertRaisesRegex(ValueError,'Missing required'):build(self.root)

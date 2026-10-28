import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import install
import package

class AlphaTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.source=self.root/'source';self.source.mkdir()
        for name,data in {'ask_formly.py':'print("fixture")','requirements.lock':'','runtime/build/knowledge.sqlite':'frozen-db'}.items():
            p=self.source/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data)
        self.files={str(p.relative_to(self.source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in self.source.rglob('*') if p.is_file()}
        self.manifest()
    def manifest(self):
        (self.source/'ALPHA-MANIFEST.json').write_text(json.dumps({'format':1,'files':self.files}))
    def test_verified_copy_is_independent_and_db_identical(self):
        target=self.root/'installed';install.stage(self.source,target)
        self.assertEqual((self.source/'runtime/build/knowledge.sqlite').read_bytes(),(target/'runtime/build/knowledge.sqlite').read_bytes())
        self.assertFalse((target/'runtime/build/knowledge.sqlite').is_symlink())
    def test_tampered_file_rejects_before_destination_creation(self):
        (self.source/'ask_formly.py').write_text('tampered')
        with self.assertRaisesRegex(ValueError,'hash'):install.stage(self.source,self.root/'installed')
        self.assertFalse((self.root/'installed').exists())
    def test_existing_destination_and_symlink_are_never_overwritten(self):
        target=self.root/'installed';target.mkdir();(target/'keep').write_text('keep')
        with self.assertRaises(FileExistsError):install.stage(self.source,target)
        self.assertEqual('keep',(target/'keep').read_text())
        link=self.root/'link';link.symlink_to(target)
        with self.assertRaises(FileExistsError):install.stage(self.source,link)
    def test_unsafe_or_private_manifest_paths_reject(self):
        for name in ('../outside','/absolute','runtime/evaluation/case.json','runtime/models/model.bin','runtime/test-output/run.json','runtime/.venv/a.py'):
            with self.subTest(name=name):
                self.files[name]='0'*64;self.manifest()
                with self.assertRaises(ValueError):install.verify(self.source)
                del self.files[name]
    def test_symlink_source_rejected(self):
        p=self.source/'ask_formly.py';p.unlink();p.symlink_to(self.source/'requirements.lock')
        self.files['ask_formly.py']=hashlib.sha256(b'').hexdigest();self.manifest()
        with self.assertRaisesRegex(ValueError,'symlink'):install.verify(self.source)
    def test_unlisted_file_is_not_installed(self):
        (self.source/'private.txt').write_text('private')
        target=self.root/'installed';install.stage(self.source,target)
        self.assertFalse((target/'private.txt').exists())
    def test_failed_dependency_install_removes_only_new_destination(self):
        with patch('install.venv.EnvBuilder.create'),patch('install.subprocess.run',side_effect=RuntimeError('download failed')):
            with self.assertRaisesRegex(RuntimeError,'download failed'):install.install(self.source,self.root/'installed')
        self.assertFalse((self.root/'installed').exists());self.assertTrue(self.source.exists())
    def test_package_rejects_modified_pinned_runtime(self):
        poc=self.root/'poc';(poc/'mcp_runtime').mkdir(parents=True)
        (poc/'mcp_runtime/model-free.json').write_text(json.dumps({'files':{'build/knowledge.sqlite':'0'*64}}))
        (poc/'build').mkdir();(poc/'build/knowledge.sqlite').write_text('wrong')
        with self.assertRaisesRegex(ValueError,'hash'):package.runtime_files(poc)

    def test_version_catalog_is_required_and_pinned(self):
        poc=self.root/'poc';(poc/'mcp_runtime').mkdir(parents=True)
        (poc/'mcp_runtime/model-free.json').write_text(json.dumps({'files':{}}))
        (poc/'mcp_runtime/launcher.py').write_text('launcher')
        with self.assertRaises(FileNotFoundError):package.runtime_files(poc)
        (poc/'mcp_v1').mkdir();(poc/'mcp_v1/versions.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'hash'):package.runtime_files(poc)

    def test_archive_is_deterministic_allowlisted_and_verifiable(self):
        import tarfile
        with patch('package.runtime_files',return_value={'runtime/build/knowledge.sqlite':b'frozen-db'}):
            one=self.root/'one.tar.gz';two=self.root/'two.tar.gz'
            package.build(one);package.build(two)
        self.assertEqual(one.read_bytes(),two.read_bytes())
        unpacked=self.root/'unpacked';unpacked.mkdir()
        with tarfile.open(one) as archive:
            self.assertTrue(all(m.isfile() and m.name.startswith('ask-formly-alpha/') for m in archive.getmembers()))
            archive.extractall(unpacked,filter='data')
        manifest=install.verify(unpacked/'ask-formly-alpha')
        self.assertEqual(b'frozen-db',(unpacked/'ask-formly-alpha/runtime/build/knowledge.sqlite').read_bytes())
        self.assertIn('THIRD_PARTY_NOTICES.md',manifest['files'])
        self.assertIn('Copyright (c) 2016 FormlyJS',(unpacked/'ask-formly-alpha/THIRD_PARTY_NOTICES.md').read_text())
        self.assertIn('LICENSE',manifest['files'])
        self.assertIn('ask-formly contributors',(unpacked/'ask-formly-alpha/LICENSE').read_text())
        self.assertEqual(8,len(manifest['files']))
        with self.assertRaises(FileExistsError):package.build(one)

if __name__=='__main__':unittest.main()

import hashlib,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch,Mock
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import launcher

class LauncherTests(unittest.TestCase):
    def test_pin_verification_detects_missing_and_drift(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'one').write_bytes(b'original')
            pins={'one':hashlib.sha256(b'original').hexdigest()}
            self.assertEqual(launcher.verify_files(root,pins),[])
            (root/'one').write_bytes(b'changed')
            self.assertIn('hash mismatch',launcher.verify_files(root,pins)[0])
            (root/'one').unlink();self.assertIn('missing',launcher.verify_files(root,pins)[0])
    def test_manifest_paths_cannot_escape_poc(self):
        with tempfile.TemporaryDirectory() as d:
            for name in ('../elsewhere','/tmp/elsewhere'):
                self.assertIn('outside POC',launcher.verify_files(Path(d),{name:'x'})[0])
    def test_doctor_does_not_start_service(self):
        with patch.object(launcher,'preflight',return_value={'ok':True,'errors':[]}),patch.object(launcher,'start') as start,patch('builtins.print'):
            self.assertEqual(launcher.main(['doctor']),0);start.assert_not_called()
    def test_failed_preflight_blocks_start(self):
        with patch.object(launcher,'preflight',return_value={'ok':False,'errors':['missing DB']}),patch.object(launcher,'start') as start,patch('builtins.print'):
            self.assertEqual(launcher.main(['serve']),2);start.assert_not_called()
    def test_default_and_explicit_seed_wiring(self):
        for args,seed in [(['serve'],1701),(['serve','--seed','1702'],1702)]:
            with patch.object(launcher,'preflight',return_value={'ok':True,'errors':[]}),patch.object(launcher,'start') as start:
                self.assertEqual(launcher.main(args),0);self.assertEqual(start.call_args.args[0].seed,seed)
    def test_invalid_seed_rejected(self):
        with self.assertRaises(SystemExit):launcher.main(['serve','--seed','42'])
    def test_preflight_missing_codex_is_clear(self):
        with patch.object(launcher,'verify_files',return_value=[]),patch.object(launcher.shutil,'which',return_value=None):
            result=launcher.preflight();self.assertFalse(result['ok']);self.assertTrue(any('codex' in e for e in result['errors']))

if __name__=='__main__':unittest.main()

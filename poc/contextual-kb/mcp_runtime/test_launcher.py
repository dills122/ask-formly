import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import launcher


class LauncherTests(unittest.TestCase):
    def test_default_starts_only_model_free(self):
        with patch.object(launcher,'model_free_preflight',return_value={'ok':True}), patch.object(launcher,'start_model_free') as free, patch.object(launcher,'run_model_backed') as backed:
            self.assertEqual(launcher.main(['serve']),0)
            free.assert_called_once();backed.assert_not_called()

    def test_explicit_backed_preserves_seed_and_command(self):
        with patch.object(launcher,'run_model_backed',return_value=7) as backed, patch.object(launcher,'model_free_preflight') as free:
            self.assertEqual(launcher.main(['doctor','--mode','model-backed','--seed','1702']),7)
            self.assertEqual(backed.call_args.args[0].seed,1702)
            self.assertEqual(backed.call_args.args[0].command,'doctor');free.assert_not_called()

    def test_model_flags_rejected_in_free_mode(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            launcher.main(['serve','--seed','1701'])

    def test_failed_free_preflight_never_falls_back(self):
        with patch.object(launcher,'model_free_preflight',return_value={'ok':False,'errors':['missing DB']}), patch.object(launcher,'start_model_free') as free, patch.object(launcher,'run_model_backed') as backed, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(launcher.main(['serve']),2)
            free.assert_not_called();backed.assert_not_called()

    def test_invalid_mode_fails(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            launcher.main(['serve','--mode','auto'])

    def test_pin_verification_rejects_drift_missing_and_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);p=root/'asset';p.write_text('good')
            pins={'asset':hashlib.sha256(p.read_bytes()).hexdigest()}
            self.assertEqual(launcher.verify_files(root,pins),[])
            p.write_text('bad');self.assertIn('hash mismatch',launcher.verify_files(root,pins)[0])
            p.unlink();self.assertIn('missing',launcher.verify_files(root,pins)[0])
            self.assertIn('outside',launcher.verify_files(root,{'../asset':'x'})[0])

    def test_model_free_doctor_only_requires_declared_server_packages(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);p=root/'data';p.write_bytes(b'database')
            manifest={'id':'fixture-runtime','files':{'data':hashlib.sha256(p.read_bytes()).hexdigest()},'server_packages':{'mcp':'1.0'}}
            with patch.object(launcher.metadata,'version',return_value='1.0') as version:
                report=launcher.model_free_preflight(root,manifest)
            self.assertTrue(report['ok']);self.assertEqual(report['mode'],'model-free')
            self.assertEqual('fixture-runtime',report['build_identity']['runtime_id'])
            self.assertNotEqual('1.0',report['build_identity']['build_id'])
            version.assert_called_once_with('mcp')
            with patch.object(launcher.metadata,'version',side_effect=launcher.metadata.PackageNotFoundError):
                self.assertFalse(launcher.model_free_preflight(root,manifest)['ok'])

    def test_identity_tracks_payload_not_json_key_order(self):
        one = {'id': 'fixture', 'files': {'a': 'digest'}}
        reordered = {'files': {'a': 'digest'}, 'id': 'fixture'}
        self.assertEqual(launcher.build_identity(one), launcher.build_identity(reordered))
        changed = {'id': 'fixture', 'files': {'a': 'other-digest'}}
        self.assertNotEqual(launcher.build_identity(one)['build_id'], launcher.build_identity(changed)['build_id'])


if __name__=='__main__':unittest.main()

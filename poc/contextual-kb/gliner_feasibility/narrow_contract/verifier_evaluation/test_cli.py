"""Real CLI control flow with filesystem artifacts and no model/process execution."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import cli

class Tests(unittest.TestCase):
    def invoke(self,root,args):
        with patch.object(cli,'OUT',root/'out'),patch.object(cli,'HERE',root),patch.object(cli,'code_binding',return_value={}),patch.object(cli,'protect',return_value=[]),patch('sys.argv',['cli.py',*args]):
            cli.main()
    def directory(self):
        return tempfile.TemporaryDirectory(dir=cli.HERE/'test-output')
    def test_invalid_seal_fails_before_native_preflight(self):
        with self.directory() as d:
            root=Path(d);(root/'out').mkdir();(root/'sealed').mkdir();fresh=root/'sealed/fresh.json';fresh.write_text('[]')
            fresh.with_suffix('.review.json').write_text(json.dumps(dict(verdict='ready',fresh_sha256=cli.digest(fresh),independent=True,reviewer='fixture')))
            with patch.object(cli,'qualify_sealed') as native:
                with self.assertRaises(RuntimeError):self.invoke(root,['prepare','--name','bad','--fresh',str(fresh)])
                native.assert_not_called()
            self.assertTrue((root/'out/bad/failure.json').exists());self.assertFalse((root/'out/bad/completion.json').exists())
    def test_unreviewed_preparation_cannot_launch_training(self):
        with self.directory() as d:
            root=Path(d);(root/'out/prep').mkdir(parents=True);fresh=root/'fresh.json';fresh.write_text('[]');review=root/'review.json';review.write_text('{}')
            folder=root/'out/prep';spec=dict(bindings={},fresh_path=str(fresh),fresh_sha256=cli.digest(fresh),review_path=str(review),review_sha256=cli.digest(review))
            (folder/'preparation.json').write_text(json.dumps(spec));(folder/'freeze.json').write_text(json.dumps(cli.freeze_files(folder)))
            with patch.object(cli.subprocess,'run') as launch:
                with self.assertRaises(RuntimeError):self.invoke(root,['train','--name','blocked','--from-run','prep'])
                launch.assert_not_called()
            self.assertTrue((root/'out/blocked/failure.json').exists())
    def test_no_threshold_cannot_open_evaluation_sources(self):
        with self.directory() as d:
            root=Path(d);folder=root/'out/cal';folder.mkdir(parents=True)
            (folder/'decision.json').write_text(json.dumps(dict(mode='calibration',selected=None,bindings={},launch='never')))
            (folder/'freeze.json').write_text(json.dumps(cli.freeze_files(folder)))
            with patch.object(cli,'training_reference') as training,patch.object(cli,'history_rows') as historical:
                with self.assertRaises(RuntimeError):self.invoke(root,['evaluate','--name','blocked','--from-run','cal'])
                training.assert_not_called();historical.assert_not_called()
            self.assertFalse((root/'out/blocked/completion.json').exists())

if __name__=='__main__':unittest.main()

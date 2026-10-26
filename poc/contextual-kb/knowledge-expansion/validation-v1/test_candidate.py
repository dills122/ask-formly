import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import candidate

class IsolationTests(unittest.TestCase):
    def test_unknown_arm_rejected_before_access(self):
        with self.assertRaises(ValueError):candidate.checked_database('typo')
    def test_drift_rejected_and_input_not_modified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'build').mkdir();db=root/'build/knowledge.sqlite';db.write_bytes(b'baseline')
            state={'installed_db_sha256':candidate.digest(db),'files':{}}
            (root/'baseline-state.json').write_text(json.dumps(state))
            with patch.object(candidate,'POC',root),patch.object(candidate,'HERE',root):
                self.assertEqual(candidate.checked_database('baseline')[0],db)
                db.write_bytes(b'drift')
                with self.assertRaises(ValueError):candidate.checked_database('baseline')
                self.assertEqual(db.read_bytes(),b'drift')
    def test_existing_candidate_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'candidate-build').mkdir();sentinel=root/'candidate-build/keep';sentinel.write_text('keep')
            with patch.object(candidate,'HERE',root),patch.object(candidate,'preserved',return_value={}):
                with self.assertRaises(FileExistsError):candidate.build()
            self.assertEqual(sentinel.read_text(),'keep');self.assertFalse((root/'candidate-inputs').exists())
    def test_manifest_cannot_redirect_candidate_to_installed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'candidate-build').mkdir();(root/'candidate-build/manifest.json').write_text(json.dumps({'database':'../build/knowledge.sqlite','sha256':'x','inputs':{}}))
            with patch.object(candidate,'HERE',root):
                with self.assertRaises(ValueError):candidate.checked_database('candidate')

if __name__=='__main__':unittest.main()

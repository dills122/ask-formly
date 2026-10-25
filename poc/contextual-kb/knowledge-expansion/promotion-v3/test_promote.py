import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import promote
from promote import guarded_replace, digest


class PromotionTests(unittest.TestCase):
    def test_success_preserves_snapshot_and_only_changes_selected_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve(); (root/'old').write_bytes(b'old'); (root/'model').write_bytes(b'model')
            result=guarded_replace(root, {'old':b'new','added':b'fact'}, {'old':digest(root/'old')}, root/'recovery', lambda: None)
            self.assertEqual((root/'old').read_bytes(),b'new'); self.assertEqual((root/'added').read_bytes(),b'fact')
            self.assertEqual((root/'recovery/old').read_bytes(),b'old'); self.assertEqual((root/'model').read_bytes(),b'model')
            self.assertEqual(result['status'],'installed')

    def test_postcheck_failure_restores_all_and_removes_new_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve(); (root/'old').write_bytes(b'old')
            def fail(): raise ValueError('postcheck')
            with self.assertRaisesRegex(ValueError,'postcheck'):
                guarded_replace(root,{'old':b'new','added':b'fact'},{'old':digest(root/'old')},root/'recovery',fail)
            self.assertEqual((root/'old').read_bytes(),b'old'); self.assertFalse((root/'added').exists())

    def test_drift_refused_before_snapshot_or_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve(); (root/'old').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'drift'):
                guarded_replace(root,{'old':b'new'},{'old':'wrong'},root/'recovery',lambda:None)
            self.assertEqual((root/'old').read_bytes(),b'changed'); self.assertFalse((root/'recovery').exists())

    def test_existing_unpinned_new_target_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve(); (root/'added').write_bytes(b'unexpected')
            with self.assertRaisesRegex(ValueError,'already exists'):
                guarded_replace(root,{'added':b'fact'},{},root/'recovery',lambda:None)

    def test_symlink_and_escape_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve(); (root/'old').write_bytes(b'old'); (root/'alias').symlink_to(root/'old')
            for target in ['../escape','alias']:
                with self.assertRaises(ValueError):
                    guarded_replace(root,{target:b'new'},{},root/'recovery',lambda:None)
            self.assertEqual((root/'old').read_bytes(),b'old')

    def test_existing_recovery_directory_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve(); (root/'recovery').mkdir()
            with self.assertRaises(FileExistsError):
                guarded_replace(root,{'added':b'fact'},{},root/'recovery',lambda:None)
            self.assertFalse((root/'added').exists())

    def test_partial_write_failure_restores_first_written_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve(); (root/'old').write_bytes(b'old')
            actual=promote.write_atomic
            def fail_new(path, content):
                if path.name=='added':raise OSError('simulated disk failure')
                return actual(path,content)
            with patch('promote.write_atomic',side_effect=fail_new):
                with self.assertRaisesRegex(OSError,'simulated disk failure'):
                    guarded_replace(root,{'old':b'new','added':b'fact'},{'old':digest(root/'old')},root/'recovery',lambda:None)
            self.assertEqual((root/'old').read_bytes(),b'old');self.assertFalse((root/'added').exists())

    def test_interruption_restores_and_records_rollback(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve(); (root/'old').write_bytes(b'old')
            def interrupt():raise KeyboardInterrupt()
            with self.assertRaises(KeyboardInterrupt):
                guarded_replace(root,{'old':b'new'},{'old':digest(root/'old')},root/'recovery',interrupt)
            self.assertEqual((root/'old').read_bytes(),b'old')
            self.assertIn('rolled_back',(root/'recovery/journal.json').read_text())

if __name__=='__main__': unittest.main()

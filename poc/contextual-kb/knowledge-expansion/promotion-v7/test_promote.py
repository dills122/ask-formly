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

class AdditionTests(unittest.TestCase):
    def test_two_sources_are_copied_without_mutating_prior_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); accepted=root/'accepted'; candidate=root/'candidate'; draft=root/'draft'
            for p in [accepted,candidate,draft]:p.mkdir()
            (accepted/'old.json').write_bytes(b'old');(candidate/'old.json').write_bytes(b'old')
            for name in ['material-select-options.json','material-select-all.json']:
                (draft/name).write_bytes(name.encode());(candidate/name).write_bytes(name.encode())
            result=promote.validate_additions(accepted,candidate,draft)
            self.assertEqual(set(result),{'material-select-options.json','material-select-all.json'})
            (candidate/'old.json').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'Accepted authored drift'):promote.validate_additions(accepted,candidate,draft)

    def test_missing_or_unexpected_addition_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);accepted=root/'accepted';candidate=root/'candidate';draft=root/'draft'
            for p in [accepted,candidate,draft]:p.mkdir()
            with self.assertRaisesRegex(ValueError,'Unexpected source set'):promote.validate_additions(accepted,candidate,draft)

class QualificationTests(unittest.TestCase):
    def fixtures(self):
        decision={'qualified':True,'reasons':[],'rounds':[{'round':i,'arm':arm,'usable':14 if arm=='candidate' else 5,'critical':0,'delivery_failed_ids':[]} for i in (1,2,3) for arm in ('baseline','candidate')]}
        checks={'successful_live_packets':90,'completed_calling_batches':18,'live_errors':[], 'planner_attempts':90,'installed_db_unchanged':True,'models_unchanged':True,'paired_replays':[{'round':i,'source_arm':'candidate' if i==2 else 'baseline','target_arm':'baseline' if i==2 else 'candidate','missing_source_cases':[],'results':15,'successful':15} for i in (1,2,3)]}
        return decision,checks

    def test_requires_both_arms_and_all_replay_rows(self):
        decision,checks=self.fixtures();promote.validate_qualification(decision,checks)
        checks['paired_replays'][1]['successful']=14
        with self.assertRaisesRegex(ValueError,'replay'):promote.validate_qualification(decision,checks)

    def test_rejects_failed_or_duplicate_candidate_round(self):
        decision,checks=self.fixtures();decision['rounds'][1]['usable']=13
        with self.assertRaisesRegex(ValueError,'answer'):promote.validate_qualification(decision,checks)
        decision,checks=self.fixtures();decision['rounds'][-1]=decision['rounds'][1].copy()
        with self.assertRaisesRegex(ValueError,'answer'):promote.validate_qualification(decision,checks)

    def test_rejects_missing_live_packets_and_model_drift(self):
        decision,checks=self.fixtures();checks['successful_live_packets']=89
        with self.assertRaisesRegex(ValueError,'integrity'):promote.validate_qualification(decision,checks)
        decision,checks=self.fixtures();checks['models_unchanged']=False
        with self.assertRaisesRegex(ValueError,'integrity'):promote.validate_qualification(decision,checks)

if __name__=='__main__': unittest.main()

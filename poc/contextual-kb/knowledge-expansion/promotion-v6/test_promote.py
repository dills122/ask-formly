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
            for name in ['array-operations.json','array-repeat-example.json']:
                (draft/name).write_bytes(name.encode());(candidate/name).write_bytes(name.encode())
            result=promote.validate_additions(accepted,candidate,draft)
            self.assertEqual(set(result),{'array-operations.json','array-repeat-example.json'})
            (candidate/'old.json').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'Accepted authored drift'):promote.validate_additions(accepted,candidate,draft)

    def test_missing_or_unexpected_addition_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);accepted=root/'accepted';candidate=root/'candidate';draft=root/'draft'
            for p in [accepted,candidate,draft]:p.mkdir()
            with self.assertRaisesRegex(ValueError,'Unexpected source set'):promote.validate_additions(accepted,candidate,draft)

class PlannerPromotionTests(unittest.TestCase):
    def test_service_switch_is_exact_and_other_composition_remains(self):
        original="from mcp_v1.planner import CodexPlanner\nunchanged = True\n"
        changed=promote.promoted_service(original.encode())
        self.assertEqual(changed,b"from condition_candidate_v2.planner import CodexPlanner\nunchanged = True\n")
        with self.assertRaisesRegex(ValueError,'Unexpected service composition'):
            promote.promoted_service(changed)

    def test_qualification_requires_semantics_and_no_delivery_errors(self):
        decision={'qualified':True,'reasons':[],'rounds':[{'round':i,'arm':'candidate','usable':n,'critical':0,'delivery_failed_ids':[]} for i,n in enumerate([15,14,15],1)]}
        probes={'reviewed':36,'semantic_pass':36}
        q20={'reviewed':3,'semantic_pass':3}
        promote.validate_qualification(decision,probes,q20)
        probes['semantic_pass']=35
        with self.assertRaisesRegex(ValueError,'semantic'):
            promote.validate_qualification(decision,probes,q20)
        probes['semantic_pass']=36;decision['rounds'][1]['delivery_failed_ids']=['A01']
        with self.assertRaisesRegex(ValueError,'answer'):
            promote.validate_qualification(decision,probes,q20)

if __name__=='__main__': unittest.main()

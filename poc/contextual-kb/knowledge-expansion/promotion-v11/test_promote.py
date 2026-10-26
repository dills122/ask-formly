import copy
from pathlib import Path
import tempfile
import unittest
import promote

class PromotionTests(unittest.TestCase):
    def test_only_db_pin_changes_in_both_runtime_manifests(self):
        old={'id':'old','files':{'build/knowledge.sqlite':'before','runtime.py':'fixed'},'knowledge':{'facts':93,'documents':21},'components':{'planner':'unchanged'}}
        for mode in ('model-free','model-backed'):
            result=promote.runtime_manifest(old,'new',mode)
            self.assertEqual(result['files'],{'build/knowledge.sqlite':'new','runtime.py':'fixed'})
            self.assertEqual(result['components'],old['components'])
            self.assertEqual(result['knowledge']['facts'],116)
            self.assertEqual(old['files']['build/knowledge.sqlite'],'before')
    def test_qualification_requires_both_semantic_and_protocol_success(self):
        good={'passed':True,'complete':True,'valid_judgments':True,'delivery_failures':0,'criticals':0,'mechanical_audit_passed':True,'repeats':[{'repeat':r,'candidate_usable':15,'all_controls':True,'regressions':[]} for r in (1,2,3)]}
        promote.require_decision(good)
        for key in ('passed','complete','valid_judgments','mechanical_audit_passed'):
            bad=copy.deepcopy(good);bad[key]=False
            with self.assertRaises(ValueError):promote.require_decision(bad)
        bad=copy.deepcopy(good);bad['repeats'].pop()
        with self.assertRaises(ValueError):promote.require_decision(bad)
    def test_source_addition_rejects_old_source_or_new_input_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();old=root/'old';new=root/'new';old.mkdir();new.mkdir();(old/'a.json').write_text('old');(new/'a.json').write_text('old');(new/'material-input-textarea.json').write_bytes(b'new')
            promote.validate_sources(old,new,b'new')
            (new/'a.json').write_text('changed')
            with self.assertRaises(ValueError):promote.validate_sources(old,new,b'new')
    def test_transaction_rolls_back_both_manifests_and_new_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();(root/'free').write_bytes(b'old-free');(root/'backed').write_bytes(b'old-backed')
            changes={'free':b'new-free','backed':b'new-backed','source':b'new'}
            expected={n:promote.sha(root/n) for n in ('free','backed')}
            def fail():raise RuntimeError('postcheck')
            with self.assertRaises(RuntimeError):promote.transaction.guarded_replace(root,changes,expected,root/'recovery',fail)
            self.assertEqual((root/'free').read_bytes(),b'old-free');self.assertEqual((root/'backed').read_bytes(),b'old-backed');self.assertFalse((root/'source').exists())
if __name__=='__main__':unittest.main()

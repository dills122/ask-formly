import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('promotion13', HERE/'promote.py')
promote = importlib.util.module_from_spec(spec)
spec.loader.exec_module(promote)

class PromotionTests(unittest.TestCase):
    def test_manifest_changes_only_identity_knowledge_and_db(self):
        old={'id':'old','files':{'build/knowledge.sqlite':'before','runtime.py':'fixed'},'components':{'models':'fixed'}}
        for mode, ident in [('model-free','formly-model-free-discovery-7'),('model-backed','formly-poc-foundation-15')]:
            got=promote.runtime_manifest(old,'new',mode)
            self.assertEqual(got['id'],ident)
            self.assertEqual(got['knowledge']['facts'],192)
            self.assertEqual(got['knowledge']['documents'],36)
            self.assertEqual(got['files'],{'build/knowledge.sqlite':'new','runtime.py':'fixed'})
            self.assertEqual(got['components'],old['components'])
            self.assertEqual(old['files']['build/knowledge.sqlite'],'before')

    def test_qualification_fails_closed(self):
        good={'passes':True,'cohort_counts_valid':True,'target_requests':24,'controls':8,'regression_requests':8,'candidate_target_usable':24,'candidate_controls_usable':8,'candidate_regressions_usable':8,'regressions':[],'critical_unsupported_claims':[],'passes_each_repeat':[True]*3,'total_tool_calls':399}
        promote.require_decision(good)
        for key,value in [('passes',False),('target_requests',23),('controls',7),('regression_requests',7),('candidate_target_usable',21),('candidate_controls_usable',7),('candidate_regressions_usable',7),('regressions',['lost']),('critical_unsupported_claims',['bad']),('passes_each_repeat',[True]*2),('total_tool_calls',398)]:
            bad=copy.deepcopy(good);bad[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):promote.require_decision(bad)

    def test_exact_additive_catalog_preserves_releases(self):
        old={'records':[{'id':'old'}],'evidence_releases':{'old':'6.3.12'}}
        good={'records':[{'id':'old'},{'id':'new'}],'evidence_releases':{'old':'6.3.12','new':'6.3.12'}}
        promote.validate_catalog(old,good,[{'id':'new'}])
        for field in ('records','evidence_releases'):
            bad=copy.deepcopy(good)
            if field=='records':bad[field][0]['id']='other'
            else:bad[field]['old']='7'
            with self.assertRaises(ValueError):promote.validate_catalog(old,bad,[{'id':'new'}])

    def test_authored_set_and_old_bytes_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);old=root/'old';new=root/'new';old.mkdir();new.mkdir()
            (old/'a.json').write_bytes(b'old');(new/'a.json').write_bytes(b'old');(new/'b.json').write_bytes(b'new')
            promote.validate_sources(old,new,{'b.json':b'new'})
            (new/'a.json').write_bytes(b'drift')
            with self.assertRaises(ValueError):promote.validate_sources(old,new,{'b.json':b'new'})

    def test_transaction_rolls_back_interrupt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();(root/'old').write_bytes(b'old')
            def fail():raise KeyboardInterrupt()
            with self.assertRaises(KeyboardInterrupt):promote.transaction.guarded_replace(root,{'old':b'changed','new':b'new'},{'old':promote.sha(root/'old')},root/'snapshot',fail)
            self.assertEqual((root/'old').read_bytes(),b'old');self.assertFalse((root/'new').exists())

    def test_fixed_spec_covers_nine_new_origins_and_326_protected(self):
        spec=promote.read(HERE/'promotion-spec.json')
        self.assertEqual(len(spec['drafts']),9)
        self.assertEqual(len(spec['protected']),326)
        for name,origin in spec['drafts'].items():
            source=promote.read(promote.ROOT/origin)['derived_from']['path']
            self.assertIn(source,spec['source_additions'])
            self.assertIn(str(Path(source).with_name('sources.md')),spec['source_additions'])

if __name__=='__main__':unittest.main()

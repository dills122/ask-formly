import unittest
from pipeline import collect, timing, validate_fresh
from test_decisions import raw

class Tests(unittest.TestCase):
    def test_operational_offsets_are_not_gold_offsets(self):
        calls=[]
        def scorer(text,offsets):calls.append(offsets);return {s:[.99,.99,0,0,0,0,0] for s in offsets}
        rows=[dict(id='q',text='abc',gold=[[1,2,'value']],probes=[dict(start=1,end=2,expected_role='value',family='gold')])]
        result=collect(rows,lambda text:raw(text),scorer)
        self.assertEqual(calls,[[(0,3)],[(1,2)]]);self.assertEqual(result[0]['operational_scores'][0]['start'],0)
    def test_expected_baseline_drift_fails(self):
        rows=[dict(id='q',text='x',gold=[],probes=[],expected_raw={'entities':{}})]
        with self.assertRaises(ValueError):collect(rows,lambda text:raw(),lambda t,s:{})
    def test_timing_five_repeats_each_seed(self):
        rows=[dict(id='q',text='x')];extract={s:lambda text:{'entities':{}} for s in ('1701','1702')}
        def fail(*args):self.fail('scored no-conflict question')
        result=timing(rows,extract,{s:fail for s in extract},(.5,.5))
        self.assertEqual(len(result['samples']),10);self.assertEqual(result['samples'][0]['seed'],'1701');self.assertEqual(result['samples'][2]['seed'],'1702')
    def test_timing_failure_after_successful_collection_cannot_pass(self):
        rows=[dict(id='q',text='x',gold=[],probes=[])]
        good=lambda text,offsets:{s:[.99,.99,0,0,0,0,0] for s in offsets}
        self.assertEqual(len(collect(rows,lambda text:raw(text),good)),1)
        for fail_after in (0,2):
            calls=[0]
            def scorer(text,offsets):
                calls[0]+=1
                if calls[0]>fail_after:raise ValueError('nonfinite verifier logits')
                return good(text,offsets)
            with self.subTest(fail_after=fail_after):
                with self.assertRaisesRegex(ValueError,'timing inference failure'):
                    timing(rows,{s:lambda text:raw(text) for s in ('1701','1702')},{s:scorer for s in ('1701','1702')},(.5,.5))
    def test_fresh_missing_coverage_rejected(self):
        with self.assertRaises(ValueError):validate_fresh([])

if __name__=='__main__':unittest.main()

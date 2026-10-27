import unittest
from report import summarize

class ReportTests(unittest.TestCase):
 def test_controls_do_not_inflate_target_score(self):
  cases=[{'id':str(i),'package':'N2','kind':'target' if i<10 else 'control'} for i in range(20)]
  b=[{'id':c['id'],'usable':False,'critical_unsupported_claim':False} for c in cases]
  c=[dict(r,usable=int(r['id'])>=2) for r in b]
  r=summarize(cases,b,c)
  self.assertEqual(r['packages']['N2']['candidate_target_usable'],8)
  self.assertFalse(r['packages']['N2']['passes'])
 def test_baseline_loss_blocks_aggregate_pass(self):
  cases,b,c=self.batch()
  next(r for r in b if r['id']=='API-0')['usable']=True
  next(r for r in c if r['id']=='API-0')['usable']=False
  r=summarize(cases,b,c)
  self.assertTrue(r['cohort_counts_valid'])
  self.assertEqual(r['regressions'],['API-0']);self.assertFalse(r['passes'])
 def test_critical_claim_blocks_pass(self):
  cases,b,c=self.batch()
  c[0]['critical_unsupported_claim']=True
  r=summarize(cases,b,c)
  self.assertTrue(r['cohort_counts_valid'])
  self.assertFalse(r['passes'])
 def batch(self):
  cases=[{'id':f'{p}-{i}', 'package':p, 'kind':k} for p,k,n in [('API','target',12),('CONFIG','target',12),('REGRESSION','regression',8),('CONTROL','control',8)] for i in range(n)]
  baseline=[{'id':r['id'],'usable':False,'critical_unsupported_claim':False} for r in cases]
  candidate=[dict(r,usable=True) for r in baseline]
  return cases,baseline,candidate
 def test_overall_target_threshold_does_not_gate_each_package(self):
  cases,b,c=self.batch()
  for r in c:
   if r['id'] in ['API-0','API-1']:r['usable']=False
  result=summarize(cases,b,c)
  self.assertTrue(result['passes'])
  self.assertEqual(result['candidate_target_usable'],22)
 def test_regression_cohort_cannot_pass_vacuously(self):
  cases,b,c=self.batch()
  next(r for r in c if r['id']=='REGRESSION-0')['usable']=False
  result=summarize(cases,b,c)
  self.assertFalse(result['passes'])
  self.assertFalse(result['packages']['REGRESSION']['passes'])
  self.assertEqual(result['candidate_regressions_usable'],7)
 def test_missing_regression_or_control_cohort_fails(self):
  for kind in ['regression','control']:
   with self.subTest(kind=kind):
    cases,b,c=self.batch();ids={r['id'] for r in cases if r['kind']==kind}
    self.assertFalse(summarize([r for r in cases if r['id'] not in ids],[r for r in b if r['id'] not in ids],[r for r in c if r['id'] not in ids])['passes'])
 def test_one_failed_control_blocks_pass(self):
  cases,b,c=self.batch();next(r for r in c if r['id']=='CONTROL-0')['usable']=False
  self.assertFalse(summarize(cases,b,c)['passes'])
 def test_21_of_24_targets_fails_even_with_all_other_cases(self):
  cases,b,c=self.batch()
  for r in c:
   if r['id'] in ['API-0','API-1','CONFIG-0']:r['usable']=False
  self.assertFalse(summarize(cases,b,c)['passes'])
 def test_complete_supported_batch_passes(self):
  cases,b,c=self.batch()
  self.assertTrue(summarize(cases,b,c)['passes'])
if __name__=='__main__':unittest.main()

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
  cases=[{'id':str(i),'package':'N3','kind':'target'} for i in range(10)]
  b=[{'id':r['id'],'usable':r['id']=='0','critical_unsupported_claim':False} for r in cases]
  c=[dict(r,usable=r['id']!='0') for r in b]
  r=summarize(cases,b,c)
  self.assertEqual(r['regressions'],['0']);self.assertFalse(r['passes'])
 def test_critical_claim_blocks_pass(self):
  cases=[{'id':'q','package':'N2','kind':'target'}]
  a=[{'id':'q','usable':True,'critical_unsupported_claim':True}]
  self.assertFalse(summarize(cases,a,a)['passes'])
if __name__=='__main__':unittest.main()

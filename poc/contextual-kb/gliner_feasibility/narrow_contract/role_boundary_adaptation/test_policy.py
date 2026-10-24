import unittest
from policy import gate,chunks,diagnostic_failure
class PolicyTests(unittest.TestCase):
 def good(self):return dict(fresh_gain=.02,exact_gain=0,api_recall_gain=0,invalid_gain=0,empty_fp_gain=0,diagnostic_regressions=[])
 def test_both_required_and_threshold(self):
  self.assertTrue(gate([self.good(),self.good()]));self.assertFalse(gate([self.good()]))
  for key,value in [('fresh_gain',.019),('exact_gain',-1),('api_recall_gain',-.001),('invalid_gain',1),('empty_fp_gain',1),('diagnostic_regressions',['olddev'])]:
   bad=self.good();bad[key]=value;self.assertFalse(gate([self.good(),bad]),key)
 def test_194_once_with_partial_chunk(self):
  c=chunks(194,1701,1);self.assertEqual([len(x) for x in c],[8]*24+[2]);self.assertEqual(sorted(sum(c,[])),list(range(194)))
  self.assertEqual(c,chunks(194,1701,1));self.assertNotEqual(c,chunks(194,1701,2))
 def test_diagnostics_require_zero_invalids_and_both_comparators(self):
  def metric(f1,invalid=0,fp=0):return dict(invalid=invalid,accepted={'all':{'f1':f1}},exact_by_gold={'clear_empty':{'raw_nonempty':fp}})
  self.assertFalse(diagnostic_failure(metric(.98),metric(1)))
  self.assertTrue(diagnostic_failure(metric(.979),metric(1)))
  self.assertTrue(diagnostic_failure(metric(1,1),metric(.8,2)))
  self.assertTrue(diagnostic_failure(metric(1,0,1),metric(.9)))
 def test_empty_training_rejected(self):
  with self.assertRaises(ValueError):chunks(0,1701,1)
if __name__=='__main__':unittest.main()

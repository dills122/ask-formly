import unittest
from policy import chunks,gate,rate
class PolicyTests(unittest.TestCase):
 def test_undefined_precision_counts_as_zero(self):
  self.assertEqual(rate(None),0.0)
  self.assertEqual(rate(.5),.5)
 def test_partial_chunk_preserves_every_example_once(self):
  result=chunks(146,1701,1)
  self.assertEqual([len(c) for c in result],[8]*18+[2])
  self.assertEqual(sorted(i for c in result for i in c),list(range(146)))
  self.assertEqual(result,chunks(146,1701,1))
  self.assertNotEqual(result,chunks(146,1701,2))
 def test_bad_sizes_rejected(self):
  for n in (0,-1):
   with self.assertRaises(ValueError):chunks(n,1,1)
 def test_gate_requires_both_no_regression_and_target_gain(self):
  good=dict(fresh_gain=.03,exact_gain=1,api_recall_gain=0,adapter_precision_gain=0,empty_fp_gain=0,diagnostic_regressions=[],target_api_gain=.06)
  self.assertTrue(gate([good,good]))
  self.assertFalse(gate([good]))
  for patch in ({'fresh_gain':.01},{'exact_gain':-1},{'api_recall_gain':-.01},{'adapter_precision_gain':-.01},{'empty_fp_gain':1},{'diagnostic_regressions':['olddev']},{'target_api_gain':.04}):
   self.assertFalse(gate([dict(good,**patch),good]))
if __name__=='__main__':unittest.main()

import unittest
from gate import case_issues,paired_gate
class Tests(unittest.TestCase):
 def test_undo_wrong_prior_preserves_correct(self):
  self.assertEqual(case_issues({'right'},{'right','wrong'},{'right','wrong'},{'right'},False,True,False,True),[])
 def test_losing_either_original_or_prior_correct_blocked(self):
  issues=case_issues({'right'},{'right'},{'right'},set(),True,False,False,False)
  self.assertIn('original_correct_lost',issues);self.assertIn('previous_correct_lost',issues);self.assertIn('previous_exact_lost',issues)
 def test_new_structurally_valid_wrong_blocked(self):
  self.assertIn('invalid_to_valid_wrong',case_issues({'right'},{'wrong_a','wrong_b'},{'wrong_a','wrong_b'},{'wrong_a'},False,True,False,False))
 def test_restoring_invalid_is_not_repair(self):
  self.assertEqual(case_issues({'right'},{'wrong_a','wrong_b'},{'wrong_a'},{'wrong_a','wrong_b'},False,True,True,False),[])
  self.assertFalse(paired_gate([{'issues':[],'correct_resolutions':0,'wrong_resolutions':0},{'issues':[],'correct_resolutions':1,'wrong_resolutions':0}]))
 def test_both_seeds_required_and_wrong_resolution_blocks(self):
  good={'issues':[],'correct_resolutions':1,'wrong_resolutions':0}
  self.assertTrue(paired_gate([good,good]));self.assertFalse(paired_gate([good]));self.assertFalse(paired_gate([good,{**good,'wrong_resolutions':1}]))

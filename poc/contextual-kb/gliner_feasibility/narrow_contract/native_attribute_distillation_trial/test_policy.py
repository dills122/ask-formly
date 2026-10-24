import unittest
import torch
from policy import schedule,anchor_schedule,anchor_weights,penalty
class PolicyTests(unittest.TestCase):
 def test_matched_supervised_budget_covers_training(self):
  p=schedule(1701)
  self.assertEqual(len(p),124);self.assertEqual(sum(map(len,p)),992);self.assertEqual(set(i for x in p for i in x),set(range(242)))
  self.assertEqual(p,schedule(1701));self.assertNotEqual(p,schedule(1702))
 def test_anchor_cycle_covers_all194_with_fixed248_exposures(self):
  p=anchor_schedule(1701)
  self.assertEqual(len(p),124);self.assertTrue(all(len(x)==2 for x in p));self.assertEqual(set(i for x in p for i in x),set(range(194)))
 def test_empty_anchor_row_does_not_dilute_available_row(self):
  self.assertEqual(anchor_weights([0,3]),[0.,1.]);self.assertEqual(anchor_weights([2,3]),[.5,.5]);self.assertEqual(anchor_weights([0,0]),[0.,0.])
 def test_control_and_treatment_use_identical_raw_kl_but_different_gradient(self):
  x=torch.tensor(2.,requires_grad=True);a=penalty(x,'control');a.backward();self.assertEqual(x.grad.item(),0.)
  x.grad=None;b=penalty(x,'treatment');b.backward();self.assertEqual(b.item(),200.);self.assertEqual(x.grad.item(),100.)
if __name__=='__main__':unittest.main()

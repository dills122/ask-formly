import unittest
import torch
from loss import preservation_kl,correct_mask
class LossTests(unittest.TestCase):
 def test_identical_logits_have_zero_loss_and_finite_zero_gradient(self):
  x=torch.tensor([[2.,0.,-1.]],requires_grad=True);p=x.detach().softmax(-1)
  z=preservation_kl(x,p,torch.tensor([True]));z.backward()
  self.assertAlmostEqual(z.item(),0.,places=6);self.assertLess(x.grad.abs().max().item(),1e-6)
 def test_wrong_teacher_and_low_confidence_are_masked(self):
  p=torch.tensor([[.1,.9],[.5,.5],[.8,.2]])
  self.assertEqual(correct_mask(p,torch.tensor([0,0,0])).tolist(),[False,False,True])
 def test_masked_wrong_target_cannot_contribute_gradient(self):
  x=torch.zeros((2,2),requires_grad=True);p=torch.tensor([[.9,.1],[.1,.9]])
  loss=preservation_kl(x,p,torch.tensor([True,False]));loss.backward()
  self.assertGreater(loss.item(),0);self.assertEqual(x.grad[1].abs().sum().item(),0.)
 def test_empty_mask_fails_closed(self):
  with self.assertRaises(ValueError):preservation_kl(torch.zeros((1,2)),torch.ones((1,2))/2,torch.tensor([False]))
if __name__=='__main__':unittest.main()

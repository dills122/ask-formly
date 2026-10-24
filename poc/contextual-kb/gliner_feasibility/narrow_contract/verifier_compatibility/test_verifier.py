import unittest
import torch
from verifier import align, decide, objective, ROLES

class VerifierTests(unittest.TestCase):
    def test_repeated_occurrences_keep_identity(self):
        self.assertEqual(align('foo foo', [(4,7),(0,3)], {0:0,1:4}, {0:3,1:7}), ([(4,7),(0,3)], [], [(1,2),(0,1)]))
    def test_no_snapping_inside_tokens(self):
        self.assertEqual(align('foo', [(1,3)], [0], [3]), ([],[(1,3)],[]))
    def test_invalid_and_duplicate_offsets_raise(self):
        for spans in ([(0,0)], [(0,4)], [(True,2)], [(0,3),(0,3)]):
            with self.assertRaises(ValueError): align('foo',spans,[0],[3])
    def test_zero_roles_abstains(self):
        self.assertEqual(decide(torch.tensor([8.,-8.,-8.,-8.,-8.,-8.,-8.]))['status'],'unresolved')
    def test_multiple_roles_abstains(self):
        self.assertEqual(decide(torch.tensor([8.,8.,8.,-8.,-8.,-8.,-8.]))['status'],'unresolved')
    def test_boundary_reject_blocks_confident_role(self):
        self.assertEqual(decide(torch.tensor([-8.,8.,-8.,-8.,-8.,-8.,-8.]))['status'],'unresolved')
    def test_single_role_can_pass(self):
        self.assertEqual(decide(torch.tensor([8.,8.,-8.,-8.,-8.,-8.,-8.]))['role'],ROLES[0])
    def test_other_logit_does_not_change_probability(self):
        a=torch.tensor([8.,1.,-1.,-2.,-3.,-4.,-5.]); b=a.clone(); b[2]=100
        self.assertEqual(decide(a)['probabilities'][1],decide(b)['probabilities'][1])
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError): decide(torch.tensor([float('nan')]*7))
    def test_bce_independent_gradients(self):
        z=torch.zeros(1,7,requires_grad=True); y=torch.tensor([[1.,1.,0.,0.,0.,0.,0.]])
        objective(z,y).backward()
        self.assertTrue((z.grad[0,:2]<0).all());self.assertTrue((z.grad[0,2:]>0).all())
    def test_bad_targets_rejected(self):
        with self.assertRaises(ValueError): objective(torch.zeros(1,7),torch.ones(1,6))

if __name__=='__main__': unittest.main()

import unittest
from collections import Counter
from schedule import schedule, weighted_loss
class ScheduleTests(unittest.TestCase):
 def test_budget_and_shared_replay_are_exactly_matched(self):
  a=schedule(1701,'control');b=schedule(1701,'treatment')
  self.assertEqual(len(a),124);self.assertEqual(sum(map(len,a)),992)
  for x,y in zip(a,b):
   self.assertEqual(x[:7],y[:7]);self.assertEqual(len(x),8);self.assertEqual(len(y),8)
   self.assertTrue(all(i<194 and w==1 for i,w in x));self.assertTrue(y[-1][0]>=194);self.assertEqual(y[-1][1],.25)
 def test_all_training_questions_replayed_balanced_and_no_evaluation_indices(self):
  for arm in ('control','treatment'):
   counts=Counter(i for row in schedule(1702,arm) for i,_ in row)
   self.assertEqual(set(i for i in counts if i<194),set(range(194)))
   if arm=='treatment':
    self.assertEqual(set(i for i in counts if i>=194),set(range(194,242)))
    vals=[counts[i] for i in range(194,242)];self.assertLessEqual(max(vals)-min(vals),1)
 def test_deterministic_but_seed_specific_and_unknown_arm_rejected(self):
  self.assertEqual(schedule(1701,'treatment'),schedule(1701,'treatment'))
  self.assertNotEqual(schedule(1701,'treatment'),schedule(1702,'treatment'))
  with self.assertRaises(ValueError):schedule(1701,'unknown')
 def test_weight_is_not_renormalized_and_preserves_native_gradient(self):
  import torch
  x=torch.tensor(2.,requires_grad=True)
  value=weighted_loss(x,.25,8);value.backward()
  self.assertEqual(value.item(),.0625);self.assertEqual(x.grad.item(),.03125)
if __name__=='__main__':unittest.main()

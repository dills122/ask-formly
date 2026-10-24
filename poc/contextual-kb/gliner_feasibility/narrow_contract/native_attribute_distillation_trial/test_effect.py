import unittest
from effect import selected,superiority
class EffectTests(unittest.TestCase):
 def test_abstention_is_not_semantic_rejection(self):
  self.assertIsNone(selected({'status':'scored','label':'no_entity','confidence':.5}))
  self.assertEqual(selected({'status':'scored','label':'no_entity','confidence':.51}),'no_entity')
 def test_fresh_gains_do_not_offset_old_loss(self):
  rows=[dict(seed=1701,fresh=True,before_correct=False,after_correct=True),dict(seed=1702,fresh=True,before_correct=False,after_correct=True),dict(seed=1701,fresh=False,before_correct=True,after_correct=False)]
  self.assertFalse(superiority(rows))
 def test_each_seed_requires_fresh_gain_and_no_loss(self):
  a=dict(seed=1701,fresh=True,before_correct=False,after_correct=True)
  self.assertFalse(superiority([a]));self.assertTrue(superiority([a,dict(a,seed=1702)]))
if __name__=='__main__':unittest.main()

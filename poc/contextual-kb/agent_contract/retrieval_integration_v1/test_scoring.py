import unittest
from scoring import retrieval_summary, bridge_pass
class ScoringTests(unittest.TestCase):
 def test_paired_loss_blocks_even_if_net_count_recovers(self):
  base=dict(recall=.8,precision=.5,complete_groups=4,unsupported_candidates=8)
  self.assertFalse(bridge_pass(base,dict(base,recall=.9),lost_complete=1))

 def test_negative_queries_not_reported_as_recall_success(self):
  rows=[{'id':'a','metrics':{'8':{'recall':None,'precision':0,'ndcg':None,'mrr':None,'complete_groups':None,'group_recall':None,'unsupported_candidates':8}},'query_count':1,'seconds':.1}]
  s=retrieval_summary(rows);self.assertEqual(s['supported'],0);self.assertIsNone(s['recall']);self.assertEqual(s['unsupported_candidates'],8)
 def test_gain_cannot_hide_complete_support_regression(self):
  base=dict(recall=.8,precision=.5,complete_groups=4,unsupported_candidates=8)
  new=dict(recall=.9,precision=.5,complete_groups=3,unsupported_candidates=8)
  self.assertFalse(bridge_pass(base,new))
 def test_clear_gain_passes(self):
  base=dict(recall=.8,precision=.5,complete_groups=4,unsupported_candidates=8)
  self.assertTrue(bridge_pass(base,dict(base,recall=.83)))
if __name__=='__main__':unittest.main()

import unittest
from metrics import assess

def fixture(base,other,gold):
 records=[dict(id='x',batch=1)];cases=[dict(id='x',relevant_fact_ids=gold,required_groups=[gold] if gold else [])]
 semantic=[dict(id='x',foundation_pass=True,supplement_pass=True,issues=[])]
 rows=[dict(id='x',batch=1,arm=a,ids=ids,logical_query_count=1,logical_query_characters=10,foundation_error=None,supplement_error=None) for a,ids in [('foundation',base),('current',other),('protected',other)]]
 return rows,records,cases,semantic
class TestMetrics(unittest.TestCase):
 def test_fact_loss_fails_even_if_group_and_recall_survive(self):
  r=assess(*fixture(['a'],['b'],['a','b']))
  self.assertFalse(r['gates']['protected']['safety']);self.assertEqual(r['paired']['protected'][0]['8']['lost_relevant'],['a'])
  self.assertEqual(r['gates']['protected']['paired_group_losses'],[])
 def test_new_relevant_fact_can_pass_safety_utility(self):
  r=assess(*fixture(['a'],['a','b'],['a','b']));self.assertTrue(r['gates']['protected']['safety']);self.assertTrue(r['gates']['protected']['utility'])
 def test_no_new_relevant_fact_not_utility(self):
  r=assess(*fixture(['a'],['a','z'],['a']));self.assertFalse(r['gates']['protected']['utility'])
 def test_missing_arm_not_hidden(self):
  args=list(fixture(['a'],['a'],['a']));args[0]=args[0][:-1]
  with self.assertRaises(ValueError):assess(*args)
 def test_unsupported_not_recall_success(self):
  r=assess(*fixture(['z'],['z'],[]));self.assertIsNone(r['summaries']['protected']['all']['8']['recall']);self.assertFalse(r['consistent_floor']['protected'])
 def test_semantic_failure_separate_from_conditional_policy(self):
  args=list(fixture(['a'],['a','b'],['a','b']));args[3][0]['supplement_pass']=False
  r=assess(*args);self.assertTrue(r['gates']['protected']['safety']);self.assertTrue(r['gates']['protected']['utility']);self.assertFalse(r['qualified'])
 def test_prefix_violation_visible(self):
  r=assess(*fixture(['a','b'],['b','a'],['a','b']));self.assertFalse(r['protected_prefix_preserved']);self.assertFalse(r['qualified'])
 def test_required_group_rescue_vs_current_is_explicit(self):
  args=list(fixture(['a'],['a'],['a']))
  args[0][1]['ids']=['z']
  report=assess(*args);change=report['protected_vs_current'][0]
  for k in ('4','8'):
   self.assertTrue(change[k]['group_gained']);self.assertFalse(change[k]['group_lost']);self.assertEqual(change[k]['rescued_relevant'],['a'])
 def test_missing_required_groups_not_just_missing_facts(self):
  args=list(fixture(['a'],['a'],['a','b','c']));args[2][0]['required_groups']=[['a'],['b','c']]
  report=assess(*args)
  for row in report['scored_rows']:
   for k in ('4','8'):self.assertEqual(row['metrics'][k]['missing_groups'],[['b','c']])
 def test_same_actual_records_all_batches_required(self):
  args=list(fixture(['a'],['a','b'],['a','b']));args[0][0]['batch']=2
  with self.assertRaises(ValueError):assess(*args)
if __name__=='__main__':unittest.main()

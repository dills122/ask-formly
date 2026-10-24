import unittest
from comparison import deltas,decision,overlaps

def m(role,start,end,text):return dict(kind=role,start=start,end=end,raw=text)
class ComparisonTests(unittest.TestCase):
 def test_same_text_different_occurrences_are_not_deduplicated(self):
  a=m('value',0,3,'"x"');b=m('value',5,8,'"x"')
  d=deltas([a,b],[a],[a,b])
  self.assertEqual(d['lost_correct'],[['value',5,8,'"x"']])
  self.assertEqual(d['removed_false'],[])
 def test_role_mismatch_is_false_positive_not_correct(self):
  a=m('model_key',0,3,'"x"');b=m('value',0,3,'"x"')
  d=deltas([a,b],[a],[a])
  self.assertEqual(d['removed_false'],[['value',0,3,'"x"']]);self.assertFalse(d['lost_correct'])
 def test_global_overlap_classifies_roles_and_allows_adjacency(self):
  a=m('value',0,3,'abc');b=m('value',1,2,'b');c=m('api_reference',1,2,'b');d=m('value',3,4,'d')
  self.assertEqual(overlaps([a,b,c,d]),{'within_role':1,'cross_role':2})
 def test_gains_do_not_hide_correct_loss(self):
  rows=[dict(lost_correct=0,invalid_before=2,invalid_after=0,new_invalid=0,accepted_before=.5,accepted_after=.9)]*2
  self.assertTrue(decision({1701:rows,1702:rows}))
  bad=[dict(rows[0],lost_correct=1),rows[1]]
  self.assertFalse(decision({1701:bad,1702:rows}))
 def test_gate_requires_both_models_and_no_split_regression(self):
  rows=[dict(lost_correct=0,invalid_before=2,invalid_after=0,new_invalid=0,accepted_before=.5,accepted_after=.9)]*2
  self.assertFalse(decision({1701:rows}))
  bad=[dict(rows[0],accepted_after=.4),rows[1]]
  self.assertFalse(decision({1701:bad,1702:rows}))
if __name__=='__main__':unittest.main()

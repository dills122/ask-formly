import unittest
from assessment import decision
def cell(f1=.4,accepted=.2,recall=.5):
 return {'raw':{'all':{'f1':f1,'precision':.8,'recall':recall},'api_reference':{'recall':recall,'precision':.8}},
 'accepted':{'all':{'f1':accepted}},'invalid':0}
class AssessmentTests(unittest.TestCase):
 def test_both_seeds_required(self):
  self.assertFalse(decision(cell(),[cell(.6,.3),cell(.45,.3)])['worth_continuing'])
 def test_role_regression_blocks(self):
  self.assertFalse(decision(cell(),[cell(.6,.3,.3),cell(.6,.3)])['worth_continuing'])
 def test_gain_not_readiness(self):
  r=decision(cell(),[cell(.6,.3),cell(.6,.3)])
  self.assertTrue(r['worth_continuing']);self.assertFalse(r['qualified'])
 def test_no_gain_from_invalid(self):
  self.assertFalse(decision(cell(),[cell(.6,.1),cell(.6,.1)])['worth_continuing'])
if __name__=='__main__':unittest.main()

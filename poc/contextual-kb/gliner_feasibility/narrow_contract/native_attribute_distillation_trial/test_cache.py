import unittest,copy
from cache_contract import validate,targets
class CacheTests(unittest.TestCase):
 def setUp(self):
  self.rows=[dict(question_id='train',question='props.x',mentions=[dict(kind='api_reference',raw='props.x',start=0,end=7)])];self.bad=[dict(question_id='train',negatives=[])]
  self.c=dict(identity={'source':'same'},records=[dict(question_id='train',question='props.x',targets=targets(self.rows[0],self.bad[0]),unsupported=[],probabilities=[[.9,.1,0,0,0,0,0]],mask=[True])])
 def test_correct_cache_passes_and_source_changes_fail(self):
  validate(self.c,{'source':'same'},self.rows,self.bad)
  with self.assertRaises(ValueError):validate(self.c,{'source':'different'},self.rows,self.bad)
 def test_wrong_teacher_cannot_be_marked_correct(self):
  self.c['records'][0]['probabilities']=[[.1,.9,0,0,0,0,0]]
  with self.assertRaises(ValueError):validate(self.c,{'source':'same'},self.rows,self.bad)
  self.c['records'][0]['mask']=[False];validate(self.c,{'source':'same'},self.rows,self.bad)
 def test_occurrence_drift_and_teacher_probability_corruption_fail(self):
  altered=copy.deepcopy(self.c);altered['records'][0]['targets'][0]['start']=1
  with self.assertRaises(ValueError):validate(altered,{'source':'same'},self.rows,self.bad)
  self.c['records'][0]['probabilities'][0][0]=float('nan')
  with self.assertRaises(ValueError):validate(self.c,{'source':'same'},self.rows,self.bad)
if __name__=='__main__':unittest.main()

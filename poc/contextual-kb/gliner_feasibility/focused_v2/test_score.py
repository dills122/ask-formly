import unittest
from score import spans, counts, metrics, shared_recall, prediction
class ScoringTests(unittest.TestCase):
 def test_offsets_and_types(self):
  self.assertEqual(spans('x x',{'api':[{'text':'x','start':2,'end':3}]}),{('api',2,3,'x')})
  with self.assertRaises(ValueError):spans('x',{'api':[{'text':'y','start':0,'end':1}]})
 def test_wrong_boundary_is_fp_and_fn(self):
  self.assertEqual(counts({('api',0,2,'xy')},{('api',0,1,'x')}),{'tp':0,'fp':1,'fn':1})
 def test_missing_prediction_not_excluded(self):
  self.assertEqual(counts(set(),{('api',0,1,'x')}),{'tp':0,'fp':0,'fn':1})
 def test_metrics(self):
  self.assertEqual(metrics({'tp':1,'fp':1,'fn':3})['f1'],1/3)
 def test_shared_atoms_deduplicate(self):
  self.assertEqual(shared_recall({('api','x')},{('api','x'),('api','y')},{('api','x')},set()),
                   {'shared':1,'original_found':1,'focused_found':0})
 def test_missing_and_malformed_outputs(self):
  for row in (None, {'output':None}, {'output':[]}, {'output':{'entities':None}}, {'output':{'entities':{},'request':None}}):
   p,error,records,label=prediction('x',row)
   self.assertEqual(p,set());self.assertIsNotNone(error)
 def test_valid_prediction(self):
  p,error,records,label=prediction('x',{'output':{'entities':{'api':[{'text':'x','start':0,'end':1}]},'request':[{}],'interpretation':{'label':'clear'}}})
  self.assertIsNone(error);self.assertEqual(records,1);self.assertEqual(label,'clear');self.assertEqual(len(p),1)
 def test_unknown_label_rejected(self):
  with self.assertRaises(ValueError):spans('x',{'other':[]})
if __name__=='__main__':unittest.main()

import unittest
from experiment import evaluate
class Tests(unittest.TestCase):
 def test_missing_output_lowers_recall(self):
  inputs=[{'id':'x','parent':'P','question':'abc'}]
  gold={'x':{('api',0,3,'abc')}}
  s=evaluate(inputs,gold,[])
  self.assertEqual(s['all']['fn'],1);self.assertEqual(len(s['errors']),1)
 def test_exact_and_parent_dedup(self):
  inputs=[{'id':str(i),'parent':'P','question':'abc'} for i in range(2)]
  gold={r['id']:{('api',0,3,'abc')} for r in inputs}
  rows=[{'id':r['id'],'output':{'entities':{'api':[{'text':'abc','start':0,'end':3}]}},'seconds':1} for r in inputs]
  s=evaluate(inputs,gold,rows)
  self.assertEqual(s['all']['tp'],2);self.assertEqual(s['parents']['P']['unique']['tp'],1)
  self.assertEqual(s['exact_questions'],2)
 def test_duplicates_rejected(self):
  with self.assertRaises(ValueError):evaluate([{'id':'x','parent':'P','question':'x'}],{'x':set()},[{'id':'x'},{'id':'x'}])
 def test_malformed_counts_failure(self):
  s=evaluate([{'id':'x','parent':'P','question':'x'}],{'x':set()},[{'id':'x','output':None}])
  self.assertEqual(len(s['errors']),1);self.assertEqual(s['exact_questions'],0)
if __name__=='__main__':unittest.main()

import unittest
import copy
from metrics import assess_structure, summarize_grades, consistency
O={'formly_questions':[{'question':'How?','reason':'Requested.'}],'library_constraints':{'formly_version':None,'ui_adapter':None}}
C=[{'id':'X','group':'g','request':'x'}]
R=[{'id':'X','required':['cover'],'forbidden':['invent']}]
class Tests(unittest.TestCase):
 def test_missing_output_retained(self):
  x=assess_structure(C,[]);self.assertFalse(x['X']['valid'])
 def test_duplicate_extra_ids_reject_batch(self):
  for rows in ([{'id':'X','output':O}]*2,[{'id':'Y','output':O}]):
   self.assertFalse(assess_structure(C,rows)['X']['valid'])
 def test_structure_blocks_semantic_pass(self):
  g=[{'id':'X','required':[True],'forbidden':[False],'evidence':'Covered'}]
  s=summarize_grades(C,R,g,{'X':{'valid':False}});self.assertEqual(s['passed'],0)
 def test_missing_duplicate_grade_fails(self):
  for gs in ([],[{'id':'X','required':[True],'forbidden':[False],'evidence':'Covered'}]*2):
   with self.assertRaises(ValueError):summarize_grades(C,R,gs,{'X':{'valid':True}})
 def test_nonboolean_grade_rejected(self):
  with self.assertRaises(ValueError):summarize_grades(C,R,[{'id':'X','required':['yes'],'forbidden':[False],'evidence':'Covered'}],{'X':{'valid':True}})
 def test_duplicates_not_allowed_in_panel(self):
  with self.assertRaises(ValueError):assess_structure(C+C,[])
 def test_reason_variation_not_query_variation(self):
  b=copy.deepcopy(O);b['formly_questions'][0]['reason']='Another reason'
  s=consistency([O,b,O]);self.assertFalse(s['exact']);self.assertTrue(s['questions']);self.assertTrue(s['counts'])
 def test_invalid_outputs_not_stable(self):
  s=consistency([None,None,None]);self.assertFalse(s['exact']);self.assertFalse(s['questions'])
if __name__=='__main__':unittest.main()

import unittest
from assess import summarize
class AssessmentTests(unittest.TestCase):
 def setUp(self):
  self.cases=[{'id':'X','batch':1,'request':'How do I use Formly?'}]
  self.plan={'formly_questions':[{'question':'How do I use Formly?','reason':'Requested usage'}],'library_constraints':{'formly_version':None,'ui_adapter':None},'condition_bindings':[]}
  self.rows=[{'id':'X','run':i,'output':self.plan} for i in (1,2,3)]
  self.grades=[{'id':'X','run':i,'semantic_pass':True,'binding_pass':True} for i in (1,2,3)]
 def test_all_pass(self):
  x=summarize(self.cases,self.rows,self.grades)
  self.assertEqual((x['slots'],x['usable'],x['all_three_usable'],x['exact_equal_cases']),(3,3,1,1))
 def test_missing_counts_as_failure(self):
  x=summarize(self.cases,self.rows[:2],self.grades)
  self.assertEqual((x['slots'],x['structural'],x['usable'],x['all_three_usable']),(3,2,2,0))
 def test_structure_not_semantics(self):
  self.grades[0]['semantic_pass']=False
  x=summarize(self.cases,self.rows,self.grades)
  self.assertEqual((x['structural'],x['usable'],x['exact_equal_cases']),(3,2,1))
 def test_invalid_output_not_dropped(self):
  self.rows[0]['output']={}
  x=summarize(self.cases,self.rows,self.grades)
  self.assertEqual((x['slots'],x['structural'],x['usable']),(3,2,2))
 def test_wording_variation_not_failure(self):
  self.rows[0]['output']={**self.plan,'formly_questions':[{'question':'How is Formly used?','reason':'Usage request'}]}
  x=summarize(self.cases,self.rows,self.grades)
  self.assertEqual((x['usable'],x['exact_equal_cases']),(3,0))
 def test_duplicate_unknown_and_missing_grades_rejected(self):
  for rows,grades in [(self.rows+self.rows[:1],self.grades),(self.rows+[{'id':'Y','run':1,'output':self.plan}],self.grades),(self.rows,self.grades[:2]),(self.rows,self.grades+self.grades[:1])]:
   with self.assertRaises(ValueError):summarize(self.cases,rows,grades)
 def test_binding_failure_blocks_success(self):
  self.grades[0]['binding_pass']=False
  self.assertEqual(summarize(self.cases,self.rows,self.grades)['usable'],2)
 def test_ungraded_no_claim(self):
  x=summarize(self.cases,self.rows)
  self.assertIsNone(x['usable'])
if __name__=='__main__':unittest.main()

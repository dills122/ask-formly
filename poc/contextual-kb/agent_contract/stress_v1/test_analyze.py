import copy
import unittest
from analyze import summarize, grade_summary
O={'formly_questions':[{'question':'How?','reason':'Requested.'}],'library_constraints':{'formly_version':None,'ui_adapter':None}}
C=[{'id':'X','group':'g','request':'A request'}]
def runs():return {str(i):[{'id':'X','output':copy.deepcopy(O)}] for i in range(1,6)}
class Tests(unittest.TestCase):
 def test_identical_results(self):
  r=summarize(C,runs());self.assertEqual(r['valid'],5);self.assertEqual(r['exact_stable_cases'],1);self.assertEqual(r['equal_pairs'],10)
 def test_rewording_not_exact_but_same_count(self):
  rs=runs();rs['5'][0]['output']['formly_questions'][0]['reason']='A different reason.'
  r=summarize(C,rs);self.assertEqual(r['exact_stable_cases'],0);self.assertEqual(r['equal_pairs'],6);self.assertTrue(r['cases'][0]['question_count_stable']);self.assertTrue(r['cases'][0]['question_text_stable'])
 def test_missing_case_kept_as_failure(self):
  rs=runs();rs['5']=[];r=summarize(C,rs);self.assertEqual(r['total'],5);self.assertEqual(r['invalid_or_missing'],1);self.assertEqual(r['exact_stable_cases'],0)
 def test_duplicate_and_extra_ids_invalid_run(self):
  for bad in ([{'id':'X','output':O}]*2,[{'id':'Y','output':O}]):
   rs=runs();rs['2']=bad;r=summarize(C,rs);self.assertEqual(r['invalid_or_missing'],1)
 def test_all_invalid_not_counted_as_deterministic(self):
  r=summarize(C,{str(i):None for i in range(1,6)});self.assertEqual(r['exact_stable_cases'],0);self.assertEqual(r['equal_pairs'],0)
 def test_consistently_wrong_is_stable_but_fails(self):
  rubric=[{'id':'X','required':['req'],'forbidden':['bad']}]
  grades=[{'run':str(i),'id':'X','required':[False],'forbidden':[False],'evidence':'Required aspect omitted.'} for i in range(1,6)]
  r=grade_summary(C,rubric,grades,{(str(i),"X"):True for i in range(1,6)});self.assertEqual(r['passed'],0);self.assertEqual(r['stable_scored_behavior_cases'],1)
 def test_missing_or_malformed_grades_rejected(self):
  rubric=[{'id':'X','required':['req'],'forbidden':['bad']}]
  for grades in ([],[{'run':str(i),'id':'X','required':['yes'],'forbidden':[False],'evidence':'x'} for i in range(1,6)]):
   with self.assertRaises(ValueError):grade_summary(C,rubric,grades,{(str(i),"X"):True for i in range(1,6)})
 def test_duplicate_case_ids_rejected_by_grade_summary(self):
  rubric=[{'id':'X','required':['req'],'forbidden':[]}]
  grades=[{'run':str(i),'id':'X','required':[True],'forbidden':[],'evidence':'Covered.'} for i in range(1,6)]
  with self.assertRaises(ValueError):grade_summary(C+C,rubric,grades,{(str(i),"X"):True for i in range(1,6)})
 def test_overall_pass_requires_valid_structure(self):
  rubric=[{'id':'X','required':['req'],'forbidden':[]}]
  grades=[{'run':str(i),'id':'X','required':[True],'forbidden':[],'evidence':'Covered.'} for i in range(1,6)]
  validity={(str(i),'X'):i!=5 for i in range(1,6)}
  r=grade_summary(C,rubric,grades,validity)
  self.assertEqual(r['passed'],4);self.assertEqual(r['rubric_passed'],5)
if __name__=='__main__':unittest.main()

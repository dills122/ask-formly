import unittest
from checks import validate_inputs,validate_predictions

def row(i,q='What does Formly do?'):
 return dict(question_id=i,question=q,schema_version='narrow-mentions-v1',mentions=[],status='ok',issues=[])
class InputChecks(unittest.TestCase):
 def test_duplicate_question_rejected_across_ids(self):
  with self.assertRaises(ValueError):validate_inputs([row('a'),row('b')],{'a':'x','b':'x'},[])
 def test_old_question_reuse_rejected(self):
  with self.assertRaises(ValueError):validate_inputs([row('a')],{'a':'x'},[row('old')])
 def test_family_coverage_must_be_exact(self):
  with self.assertRaises(ValueError):validate_inputs([row('a')],{'other':'x'},[])
 def test_grounded_empty_case_allowed(self):
  validate_inputs([row('a')],{'a':'x'},[])
 def test_predictions_missing_duplicate_unknown_rejected(self):
  gold=[row('a'),row('b','How are Formly wrappers used?')]
  for predictions in ([{'id':'a'}],[{'id':'a'},{'id':'a'}],[{'id':'a'},{'id':'c'}]):
   with self.assertRaises(ValueError):validate_predictions(gold,predictions)
  validate_predictions(gold,[{'id':'b'},{'id':'a'}])
if __name__=='__main__':unittest.main()

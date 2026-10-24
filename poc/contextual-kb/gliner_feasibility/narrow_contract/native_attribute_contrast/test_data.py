import unittest
from annotation_contract import build,negatives
class Tests(unittest.TestCase):
 def test_occurrence_context_not_spelling(self):
  row=build('x','In Formly, compare API <api_reference>props</api_reference> with <api_reference>props.label</api_reference>.')
  bad=negatives(row,[('props',1,'clipped_api')]);self.assertEqual(bad[0]['start'],row['question'].rindex('props'))
  with self.assertRaises(ValueError):negatives(row,[('props',0,'clipped_api')])
 def test_ambiguous_default_anchor_fails(self):
  row=build('x','Compare same with same in Formly.')
  with self.assertRaises(ValueError):negatives(row,[('same',None,'ordinary_prose')])
 def test_full_opaque_value_cannot_be_negative(self):
  row=build('x','Formly receives opaque <value>{ x: false }</value>.')
  with self.assertRaises(ValueError):negatives(row,[('{ x: false }',0,'merged_api_value')])
  self.assertEqual(negatives(row,[('x: false',0,'nested_fragment')])[0]['text'],'x: false')
 def test_missing_anchor_and_duplicate_rejected(self):
  row=build('x','Formly API <api_reference>props.label</api_reference>.')
  with self.assertRaises(ValueError):negatives(row,[('absent',0,'clipped_api')])
  with self.assertRaises(ValueError):negatives(row,[('props',0,'clipped_api'),('props',0,'clipped_api')])

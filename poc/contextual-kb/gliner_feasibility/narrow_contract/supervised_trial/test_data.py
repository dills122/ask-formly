import unittest
from data import export,combine
def e(id='x',text="'0' 0"):
 return dict(question_id=id,question=text,schema_version='narrow-mentions-v1',status='ok',issues=[],
 mentions=[dict(kind='model_key',raw="'0'",start=0,end=3),dict(kind='value',raw='0',start=4,end=5)])
class DataTests(unittest.TestCase):
 def test_export_preserves_offsets_and_negatives(self):
  r=export(e(),{})
  self.assertEqual(r['output']['entities']['model_key'],[dict(text="'0'",start=0,end=3)])
  self.assertEqual(r['output']['entities']['value'],[dict(text='0',start=4,end=5)])
  self.assertEqual(len(r['output']['entities']),6)
 def test_ambiguous_excluded(self):
  a=e();a.update(status='needs_review',issues=[dict(reason='role_ambiguous',start=0,end=3)])
  self.assertEqual(combine([a],[]),[])
 def test_duplicate_question_rejected(self):
  with self.assertRaises(ValueError):combine([e('a')],[e('b')])
 def test_bad_span_rejected(self):
  a=e();a['mentions'][0]['end']=2
  with self.assertRaises(ValueError):export(a,{})
if __name__=='__main__':unittest.main()

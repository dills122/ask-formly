import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch
import assessment
from assessment import metrics, extraction_coverage

class AssessmentTests(unittest.TestCase):
 def test_full_assessment_blocks_missing_gold_empty_attempt(self):
  with tempfile.TemporaryDirectory(dir=Path(__file__).parent/'test-output') as tmp:
   root=Path(tmp);(root/'data').mkdir();out=root/'test-output/inference';out.mkdir(parents=True)
   core={'formly_questions':[{'question':'hide'},{'question':'Any information?'}]}
   record={'id':'I01','output':core}
   (root/'data/records.json').write_text(json.dumps([record]))
   mention={'start':0,'end':4,'text':'hide','role':'api_reference'}
   gold=[dict(id='I01-q0',record_id='I01',question_index=0,text='hide',empty_control=False,gold=[mention],alternatives=[]),dict(id='I01-q1',record_id='I01',question_index=1,text='Any information?',empty_control=False,gold=[],alternatives=[])]
   (root/'data/gold.json').write_text(json.dumps(gold))
   plan={'question_plan':core,'search_requests':[{'query':'hide'},{'query':'Any information?'}],'role_hints':[]}
   base=dict(id='I01',plan=plan,extractions=[],extraction_seconds=0,projection_seconds=.01)
   (out/'foundation.jsonl').write_text(json.dumps(base)+'\n')
   for arm in ('1701','1702'):
    model=dict(base,plan=dict(plan,role_hints=[dict(mention,question_index=0,usable_as_filter=False)]),extractions=[dict(question_index=0,text='hide',raw={'entities':{'api_reference':[mention]}},error=None,seconds=.1)])
    (out/(arm+'.jsonl')).write_text(json.dumps(model)+'\n')
   with patch.object(assessment,'HERE',root):assessment.main()
   scores=json.loads((root/'test-output/scores.json').read_text())
   self.assertFalse(scores['1701']['advisory_value_pass'])
   self.assertTrue(scores['1701']['extraction_errors'])
   self.assertGreater(scores['1701']['annotation']['accepted']['combined']['missing'],0)

 def test_absent_empty_question_attempt_is_failure(self):
  errors=extraction_coverage('1701', [{'question':'Any API?'}], [])
  self.assertTrue(errors)
 def test_duplicate_or_wrong_text_attempt_is_failure(self):
  qs=[{'question':'Any API?'}];e={'question_index':0,'text':'Any API?','raw':{'entities':{}},'error':None,'seconds':.1}
  self.assertTrue(extraction_coverage('1701',qs,[e,e]))
  self.assertTrue(extraction_coverage('1701',qs,[dict(e,text='different')]))
 def test_correct_empty_model_and_foundation_coverage(self):
  e={'question_index':0,'text':'Any API?','raw':{'entities':{}},'error':None,'seconds':.1}
  self.assertEqual(extraction_coverage('1701',[{'question':'Any API?'}],[e]),[])
  self.assertEqual(extraction_coverage('foundation',[{'question':'Any API?'}],[]),[])
  self.assertEqual(extraction_coverage('1701',[],[]),[])

 def test_missing_prediction_counts_as_miss(self):
  r=metrics([{'id':'x','gold':[{'start':0,'end':1,'text':'a','role':'api_reference'}]}],{})
  self.assertEqual(r['typed']['fn'],1);self.assertEqual(r['missing'],1)
  self.assertFalse(r['value_gate'])
 def test_wrong_role_preserves_boundary_score_not_typed(self):
  g={'id':'x','gold':[{'start':0,'end':1,'text':'a','role':'api_reference'}]}
  r=metrics([g],{'x':[{'start':0,'end':1,'text':'a','role':'value'}]})
  self.assertEqual(r['typed']['tp'],0);self.assertEqual(r['untyped']['tp'],1)
 def test_false_positive_on_empty_control_blocks_value(self):
  g=[{'id':'x','gold':[]}];p={'x':[{'start':0,'end':1,'text':'a','role':'value'}]}
  r=metrics(g,p);self.assertEqual(r['empty_false_positive_questions'],1);self.assertFalse(r['value_gate'])
 def test_correct_nonempty_passes(self):
  g=[{'id':'x','gold':[{'start':0,'end':1,'text':'a','role':'value'}]}]
  r=metrics(g,{'x':g[0]['gold']});self.assertTrue(r['value_gate'])
 def test_empty_only_is_not_evidence_of_value(self):
  r=metrics([{'id':'x','gold':[]}],{'x':[]});self.assertFalse(r['value_gate'])
if __name__=='__main__':unittest.main()

import copy,unittest
from candidate import validate,build_plan,build_messages,parse_output
class Tests(unittest.TestCase):
 def setUp(self):
  self.request='In Formly, while disabled, can choices change and can selection remain?'
  self.value={'formly_questions':[{'question':'In Formly, while disabled, can choices change?','reason':'Requested update.'},{'question':'In Formly, while disabled, can selection remain?','reason':'Requested retention.'}],'library_constraints':{'formly_version':None,'ui_adapter':None},'condition_bindings':[{'condition':'while disabled','question_indexes':[0,1]}]}
 def test_shared_condition_present_in_every_target(self):
  self.assertEqual(validate(self.request,self.value),self.value)
  self.value['formly_questions'][0]['question']='In Formly, can choices change?'
  with self.assertRaisesRegex(ValueError,'missing condition'):validate(self.request,self.value)
 def test_source_must_ground_condition(self):
  self.value['condition_bindings'][0]['condition']='when hidden'
  with self.assertRaisesRegex(ValueError,'source'):validate(self.request,self.value)
 def test_local_condition_not_forced_into_other_question(self):
  self.value['condition_bindings'][0]['question_indexes']=[0]
  self.value['formly_questions'][1]['question']='In Formly, can selection remain?'
  validate(self.request,self.value)
 def test_invalid_target_indices(self):
  for ids in ([2],[True],[-1],[],[0,0]):
   self.value['condition_bindings'][0]['question_indexes']=ids
   with self.assertRaises(ValueError):validate(self.request,self.value)
 def test_empty_library_plan(self):
  self.value['formly_questions']=[];self.value['condition_bindings']=[]
  self.assertEqual(build_plan(self.request,self.value)['search_requests'],[])
 def test_duplicate_json_keys_rejected(self):
  with self.assertRaises(ValueError):parse_output(self.request,'{"x": 1, "x": 2}')
 def test_hint_independence_and_no_mutation(self):
  saved=copy.deepcopy(self.value);q=self.value['formly_questions'][0]['question'];hint={'question_index':0,'start':3,'end':9,'text':q[3:9],'role':'api_reference'}
  a=build_plan(self.request,self.value);b=build_plan(self.request,self.value,[hint]);c=build_plan(self.request,self.value,[dict(hint,role='value')])
  self.assertEqual(a['search_requests'],b['search_requests']);self.assertEqual(a['search_requests'],c['search_requests']);self.assertEqual(self.value,saved)
  self.assertEqual(b['hint_policy'],'advisory_only');self.assertFalse(b['role_hints'][0]['usable_as_filter'])
 def test_bad_hints_cannot_block_valid_plan(self):
  a=build_plan(self.request,self.value)
  for hints in ('bad',[None],[{'question_index':99}],{'untrusted':'value'}):
   b=build_plan(self.request,self.value,hints);self.assertEqual(a['search_requests'],b['search_requests']);self.assertTrue(b['hint_warnings'])
 def test_quote_boundary_mismatch_ignored(self):
  hint={'question_index':0,'start':3,'end':9,'text':'wrong!','role':'value'}
  b=build_plan(self.request,self.value,[hint]);self.assertEqual(b['role_hints'],[]);self.assertTrue(b['hint_warnings'])
 def test_conflicts_abstain_instead_of_selecting_role(self):
  q=self.value['formly_questions'][0]['question'];h={'question_index':0,'start':3,'end':9,'text':q[3:9],'role':'value'}
  b=build_plan(self.request,self.value,[h,dict(h,role='api_reference')]);self.assertEqual(b['role_hints'],[]);self.assertTrue(b['hint_warnings'])
 def test_invalid_plan_not_repaired_by_hints(self):
  self.value['formly_questions'][0]['question']='Missing condition'
  with self.assertRaises(ValueError):build_plan(self.request,self.value,[])
 def test_prompt_preserves_request_as_data(self):
  self.assertEqual(build_messages(self.request)[1],{'role':'user','content':self.request})
  with self.assertRaises(ValueError):build_messages('')
if __name__=='__main__':unittest.main()

class KnownRegression(unittest.TestCase):
 def test_saved_h07_omission_detected_with_declared_binding(self):
  import json
  from pathlib import Path
  root=Path(__file__).resolve().parent.parent/'refinement_v2'
  request=next(r['request'] for r in json.loads((root/'cases.json').read_text()) if r['id']=='H07')
  original=next(r['output'] for r in json.loads((root/'test-output/beta1.json').read_text()) if r['id']=='H07')
  audited=dict(original,condition_bindings=[{'condition':'if its value still appears among the new options','question_indexes':[0,1]}])
  with self.assertRaisesRegex(ValueError,'missing condition'):validate(request,audited)

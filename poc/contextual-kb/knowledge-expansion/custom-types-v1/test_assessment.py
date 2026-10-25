import json,tempfile,unittest
from pathlib import Path
from assess import prepare
from replay import replay

class AssessmentTests(unittest.TestCase):
 def fixture(self,root,exit_code=0,change_delivery=False):
  packet={'retrieval':{'ids':['f'],'foundation_ids':['f']},'selection':{'queries':[],'status':'unchanged'},'advisory':{'status':'available'},'runtime':{'index_setup_seconds':0}}
  case={'id':'Q','request':'q','required_support':['f'],'category':'test','answer_checks':[]}
  (root/'prompt.json').write_text(json.dumps([case]));(root/'receipt.json').write_text(json.dumps({'exit_code':exit_code,'error':None}))
  answer={'answers':[{'id':'Q','answer':'a','citations':['f'],'gaps':[]}]}
  call={'id':'c','type':'mcp_tool_call','server':'formly','tool':'lookup_formly','arguments':{'request':'q'}}
  delivered=dict(packet,wrong=True) if change_delivery else packet
  events=[{'type':'item.started','item':call},{'type':'item.completed','item':dict(call,status='completed',error=None,result={'structured_content':delivered})},{'type':'item.completed','item':{'type':'agent_message','text':json.dumps(answer)}},{'type':'turn.completed'}]
  (root/'events.jsonl').write_text('\n'.join(json.dumps(e) for e in events))
  p=root/'mcp/audit';p.mkdir(parents=True);(p/'x.json').write_text(json.dumps({'request':'q','seconds':1,'result':packet}))
  return [case]
 def test_nonzero_process_cannot_be_usable_delivery(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);cases=self.fixture(root,exit_code=1)
   self.assertTrue(prepare(root,cases)[0]['delivery_errors'])
 def test_delivered_packet_must_equal_audit(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);cases=self.fixture(root,change_delivery=True)
   self.assertTrue(prepare(root,cases)[0]['delivery_errors'])
 def test_correct_delivery_has_no_errors(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);cases=self.fixture(root)
   self.assertFalse(prepare(root,cases)[0]['delivery_errors'])
 def test_all_missing_replay_writes_report_without_mcp(self):
  import asyncio
  with tempfile.TemporaryDirectory() as t:
   root=Path(t).resolve();asyncio.run(replay(root,[{'id':'Q','request':'q'}],1))
   d=json.loads((root/'paired-r1/results.json').read_text())
   self.assertEqual(d['missing_source_cases'],['Q']);self.assertEqual(d['results'],[])
if __name__=='__main__':unittest.main()

class AssessmentRecoveryTests(unittest.TestCase):
 def test_existing_attempt_directory_is_not_completion(self):
  from assess import assessment_complete
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);(root/'assessment/attempt-1').mkdir(parents=True)
   self.assertFalse(assessment_complete(root))
 def test_corrupt_results_are_not_completion(self):
  from assess import assessment_complete
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);(root/'assessment').mkdir();(root/'assessment/results.json').write_text('{')
   self.assertFalse(assessment_complete(root))

class GradingEvidenceTests(unittest.TestCase):
 def test_grader_sees_source_excerpt_the_caller_could_cite(self):
  from assess import inventory
  fact=inventory()['custom-type-recipe-core/root-and-child-configuration']
  self.assertTrue(any('FormlyFormBuilder' in e.get('excerpt','') for e in fact['evidence']))

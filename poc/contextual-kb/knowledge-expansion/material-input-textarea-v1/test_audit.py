import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import results

class AuditTests(unittest.TestCase):
 def fixture(self,root,changed=None,fetch_id='found',scope='6.3.12'):
  args={'request':'q','plan':{'formly_questions':[]},'formly_version':'6.3.12','ui_adapter':'material'}
  canonical={'id':'Q','tool':'lookup_formly','arguments':args}
  call=copy.deepcopy(canonical)
  if changed:changed(call['arguments'])
  root.joinpath('lookup-calls.json').write_text(json.dumps([canonical]));root.joinpath('cases.json').write_text('[{"id":"Q"}]')
  blocks={n:[] for n in ['batch-1','batch-2','batch-3','discovery-page1','discovery-page2','fetch']}
  blocks['batch-1']=[dict(call,result={'structuredContent':{'status':'ok','facts':[],'questions':[]}})]
  blocks['discovery-page1']=[dict(id='Q',tool='discover_formly_candidates',arguments=dict(args,offset=0,limit=16),result={'structuredContent':{'status':'candidates','candidates':[{'id':'found'}]}})]
  blocks['fetch']=[dict(id='Q',tool='get_formly_facts',arguments={'fact_ids':[fetch_id],'formly_version':scope,'ui_adapter':'material'},result={'structuredContent':{'facts':[{'id':fetch_id}]}})]
  inp=root/'test-output/baseline';out=root/'test-output/qualification/baseline/r1';inp.mkdir(parents=True);out.mkdir(parents=True)
  for name,rows in blocks.items():
   for r in rows:r['operational_or_tool_error']=False
   (inp/(name+'.json')).write_text(json.dumps([{k:r[k] for k in ['id','tool','arguments']} for r in rows]))
   (out/(name+'.json')).write_text(json.dumps(rows));(out/(name+'.receipt.json')).write_text(json.dumps({'expected':len(rows),'attempted':len(rows),'errors':0,'unattempted':[]}));(out/(name+'.stderr')).write_text('OFFLINE_GUARDS_ACTIVE')
 def test_discovered_fact_can_be_fetched_and_initial_remains_separate(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);self.fixture(root)
   with patch.object(results,'HERE',root):initial,completed,raw=results.read_run('baseline',1)
   self.assertEqual(initial['Q']['facts'],[]);self.assertEqual(completed['Q']['facts'],[{'id':'found'}])
 def test_unobserved_fetch_is_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);self.fixture(root,fetch_id='oracle')
   with patch.object(results,'HERE',root),self.assertRaisesRegex(ValueError,'unseen'):results.read_run('baseline',1)
 def test_changed_request_scope_or_plan_is_rejected(self):
  for field,value in [('request','other'),('formly_version','7'),('plan',{'formly_questions':[{'question':'different'}]})]:
   with self.subTest(field=field),tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);self.fixture(root,changed=lambda a:a.update({field:value}))
    with patch.object(results,'HERE',root),self.assertRaisesRegex(ValueError,'frozen'):results.read_run('baseline',1)
 def test_recovery_scope_change_is_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);self.fixture(root,scope='7')
   with patch.object(results,'HERE',root),self.assertRaisesRegex(ValueError,'scope'):results.read_run('baseline',1)

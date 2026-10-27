import unittest
from audit import validate_observation,validate_judgments,compare_repeats

class AuditTests(unittest.TestCase):
 def test_unobserved_fetch_rejected(self):
  with self.assertRaises(ValueError): validate_observation([{'id':'q','tool':'get_formly_facts','arguments':{'fact_ids':['hidden'],'formly_version':'6.3.12','ui_adapter':'material'},'result':{'structuredContent':{'facts':[]}},'operational_or_tool_error':False}],{})
 def test_forged_citation_rejected(self):
  with self.assertRaises(ValueError): validate_judgments([{'id':'q','usable':True,'critical_unsupported_claim':False,'answer':'a','reason':'r','citations':['not-delivered']}],{'q':{'facts':[]}})
 def test_critical_claim_blocks_usable(self):
  with self.assertRaises(ValueError): validate_judgments([{'id':'q','usable':True,'critical_unsupported_claim':True,'answer':'a','reason':'r','citations':[]}],{'q':{'facts':[]}})
 def test_missing_case_rejected(self):
  with self.assertRaises(ValueError): validate_judgments([],{'q':{'facts':[]}})
 def test_changed_packet_not_reused(self):
  with self.assertRaises(ValueError): compare_repeats([{'x':1}],[{'x':2}])
 def test_latency_does_not_change_packet(self):
  compare_repeats([{'id':'q','tool':'lookup_formly','arguments':{},'result':{'structuredContent':{'status':'ok'}},'seconds':1}],[{'id':'q','tool':'lookup_formly','arguments':{},'result':{'structuredContent':{'status':'ok'}},'seconds':2}])
 def test_unsupported_scope_cannot_recover(self):
  plan={'q':{'request':'r','formly_version':'7','ui_adapter':'material','plan':{}}}
  rows=[{'id':'q','tool':'lookup_formly','arguments':plan['q'],'result':{'structuredContent':{'status':'unsupported_scope'}},'operational_or_tool_error':False},{'id':'q','tool':'get_formly_facts','arguments':{'fact_ids':[],'formly_version':'7','ui_adapter':'material'},'result':{'structuredContent':{'facts':[]}},'operational_or_tool_error':False}]
  with self.assertRaises(ValueError):validate_observation(rows,plan)
 def test_recovery_scope_change_rejected(self):
  plan={'q':{'request':'r','formly_version':'6.3.12','ui_adapter':'material','plan':{}}}
  rows=[{'id':'q','tool':'lookup_formly','arguments':plan['q'],'result':{'structuredContent':{'status':'ok','facts':[{'id':'x'}]}},'operational_or_tool_error':False},{'id':'q','tool':'get_formly_facts','arguments':{'fact_ids':['x'],'formly_version':'7','ui_adapter':'material'},'result':{'structuredContent':{'facts':[{'id':'x'}]}},'operational_or_tool_error':False}]
  with self.assertRaises(ValueError):validate_observation(rows,plan)
 def fetch_observation(self, count, calls=1):
  ids=[f'f{i}' for i in range(count)]
  plan={'q':{'request':'r','formly_version':'6.3.12','ui_adapter':'material','plan':{}}}
  rows=[{'id':'q','tool':'lookup_formly','arguments':plan['q'],'result':{'structuredContent':{'status':'ok','facts':[],'questions':[{'omitted_ids':ids}]}},'operational_or_tool_error':False}]
  for _ in range(calls):
   rows.append({'id':'q','tool':'get_formly_facts','arguments':{'fact_ids':ids,'formly_version':'6.3.12','ui_adapter':'material'},'result':{'structuredContent':{'facts':[{'id':i} for i in ids]}},'operational_or_tool_error':False})
  return rows,plan
 def test_seven_observed_ids_exceed_fetch_limit(self):
  rows,plan=self.fetch_observation(7)
  with self.assertRaisesRegex(ValueError,'excessive fetch'):validate_observation(rows,plan)
 def test_six_observed_ids_allowed_for_each_of_two_fetches(self):
  rows,plan=self.fetch_observation(6,calls=2)
  _,completed=validate_observation(rows,plan)
  self.assertEqual(len(completed['q']['facts']),12)
 def test_third_fetch_still_exceeds_recovery_budget(self):
  rows,plan=self.fetch_observation(6,calls=3)
  with self.assertRaisesRegex(ValueError,'Recovery budget exceeded'):validate_observation(rows,plan)
if __name__=='__main__':unittest.main()

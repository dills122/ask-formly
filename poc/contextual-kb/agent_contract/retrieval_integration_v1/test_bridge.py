import copy
from pathlib import Path
import sqlite3
import tempfile
import unittest
from bridge import api_probe, retrieve, relevance, readonly, consistency

class BridgeTests(unittest.TestCase):
 def test_probe_exact_order_unique_only_apis(self):
  hints=[dict(question_index=0,start=20,text='props.disabled',role='api_reference',usable_as_filter=False),dict(question_index=0,start=1,text='resetOnHide',role='api_reference',usable_as_filter=False),dict(question_index=0,start=30,text='props.disabled',role='api_reference',usable_as_filter=False),dict(question_index=0,start=0,text='false',role='value',usable_as_filter=False)]
  self.assertEqual(api_probe(hints,0),'Formly resetOnHide props.disabled')
 def test_full_query_preserved_and_budget_fixed(self):
  class Index:
   def __init__(self):self.calls=[]
   def hybrid(self,q,k):self.calls.append((q,k));return ['a','b'] if q=='original without polling' else ['c','a']
  index=Index();plan={'search_requests':[{'query':'original without polling'}],'role_hints':[dict(question_index=0,start=0,text='API',role='api_reference',usable_as_filter=False)]};old=copy.deepcopy(plan)
  r=retrieve(index,plan,True);self.assertEqual(index.calls,[('original without polling',8),('Formly API',8)]);self.assertEqual(plan,old);self.assertLessEqual(len(r['ids']),8)
 def test_no_hint_no_extra_search(self):
  class Index:
   def hybrid(self,q,k):return ['x']
  r=retrieve(Index(),{'search_requests':[{'query':'q'}],'role_hints':[]},True);self.assertEqual(r['query_count'],1)
 def test_no_questions_no_search(self):
  self.assertEqual(retrieve(None,{'search_requests':[],'role_hints':[]},True)['ids'],[])
 def test_relevance_partial_and_alternatives(self):
  r=relevance(['a','z'],{'relevant_fact_ids':['a','b'],'required_groups':[['a','b']]},8)
  self.assertEqual(r['recall'],.5);self.assertEqual(r['precision'],.125);self.assertTrue(r['complete_groups'])
 def test_unsupported_not_scored_perfect_recall(self):
  r=relevance(['x'],{'relevant_fact_ids':[],'required_groups':[]},8)
  self.assertIsNone(r['recall']);self.assertEqual(r['unsupported_candidates'],1)
 def test_readonly_rejects_write_to_disposable_fixture(self):
  with tempfile.TemporaryDirectory(dir=Path(__file__).parent/'test-output') as td:
   p=Path(td)/'fixture.sqlite';db=sqlite3.connect(p);db.execute('create table x (a integer)');db.commit();db.close()
   with readonly(p) as ro:
    with self.assertRaises(sqlite3.OperationalError):ro.execute('insert into x values (1)')
 def test_consistency_floor_not_rounded_up(self):
  self.assertFalse(consistency(249,30,10)['within_tolerance']);self.assertTrue(consistency(250,30,10)['within_tolerance'])
 def test_empty_not_consistent_evidence(self):self.assertFalse(consistency(0,0,0)['within_tolerance'])
if __name__=='__main__':unittest.main()

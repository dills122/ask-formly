import copy,unittest
from candidate import supplemental_queries,retrieve,utility_pass

CORE={'formly_questions':[{'question':'In Formly, retain a value when hidden without polling?','reason':'Requested'}],'condition_bindings':[{'condition':'when hidden','question_indexes':[0]},{'condition':'without polling','question_indexes':[0]}]}
class Index:
 def __init__(self):self.calls=[]
 def hybrid(self,text,k):
  self.calls.append(text)
  return ['a','b','c','d','e','f','g','h'] if text.startswith('In') else ['z','b','a','c','d','e','f','g']
class TestCandidate(unittest.TestCase):
 def test_exact_conditions_required(self):
  with self.assertRaises(ValueError):supplemental_queries(CORE,[{'question_index':0,'query':'Formly retain a value when hidden?'}])
 def test_complete_ordered_coverage(self):
  for rows in ([],[{'question_index':1,'query':'when hidden without polling'}],[{'question_index':False,'query':'when hidden without polling'}]):
   with self.assertRaises(ValueError):supplemental_queries(CORE,rows)
 def test_nonstring_and_extra_fields_rejected(self):
  for row in ({'question_index':0,'query':False},{'question_index':0,'query':'when hidden without polling','answer':'yes'}):
   with self.assertRaises(ValueError):supplemental_queries(CORE,[row])
 def test_empty_plan_needs_empty_supplement(self):self.assertEqual(supplemental_queries({'formly_questions':[],'condition_bindings':[]},[]),[])
 def test_query_keeps_source_and_budget(self):
  before=copy.deepcopy(CORE);idx=Index();q='Formly retain a value when hidden without polling?'
  result=retrieve(idx,CORE,[{'question_index':0,'query':q}])
  self.assertEqual(idx.calls,[CORE['formly_questions'][0]['question'],q]);self.assertEqual(CORE,before)
  self.assertEqual(len(result['ids']),8);self.assertEqual(len(set(result['ids'])),8);self.assertIsNone(result['supplement_error'])
 def test_invalid_supplement_falls_back_whole_record(self):
  idx=Index();result=retrieve(idx,CORE,[])
  self.assertEqual(idx.calls,[CORE['formly_questions'][0]['question']]);self.assertIsNotNone(result['supplement_error']);self.assertEqual(result['ids'],list('abcdefgh'))
 def test_identical_query_not_double_voted(self):
  idx=Index();result=retrieve(idx,CORE,[{'question_index':0,'query':CORE['formly_questions'][0]['question']}])
  self.assertEqual(result['query_count'],1);self.assertEqual(result['ids'],list('abcdefgh'))
 def test_no_supplement_baseline(self):
  result=retrieve(Index(),CORE,None);self.assertIsNone(result['supplement_error']);self.assertEqual(result['query_count'],1)
 def test_gate_cannot_hide_paired_loss_or_semantics(self):
  base={'recall':.8,'precision':.2,'unsupported_candidates':16};candidate=dict(base,recall=.9)
  self.assertTrue(utility_pass(base,candidate,0,[.01,.02,0],0))
  self.assertFalse(utility_pass(base,candidate,1,[.01,.02,0],0))
  self.assertFalse(utility_pass(base,candidate,0,[.01,-.01,.1],0))
  self.assertFalse(utility_pass(base,candidate,0,[.01,.02,0],1))
 def test_gate_rejects_missing_recall_or_small_gain(self):
  b={'recall':.8,'precision':.2,'unsupported_candidates':0}
  self.assertFalse(utility_pass(b,dict(b,recall=.819),0,[0],0))
  self.assertFalse(utility_pass(b,dict(b,recall=None),0,[0],0))
if __name__=='__main__':unittest.main()

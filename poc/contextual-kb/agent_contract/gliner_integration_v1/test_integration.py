import copy
import unittest
from integration import integrate, score_sets, summarize_times

REQUEST="In Formly, compare props.disabled and hide without polling."
VALUE={'formly_questions':[{'question':REQUEST,'reason':'Compare states.'}], 'library_constraints':{'formly_version':None,'ui_adapter':None},'condition_bindings':[{'condition':'without polling','question_indexes':[0]}]}
def raw(entities):return {'entities':entities}
def mention(text,start=None,end=None):
 a=REQUEST.index(text) if start is None else start
 return {'text':text,'start':a,'end':a+len(text) if end is None else end,'confidence':.9}

class IntegrationTests(unittest.TestCase):
 def test_correct_annotations_keep_all_meaning(self):
  before=copy.deepcopy(VALUE)
  result=integrate(REQUEST,VALUE,lambda q:raw({'api_reference':[mention('props.disabled')]}))
  self.assertEqual(result['plan']['question_plan'],VALUE)
  self.assertEqual(result['plan']['search_requests'],[{'query':REQUEST}])
  self.assertFalse(result['plan']['role_hints'][0]['usable_as_filter'])
  self.assertEqual(VALUE,before)
 def test_exception_keeps_search(self):
  def broken(q):raise RuntimeError('failed')
  result=integrate(REQUEST,VALUE,broken)
  self.assertEqual(result['plan']['search_requests'],[{'query':REQUEST}])
  self.assertEqual(result['plan']['role_hints'],[])
  self.assertIn('RuntimeError',result['extractions'][0]['error'])
 def test_malformed_envelopes_explicitly_fail_open(self):
  for bad in [None,{}, {'entities':[]},{'entities':{'api_reference':None}}, {'entities':{'api_reference':[{}]}}]:
   with self.subTest(bad=bad):
    r=integrate(REQUEST,VALUE,lambda q:bad)
    self.assertEqual(r['plan']['role_hints'],[]);self.assertTrue(r['extractions'][0]['error'])
 def test_invalid_offset_or_unknown_role_ignored(self):
  r=integrate(REQUEST,VALUE,lambda q:raw({'alien':[mention('hide')], 'api_reference':[mention('props.disabled',0)]}))
  self.assertEqual(r['plan']['role_hints'],[]);self.assertEqual(len(r['plan']['hint_warnings']),2)
 def test_cross_role_conflicts_discard_both_not_search(self):
  r=integrate(REQUEST,VALUE,lambda q:raw({'api_reference':[mention('hide')],'value':[mention('hide')]}))
  self.assertEqual(r['plan']['role_hints'],[]);self.assertEqual(len(r['plan']['hint_warnings']),2)
 def test_empty_mentions_and_baseline(self):
  a=integrate(REQUEST,VALUE);b=integrate(REQUEST,VALUE,lambda q:raw({}))
  self.assertEqual(a['plan'],b['plan']);self.assertEqual(a['extractions'],[])
 def test_empty_plan_never_invokes_extractor(self):
  v=copy.deepcopy(VALUE);v['formly_questions']=[];v['condition_bindings']=[]
  r=integrate('Who owns our form?',v,lambda _:self.fail('called'))
  self.assertEqual(r['plan']['search_requests'],[])
 def test_identical_text_occurrences_are_not_collapsed(self):
  q='Formly: hide or hide?';v=copy.deepcopy(VALUE);v['formly_questions'][0]['question']=q;v['condition_bindings']=[]
  r=integrate(q,v,lambda _:raw({'api_reference':[{'text':'hide','start':8,'end':12},{'text':'hide','start':16,'end':20}]}))
  self.assertEqual(len(r['plan']['role_hints']),2)
 def test_semantically_wrong_valid_hint_is_not_claimed_fixed(self):
  r=integrate(REQUEST,VALUE,lambda q:raw({'value':[mention('hide')]}))
  self.assertEqual(r['plan']['role_hints'][0]['role'],'value')
  self.assertEqual(r['plan']['search_requests'],[{'query':REQUEST}])
 def test_invalid_core_remains_an_error(self):
  v=copy.deepcopy(VALUE);v['condition_bindings'][0]['condition']='invented'
  with self.assertRaises(ValueError):integrate(REQUEST,v)
 def test_scoring_counts_wrong_role_as_fp_and_fn(self):
  r=score_sets({(1,4,'api_reference')},{(1,4,'value')})
  self.assertEqual((r['tp'],r['fp'],r['fn']),(0,1,1));self.assertEqual(r['f1'],0)
 def test_empty_scoring_has_no_fake_precision(self):
  r=score_sets(set(),set());self.assertIsNone(r['precision']);self.assertIsNone(r['recall'])
 def test_latency_nearest_rank(self):
  self.assertEqual(summarize_times([1,2,3,4])['p95'],4)

if __name__=='__main__':unittest.main()

import copy
import unittest
from scoring import decode, score_case, aggregate

FIELDS=('targets','request_cues','conditions','negative_constraints','identifiers','literals','versions','ui_adapters','references','resolved_antecedents','unresolved_references')
Q='Without x, set foo to 0 and read foo.'
def span(t,start=0):
 a=Q.index(t,start);return dict(text=t,start=a,end=a+len(t))
def fixture():
 a={k:[] for k in FIELDS};a.update(target_anchor=span('foo'),targets=[span('foo')],request_cues=[span('set')],negative_constraints=[span('Without x')],identifiers=[span('foo')],literals=[span('0')])
 b=copy.deepcopy(a);b.update(target_anchor=span('foo',19),targets=[span('foo',19)],request_cues=[span('read')],identifiers=[span('foo',19)],literals=[])
 gold=dict(id='X',question=Q,status='clear',aspects=[a,b],entities={'api':[span('foo'),span('foo',19)],'literal':[span('0')]},relations=[dict(kind='has_value',head=span('foo'),tail=span('0'))])
 raw=dict(request=copy.deepcopy(gold['aspects']),entities=copy.deepcopy(gold['entities']),interpretation={'label':'clear'},relation_extraction={'has_value':[dict(head=span('foo'),tail=span('0'))]})
 return gold,raw
class ScoringTests(unittest.TestCase):
 def test_permutation_complete(self):
  g,r=fixture();r['request'].reverse();self.assertTrue(score_case(g,decode(Q,r))['exact_complete'])
 def test_missing_ask_not_complete(self):
  g,r=fixture();r['request'].pop();s=score_case(g,decode(Q,r));self.assertFalse(s['exact_complete']);self.assertEqual(s['predicted_aspects'],1)
 def test_extra_ask_not_complete(self):
  g,r=fixture();r['request'].append(copy.deepcopy(r['request'][0]));self.assertFalse(score_case(g,decode(Q,r))['exact_complete'])
 def test_lost_negation(self):
  g,r=fixture();r['request'][1]['negative_constraints']=[];s=score_case(g,decode(Q,r));self.assertEqual(s['categories']['negative_constraints']['matched'],1);self.assertFalse(s['exact_complete'])
 def test_wrong_occurrence_relation(self):
  g,r=fixture();r['relation_extraction']['has_value'][0]['head']=span('foo',19);s=score_case(g,decode(Q,r));self.assertEqual(s['categories']['relations']['matched'],0)
 def test_invalid_span_never_repaired(self):
  g,r=fixture();r['request'][0]['target_anchor']['text']='bar'
  with self.assertRaises(ValueError):decode(Q,r)
 def test_absent_records_are_empty(self):
  g,r=fixture();del r['request'];self.assertEqual(decode(Q,r)['aspects'],[])
 def test_ambiguity_wrong_fails(self):
  g,r=fixture();r['interpretation']['label']='needs_clarification';self.assertFalse(score_case(g,decode(Q,r))['exact_complete'])
 def test_missing_required_target_invalid(self):
  g,r=fixture();del r['request'][0]['target_anchor']
  with self.assertRaises(ValueError):decode(Q,r)
 def test_empty_denominators_not_pass(self):
  g,r=fixture();s=aggregate([score_case(g,decode(Q,r))]);self.assertIsNone(s['categories']['conditions']['precision'])
if __name__=='__main__':unittest.main()

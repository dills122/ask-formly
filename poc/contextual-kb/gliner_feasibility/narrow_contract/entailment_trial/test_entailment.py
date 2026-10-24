import unittest
from entailment import marked, decide, simulate, assess
class Tests(unittest.TestCase):
 def test_occurrence_and_unicode(self):
  text="'é' then 'é'"; self.assertEqual(marked(text,9,12),"'é' then <mention>'é'</mention>")
 def test_bad_offsets_and_marker(self):
  for args in [('x',-1,1),('x',0,2),('<mention>x',0,1)]:
   with self.assertRaises(ValueError):marked(*args)
 def test_absolute_support_required(self):
  self.assertIsNone(decide([.5,.1,.1,.1,.1,.1,.1])['role'])
 def test_margin_and_multi_support(self):
  self.assertIsNone(decide([.9,.85,.1,.1,.1,.1,.1])['role'])
 def test_none_is_not_an_entity_role(self):
  self.assertEqual(decide([.01]*6+[.95])['reason'],'no_entity')
 def test_nonfinite_rejected(self):
  with self.assertRaises(ValueError):decide([float('nan')]*7)
 def test_no_span_creation_or_mutation(self):
  raw={(0,1,'value')}; scores={(0,1):[.95,.01,.01,.01,.01,.01,.01]}
  self.assertEqual(simulate(raw,scores),{(0,1,'api_reference')});self.assertEqual(raw,{(0,1,'value')})
  with self.assertRaises(ValueError):simulate(raw,{(1,2):scores[0,1]})
 def test_abstention_retains_original_and_conflict(self):
  raw={(0,1,'value'),(0,1,'registration_name')}
  self.assertEqual(simulate(raw,{(0,1):[.1]*7}),raw)
  self.assertEqual(simulate(raw,{(0,1):[.01]*6+[.99]}),raw)
 def test_regression_and_repair_count(self):
  rows=[dict(id='x',text='ab',gold=[[0,1,'value'],[1,2,'value']],before=[[0,1,'value'],[1,2,'api_reference']],scores=[dict(start=0,end=1,p=[.99,.01,.01,.01,.01,.01,.01]),dict(start=1,end=2,p=[.01,.01,.01,.99,.01,.01,.01])])]
  s=assess(rows);self.assertEqual(s['lost_correct'],1);self.assertEqual(s['gained_correct'],1);self.assertFalse(s['gate_passed'])
 def test_no_repairs_is_not_success(self):
  row=dict(id='x',text='a',gold=[[0,1,'value']],before=[[0,1,'value']],scores=[dict(start=0,end=1,p=[.01,.01,.01,.99,.01,.01,.01])])
  self.assertFalse(assess([row])['gate_passed'])
if __name__=='__main__':unittest.main()

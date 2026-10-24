import unittest
from experiment import annotation, verify_splits, paired_decision, challenge_hashes

class ExperimentTests(unittest.TestCase):
 def test_challenge_manifest_ignores_metadata(self):
  self.assertEqual(challenge_hashes({"schema_version":"challenge-freeze-v1","files":{"x":{"sha256":"abc","bytes":4}}}),{"x":"abc"})
 def test_occurrences_keep_quotes_and_distinct_roles(self):
  r=annotation('X','Use <model_key>"same"</model_key> and <value>"same"</value>.')
  self.assertEqual(r['question'],'Use "same" and "same".')
  self.assertEqual([(m['kind'],m['start'],m['end'],m['raw']) for m in r['mentions']],
   [('model_key',4,10,'"same"'),('value',15,21,'"same"')])
 def test_unmarked_claim_stays_empty(self):
  self.assertEqual(annotation('X','Does Formly guarantee "always"?')['mentions'],[])
 def test_bad_markup_rejected(self):
  for s in ('<value>x','<bogus>x</bogus>','<value><model_key>x</model_key></value>'):
   with self.assertRaises(ValueError):annotation('X',s)
 def test_duplicate_questions_and_ids_rejected(self):
  a=annotation('A','one');b=annotation('B','two')
  verify_splits([a],[b])
  for bad in (a,annotation('B','one'),annotation('A','different')):
   with self.assertRaises(ValueError):verify_splits([a],[bad])
 def test_paired_gate_requires_both_and_regression_guard(self):
  def report(f1,exact,invalid=0):return {'accepted':{'all':{'f1':f1}},'exact':exact,'invalid':invalid,'groups':{'family':{'values':{'accepted':{'f1':f1}}}}}
  before=report(.5,10);after=report(.7,15);reg=report(.95,22)
  pairs=[(before,after,reg,reg)]*2
  self.assertTrue(paired_decision(pairs)['improved'])
  self.assertFalse(paired_decision(pairs[:1])['improved'])
  self.assertFalse(paired_decision([(before,before,reg,reg),pairs[1]])['improved'])
  self.assertFalse(paired_decision([(before,after,reg,report(.92,22)),pairs[1]])['improved'])
  self.assertFalse(paired_decision([(before,after,reg,report(.96,22,1)),pairs[1]])['improved'])
 def test_family_regression_not_hidden_by_overall_gain(self):
  b={'accepted':{'all':{'f1':.5}},'exact':5,'invalid':0,'groups':{'family':{'x':{'accepted':{'f1':.9}}}}}
  a={'accepted':{'all':{'f1':.8}},'exact':10,'invalid':0,'groups':{'family':{'x':{'accepted':{'f1':.8}}}}}
  self.assertFalse(paired_decision([(b,a,b,b)]*2)['improved'])
if __name__=='__main__':unittest.main()

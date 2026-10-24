import copy
import unittest
from shadow import collect, summarize, decision, validate

def row():return dict(id='q',text='abc def',gold=[[0,3,'api_reference']],probes=[dict(start=0,end=3,expected_role='api_reference',family='gold'),dict(start=1,end=3,expected_role=None,family='clipped')])
def raw(role='value'):return {'entities':{role:[dict(start=0,end=3,text='abc',confidence=.8)]}}
def scores(role='api_reference'):
 from shadow import ROLES
 return [.9]+[.9 if r==role else .01 for r in ROLES]

class Tests(unittest.TestCase):
 def test_operational_only_baseline_offsets_and_original_unchanged(self):
  calls=[];source=raw();saved=copy.deepcopy(source)
  def score(text,offsets):calls.append(offsets);return {s:scores() for s in offsets}
  result=collect([row()],lambda text:source,score)
  self.assertEqual(calls,[[(0,3)],[(0,3),(1,3)]])
  self.assertEqual(source,saved);self.assertEqual(result[0]['raw'],saved)
 def test_no_baseline_mentions_does_not_use_gold_as_operational_candidates(self):
  calls=[]
  def score(text,offsets):calls.append(offsets);return {s:scores() for s in offsets}
  result=collect([row()],lambda text:{'entities':{}},score)
  self.assertEqual(result[0]['operational_scores'],[]);self.assertEqual(len(calls),1)
 def test_repair_opportunity_not_applied(self):
  result=collect([row()],lambda text:raw(),lambda t,offsets:{s:scores() for s in offsets})
  d=summarize(result)
  self.assertEqual(d['wrong_role_repair_opportunities'],1);self.assertEqual(d['baseline_correct'],0)
  self.assertEqual(result[0]['raw'],raw())
 def test_correct_mention_harm_and_abstention_separate(self):
  for probs,wrong,abstain in [(scores('value'),1,0),([.1]*7,0,1)]:
   result=collect([row()],lambda t:raw('api_reference'),lambda t,offsets:{s:probs for s in offsets})
   d=summarize(result);self.assertEqual(d['correct_wrong_role_endorsements'],wrong);self.assertEqual(d['correct_abstentions'],abstain)
 def test_unsupported_not_learned_rejection(self):
  result=collect([row()],lambda t:raw(),lambda t,offsets:{s:None for s in offsets})
  d=summarize(result);self.assertEqual(d['oracle_negative_rejected'],0);self.assertEqual(d['oracle_negative_unsupported'],1)
 def test_invalid_scores_fail_and_multirole_abstains(self):
  with self.assertRaises(ValueError):decision([float('inf')]*7)
  self.assertEqual(decision([.9,.9,.9,0,0,0,0])['reason'],'multiple_roles')
 def test_score_coverage_mismatch_fails(self):
  with self.assertRaises(ValueError):collect([row()],lambda t:raw(),lambda t,o:{})
 def test_duplicate_and_overlapping_gold_rejected(self):
  a=row();a['gold'].append([1,2,'value'])
  with self.assertRaises(ValueError):validate([a])
  with self.assertRaises(ValueError):validate([row(),row()])
 def test_probe_inventory_mismatch_rejected(self):
  a=row();a['probes']=[]
  with self.assertRaises(ValueError):validate([a])
 def test_cached_baseline_drift_rejected(self):
  a=row();a['expected_raw']={'entities':{}}
  with self.assertRaises(ValueError):collect([a],lambda t:raw(),lambda t,o:{s:scores() for s in o})

if __name__=='__main__':unittest.main()

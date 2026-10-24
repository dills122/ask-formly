import unittest
from assessment import summary,validate_coverage,assess

def row(identity,arm,recall,complete=True,batch=1):
 m=dict(recall=recall,precision=.25,ndcg=recall,mrr=1 if recall else 0,group_recall=1 if complete else .5,complete_groups=complete,unsupported_candidates=8 if recall is None else 0)
 return dict(id=identity,arm=arm,batch=batch,metrics={'4':m,'8':m},seconds=.1,query_count=1,query_characters=20,ids=['a'],supplement_error=None,foundation_error=None)
class TestAssessment(unittest.TestCase):
 def test_unsupported_excluded_only_from_recall(self):
  s=summary([row('x','foundation',.5),row('y','foundation',None)],'8')
  self.assertEqual(s['recall'],.5);self.assertEqual(s['cases'],2);self.assertEqual(s['supported'],1);self.assertEqual(s['unsupported_candidates'],8)
 def test_missing_duplicate_or_unexpected_arms_fail(self):
  records=[dict(id='x',batch=1)]
  for rows in ([row('x','foundation',1)],[row('x','foundation',1),row('x','foundation',1)],[row('x','foundation',1),row('x','other',1)]):
   with self.assertRaises(ValueError):validate_coverage(rows,records)
 def test_correct_coverage(self):validate_coverage([row('x','foundation',1),row('x','context',1)],[dict(id='x',batch=1)])
 def test_paired_loss_blocks_despite_net_recovery(self):
  records=[dict(id='x',batch=1),dict(id='y',batch=1)]
  rows=[row('x','foundation',.5,True),row('x','context',.9,False),row('y','foundation',.5,False),row('y','context',.9,True)]
  semantic=[dict(id=i,foundation_pass=True,supplement_pass=True,issues=[]) for i in ('x','y')]
  report=assess(rows,records,semantic);self.assertEqual(report['paired_group_losses']['8'],['x']);self.assertFalse(report['utility_pass'])
 def test_semantic_failure_not_hidden_by_retrieval_improvement(self):
  records=[dict(id='x',batch=1)];rows=[row('x','foundation',.5),row('x','context',1)]
  sem=[dict(id='x',foundation_pass=True,supplement_pass=False,issues=['dropped condition'])]
  self.assertFalse(assess(rows,records,sem)['utility_pass'])
 def test_optional_failure_does_not_disqualify_foundation(self):
  records=[dict(id='x',batch=1)];rows=[row('x','foundation',1),row('x','context',1)]
  rows[1]['supplement_error']='bad optional query'
  sem=[dict(id='x',foundation_pass=True,supplement_pass=False,issues=['missing condition'])]
  report=assess(rows,records,sem)
  self.assertTrue(report['consistent_floor']['foundation']);self.assertFalse(report['consistent_floor']['context'])
 def test_consistency_uses_each_batch(self):
  records=[dict(id='x',batch=1),dict(id='y',batch=2)]
  rows=[row('x',a,1,batch=1) for a in ('foundation','context')]+[row('y',a,.85,batch=2) for a in ('foundation','context')]
  sem=[dict(id=i,foundation_pass=True,supplement_pass=True,issues=[]) for i in ('x','y')]
  self.assertFalse(assess(rows,records,sem)['consistent_floor']['foundation'])
if __name__=='__main__':unittest.main()

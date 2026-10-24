import unittest
from score import evaluate
from contract import envelope
class ScoringTests(unittest.TestCase):
 def test_complete_empty_and_missing(self):
  q=[dict(id='x',parent='P',family='empty',origin='developer_diagnostic',question='Formly')]
  g={'x':envelope('x','Formly',[])}
  self.assertEqual(evaluate(q,g,[])['exact'],0)
  self.assertEqual(evaluate(q,g,[dict(id='x',output={'entities':{}},seconds=0)])['exact'],1)
 def test_duplicate_id_rejected(self):
  with self.assertRaises(ValueError):evaluate([dict(id='x')],{},[dict(id='x'),dict(id='x')])
 def test_overlap_raw_kept_accepted_empty(self):
  q=[dict(id='x',parent='P',family='value',origin='saved_v2',question='false')]
  g={'x':envelope('x','false',[dict(kind='value',raw='false',start=0,end=5)])}
  r=[dict(id='x',output={'entities':{'value':[dict(text='false',start=0,end=5)],'model_key':[dict(text='false',start=0,end=5)]}},seconds=1)]
  s=evaluate(q,g,r)
  self.assertEqual(s['raw']['all']['tp'],1);self.assertEqual(s['raw']['all']['fp'],1)
  self.assertEqual(s['accepted']['all']['fn'],1);self.assertEqual(s['invalid'],1)
if __name__=='__main__':unittest.main()

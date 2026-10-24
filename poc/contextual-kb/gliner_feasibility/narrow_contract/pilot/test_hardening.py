import json,unittest
from pathlib import Path
from hardened import adapt,score_case
from contract import envelope,adapt as frozen_adapt,score_case as frozen_score
class HardenedTests(unittest.TestCase):
 def test_nonobject_inputs_return_error(self):
  for row in (42,True,False,[],['error'],'text'):
   e,raw,error=adapt('q','false',row)
   self.assertEqual(e['status'],'extraction_error');self.assertEqual(raw,[])
   self.assertEqual(e['issues'][0]['reason'],'invalid_output')
 def test_nonobject_scoring_loses_recall(self):
  g=envelope('q','false',[dict(kind='value',raw='false',start=0,end=5)])
  for row in (42,True,[], 'text'):
   s=score_case(g,row)
   self.assertEqual(s['accepted']['fn'],1);self.assertFalse(s['exact'])
 def test_saved_prediction_parity(self):
  p=Path(__file__).resolve().parent
  gold={r['question_id']:r for r in json.loads((p/'gold.json').read_text())}
  rows=[json.loads(l) for l in (p/'test-output/predictions.jsonl').read_text().splitlines()]
  self.assertEqual(len(rows),48)
  for row in rows:
   g=gold[row['id']]
   self.assertEqual(adapt(g['question_id'],g['question'],row),frozen_adapt(g['question_id'],g['question'],row))
   self.assertEqual(score_case(g,row),frozen_score(g,row))
if __name__=='__main__':unittest.main()

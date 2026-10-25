import tempfile,unittest,json
from pathlib import Path
from summarize import summary
class SummaryTests(unittest.TestCase):
 def test_missing_jobs_stay_in_denominator(self):
  with tempfile.TemporaryDirectory() as t:
   report=summary(Path(t),[{'id':'Q','category':'custom-type'}],3)
   self.assertEqual(len(report['rounds']),6)
   for row in report['rounds']:self.assertEqual((row['usable'],row['total']),(0,1))
 def test_duplicate_assessments_are_not_cherry_picked(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)
   for batch in [1,2]:
    p=root/f'r1-b{batch}-candidate/assessment';p.mkdir(parents=True)
    (p/'results.json').write_text(json.dumps({'rows':[{'id':'Q','usable':True}]}))
   report=summary(root,[{'id':'Q','category':'custom-type'}],1)
   self.assertEqual(report['rounds'][1]['usable'],0)
if __name__=='__main__':unittest.main()

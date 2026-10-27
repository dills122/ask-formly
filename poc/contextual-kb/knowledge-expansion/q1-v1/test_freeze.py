import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import evaluate
class FreezeTests(unittest.TestCase):
 def test_missing_run_freeze_rejected(self):
  with tempfile.TemporaryDirectory() as d,patch.object(evaluate,'HERE',Path(d)),patch.object(evaluate,'preserved'),patch.object(evaluate,'checked_database'):
   (Path(d)/'assessment-freeze.json').write_text(json.dumps({'files':{}}))
   with self.assertRaises(FileNotFoundError):evaluate.verify()
 def test_missing_assessment_freeze_rejected(self):
  with tempfile.TemporaryDirectory() as d,patch.object(evaluate,'HERE',Path(d)),patch.object(evaluate,'preserved'),patch.object(evaluate,'checked_database'):
   (Path(d)/'freeze.json').write_text(json.dumps({'files':{}}))
   with self.assertRaises(FileNotFoundError):evaluate.verify()
if __name__=='__main__':unittest.main()

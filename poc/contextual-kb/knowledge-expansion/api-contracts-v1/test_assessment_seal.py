import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import report
from candidate import digest

class AssessmentSealTests(unittest.TestCase):
 def fixture(self,tmp):
  root=Path(tmp).resolve();p=root/'test-output/assessment/API/completed-candidate-API.json';p.parent.mkdir(parents=True);p.write_text('[{"usable":true}]')
  (root/'assessment-freeze.json').write_text(json.dumps({'files':{str(p.relative_to(root)):digest(p)}}));return root,p
 def test_valid_seal(self):
  with tempfile.TemporaryDirectory() as tmp:
   root,p=self.fixture(tmp)
   with patch.object(report,'HERE',root):report.verify_assessment_seal()
 def test_changed_answer_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   root,p=self.fixture(tmp);p.write_text('[{"usable":false}]')
   with patch.object(report,'HERE',root):
    with self.assertRaises(ValueError):report.verify_assessment_seal()
 def test_unsealed_file_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   root,p=self.fixture(tmp);p.with_name('extra.json').write_text('[]')
   with patch.object(report,'HERE',root):
    with self.assertRaises(ValueError):report.verify_assessment_seal()
 def test_escape_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   root,p=self.fixture(tmp);(root/'assessment-freeze.json').write_text(json.dumps({'files':{'../escape.json':'x'}}))
   with patch.object(report,'HERE',root):
    with self.assertRaises(ValueError):report.verify_assessment_seal()
 def test_main_requires_seal_before_scoring(self):
  with tempfile.TemporaryDirectory() as tmp,patch.object(report,'HERE',Path(tmp)),patch.object(report,'preserved') as preserved:
   with self.assertRaises(FileNotFoundError):report.main()
   preserved.assert_not_called()

if __name__=='__main__':unittest.main()

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import run

class Tests(unittest.TestCase):
 def test_review_must_bind_data_and_detect_drift(self):
  with tempfile.TemporaryDirectory(dir=run.HERE/'test-output') as tmp:
   root=Path(tmp);data=root/'data';data.mkdir();new=data/'new.json';adj=data/'adj.json';rev=data/'review.json'
   new.write_text('[]');adj.write_text('[]')
   with patch.object(run,'HERE',root):
    rev.write_text(json.dumps(dict(verdict='ready',independent=True,bindings={})))
    with self.assertRaises(ValueError):run.authorize(new,adj,rev)
    binding={str(p):run.digest(p) for p in (new,adj)}
    rev.write_text(json.dumps(dict(verdict='ready',independent=True,bindings=binding)))
    self.assertEqual(run.authorize(new,adj,rev),binding)
    new.write_text('[1]')
    with self.assertRaises(ValueError):run.authorize(new,adj,rev)

if __name__=='__main__':unittest.main()

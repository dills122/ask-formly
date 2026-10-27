import hashlib,json,sqlite3,tempfile,unittest
from pathlib import Path
from contextlib import closing
from unittest.mock import patch
import candidate

class AcceptedBaselineTests(unittest.TestCase):
 def fixture(self,tmp):
  root=Path(tmp).resolve();source=root/'accepted';source.mkdir();auth=source/'authored';auth.mkdir();a=auth/'a.json';a.write_text('{}');catalog=source/'catalog.json';catalog.write_text('{}');db=source/'knowledge.sqlite'
  with closing(sqlite3.connect(db)) as c:
   c.execute('create table facts (id text)');c.executemany('insert into facts values (?)',[(str(i),) for i in range(176)])
   c.execute('create table documents (id text)');c.executemany('insert into documents values (?)',[(str(i),) for i in range(33)]);c.commit()
  data=dict(database='accepted/knowledge.sqlite',sha256=candidate.digest(db),authored='accepted/authored',catalog='accepted/catalog.json',counts=dict(facts=176,documents=33),inputs={str(p.relative_to(root)):candidate.digest(p) for p in [a,catalog]})
  (root/'accepted-baseline.json').write_text(json.dumps(data));return root,data
 def test_selects_frozen_176_inputs_and_db(self):
  with tempfile.TemporaryDirectory() as tmp:
   root,data=self.fixture(tmp)
   with patch.object(candidate,'HERE',root),patch.object(candidate,'POC',root):
    authored,catalog,db=candidate.accepted_inputs()
    self.assertEqual(authored,root/'accepted/authored');self.assertEqual(db,root/'accepted/knowledge.sqlite')
 def test_drift_rejected_before_build(self):
  for target in ['accepted/authored/a.json','accepted/knowledge.sqlite','accepted/catalog.json']:
   with tempfile.TemporaryDirectory() as tmp:
    root,data=self.fixture(tmp);(root/target).write_bytes(b'changed')
    with patch.object(candidate,'HERE',root),patch.object(candidate,'POC',root):
     with self.assertRaises(ValueError):candidate.accepted_inputs()
 def test_escape_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   root,data=self.fixture(tmp);data['database']='../outside.sqlite';(root/'accepted-baseline.json').write_text(json.dumps(data))
   with patch.object(candidate,'HERE',root),patch.object(candidate,'POC',root):
    with self.assertRaises(ValueError):candidate.accepted_inputs()

if __name__=='__main__':unittest.main()

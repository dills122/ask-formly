import sqlite3,tempfile,unittest
from unittest.mock import patch
import candidate
from contextlib import closing
from pathlib import Path
from candidate import compare_rows,verify_candidate_counts

class CandidateTests(unittest.TestCase):
 def test_all_versioned_tables_must_preserve_accepted_rows(self):
  with tempfile.TemporaryDirectory() as tmp:
   old=Path(tmp)/'old.sqlite';new=Path(tmp)/'new.sqlite'
   for path in (old,new):
    with closing(sqlite3.connect(path)) as db:
     for table in ('documents','facts','evidence','fact_evidence','fact_links','applicability','applicability_evidence','evidence_releases'):
      db.execute('CREATE TABLE '+table+' (value TEXT)');db.execute('INSERT INTO '+table+' VALUES (?)',('old',))
      if path==new:db.execute('INSERT INTO '+table+' VALUES (?)',('new',))
     db.commit()
   self.assertTrue(all(v==2 for v in compare_rows(old,new).values()))
   with closing(sqlite3.connect(new)) as db:
    db.execute("DELETE FROM applicability WHERE value='old'");db.commit()
   with self.assertRaisesRegex(ValueError,'applicability'):compare_rows(old,new)
 def test_build_requires_freeze_before_creating_outputs(self):
  with tempfile.TemporaryDirectory() as tmp,patch.object(candidate,"HERE",Path(tmp).resolve()),patch.object(candidate,"preserved",return_value={}):
   with self.assertRaises(FileNotFoundError):candidate.build()
   self.assertEqual(list(Path(tmp).iterdir()),[])

 def test_expected_size_is_fixed(self):
  verify_candidate_counts({'facts':176,'documents':33})
  with self.assertRaises(ValueError):verify_candidate_counts({'facts':175,'documents':33})

 def test_runtime_database_wiring_freeze_detects_drift(self):
  import json
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);db=root/'build/knowledge.sqlite';db.parent.mkdir();db.write_bytes(b'db')
   (root/'baseline-state.json').write_text(json.dumps({'installed_db_sha256':candidate.digest(db),'files':{}}))
   wiring=root/'databases.json';wiring.write_text('original')
   (root/'run-freeze.json').write_text(json.dumps({'files':{'databases.json':candidate.digest(wiring)}}))
   with patch.object(candidate,'HERE',root),patch.object(candidate,'POC',root):
    candidate.preserved();wiring.write_text('changed')
    with self.assertRaisesRegex(ValueError,'Preservation mismatch'):candidate.preserved()

if __name__=='__main__':unittest.main()

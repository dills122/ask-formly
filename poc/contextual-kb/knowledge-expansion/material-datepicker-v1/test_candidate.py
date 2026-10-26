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
  verify_candidate_counts({'facts':104,'documents':23})
  with self.assertRaises(ValueError):verify_candidate_counts({'facts':103,'documents':23})

if __name__=='__main__':unittest.main()

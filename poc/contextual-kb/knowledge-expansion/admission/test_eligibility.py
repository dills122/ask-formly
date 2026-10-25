import importlib.util
from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import unittest

from eligibility import verify_retrieval_eligibility

POC=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('actual_frozen_question_pilot',POC/'kbcompiler/question_pilot.py')
runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(runtime)

class EligibilityTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve()

    def database(self,name,rows):
        path=self.root/name
        with closing(sqlite3.connect(path)) as db, db:
            db.execute('CREATE TABLE documents (id TEXT PRIMARY KEY, formly_version TEXT, adapter TEXT)')
            db.execute('CREATE TABLE facts (id TEXT PRIMARY KEY,doc_id TEXT)')
            for fact,version,adapter in rows:
                db.execute('INSERT INTO documents VALUES (?,?,?)',(fact,version,adapter))
                db.execute('INSERT INTO facts VALUES (?,?)',(fact,fact))
        return path

    def test_mixed_document_is_rejected_before_live_comparison(self):
        candidate=self.database('candidate.sqlite',[('extension/new',runtime.BASELINE,'mixed')])
        with self.assertRaisesRegex(ValueError,'extension/new.*mixed'):
            verify_retrieval_eligibility(candidate)

    def test_actual_runtime_core_material_profile_is_used_and_additions_reported(self):
        accepted=self.database('accepted.sqlite',[('old',runtime.BASELINE,runtime.ADAPTERS[0])])
        candidate=self.database('candidate.sqlite',[('old',runtime.BASELINE,runtime.ADAPTERS[0]),('new',runtime.BASELINE,runtime.ADAPTERS[1])])
        before={p:p.read_bytes() for p in (accepted,candidate)}
        report=verify_retrieval_eligibility(candidate,accepted)
        self.assertEqual(report['profile']['baseline'],runtime.BASELINE)
        self.assertEqual(report['profile']['adapters'],list(runtime.ADAPTERS))
        self.assertEqual(report['new_fact_ids'],['new'])
        self.assertEqual(report['eligible_fact_ids'],['new','old'])
        for path,data in before.items():self.assertEqual(path.read_bytes(),data)

    def test_wrong_version_rejected(self):
        candidate=self.database('candidate.sqlite',[('wrong-version','7.0.0',runtime.ADAPTERS[0])])
        with self.assertRaisesRegex(ValueError,'wrong-version.*7.0.0'):
            verify_retrieval_eligibility(candidate)

    def test_orphan_fact_cannot_disappear_in_inner_join(self):
        candidate=self.database('candidate.sqlite',[])
        with closing(sqlite3.connect(candidate)) as db, db:db.execute("INSERT INTO facts VALUES ('orphan','absent')")
        with self.assertRaisesRegex(ValueError,'orphan.*missing document'):
            verify_retrieval_eligibility(candidate)

    def test_missing_database_is_not_created(self):
        candidate=self.root/'missing.sqlite'
        with self.assertRaises((FileNotFoundError,sqlite3.OperationalError)):
            verify_retrieval_eligibility(candidate)
        self.assertFalse(candidate.exists())

if __name__=='__main__':unittest.main()

import json, os, tempfile, unittest
from pathlib import Path
from candidate import fresh_directory, assert_digest, verify_superset

class SafetyTests(unittest.TestCase):
    def test_refuses_existing_output_even_if_empty(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t).resolve(); (root/'candidate-build').mkdir()
            with self.assertRaises(FileExistsError): fresh_directory(root,'candidate-build')
    def test_refuses_parent_escape(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValueError): fresh_directory(Path(t).resolve(),'../outside')
    def test_refuses_symlinked_root(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t).resolve(); (root/'real').mkdir(); (root/'link').symlink_to(root/'real',target_is_directory=True)
            with self.assertRaises(ValueError): fresh_directory(root/'link','candidate-build')
    def test_refuses_dangling_output_symlink(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t).resolve(); (root/'candidate-build').symlink_to(root/'missing')
            with self.assertRaises(FileExistsError): fresh_directory(root,'candidate-build')
    def test_creates_only_new_child(self):
        with tempfile.TemporaryDirectory() as t:
            p=fresh_directory(Path(t).resolve(),'candidate-build'); self.assertTrue(p.is_dir())
    def test_detects_changed_bytes(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'db'; p.write_bytes(b'changed')
            with self.assertRaises(ValueError): assert_digest(p,'0'*64)
    def test_superset_rejects_lost_original_row(self):
        import sqlite3
        with tempfile.TemporaryDirectory() as t:
            a=Path(t)/'a'; b=Path(t)/'b'
            for path,value in [(a,'original'),(b,'changed')]:
                with sqlite3.connect(path) as db:
                    for table in ['documents','facts','evidence','fact_evidence','fact_links']:
                        db.execute(f'create table {table}(id text)'); db.execute(f'insert into {table} values (?)',(value,))
            with self.assertRaises(ValueError): verify_superset(a,b)

if __name__=='__main__': unittest.main()

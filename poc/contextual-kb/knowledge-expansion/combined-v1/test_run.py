import tempfile, unittest
from pathlib import Path
import run

class CombinedTests(unittest.TestCase):
    def test_frozen_repeats_use_candidate_and_exact_batches(self):
        cases=[{'id':str(i)} for i in range(30)]
        with tempfile.TemporaryDirectory() as tmp:
            calls=[]
            def agent(batch,arm,seed,path):
                calls.append((list(batch),arm,seed,Path(path).name));return {'exit_code':0}
            run.execute(cases,Path(tmp)/'fresh',agent)
        self.assertEqual(len(calls),18)
        for repeat,seed in [(1,1701),(2,1702),(3,1701)]:
            rows=calls[(repeat-1)*6:repeat*6]
            self.assertEqual([r for call in rows for r in call[0]],cases)
            self.assertTrue(all(call[1]=='candidate' and call[2]==seed for call in rows))
            self.assertEqual([r[3] for r in rows],[f'r{repeat}-b{i}-candidate' for i in range(1,7)])
    def test_failed_startup_stops_without_retry_and_existing_output_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'fresh'
            calls=[]
            def fail(*args):calls.append(args);return {'exit_code':1}
            with self.assertRaises(RuntimeError):run.execute([{'id':str(i)} for i in range(30)],root,fail)
            self.assertEqual(len(calls),1)
            with self.assertRaises(FileExistsError):run.execute([{'id':str(i)} for i in range(30)],root,fail)
    def test_wrong_case_count_or_duplicates_rejected_before_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'fresh'
            for cases in [[{'id':'x'}], [{'id':'x'}]*30]:
                with self.assertRaises(ValueError):run.execute(cases,root,lambda *a:None)
                self.assertFalse(root.exists())

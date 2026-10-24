import copy
import unittest
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from check_trial import check_trial

CASES = [{'id':'C01','request':'How do I use a custom Formly type?'}]
OUTPUT = {'formly_questions':[{'question':'How do I use a custom Formly type?', 'reason':'The user asks about custom type use.'}], 'library_constraints':{'formly_version':None,'ui_adapter':None}}

class TrialTests(unittest.TestCase):
    def test_valid_structure_is_not_semantic_success(self):
        result = check_trial(CASES, [{'id':'C01','output':OUTPUT}])
        self.assertEqual(result['valid_structures'],1)
        self.assertEqual(result['semantic_assessment'],'not performed by this checker')
        self.assertNotIn('passed',result)

    def test_missing_extra_and_duplicate_cases_fail(self):
        for rows in ([], [{'id':'unknown','output':OUTPUT}], [{'id':'C01','output':OUTPUT}]*2):
            with self.assertRaises(ValueError):check_trial(CASES,rows)

    def test_malformed_output_counts_as_failure_without_exclusion(self):
        result=check_trial(CASES,[{'id':'C01','output':dict(OUTPUT,application_investigation=[])}])
        self.assertEqual(result['total_cases'],1)
        self.assertEqual(result['invalid_structures'],1)
        self.assertEqual(result['valid_structures'],0)

    def test_no_repair_or_mutation(self):
        rows=[{'id':'C01','output':copy.deepcopy(OUTPUT)}]
        before=copy.deepcopy(rows)
        check_trial(CASES,rows)
        self.assertEqual(rows,before)

    def test_cli_rejects_duplicate_output_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases = Path(tmp)/'cases.json'
            trial = Path(tmp)/'trial.json'
            cases.write_text(json.dumps(CASES))
            trial.write_text('[{"id":"C01","output":' + json.dumps(OUTPUT) + ',"output":' + json.dumps(OUTPUT) + '}]')
            result = subprocess.run([sys.executable, '-B', str(Path(__file__).with_name('check_trial.py')), '--cases', str(cases), '--trial', str(trial)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Duplicate key', result.stderr)

if __name__=='__main__':unittest.main()

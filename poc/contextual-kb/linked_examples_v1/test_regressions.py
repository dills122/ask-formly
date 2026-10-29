"""Asset-free checks of honest retrieval metrics and non-oracle recovery."""
import importlib.util
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('examples_replay', HERE / 'regressions/run.py')
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)


class RetrievalRegressionTests(unittest.TestCase):
    def test_recovery_only_selects_returned_candidates(self):
        rows = [dict(id='noise', claim='A numeric bound'), dict(id='hide', claim='hide retains model value')]
        self.assertEqual(replay.select_recovery(rows, set(), 'hide model value', 1), ['hide'])
        self.assertEqual(replay.select_recovery(rows, {'hide'}, 'hide model value', 1), ['noise'])

    def test_recovery_deduplicates_and_is_deterministic(self):
        a, b = dict(id='a', claim='value'), dict(id='b', claim='value')
        self.assertEqual(replay.select_recovery([b, a, a], set(), 'value'), ['a', 'b'])

    def test_metrics_do_not_call_unknown_facts_noise(self):
        row = dict(case_id='x', calls=[dict(tool='lookup_formly', arguments={},
                   packet=dict(status='ok', facts=[dict(id='wanted'), dict(id='other')]),
                   sdk_bytes=120, is_error=False)])
        result = replay.grade(row, dict(expected_fact_ids=['wanted', 'missing'], expected_status='ok'))
        self.assertEqual(result['first_pass_expected'], 1)
        self.assertEqual(result['missing_expected'], ['missing'])
        self.assertEqual(result['first_pass_outside_rubric'], 1)
        self.assertEqual(result['answer_quality'], 'not_assessed')

    def test_grader_detects_oracle_fact_fetch(self):
        row = dict(case_id='x', calls=[
            dict(tool='lookup_formly', arguments={}, packet=dict(status='ok', facts=[]), sdk_bytes=10, is_error=False),
            dict(tool='get_formly_facts', arguments=dict(fact_ids=['secret']), packet=dict(facts=[dict(id='secret')]), sdk_bytes=10, is_error=False)])
        result = replay.grade(row, dict(expected_fact_ids=['secret'], expected_status='ok'))
        self.assertEqual(result['recovery_ids_not_discovered'], ['secret'])

    def test_public_cases_and_rubric_separate(self):
        cases = json.loads((HERE / 'regressions/cases.json').read_text())
        rubric = json.loads((HERE / 'regressions/rubric.json').read_text())
        self.assertEqual({r['case_id'] for r in cases}, set(rubric))
        self.assertEqual(len(cases), 8)
        self.assertNotIn('expected_fact_ids', json.dumps(cases))
        for case in cases:
            self.assertNotIn('fact_ids', case)
            self.assertIn('plan', case)


if __name__ == '__main__':
    unittest.main()

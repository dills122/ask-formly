import copy
import importlib.util
import inspect
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('conditional_v3', HERE / 'run.py')
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)


class ConditionalPolicyTests(unittest.TestCase):
    def test_frozen_inputs_and_prior_rubrics_unchanged(self):
        self.assertEqual(run.v1.verify_freeze(HERE)['revision'], 2)
        self.assertEqual(run.v1.verify_freeze(HERE / 'history/revision1')['revision'], 1)
        self.assertEqual(run.v1.verify_freeze(run.V1)['revision'], 2)
        self.assertEqual(run.v1.verify_freeze(run.V2)['revision'], 1)
        rubric = json.loads((HERE / 'rubric.json').read_text())
        self.assertEqual(sum(len(row['essential']) for row in rubric.values()), 15)
        self.assertIn('hide-control-warning', [row['id'] for row in rubric['G2']['essential']])

    def test_claim_alignment_beats_contextual_word_overlap(self):
        rows = [dict(id='incidental', claim='Render a widget.', context='key path literal array model group'),
                dict(id='direct', claim='Array keys preserve literal path segments.'),
                dict(id='seen', claim='Array keys preserve literal path segments.')]
        self.assertEqual(run.select_claim_first(rows, [rows[2]], 'key paths literal arrays', 1), ['direct'])

    def test_claim_first_stable_bounded_and_deduplicated(self):
        rows = [dict(id='z', claim='key'), dict(id='a', claim='key'), dict(id='z', claim='key')]
        self.assertEqual(run.select_claim_first(rows, [], 'keys', 2), ['z', 'a'])
        self.assertEqual(run.select_claim_first(rows, [], 'unmatched', 4), [])

    def test_executor_has_no_grader_or_expected_ids(self):
        body = inspect.getsource(run.execute)
        self.assertNotIn('rubric', body)
        self.assertNotIn('expected', body)
        self.assertIn('same_page_selections', body)

    def test_drift_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            for name in ('freeze.json', 'policy.json', 'cases.json', 'rubric.json'):
                (path / name).write_bytes((HERE / name).read_bytes())
            (path / 'policy.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'Frozen input changed'):
                run.v1.verify_freeze(path)

    def test_gate_detects_missing_warning_oracle_budget_and_regression(self):
        row = dict(case_id='G2', repetition=1, status='ok', expected_status='ok', tool_errors=0,
                   undiscovered_fetch_ids=[], followup_calls=4, max_sdk_bytes=100, max_packet_bytes=90,
                   first_pass_facets=['scope', 'hide-control-warning'], recovered_facets=['scope','hide-control-warning'],
                   missing_facets=[], essential_count=2, recovered_ids=['a','b'])
        metrics = {mode: [copy.deepcopy(row)] for mode in
                   ('baseline-novelty', 'baseline-claim-first', 'candidate-novelty', 'candidate-claim-first')}
        policy = json.loads((HERE / 'policy.json').read_text())
        self.assertEqual(run.failures(metrics, policy), [])
        metrics['candidate-claim-first'][0].update(first_pass_facets=['scope'], undiscovered_fetch_ids=['oracle'],
                                                 max_sdk_bytes=30001, followup_calls=5)
        failures = run.failures(metrics, policy)
        for fragment in ('initial control warning', 'undiscovered fetch', 'byte budget', 'call budget', 'facet regression'):
            self.assertTrue(any(fragment in item for item in failures))


if __name__ == '__main__':
    unittest.main()

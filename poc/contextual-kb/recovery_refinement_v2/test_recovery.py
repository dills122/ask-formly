import copy
import importlib.util
import inspect
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('recovery_v2', HERE / 'run.py')
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)


class RecoveryPolicyTests(unittest.TestCase):
    def test_frozen_inputs_and_existing_equivalents(self):
        self.assertEqual(run.v1.verify_freeze(HERE)['revision'], 1)
        self.assertEqual(run.v1.verify_freeze(run.V1)['revision'], 2)
        rubric = json.loads((HERE / 'rubric.json').read_text())
        old = json.loads((run.V1 / 'rubric.json').read_text())
        self.assertEqual(rubric['historical-G3']['essential'], old['I2-overview']['essential'])
        self.assertEqual(rubric['historical-G4']['essential'],
                         old['K1-natural']['essential'] + old['K3-sharing']['essential'])
        self.assertEqual(sum(len(row['essential']) for row in rubric.values()), 8)

    def test_drift_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            for name in ('freeze.json', 'policy.json', 'cases.json', 'rubric.json'):
                (path / name).write_bytes((HERE / name).read_bytes())
            (path / 'policy.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'Frozen input changed'):
                run.v1.verify_freeze(path)

    def test_selection_rewards_unrepresented_focus_and_never_invents_ids(self):
        candidates = [dict(id='repeat', claim='model initial values'),
                      dict(id='new', claim='defaultValue fallback'),
                      dict(id='offtopic', claim='material appearance'),
                      dict(id='seen', claim='defaultValue fallback')]
        delivered = [dict(id='seen', claim='model initial values')]
        self.assertEqual(run.select_candidates(candidates, delivered, 'model initial defaultValue', 2),
                         ['new', 'repeat'])
        self.assertEqual(run.select_candidates(candidates, delivered, 'unrelatedunknown', 4), [])

    def test_selection_is_stable_deduplicated_and_bounded(self):
        candidates = [dict(id='z', claim='key'), dict(id='a', claim='key'), dict(id='z', claim='key')]
        self.assertEqual(run.select_candidates(candidates, [], 'key', 4), ['z', 'a'])
        self.assertEqual(run.select_candidates(candidates, [], 'key', 1), ['z'])

    def test_executor_has_no_grader_or_expected_ids(self):
        self.assertEqual(list(inspect.signature(run.execute_guided).parameters),
                         ['session', 'parameters', 'case', 'policy'])
        body = inspect.getsource(run.execute_guided)
        self.assertNotIn('rubric', body)
        self.assertNotIn('expected', body)

    def test_failures_disclose_scope_oracle_budget_and_missing_support(self):
        row = dict(case_id='x', repetition=1, status='ok', expected_status='ok', tool_errors=0,
                   undiscovered_fetch_ids=[], followup_calls=4, max_sdk_bytes=100, max_packet_bytes=90,
                   first_pass_ids=['a'], recovered_facets=['facet'], missing_facets=[], historical_id_count=1)
        metrics = {mode: [copy.deepcopy(row)] for mode in
                   ('baseline-original', 'baseline-guided', 'candidate-original', 'candidate-guided')}
        metrics['candidate-guided'][0]['historical_id_count'] = 2
        policy = json.loads((HERE / 'policy.json').read_text())
        self.assertEqual(run.failures(metrics, policy), [])
        metrics['candidate-guided'][0].update(undiscovered_fetch_ids=['oracle'], max_sdk_bytes=30001,
                                            missing_facets=['missing'], followup_calls=5)
        failure = run.failures(metrics, policy)
        for fragment in ('undiscovered fetch', 'byte budget', 'missing essentials', 'call budget'):
            self.assertTrue(any(fragment in item for item in failure))


if __name__ == '__main__':
    unittest.main()

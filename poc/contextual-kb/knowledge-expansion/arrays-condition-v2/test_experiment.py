import tempfile
import unittest
from pathlib import Path
from experiment import HERE, caller_command, run_agent, CodexPlanner

class ExperimentTests(unittest.TestCase):
    def test_selects_new_planner_with_same_real_mcp_caller(self):
        self.assertEqual(CodexPlanner.__module__, 'condition_candidate_v2.planner')
        command = caller_command(HERE/'test-output'/'synthetic-job', 'candidate', 1701)
        config = '\n'.join(command)
        self.assertIn(str(HERE/'experiment.py'), config)
        self.assertIn('lookup_formly', config)
        self.assertIn('"candidate"', config)

    def test_baseline_caller_is_rejected(self):
        with self.assertRaises(ValueError):
            caller_command(HERE/'test-output'/'unused', 'baseline', 1701)

    def test_outside_output_rejected_before_launch(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)/'must-not-exist'
            with self.assertRaises(ValueError):
                run_agent([], 'candidate', 1701, output)
            self.assertFalse(output.exists())

if __name__ == '__main__': unittest.main()

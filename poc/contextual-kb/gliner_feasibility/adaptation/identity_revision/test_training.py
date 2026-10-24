"""Acceptance of bounded local adapter training mechanics, never accuracy."""
import unittest
from training_smoke import run_smoke


class TrainingAcceptance(unittest.TestCase):
    def test_joint_training_gradient_inventory_and_saved_adapter_parity(self):
        result=run_smoke()
        self.assertEqual(result['optimizer_steps'],24)
        self.assertEqual(set(result['cases']),{f'P{i:02d}' for i in range(1,25)})
        self.assertTrue(all(v>0 for v in result['task_gradient_norms'].values()))
        self.assertEqual(set(result['task_gradient_norms']),{'entities','records','relations','classification'})
        self.assertGreater(result['changed_adapter_tensors'],0)
        self.assertEqual(result['changed_frozen_tensors'],0)
        self.assertEqual(result['reload_checks'],24)
        self.assertTrue(result['reload_parity'])


if __name__=='__main__':unittest.main()

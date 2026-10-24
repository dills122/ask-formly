"""Supplemental checkpoint transport only; no optimizer updates."""
import unittest
from reload_check import verify_reload


class ReloadTests(unittest.TestCase):
    def test_all_24_losses_outputs_and_all_parameters_survive_resave(self):
        result=verify_reload()
        self.assertEqual(result['cases'],24)
        self.assertEqual(result['optimizer_steps'],0)
        self.assertTrue(result['losses_equal'])
        self.assertTrue(result['parameters_equal'])
        self.assertTrue(result['outputs_equal'])


if __name__=='__main__':unittest.main()

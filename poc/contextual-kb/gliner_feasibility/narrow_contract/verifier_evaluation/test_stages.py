import unittest
from stages import evaluation_ready, review_receipt

class Tests(unittest.TestCase):
    def test_invalid_decision_never_opens_evaluation(self):
        for decision in ({'mode':'smoke','selected':[.5,.5]}, {'mode':'calibration','selected':None}, {'mode':'calibration','selected':[.6,.5]}):
            with self.assertRaises(ValueError):evaluation_ready(decision,{'x':'hash'},lambda:self.fail('evaluation opened'))
    def test_binding_drift_blocks_evaluation(self):
        with self.assertRaises(ValueError):evaluation_ready(dict(mode='calibration',selected=[.5,.5],bindings={'x':'old'}),{'x':'new'},lambda:self.fail('opened'))
    def test_unreviewed_or_wrong_hash_seal_rejected(self):
        for receipt in ({},dict(verdict='ready',fresh_sha256='wrong',independent=True,reviewer='reviewer'),dict(verdict='ready',fresh_sha256='hash',independent=False,reviewer='reviewer')):
            with self.assertRaises(ValueError):review_receipt(receipt,'hash')
        self.assertTrue(review_receipt(dict(verdict='ready',fresh_sha256='hash',independent=True,reviewer='reviewer'),'hash'))
    def test_valid_binding_allows_loader(self):
        self.assertEqual(evaluation_ready(dict(mode='calibration',selected=[.5,.5],bindings={'x':'same'}),{'x':'same'},lambda:42),42)

if __name__=='__main__':unittest.main()

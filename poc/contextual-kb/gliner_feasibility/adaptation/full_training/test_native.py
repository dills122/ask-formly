"""Native API guard tests, without loading a checkpoint."""
import unittest
from native import fingerprint,predict,loss_terms,prepare
import torch
from types import SimpleNamespace

class NativeTests(unittest.TestCase):
    def test_more_than_32_records_rejected_before_native_preprocessing(self):
        with self.assertRaisesRegex(ValueError,'32 record'):prepare(None,{'aspects':[{}]*33})
    def test_inference_rejects_gold_frames(self):
        with self.assertRaises(ValueError):predict(None,[{'question':'q','aspects':[]}])
    def test_fingerprint_is_json_safe_and_preserves_dtype_and_shape(self):
        import json
        from dataclasses import dataclass
        @dataclass
        class Batch:
            tokens:object
            marker:object
        fp=fingerprint(Batch(torch.tensor([[1,2]]),int))
        self.assertEqual(json.loads(json.dumps(fp)),fp)
        self.assertEqual(fp['tokens']['shape'],[1,2])
    def test_native_missing_loss_is_fatal(self):
        with self.assertRaises(ValueError):loss_terms(SimpleNamespace(total_loss=torch.tensor(1.),losses={}))

if __name__=='__main__':unittest.main()

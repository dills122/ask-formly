import unittest
from unittest.mock import patch
import runtime

class Tests(unittest.TestCase):
    def test_nonfinite_native_logits_are_rejected_before_sigmoid(self):
        model=runtime.Models.__new__(runtime.Models);model.verifier=object()
        for value in (float('inf'),float('-inf'),float('nan')):
            with self.subTest(value=value):
                z=runtime.torch.tensor([[value,100.,-100.,-100.,-100.,-100.,-100.]])
                with patch.object(runtime,'score',return_value=(z,[(0,1)],[],None)):
                    with self.assertRaisesRegex(ValueError,'nonfinite verifier logits'):
                        model.score('x',[(0,1)])
    def test_finite_logits_and_unsupported_offsets_preserved(self):
        model=runtime.Models.__new__(runtime.Models);model.verifier=object()
        with patch.object(runtime,'score',return_value=(runtime.torch.zeros((1,7)),[(0,1)],[(1,2)],None)):
            self.assertEqual(model.score('xy',[(0,1),(1,2)]),{(0,1):[.5]*7,(1,2):None})

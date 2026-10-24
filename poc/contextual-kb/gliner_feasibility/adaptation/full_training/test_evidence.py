"""Read the retained pilot preflight; does not train or rerun the model."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parent/'test-output/preflight-01'
class PreflightEvidenceTests(unittest.TestCase):
    def test_real_first_save_exact_parity_on_all_24_original_cases(self):
        checkpoint=ROOT/'checkpoint-1'
        receipt=json.loads((checkpoint/'receipt.json').read_text())
        self.assertEqual(receipt['status'],'verified')
        self.assertEqual(receipt['cases'],24)
        self.assertEqual(receipt['differences'],[])
        before=json.loads((checkpoint/'before.json').read_text())
        after=json.loads((checkpoint/'after.json').read_text())
        self.assertEqual(before,after)
        self.assertEqual(len(before['parameters']),478)
        for which in ('before','after'):
            self.assertEqual(receipt[which+'_sha256'],hashlib.sha256((checkpoint/(which+'.json')).read_bytes()).hexdigest())
        for path,digest in receipt['artifact_hashes'].items():
            self.assertEqual(digest,hashlib.sha256((checkpoint/path).read_bytes()).hexdigest())
        result=json.loads((ROOT/'run.json').read_text())
        self.assertEqual(result['steps'],2)
        self.assertEqual(result['changed_frozen_tensors'],0)
        self.assertEqual(result['changed_adapter_tensors'],144)
        self.assertEqual(json.loads((ROOT/'controller.json').read_text())['status'],'completed')

if __name__=='__main__':unittest.main()

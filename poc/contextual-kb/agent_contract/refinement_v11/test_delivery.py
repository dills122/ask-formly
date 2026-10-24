import copy
import json
import unittest
from pathlib import Path
from delivery import serialize_batch

class DeliveryTests(unittest.TestCase):
    def test_roundtrip_quotes_backslashes_newlines_unicode(self):
        rows=[{'id':'x','output':{'text':'quote " / slash \\ / literal \\n / newline\n / café 🦉'}}]
        before=copy.deepcopy(rows)
        self.assertEqual(json.loads(serialize_batch(rows)),rows)
        self.assertEqual(rows,before)

    def test_does_not_repair_or_filter_semantically_invalid_objects(self):
        rows=[{'id':'x','output':{'wrong_schema':True,'scope':'unknown'}}]
        self.assertEqual(json.loads(serialize_batch(rows)),rows)

    def test_non_json_numbers_rejected(self):
        for value in [float('nan'),float('inf'),float('-inf')]:
            with self.assertRaises(ValueError):serialize_batch([value])

    def test_non_json_objects_rejected(self):
        with self.assertRaises(TypeError):serialize_batch([object()])

    def test_batch_must_be_list(self):
        with self.assertRaises(ValueError):serialize_batch({'id':'x'})

    def test_old_malformed_text_still_fails_json_parsing(self):
        text=(Path(__file__).resolve().parent.parent/'refinement_v10/test-output/b4-r2-raw.json').read_text()
        with self.assertRaises(json.JSONDecodeError):json.loads(text)

if __name__=='__main__':unittest.main()

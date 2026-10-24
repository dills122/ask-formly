import os
import unittest
from revision import HERE,load_pilot
os.environ.update(HF_HOME=str(HERE/'.cache/hf'),HF_HUB_OFFLINE='1',
                  TRANSFORMERS_OFFLINE='1',TOKENIZERS_PARALLELISM='false')
from compatibility import load_model, prepare, verify_transport, oracle_records


class CompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model=load_model();cls.rows=load_pilot()

    def test_all_24_native_targets_and_negative_relations(self):
        for row in self.rows:
            with self.subTest(case=row['id']):
                batch=prepare(self.model,row)
                result=verify_transport(row,batch)
                self.assertEqual(result['records'],len(row['aspects']))
                self.assertEqual(result['relation_tasks'],2)

    def test_all_24_anchorless_oracle_records_preserve_identity_and_fields(self):
        for row in self.rows:
            with self.subTest(case=row['id']):
                batch=prepare(self.model,row)
                result=oracle_records(batch)
                self.assertEqual(result['decoded'],result['expected'])
                self.assertEqual(result['dense_decoded'],result['expected'])
                self.assertEqual(result['dense_instance_count'],32)

    def test_same_target_natural_control_still_fails(self):
        batch=prepare(self.model,self.rows[3])
        result=oracle_records(batch,natural_control=True)
        self.assertEqual(len(result['expected']),2)
        self.assertNotEqual(result['decoded'],result['expected'])


if __name__=='__main__':unittest.main()

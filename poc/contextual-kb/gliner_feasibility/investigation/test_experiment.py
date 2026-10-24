import unittest
from experiment import validate_native, observe_native


class ExtractionEvidenceTests(unittest.TestCase):
    def test_record_fields_and_relations_are_checked(self):
        text = 'x is off'
        span = {'text': 'off', 'start': 5, 'end': 8, 'confidence': .9}
        result = {'request': [{'action': span, 'condition': [span]}],
                  'relation_extraction': {'requires': [{'head': span, 'tail': span}]},
                  'interpretation': {'label': 'clear', 'confidence': .7}}
        self.assertEqual(validate_native(text,result),4)

    def test_incorrect_record_span_is_not_ignored(self):
        with self.assertRaises(ValueError):
            validate_native('off', {'request': [{'action': {'text':'on','start':0,'end':3}}]})

    def test_native_output_preserved_on_validation_error(self):
        native = {'request': [{'action': {'text':'on','start':0,'end':3}}]}
        row = observe_native('off', lambda: native)
        self.assertEqual(row['native'], native)
        self.assertEqual(row['error']['type'],'ValueError')

    def test_no_retry_on_backend_error(self):
        calls=[]
        def extract():
            calls.append(1)
            raise RuntimeError('failed')
        row=observe_native('off',extract)
        self.assertEqual(calls,[1])
        self.assertEqual(row['error']['message'],'failed')


if __name__ == '__main__':
    unittest.main()

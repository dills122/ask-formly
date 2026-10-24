import json,tempfile,unittest
from pathlib import Path
from cli import read_input,write_output
from test_lookup import CORE,Q

class CliTests(unittest.TestCase):
    def test_valid_foundation_envelope(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent/'test-output') as d:
            p=Path(d)/'in.json';p.write_text(json.dumps(dict(request=Q,question_plan=CORE)))
            self.assertEqual(read_input(p),(Q,CORE))
    def test_invalid_envelope_or_core_rejected(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent/'test-output') as d:
            p=Path(d)/'in.json'
            for value in [{},dict(request=Q,question_plan={}),dict(request=Q,question_plan=CORE,role_hints=[])]:
                p.write_text(json.dumps(value))
                with self.assertRaises(ValueError):read_input(p)
            p.write_text('{"request":"one","request":"two","question_plan":{}}')
            with self.assertRaises(ValueError):read_input(p)
    def test_output_never_overwrites(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent/'test-output') as d:
            p=Path(d)/'out.json';write_output(p,{'first':1})
            with self.assertRaises(FileExistsError):write_output(p,{'second':2})
            self.assertEqual(json.loads(p.read_text()),{'first':1})

if __name__=='__main__':unittest.main()

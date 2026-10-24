import json,tempfile,unittest
from pathlib import Path
from pipeline import save,freeze,verify

class SafetyTests(unittest.TestCase):
    def test_first_save_cannot_overwrite(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent/'test-output') as d:
            p=Path(d)/'output.json';save(p,{'first':1})
            with self.assertRaises(FileExistsError):save(p,{'second':2})
            self.assertEqual(json.loads(p.read_text()),{'first':1})
    def test_mutation_detected(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent/'test-output') as d:
            p=Path(d)/'input.json';m=Path(d)/'freeze.json';save(p,{'first':1});freeze(m,[p]);verify(m)
            p.write_text('{}')
            with self.assertRaises(ValueError):verify(m)

if __name__=='__main__':unittest.main()

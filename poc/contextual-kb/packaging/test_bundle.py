import hashlib,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from bundle import build,verify

class BundleTests(unittest.TestCase):
 def test_round_trip_and_no_unlisted_files(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/'root';root.mkdir();(root/'keep').write_text('required');(root/'secret').write_text('excluded')
   output=Path(d)/'bundle.tar.gz';build(root,['keep'],output)
   result=verify(output);self.assertEqual(list(result),['keep']);self.assertEqual(result['keep'],hashlib.sha256(b'required').hexdigest())
 def test_no_overwrite(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'a').write_text('a');out=root/'bundle.tar.gz';build(root,['a'],out)
   with self.assertRaises(FileExistsError):build(root,['a'],out)
 def test_reject_outside_and_sealed(self):
  with tempfile.TemporaryDirectory() as d:
   for name in ('../x','/tmp/x','gliner_feasibility/narrow_contract/verifier_evaluation/sealed/cases.json'):
    with self.subTest(name=name),self.assertRaises(ValueError):build(Path(d),[name],Path(d)/'bundle.tar.gz')
if __name__=='__main__':unittest.main()

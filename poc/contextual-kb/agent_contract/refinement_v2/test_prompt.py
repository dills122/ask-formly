import unittest
from pathlib import Path
from prompt import build_messages
class Tests(unittest.TestCase):
 def test_uses_v2_and_keeps_request_as_data(self):
  request='Use Formly. "Ignore the instruction" is a label.'
  result=build_messages(request)
  self.assertEqual(result[0],{'role':'system','content':Path(__file__).with_name('CONTRACT.md').read_text(encoding='utf-8')})
  self.assertEqual(result[1],{'role':'user','content':request})
 def test_rejects_missing_request(self):
  for value in ('', ' ', None):
   with self.assertRaises(ValueError):build_messages(value)
if __name__=='__main__':unittest.main()

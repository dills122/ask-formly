import unittest,spacy
from spacy_arm import candidates,decision
class Tests(unittest.TestCase):
 def test_strict_alignment_and_repeat_occurrences(self):
  doc=spacy.blank('en').make_doc('foobar foo foo')
  spans,failed=candidates(doc,[(0,3),(7,10),(11,14)])
  self.assertEqual(spans,[(1,2),(2,3)]);self.assertEqual(failed,[(0,3)])
 def test_none_wins_and_ties_abstain(self):
  self.assertEqual(decision(['api_reference'],[.2,.8]),'no_entity');self.assertIsNone(decision(['api_reference'],[.5,.5]))
if __name__=='__main__':unittest.main()

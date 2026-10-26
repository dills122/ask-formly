import unittest
from results import validate_answers, require_identical

class ResultTests(unittest.TestCase):
 def setUp(self):
  self.packets={'D01':{'facts':[{'id':'observed'}]}}
  self.answers=[{'id':'D01','citations':['observed'],'answer':'Supported statement','usable':True,'reason':'Reviewed'}]
 def test_valid_and_false_manual_judgments_are_counted(self):
  self.assertEqual(validate_answers(self.answers,self.packets),1)
  self.answers[0]['usable']=False
  self.assertEqual(validate_answers(self.answers,self.packets),0)
 def test_unseen_citation_is_rejected(self):
  self.answers[0]['citations']=['oracle']
  with self.assertRaises(ValueError):validate_answers(self.answers,self.packets)
 def test_missing_and_duplicate_answers_are_rejected(self):
  for answers in [[],self.answers*2]:
   with self.assertRaises(ValueError):validate_answers(answers,self.packets)
 def test_repeat_difference_cannot_reuse_judgment(self):
  require_identical(self.packets,self.packets)
  with self.assertRaises(ValueError):require_identical(self.packets,{'D01':{'facts':[]}})

import unittest
from candidate import add_candidate_evidence
class CatalogTests(unittest.TestCase):
 def test_additions_have_exact_release_without_changing_old_records(self):
  old={'records':[{'id':'old'}],'evidence_releases':{'old':'6.3.12'}}
  out=add_candidate_evidence(old,[{'id':'new'}])
  self.assertEqual(out['records'],[{'id':'old'},{'id':'new'}])
  self.assertEqual(out['evidence_releases']['new'],'6.3.12')
  self.assertEqual(old,{'records':[{'id':'old'}],'evidence_releases':{'old':'6.3.12'}})
 def test_collision_and_orphan_release_refused(self):
  for old in [{'records':[{'id':'new'}],'evidence_releases':{}},{'records':[],'evidence_releases':{'new':'7.0.0'}}]:
   with self.assertRaises(ValueError):add_candidate_evidence(old,[{'id':'new'}])
  with self.assertRaises(ValueError):add_candidate_evidence({'records':[],'evidence_releases':{}},[{'id':'new'},{'id':'new'}])

import unittest
from policy import combine
class TestPolicy(unittest.TestCase):
 def test_no_supplement_exact_baseline(self):
  r=combine([list('abcdefgh')],[None]);self.assertEqual(r['protected'],list('abcdefgh'));self.assertEqual(r['current'],r['foundation'])
 def test_six_reserved_even_when_fusion_changes_rank(self):
  r=combine([list('abcdefgh')],[list('zxywvuts')]);self.assertEqual(r['protected'][:6],list('abcdef'));self.assertEqual(len(r['protected']),8)
  self.assertNotEqual(r['protected'],r['current'])
 def test_fill_follows_current_fusion_not_fact_name(self):
  r=combine([list('abcdefgh')],[list('hgzabcde')]);expected=list('abcdef')
  for f in r['current']+r['foundation']:
   if f not in expected and len(expected)<8:expected.append(f)
  self.assertEqual(r['protected'],expected)
 def test_short_baseline_protects_all(self):
  r=combine([['a','b']],[['z','x','a']]);self.assertEqual(r['protected'][:2],['a','b']);self.assertEqual(set(r['protected']),{'a','b','z','x'})
 def test_empty_inputs(self):self.assertEqual(combine([],[])['protected'],[])
 def test_empty_original_can_add_candidates(self):self.assertEqual(combine([[]],[['z','a']])['protected'],['z','a'])
 def test_multiple_questions_keep_original_interleave(self):
  r=combine([list('abcdefgh'),list('ijklmnop')],[list('qrstuvwx'),list('yzabcdef')]);self.assertEqual(r['protected'][:6],list('aibjck'))
 def test_unique_bounded_and_only_sourced(self):
  full=[['a','a','b','c','d','e','f','g','h']];extra=[list('zxywvuts')];r=combine(full,extra)
  for ids in r.values():self.assertLessEqual(len(ids),8);self.assertEqual(len(ids),len(set(ids)));self.assertTrue(set(ids)<=set(full[0]+extra[0]))
 def test_mismatched_question_counts_rejected(self):
  with self.assertRaises(ValueError):combine([['a']],[])
 def test_tail_is_not_falsely_guaranteed(self):
  r=combine([list('abcdefgh')],[list('zxywvuts')]);self.assertTrue(set('abcdef')<=set(r['protected']));self.assertNotEqual(set(r['protected']),set('abcdefgh'))
if __name__=='__main__':unittest.main()

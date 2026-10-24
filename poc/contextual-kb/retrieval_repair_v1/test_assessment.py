import unittest
from assessment import compare_groups
class AssessmentTests(unittest.TestCase):
    def test_equal_counts_cannot_hide_lost_group(self):
        r=compare_groups(['a'],['b'],[['a'],['b']])
        self.assertEqual(r['lost_group_indexes'],[0]);self.assertEqual(r['gained_group_indexes'],[1]);self.assertFalse(r['nonregression'])
    def test_alternate_fact_in_same_group_is_not_group_loss(self):
        r=compare_groups(['a'],['b'],[['a','b']])
        self.assertEqual(r['lost_group_indexes'],[]);self.assertTrue(r['nonregression'])
if __name__=='__main__':unittest.main()

import unittest
from native_logits import validate_offsets,inverse_mapping
class OffsetTests(unittest.TestCase):
 def test_native_list_and_dict_mappings_have_equal_offset_identity(self):
  self.assertEqual(inverse_mapping([0,5]),{0:0,5:1})
  self.assertEqual(inverse_mapping({0:4,1:9},1),{4:1,9:2})
 def test_repeated_text_keeps_distinct_occurrence_identity(self):
  self.assertEqual(validate_offsets('same same',[(0,4),(5,9)]),[(0,4),(5,9)])
 def test_duplicate_cannot_double_weight_anchor(self):
  with self.assertRaises(ValueError):validate_offsets('same',[(0,4),(0,4)])
 def test_out_of_bounds_is_invalid_not_transport_abstention(self):
  with self.assertRaises(ValueError):validate_offsets('same',[(0,5)])
if __name__=='__main__':unittest.main()

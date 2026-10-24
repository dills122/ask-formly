import unittest
from transport import export, malformed, ROLES
class TransportTests(unittest.TestCase):
 def test_occurrences_and_negative_queries(self):
  r={'question':'type type', 'mentions':[{'kind':'api_reference','raw':'type','start':0,'end':4},{'kind':'registration_name','raw':'type','start':5,'end':9}]}
  e=export(r,[] )['output']['entities']
  self.assertEqual(e['target_role: api_reference'],[{'text':'type','start':0,'end':4}])
  self.assertEqual(e['target_role: registration_name'],[{'text':'type','start':5,'end':9}])
  self.assertEqual(e['target_role: no_entity'],[])
  self.assertEqual(set(e),set(ROLES[:-1])|{'target_role: '+x for x in ROLES})
 def test_bad_span_does_not_delete_gold(self):
  r={'question':"Set props.disabled to false",'mentions':[{'kind':'api_reference','raw':'props.disabled','start':4,'end':18},{'kind':'value','raw':'false','start':22,'end':27}]}
  bad=malformed(r)
  self.assertTrue(any(x['family']=='merged_mentions' for x in bad))
  e=export(r,bad)['output']['entities'];self.assertEqual(len(e['api_reference']),1)
  self.assertEqual(len(e['target_role: no_entity']),len(bad))
 def test_invalid_offsets_rejected(self):
  with self.assertRaises(ValueError):export({'question':'type','mentions':[{'kind':'api_reference','raw':'type','start':1,'end':4}]},[])

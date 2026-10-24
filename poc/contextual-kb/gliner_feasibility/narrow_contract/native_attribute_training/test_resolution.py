import unittest
from resolution import resolve_scores
class Tests(unittest.TestCase):
 def test_rejection_retains_raw(self):
  r={'output':{'entities':{'api_reference':[{'start':0,'end':4,'text':'type'}],'value':[{'start':0,'end':4,'text':'type'}]}}}
  out,log=resolve_scores('type',r,[{'start':0,'end':4,'status':'scored','label':'no_entity','confidence':.99}]);self.assertEqual(out,r);self.assertEqual(log[0]['attribute_decision'],'learned_no_entity')
 def test_partial_kept_and_nonconflict_kept(self):
  r={'output':{'entities':{'api_reference':[{'start':0,'end':4,'text':'type'}],'value':[{'start':0,'end':7,'text':'type xx'}]}}}
  out,log=resolve_scores('type xx',r,[{'start':0,'end':4,'status':'scored','label':'api_reference','confidence':.99}]);self.assertEqual(out,r);self.assertEqual(log[0]['decision'],'partial_overlap')
 def test_only_losing_same_span_removed(self):
  r={'output':{'entities':{'api_reference':[{'start':0,'end':4,'text':'type'}],'value':[{'start':0,'end':4,'text':'type'}]}}}
  out,log=resolve_scores('type',r,[{'start':0,'end':4,'status':'scored','label':'api_reference','confidence':.99}]);self.assertEqual(out['output']['entities']['value'],[]);self.assertEqual(r['output']['entities']['value'][0]['text'],'type')

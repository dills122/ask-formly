import unittest,math
from policy import resolve,select,native_choices

def row():return {'id':'x','output':{'entities':{'api_reference':[{'text':'foo','start':0,'end':3,'confidence':.8}], 'registration_name':[{'text':'foo','start':0,'end':3,'confidence':.7}], 'value':[{'text':'foo','start':4,'end':7,'confidence':.9}]}}}
class Tests(unittest.TestCase):
 def test_resolve_exact_occurrence_preserves_other_occurrence(self):
  x=row();y,a=resolve('foo foo',x,{(0,3):'registration_name',(4,7):'api_reference'})
  self.assertEqual(y['output']['entities']['api_reference'],[]);self.assertEqual(y['output']['entities']['value'],x['output']['entities']['value']);self.assertEqual(len(x['output']['entities']['api_reference']),1)
 def test_partial_overlap_abstains(self):
  x=row();x['output']['entities']['registration_name'][0].update(text='foo foo',end=7)
  self.assertEqual(resolve('foo foo',x,{(0,3):'api_reference'})[0],x)
 def test_unknown_none_missing_abstains(self):
  for choice in ('no_entity','unknown',None):self.assertEqual(resolve('foo foo',row(),{(0,3):choice})[0],row())
 def test_errors_and_malformed_retained(self):
  for x in ({'id':'x','error':'failure'}, {'output':{'entities':{'bad':[]}}}):self.assertEqual(resolve('foo foo',x,{})[0],x)
 def test_scores_fail_closed(self):
  self.assertEqual(select({'api_reference':.6,'no_entity':.4}),'api_reference')
  for scores in ({'api_reference':.5,'value':.5},{'api_reference':float('nan')},{'api_reference':.4},{'bad':.8},{'api_reference':1.1}):self.assertIsNone(select(scores))
 def test_malformed_native_abstains(self):
  for output in ({'entities':{'value':[{}]}},{'entities':None},{'entities':{'value':[dict(text='foo',start=0,end=3,target_role=None)]}}):self.assertEqual(native_choices('foo',output),{})
 def test_native_requires_exact_text_and_agreement(self):
  x=row()['output'];x['entities']['api_reference'][0]['target_role']={'label':'registration_name','confidence':.8};x['entities']['registration_name'][0]['target_role']={'label':'registration_name','confidence':.9}
  self.assertEqual(native_choices('foo foo',x)[(0,3)],'registration_name')
  x['entities']['api_reference'][0]['target_role']['label']='api_reference';self.assertIsNone(native_choices('foo foo',x)[(0,3)])
if __name__=='__main__':unittest.main()

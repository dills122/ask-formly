import unittest
from gate import assess
class GateTests(unittest.TestCase):
 def rows(self,usable):
  cases=[{'id':str(i),'kind':'target','group':'g'} for i in range(160)]+[{'id':'c'+str(i),'kind':'control','group':'g'} for i in range(16)]
  answers=[{'id':r['id'],'usable':i<usable or i>=160,'critical_unsupported_claim':False} for i,r in enumerate(cases)]
  return cases,answers
 def test_target(self):self.assertEqual(assess(*self.rows(144))['decision'],'target_met')
 def test_tolerance(self):self.assertEqual(assess(*self.rows(143))['decision'],'accepted_lower_band')
 def test_below_band(self):self.assertEqual(assess(*self.rows(142))['decision'],'failed')
 def test_control_failure(self):
  c,a=self.rows(160);a[-1]['usable']=False;self.assertEqual(assess(c,a)['decision'],'failed')
 def test_critical_failure(self):
  c,a=self.rows(160);a[0]['critical_unsupported_claim']=True;self.assertEqual(assess(c,a)['decision'],'failed')
 def test_wrong_denominator(self):
  c,a=self.rows(160)
  with self.assertRaises(ValueError):assess(c[:-1],a[:-1])
if __name__=='__main__':unittest.main()

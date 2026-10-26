import unittest
import assessment

class AssessmentTests(unittest.TestCase):
    def rows(self):
        return [dict(repeat=r,arm=a,id=i,usable=True,critical=False) for r in (1,2,3) for a in ('baseline','candidate') for i in assessment.IDS]
    def test_full_matrix_passes(self):self.assertTrue(assessment.gate(self.rows(),0)['passed'])
    def test_missing_or_duplicate_never_pass(self):
        rows=self.rows()
        self.assertFalse(assessment.gate(rows[:-1],0)['passed'])
        self.assertFalse(assessment.gate(rows+[rows[0]],0)['passed'])
    def test_controls_criticals_delivery_and_regressions_fail(self):
        for key,value in [('usable',False),('critical',True)]:
            rows=self.rows();next(x for x in rows if x['arm']=='candidate' and x['id']=='C01')[key]=value
            self.assertFalse(assessment.gate(rows,0)['passed'])
        self.assertFalse(assessment.gate(self.rows(),1)['passed'])
        rows=self.rows();next(x for x in rows if x['arm']=='candidate' and x['id']=='J01')['usable']=False
        self.assertFalse(assessment.gate(rows,0)['passed'])
    def test_one_candidate_miss_allowed_only_if_baseline_also_misses(self):
        rows=self.rows()
        for x in rows:
            if x['id']=='J01':x['usable']=False
        self.assertTrue(assessment.gate(rows,0)['passed'])
if __name__=='__main__':unittest.main()

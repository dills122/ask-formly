import unittest
from assessment import assess,ARMS

class AssessmentTests(unittest.TestCase):
    def fixture(self):
        cases=[];rows=[];traces=[];semantic=[]
        for b in (1,2,3):
            identity=f'R{b}';cases.append(dict(id=identity,batch=b,relevant_fact_ids=['a','b'],required_groups=[['a','b']]))
            semantic.append(dict(id=identity,foundation_pass=True,issues=[]))
            traces.append(dict(id=identity,narrow_pool=['a'],wide_pool=['a','b']))
            for a in ARMS:rows.append(dict(id=identity,batch=b,arm=a,ids=['a'],error=None))
        return rows,cases,traces,semantic
    def test_joint_gain_can_qualify(self):
        rows,cases,traces,semantic=self.fixture()
        for r in rows:
            if r['arm']=='wide_select':r['ids']=['a','b']
        report=assess(rows,cases,traces,semantic)
        self.assertTrue(report['qualified']);self.assertEqual(report['pools']['wide']['all'],1)
    def test_substitute_does_not_hide_fact_loss(self):
        rows,cases,traces,semantic=self.fixture()
        for r in rows:
            if r['arm']=='wide_select':r['ids']=['b']
        report=assess(rows,cases,traces,semantic)
        self.assertFalse(report['gates']['preservation']);self.assertEqual(report['paired']['wide_select'][0]['lost'],['a'])
    def test_semantic_failure_prevents_qualification(self):
        rows,cases,traces,semantic=self.fixture()
        for r in rows:
            if r['arm']=='wide_select':r['ids']=['a','b']
        semantic[0]['foundation_pass']=False
        self.assertFalse(assess(rows,cases,traces,semantic)['qualified'])
    def test_failed_selection_empty_still_counted(self):
        rows,cases,traces,semantic=self.fixture();rows[-1].update(ids=[],error='bad')
        self.assertEqual(assess(rows,cases,traces,semantic)['summaries']['wide_select']['all']['8']['n'],3)
    def test_empty_precision_not_inflated(self):
        rows,cases,traces,semantic=self.fixture()
        for r in rows:r['ids']=[]
        report=assess(rows,cases,traces,semantic)
        self.assertEqual(report['summaries']['wide_select']['all']['8']['precision'],0)
        self.assertIsNone(report['summaries']['wide_select']['all']['8']['selected_precision'])
    def test_missing_duplicate_wrong_batch_rejected(self):
        for mutation in ('missing','duplicate','batch'):
            rows,cases,traces,semantic=self.fixture()
            if mutation=='missing':rows.pop()
            if mutation=='duplicate':rows.append(dict(rows[0]))
            if mutation=='batch':rows[0]['batch']=7
            with self.assertRaises(ValueError):assess(rows,cases,traces,semantic)
    def test_unsupported_exposure_separate(self):
        rows,cases,traces,semantic=self.fixture();cases[0].update(relevant_fact_ids=[],required_groups=[])
        report=assess(rows,cases,traces,semantic)
        self.assertEqual(report['summaries']['foundation']['all']['8']['unsupported_candidates'],1)
        self.assertEqual(report['summaries']['foundation']['all']['8']['n'],2)

if __name__=='__main__':unittest.main()

import copy,json,unittest
from pathlib import Path
from evaluate import evaluate

CASES=json.loads((Path(__file__).parent/'qualification-cases.json').read_text())

def good_summary():
    return {'rounds':[{'round':repeat,'arm':arm,'total':15,'usable':15,'critical':0,
        'rows':[{'id':c['id'],'category':c['category'],'usable':True,'critical':False,'delivery_errors':[]} for c in CASES['cases']]}
        for repeat in (1,2,3) for arm in ('baseline','candidate')]}

def fail_case(summary,repeat,arm,id,**extra):
    r=next(r for r in summary['rounds'] if r['round']==repeat and r['arm']==arm)
    row=next(c for c in r['rows'] if c['id']==id);row.update(usable=False,**extra)
    r['usable']=sum(c['usable'] for c in r['rows']);r['critical']=sum(c['critical'] for c in r['rows'])

class EvaluationTests(unittest.TestCase):
    def test_all_rounds_pass(self):self.assertTrue(evaluate(good_summary(),CASES)['qualified'])
    def test_14_passes_only_when_miss_is_not_control_or_baseline_supported(self):
        s=good_summary();fail_case(s,1,'candidate','V01');fail_case(s,1,'baseline','V01')
        self.assertTrue(evaluate(s,CASES)['qualified'])
    def test_subthreshold_control_critical_and_regression_each_fail(self):
        for kind in ('threshold','control','critical','regression'):
            with self.subTest(kind=kind):
                s=good_summary()
                if kind=='threshold':
                    for id in ('V01','V02'):
                        fail_case(s,1,'candidate',id);fail_case(s,1,'baseline',id)
                elif kind=='control':
                    fail_case(s,1,'candidate','E05');fail_case(s,1,'baseline','E05')
                elif kind=='critical':fail_case(s,1,'candidate','V01',critical=True)
                else:fail_case(s,1,'candidate','V01')
                self.assertFalse(evaluate(s,CASES)['qualified'])
    def test_missing_duplicate_or_extra_round_and_case_never_disappear(self):
        for kind in ('missing_round','duplicate_round','extra_round','missing_case','duplicate_case','extra_case'):
            with self.subTest(kind=kind):
                s=good_summary()
                if kind=='missing_round':s['rounds'].pop()
                elif kind=='duplicate_round':s['rounds'].append(copy.deepcopy(s['rounds'][0]))
                elif kind=='extra_round':s['rounds'][0]['round']=4
                elif kind=='missing_case':s['rounds'][0]['rows'].pop()
                elif kind=='duplicate_case':s['rounds'][0]['rows'][-1]=copy.deepcopy(s['rounds'][0]['rows'][0])
                else:s['rounds'][0]['rows'].append({'id':'unexpected'})
                self.assertFalse(evaluate(s,CASES)['qualified'])
    def test_delivery_error_in_either_arm_or_missing_assessment_fails(self):
        for arm in ('baseline','candidate'):
            s=good_summary();fail_case(s,1,arm,'V01',delivery_errors=['no audit'])
            self.assertFalse(evaluate(s,CASES)['qualified'])
        s=good_summary();fail_case(s,1,'baseline','V01',error='Missing/duplicate assessment')
        self.assertFalse(evaluate(s,CASES)['qualified'])
    def test_inconsistent_or_nonboolean_summary_rejected(self):
        s=good_summary();s['rounds'][0]['usable']=14
        self.assertFalse(evaluate(s,CASES)['qualified'])
        s=good_summary();s['rounds'][0]['rows'][0]['usable']='false'
        self.assertFalse(evaluate(s,CASES)['qualified'])

if __name__=='__main__':unittest.main()

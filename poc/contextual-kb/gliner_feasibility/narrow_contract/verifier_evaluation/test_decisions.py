import copy
import unittest
from decisions import resolve, assess, select_thresholds, qualification, ROLES


def raw(text='x'):
    item=dict(start=0,end=len(text),text=text,confidence=.8)
    return {'entities':{'api_reference':[item.copy()],'value':[item.copy()]}}


def case(p=None):
    return dict(id='q',text='x',gold=[[0,1,'api_reference']],raw=raw(),operational_scores=[dict(start=0,end=1,probabilities=p or [.99,.99,.01,.01,.01,.01,.01])],probes=[dict(start=0,end=1,expected_role='api_reference',family='gold',probabilities=[.99,.99,.01,.01,.01,.01,.01]),dict(start=0,end=1,expected_role=None,family='synthetic',probabilities=[.01]*7)],prior_correct_repairs=[])

class Tests(unittest.TestCase):
    def test_only_single_supported_proposed_role_resolves(self):
        source=raw();out,log=resolve('x',source,lambda offsets:{(0,1):[.99,.99,.01,.01,.01,.01,.01]},(.7,.7))
        self.assertEqual(out['entities']['value'],[]);self.assertEqual(source,raw());self.assertEqual(log[0]['decision'],'resolved')
    def test_no_conflict_never_calls_scorer(self):
        r=raw();r['entities']['value']=[]
        out,log=resolve('x',r,lambda x:self.fail('scorer called'),(.7,.7));self.assertEqual(out,r)
    def test_partial_overlap_never_scored(self):
        r=raw('abc');r['entities']['model_key']=[dict(start=1,end=2,text='b')]
        out,log=resolve('abc',r,lambda x:self.fail('scorer called'),(.5,.5));self.assertEqual(out,r)
    def test_multiple_unproposed_nonfinite_or_boundary_fail_abstains(self):
        for p in ([.9,.9,.9,0,0,0,0],[.9,0,.9,0,0,0,0],[float('nan')]*7,[.1,.99,0,0,0,0,0],None):
            out,log=resolve('x',raw(),lambda x:{(0,1):p},(.5,.5));self.assertEqual(out,raw())
    def test_overflow_skips_entire_question(self):
        text='x '*9;r={'entities':{r:[] for r in ROLES}}
        for i in range(9):
            for role in ('api_reference','value'):r['entities'][role].append(dict(start=2*i,end=2*i+1,text='x'))
        out,log=resolve(text,r,lambda x:self.fail('scorer called'),(.5,.5));self.assertEqual(out,r);self.assertEqual(log[0]['decision'],'overflow')
    def test_wrong_resolution_lost_gold_counted(self):
        d=assess([case([.99,.01,.01,.01,.99,.01,.01])],(.5,.5))
        self.assertEqual(d['wrong_repairs'],1);self.assertEqual(d['lost_mentions'],1)
    def test_raw_metrics_do_not_invent_recall_gain(self):
        d=assess([case()],(.5,.5))
        self.assertEqual(d['raw_baseline_metrics']['api_reference']['recall'],1.)
        self.assertEqual(d['raw_candidate_metrics']['api_reference']['recall'],1.)
    def test_unresolved_reasons_are_distinct(self):
        for p,reason in (([.1,.99,0,0,0,0,0],'boundary'),([.9,.9,.9,0,0,0,0],'multiple_roles'),([.9,0,0,0,0,0,0],'no_role'),(None,'unsupported')):
            _,log=resolve('x',raw(),lambda x:{(0,1):p},(.5,.5))
            self.assertEqual(log[0]['reason'],reason)
    def test_invalid_to_clean_wrong_is_blocked(self):
        c=case();c['text']='x y';c['raw']['entities']['model_key']=[dict(start=2,end=3,text='y')]
        d=assess([c],(.5,.5));self.assertEqual(d['invalid_to_valid_wrong'],1)
    def test_multi_role_gold_probe_fails(self):
        c=case();c['probes'][0]['probabilities'][2]=.99
        self.assertEqual(assess([c],(.5,.5))['gold_probe_failures'],1)
    def test_unsupported_negative_is_not_rejection(self):
        c=case();c['probes'][1]['probabilities']=None
        d=assess([c],(.5,.5));self.assertEqual(d['negative_total'],1);self.assertEqual(d['negative_rejected'],0)
    def test_supported_only_rejection_denominator(self):
        c=case();c['probes'].append(dict(start=0,end=1,expected_role=None,family='unsupported',probabilities=None))
        d=assess([c],(.5,.5))
        self.assertEqual(d['negative_supported'],1)
        self.assertEqual(d['supported_rejection_fraction'],1.)
        self.assertEqual(d['rejection_fraction'],.5)
        c['probes'][1]['probabilities']=None
        d=assess([c],(.5,.5))
        self.assertEqual(d['negative_supported'],0)
        self.assertIsNone(d['supported_rejection_fraction'])
    def test_shared_grid_tie_and_no_eligible(self):
        selected=select_thresholds({'1701':[case()],'1702':[case()]},split='calibration')
        self.assertEqual(selected['selected'],[.9,.9]);self.assertEqual(len(selected['candidates']),9)
        bad=case();bad['probes'][0]['probabilities']=None
        self.assertIsNone(select_thresholds({'1701':[case()],'1702':[bad]},split='calibration')['selected'])
    def test_selection_rejects_evaluation_split(self):
        with self.assertRaises(ValueError):select_thresholds({'1701':[case()],'1702':[case()]},split='fresh')
    def test_seed_or_question_missing_rejected(self):
        for data in ({'1701':[case()]},{'1701':[case()],'1702':[]}):
            with self.assertRaises(ValueError):select_thresholds(data,split='calibration')
    def test_qualification_requires_both_seeds_fresh_repair_and_timing(self):
        extra=case();extra['id']='value-case';extra['gold']=[[0,1,'value']];extra['raw']={'entities':{'value':[dict(start=0,end=1,text='x')]}};extra['operational_scores']=[];extra['probes']=[]
        d=assess([case(),extra],(.5,.5));groups={str(n):{'fresh':d,'historical':d} for n in (1701,1702)}
        self.assertTrue(qualification(groups,{'1701':.1,'1702':.2})['passed'])
        self.assertFalse(qualification(groups,{'1701':.1,'1702':1.1})['passed'])
        groups['1702']['fresh']=dict(d,correct_repairs=0)
        self.assertFalse(qualification(groups,{'1701':.1,'1702':.2})['passed'])

if __name__=='__main__':unittest.main()

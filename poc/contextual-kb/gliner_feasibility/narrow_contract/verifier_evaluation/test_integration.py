"""Synthetic plumbing only: these are neither Formly evaluation cases nor model evidence."""
import copy
import unittest
from decisions import ROLES,assess,qualification,select_thresholds
from pipeline import collect,timing,validate_fresh
from stages import evaluation_ready


def fixtures():
    rows=[];families=['cross_role','boundary','unfamiliar','ordinary']
    for i in range(40):
        gold=[[0,2,ROLES[i%6]],[3,5,ROLES[(i+1)%6]]] if i<36 else []
        probes=[dict(start=a,end=b,expected_role=r,family='gold') for a,b,r in gold]
        if i<36:
            a,b,f=(1,2,'clipped_path') if i<12 else (4,5,'broken_quote') if i<24 else (0,5,'merged_mentions')
            probes.append(dict(start=a,end=b,expected_role=None,family=f))
        if i<12:probes.append(dict(start=6,end=7,expected_role=None,family='nested_fragment'))
        if i<4:probes.append(dict(start=10,end=11,expected_role=None,family='unsupported'))
        rows.append(dict(id=str(i),text='aa bb cc dd example '+str(i),group=families[i//10],gold=gold,probes=probes))
    return rows


class Tests(unittest.TestCase):
    def test_full_synthetic_path(self):
        rows=fixtures();self.assertTrue(validate_fresh(rows));lookup={r['text']:r for r in rows}
        def extract(text):
            row=lookup[text];entities={r:[] for r in ROLES}
            for a,b,r in row['gold']:entities[r].append(dict(start=a,end=b,text=text[a:b]))
            if row['gold']:
                a,b,r=row['gold'][0];entities[ROLES[(ROLES.index(r)+2)%6]].append(dict(start=a,end=b,text=text[a:b]))
            return dict(entities=entities)
        def score(text,offsets):
            row=lookup[text];gold={(a,b):r for a,b,r in row['gold']};out={}
            for span in offsets:
                if span==(10,11):out[span]=None
                elif span in gold:out[span]=[.99]+[.99 if r==gold[span] else .01 for r in ROLES]
                else:out[span]=[.01]*7
            return out
        # Explicitly synthetic calibration envelope, separate from production sealed sets.
        cached={s:collect(rows,extract,score) for s in ('1701','1702')}
        choice=select_thresholds(cached,split='calibration');self.assertEqual(choice['selected'],[.9,.9])
        decision=dict(mode='calibration',bindings={'fixture':'fixed'},**choice)
        opened=evaluation_ready(decision,{'fixture':'fixed'},lambda:rows)
        groups={s:{'fresh':assess(collect(opened,extract,score),choice['selected'])} for s in cached}
        timed=timing(rows,{s:extract for s in cached},{s:score for s in cached},choice['selected'])
        self.assertTrue(qualification(groups,timed['budget_p95'])['passed'])
        self.assertEqual(groups['1701']['fresh']['negative_rejected'],48)
        self.assertEqual(groups['1701']['fresh']['negative_total'],52)
        self.assertEqual(groups['1701']['fresh']['correct_repairs'],36)
        self.assertEqual(len(timed['samples']),400)
    def test_fresh_missing_family_duplicate_text_and_wrong_gold_fail(self):
        for fault in ('family','duplicate','role'):
            rows=fixtures()
            if fault=='family':rows[0]['probes'].pop()
            if fault=='duplicate':rows[1]['text']=rows[0]['text']
            if fault=='role':rows[0]['gold'][0][2]='unknown'
            with self.assertRaises(ValueError):validate_fresh(rows)

if __name__=='__main__':unittest.main()

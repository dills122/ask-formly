"""Comparison bookkeeping; semantic judgments must be supplied, never inferred."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from contract import parse_json,validate

def canonical(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'))

def unique_panel(rows):
    if not isinstance(rows,list) or any(not isinstance(r,dict) or not isinstance(r.get('id'),str) for r in rows):
        raise ValueError('Invalid panel')
    if len({r['id'] for r in rows})!=len(rows):raise ValueError('Duplicate case IDs')
    return {r['id']:r for r in rows}

def assess_structure(cases,rows):
    expected=unique_panel(cases)
    try:
        indexed=unique_panel(rows)
        if set(indexed)-set(expected) or any(set(r)!={'id','output'} for r in rows):raise ValueError('Unexpected output envelope')
    except ValueError:indexed={}
    report={}
    for id in expected:
        try:
            v=validate(indexed[id]['output'])
            report[id]={'valid':True,'output':v}
        except (KeyError,ValueError):report[id]={'valid':False,'output':None}
    return report

def consistency(values):
    if not values or any(v is None for v in values):
        return dict(exact=False,questions=False,counts=False,constraints=False)
    return {'exact':len({canonical(v) for v in values})==1,
            'questions':len({canonical([q['question'] for q in v['formly_questions']]) for v in values})==1,
            'counts':len({len(v['formly_questions']) for v in values})==1,
            'constraints':len({canonical(v['library_constraints']) for v in values})==1}

def summarize_grades(cases,rubric,grades,structure):
    panel=unique_panel(cases);rules=unique_panel(rubric);gs=unique_panel(grades)
    if set(panel)!=set(rules) or set(panel)!=set(gs) or set(panel)!=set(structure):
        raise ValueError('Incomplete grading/structure evidence')
    results=[]
    for id,c in panel.items():
        g=gs[id]
        for key in ('required','forbidden'):
            if not isinstance(g.get(key),list) or len(g[key])!=len(rules[id][key]) or any(type(v) is not bool for v in g[key]):
                raise ValueError('Invalid criterion grades')
        if not isinstance(g.get('evidence'),str) or not g['evidence'].strip():raise ValueError('Missing evidence')
        valid=structure[id].get('valid')
        if type(valid) is not bool:raise ValueError('Invalid structural grade')
        passed=valid and all(g['required']) and not any(g['forbidden'])
        results.append(dict(g,group=c['group'],valid=valid,passed=passed))
    return {'total':len(panel),'passed':sum(r['passed'] for r in results),
            'groups':{group:{'total':sum(c['group']==group for c in cases),'passed':sum(r['passed'] for r in results if r['group']==group)} for group in sorted({c['group'] for c in cases})},
            'cases':results}

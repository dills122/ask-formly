"""Repeatability measurements, separate from supplied semantic judgments."""
import hashlib
import itertools
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from contract import validate,parse_json
RUNS=tuple(str(i) for i in range(1,6))

def canonical(value):return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'))

def summarize(cases,runs):
    ids=[c['id'] for c in cases]
    if len(set(ids))!=len(ids):raise ValueError('Duplicate cases')
    outputs={};errors={}
    for run in RUNS:
        try:
            rows=runs[run]
            if not isinstance(rows,list) or any(not isinstance(r,dict) or set(r)!={'id','output'} or not isinstance(r['id'],str) for r in rows):
                raise ValueError('Invalid trial envelope')
            if len({r['id'] for r in rows})!=len(rows) or set(r['id'] for r in rows)-set(ids):
                raise ValueError('Duplicate or unexpected case ID')
            by_id={r['id']:r['output'] for r in rows}
        except (KeyError,ValueError) as exc:
            by_id={};errors[run]=str(exc)
        for id in ids:
            try:outputs[run,id]=validate(by_id[id])
            except (KeyError,ValueError):outputs[run,id]=None
    per_case=[]
    for c in cases:
        values=[outputs[r,c['id']] for r in RUNS]
        valid=[v for v in values if v is not None]
        counts=[len(v['formly_questions']) if v is not None else None for v in values]
        signatures=[canonical(v) if v is not None else None for v in values]
        equal_pairs=sum(a is not None and a==b for a,b in itertools.combinations(signatures,2))
        per_case.append({'id':c['id'],'group':c['group'],'valid_runs':len(valid),'distinct_valid_outputs':len(set(canonical(v) for v in valid)),
                         'valid_by_run':{r:outputs[r,c['id']] is not None for r in RUNS},
                         'exact_stable':len(valid)==5 and len(set(signatures))==1,'equal_pairs':equal_pairs,'question_counts':counts,
                         'question_count_stable':len(valid)==5 and len(set(counts))==1,
                         'question_text_stable':len(valid)==5 and len({canonical([q['question'] for q in v['formly_questions']]) for v in valid})==1,
                         'constraints_stable':len(valid)==5 and len({canonical(v['library_constraints']) for v in valid})==1})
    total=len(cases)*5;valid_count=sum(c['valid_runs'] for c in per_case)
    return {'total':total,'valid':valid_count,'invalid_or_missing':total-valid_count,
            'exact_stable_cases':sum(c['exact_stable'] for c in per_case),
            'equal_pairs':sum(c['equal_pairs'] for c in per_case),'possible_pairs':len(cases)*10,
            'cases':per_case,'run_errors':errors,'semantic_quality':'not inferred from structural or exact agreement'}

def grade_summary(cases,rubric,grades,validity=None):
    if len({c["id"] for c in cases})!=len(cases):raise ValueError("Duplicate case IDs")
    if len({r["id"] for r in rubric})!=len(rubric):raise ValueError("Duplicate rubric IDs")
    expected={(r,c['id']) for r in RUNS for c in cases}
    if not isinstance(validity,dict) or set(validity)!=expected or any(type(v) is not bool for v in validity.values()):
        raise ValueError('Full structural validity map required')
    rules={r['id']:r for r in rubric}
    if set(rules)!={c['id'] for c in cases}:raise ValueError('Rubric coverage mismatch')
    indexed={}
    for g in grades:
        key=(g.get('run'),g.get('id'))
        if key not in expected or key in indexed:raise ValueError('Duplicate or unexpected grade')
        rule=rules[g['id']]
        for name in ('required','forbidden'):
            if not isinstance(g.get(name),list) or len(g[name])!=len(rule[name]) or any(type(v) is not bool for v in g[name]):
                raise ValueError('Invalid criterion grades')
        if not isinstance(g.get('evidence'),str) or not g['evidence'].strip():raise ValueError('Missing grading evidence')
        indexed[key]=g
    if set(indexed)!=expected:raise ValueError('Missing grades')
    def rubric_passes(g):return all(g['required']) and not any(g['forbidden'])
    def passes(g):return validity[g['run'],g['id']] and rubric_passes(g)
    per_run={r:sum(passes(indexed[r,c['id']]) for c in cases) for r in RUNS}
    per_group={group:sum(passes(indexed[r,c['id']]) for r in RUNS for c in cases if c['group']==group) for group in sorted({c['group'] for c in cases})}
    failures=[dict(g,valid_structure=validity[g['run'],g['id']]) for g in grades if not passes(g)]
    stability=[]
    for c in cases:
        gs=[indexed[r,c['id']] for r in RUNS]
        signatures={canonical([validity[g['run'],g['id']],g['required'],g['forbidden']]) for g in gs}
        stability.append({'id':c['id'],'distinct_grade_signatures':len(signatures),'passed_runs':sum(map(passes,gs))})
    return {'total':len(expected),'rubric_passed':sum(map(rubric_passes,grades)),'passed':sum(per_run.values()),'per_run_passed':per_run,'per_group_passed':per_group,
            'stable_scored_behavior_cases':sum(c['distinct_grade_signatures']==1 for c in stability),
            'cases':stability,'failures':failures,
            'limitation':'Stability of criterion grades is not full semantic equivalence; grades are agent judgments.'}

def main():
    p=Path(__file__).resolve().parent
    cases=parse_json((p/'cases.json').read_text());runs={};hashes={};load_errors={}
    for run in RUNS:
        f=p/'test-output'/f'repeat-{run}.json'
        try:
            raw=f.read_bytes();hashes[run]=hashlib.sha256(raw).hexdigest();runs[run]=parse_json(raw)
        except (OSError,ValueError) as exc:runs[run]=None;load_errors[run]=str(exc)
    report=summarize(cases,runs);report.update(raw_sha256=hashes,load_errors=load_errors)
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()

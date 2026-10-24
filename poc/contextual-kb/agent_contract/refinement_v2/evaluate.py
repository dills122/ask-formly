"""Freeze raw runs, blind grading packets, and join grades without dropping failures."""
import argparse
import hashlib
import json
from pathlib import Path
import random
from metrics import parse_json,assess_structure,consistency,summarize_grades
P=Path(__file__).resolve().parent
RUNS=tuple(f'{arm}{repeat}' for arm in ('alpha','beta') for repeat in ('1','2','3','reverse'))

def read(name):return parse_json((P/name).read_bytes())
def save(name,value):
    with (P/name).open('x') as f:json.dump(value,f,indent=2,ensure_ascii=False)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def frozen_inputs():
    for name,h in read('panel-freeze.json').items():
        if digest(P/name)!=h:raise ValueError('Frozen input changed: '+name)
def structures(cases):
    result={}
    for run in RUNS:
        try:rows=read(f'test-output/{run}.json')
        except (OSError,ValueError):rows=None
        result[run]=assess_structure(cases,rows)
    return result

def prepare():
    frozen_inputs();cases=read('cases.json');rules={r['id']:r for r in read('rubric.json')}
    ss=structures(cases);hashes={}
    for run in RUNS:
        f=P/f'test-output/{run}.json';hashes[run]=digest(f) if f.exists() else None
    save('test-output/raw-freeze.json',hashes)
    packets=[[],[],[]];mapping={};rng=random.Random(1207)
    for index,c in enumerate(cases):
        runs=list(RUNS);rng.shuffle(runs);candidates=[]
        for i,run in enumerate(runs):
            token=c['id']+'-'+chr(65+i);mapping[token]={'run':run,'id':c['id']}
            candidates.append({'candidate':token,'valid_structure':ss[run][c['id']]['valid'],'output':ss[run][c['id']]['output']})
        packets[index//10].append(dict(c,**rules[c['id']],candidates=candidates))
    for index,packet in enumerate(packets,1):save(f'test-output/packet-{index}.json',packet)
    save('test-output/grading-map.json',mapping)
    print('Frozen eight runs; three blinded panels prepared.')

def finalize():
    frozen_inputs();raw_hashes=read('test-output/raw-freeze.json')
    for run,h in raw_hashes.items():
        f=P/f'test-output/{run}.json'
        if (digest(f) if f.exists() else None)!=h:raise ValueError('Raw response changed: '+run)
    cases=read('cases.json');rubric=read('rubric.json');ss=structures(cases)
    mapping=read('test-output/grading-map.json');grades={r:[] for r in RUNS};seen=set()
    for panel in (1,2,3):
        for g in read(f'test-output/grades-{panel}.json'):
            token=g['candidate']
            if token in seen or token not in mapping:raise ValueError('Duplicate/unknown candidate grade')
            seen.add(token);m=mapping[token]
            grades[m['run']].append(dict(g,id=m['id']))
    if seen!=set(mapping):raise ValueError('Missing candidate grades')
    results={run:summarize_grades(cases,rubric,grades[run],ss[run]) for run in RUNS}
    stable={}
    for arm in ('alpha','beta'):
        stable[arm]=[dict(id=c['id'],**consistency([ss[arm+str(i)][c['id']]['output'] for i in (1,2,3)])) for c in cases]
    conformance={};rule=read('candidate-conformance.json')
    for run in RUNS:
        conformance[run]={}
        for id,required in rule.items():
            o=ss[run][id]['output']
            conformance[run][id]={'actual_questions':len(o['formly_questions']) if o else None,
                                 'passes_v2_representation':bool(o) and len(o['formly_questions'])==required['expected_questions'] and
                                 ('ui_adapter' not in required or o['library_constraints']['ui_adapter']==required['ui_adapter'])}
    report={'runs':results,'same_order_stability':stable,'candidate_specific_conformance':conformance,
            'structure_valid':{run:sum(r['valid'] for r in ss[run].values()) for run in RUNS},
            'raw_sha256':raw_hashes,'grades_sha256':{str(i):digest(P/f'test-output/grades-{i}.json') for i in (1,2,3)},
            'limits':'Three forward runs for consistency. Reverse-order runs reported separately. Combined score requires structure and rubric. No deterministic guarantee.'}
    save('test-output/final-summary.json',report)
    print(json.dumps({r:{'passed':v['passed'],'total':v['total']} for r,v in results.items()},indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['prepare','finalize']);args=parser.parse_args()
    (prepare if args.mode=='prepare' else finalize)()

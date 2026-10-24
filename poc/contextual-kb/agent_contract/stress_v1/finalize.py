"""Join frozen run outputs and blinded grades; fail on missing/mismatched evidence."""
import hashlib
import json
from pathlib import Path
from analyze import RUNS,parse_json,summarize,grade_summary


def main():
    p=Path(__file__).resolve().parent
    freeze=parse_json((p/'freeze.json').read_text())
    for name,digest in freeze['files'].items():
        if hashlib.sha256((p/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Frozen input changed: '+name)
    raw_freeze=parse_json((p/'test-output/raw-freeze.json').read_text())
    for name,digest in raw_freeze.items():
        if hashlib.sha256((p/'test-output'/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Raw output changed: '+name)
    cases=parse_json((p/'cases.json').read_text())
    runs={run:parse_json((p/'test-output'/f'repeat-{run}.json').read_text()) for run in RUNS}
    structure=summarize(cases,runs)
    validity={(run,case['id']):case['valid_by_run'][run] for case in structure['cases'] for run in RUNS}
    mapping=parse_json((p/'test-output/grading-map.json').read_text())
    grades=[]
    for name in ('a','b'):
        for g in parse_json((p/'test-output'/f'grades-{name}.json').read_text()):
            grades.append(dict(mapping[g['candidate']],required=g['required'],forbidden=g['forbidden'],evidence=g['evidence'],candidate=g['candidate']))
    quality=grade_summary(cases,parse_json((p/'rubric.json').read_text()),grades,validity)
    report={'structure':structure,'quality':quality,'raw_sha256':raw_freeze,
            'grade_sha256':{name:hashlib.sha256((p/'test-output'/f'grades-{name}.json').read_bytes()).hexdigest() for name in ('a','b')},
            'group_totals':{group:5*sum(c['group']==group for c in cases) for group in sorted({c['group'] for c in cases})}}
    with (p/'test-output/final-summary.json').open('x') as f:json.dump(report,f,indent=2)
    with (p/'test-output/joined-grades.json').open('x') as f:json.dump(grades,f,indent=2)
    print(json.dumps({k:v for k,v in quality.items() if k not in ('cases','failures')},indent=2))

if __name__=='__main__':main()

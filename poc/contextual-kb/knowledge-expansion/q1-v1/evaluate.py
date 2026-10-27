"""Read-only Q1 evidence audit, reusing the reviewed admission receipt loader."""
import importlib.util
import json
import sys
from pathlib import Path
from audit import compare_repeats,validate_judgments
from gate import assess
HERE=Path(__file__).resolve().parent
PREVIOUS=HERE.parent/'completion-v1'
sys.path.append(str(PREVIOUS))
from candidate import digest,assert_digest,preserved,checked_database
spec=importlib.util.spec_from_file_location('admission_report',PREVIOUS/'report.py')
loader=importlib.util.module_from_spec(spec);spec.loader.exec_module(loader)
loader.HERE=HERE  # Process-local path injection; no prior files are changed.


def verify():
    preserved();checked_database('baseline');checked_database('candidate')
    for name in ['freeze.json','assessment-freeze.json']:
        path=HERE/name
        if not path.is_file():raise FileNotFoundError(path)
        for relative,sha in json.loads(path.read_text())['files'].items():assert_digest(HERE/relative,sha)


def main():
    verify();cases=json.loads((HERE/'cases.json').read_text());answers={}
    for stage in ['initial','completed']:
        rows=[]
        for group in sorted({r['package'] for r in cases}):
            rows.extend(json.loads(loader.assessment_file(f'{stage}-candidate-{group}.json').read_text()))
        answers[stage]=rows
    runs=[];first=None
    for repeat in [1,2,3]:
        initial,completed,raw=loader.read_run('candidate',repeat,cases)
        if first is None:first=raw
        else:compare_repeats(first,raw)
        validate_judgments(answers['initial'],initial);validate_judgments(answers['completed'],completed)
        runs.append(dict(repeat=repeat,initial=assess(cases,answers['initial']),completed=assess(cases,answers['completed']),calls=len(raw)))
    print(json.dumps(dict(repeats=runs,total_calls=sum(r['calls'] for r in runs),exact_repeat_equality=True,
        semantics='Explicit caller judgments; identical-packet reuse, not independent generations. Model-backed mode preserved/preflight-checked only.'),indent=2))

if __name__=='__main__':main()

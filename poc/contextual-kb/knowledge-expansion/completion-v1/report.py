"""Recompute the predeclared gates from audited packets and caller judgments."""
import json
from pathlib import Path
from audit import compare_repeats,validate_observation,validate_judgments
from candidate import preserved,checked_database
HERE=Path(__file__).resolve().parent


def summarize(cases,baseline,candidate):
    b={r['id']:r for r in baseline};c={r['id']:r for r in candidate}
    regressions=[r['id'] for r in cases if b[r['id']]['usable'] and not c[r['id']]['usable']]
    critical=[r['id'] for r in candidate if r['critical_unsupported_claim']]
    packages={}
    for package in sorted({r['package'] for r in cases}):
        targets=[r['id'] for r in cases if r['package']==package and r['kind']=='target']
        controls=[r['id'] for r in cases if r['package']==package and r['kind']=='control']
        bt=sum(b[i]['usable'] for i in targets);ct=sum(c[i]['usable'] for i in targets)
        control_ok=all(c[i]['usable'] for i in controls)
        packages[package]=dict(target_requests=len(targets),baseline_target_usable=bt,candidate_target_usable=ct,
            controls=len(controls),candidate_controls_pass=control_ok,
            passes=ct*100>=len(targets)*90 and control_ok and not any(i in regressions or i in critical for i in targets+controls))
    return dict(packages=packages,regressions=regressions,critical_unsupported_claims=critical,
        baseline_total_usable=sum(r['usable'] for r in baseline),candidate_total_usable=sum(r['usable'] for r in candidate),
        requests=len(cases),passes=all(r['passes'] for r in packages.values()) and not critical and not regressions)


def assessment_file(name):
    paths=list((HERE/'test-output/assessment').rglob(name))
    if len(paths)!=1:raise ValueError(f'Expected exactly one {name}, got {paths}')
    return paths[0]


def read_run(arm,repeat,cases):
    rows=[]
    for package in sorted({r['package'] for r in cases}):
        stages=[('',HERE/f'test-output/calls/{package}.json')]
        for suffix,prefix in [('fetch','fetch'),('discovery','discovery'),('discovery2','discovery2'),('fetch2','fetch2')]:
            output=HERE/f'test-output/qualification/{arm}/r{repeat}/{package}-{suffix}.json'
            paths=list((HERE/'test-output/assessment').rglob(f'{prefix}-{arm}-{package}.json'))
            if len(paths)>1:raise ValueError('Duplicate recovery input')
            if paths and json.loads(paths[0].read_text()):stages.append(('-'+suffix,paths[0]))
            elif output.exists():raise ValueError('Unplanned recovery output')
        for suffix,input_path in stages:
            output=HERE/f'test-output/qualification/{arm}/r{repeat}/{package}{suffix}.json'
            calls=json.loads(input_path.read_text());batch=json.loads(output.read_text())
            receipt=json.loads(output.with_suffix('.receipt.json').read_text())
            if receipt!=dict(expected=len(calls),attempted=len(calls),errors=0,unattempted=[]):raise ValueError('Incomplete/error receipt')
            if [{k:r[k] for k in ('id','tool','arguments')} for r in batch]!=calls:raise ValueError('Actual calls differ from planned')
            if 'OFFLINE_GUARDS_ACTIVE' not in output.with_suffix('.stderr').read_text():raise ValueError('Offline guard absent')
            rows.extend(batch)
    plans={r['id']:r['arguments'] for r in json.loads((HERE/'lookup-calls.json').read_text())}
    initial,completed=validate_observation(rows,plans)
    return initial,completed,rows


def main():
    preserved();checked_database('baseline');checked_database('candidate')
    cases=json.loads((HERE/'cases.json').read_text());judgments={};arms={}
    for arm in ['baseline','candidate']:
        initial_answers=[];answers=[]
        for p in sorted({r['package'] for r in cases}):
            initial_answers.extend(json.loads(assessment_file(f'initial-{arm}-{p}.json').read_text()))
            answers.extend(json.loads(assessment_file(f'completed-{arm}-{p}.json').read_text()))
        first=None;initial_scores=[];scores=[]
        for repeat in [1,2,3]:
            initial,completed,raw=read_run(arm,repeat,cases)
            if first is None:first=raw
            else:compare_repeats(first,raw)
            initial_scores.append(validate_judgments(initial_answers,initial));scores.append(validate_judgments(answers,completed))
        judgments[arm]=answers
        arms[arm]=dict(initial_usable_each_repeat=initial_scores,completed_usable_each_repeat=scores,tool_calls_per_repeat=len(first),
            unique_initial_assessments=len(initial_answers),unique_completed_answers=len(answers),exact_repeat_packets=True)
    report=summarize(cases,judgments['baseline'],judgments['candidate']);report['arms']=arms
    report['total_tool_calls']=sum(r['tool_calls_per_repeat']*3 for r in arms.values())
    report['interpretation']='Manual calling-agent judgments on actual delivered packets; repeated identical-plan transport, not independent autonomous generations or unseen whole-library accuracy.'
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()

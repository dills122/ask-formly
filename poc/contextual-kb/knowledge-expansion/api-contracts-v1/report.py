"""Recompute the predeclared gates from audited packets and caller judgments."""
import json
from pathlib import Path
from audit import compare_repeats,validate_observation,validate_judgments
from candidate import preserved,checked_database,assert_digest
HERE=Path(__file__).resolve().parent


def summarize(cases,baseline,candidate):
    b={r['id']:r for r in baseline};c={r['id']:r for r in candidate}
    regressions=[r['id'] for r in cases if b[r['id']]['usable'] and not c[r['id']]['usable']]
    critical=[r['id'] for r in candidate if r['critical_unsupported_claim']]
    packages={}
    for package in sorted({r['package'] for r in cases}):
        targets=[r['id'] for r in cases if r['package']==package and r['kind']=='target']
        controls=[r['id'] for r in cases if r['package']==package and r['kind']=='control']
        preservation=[r['id'] for r in cases if r['package']==package and r['kind']=='regression']
        bt=sum(b[i]['usable'] for i in targets);ct=sum(c[i]['usable'] for i in targets)
        control_ok=all(c[i]['usable'] for i in controls)
        preservation_ok=all(c[i]['usable'] for i in preservation)
        # Package rates are descriptive; only the combined fresh-target rate gates the batch.
        packages[package]=dict(target_requests=len(targets),baseline_target_usable=bt,candidate_target_usable=ct,
            controls=len(controls),candidate_controls_pass=control_ok,
            regression_requests=len(preservation),candidate_regressions_usable=sum(c[i]['usable'] for i in preservation),
            candidate_regressions_pass=preservation_ok,
            passes=ct*100>=len(targets)*90 and control_ok and preservation_ok
                and not any(i in regressions or i in critical for i in targets+controls+preservation))
    targets=[r['id'] for r in cases if r['kind']=='target']
    controls=[r['id'] for r in cases if r['kind']=='control']
    preservation=[r['id'] for r in cases if r['kind']=='regression']
    target_usable=sum(c[i]['usable'] for i in targets)
    controls_usable=sum(c[i]['usable'] for i in controls)
    preservation_usable=sum(c[i]['usable'] for i in preservation)
    cohort_counts_ok=len(cases)==40 and len(targets)==24 and len(controls)==8 and len(preservation)==8
    passes=(cohort_counts_ok and target_usable*100>=len(targets)*90 and controls_usable==8
        and preservation_usable==8 and not critical and not regressions)
    return dict(packages=packages,regressions=regressions,critical_unsupported_claims=critical,
        target_requests=len(targets),candidate_target_usable=target_usable,
        controls=len(controls),candidate_controls_usable=controls_usable,
        regression_requests=len(preservation),candidate_regressions_usable=preservation_usable,
        cohort_counts_valid=cohort_counts_ok,
        baseline_total_usable=sum(r['usable'] for r in baseline),candidate_total_usable=sum(r['usable'] for r in candidate),
        requests=len(cases),passes=passes)


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


def verify_assessment_seal():
    seal = json.loads((HERE/'assessment-freeze.json').read_text())['files']
    observed = {str(p.relative_to(HERE)) for base in ('test-output/assessment','test-output/qualification')
                for p in (HERE/base).rglob('*') if p.is_file() and p.suffix in ('.json','.stderr')}
    if not observed or set(seal) != observed:
        raise ValueError('Assessment seal inventory mismatch')
    for name, sha in seal.items():
        path = HERE/name
        if path != path.resolve() or not path.resolve().is_relative_to(HERE.resolve()):
            raise ValueError('Assessment path escapes batch or is aliased')
        assert_digest(path, sha)


def main():
    verify_assessment_seal()
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
    # All three repeats were audited above and their complete packets match exactly.
    report['passes_each_repeat']=[report['passes'] for _ in range(3)]
    report['total_tool_calls']=sum(r['tool_calls_per_repeat']*3 for r in arms.values())
    report['interpretation']='Manual calling-agent judgments on actual delivered packets; repeated identical-plan transport, not independent autonomous generations or unseen whole-library accuracy.'
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()

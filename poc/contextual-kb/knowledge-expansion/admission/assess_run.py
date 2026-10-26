"""One-pass grading using an existing reviewed assessor; never retries a prior attempt."""
import argparse
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import re
import sys

EXPANSION = Path(__file__).resolve().parent.parent


def canonical(path, boundary):
    path = Path(path).absolute()
    if path != path.resolve() or not path.is_relative_to(boundary.resolve()):
        raise ValueError(f'Path outside allowed scope or symlink alias: {path}')
    return path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_implementation(implementation):
    # The CLI runs in a fresh process. Refuse collisions rather than importing a
    # same-named experiment from another batch in an embedding application's state.
    for name in ('assess','experiment','candidate','delivery'):
        module = sys.modules.get(name)
        if module is not None:
            origin = getattr(module,'__file__',None)
            if origin is None or Path(origin).resolve().parent != implementation:
                raise ValueError(f'Conflicting loaded module {name}; use a fresh CLI process')
    sys.path.insert(0,str(implementation))
    assessor = importlib.import_module('assess')
    spec = importlib.util.spec_from_file_location('_admission_existing_summarizer',implementation/'summarize.py')
    summarizer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(summarizer)
    return assessor,summarizer


# Fields added by the unchanged reviewed assessor. All other fields in a saved
# row are the original frozen case and must match, including optional fields.
ASSESSMENT_FIELDS = {'answer','delivery_errors','pool_ids','foundation_ids','final_ids',
                     'seconds','advisory','selection','index_setup_seconds','id_diagnostics',
                     'assessment','usable'}


def validate_case_binding(job, cases_by_id, cached=False):
    prompt_path = job/'prompt.json'
    if not prompt_path.exists() and not (job/'receipt.json').exists() and not cached:
        return  # An unfinished directory remains missing in fixed denominators.
    try:
        prompts = json.loads(prompt_path.read_text())
        if not isinstance(prompts,list) or not prompts:
            raise ValueError('Empty or malformed prompt')
        ids = []
        for prompt in prompts:
            case_id = prompt['id']
            if case_id not in cases_by_id or prompt['request'] != cases_by_id[case_id]['request'] or case_id in ids:
                raise ValueError('Prompt ID/request differs')
            ids.append(case_id)
    except (OSError,KeyError,TypeError,ValueError) as exc:
        raise ValueError(f'Saved prompt disagrees with current cases: {job.name}') from exc
    if not cached: return
    try:
        rows = json.loads((job/'assessment/results.json').read_text())['rows']
        if len(rows) != len(ids) or {row['id'] for row in rows} != set(ids):
            raise ValueError('Cached IDs differ from prompt')
        for row in rows:
            original_case = {key:value for key,value in row.items() if key not in ASSESSMENT_FIELDS}
            current_case = cases_by_id[row['id']]
            if json.dumps(original_case,sort_keys=True) != json.dumps(current_case,sort_keys=True):
                raise ValueError('Original case fields differ')
    except (OSError,KeyError,TypeError,ValueError) as exc:
        raise ValueError(f'Stale cached assessment disagrees with current cases; no regrade: {job.name}') from exc


def assess_run(implementation, root, cases_path, repeats, arms, *, expansion=EXPANSION, grader=None, summarizer=None):
    expansion = Path(expansion).resolve()
    if not re.fullmatch(r'[a-z][a-z0-9-]*',implementation):
        raise ValueError('Implementation must be a direct named knowledge-expansion child')
    implementation_path = canonical(expansion/implementation,expansion)
    for filename in ('assess.py','summarize.py'):
        if not canonical(implementation_path/filename,implementation_path).is_file():
            raise ValueError(f'Missing implementation {filename}')
    root = canonical(root,expansion)
    parts = root.relative_to(expansion).parts
    if len(parts) < 3 or parts[1] != 'test-output' or not root.is_dir():
        raise ValueError('Root must be an existing run directory inside a batch/test-output')
    # Existing assess/summary functions read nested artifacts. Reject aliases
    # before invoking them, including aliases in an existing assessment directory.
    for path in root.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'Run contains a symlink: {path}')
    cases_path = canonical(cases_path,expansion)
    cases = json.loads(cases_path.read_text())['cases']
    if not cases or any(not isinstance(c,dict) or not all(isinstance(c.get(k),str) and c[k] for k in ('id','request','category')) for c in cases):
        raise ValueError('Cases require nonempty id, request and category')
    if len({c['id'] for c in cases}) != len(cases) or len({c['request'] for c in cases}) != len(cases):
        raise ValueError('Cases must have unique IDs and requests')
    if any(set(case) & ASSESSMENT_FIELDS for case in cases):
        raise ValueError('Case fields collide with assessor-owned output fields')
    cases_by_id = {case['id']:case for case in cases}
    if type(repeats) is not int or repeats < 1:
        raise ValueError('Positive repeat count required')
    if not arms or len(arms) != len(set(arms)) or not set(arms) <= {'baseline','candidate'}:
        raise ValueError('Arms must be unique baseline and/or candidate')
    jobs = []
    for job in sorted(root.glob('r*-b*-*')):
        match = re.fullmatch(r'r([1-9][0-9]*)-b([1-9][0-9]*)-(baseline|candidate)',job.name)
        if match is None or not job.is_dir():
            raise ValueError(f'Malformed job directory: {job}')
        if match[3] not in arms: continue
        if int(match[1]) > repeats:
            raise ValueError(f'Job repeat exceeds requested denominator: {job.name}')
        jobs.append(job)
    if grader is None or summarizer is None:
        if grader is not None or summarizer is not None:
            raise ValueError('Supply both test dependencies or neither')
        grader,summarizer = load_implementation(implementation_path)
    to_grade = []
    for job in jobs:
        result = job/'assessment/results.json'
        validate_case_binding(job,cases_by_id)
        if result.exists():
            if not grader.assessment_complete(job):
                raise ValueError(f'Invalid existing assessment; explicit investigation required: {job.name}')
            validate_case_binding(job,cases_by_id,cached=True)
            continue
        if list((job/'assessment').glob('attempt-*')):
            raise ValueError(f'No retry after prior assessment attempt without result: {job.name}')
        if (job/'receipt.json').is_file(): to_grade.append(job)
    # Check every job for prior attempts before spending any new inference calls.
    for job in to_grade:
        grader.grade(job,cases)
        if not grader.assessment_complete(job):
            raise ValueError(f'Assessment produced no complete result: {job.name}')
        validate_case_binding(job,cases_by_id,cached=True)
    result = summarizer.summary(root,cases,repeats)
    result['rounds'] = [row for row in result['rounds'] if row['arm'] in arms]
    result['orchestration'] = dict(implementation=implementation,root=str(root),cases=str(cases_path),
        cases_sha256=sha(cases_path),implementation_sha256={name:sha(implementation_path/name) for name in ('assess.py','summarize.py')},
        repeats=repeats,arms=arms,graded_jobs=[job.name for job in to_grade],
        policy='No automatic assessment retries. Fixed denominators retain missing/duplicate assessments. Independent audit still required.')
    (root/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--implementation',required=True)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--cases',type=Path,required=True)
    parser.add_argument('--repeats',type=int,required=True)
    parser.add_argument('--arms',required=True,help='candidate or baseline,candidate')
    args = parser.parse_args()
    result = assess_run(args.implementation,args.root,args.cases,args.repeats,args.arms.split(','))
    for row in result['rounds']:
        print(row['round'],row['arm'],row['usable'],'/',row['total'],'critical',row['critical'])


if __name__ == '__main__': main()

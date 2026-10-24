"""Gated A/B runner. Imports no existing POC data/retrieval implementation."""
import argparse
from contextlib import ExitStack
import hashlib
import json
import math
from pathlib import Path
import platform
import random
import statistics as stats
import time
import urllib.request
from .runner import PlannerProcess
from .llama import BASE_URL, MODEL, MODEL_DIGEST
from .environment import hardware_snapshot

ROOT = Path(__file__).resolve().parents[1]


def verify_manifest(root, manifest):
    for name, expected in manifest.items():
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError('Manifest path outside root')
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Frozen file changed: {name}')


def schedule(ids, passes=5):
    rng = random.Random(1701)
    result = []
    for repeat in range(passes):
        ordered = list(ids)
        rng.shuffle(ordered)
        for position, case_id in enumerate(ordered):
            arms = ['A', 'B'] if (repeat + position) % 2 == 0 else ['B', 'A']
            result.extend((repeat, case_id, arm) for arm in arms)
    return result


def normalize(plan):
    # Contract IDs already sequential; preserve ordering, all text and grouping.
    return json.dumps(plan, sort_keys=True, ensure_ascii=True, separators=(',', ':'))


def statistics(rows):
    times = sorted(row['seconds'] for row in rows)
    return {'samples': len(rows), 'median_seconds': stats.median(times),
            'p95_seconds': times[math.ceil(.95 * len(times)) - 1],
            'max_seconds': max(times),
            'timeout_count': sum((r['plan'].get('failure') or {}).get('code') == 'timeout' for r in rows),
            'failure_count': sum(r['plan']['status'] == 'failed' for r in rows),
            'after_recovery_count': sum(r.get('after_recovery', False) for r in rows)}


def _api(path, payload=None, timeout=60):
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(BASE_URL + path, data=data,
                                     headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def collect_samples(jobs, cases, workers, stack, log, meta, rows, factory=PlannerProcess):
    for repeat, case_id, arm in jobs:
        recovered = workers[arm].process.poll() is not None
        if recovered:
            recovery = {'arm': arm, 'before_repeat': repeat, 'before_case': case_id}
            meta.setdefault('recoveries', []).append(recovery)
            recovery_start = time.monotonic()
            try:
                workers[arm] = stack.enter_context(factory(arm))
                recovery['startup_seconds'] = workers[arm].startup_seconds
                recovery['warmup'] = workers[arm].query('Where does a wrapper render its field?')
                if recovery['warmup']['plan']['status'] == 'failed':
                    raise RuntimeError('Recovery warmup failed; execution environment unavailable')
            except BaseException as exc:
                recovery['error'] = f'{type(exc).__name__}: {exc}'
                raise
            finally:
                recovery['seconds'] = time.monotonic() - recovery_start
        result = workers[arm].query(cases[case_id]['question'])
        row = {'repeat': repeat, 'case_id': case_id, 'arm': arm,
               'after_recovery': recovered, **result}
        rows.append(row)
        log.write(json.dumps(row) + '\n'); log.flush()
        print(f'{len(rows)}/{len(jobs)} {arm} {case_id} {result["plan"]["status"]}', flush=True)


def run(freeze_path, review_path, locked_path, output):
    """Only the reviewed executable may open the sealed cases."""
    freeze_bytes = freeze_path.read_bytes()
    freeze = json.loads(freeze_bytes)
    review = json.loads(review_path.read_text())
    if review.get('verdict') != 'Ready' or review.get('freeze_sha256') != hashlib.sha256(freeze_bytes).hexdigest():
        raise ValueError('Independent Ready review of this exact freeze required')
    verify_manifest(ROOT, freeze['files'])
    environment = json.loads((ROOT / freeze['environment_file']).read_text())
    actual_hardware = hardware_snapshot()
    if actual_hardware != environment['hardware']:
        raise ValueError('Hardware differs from reviewed environment manifest')
    locked = json.loads(locked_path.read_text())
    verify_manifest(ROOT, locked)
    commitment = json.loads((ROOT / 'planner_cases/heldout-commitment.json').read_text())
    # Explicit path comes from reviewed freeze, not from case text or model output.
    sealed_path = ROOT / freeze['heldout_file']
    sealed_bytes = sealed_path.read_bytes()
    if hashlib.sha256(sealed_bytes).hexdigest() != freeze['heldout_sha256']:
        raise ValueError('Held-out commitment mismatch')
    cases = json.loads(sealed_bytes)['cases']
    if len(cases) != 30 or len({c['id'] for c in cases}) != 30:
        raise ValueError('Expected thirty unique held-out cases')
    by_id = {c['id']: c for c in cases}
    output.mkdir(parents=True, exist_ok=False)
    meta = {'freeze_sha256': hashlib.sha256(freeze_bytes).hexdigest(),
            'platform': platform.platform(), 'python': platform.python_version(),
            'hardware': actual_hardware, 'environment': environment,
            'commitment': commitment, 'startup_seconds': {}, 'valid': False}
    rows = []
    try:
        models = _api('/api/tags')['models']
        if not any(m['name'] == MODEL and m['digest'] == MODEL_DIGEST for m in models):
            raise ValueError('Local model identity differs from frozen configuration')
        meta['ollama_version'] = _api('/api/version')
        meta['server_models_before'] = _api('/api/ps')
        # Loading is reported separately; do not unload another user's model.
        load_start = time.monotonic()
        warm = _api('/api/generate', {'model': MODEL, 'prompt': 'Ready', 'stream': False,
                    'keep_alive': '10m', 'options': {'num_predict': 1, 'num_ctx': 8192}})
        meta['model_preparation_seconds'] = time.monotonic() - load_start
        meta['model_load_duration_ns'] = warm.get('load_duration')
        meta['server_models_after_preparation'] = _api('/api/ps')
        with ExitStack() as stack, (output / 'raw.jsonl').open('x') as log:
            workers = {arm: stack.enter_context(PlannerProcess(arm)) for arm in ['A', 'B']}
            for arm, worker in workers.items():
                meta['startup_seconds'][arm] = worker.startup_seconds
                meta.setdefault('warmup', {})[arm] = worker.query('Where does a wrapper render its field?')
                if meta['warmup'][arm]['plan']['status'] == 'failed':
                    raise RuntimeError(f'Warmup failed for {arm}')
            collect_samples(schedule(list(by_id)), by_id, workers, stack, log, meta, rows)
        meta['server_models_after_samples'] = _api('/api/ps')
        verify_manifest(ROOT, freeze['files'])
        verify_manifest(ROOT, locked)
        meta['valid'] = True
        meta['timings'] = {arm: statistics([r for r in rows if r['arm'] == arm]) for arm in ['A', 'B']}
        meta['recovery_seconds'] = sum(r['seconds'] for r in meta.get('recoveries', []))
        # Remove method/timing/native trace before independent semantic grading.
        unique = {}
        mapping = []
        for row in rows:
            key = row['case_id'] + normalize(row['plan'])
            anon = hashlib.sha256(key.encode()).hexdigest()[:16]
            unique[anon] = {'output_id': anon, 'case_id': row['case_id'], 'plan': row['plan'],
                            'rubric': by_id[row['case_id']]['rubric'],
                            'expected_status': by_id[row['case_id']]['expected_status']}
            mapping.append({'output_id': anon, 'case_id': row['case_id'], 'arm': row['arm'], 'repeat': row['repeat']})
        (output / 'grading.json').write_text(json.dumps(sorted(unique.values(), key=lambda x: x['output_id']), indent=2))
        (output / 'mapping.json').write_text(json.dumps(mapping, indent=2))
    except BaseException as exc:
        meta['error'] = f'{type(exc).__name__}: {exc}'
        raise
    finally:
        try:
            verify_manifest(ROOT, locked)
            meta['locked_unchanged'] = True
        except ValueError as exc:
            meta['locked_unchanged'] = False
            meta['valid'] = False
            meta['lock_error'] = str(exc)
        (output / 'metadata.json').write_text(json.dumps(meta, indent=2))


def main():
    parser = argparse.ArgumentParser()
    for flag in ('freeze', 'review', 'locked', 'output'):
        parser.add_argument('--' + flag, type=Path, required=True)
    args = parser.parse_args()
    run(args.freeze, args.review, args.locked, args.output)


if __name__ == '__main__': main()

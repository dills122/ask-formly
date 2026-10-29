"""Frozen guided intent recovery comparison, independent of the grading IDs."""
import argparse
import asyncio
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
V1 = HERE.parent / 'retrieval_refinement_v1'
spec = importlib.util.spec_from_file_location('frozen_retrieval_v1', V1 / 'run.py')
v1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v1)


def select_candidates(candidates, delivered, focus, count):
    """Select observed records by uncovered focus terms; retain discovery tie order."""
    query = v1.tokens(focus)
    seen = {row['id'] for row in delivered}
    covered = set().union(*(v1.primary_tokens(row) for row in delivered)) if delivered else set()
    unique = {}
    for row in candidates:
        if row['id'] not in seen:
            unique.setdefault(row['id'], row)
    pool = list(unique.values())
    selected = []
    while pool and len(selected) < count:
        best = max(range(len(pool)), key=lambda index: (
            len((query - covered) & v1.primary_tokens(pool[index])),
            len(query & v1.primary_tokens(pool[index])), -index))
        row = pool.pop(best)
        if not query & v1.primary_tokens(row):
            break
        selected.append(row['id'])
        covered.update(v1.primary_tokens(row))
    return selected


async def execute_guided(session, parameters, case, policy):
    args = {key: value for key, value in case.items() if key != 'case_id'}
    calls = []
    first = await v1.call(session, calls, 'lookup_formly', args)
    delivered = list(first.get('facts', []))
    if first.get('status') == 'ok':
        for intent in policy['focuses'][case['case_id']]:
            discovery_args = dict(args, offset=0, limit=policy['discovery_limit'])
            if 'question_index' in parameters:
                discovery_args['question_index'] = intent['question_index']
            if 'focus' in parameters:
                discovery_args['focus'] = intent['focus']
            page = await v1.call(session, calls, 'discover_formly_candidates', discovery_args)
            selected = select_candidates(page.get('candidates', []), delivered,
                                         intent['focus'], policy['fetch_per_round'])
            if selected:
                packet = await v1.call(session, calls, 'get_formly_facts', dict(
                    fact_ids=selected, formly_version=args['formly_version'],
                    ui_adapter=args['ui_adapter']))
                delivered.extend(packet.get('facts', []))
    return dict(case_id=case['case_id'], calls=calls)


def failures(metrics, policy):
    errors = []
    gate = policy['gates']
    for mode, rows in metrics.items():
        signatures = {}
        for row in rows:
            key = mode + '/' + row['case_id']
            if row['status'] != row['expected_status'] or row['tool_errors']:
                errors.append(key + ': status/tool error')
            if row['undiscovered_fetch_ids']:
                errors.append(key + ': undiscovered fetch')
            if row['followup_calls'] > policy['max_followup_calls']:
                errors.append(key + ': call budget')
            if row['max_sdk_bytes'] > gate['max_sdk_bytes'] or row['max_packet_bytes'] > gate['max_packet_bytes']:
                errors.append(key + ': byte budget')
            signature = {k: v for k, v in row.items() if k != 'repetition'}
            if signatures.setdefault(row['case_id'], signature) != signature:
                errors.append(key + ': unstable repeats')
            if mode == 'candidate-guided' and row['missing_facets']:
                errors.append(key + ': missing essentials ' + str(row['missing_facets']))
    for index, base in enumerate(metrics['baseline-original']):
        peers = {mode: rows[index] for mode, rows in metrics.items()}
        if any((row['case_id'], row['repetition']) != (base['case_id'], base['repetition']) for row in peers.values()):
            raise ValueError('Unpaired metrics')
        if any(row['first_pass_ids'] != base['first_pass_ids'] for row in peers.values()):
            errors.append(base['case_id'] + ': first-pass changed')
        for source in ('baseline', 'candidate'):
            before, after = peers[source + '-original'], peers[source + '-guided']
            if not set(before['recovered_facets']) <= set(after['recovered_facets']):
                errors.append(source + '/' + base['case_id'] + ': guided facet regression')
        if not set(peers['baseline-guided']['recovered_facets']) <= set(peers['candidate-guided']['recovered_facets']):
            errors.append(base['case_id'] + ': candidate facet regression')
    before = sum(row['historical_id_count'] for row in metrics['candidate-original'])
    after = sum(row['historical_id_count'] for row in metrics['candidate-guided'])
    if after <= before:
        errors.append('No aggregate historical recovery gain')
    return sorted(set(errors))


async def replay(args):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    freeze = v1.verify_freeze(HERE)
    original_freeze = v1.verify_freeze(V1)
    db = args.database.resolve()
    if hashlib.sha256(db.read_bytes()).hexdigest() != args.sha256:
        raise ValueError('Database hash mismatch')
    args.output.mkdir(parents=True, exist_ok=False)
    cases = json.loads((HERE / 'cases.json').read_text())
    policy = json.loads((HERE / 'policy.json').read_text())
    original_policy = json.loads((V1 / 'policy.json').read_text())
    transcripts = {}
    for source, poc in [('baseline', args.baseline_poc), ('candidate', args.candidate_poc)]:
        command = [str(V1 / 'server.py'), '--poc', str(poc.resolve()), '--database', str(db),
                   '--sha256', args.sha256, '--settings', str(args.output / (source + '-settings.sqlite'))]
        with (args.output / (source + '-stderr.log')).open('w') as log:
            async with stdio_client(StdioServerParameters(command=sys.executable, args=command), errlog=log) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = {tool.name: tool for tool in (await session.list_tools()).tools}
                    parameters = tools['discover_formly_candidates'].inputSchema.get('properties', {})
                    for strategy in ('original', 'guided'):
                        mode = source + '-' + strategy
                        rows = []
                        for repetition in range(1, policy['repetitions'] + 1):
                            for case in cases:
                                if strategy == 'original':
                                    row = await v1.execute_case(session, parameters, case, original_policy)
                                else:
                                    row = await execute_guided(session, parameters, case, policy)
                                row['repetition'] = repetition
                                rows.append(row)
                                (args.output / (mode + '-transcript.json')).write_text(json.dumps(rows, indent=2) + '\n')
                        transcripts[mode] = rows
    # Grading IDs are first loaded after every tool decision/transcript is complete.
    rubric = json.loads((HERE / 'rubric.json').read_text())
    metrics = {mode: [v1.grade(row, rubric[row['case_id']]) for row in rows]
               for mode, rows in transcripts.items()}
    failed = failures(metrics, policy)
    if hashlib.sha256(db.read_bytes()).hexdigest() != args.sha256:
        raise AssertionError('DB changed')
    v1.verify_freeze(HERE)
    v1.verify_freeze(V1)
    report = dict(status='failed' if failed else 'passed', freeze=freeze, original_freeze=original_freeze,
                  mode='guided_fixed_intent_factorial_not_autonomous', database_sha256=args.sha256,
                  harness_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  source_roots=dict(baseline=str(args.baseline_poc.resolve()), candidate=str(args.candidate_poc.resolve())),
                  metrics=metrics, gate_failures=failed, limitations=policy['limitations'],
                  manual_answer_review='required_separately')
    (args.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], gate_failures=failed, report=str(args.output / 'report.json')), indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-poc', type=Path, required=True)
    parser.add_argument('--candidate-poc', type=Path, required=True)
    parser.add_argument('--database', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--output', type=Path, required=True)
    asyncio.run(replay(parser.parse_args()))

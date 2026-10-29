"""Frozen conditional evidence comparison; caller policies never load grading IDs."""
import argparse
import asyncio
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
V1 = HERE.parent / 'retrieval_refinement_v1'
V2 = HERE.parent / 'recovery_refinement_v2'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v1 = load('conditional_transport', V1 / 'run.py')
v2 = load('conditional_novelty', V2 / 'run.py')


def terms(text):
    """Frozen modest plural normalization, not API or semantic equivalence."""
    return {word[:-1] if len(word) > 3 and word.endswith('s')
            and not word.endswith(('ss', 'is')) else word for word in v1.tokens(text)}


def select_claim_first(candidates, delivered, focus, count):
    query = terms(focus)
    seen = {row['id'] for row in delivered}
    unique = {}
    for row in candidates:
        if row['id'] not in seen:
            unique.setdefault(row['id'], row)
    rows = list(unique.values())
    def score(row):
        return tuple(len(query & terms(str(row.get(field, ''))))
                     for field in ('claim', 'context', 'title'))
    ranked = sorted(rows, key=score, reverse=True)
    return [row['id'] for row in ranked if any(score(row))][:count]


async def execute(session, parameters, case, policy, strategy):
    args = {key: value for key, value in case.items() if key != 'case_id'}
    calls, shadows = [], []
    first = await v1.call(session, calls, 'lookup_formly', args)
    delivered = list(first.get('facts', []))
    offsets = {}
    if first.get('status') == 'ok':
        for intent in policy['focuses'][case['case_id']]:
            key = (intent['question_index'], intent['focus'])
            offset = offsets.get(key, 0)
            if offset is None:
                continue
            discovery_args = dict(args, offset=offset, limit=policy['discovery_limit'])
            if 'question_index' in parameters:
                discovery_args['question_index'] = key[0]
            if 'focus' in parameters:
                discovery_args['focus'] = key[1]
            page = await v1.call(session, calls, 'discover_formly_candidates', discovery_args)
            offsets[key] = page.get('next_offset')
            candidates = page.get('candidates', [])
            selections = {
                'novelty': v2.select_candidates(candidates, delivered, key[1], policy['fetch_per_round']),
                'claim-first': select_claim_first(candidates, delivered, key[1], policy['fetch_per_round']),
            }
            shadows.append(dict(discovery_call_index=len(calls)-1, focus=key[1],
                                question_index=key[0], selections=selections))
            selected = selections[strategy]
            if selected:
                packet = await v1.call(session, calls, 'get_formly_facts', dict(
                    fact_ids=selected, formly_version=args['formly_version'], ui_adapter=args['ui_adapter']))
                delivered.extend(packet.get('facts', []))
    return dict(case_id=case['case_id'], calls=calls, same_page_selections=shadows)


def failures(metrics, policy):
    failed = []
    gate = policy['gates']
    for mode, rows in metrics.items():
        signatures = {}
        for row in rows:
            key = mode + '/' + row['case_id']
            if row['status'] != row['expected_status'] or row['tool_errors']:
                failed.append(key + ': status/tool error')
            if row['expected_status'] == 'unsupported_scope' and row['recovered_ids']:
                failed.append(key + ': unsupported evidence')
            if row['undiscovered_fetch_ids']:
                failed.append(key + ': undiscovered fetch')
            if row['followup_calls'] > policy['max_followup_calls']:
                failed.append(key + ': call budget')
            if row['max_sdk_bytes'] > gate['max_sdk_bytes'] or row['max_packet_bytes'] > gate['max_packet_bytes']:
                failed.append(key + ': byte budget')
            signature = {k: v for k, v in row.items() if k != 'repetition'}
            if signatures.setdefault(row['case_id'], signature) != signature:
                failed.append(key + ': unstable repeats')
            if mode == 'candidate-claim-first':
                if row['missing_facets']:
                    failed.append(key + ': missing essential ' + str(row['missing_facets']))
                if row['case_id'] == 'G2' and 'hide-control-warning' not in row['first_pass_facets']:
                    failed.append(key + ': missing initial control warning')
                if row['case_id'] in gate['critical_controls_first_pass'] and len(row['first_pass_facets']) != row['essential_count']:
                    failed.append(key + ': first-pass control')
    for strategy in ('novelty', 'claim-first'):
        for base, candidate in zip(metrics['baseline-' + strategy], metrics['candidate-' + strategy]):
            if (base['case_id'], base['repetition']) != (candidate['case_id'], candidate['repetition']):
                raise ValueError('Unpaired metrics')
            if not set(base['first_pass_facets']) <= set(candidate['first_pass_facets']):
                failed.append(candidate['case_id'] + ': first-pass facet regression')
    return sorted(set(failed))


async def replay(args):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    freeze = v1.verify_freeze(HERE)
    original_freezes = [v1.verify_freeze(V1), v1.verify_freeze(V2)]
    db = args.database.resolve()
    if hashlib.sha256(db.read_bytes()).hexdigest() != args.sha256:
        raise ValueError('Database hash mismatch')
    args.output.mkdir(parents=True, exist_ok=False)
    cases = json.loads((HERE / 'cases.json').read_text())
    policy = json.loads((HERE / 'policy.json').read_text())
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
                    for strategy in policy['policies']:
                        mode, rows = source + '-' + strategy, []
                        for repetition in range(1, policy['repetitions'] + 1):
                            for case in cases:
                                row = await execute(session, parameters, case, policy, strategy)
                                row['repetition'] = repetition
                                rows.append(row)
                                (args.output / (mode + '-transcript.json')).write_text(json.dumps(rows, indent=2) + '\n')
                        transcripts[mode] = rows
    # All decisions, including shadow selections, are saved before grading loads.
    rubric = json.loads((HERE / 'rubric.json').read_text())
    metrics = {mode: [v1.grade(row, rubric[row['case_id']]) for row in rows]
               for mode, rows in transcripts.items()}
    ablations = {}
    for mode, rows in transcripts.items():
        ablations[mode] = []
        for row in rows:
            facets = rubric[row['case_id']]['essential']
            for shadow in row['same_page_selections']:
                ablations[mode].append(dict(case_id=row['case_id'], repetition=row['repetition'], **shadow,
                    selected_facets={strategy: [facet['id'] for facet in facets if set(facet['any_of']) & set(ids)]
                                     for strategy, ids in shadow['selections'].items()}))
    failed = failures(metrics, policy)
    if hashlib.sha256(db.read_bytes()).hexdigest() != args.sha256:
        raise AssertionError('DB changed')
    for path in (HERE, V1, V2):
        v1.verify_freeze(path)
    report = dict(status='failed' if failed else 'passed', freeze=freeze, original_freezes=original_freezes,
                  mode='guided_fixed_intent_factorial_not_autonomous', database_sha256=args.sha256,
                  harness_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  source_roots=dict(baseline=str(args.baseline_poc.resolve()), candidate=str(args.candidate_poc.resolve())),
                  metrics=metrics, same_page_ablations=ablations, gate_failures=failed,
                  limitations=policy['limitations'], manual_answer_review='required_separately')
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

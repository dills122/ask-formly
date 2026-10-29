"""Public development replay, not autonomous caller or answer-quality qualification.

The executor never reads rubric.json. Grading happens only after transcripts exist.
Recovery uses only text and IDs returned by discovery, with a fixed lexical policy.
"""
import argparse
import asyncio
from datetime import timedelta
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
STOP = {'the', 'and', 'for', 'with', 'from', 'formly', 'material', 'how', 'does', 'can',
        'what', 'that', 'this', 'its', 'are', 'into', 'when', 'show', 'example'}


def tokens(text):
    return {s.lower() for s in re.findall(r'[A-Za-z][A-Za-z0-9_]+', text)} - STOP


def select_recovery(candidates, seen, request, count=4):
    """No expected IDs or topic oracle: lexical overlap over discovered content."""
    query = tokens(request)
    unique = {row['id']: row for row in candidates if row['id'] not in seen}
    ranked = sorted(unique.values(), key=lambda row: (
        -len(query & tokens(' '.join(str(row.get(k, '')) for k in ('title', 'claim', 'context')))), row['id']))
    return [row['id'] for row in ranked[:count]]


def facts(packet):
    return [row['id'] for row in packet.get('facts', [])]


def decode(result):
    return result.structuredContent or json.loads(result.content[0].text)


async def call(session, transcript, name, arguments):
    result = await session.call_tool(name, arguments, read_timeout_seconds=timedelta(seconds=60))
    raw = result.model_dump(mode='json')
    size = len(json.dumps(raw, ensure_ascii=False).encode())
    try:
        packet = decode(result)
    except (ValueError, AttributeError, IndexError):
        packet = {'status': 'tool_error', 'text': str(result.content)}
    transcript.append(dict(tool=name, arguments=arguments, result=raw, packet=packet,
                           sdk_bytes=size, is_error=bool(result.isError)))
    if size > 30000:
        raise AssertionError(f'{name} exceeds 30000 serialized SDK bytes: {size}')
    return packet


async def execute_case(session, names, case):
    """Run fixed caller policy. Deliberately accepts no rubric argument."""
    args = {k: v for k, v in case.items() if k != 'case_id'}
    calls = []
    first = await call(session, calls, 'lookup_formly', args)
    seen = set(facts(first))
    if first.get('status') == 'ok':
        candidates, offset = [], 0
        for _ in range(2):
            page = await call(session, calls, 'discover_formly_candidates', dict(args, offset=offset, limit=8))
            candidates.extend(page.get('candidates', []))
            offset = page.get('next_offset')
            if offset is None:
                break
        recovery = select_recovery(candidates, seen, case['request'])
        scope = dict(formly_version=args['formly_version'], ui_adapter=args['ui_adapter'])
        # Two per fetch avoids making the recovery budget depend on record size.
        for start in range(0, len(recovery), 2):
            packet = await call(session, calls, 'get_formly_facts', dict(scope, fact_ids=recovery[start:start + 2]))
            seen.update(facts(packet))
        if 'get_formly_examples' in names:
            example_ids = []
            for start in range(0, len(seen), 16):
                linked = sorted(seen)[start:start + 16]
                offset = 0
                for _ in range(2):
                    packet = await call(session, calls, 'get_formly_examples', dict(scope, fact_ids=linked, offset=offset, limit=8))
                    example_ids.extend(row['id'] for row in packet.get('examples', []))
                    offset = packet.get('next_offset')
                    if offset is None:
                        break
            for example_id in sorted(set(example_ids))[:3]:
                await call(session, calls, 'get_formly_examples', dict(scope, example_ids=[example_id]))
    elif 'get_formly_examples' in names:
        # Unsupported scope is checked directly without inventing any known ID.
        await call(session, calls, 'get_formly_examples', dict(
            fact_ids=['hiding-and-visibility/reset-on-hide-false'],
            formly_version=args['formly_version'], ui_adapter=args['ui_adapter']))
    return dict(case_id=case['case_id'], mode='scripted_public_development_replay', calls=calls)


def grade(row, rubric):
    calls = row['calls']
    wanted = set(rubric['expected_fact_ids'])
    first = set(facts(calls[0]['packet']))
    recovered = set(first)
    fetched_examples = set()
    discovered = set()
    invalid_fetches = []
    for call_row in calls:
        packet = call_row['packet']
        if call_row['tool'] == 'discover_formly_candidates':
            discovered.update(r['id'] for r in packet.get('candidates', []))
        if call_row['tool'] == 'get_formly_facts':
            invalid_fetches.extend(set(call_row['arguments']['fact_ids']) - discovered - first)
            recovered.update(facts(packet))
        if call_row['tool'] == 'get_formly_examples' and call_row['arguments'].get('example_ids'):
            fetched_examples.update(r['id'] for r in packet.get('examples', []))
    return dict(case_id=row['case_id'], repetition=row.get('repetition', 1), expected=len(wanted), first_pass_expected=len(first & wanted),
                recovered_expected=len(recovered & wanted), missing_expected=sorted(wanted - recovered),
                first_pass_outside_rubric=len(first - wanted), recovered_outside_rubric=len(recovered - wanted),
                first_pass_ids=sorted(first), recovered_ids=sorted(recovered),
                status=calls[0]['packet'].get('status'), expected_status=rubric['expected_status'],
                status_matches=calls[0]['packet'].get('status') == rubric['expected_status'],
                followup_calls=len(calls)-1, recovery_ids_not_discovered=sorted(set(invalid_fetches)),
                examples_fetched=sorted(fetched_examples),
                missing_expected_examples=sorted(set(rubric.get('expected_example_ids', [])) - fetched_examples), tool_errors=sum(c['is_error'] for c in calls),
                max_sdk_bytes=max(c['sdk_bytes'] for c in calls),
                answer_quality='not_assessed', precision='not_assessed_outside_rubric_is_not_irrelevance')


async def replay(args):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    db = args.database.resolve()
    if hashlib.sha256(db.read_bytes()).hexdigest() != args.sha256:
        raise ValueError('Database hash mismatch')
    args.output.mkdir(parents=True, exist_ok=False)
    cases = json.loads((HERE / 'cases.json').read_text())
    all_rows = {}
    for mode in ('baseline', 'candidate'):
        script = HERE / 'baseline.py' if mode == 'baseline' else HERE.parent / 'serve.py'
        command = [str(script), '--database', str(db), '--sha256', args.sha256,
                   '--settings', str(args.output / (mode + '-settings.sqlite'))]
        with (args.output / (mode + '-stderr.log')).open('w') as log:
            async with stdio_client(StdioServerParameters(command=sys.executable, args=command), errlog=log) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    names = {t.name for t in (await session.list_tools()).tools}
                    rows = []
                    for repetition in range(1, 4):
                        for case in cases:
                            row = await execute_case(session, names, case)
                            row['repetition'] = repetition
                            rows.append(row)
                            (args.output / (mode + '-transcript.json')).write_text(json.dumps(rows, indent=2) + '\n')
                    all_rows[mode] = rows
    # Rubric is intentionally loaded only once all caller decisions are recorded.
    rubric = json.loads((HERE / 'rubric.json').read_text())
    metrics = {mode: [grade(row, rubric[row['case_id']]) for row in rows] for mode, rows in all_rows.items()}
    parity = []
    for base, candidate in zip(metrics['baseline'], metrics['candidate']):
        parity.append(dict(case_id=base['case_id'],
                           first_pass_fact_ids_equal=base['first_pass_ids'] == candidate['first_pass_ids'],
                           recovered_fact_ids_equal=base['recovered_ids'] == candidate['recovered_ids']))
    stable = {}
    for mode, rows in metrics.items():
        signatures = {}
        for row in rows:
            signature = {k: v for k, v in row.items() if k != 'repetition'}
            previous = signatures.setdefault(row['case_id'], signature)
            if previous != signature:
                raise AssertionError(f'Non-deterministic metrics for {mode}/{row["case_id"]}')
        stable[mode] = True
    report = dict(mode='scripted_public_development_replay', database_sha256=args.sha256,
                  cases_sha256=hashlib.sha256((HERE / 'cases.json').read_bytes()).hexdigest(),
                  rubric_sha256=hashlib.sha256((HERE / 'rubric.json').read_bytes()).hexdigest(),
                  repetitions=3,
                  stable_repeated_metrics=stable,
                  limitations=['Fixed plans are not autonomous calling-agent evidence.',
                               'Expected IDs measure selected evidence coverage, not answer correctness.',
                               'Outside-rubric facts are not automatically irrelevant.',
                               'Two discovery pages and four recovery facts are a bounded policy, not exhaustive recall.'],
                  metrics=metrics, parity=parity)
    (args.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    if hashlib.sha256(db.read_bytes()).hexdigest() != args.sha256:
        raise AssertionError('Database changed during read-only replay')
    assert all(r['status_matches'] and not r['tool_errors'] and not r['recovery_ids_not_discovered'] for mode in metrics.values() for r in mode), report
    assert all(not r['missing_expected_examples'] for r in metrics['candidate']), metrics['candidate']
    assert all(p['first_pass_fact_ids_equal'] and p['recovered_fact_ids_equal'] for p in parity), parity
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--output', type=Path, required=True)
    asyncio.run(replay(parser.parse_args()))

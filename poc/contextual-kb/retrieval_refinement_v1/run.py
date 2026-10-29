"""Frozen public retrieval comparison. The executor never loads the grading rubric."""
import argparse
import asyncio
from datetime import timedelta
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
STOP = frozenset('a an and are as at be by can do does for formly from how i if in is it its my of on or should that the then this to use using what when where which why with would could please explain material'.split())


def tokens(text):
    return {word.casefold() for word in re.findall(r'[A-Za-z][A-Za-z0-9_]*', text)
            if word.casefold() not in STOP}


def primary_tokens(record):
    return tokens(' '.join(str(record.get(key, '')) for key in ('title', 'claim', 'context')))


def select_question(questions, delivered, used):
    available = [i for i in range(len(questions)) if i not in used] or list(range(len(questions)))
    corpus = set().union(*(primary_tokens(row) for row in delivered)) if delivered else set()
    def coverage(i):
        query = tokens(questions[i]['question'])
        return len(query & corpus) / max(1, len(query)), i
    return min(available, key=coverage)


def select_recovery(candidates, seen, question, count=2):
    query = tokens(question)
    unique = {row['id']: row for row in candidates if row['id'] not in seen}
    ranked = sorted(unique.values(), key=lambda row: (-len(query & primary_tokens(row)), row['id']))
    return [row['id'] for row in ranked[:count]]


def verify_freeze(folder=HERE):
    manifest = json.loads((folder / 'freeze.json').read_text())
    for name, expected in manifest['files'].items():
        if hashlib.sha256((folder / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen input changed: ' + name)
    return manifest


def fact_ids(packet):
    return [row['id'] for row in packet.get('facts', [])]


async def call(session, calls, tool, arguments):
    result = await session.call_tool(tool, arguments, read_timeout_seconds=timedelta(seconds=60))
    raw = result.model_dump(mode='json')
    packet = result.structuredContent
    if packet is None:
        try:
            packet = json.loads(result.content[0].text)
        except (ValueError, IndexError, AttributeError):
            packet = {'status': 'tool_error', 'text': str(result.content)}
    calls.append(dict(tool=tool, arguments=arguments, packet=packet, result=raw,
                      sdk_bytes=len(json.dumps(raw, ensure_ascii=False).encode()),
                      packet_bytes=len(json.dumps(packet, ensure_ascii=False).encode()),
                      is_error=bool(result.isError)))
    return packet


async def execute_case(session, discovery_parameters, case, policy):
    """Receive cases/policy only. Expected IDs are unavailable until grading."""
    args = {key: value for key, value in case.items() if key != 'case_id'}
    calls = []
    first = await call(session, calls, 'lookup_formly', args)
    seen = set(fact_ids(first))
    delivered = list(first.get('facts', []))
    used = set()
    offsets = {}
    if first.get('status') == 'ok':
        questions = args['plan']['formly_questions']
        for _ in range(policy['rounds']):
            qi = select_question(questions, delivered, used)
            used.add(qi)
            targeted = 'question_index' in discovery_parameters
            key = qi if targeted else 'global'
            offset = offsets.get(key, 0)
            if offset is None:
                continue
            discovery_args = dict(args, offset=offset, limit=policy['discovery_limit'])
            if targeted:
                discovery_args['question_index'] = qi
            page = await call(session, calls, 'discover_formly_candidates', discovery_args)
            offsets[key] = page.get('next_offset')
            selected = select_recovery(page.get('candidates', []), seen,
                                       questions[qi]['question'], policy['fetch_per_round'])
            if not selected:
                continue
            packet = await call(session, calls, 'get_formly_facts', dict(
                fact_ids=selected, formly_version=args['formly_version'], ui_adapter=args['ui_adapter']))
            seen.update(fact_ids(packet))
            delivered.extend(packet.get('facts', []))
    return dict(case_id=case['case_id'], calls=calls)


def supported_facets(ids, facets):
    return [facet['id'] for facet in facets if set(facet['any_of']) & set(ids)]


def grade(row, rubric):
    first = set(fact_ids(row['calls'][0]['packet']))
    seen = set(first)
    discoverable = set(first)
    illegal = []
    for entry in row['calls'][1:]:
        if entry['tool'] == 'discover_formly_candidates':
            discoverable.update(candidate['id'] for candidate in entry['packet'].get('candidates', []))
        elif entry['tool'] == 'get_formly_facts':
            illegal.extend(set(entry['arguments']['fact_ids']) - discoverable)
            seen.update(fact_ids(entry['packet']))
    essentials = rubric['essential']
    first_facets = supported_facets(first, essentials)
    final_facets = supported_facets(seen, essentials)
    wanted = {facet['id'] for facet in essentials}
    return dict(case_id=row['case_id'], repetition=row.get('repetition', 1),
        diagnostic_only=rubric.get('diagnostic_only', False),
        essential_count=len(essentials), first_pass_facets=first_facets,
        recovered_facets=final_facets, missing_facets=sorted(wanted-set(final_facets)),
        first_pass_ids=sorted(first), recovered_ids=sorted(seen),
        conditional_evidence={condition: sorted(set(ids)&seen) for condition, ids in rubric['conditional'].items()},
        historical_id_count=len(set(rubric.get('historical_expected_fact_ids', []))&seen),
        status=row['calls'][0]['packet'].get('status'), expected_status=rubric['expected_status'],
        followup_calls=len(row['calls'])-1, undiscovered_fetch_ids=sorted(set(illegal)),
        tool_errors=sum(entry['is_error'] for entry in row['calls']),
        max_sdk_bytes=max(entry['sdk_bytes'] for entry in row['calls']),
        max_packet_bytes=max(entry['packet_bytes'] for entry in row['calls']),
        manual_answer_review='required_not_automatically_scored')


def gate_failures(metrics, policy):
    failures = []
    gate = policy['gates']
    for mode, rows in metrics.items():
        signatures = {}
        for row in rows:
            case = row['case_id']
            if row['status'] != row['expected_status']:failures.append(f'{mode}/{case}: scope/status')
            if row['expected_status'] == 'unsupported_scope' and row['recovered_ids']:failures.append(f'{mode}/{case}: unsupported facts')
            if row['tool_errors']:failures.append(f'{mode}/{case}: tool error')
            if row['undiscovered_fetch_ids']:failures.append(f'{mode}/{case}: oracle fetch')
            if row['followup_calls'] > policy['max_followup_calls']:failures.append(f'{mode}/{case}: call budget')
            if row['max_sdk_bytes'] > gate['max_sdk_bytes'] or row['max_packet_bytes'] > gate['max_packet_bytes']:failures.append(f'{mode}/{case}: byte budget')
            signature = {key:value for key,value in row.items() if key != 'repetition'}
            if signatures.setdefault(case, signature) != signature:failures.append(f'{mode}/{case}: unstable repeats')
            if mode == 'candidate' and not row['diagnostic_only']:
                if row['missing_facets']:failures.append(f'{mode}/{case}: missing essentials {row["missing_facets"]}')
                if case in gate['critical_controls_all_essential_first_pass'] + gate['alias_pair_both_observation_first_pass']:
                    if len(row['first_pass_facets']) != row['essential_count']:failures.append(f'{mode}/{case}: first-pass control')
    for base,candidate in zip(metrics['baseline'],metrics['candidate']):
        if (base['case_id'],base['repetition']) != (candidate['case_id'],candidate['repetition']):raise ValueError('Unpaired results')
        if not candidate['diagnostic_only'] and len(candidate['first_pass_facets']) < len(base['first_pass_facets']):
            failures.append('candidate/'+candidate['case_id']+': first-pass regression')
    return sorted(set(failures))


async def replay(args):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    freeze = verify_freeze()
    db = args.database.resolve()
    if hashlib.sha256(db.read_bytes()).hexdigest() != args.sha256:raise ValueError('Database hash mismatch')
    args.output.mkdir(parents=True, exist_ok=False)
    cases = json.loads((HERE/'cases.json').read_text())
    policy = json.loads((HERE/'policy.json').read_text())
    transcripts = {}
    for mode,poc in [('baseline',args.baseline_poc),('candidate',args.candidate_poc)]:
        command = [str(HERE/'server.py'),'--poc',str(poc.resolve()),'--database',str(db),'--sha256',args.sha256,
                   '--settings',str(args.output/(mode+'-settings.sqlite'))]
        with (args.output/(mode+'-stderr.log')).open('w') as log:
            async with stdio_client(StdioServerParameters(command=sys.executable,args=command),errlog=log) as (read,write):
                async with ClientSession(read,write) as session:
                    await session.initialize()
                    tools = {tool.name: tool for tool in (await session.list_tools()).tools}
                    discovery_parameters = tools['discover_formly_candidates'].inputSchema.get('properties',{})
                    rows=[]
                    for repetition in range(1,policy['repetitions']+1):
                        for case in cases:
                            row=await execute_case(session,discovery_parameters,case,policy)
                            row['repetition']=repetition;rows.append(row)
                            (args.output/(mode+'-transcript.json')).write_text(json.dumps(rows,indent=2)+'\n')
                    transcripts[mode]=rows
    # Only here are the oracle IDs/alternatives loaded. They cannot guide execution.
    rubric=json.loads((HERE/'rubric.json').read_text())
    metrics={mode:[grade(row,rubric[row['case_id']]) for row in rows] for mode,rows in transcripts.items()}
    failures=gate_failures(metrics,policy)
    if hashlib.sha256(db.read_bytes()).hexdigest()!=args.sha256:raise AssertionError('DB changed')
    verify_freeze()
    report=dict(status='failed' if failures else 'passed',freeze=freeze,database_sha256=args.sha256,
                harness_sha256={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ('run.py','server.py')},
                source_roots=dict(baseline=str(args.baseline_poc.resolve()),candidate=str(args.candidate_poc.resolve())),
                mode='deterministic_public_replay_not_autonomous_answers',metrics=metrics,gate_failures=failures,
                manual_answer_review='pending_separate_fresh_caller',limitations=policy['limitations'])
    (args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'gate_failures':failures,'report':str(args.output/'report.json')},indent=2))
    if failures:raise SystemExit(1)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-poc',type=Path,required=True)
    parser.add_argument('--candidate-poc',type=Path,required=True)
    parser.add_argument('--database',type=Path,required=True)
    parser.add_argument('--sha256',required=True)
    parser.add_argument('--output',type=Path,required=True)
    asyncio.run(replay(parser.parse_args()))

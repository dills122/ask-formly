"""Blind, separate-context semantic assessment plus deterministic delivery checks."""
import argparse,json,os,signal,subprocess,time,sys
from pathlib import Path
from experiment import HERE,POC,MODEL,EFFORT,parse_agent_output
from mcp_v1.planner import planner_command,decode_plan
from delivery import verify_calls


def inventory():
    result={}
    catalog=json.loads((POC/'corpus/evidence-catalog.json').read_text())['records']
    evidence={e['id']:e for e in catalog}
    for folder in (POC/'authored',HERE/'draft-authored'):
        for path in folder.glob('*.json'):
            d=json.loads(path.read_text())
            for f in d['facts']:result[d['id']+'/'+f['id']]=dict(f,version=d['formly_version'],adapter=d['adapter'],evidence=[evidence[e] for e in f['evidence_ids']])
    return result


def prepare(job,cases):
    byrequest={c['request']:c for c in cases}
    requests=json.loads((job/'prompt.json').read_text())
    expected=[r['request'] for r in requests]
    events=[json.loads(line) for line in (job/'events.jsonl').read_text().splitlines() if line]
    errors=[]
    receipt=json.loads((job/'receipt.json').read_text())
    if receipt.get('exit_code')!=0 or receipt.get('error'):
        errors.append('Calling-agent process/receipt failed')
    try:verify_calls(events,expected)
    except Exception as exc:errors.append(str(exc))
    try:answers=parse_agent_output(events,[r['id'] for r in requests])['answers']
    except Exception as exc:errors.append(str(exc));answers=[]
    audits=[json.loads(p.read_text()) for p in (job/'mcp/audit').glob('*.json')]
    rows=[]
    for request in requests:
        c=byrequest[request['request']]; matches=[a for a in audits if a['request']==c['request']]
        answer=next((a for a in answers if a['id']==c['id']),None)
        row=dict(c,answer=answer,delivery_errors=list(errors))
        if len(matches)!=1 or 'result' not in matches[0]:
            row.update(delivery_errors=row['delivery_errors']+['No single successful MCP audit'],pool_ids=[],foundation_ids=[],final_ids=[])
        else:
            audit=matches[0];r=audit['result']; ids=r['retrieval']['ids']; foundation=r['retrieval']['foundation_ids']
            calls=[e['item'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='mcp_tool_call' and e['item'].get('arguments',{}).get('request')==c['request']]
            if len(calls)!=1 or calls[0].get('status')!='completed' or calls[0].get('error') is not None or (calls[0].get('result') or {}).get('structured_content')!=r:
                row['delivery_errors'].append('Delivered MCP packet differs from successful saved audit')
            pool=list(dict.fromkeys(foundation+[f for q in r['selection']['queries'] for f in q['ids']]))
            row.update(pool_ids=pool,foundation_ids=foundation,final_ids=ids,seconds=audit['seconds'],advisory=r['advisory']['status'],selection=r['selection']['status'],index_setup_seconds=r['runtime']['index_setup_seconds'])
            if answer is None or not set(answer['citations'])<=set(ids):row['delivery_errors'].append('Missing answer or nonreturned citation')
            row['id_diagnostics']={stage:sum(f in values for f in c['required_support'])/len(c['required_support']) if c['required_support'] else None for stage,values in [('pool',pool),('foundation',foundation),('final',ids)]}
        rows.append(row)
    return rows


def grade(job,cases):
    rows=prepare(job,cases);assessment=job/'assessment';assessment.mkdir(exist_ok=True)
    attempts=list(assessment.glob('attempt-*'))
    if len(attempts)>=2:raise ValueError('Assessment failed twice; report ungraded batch, do not omit it')
    out=assessment/f'attempt-{len(attempts)+1}';out.mkdir(exist_ok=False)
    public=[{k:v for k,v in r.items() if k not in ('seconds','advisory','selection','index_setup_seconds','id_diagnostics')} for r in rows]
    prompt=json.dumps(dict(facts=inventory(),cases=public));(out/'input.json').write_text(prompt)
    command=planner_command('codex',HERE/'GRADER.md',HERE/'grade.schema.json',out)
    start=time.perf_counter()
    with (out/'events.jsonl').open('xb') as stdout,(out/'stderr.txt').open('xb') as stderr:
        process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=stdout,stderr=stderr,start_new_session=True)
        try:process.communicate(prompt.encode(),timeout=300)
        except BaseException:
            os.killpg(process.pid,signal.SIGTERM)
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait()
            raise
    if process.returncode:raise ValueError('Independent grader process failed')
    events=[json.loads(l) for l in (out/'events.jsonl').read_text().splitlines() if l]
    messages=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
    if events[-1].get('type')!='turn.completed' or len(messages)!=1:raise ValueError('Grader delivery failed')
    if any(e.get('type')=='item.completed' and e.get('item',{}).get('type') not in ('reasoning','agent_message') for e in events):raise ValueError('Grader used tools')
    judgments=decode_plan(messages[0])['results']
    if len(judgments)!=len(rows) or {r['id'] for r in judgments}!={r['id'] for r in rows}:raise ValueError('Grader IDs differ')
    for row in rows:
        row['assessment']=next(j for j in judgments if j['id']==row['id'])
        # Delivery failures cannot be rescued by prose or model generosity.
        row['usable']=not row['delivery_errors'] and row['assessment']['answer_usable'] and not row['assessment']['critical']
    report=dict(model=MODEL,effort=EFFORT,seconds=time.perf_counter()-start,method='Separate-context automated semantic review, arm identity withheld; requires final independent audit.',rows=rows)
    (out/'results.json').write_text(json.dumps(report,indent=2));(assessment/'results.json').write_text(json.dumps(report,indent=2));print(job.name,'usable',sum(r['usable'] for r in rows),'/',len(rows),flush=True)


def assessment_complete(job):
    try:
        report=json.loads((job/'assessment/results.json').read_text())
        expected=[r['id'] for r in json.loads((job/'prompt.json').read_text())]
        rows=report['rows']
        return len(rows)==len(expected) and {r['id'] for r in rows}==set(expected) and all(type(r['usable']) is bool and isinstance(r['assessment'],dict) for r in rows)
    except (OSError,ValueError,KeyError,TypeError):return False


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',required=True);parser.add_argument('--cases',required=True);args=parser.parse_args()
    root=Path(args.root).resolve();cases=json.loads(Path(args.cases).read_text())['cases']
    if not root.is_relative_to(HERE/'test-output'):raise ValueError('Assessment output outside POC experiment')
    for job in sorted(root.glob('r*-b*-*')):
        if (job/'receipt.json').exists() and not assessment_complete(job):grade(job,cases)

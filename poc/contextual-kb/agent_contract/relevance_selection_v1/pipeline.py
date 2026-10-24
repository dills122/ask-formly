"""Exclusive first-save acquisition and later accounting of native selections."""
import hashlib,json,os,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parents[1]
sys.path.insert(0,str(POC))
from agent_contract.qualification_v3.candidate import build_plan
from agent_contract.retrieval_integration_v1.bridge import readonly
from kbcompiler.question_pilot import PilotIndex
from agent_contract.relevance_selection_v1.candidate import acquire,present,account
from agent_contract.relevance_selection_v1.assessment import assess,ARMS

def read(path):return json.loads(Path(path).read_text())
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(path,value):
    with Path(path).open('x') as f:json.dump(value,f,indent=2,allow_nan=False)
def verify(path):
    for filename,digest in read(path).items():
        if sha(filename)!=digest:raise ValueError('frozen input changed: '+filename)
def freeze(path,files):save(path,{str(p.resolve()):sha(p) for p in files})

def acquire_all():
    for name in ('design','generation','run'):verify(HERE/f'test-output/{name}-freeze.json')
    if read(HERE/'PREFLIGHT-DECISION.json')['verdict'].lower()!='ready':raise ValueError('preflight not ready')
    records=read(HERE/'data/records.json');cases=read(HERE/'data/cases.json')
    expected=[r['id'] for r in read(HERE/'data/requests.json')]
    if len(expected)!=36 or len(set(expected))!=36 or [r['id'] for r in records]!=expected or [r['id'] for r in cases]!=expected:raise ValueError('input/gold coverage')
    out=HERE/'test-output/acquisition';out.mkdir(exist_ok=False)
    save(out/'first-save.json',dict(run_freeze=sha(HERE/'test-output/run-freeze.json'),started_epoch=time.time()))
    os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(HERE/'test-output/embed-cache'),HF_HUB_OFFLINE='1')
    dbpath=POC/'build/knowledge.sqlite';dbhash=sha(dbpath);traces=[];payloads={};mappings={}
    with readonly(dbpath) as db:
        started=time.perf_counter();index=PilotIndex(db)
        save(out/'setup.json',dict(seconds=time.perf_counter()-started,facts=len(index.ids),db_hash=dbhash))
        for case in cases:
            if not set(case['relevant_fact_ids'])<=set(index.ids) or any(not g or not set(g)<=set(case['relevant_fact_ids']) for g in case['required_groups']) or bool(case['relevant_fact_ids'])!=bool(case['required_groups']):raise ValueError('invalid gold')
        with (out/'traces.jsonl').open('x') as f:
            for record in records:
                error=record['foundation_error'];core=record['output']
                if not error:
                    try:build_plan(record['request'],core)
                    except (ValueError,TypeError,KeyError) as exc:error=str(exc)
                if error:
                    trace=dict(queries=[],foundation=[],wide_rank=[],narrow_pool=[],wide_pool=[])
                    core=dict(formly_questions=[],condition_bindings=[],library_constraints={'formly_version':None,'ui_adapter':None})
                else:trace=acquire(index,core)
                trace.update(id=record['id'],batch=record['batch'],foundation_error=error);traces.append(trace)
                f.write(json.dumps(trace,allow_nan=False)+'\n');f.flush()
                for arm in ('narrow','wide'):
                    key=f'{arm}-batch{record["batch"]}'
                    payload,mapping=present(record['id'],core,trace[arm+'_pool'],index.facts)
                    payloads.setdefault(key,[]).append(payload);mappings.setdefault(key,{})[record['id']]=mapping
        if sha(dbpath)!=dbhash:raise ValueError('DB changed')
    for key,value in payloads.items():save(out/(key+'.json'),value)
    save(out/'mappings.json',mappings)
    save(out/'completion.json',dict(records=len(traces),db_unchanged=True,actual_query_calls=sum(len(t['queries']) for t in traces),completed_epoch=time.time()))
    for name in ('design','generation','run'):verify(HERE/f'test-output/{name}-freeze.json')
    freeze(HERE/'test-output/acquisition-freeze.json',[p for p in out.iterdir() if p.is_file()])
    print('Acquisition frozen; native selection may now run.')

def score_all():
    for name in ('design','generation','run','acquisition','selection'):verify(HERE/f'test-output/{name}-freeze.json')
    traces=[json.loads(s) for s in (HERE/'test-output/acquisition/traces.jsonl').read_text().splitlines()]
    mappings=read(HERE/'test-output/acquisition/mappings.json');selected={}
    for key,mapping in mappings.items():
        payload=read(HERE/f'test-output/acquisition/{key}.json')
        path=HERE/f'test-output/selections/{key}.json'
        raw=path.read_text() if path.exists() else ''
        for row in account(raw,payload,mapping):selected[row['id'],key.split('-')[0]]=row
    rows=[]
    for trace in traces:
        for arm in ARMS:
            if arm in ('foundation','wide_rank'):ids=trace[arm];error=trace['foundation_error']
            else:
                result=selected[trace['id'],arm.split('_')[0]];ids=result['ids'];error=trace['foundation_error'] or result['error']
            rows.append(dict(id=trace['id'],batch=trace['batch'],arm=arm,ids=ids,error=error))
    save(HERE/'test-output/packets.json',rows)
    freeze(HERE/'test-output/packets-freeze.json',[HERE/'test-output/packets.json'])
    report=assess(rows,read(HERE/'data/cases.json'),traces,read(HERE/'data/semantic-review.json'))
    save(HERE/'test-output/scores.json',report)
    print(json.dumps(dict(summaries={a:report['summaries'][a]['all']['8'] for a in ARMS},gates=report['gates'],qualified=report['qualified']),indent=2))

if __name__=='__main__':
    if sys.argv[1:] == ['acquire']:acquire_all()
    elif sys.argv[1:] == ['score']:score_all()
    else:raise SystemExit('Use acquire or score')

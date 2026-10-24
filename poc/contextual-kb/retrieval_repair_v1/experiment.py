"""First-save prospective plans, blind selector runs and fixed regression accounting."""
import concurrent.futures,hashlib,json,os,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parent
sys.path.insert(0,str(POC))
from mcp_v1.planner import CodexPlanner
from agent_contract.qualification_v3.candidate import build_plan
from agent_contract.retrieval_integration_v1.bridge import readonly,retrieve
from kbcompiler.question_pilot import PilotIndex
from retrieval_repair_v1.policy import acquire,present,apply_repair
from retrieval_repair_v1.selector import Selector
from retrieval_repair_v1.preserve import snapshot

def read(p):return json.loads(p.read_text())
def save(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')
def freeze(p,files):save(p,{str(f.resolve()):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
def verify(p):
    for file,h in read(p).items():assert hashlib.sha256(Path(file).read_bytes()).hexdigest()==h,file

def plans():
    out=HERE/'test-output/fresh';out.mkdir()
    cases=read(HERE/'fresh-cases.json')
    def run(case):
        try:core,receipt=CodexPlanner(out/'planner')(case['request']);error=None
        except Exception as e:core=None;receipt=None;error=type(e).__name__+': '+str(e)
        row=dict(case,core=core,receipt=receipt,error=error);save(out/(case['id']+'.json'),row)
        return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(run,cases))
    # First response saved before frozen validator is consulted.
    for row in rows:
        if row['error'] is None:
            try:build_plan(row['request'],row['core'])
            except Exception as e:row['error']=str(e)
    save(out/'records.json',rows)
    freeze(out/'freeze.json',[p for p in out.rglob('*') if p.is_file()])

def acquire_all():
    out=HERE/'test-output/panel';out.mkdir()
    records=[]
    mcp=read(POC/'mcp_v1/test-output/results/rows.json')
    for r in mcp:
        if r['round']==1 or r['id']=='M03':records.append(dict(id=f"D{r['round']}-{r['id']}",request=r['request'],core=r['plan'],group='diagnostic',original_ids=r['fact_ids'],gold=None))
    historical=POC/'agent_contract/relevance_selection_v1/data'
    gold={r['id']:r for r in read(historical/'cases.json')}
    for r in read(historical/'records.json'):records.append(dict(id=r['id'],request=r['request'],core=r['output'],group='historical',gold=gold[r['id']]))
    for r in read(HERE/'test-output/fresh/records.json'):
        for repeat in range(1,4):records.append(dict(id=f"{r['id']}-{repeat}",request=r['request'],core=r['core'],group='fresh',gold=r,error=r['error']))
    os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(POC/'agent_contract/advisory_lookup_v1/test-output/embed-cache'),HF_HUB_OFFLINE='1')
    with readonly(POC/'build/knowledge.sqlite') as db:
        index=PilotIndex(db)
        for record in records:
            if record.get('error'):continue
            plan=build_plan(record['request'],record['core'])
            baseline=retrieve(index,plan,enhanced=False)
            if 'original_ids' in record:assert baseline['ids']==record['original_ids']
            acquired=acquire(index,record['core'],baseline['ids'])
            payload,mapping=present(record['core'],baseline['ids'],acquired['pool'],index.facts,lambda f:db.execute('select source_quote from facts where id=?',(f,)).fetchone()[0])
            record.update(baseline=baseline,acquired=acquired,payload=payload,mapping=mapping)
    save(out/'inputs.json',records);freeze(out/'inputs-freeze.json',[out/'inputs.json'])

def select_all():
    out=HERE/'test-output/panel';verify(HERE/'test-output/design-freeze.json');verify(out/'inputs-freeze.json')
    results=out/'decisions';results.mkdir()
    def run(record):
        started=time.perf_counter();error=record.get('error');decision=None
        try:
            if error:raise ValueError(error)
            if not record['core']['formly_questions']:decision={'replacements':[]}
            else:decision=Selector(out/'selector')(record['payload'])
            ids=apply_repair(decision,record['payload'],record['mapping'])
        except Exception as e:error=type(e).__name__+': '+str(e);ids=record.get('baseline',{}).get('ids',[])
        result=dict(id=record['id'],ids=ids,decision=decision,error=error,seconds=time.perf_counter()-started)
        save(results/(record['id']+'.json'),result);print(record['id'],'ERROR' if error else 'ok',flush=True)
        return result
    records=read(out/'inputs.json')
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(run,records))
    save(out/'all-decisions.json',rows)

def score():
    out=HERE/'test-output/panel';verify(HERE/'test-output/design-freeze.json');verify(out/'inputs-freeze.json')
    records=read(out/'inputs.json');decisions={r['id']:r for r in read(out/'all-decisions.json')};rows=[]
    callbacks={'expression-callbacks-and-hooks/'+s for s in ['modern-callback-field-argument','legacy-callback-arguments','conditional-disabled-target']}
    for r in records:
        d=decisions[r['id']];base=set(r.get('baseline',{}).get('ids',[]));ids=set(d['ids']);gold=r['gold']
        row=dict(id=r['id'],group=r['group'],error=d['error'],removed=sorted(base-ids),added=sorted(ids-base),callback_present=bool(ids&callbacks),baseline_callback_present=bool(base&callbacks))
        if gold is not None:
            relevant=set(gold['relevant_fact_ids']);groups=gold['required_groups']
            row.update(relevant_lost=sorted((base&relevant)-ids),relevant_gained=sorted((ids&relevant)-base),baseline_groups=sum(bool(base&set(g)) for g in groups),candidate_groups=sum(bool(ids&set(g)) for g in groups),group_count=len(groups),unsupported_replacements=bool(not relevant and base!=ids))
        rows.append(row)
    diag=[r for r in rows if r['id'].endswith('M03')];freshcallback=[r for r in rows if r['id'].split('-')[0] in {'F01','F02','F03'}]
    passed=all(not r['error'] for r in rows) and all(r['callback_present'] for r in diag+freshcallback) and all(not r.get('relevant_lost') and r.get('candidate_groups',0)>=r.get('baseline_groups',0) and not r.get('unsupported_replacements') for r in rows)
    summary=dict(slots=len(rows),errors=sum(bool(r['error']) for r in rows),changed=sum(bool(r['added']) for r in rows),relevant_losses=sum(len(r.get('relevant_lost',[])) for r in rows),relevant_gains=sum(len(r.get('relevant_gained',[])) for r in rows),diagnostic_callback=sum(r['callback_present'] for r in diag),fresh_callback=sum(r['callback_present'] for r in freshcallback),passed=passed)
    save(out/'scores.json',rows);save(out/'summary.json',summary)
    assert snapshot()==read(HERE/'test-output/protected-before.json')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':globals()[sys.argv[1]]()

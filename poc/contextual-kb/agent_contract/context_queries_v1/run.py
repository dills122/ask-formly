"""Exclusive first-run read-only retrieval and frozen-metric scoring."""
import hashlib,json,os,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parents[1]
sys.path.insert(0,str(POC))
from agent_contract.retrieval_integration_v1.bridge import readonly,relevance
from agent_contract.qualification_v3.candidate import build_plan
from kbcompiler.question_pilot import PilotIndex
from candidate import retrieve
from assessment import assess

def read(path):return json.loads(Path(path).read_text())
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(path,value):
    with Path(path).open('x') as f:json.dump(value,f,indent=2,allow_nan=False)
def verify(path):
    for filename,digest in read(path).items():
        if sha(filename)!=digest:raise ValueError('frozen input changed: '+filename)
def main():
    for name in ('design','generation','run'):verify(HERE/f'test-output/{name}-freeze.json')
    if read(HERE/'PREFLIGHT-DECISION.json')['verdict']!='ready':raise ValueError('preflight not ready')
    records=read(HERE/'data/records.json');cases=read(HERE/'data/cases.json');semantic=read(HERE/'data/semantic-review.json')
    expected=[r['id'] for r in read(HERE/'data/requests.json')]
    if len(expected)!=36 or len(set(expected))!=36 or [r['id'] for r in records]!=expected or [r['id'] for r in cases]!=expected:raise ValueError('input/gold coverage')
    byid={r['id']:r for r in cases}
    out=HERE/'test-output/retrieval';out.mkdir(exist_ok=False)
    save(out/'first-save.json',dict(run_freeze=sha(HERE/'test-output/run-freeze.json'),records=len(records)))
    os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(HERE/'test-output/embed-cache'),HF_HUB_OFFLINE='1')
    dbpath=POC/'build/knowledge.sqlite';dbhash=sha(dbpath)
    with readonly(dbpath) as db:
        started=time.perf_counter();index=PilotIndex(db)
        save(out/'setup.json',dict(seconds=time.perf_counter()-started,facts=len(index.ids),db_hash=dbhash))
        for case in cases:
            if not set(case['relevant_fact_ids'])<=set(index.ids) or any(not group or not set(group)<=set(case['relevant_fact_ids']) for group in case['required_groups']):raise ValueError('invalid relevance IDs/groups')
            if bool(case['relevant_fact_ids'])!=bool(case['required_groups']):raise ValueError('support/groups mismatch')
        with (out/'results.jsonl').open('x') as f:
            for number,record in enumerate(records):
                core=record['output'];error=record['foundation_error']
                if not error:
                    try:build_plan(record['request'],core)
                    except (ValueError,TypeError,KeyError) as exc:error=str(exc)
                for arm in (('foundation','context') if number%2==0 else ('context','foundation')):
                    if error:result=dict(ids=[],questions=[],queries=[],query_count=0,query_characters=0,seconds=0,supplement_error=None)
                    else:result=retrieve(index,core,record['supplements'] if arm=='context' else None)
                    if arm=='context' and record['supplement_delivery_error']:result['supplement_error']=record['supplement_delivery_error']
                    result.update(id=record['id'],batch=record['batch'],arm=arm,foundation_error=error,metrics={str(k):relevance(result['ids'],byid[record['id']],k) for k in (4,8)})
                    f.write(json.dumps(result,allow_nan=False)+'\n');f.flush()
        if sha(dbpath)!=dbhash:raise ValueError('DB changed')
    for name in ('design','generation','run'):verify(HERE/f'test-output/{name}-freeze.json')
    save(out/'completion.json',dict(complete=True,records=36,arms=['foundation','context'],db_unchanged=True))
    save(HERE/'test-output/retrieval-freeze.json',{str(p):sha(p) for p in out.iterdir() if p.is_file()})
    verify(HERE/'test-output/retrieval-freeze.json')
    rows=[json.loads(s) for s in (out/'results.jsonl').read_text().splitlines()]
    report=assess(rows,records,semantic);save(HERE/'test-output/scores.json',report)
    print(json.dumps(dict(summaries={a:s['all']['8'] for a,s in report['summaries'].items()},utility_pass=report['utility_pass'],consistent_floor=report['consistent_floor']),indent=2))
if __name__=='__main__':main()

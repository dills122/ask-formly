"""Post-promotion stable-launcher replay and bounded hosted-inference smoke."""
import argparse
import asyncio
from datetime import timedelta
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
POC=HERE.parents[1]
QUAL=HERE.parent/'api-contracts-v1'
DATABASE_SHA256='f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09'
MANIFESTS={'mcp_foundation/foundation.json':'formly-poc-foundation-15',
           'mcp_runtime/model-free.json':'formly-model-free-discovery-7'}
BACKED_IDS=('API-02','API-09','CONFIG-04','CONFIG-11','CONTROL-01')
STAGES=('API','API-fetch','CONFIG','CONFIG-fetch','CONTROL','REGRESSION','REGRESSION-fetch')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def installed_preflight(root=POC,expected=DATABASE_SHA256):
    actual=digest(root/'build/knowledge.sqlite')
    if actual!=expected:raise ValueError('Installed database is not the reviewed 192-fact candidate')
    manifests={}
    for name,ident in MANIFESTS.items():
        path=root/name;m=json.loads(path.read_text());k=m.get('knowledge',{})
        if (m.get('id')!=ident or m.get('files',{}).get('build/knowledge.sqlite')!=expected
            or k.get('facts')!=192 or k.get('documents')!=36 or k.get('promotion')!='knowledge-expansion/promotion-v13'):
            raise ValueError(f'Promotion manifest mismatch: {name}')
        manifests[name]=digest(path)
    return dict(database_sha256=actual,manifest_sha256=manifests)


def candidate_rows(root=QUAL):
    # Audit order is package-sorted, then initial/fetch/discovery/discovery2/fetch2.
    # This reviewed candidate has only these four fetch calls, with no discoveries.
    seal=json.loads((root/'assessment-freeze.json').read_text())['files']
    rows=[]
    for stage in STAGES:
        relative=f'test-output/qualification/candidate/r1/{stage}.json'
        path=root/relative
        if digest(path)!=seal.get(relative):raise ValueError(f'Changed candidate packet: {relative}')
        batch=json.loads(path.read_text())
        if any(r.get('operational_or_tool_error') or r['result'].get('isError') for r in batch):
            raise ValueError('Candidate packet contains tool failure')
        rows.extend(batch)
    if len(rows)!=44 or len({r['id'] for r in rows})!=40 or sum(r['tool']=='lookup_formly' for r in rows)!=40:
        raise ValueError('Candidate cohort must contain 40 requests and 44 calls')
    return rows


def model_backed_calls(rows):
    by_id={r['id']:r for r in rows if r['tool']=='lookup_formly'}
    if not set(BACKED_IDS)<=set(by_id):raise ValueError('Missing bounded smoke request')
    return [dict(id=i,tool='lookup_formly',arguments={k:v for k,v in by_id[i]['arguments'].items() if k!='plan'}) for i in BACKED_IDS]


def launcher_args(mode,seed,out):
    args=['-B']
    if mode=='model-free':args.append(str(POC/'model_free_v1/offline_guard.py'))
    args += [str(POC/'mcp_runtime/launcher.py'),'serve','--mode',mode,'--runtime-dir',str(out/'runtime')]
    if mode=='model-backed':args+=['--seed',str(seed)]
    return args


def check_results(records,expected):
    if len(records)!=len(expected) or [r.get('result') for r in records]!=[r['result'] for r in expected]:
        raise ValueError('Installed free replies differ from qualified candidate')


async def run(mode,seed,name):
    if mode not in ('model-free','model-backed') or seed not in (1701,1702):raise ValueError('Invalid smoke mode/seed')
    if Path(name).name!=name or name in ('','.','..'):raise ValueError('Invalid output name')
    pins=installed_preflight()
    expected=candidate_rows()
    calls=([{k:r[k] for k in ('id','tool','arguments')} for r in expected]
           if mode=='model-free' else model_backed_calls(expected))
    out=HERE/'test-output'/name;out.mkdir(parents=True,exist_ok=False)
    def save(name,value):
        (out/name).write_text(json.dumps(value,indent=2)+'\n')
    command=launcher_args(mode,seed,out);records=[];failure=None;equivalent=False
    save('input.json',calls)
    save('settings.json',dict(mode=mode,seed=seed,command=[sys.executable,*command],installed=pins,
        candidate_packets={s:digest(QUAL/f'test-output/qualification/candidate/r1/{s}.json') for s in STAGES},
        scope='44-call exact packet replay' if mode=='model-free' else 'five-request bounded smoke; requires evidence assessment'))
    try:
        from mcp import ClientSession,StdioServerParameters
        from mcp.client.stdio import stdio_client
        with (out/'stderr.txt').open('x') as log:
            async with stdio_client(StdioServerParameters(command=sys.executable,args=command),errlog=log) as (read,write):
                async with ClientSession(read,write) as session:
                    await session.initialize()
                    save('tools.json',[t.name for t in (await session.list_tools()).tools])
                    for call in calls:
                        row=dict(call)
                        try:
                            result=await session.call_tool(call['tool'],call['arguments'],read_timeout_seconds=timedelta(seconds=600 if mode=='model-backed' else 60))
                            row.update(result=result.model_dump(mode='json'),failed=bool(result.isError))
                        except Exception as exc:
                            row.update(error=dict(type=type(exc).__name__,message=str(exc)),failed=True)
                        records.append(row);save('calls.json',records)
                        print(mode,seed,call['id'],'error' if row['failed'] else 'delivered',flush=True)
        if len(records)!=len(calls) or any(r['failed'] for r in records):raise RuntimeError('Smoke delivery failed; inspect retained calls')
        if installed_preflight()!=pins:raise ValueError('Installed pins changed during smoke')
        if mode=='model-free':
            if 'OFFLINE_GUARDS_ACTIVE' not in (out/'stderr.txt').read_text():raise ValueError('Offline guard absent')
            check_results(records,expected);equivalent=True
            save('equivalence.json',dict(exact_result_equality=True,calls=len(records),requests=40))
    except BaseException as exc:
        failure=dict(type=type(exc).__name__,message=str(exc));raise
    finally:
        save('calls.json',records)
        save('receipt.json',dict(mode=mode,seed=seed,expected=len(calls),attempted=len(records),
            errors=sum(r['failed'] for r in records),unattempted=[c['id'] for c in calls[len(records):]],
            failure=failure,exact_result_equality=equivalent if mode=='model-free' else None))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=('model-free','model-backed'),required=True)
    parser.add_argument('--seed',type=int,choices=(1701,1702),default=1701)
    parser.add_argument('--name',required=True)
    args=parser.parse_args();asyncio.run(run(args.mode,args.seed,args.name))

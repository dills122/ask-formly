"""Installed stable-launcher tests; model-backed explicitly permits hosted inference."""
import argparse
import asyncio
from datetime import timedelta
import json
from pathlib import Path
import sys
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client

HERE=Path(__file__).resolve().parent;POC=HERE.parents[1]
QUAL=HERE.parent/'material-radio-native-v1'

async def run(mode,seed,name):
    if Path(name).name!=name or name in ('','.','..'):raise ValueError('Invalid output name')
    out=HERE/'test-output'/name;out.mkdir(exist_ok=False);calls=[];records=[]
    if mode=='model-free':
        for stage in ('batch-1','batch-2','batch-3','fetch'):
            rows=json.loads((QUAL/f'test-output/qualification/candidate/r1/{stage}.json').read_text())
            calls.extend({k:r[k] for k in ('id','tool','arguments')} for r in rows)
    else:
        for row in json.loads((QUAL/'lookup-calls.json').read_text()):
            if row['id'] in ('Q02','Q05','Q06','Q08','C04'):
                calls.append(dict(id=row['id'],tool='lookup_formly',arguments={k:v for k,v in row['arguments'].items() if k!='plan'}))
    (out/'input.json').write_text(json.dumps(calls,indent=2))
    command=['-B']
    if mode=='model-free':command.append(str(POC/'model_free_v1/offline_guard.py'))
    command += [str(POC/'mcp_runtime/launcher.py'),'serve','--mode',mode,'--runtime-dir',str(out/'runtime')]
    if mode=='model-backed':command+=['--seed',str(seed)]
    try:
        with (out/'stderr.txt').open('x') as log:
            async with stdio_client(StdioServerParameters(command=sys.executable,args=command),errlog=log) as (read,write):
                async with ClientSession(read,write) as session:
                    await session.initialize()
                    (out/'tools.json').write_text(json.dumps([t.name for t in (await session.list_tools()).tools]))
                    for call in calls:
                        row=dict(call)
                        try:
                            r=await session.call_tool(call['tool'],call['arguments'],read_timeout_seconds=timedelta(seconds=600 if mode=='model-backed' else 60))
                            row.update(result=r.model_dump(mode='json'),failed=bool(r.isError))
                        except Exception as exc:row.update(error=dict(type=type(exc).__name__,message=str(exc)),failed=True)
                        records.append(row);(out/'calls.json').write_text(json.dumps(records,indent=2));print(mode,seed,call['id'],'error' if row['failed'] else 'delivered',flush=True)
    finally:
        (out/'receipt.json').write_text(json.dumps(dict(mode=mode,seed=seed,expected=len(calls),attempted=len(records),errors=sum(r['failed'] for r in records),unattempted=[c['id'] for c in calls[len(records):]]),indent=2))
    if any(r['failed'] for r in records):raise RuntimeError('Smoke delivery failed; inspect retained calls')
    if mode=='model-free':
        expected=[]
        for stage in ('batch-1','batch-2','batch-3','fetch'):
            expected.extend(json.loads((QUAL/f'test-output/qualification/candidate/r1/{stage}.json').read_text()))
        if [r['result'] for r in records]!=[r['result'] for r in expected]:raise ValueError('Installed free replies differ from qualified candidate')
        (out/'equivalence.json').write_text(json.dumps(dict(exact_result_equality=True,calls=len(records))))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mode',choices=('model-free','model-backed'),required=True);p.add_argument('--seed',type=int,choices=(1701,1702),default=1701);p.add_argument('--name',required=True);a=p.parse_args();asyncio.run(run(a.mode,a.seed,a.name))

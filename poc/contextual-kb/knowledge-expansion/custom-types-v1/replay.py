"""Replay actual normalized MCP plans against the other isolated DB arm."""
import argparse,asyncio,json,sys
from datetime import timedelta
from pathlib import Path
from experiment import HERE, preserved
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def collect(root, cases, arm, repeat):
    records={}; source={}; missing=[]
    for case in cases:
        matches=[]
        for file in root.glob(f'r{repeat}-b*-{arm}/mcp/audit/*.json'):
            row=json.loads(file.read_text())
            if row['request']==case['request']:matches.append(row)
        if len(matches)!=1 or 'result' not in matches[0]:
            missing.append(case['id']);continue
        result=matches[0]['result'];source[case['id']]=matches[0]
        records[case['request']]=dict(core=result['plan']['question_plan'],generation=result['generation'])
    return records,source,missing


async def replay(root, cases, repeat):
    source_arm='baseline' if repeat%2 else 'candidate'
    target_arm='candidate' if source_arm=='baseline' else 'baseline'
    records,source,missing=collect(root,cases,source_arm,repeat)
    out=root/f'paired-r{repeat}';out.mkdir(exist_ok=False)
    (out/'plans.json').write_text(json.dumps(records,indent=2))
    (out/'source.json').write_text(json.dumps(source,indent=2))
    report=dict(source_arm=source_arm,target_arm=target_arm,round=repeat,missing_source_cases=missing,results=[])
    (out/'results.json').write_text(json.dumps(report,indent=2))
    if not records:return report
    with (out/'stderr.txt').open('w') as err:
        async with stdio_client(StdioServerParameters(command=sys.executable,args=['-B',str(HERE/'experiment.py'),'serve','--arm',target_arm,'--seed',str(1702 if repeat==2 else 1701),'--runtime',str(out/'mcp'),'--replay',str(out/'plans.json')]),errlog=err) as (r,w):
            async with ClientSession(r,w) as session:
                await session.initialize()
                for case in cases:
                    if case['id'] in missing:continue
                    result=await session.call_tool('lookup_formly',{'request':case['request']},read_timeout_seconds=timedelta(seconds=600))
                    row=dict(id=case['id'],is_error=result.isError,packet=result.structuredContent)
                    if not result.isError:
                        expected=source[case['id']]['result']['plan']['question_plan']
                        if row['packet']['plan']['question_plan']!=expected:raise ValueError('Replay plan drift')
                    report['results'].append(row)
                    (out/'results.json').write_text(json.dumps(report,indent=2))
                    print('paired',repeat,case['id'],'error',result.isError,flush=True)
    preserved()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',required=True);parser.add_argument('--cases',required=True);parser.add_argument('--repeats',type=int,default=1);args=parser.parse_args()
    root=Path(args.root).resolve()
    if not root.is_relative_to(HERE/'test-output'):raise ValueError('Replay outputs outside experiment')
    cases=json.loads(Path(args.cases).read_text())['cases']
    for repeat in range(1,args.repeats+1):asyncio.run(replay(root,cases,repeat))

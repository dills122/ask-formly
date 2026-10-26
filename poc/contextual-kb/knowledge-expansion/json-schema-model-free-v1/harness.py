"""Experiment-only stdio transport; callers supply every plan and tool decision."""
import argparse
import asyncio
from datetime import timedelta
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
POC=HERE.parents[1]


def database(arm):
    if arm not in ('baseline','candidate'):raise ValueError('Unknown arm')
    config=json.loads((HERE/'databases.json').read_text())[arm]
    path=(POC/config['path']).resolve()
    if not path.is_relative_to(POC):raise ValueError('DB outside POC')
    return path,config['sha256']


def validate_call(row):
    if (not isinstance(row,dict) or not isinstance(row.get('id'),str) or not row['id']
        or row.get('tool') not in {'lookup_formly','discover_formly_candidates','get_formly_facts'}
        or not isinstance(row.get('arguments'),dict)):
        raise ValueError('Expected case id, allowed MCP tool and arguments')
    return row


def reserve(path):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as f:f.write('[]')


def receipt(calls,rows):
    return dict(expected=len(calls),attempted=len(rows),
                errors=sum(bool(r.get('operational_or_tool_error')) for r in rows),
                unattempted=[c['id'] for c in calls[len(rows):]])


async def run(arm,input_path,output_path):
    from mcp import ClientSession,StdioServerParameters
    from mcp.client.stdio import stdio_client
    database(arm)
    calls=[validate_call(c) for c in json.loads(input_path.read_text())]
    reserve(output_path);rows=[]
    command=['-B',str(POC/'model_free_v1/offline_guard.py'),str(HERE/'server.py'),arm,'--settings',str(output_path.with_suffix('.settings.sqlite'))]
    try:
        with output_path.with_suffix('.stderr').open('x') as stderr:
            async with stdio_client(StdioServerParameters(command=sys.executable,args=command),errlog=stderr) as (read,write):
                async with ClientSession(read,write) as session:
                    init=await session.initialize()
                    output_path.with_suffix('.init.json').write_text(init.model_dump_json(indent=2))
                    for call in calls:
                        row=dict(call);started=time.perf_counter()
                        try:
                            result=await session.call_tool(call['tool'],call['arguments'],read_timeout_seconds=timedelta(seconds=60))
                            row.update(result=result.model_dump(mode='json'),operational_or_tool_error=bool(result.isError))
                        except Exception as exc:
                            row.update(error=dict(type=type(exc).__name__,message=str(exc)),operational_or_tool_error=True)
                        row['seconds']=time.perf_counter()-started;rows.append(row)
                        output_path.write_text(json.dumps(rows,indent=2))
    finally:
        output_path.with_suffix('.receipt.json').write_text(json.dumps(receipt(calls,rows),indent=2))
    print(json.dumps(receipt(calls,rows)))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('arm',choices=('baseline','candidate'));p.add_argument('input',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();asyncio.run(run(a.arm,a.input,a.output))

"""Explicit local transport smoke; --mode model-backed permits its hosted inference."""
import argparse
import asyncio
from datetime import timedelta
import json
from pathlib import Path
import sys
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client

HERE=Path(__file__).resolve().parent
POC=HERE.parent


async def run(mode):
    from datetime import datetime
    out=HERE/'test-output'/('smoke-'+mode+'-'+datetime.now().strftime('%Y%m%dT%H%M%S'))
    out.mkdir(parents=True,exist_ok=False)
    command=['-B']
    if mode=='model-free':command.append(str(POC/'model_free_v1/offline_guard.py'))
    command += [str(HERE/'launcher.py'),'serve','--mode',mode,'--runtime-dir',str(out/'runtime')]
    request='In Formly 6.3.12 Material, can I extend input with type defaults instead of rewriting its renderer, and how do defaults combine with an already supplied field prop?'
    args=dict(request=request,formly_version='6.3.12',ui_adapter='material')
    if mode=='model-free':
        args['plan']=dict(formly_questions=[dict(question=request,reason='Resolve inheritance and default merging without inventing rendering code.')],
            library_constraints=dict(formly_version='6.3.12',ui_adapter='material'),condition_bindings=[dict(condition='In Formly 6.3.12 Material',question_indexes=[0])])
    records=[]
    with (out/'stderr.txt').open('w') as log:
        async with stdio_client(StdioServerParameters(command=sys.executable,args=command),errlog=log) as (read,write):
            async with ClientSession(read,write) as session:
                await session.initialize()
                names={t.name for t in (await session.list_tools()).tools}
                (out/'tools.json').write_text(json.dumps(sorted(names)))
                assert names==({'lookup_formly','get_formly_facts','discover_formly_candidates'} if mode=='model-free' else {'lookup_formly','get_formly_project_settings','set_formly_project_settings'})
                async def call(name,arguments):
                    result=await session.call_tool(name,arguments,read_timeout_seconds=timedelta(seconds=600))
                    records.append(dict(tool=name,arguments=arguments,result=result.model_dump(mode='json')))
                    (out/'calls.json').write_text(json.dumps(records,indent=2))
                    assert not result.isError,result
                    return result.structuredContent
                packet=await call('lookup_formly',args)
                assert packet['facts'] and packet['citations']
                if mode=='model-free':
                    page=await call('discover_formly_candidates',dict(args,offset=0,limit=16))
                    assert page['candidates']
                    ids=[page['candidates'][0]['id']]
                    full=await call('get_formly_facts',dict(fact_ids=ids,formly_version='6.3.12',ui_adapter='material'))
                    assert [f['id'] for f in full['facts']]==ids and set(ids)<=full['citations'].keys()
                    assert packet['status']=='ok'
                else:
                    assert 'advisory' in packet and 'selection' in packet
    (out/'receipt.json').write_text(json.dumps(dict(mode=mode,tools=sorted(names),calls=len(records),status='passed'),indent=2))
    print(mode,'transport smoke passed')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--mode',choices=('model-free','model-backed'),required=True)
    asyncio.run(run(parser.parse_args().mode))

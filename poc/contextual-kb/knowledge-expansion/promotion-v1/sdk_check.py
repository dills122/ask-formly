"""Replay the actual failed raw planner output over MCP with both frozen seeds."""
import asyncio
import json
import sys
from datetime import timedelta
from pathlib import Path
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parent/'custom-types-v1'


async def check():
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    root=HERE/'test-output/saved-failure-replay';root.mkdir(exist_ok=False)
    planners=PRIOR/'test-output/qualification-1/r2-b4-candidate/mcp/planner'
    matches=[]
    for job in planners.iterdir():
        request=json.loads((job/'request.json').read_text())
        if not request.startswith('An internal Formly source file exports TypeOption.'):
            continue
        messages=[json.loads(line)['item']['text'] for line in (job/'events.jsonl').read_text().splitlines()
                  if json.loads(line).get('type')=='item.completed' and json.loads(line).get('item',{}).get('type')=='agent_message']
        assert len(messages)==1
        matches.append((request,json.loads(messages[0])))
    assert len(matches)==1
    request,core=matches[0]
    plans=root/'plans.json';plans.write_text(json.dumps({request:dict(core=core,generation=dict(replay=True,source='saved actual failed Q20'))},indent=2))
    for seed in (1701,1702):
        job=root/str(seed);job.mkdir()
        with (job/'client-stderr.txt').open('w') as errors:
            args=['-B',str(HERE/'replay_server.py'),'--seed',str(seed),'--runtime',str(job/'mcp'),'--replay',str(plans)]
            async with stdio_client(StdioServerParameters(command=sys.executable,args=args),errlog=errors) as (r,w):
                async with ClientSession(r,w) as session:
                    await session.initialize()
                    tools=await session.list_tools()
                    assert [t.name for t in tools.tools]==['lookup_formly']
                    result=await session.call_tool('lookup_formly',{'request':request},read_timeout_seconds=timedelta(seconds=600))
                    (job/'result.json').write_text(result.model_dump_json(indent=2))
                    assert not result.isError
                    packet=result.structuredContent
                    assert packet['generation']['wording_normalization']['original_plan']==core
                    assert packet['generation']['wording_normalization']['rewrites'][0]['rule']=='source-initial-article-case'
                    assert 'custom-type-recipe-core/public-registration-type' in packet['retrieval']['ids']
                    assert packet['runtime']['db_unchanged']
                    assert all(c['parameters_unchanged'] for c in packet['runtime']['model_checks'])
                    print('saved failure repaired over real MCP, seed',seed,flush=True)


if __name__=='__main__':asyncio.run(check())

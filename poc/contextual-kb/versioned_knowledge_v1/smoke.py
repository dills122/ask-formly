"""Real hosted planning/selector + native extractor over candidate stdio MCP."""
import asyncio
from datetime import timedelta
import json
import os
from pathlib import Path
import sys
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
HERE=Path(__file__).resolve().parent

async def run():
    reports=[]
    for seed in (1701,1702):
        out=HERE/'test-output'/f'smoke-{seed}';out.mkdir(exist_ok=True)
        env=dict(os.environ,FORMLY_SETTINGS_PATH=str(out/'settings.sqlite'))
        params=StdioServerParameters(command=sys.executable,args=['-B',str(HERE/'server.py'),'--database',str(HERE/'test-output/candidate.sqlite'),'--runtime',str(out/'runtime'),'--seed',str(seed)],env=env)
        with (out/'stderr.log').open('w') as log:
            async with stdio_client(params,errlog=log) as (r,w):
                async with ClientSession(r,w) as session:
                    await session.initialize()
                    cases=[
                        {'request':'In Formly, how do I register a custom field type and use it in a field configuration?'},
                        {'request':'In Formly, how do defaultValue and resetModel differ?','project_id':'candidate-smoke','formly_version':'6.3.12','ui_adapter':'core'},
                        {'request':'In Formly, does hiding a field clear its model value, and how do I retain it?','project_id':'candidate-smoke'},
                        {'request':'How do I register a Formly field type?','formly_version':'7'},
                    ]
                    for i,args in enumerate(cases):
                        raw=await session.call_tool('lookup_formly',args,read_timeout_seconds=timedelta(seconds=240))
                        (out/f'call-{i}.json').write_text(raw.model_dump_json(indent=2))
                        assert not raw.isError,raw
                        data=raw.structuredContent
                        if i==3:
                            assert data['status']=='unsupported_version' and 'facts' not in data
                            reports.append(dict(seed=seed,case=i,unsupported=True));continue
                        assert data['facts'] and data['runtime']['db_unchanged']
                        assert data['runtime']['model_checks'] and all(c['parameters_unchanged'] for c in data['runtime']['model_checks'])
                        assert data['advisory']['status']=='available',data['advisory']
                        assert data['selection']['status'] in ('unchanged','repaired'),data['selection']
                        if i in (1,2):assert all(f['adapter']=='core' for f in data['facts'])
                        for fid,c in data['citations'].items():
                            assert c['applicability'] and all(a['scope']=={'kind':'exact','value':'6.3.12'} for a in c['applicability'])
                        reports.append(dict(seed=seed,case=i,facts=len(data['facts']),advisory=data['advisory']['status'],selection=data['selection']['status'],model_checks=data['runtime']['model_checks']))
                        print(f'seed {seed} case {i}: passed',flush=True)
    (HERE/'test-output/smoke-summary.json').write_text(json.dumps(reports,indent=2)+'\n')

if __name__=='__main__':asyncio.run(run())

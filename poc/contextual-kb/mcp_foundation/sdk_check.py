"""Real local transport checks, no hosted generations or model changes."""
import asyncio,json,os,subprocess,sys
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
HERE=Path(__file__).resolve().parent
async def main():
    root=HERE/'test-output/sdk';root.mkdir()
    rows=[]
    for restart in (1,2):
        job=root/str(restart);job.mkdir()
        with (job/'stderr.txt').open('x') as err:
            async with stdio_client(StdioServerParameters(command=sys.executable,args=['-B',str(HERE/'launcher.py'),'serve','--runtime-dir',str(job/'runtime'),'--audit-dir',str(job/'audit')]),errlog=err) as (r,w):
                async with ClientSession(r,w) as session:
                    init=await session.initialize();tools=await session.list_tools()
                    assert [t.name for t in tools.tools]==['lookup_formly']
                    invalid=await session.call_tool('lookup_formly',{'request':''})
                    assert invalid.isError
                    await session.send_ping()
                    for name,result in [('initialize',init),('tools',tools),('invalid',invalid)]:
                        (job/f'{name}.json').write_text(result.model_dump_json(indent=2))
                    rows.append(dict(restart=restart,initialized=True,invalid_error=True,ping_after_error=True))
    # Controlled missing-CLI startup, with executable and all assets unchanged.
    env=dict(os.environ,PATH='')
    result=subprocess.run([sys.executable,'-B',str(HERE/'launcher.py'),'serve'],env=env,capture_output=True,text=True,timeout=30)
    assert result.returncode==2 and result.stdout=='' and 'codex CLI not found' in result.stderr
    (root/'missing-cli.json').write_text(json.dumps(dict(exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr),indent=2))
    (root/'summary.json').write_text(json.dumps(rows,indent=2))
    print(json.dumps(rows))
if __name__=='__main__':asyncio.run(main())

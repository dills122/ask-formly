"""Actual SDK transport smoke, separate from fixed agent qualification."""
import asyncio,json,sys
from datetime import timedelta
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
HERE=Path(__file__).resolve().parent
async def main():
    out=HERE/'test-output/sdk-smoke';out.mkdir()
    with (out/'stderr.txt').open('w') as err:
        async with stdio_client(StdioServerParameters(command=sys.executable,args=['-B',str(HERE/'server.py'),'--audit-dir',str(out/'audit'),'--planner-runs',str(out/'planner')]),errlog=err) as (r,w):
            async with ClientSession(r,w) as session:
                init=await session.initialize(); listing=await session.list_tools()
                (out/'initialize.json').write_text(init.model_dump_json(indent=2))
                (out/'tools.json').write_text(listing.model_dump_json(indent=2))
                result=await session.call_tool('lookup_formly',{'request':'In Formly, what does resetOnHide: false do when a field is hidden?'},read_timeout_seconds=timedelta(seconds=240))
                (out/'result.json').write_text(result.model_dump_json(indent=2))
                print('isError:',result.isError,'structured:',bool(result.structuredContent))
                if result.isError:raise RuntimeError(str(result.content))
asyncio.run(main())

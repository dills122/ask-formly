"""Single live MCP call for blind callers; never loads cases, policy or rubric."""
import argparse
import asyncio
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import sys


async def main(args):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    command=[str(Path(__file__).with_name('server.py')),'--poc',str(args.poc.resolve()),
             '--database',str(args.database.resolve()),'--sha256',args.sha256,
             '--settings',str(args.transcript.with_suffix('.settings.sqlite').resolve())]
    args.transcript.parent.mkdir(parents=True,exist_ok=True)
    async with stdio_client(StdioServerParameters(command=sys.executable,args=command)) as (read,write):
        async with ClientSession(read,write) as session:
            initialized=await session.initialize()
            if args.tool=='list_tools':
                row=dict(tool='list_tools',instructions=initialized.instructions,
                         tools=[tool.model_dump(mode='json') for tool in (await session.list_tools()).tools])
            else:
                if args.arguments is None:raise ValueError('--arguments required for a tool call')
                arguments=json.loads(args.arguments.read_text())
                result=await session.call_tool(args.tool,arguments,read_timeout_seconds=timedelta(seconds=60))
                raw=result.model_dump(mode='json')
                packet=result.structuredContent
                if packet is None:
                    try:packet=json.loads(result.content[0].text)
                    except (ValueError,IndexError,AttributeError):packet={'status':'tool_error','text':str(result.content)}
                row=dict(tool=args.tool,arguments=arguments,result=raw,packet=packet,
                         sdk_bytes=len(json.dumps(raw,ensure_ascii=False).encode()),is_error=bool(result.isError))
    row.update(timestamp=datetime.now(timezone.utc).isoformat(),poc=str(args.poc.resolve()))
    with args.transcript.open('a') as stream:stream.write(json.dumps(row,ensure_ascii=False)+'\n')
    print(json.dumps(row,ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--poc',type=Path,required=True)
    parser.add_argument('--database',type=Path,required=True)
    parser.add_argument('--sha256',required=True)
    parser.add_argument('--transcript',type=Path,required=True)
    parser.add_argument('--tool',required=True)
    parser.add_argument('--arguments',type=Path)
    asyncio.run(main(parser.parse_args()))

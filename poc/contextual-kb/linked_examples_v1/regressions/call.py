"""One real MCP operation for a blind caller; writes an append-only transcript.

Use --tool list_tools for tool schemas and server instructions. Otherwise supply
--arguments with a JSON object file. No cases, expected IDs, or rubric are loaded.
"""
import argparse
import asyncio
import json
from pathlib import Path
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent


async def main(args):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from run import call
    if args.tool != 'list_tools' and not args.arguments:
        raise ValueError('--arguments JSON file is required for tool calls')
    arguments = json.loads(args.arguments.read_text()) if args.arguments else {}
    script = HERE / 'baseline.py' if args.mode == 'baseline' else HERE.parent / 'serve.py'
    args.transcript.parent.mkdir(parents=True, exist_ok=True)
    command = [str(script), '--database', str(args.database.resolve()), '--sha256', args.sha256,
               '--settings', str(args.transcript.with_suffix('.settings.sqlite').resolve())]
    async with stdio_client(StdioServerParameters(command=sys.executable, args=command)) as (read, write):
        async with ClientSession(read, write) as session:
            initialized = await session.initialize()
            if args.tool == 'list_tools':
                packet = dict(instructions=initialized.instructions,
                              tools=[t.model_dump(mode='json') for t in (await session.list_tools()).tools])
                row = dict(tool='list_tools', arguments={}, packet=packet)
            else:
                rows = []
                packet = await call(session, rows, args.tool, arguments)
                row = rows[0]
            row.update(timestamp=datetime.now(timezone.utc).isoformat(), mode=args.mode)
            with args.transcript.open('a') as f:
                f.write(json.dumps(row, ensure_ascii=False) + '\n')
            print(json.dumps(packet, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('baseline', 'candidate'), default='candidate')
    parser.add_argument('--database', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--transcript', type=Path, required=True)
    parser.add_argument('--tool', required=True)
    parser.add_argument('--arguments', type=Path)
    asyncio.run(main(parser.parse_args()))

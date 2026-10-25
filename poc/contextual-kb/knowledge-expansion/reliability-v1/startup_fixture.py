"""Disposable MCP availability fixture; never returns Formly knowledge."""
import argparse
import json
import time
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--delay', type=float, default=0)
parser.add_argument('--fail', action='store_true')
parser.add_argument('--log', required=True)
args = parser.parse_args()


def log(event):
    with Path(args.log).open('a') as handle:
        handle.write(json.dumps({'event':event,'time':time.time()})+'\n')


log('process_started')
time.sleep(args.delay)
if args.fail:
    log('injected_startup_failure')
    raise SystemExit(17)

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from mcp import types
server = FastMCP('formly-startup-fixture')


@server.tool(annotations=ToolAnnotations(readOnlyHint=True))
def lookup_formly(request: str) -> dict:
    """Availability probe only. Returns a marker, never Formly knowledge."""
    log('lookup_called')
    return {'marker':request}


original_list=server._mcp_server.request_handlers[types.ListToolsRequest]


async def record_list(request):
    log('tools_list_requested')
    return await original_list(request)


server._mcp_server.request_handlers[types.ListToolsRequest]=record_list
log('server_ready')
server.run(transport='stdio')

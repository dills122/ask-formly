"""Local stdio Formly MCP; one raw-request tool and unchanged retrieval foundation."""
import argparse
import contextlib
import json
import sys
import time
import uuid
from pathlib import Path
from typing import Any
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from planner import CodexPlanner
from service import LookupService
from backend import Backend

HERE = Path(__file__).resolve().parent

def create_server(service, audit_dir=None):
    @contextlib.asynccontextmanager
    async def lifespan(_):
        try:
            with contextlib.redirect_stdout(sys.stderr):
                yield {}
        finally: await service.close()
    mcp = FastMCP('formly-poc', lifespan=lifespan, instructions=(
        'Use lookup_formly for Formly library questions. It derives library questions, '
        'adds advisory GLiNER spans and returns candidate facts, not verified answers. '
        'Check each claim and its conditions against the request, cite returned provenance, '
        'and state missing support. Knowledge is a bounded Formly 6.3.12 core/Material sample. '
        'No application investigation is available.'))

    @mcp.tool(structured_output=True, annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                                          idempotentHint=False, openWorldHint=True))
    async def lookup_formly(request: str) -> dict[str, Any]:
        """Look up a natural-language Formly library request. Preserve the complete request, including conditions and exclusions. Returns derived questions, advisory spans, original candidate facts/citations and explicit limits. Planning uses the configured authenticated Codex model. Does not inspect applications or certify answer completeness."""
        started = time.perf_counter()
        record = {'request':request}
        try:
            result = await service.lookup(request)
            record['result'] = result
            return result
        except Exception as exc:
            record['error']={'type':type(exc).__name__,'message':str(exc)}
            raise
        finally:
            record['seconds']=time.perf_counter()-started
            if audit_dir is not None:
                path=Path(audit_dir);path.mkdir(parents=True,exist_ok=True)
                with (path/(uuid.uuid4().hex+'.json')).open('x') as f:
                    json.dump(record,f,indent=2,allow_nan=False)
    return mcp

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed',type=int,choices=(1701,1702),default=1701)
    parser.add_argument('--audit-dir',type=Path)
    parser.add_argument('--planner-runs',type=Path,default=HERE/'runtime/planner')
    args=parser.parse_args()
    service=LookupService(CodexPlanner(args.planner_runs),lambda:Backend(args.seed))
    # Native dependencies may print to stdout; MCP owns the original stdout only.
    mcp=create_server(service,args.audit_dir)
    mcp.run(transport='stdio')

if __name__=='__main__':main()

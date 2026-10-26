"""Local stdio Formly MCP with project settings and unchanged retrieval."""
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
from request_context import ContextLookup

HERE = Path(__file__).resolve().parent

def create_server(service, audit_dir=None, settings=None, *, context=None):
    context = context if context is not None else ContextLookup(service, settings=settings)
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
        'Use project_id and optional worktree_id to reuse saved Formly version and UI adapter settings. '
        'Supplying those settings with a project_id saves them. Use get_formly_project_settings '
        'and set_formly_project_settings to inspect or update them without a question. '
        'Coverage errors recommend web lookup; do not present them as an evidence packet. '
        'No application investigation is available.'))

    @mcp.tool(structured_output=True, annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False,
                                          idempotentHint=False, openWorldHint=True))
    async def lookup_formly(request: str, project_id: str | None = None,
                            worktree_id: str | None = None, formly_version: str | None = None,
                            ui_adapter: str | None = None) -> dict[str, Any]:
        """Preserve the complete question. Version accepts v6, 6.3 or 6.3.12. With project_id, supplied version/adapter update saved settings; omissions reuse them. Worktree settings take precedence over project settings. Without project_id, supplied settings apply only to this call. IDs are caller-supplied stable keys (paths are fine); no repository inspection occurs. Returns candidate facts or an explainable coverage error. Hosted planning is used for supported requests."""
        started = time.perf_counter()
        record = {'request':request, 'project_id':project_id, 'worktree_id':worktree_id,
                  'formly_version':formly_version, 'ui_adapter':ui_adapter}
        try:
            result = await context.lookup(request, project_id, worktree_id, formly_version, ui_adapter)
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
    @mcp.tool(structured_output=True, annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
    async def get_formly_project_settings(project_id: str, worktree_id: str | None = None) -> dict[str, Any]:
        """Read effective settings; absent worktree fields inherit project settings. Missing values remain unset."""
        return context.settings.get(project_id, worktree_id)

    @mcp.tool(structured_output=True, annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False,
                                                               idempotentHint=True, openWorldHint=False))
    async def set_formly_project_settings(project_id: str, worktree_id: str | None = None,
                                          formly_version: str | None = None,
                                          ui_adapter: str | None = None) -> dict[str, Any]:
        """Save supplied fields; omitted fields remain unchanged. Versions may be saved even when knowledge is unavailable. Settings persist across server restarts, with no expiry."""
        return context.settings.set(project_id, worktree_id, formly_version, ui_adapter)

    return mcp

def main():
    from planner import CodexPlanner
    from service import LookupService
    from backend import Backend
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

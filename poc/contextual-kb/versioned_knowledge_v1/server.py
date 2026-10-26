"""Opt-in candidate stdio server; only the accepted 6.3.12 catalog is enabled."""
import argparse
import contextlib
import sys
from pathlib import Path
from typing import Any
POC=Path(__file__).resolve().parent.parent
sys.path[:0]=[str(POC),str(POC/'mcp_v1')]
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from mcp_foundation.service import make_service
from retrieval_repair_v1.selector import Selector
from versioned_knowledge_v1.backend import Backend
from versioned_knowledge_v1.context import Context


def create_server(database,runtime,seed=1701):
    def factory(adapter):
        run=runtime/(adapter or 'default')
        return make_service(seed=seed,runtime_dir=run,backend_factory=lambda:Backend(database,seed,adapter,Selector(run/'selector')))
    context=Context(factory)
    @contextlib.asynccontextmanager
    async def lifespan(_):
        try:
            with contextlib.redirect_stdout(sys.stderr):yield {}
        finally:await context.close()
    mcp=FastMCP('formly-versioned-candidate',lifespan=lifespan,instructions='Bounded Formly 6.3.12 core/Material candidate facts with exact source provenance. Check conditions and cite returned evidence. Unsupported versions require official web lookup. No application investigation.')
    @mcp.tool(structured_output=True,annotations=ToolAnnotations(readOnlyHint=False,openWorldHint=True))
    async def lookup_formly(request:str,project_id:str|None=None,worktree_id:str|None=None,formly_version:str|None=None,ui_adapter:str|None=None)->dict[str,Any]:
        """Look up Formly library knowledge. Supplied settings persist with project_id."""
        return await context.lookup(request,project_id,worktree_id,formly_version,ui_adapter)
    @mcp.tool(structured_output=True)
    def get_formly_project_settings(project_id:str,worktree_id:str|None=None)->dict[str,Any]:
        return context.settings.get(project_id,worktree_id)
    @mcp.tool(structured_output=True)
    def set_formly_project_settings(project_id:str,worktree_id:str|None=None,formly_version:str|None=None,ui_adapter:str|None=None)->dict[str,Any]:
        return context.settings.set(project_id,worktree_id,formly_version,ui_adapter)
    return mcp

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',type=Path,required=True)
    parser.add_argument('--runtime',type=Path,required=True)
    parser.add_argument('--seed',type=int,choices=(1701,1702),default=1701)
    args=parser.parse_args()
    create_server(args.database,args.runtime,args.seed).run(transport='stdio')

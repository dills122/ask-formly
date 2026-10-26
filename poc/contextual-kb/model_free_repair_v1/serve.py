"""Stateless structured repair results around the frozen model-free service."""
import argparse
import contextlib
import json
from pathlib import Path
import time
import uuid
from typing import Any
from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult,TextContent,ToolAnnotations
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from feedback import RepairService,QuestionPlan
from candidate import POC,Service,Store

HERE=Path(__file__).resolve().parent


def tool_result(packet,error=False):
    return CallToolResult(content=[TextContent(type='text',text=json.dumps(packet,ensure_ascii=False))],structuredContent=packet,isError=error)


def create_server(service,audit_dir=None):
    @contextlib.asynccontextmanager
    async def lifespan(_):
        try:yield {}
        finally:service.store.close()
    mcp=FastMCP('ask-formly-model-free-repair',lifespan=lifespan,instructions=(HERE/'CALLER.md').read_text())
    @mcp.tool(structured_output=False,annotations=ToolAnnotations(readOnlyHint=False,destructiveHint=False,openWorldHint=False))
    async def lookup_formly(request:str,plan:QuestionPlan|None=None,project_id:str|None=None,worktree_id:str|None=None,formly_version:str|None=None,ui_adapter:str|None=None)->CallToolResult:
        """Supply the original request AND your Formly library plan on the first call. Missing plans return PLAN_REQUIRED. needs_refinement means repair the indicated fields and resubmit without weakening the request (at most two repairs). unsupported_scope means stop. no_evidence is not proof of nonexistence. ok returns candidate facts, not a verified answer. This call completes with feedback; there is no server callback or model. Explicit project settings are saved separately when project_id is supplied. Schema-invalid arguments use ordinary SDK errors; structured repair feedback applies to shaped plans."""
        args=dict(request=request,plan=plan.model_dump() if plan is not None else None,project_id=project_id,worktree_id=worktree_id,formly_version=formly_version,ui_adapter=ui_adapter)
        row=dict(arguments=args);started=time.perf_counter()
        try:
            packet,error=await service.lookup(**args);row.update(result=packet,is_error=error)
            return tool_result(packet,error)
        except Exception as exc:
            row['error']=dict(type=type(exc).__name__,message=str(exc));raise
        finally:
            row['seconds']=time.perf_counter()-started
            if audit_dir:
                audit_dir.mkdir(parents=True,exist_ok=True)
                with (audit_dir/(uuid.uuid4().hex+'.json')).open('x') as f:json.dump(row,f,indent=2)
    @mcp.tool(structured_output=False,annotations=ToolAnnotations(readOnlyHint=True,openWorldHint=False))
    async def get_formly_facts(fact_ids:list[str],formly_version:str|None=None,ui_adapter:str|None=None)->CallToolResult:
        """Fetch full records for known IDs, repeating lookup's resolved scope. No inference. Use fewer IDs if the bounded evidence budget is exceeded."""
        return tool_result(await service.base.get_facts(fact_ids,formly_version,ui_adapter))
    return mcp


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--database',type=Path,default=POC/'build/knowledge.sqlite')
    p.add_argument('--sha256',default=json.loads((HERE.parent/'model_free_v1/baseline-state.json').read_text())['installed_db_sha256'])
    p.add_argument('--settings',type=Path,default=HERE/'test-output/settings.sqlite')
    p.add_argument('--audit-dir',type=Path)
    a=p.parse_args();store=Store(a.database,a.sha256)
    create_server(RepairService(Service(store,a.settings)),a.audit_dir).run(transport='stdio')

if __name__=='__main__':main()

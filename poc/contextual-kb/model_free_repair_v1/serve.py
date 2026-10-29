"""Stateless structured repair results around the frozen model-free service."""
import argparse
import contextlib
import json
from pathlib import Path
import time
import uuid
from typing import Any, Literal
from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult,TextContent,ToolAnnotations
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from feedback import RepairService,QuestionPlan
from model_free_v1.server import OriginalRequest, FactIds, ProjectId
from model_free_v1.help import HelpLimit, HelpOffset, HelpTopic, help_packet
from model_free_v1.response import fits_packet, make_tool_result
from candidate import POC,Service,Store
from mcp_runtime.identity import build_identity

HERE=Path(__file__).resolve().parent


def tool_result(packet,error=False):
    # structured_output=False promises no separate output schema. A single full
    # JSON text block works for text-only clients and avoids doubling evidence.
    if packet.get('response_format')!='full-v1' and not fits_packet(packet,error):
        raise ValueError('Tool result exceeds its byte budget; request fewer IDs or a smaller discovery/help page')
    return make_tool_result(packet,error)


def create_server(service,audit_dir=None):
    identity = build_identity(json.loads((POC/'mcp_runtime/model-free.json').read_text()))
    @contextlib.asynccontextmanager
    async def lifespan(_):
        try:yield {}
        finally:service.store.close()
    mcp=FastMCP('ask-formly-model-free-repair',lifespan=lifespan,instructions=(HERE/'CALLER.md').read_text())
    # Pinned MCP 1.26 FastMCP has no version constructor argument. Its low-level
    # server uses this explicit version for the initialize serverInfo response.
    mcp._mcp_server.version = identity['build_id']
    @mcp.tool(structured_output=False,annotations=ToolAnnotations(readOnlyHint=False,destructiveHint=False,openWorldHint=False))
    async def lookup_formly(request:OriginalRequest,plan:QuestionPlan|None=None,project_id:ProjectId=None,worktree_id:str|None=None,formly_version:str|None=None,ui_adapter:str|None=None)->CallToolResult:
        """First time? Call help_formly for a valid two-question example and scoped topic IDs. Supply the unchanged original request AND your Formly library plan on the first call. Copy each condition exactly from request into every bound question. Include known relevant Formly API/config names; matching is lexical/symbol-based, not semantic. Copy explicitly requested version/adapter into library_constraints, even when also in question text. Missing plans return PLAN_REQUIRED; an omitted field in a recognized opening scope clause returns MISSING_SCOPE_METADATA. needs_refinement means repair the indicated fields and resubmit without weakening the request (at most two repairs). unsupported_scope means stop. no_evidence is not proof of nonexistence. ok returns candidate facts, not a verified answer. This call completes with feedback; there is no server callback or model. Explicit project settings are saved separately when project_id is supplied. Schema-invalid arguments use ordinary SDK errors; structured repair feedback applies to shaped plans."""
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
    async def get_formly_facts(fact_ids:FactIds,formly_version:str|None=None,ui_adapter:str|None=None,response_format:Literal["compact","full"]="compact")->CallToolResult:
        """Fetch 1..16 complete known fact IDs, repeating lookup's resolved version/adapter. Compact responses share provenance via sources/evidence references; full expands citations inline. Read claims with conditions/limits. Unknown/ineligible IDs reject atomically. Compact oversize returns batch_required with no facts and measured retry_batches arguments: retry directly without rediscovery. response_too_large identifies records that cannot fit alone. No relevance or completeness certification."""
        return tool_result(await service.base.get_facts(fact_ids,formly_version,ui_adapter,response_format=response_format))
    @mcp.tool(structured_output=False,annotations=ToolAnnotations(readOnlyHint=True,openWorldHint=False))
    async def help_formly(topic:HelpTopic=None,formly_version:str|None=None,ui_adapter:str|None=None,offset:HelpOffset=0,limit:HelpLimit=16)->CallToolResult:
        """First-time workflow, valid example, limits and scoped topic inventory. Pass an exact topic prefix to list complete fetchable fact IDs. Use offset >= 0 and limit 1..32 (default 16). Page using next_offset; repeat resolved scope. Help does not certify relevance or runtime behavior."""
        packet = await help_packet(service,topic,formly_version,ui_adapter,offset,limit)
        packet['build_identity'] = identity.copy()
        return tool_result(packet)
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

"""Isolated model-free stdio MCP. The client harness supplies all reasoning."""
import argparse
import contextlib
import json
from pathlib import Path
import time
from typing import Annotated, Any, Literal
import uuid

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import BaseModel, ConfigDict, Field, StrictInt
from candidate import POC, Service, Store
from model_free_v1.help import help_packet

HERE=Path(__file__).resolve().parent
OriginalRequest = Annotated[str, Field(description="The user request unchanged; put derived library questions in plan, not here.")]
FactIds = Annotated[list[str], Field(min_length=1, max_length=16, description="1..16 complete known fact IDs, never topic prefixes. Byte limits may require fewer IDs.")]
ProjectId = Annotated[str | None, Field(description="Stable project ID. Explicit scope saves to a separate settings file; clients sharing that file and ID share defaults, not conversations.")]

class Question(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    question: str=Field(min_length=1,max_length=2000,description="Focused library question; include every bound condition verbatim and known relevant API/config names.")
    reason: str=Field(min_length=1,max_length=1000,description="Why this question is needed to answer the original request.")

class Constraints(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    formly_version: str|None=Field(description="Copy explicitly requested Formly version here even when repeated in question text or top-level args; null only when unspecified.")
    ui_adapter: str|None=Field(description="Copy explicitly requested UI adapter here; null only when unspecified. Explicit scope must agree with top-level arguments.")

class Binding(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    condition: str=Field(min_length=1,max_length=12000,description="Copy an exact excerpt from request into every bound question text. Preserve spelling, negation and restrictions; do not paraphrase.")
    question_indexes: list[StrictInt]=Field(min_length=1,max_length=6,description="Unique zero-based indexes of questions containing condition verbatim.")

class QuestionPlan(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    formly_questions: list[Question]=Field(max_length=6)
    library_constraints: Constraints
    condition_bindings: list[Binding]=Field(max_length=48)


def create_server(service,audit_dir=None):
    @contextlib.asynccontextmanager
    async def lifespan(_):
        try:yield {}
        finally:service.store.close()
    mcp=FastMCP('ask-formly-model-free-candidate',lifespan=lifespan,instructions=(HERE/'CALLER.md').read_text())
    @mcp.tool(structured_output=True,annotations=ToolAnnotations(readOnlyHint=False,destructiveHint=False,openWorldHint=False))
    async def lookup_formly(request:OriginalRequest,plan:QuestionPlan|None=None,project_id:ProjectId=None,worktree_id:str|None=None,formly_version:str|None=None,ui_adapter:str|None=None)->dict[str,Any]:
        """First time? Call help_formly for a valid two-question example and topic IDs. Retrieve Formly library evidence. YOU derive focused questions and supply plan; preserve conditions, exact names, exclusions and supplied premises. Without plan this searches the raw request once (not decomposed). No server inference. Returns candidate facts, not a verified answer. With project_id, explicit settings are saved separately from knowledge. Scope conflicts reject. Read conditions/limits; use get_formly_facts for omitted IDs. Explicit version/UI args take precedence over saved defaults, but may not conflict with plan constraints."""
        inputs=dict(request=request,plan=plan.model_dump() if plan is not None else None,project_id=project_id,worktree_id=worktree_id,formly_version=formly_version,ui_adapter=ui_adapter)
        row=dict(arguments=inputs);start=time.perf_counter()
        try:
            result=await service.lookup(**inputs);row['result']=result;return result
        except Exception as exc:
            row['error']=dict(type=type(exc).__name__,message=str(exc));raise
        finally:
            row['seconds']=time.perf_counter()-start
            if audit_dir:
                audit_dir.mkdir(parents=True,exist_ok=True)
                with (audit_dir/(uuid.uuid4().hex+'.json')).open('x') as f:json.dump(row,f,indent=2)
    @mcp.tool(structured_output=True,annotations=ToolAnnotations(readOnlyHint=True,openWorldHint=False))
    async def get_formly_facts(fact_ids:FactIds,formly_version:str|None=None,ui_adapter:str|None=None,response_format:Literal["compact","full"]="compact")->dict[str,Any]:
        """Fetch 1..16 known fact IDs with full provenance, conditions and limits. Repeat lookup's resolved version and adapter to preserve scope. Unknown or ineligible IDs reject atomically. If output exceeds budget, request fewer IDs. No inference, no answer completeness judgment."""
        return await service.get_facts(fact_ids,formly_version,ui_adapter,response_format=response_format)
    @mcp.tool(structured_output=True,annotations=ToolAnnotations(readOnlyHint=True,openWorldHint=False))
    async def help_formly(topic:str|None=None,formly_version:str|None=None,ui_adapter:str|None=None,offset:int=0,limit:int=16)->dict[str,Any]:
        """First-time workflow, valid example, limits and scoped topic inventory. Pass an exact topic prefix to list complete fetchable fact IDs. Page using next_offset; repeat resolved scope. Help does not certify relevance or runtime behavior."""
        return await help_packet(service,topic,formly_version,ui_adapter,offset,limit)
    return mcp


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',type=Path,default=POC/'build/knowledge.sqlite')
    parser.add_argument('--sha256',default=json.loads((HERE/'baseline-state.json').read_text())['installed_db_sha256'])
    parser.add_argument('--settings',type=Path,default=HERE/'test-output/project-settings.sqlite')
    parser.add_argument('--audit-dir',type=Path)
    args=parser.parse_args()
    store=Store(args.database,args.sha256)
    create_server(Service(store,args.settings),args.audit_dir).run(transport='stdio')

if __name__=='__main__':main()

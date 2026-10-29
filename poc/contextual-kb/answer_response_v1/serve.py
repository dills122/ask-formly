"""Run the isolated answer/provenance experiment against an explicit read-only DB."""
import argparse
import contextlib
import json
from pathlib import Path
import sys
from typing import Literal

POC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(POC))
sys.path.insert(0, str(POC / 'model_free_v1'))
sys.path.insert(0, str(POC / 'model_free_repair_v1'))
from answer_response_v1.candidate import AnswerService, Store, identity
from model_free_repair_v1.feedback import RepairService, QuestionPlan
from model_free_repair_v1.serve import tool_result
from model_free_v1.server import OriginalRequest, FactIds, ProjectId
from model_free_v1.help import HelpTopic, HelpLimit, HelpOffset, help_packet
from model_free_v1.response import fits_packet
from parity_v1.discovery import discover
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import StrictInt, StrictStr

HERE = Path(__file__).resolve().parent
READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=False)
SELECTION_FIRST = ('Before paging, map unmet decisions to current claims/conditions/limits. '
    'Batch-fetch suitable IDs for citations; examples support only demonstrated behavior, not a full contract. '
    'Continue for gaps with no suitable listed fact; keep scope/selectors while paging.')
FOCUS_REMINDER = (' Focus reranks omissions only; keep it unchanged while paging, reset offset zero when it changes. '
    'Matching or absence is not support or completeness.')


async def discover_with_repair(service, request, plan=None, **arguments):
    """Keep structured discovery repair on the same operation and selectors.

    The public schema requires a non-null plan. This wrapper also handles legacy
    direct invocations and valid-shaped plans rejected by the existing gate.
    It never reconstructs a missing plan or relaxes any declared condition.
    """
    packet, error = await discover(service, request, plan=plan, **arguments)
    if packet.get('status') == 'needs_refinement':
        packet['next_action'] = dict(packet['next_action'],
            tool='discover_formly_candidates',
            preserve_arguments=['request', 'formly_version', 'ui_adapter',
                                'offset', 'limit', 'question_index', 'focus'],
            message='Retry discovery with the complete original lookup plan and unchanged request, scope, offset, limit, question_index and focus. There is no saved conversation plan. Correct only the reported plan issues; do not restart lookup or invent a smaller plan.')
    elif packet.get('status') == 'candidates' and packet.get('candidates'):
        message = SELECTION_FIRST + (FOCUS_REMINDER if 'focus_ref' in packet else '')
        # Replace prose only. Never reclaim bytes by dropping/reordering candidates.
        if len(message.encode('utf-8')) > len(packet['next_action']['message'].encode('utf-8')):
            raise ValueError('Selection guidance must not enlarge discovery responses')
        packet['next_action']['message'] = message
        if not fits_packet(packet, error):
            raise ValueError('Selection guidance exceeds the existing response budget')
    return packet, error


def create_server(service):
    build = identity()
    @contextlib.asynccontextmanager
    async def lifespan(_):
        try:
            yield {}
        finally:
            service.store.close()
    server = FastMCP('ask-formly-answer-response-candidate', lifespan=lifespan,
                     instructions=(HERE / 'CALLER.md').read_text())
    server._mcp_server.version = build['build_id']

    @server.tool(structured_output=False, annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=False))
    async def lookup_formly(request: OriginalRequest, plan: QuestionPlan | None = None,
            project_id: ProjectId = None, worktree_id: str | None = None,
            formly_version: str | None = None, ui_adapter: str | None = None):
        """Supply unchanged request plus focused Formly question plan; call help_formly for an example. Preserve exact conditions and scope. Returns complete answer facts and usable citations; detailed provenance is deferred, not missing claims. Assess relevance, conditions and limits. Fetch provenance only for requested quotes, hashes, offsets or source audits. Repair needs_refinement without weakening the request; stop for unsupported_scope. No model callback or completeness certification."""
        packet, error = await service.lookup(request, plan.model_dump() if plan else None,
            project_id=project_id, worktree_id=worktree_id,
            formly_version=formly_version, ui_adapter=ui_adapter)
        return tool_result(packet, error)

    @server.tool(structured_output=False, annotations=READ_ONLY)
    async def get_formly_facts(fact_ids: FactIds, formly_version: str | None = None,
            ui_adapter: str | None = None, response_format: Literal['answer', 'compact', 'full'] = 'answer'):
        """Fetch1..16 selected complete facts. Default answer includes complete claims, context, conditions, limits, scope, relationships and source citations. Detailed provenance is deferred; ordinary answers do not require fetching it. Repeat resolved scope. Unknown/ineligible IDs reject atomically. batch_required delivers no records: follow exact retry_batches tool/arguments. Explicit compact/full retain the baseline evidence formats."""
        return tool_result(await service.base.get_facts(fact_ids, formly_version, ui_adapter, response_format))

    @server.tool(structured_output=False, annotations=READ_ONLY)
    async def get_formly_provenance(fact_ids: FactIds, formly_version: str, ui_adapter: str | None):
        """Fetch original detailed provenance for1..16 fact IDs: authored quotation/hash/offsets and full evidence records. Repeat exact resolved version/adapter from answer. Use only for requested provenance verification, quotations or audit details; ordinary citing uses answer citations. Stored-excerpt availability is explicit; authored summary quotations are not implementation excerpts. Switching formats or refetching the same IDs cannot add absent stored excerpts. No duplicate facts or new relevance claims. IDs validate atomically. batch_required delivers no records: follow measured retry_batches tool/arguments; unsplittable IDs must not be retried unchanged."""
        return tool_result(await service.base.get_provenance(fact_ids, formly_version, ui_adapter))

    @server.tool(structured_output=False, annotations=READ_ONLY)
    async def discover_formly_candidates(request: str, plan: QuestionPlan,
            formly_version: str | None = None, ui_adapter: str | None = None,
            offset: int = 0, limit: int = 16, question_index: StrictInt | None = None,
            focus: StrictStr | None = None):
        """Recover omissions for an unmet original question. Required plan is the complete original lookup plan, even after a successful lookup; the server stores no conversation plan. Repeat original request/plan/scope. question_index selects an original question; focus reranks its omissions only. Change selector/focus resets offset0; otherwise use next_offset. Before another page/refocus, map unmet decisions to these claims/conditions/limits and batch-fetch suitable listed IDs with get_formly_facts. Retain limited support from examples without assuming a complete contract. Continue only for remaining gaps with no suitable listed candidate. Do not rediscover delivered IDs. Matching and absence are not completeness judgments."""
        packet, error = await discover_with_repair(service, request, plan.model_dump(),
            formly_version=formly_version, ui_adapter=ui_adapter, offset=offset, limit=limit,
            question_index=question_index, focus=focus)
        return tool_result(packet, error)

    @server.tool(structured_output=False, annotations=READ_ONLY)
    async def help_formly(topic: HelpTopic = None, formly_version: str | None = None,
            ui_adapter: str | None = None, offset: HelpOffset = 0, limit: HelpLimit = 16):
        """Workflow and scoped topic/ID inventory; not supporting facts. Exact topic prefixes, limit1..32, next_offset for paging. Includes valid plan example. Answer facts have usable citations; provenance retrieval is optional unless requested details require it."""
        packet = await help_packet(service, topic, formly_version, ui_adapter, offset, limit)
        if packet.get('status') == 'help':
            packet['workflow'] = [
                'Before another discovery page or refocus, map each unmet decision to already-listed claims, conditions and limits. Batch-fetch suitable selected IDs for citations, then reassess the remaining gaps. Keep partial support from a worked example without treating it as a full API contract; continue only for facets without a suitable current candidate. Do not fetch irrelevant IDs or mark an unresolved facet complete.'
                if step.startswith('Before another discovery,') else step
                for step in packet['workflow']]
            packet['response'].update(
                record_kinds='answer_facts: complete facts and usable source citations; detailed provenance deferred. claims_without_provenance: discovery claims need selected fact fetch. topic_inventory: IDs/titles only. batch_instructions: no records delivered.',
                answer='Default lookup/fetch preserves complete facts, conditions, limits, scope and citations. candidate_only means relevance needs assessment; deferred provenance does not mean incomplete facts.',
                provenance='get_formly_provenance takes selected IDs and exact resolved scope. Use for requested source quotes, hashes, offsets or audits, not automatically after every answer response. stored_excerpt reports whether a nonblank evidence excerpt is stored; absent is not a claim that source text does not exist. Changing formats/refetching the same IDs cannot add absent excerpts. Authored summary quotations are distinct. Different relevant facts and pinned external sources remain legitimate recovery.')
            packet['workflow'].extend([
                'Use answer facts directly for ordinary answers. Fetch detailed provenance only when the task requires details absent from the returned citations; batch the necessary selected IDs.',
                'Discovery requires the complete original lookup plan on every call, plus unchanged request and resolved scope; no conversation plan is stored. Preserve selector/focus/paging arguments while repairing a plan error.',
                'Reuse previously fetched source evidence only when its ID, release and source location agree, and its hash agrees when supplied. A shared evidence record does not replace a different fact’s authored quotation, offsets, applicability or other evidence; fetch those distinct details when requested.'])
        packet['build_identity'] = {key: value for key, value in build.items() if key not in ('files', 'first_party_import_closure')}
        return tool_result(packet)
    return server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--settings', type=Path, required=True)
    args = parser.parse_args()
    args.settings.parent.mkdir(parents=True, exist_ok=True)
    store = Store(args.database, args.sha256)
    create_server(RepairService(AnswerService(store, args.settings))).run(transport='stdio')


if __name__ == '__main__':
    main()

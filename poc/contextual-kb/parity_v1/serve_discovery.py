"""Isolated additive discovery tool; installed/native MCP remains unchanged."""
import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'model_free_repair_v1'))
from serve import create_server, tool_result, RepairService, QuestionPlan, Service, Store, POC
from mcp.types import ToolAnnotations
from pydantic import StrictInt, StrictStr
from discovery import discover


def create_discovery_server(service, audit_dir=None):
    server = create_server(service, audit_dir)

    @server.tool(structured_output=False, annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
    async def discover_formly_candidates(request: str, plan: QuestionPlan | None = None,
            formly_version: str | None = None, ui_adapter: str | None = None,
            offset: int = 0, limit: int = 16, question_index: StrictInt | None = None,
            focus: StrictStr | None = None):
        """Recover evidence for an unmet question after lookup. Repeat the identical original request, plan and resolved scope; optionally set question_index to that question's zero-based index in the original plan. Null pages all questions. Optional focus (1..500 nonblank characters) lexically reranks only original omissions for an unmet aspect, e.g. 'initial model versus defaultValue' or 'shared control validators'. It adds no candidates and changes no conditions or scope. Without focus, targeted pages retain the question's ranking. Globally delivered facts are excluded. Page using next_offset with identical selectors and focus; restart offset zero when either changes. Up to32 records/24KB per page. Read complete claims/conditions/limits, select relevant IDs and fetch citations with get_formly_facts. Matching is not support, no useful match is not proof of absence, and no relevance/completeness judgment or plan repair occurs."""
        packet, error = await discover(service, request, plan.model_dump() if plan else None,
            formly_version=formly_version, ui_adapter=ui_adapter, offset=offset, limit=limit,
            question_index=question_index, focus=focus)
        return tool_result(packet, error)
    return server


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--settings', type=Path, default=HERE / 'test-output/discovery-settings.sqlite')
    parser.add_argument('--audit-dir', type=Path)
    args = parser.parse_args()
    sha = json.loads((POC / 'model_free_v1/baseline-state.json').read_text())['installed_db_sha256']
    store = Store(POC / 'build/knowledge.sqlite', sha)
    create_discovery_server(RepairService(Service(store, args.settings)), args.audit_dir).run(transport='stdio')

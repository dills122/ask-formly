"""Isolated additive discovery tool; installed/native MCP remains unchanged.

For the model-free runtime this IS the outermost served layer: mcp_runtime/
launcher.py's start_model_free calls create_discovery_server from here
directly. It wraps model_free_repair_v1.serve.create_server, which in turn
wraps model_free_v1.candidate.Store/Service.
"""
import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'model_free_repair_v1'))
from serve import create_server, tool_result, RepairService, QuestionPlan, Service, Store, POC
from mcp.types import ToolAnnotations
from discovery import discover


def create_discovery_server(service, audit_dir=None):
    server = create_server(service, audit_dir)

    @server.tool(structured_output=False, annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
    async def discover_formly_candidates(request: str, plan: QuestionPlan | None = None,
            formly_version: str | None = None, ui_adapter: str | None = None,
            offset: int = 0, limit: int = 16):
        """After lookup, inspect omitted fact candidates with complete claims/conditions/limits. Repeat the identical original request, plan and resolved scope. Page using next_offset; stop when sufficient or exhausted. Up to32 records/24KB per page. These are not cited answers: assess relevance and use get_formly_facts for chosen IDs. No inference, automatic relevance judgment or plan repair occurs. Never treat an irrelevant hit as support."""
        packet, error = await discover(service, request, plan.model_dump() if plan else None,
            formly_version=formly_version, ui_adapter=ui_adapter, offset=offset, limit=limit)
        return tool_result(packet, error)
    return server


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--settings', type=Path, default=HERE / 'test-output/discovery-settings.sqlite')
    parser.add_argument('--audit-dir', type=Path)
    args = parser.parse_args()
    # baseline-state.json is a one-time snapshot from #9, never updated across later
    # promotions; mcp_runtime/model-free.json is the pin the real launcher trusts.
    sha = json.loads((POC / 'mcp_runtime/model-free.json').read_text())['files']['build/knowledge.sqlite']
    store = Store(POC / 'build/knowledge.sqlite', sha)
    create_discovery_server(RepairService(Service(store, args.settings)), args.audit_dir).run(transport='stdio')

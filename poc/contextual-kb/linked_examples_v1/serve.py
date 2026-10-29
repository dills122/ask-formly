"""Explicit opt-in MCP for candidate examples; never modifies the installed DB."""
import argparse
from pathlib import Path
import sys
from typing import Annotated

HERE = Path(__file__).resolve().parent
POC = HERE.parent
sys.path.insert(0, str(POC))
sys.path.insert(0, str(POC / 'model_free_v1'))
from mcp.types import ToolAnnotations
from pydantic import Field, StrictInt, StrictStr
from model_free_repair_v1.serve import create_server as repair_server, tool_result, QuestionPlan
from model_free_repair_v1.feedback import RepairService
from model_free_v1.candidate import Service, Store
from parity_v1.discovery import discover
from linked_examples_v1.catalog import Catalog, authored_fact_ids

Ids = Annotated[list[str], Field(min_length=1, max_length=16)]


class BaseWithExamples:
    def __init__(self, base, catalog):
        self.base = base
        self.catalog = catalog

    def __getattr__(self, name):
        return getattr(self.base, name)

    async def get_facts(self, *args, **kwargs):
        packet = await self.base.get_facts(*args, **kwargs)
        # Full facts retain their existing explicit large-response contract.
        return packet if packet.get('response_format') == 'full-v1' else self.catalog.enrich(packet)


class WithExamples:
    def __init__(self, service, catalog):
        self.service = service
        self.catalog = catalog
        self.base = BaseWithExamples(service.base, catalog)
        self.store = service.store

    async def lookup(self, *args, **kwargs):
        packet, error = await self.service.lookup(*args, **kwargs)
        return (packet if error else self.catalog.enrich(packet)), error


def create_server(service, catalog, audit_dir=None):
    linked = WithExamples(service, catalog)
    server = repair_server(linked, audit_dir)
    # FastMCP exposes instructions as a read-only property; the low-level server
    # owns the initialize response. Keep this change on the candidate instance.
    server._mcp_server.instructions = server.instructions + '\n\n' + (HERE / 'CALLER.md').read_text()

    @server.tool(structured_output=False, annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
    async def discover_formly_candidates(request: str, plan: QuestionPlan | None = None,
            formly_version: str | None = None, ui_adapter: str | None = None,
            offset: int = 0, limit: int = 16, question_index: StrictInt | None = None,
            focus: StrictStr | None = None):
        """Inspect omitted fact candidates after lookup. Repeat original request, plan and resolved scope. Optional question_index selects an original question; focus (1..500 nonblank characters) only reranks its original omissions lexically, adding no evidence or conditions. Keep both selectors identical while paging next_offset; restart offset zero if either changes. Matching is not support and no useful match is not proof of absence. Fetch relevant IDs for citations before answering. Examples are separate: get_formly_examples(fact_ids=[...])."""
        packet, error = await discover(service, request, plan.model_dump() if plan else None,
            formly_version=formly_version, ui_adapter=ui_adapter, offset=offset, limit=limit,
            question_index=question_index, focus=focus)
        return tool_result(packet, error)

    @server.tool(structured_output=False, annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
    async def get_formly_examples(fact_ids: Ids | None = None, example_ids: Ids | None = None,
            formly_version: str = '6.3.12', ui_adapter: str = 'Material',
            offset: StrictInt = 0, limit: StrictInt = 8, file_paths: Ids | None = None):
        """Isolated candidate examples, not promoted knowledge. Supply exactly one selector: fact_ids lists linked example summaries; example_ids retrieves complete examples/code. Repeat resolved scope; only 6.3.12 Material is available. Page with next_offset, never infer absence from a partial page. For large examples request named file_paths from their manifest. Code is never truncated; excessive single files reject. Read per-fact support, prerequisites, limits and verification status. Linking does not prove every line or certify application behavior."""
        return tool_result(catalog.retrieve(fact_ids=fact_ids, example_ids=example_ids,
            formly_version=formly_version, ui_adapter=ui_adapter, offset=offset, limit=limit,
            file_paths=file_paths))
    return server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--settings', type=Path, required=True)
    parser.add_argument('--examples', type=Path, default=HERE / 'examples')
    parser.add_argument('--audit-dir', type=Path)
    args = parser.parse_args()
    if args.database.resolve() == args.settings.resolve():
        parser.error('Settings must be separate from knowledge database')
    catalog = Catalog(args.examples, authored_fact_ids(POC / 'authored'))
    store = Store(args.database, args.sha256)
    if not set(fid for r in catalog.records.values() for fid in [l['fact_id'] for l in r['fact_links']]) <= store.scopes('6.3.12', 'material').keys():
        store.close()
        raise ValueError('Example links are not eligible in candidate DB scope')
    create_server(RepairService(Service(store, args.settings)), catalog, args.audit_dir).run(transport='stdio')


if __name__ == '__main__':
    main()

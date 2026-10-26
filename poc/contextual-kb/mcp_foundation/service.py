"""Accepted composition with reviewed capitalization repair and installed DB."""
from pathlib import Path
from mcp_v1.service import LookupService
from condition_candidate_v2.planner import CodexPlanner
from retrieval_repair_v1.integration import Backend
from retrieval_repair_v1.selector import Selector
from mcp_foundation.capitalization import CapitalizingPlanner


def make_service(seed=1701, runtime_dir=None, planner=None, backend_factory=None):
    runtime_dir = Path(runtime_dir) if runtime_dir is not None else Path(__file__).resolve().parent/'runtime'
    if planner is None:
        planner = CodexPlanner(runtime_dir/'planner')
    if backend_factory is None:
        backend_factory = lambda: Backend(seed, Selector(runtime_dir/'selector'))
    return LookupService(CapitalizingPlanner(planner), backend_factory)

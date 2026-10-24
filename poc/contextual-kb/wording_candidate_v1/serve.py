"""Opt-in launcher: wording adapter plus unchanged bounded retrieval candidate."""
import argparse
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
POC = HERE.parent
sys.path.insert(0, str(POC))
sys.path.insert(0, str(POC/'mcp_v1'))
from mcp_v1.server import create_server
from mcp_v1.service import LookupService
from mcp_v1.planner import CodexPlanner
from retrieval_repair_v1.integration import Backend
from retrieval_repair_v1.selector import Selector
from wording_candidate_v1.candidate import NormalizingPlanner


def make_service(seed=1701, runtime_dir=None, planner=None, backend_factory=None):
    runtime_dir = Path(runtime_dir) if runtime_dir is not None else HERE/'runtime'
    if planner is None:
        planner = CodexPlanner(runtime_dir/'planner')
    if backend_factory is None:
        backend_factory = lambda: Backend(seed, Selector(runtime_dir/'selector'))
    return LookupService(NormalizingPlanner(planner), backend_factory)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, choices=(1701,1702), default=1701)
    parser.add_argument('--audit-dir', type=Path)
    parser.add_argument('--runtime-dir', type=Path, default=HERE/'runtime')
    args = parser.parse_args()
    create_server(make_service(args.seed,args.runtime_dir),args.audit_dir).run(transport='stdio')

if __name__=='__main__':main()

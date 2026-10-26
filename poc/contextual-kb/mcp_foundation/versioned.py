"""Installed schema2 composition; only the accepted 6.3.12 backend is provisioned."""
from pathlib import Path
from mcp_foundation.service import make_service
from retrieval_repair_v1.selector import Selector
from versioned_knowledge_v1.backend import Backend as CandidateBackend
from versioned_knowledge_v1.context import Context

POC=Path(__file__).resolve().parent.parent

class InstalledBackend(CandidateBackend):
    def validate_database(self):
        if self.dbpath!=(POC/'build/knowledge.sqlite').resolve():
            raise ValueError('Installed backend requires the accepted database path')


def make_context(seed=1701,runtime_dir=None,settings=None):
    runtime=Path(runtime_dir) if runtime_dir is not None else POC/'mcp_foundation/runtime'
    def factory(adapter):
        run=runtime/(adapter or 'default')
        return make_service(seed=seed,runtime_dir=run,backend_factory=lambda:InstalledBackend(
            POC/'build/knowledge.sqlite',seed,adapter,Selector(run/'selector')))
    return Context(factory,settings=settings)

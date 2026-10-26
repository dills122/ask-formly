import sys, unittest, tomllib, tempfile
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from mcp_foundation import launcher
from mcp_v1.service import LookupService

class PromotionTests(unittest.TestCase):
    def test_stable_composition_uses_reviewed_normalizer(self):
        from mcp_foundation.service import make_service
        from mcp_foundation.capitalization import CapitalizingPlanner
        planner=lambda request: ({}, {})
        service=make_service(planner=planner,backend_factory=lambda:None)
        self.assertIsInstance(service,LookupService)
        self.assertIsInstance(service.planner,CapitalizingPlanner)
        self.assertIs(service.planner.planner,planner)

    def test_default_service_uses_qualified_premise_planner(self):
        from mcp_foundation.service import make_service
        from condition_candidate_v2.planner import CodexPlanner
        from mcp_foundation.capitalization import CapitalizingPlanner
        with tempfile.TemporaryDirectory() as directory:
            service=make_service(runtime_dir=directory,backend_factory=lambda:None)
            self.assertIsInstance(service.planner,CapitalizingPlanner)
            self.assertIsInstance(service.planner.planner,CodexPlanner)
            self.assertEqual(service.planner.planner.directory,Path(directory)/'planner')

    def test_stable_launcher_uses_promoted_service(self):
        from mcp_foundation import service
        from types import SimpleNamespace
        sys.path.insert(0,str(HERE.parent/'mcp_v1'))
        import mcp_v1.server
        with tempfile.TemporaryDirectory() as d, patch.object(service,'make_service') as factory, patch('mcp_v1.server.create_server') as server:
            launcher.start(SimpleNamespace(seed=1702,runtime_dir=Path(d),audit_dir=None))
            factory.assert_called_once_with(seed=1702,runtime_dir=Path(d))
            server.return_value.run.assert_called_once_with(transport='stdio')
            self.assertIn('server_ready',(Path(d)/'startup.jsonl').read_text())

    def test_client_requires_startup_and_initial_catalog(self):
        config=tomllib.loads((HERE/'codex.example.toml').read_text())
        self.assertEqual(config['mcp_optional_startup_grace_ms'],0)
        self.assertIs(config['mcp_servers']['formly']['required'],True)

if __name__=='__main__':unittest.main()

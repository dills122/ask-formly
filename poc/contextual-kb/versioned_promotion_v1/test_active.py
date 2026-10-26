import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
POC=Path(__file__).resolve().parent.parent
sys.path[:0]=[str(POC),str(POC/'mcp_v1'),str(POC/'versioned_knowledge_v1')]
import test_compiler
from kbcompiler.current_source import lint_sources,build_sources

class ActiveTests(unittest.TestCase):
    def setUp(self):test_compiler.CompilerTests.setUp(self)
    def test_active_compiler_accepts_v2_and_rejects_legacy_without_installing(self):
        self.assertEqual([],lint_sources(self.new/'authored',self.root,self.cat))
        build_sources(self.new/'authored',self.root,self.cat,self.db)
        self.assertTrue(lint_sources(self.old,self.root,self.catalog))
        with self.assertRaises(FileExistsError):build_sources(self.new/'authored',self.root,self.cat,self.db)
    def test_installed_factory_routes_core_and_default_to_versioned_backend(self):
        from mcp_foundation.versioned import make_context
        context=make_context(runtime_dir=Path(tempfile.gettempdir())/'formly-fixture')
        self.assertEqual('Context',type(context).__name__)
        self.assertEqual('CapitalizingPlanner',type(context.factory('core').planner).__name__)

if __name__=='__main__':unittest.main()

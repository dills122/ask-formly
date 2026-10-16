"""Offline tests of the exact source fixture with a captured real Nx 23 export."""
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from pnpm_nx_contract import REPO,call,verify

class PnpmNxTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'workspace';shutil.copytree(REPO/'tests/fixtures/pnpm-nx-formly',self.root)
        self.ts=os.environ.get('FORMLY_TEST_TYPESCRIPT',str(REPO/'node_modules/typescript/lib/typescript.js'))
    def scan(self):
        call(self.root,'scan','--typescript',self.ts,'--nx-graph','nx-project-graph.json','--project','admin')
        return json.loads((self.root/'.agents/ask-formly/graph.json').read_text())
    def test_entire_flow_crosses_four_libraries_and_excludes_portal(self):
        verify(self.root,self.scan())
    def test_broken_barrel_cannot_false_pass_full_flow_assertions(self):
        (self.root/'libs/forms/src/index.ts').write_text('export {};\n')
        g=self.scan()
        with self.assertRaises(AssertionError):verify(self.root,g)
        self.assertFalse(any(n['name']=='buildSupplierFields' for n in g['nodes']))
    def test_shared_config_changes_invalidate_admin(self):
        self.scan();p=self.root/'libs/form-helpers/src/address.fields.ts';p.write_text(p.read_text().replace("key: 'accountCode'","key: 'changedCode'"))
        self.assertIn('libs/form-helpers/src/address.fields.ts',call(self.root,'check',expected=1)['changes']['changed'])

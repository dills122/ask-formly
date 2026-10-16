"""Reduced public-source patterns expressed using Formly v6 configuration APIs."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / 'skill/ask-formly/scripts/project_index.py'
TS = os.environ.get('FORMLY_TEST_TYPESCRIPT', str(REPO / 'node_modules/typescript/lib/typescript.js'))


class PublicGapTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.write('tsconfig.json', '{"compilerOptions":{"experimentalDecorators":true}}')
        self.write('names.ts', """
            export enum Names { Type = 'account', Wrapper = 'panel', Validator = 'accountCode' }
            export const BASE = 'input';
            export const ALIAS = Names.Type;
        """)
        self.write('custom.ts', 'export class AccountType {} export class Panel {} export const valid = () => true;')

    def write(self, name, text):
        (self.root / name).write_text(text)

    def scan(self):
        result = subprocess.run([sys.executable, str(SCRIPT), 'scan', '--root', str(self.root),
                                 '--typescript', TS], capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.graph = json.loads((self.root / '.agents/ask-formly/graph.json').read_text())
        self.assertEqual(self.graph['mode'], 'typescript-static')
        self.nodes = {n['id']: n for n in self.graph['nodes']}

    def has_edge(self, source, relation, target):
        return any(self.nodes[e['from']]['name'] == source and e['relation'] == relation
                   and self.nodes[e['to']]['name'] == target for e in self.graph['edges'])

    def test_imported_enum_and_const_names_connect_fields_to_registrations(self):
        self.write('setup.ts', """
            import { FormlyModule } from '@ngx-formly/core';
            import { Names, ALIAS } from './names';
            import { AccountType, Panel, valid } from './custom';
            FormlyModule.forRoot({
                types: [{ name: ALIAS, component: AccountType }],
                wrappers: [{ name: Names.Wrapper, component: Panel }],
                validators: [{ name: Names.Validator, validation: valid }]
            });
            const fields = [{ key: 'code', type: Names.Type, wrappers: [Names.Wrapper],
                              validators: { validation: [Names.Validator] } }];
        """)
        self.scan()
        for relation, target in [('type-candidate', 'account'), ('wrapper-candidate', 'panel'),
                                 ('validator-candidate', 'accountCode')]:
            self.assertTrue(self.has_edge('code', relation, target), relation)
        self.assertTrue(self.has_edge('account', 'implementation', 'AccountType'))
        self.assertFalse(any(u['reason'] in ['dynamic-registration-name', 'dynamic-wrapper']
                             for u in self.graph['unresolved']))

    def test_registered_base_type_and_shared_wrapper_list_are_traceable_candidates(self):
        self.write('setup.ts', """
            import { FormlyModule } from '@ngx-formly/core';
            import { Names, BASE } from './names';
            import { AccountType, Panel } from './custom';
            const common = [Names.Wrapper];
            const wrappers = [...common];
            FormlyModule.forRoot({
                types: [{name: 'input', component: AccountType},
                        {name: 'account', extends: BASE, wrappers}],
                wrappers: [{name: 'panel', component: Panel}]
            });
            const fields = [{key: 'code', type: 'account', wrappers}];
        """)
        self.scan()
        self.assertTrue(self.has_edge('account', 'extends-type-candidate', 'input'))
        self.assertTrue(self.has_edge('account', 'wrapper-candidate', 'panel'))
        self.assertTrue(self.has_edge('code', 'wrapper-candidate', 'panel'))
        self.assertTrue(any(u['reason'] == 'registration-inheritance-needs-review' for u in self.graph['unresolved']))
        self.assertTrue(all(e['evidence'] == 'registration-scope-unresolved' for e in self.graph['edges']
                            if e['relation'] in ['extends-type-candidate', 'wrapper-candidate']))

    def test_inheritance_cycles_and_missing_bases_remain_bounded_and_unresolved(self):
        self.write('setup.ts', """
            import { FormlyModule } from '@ngx-formly/core';
            FormlyModule.forRoot({types: [{name:'a', extends:'b'}, {name:'b', extends:'a'},
                                         {name:'missing', extends:'outside'}]});
        """)
        self.scan()
        self.assertTrue(self.has_edge('a', 'extends-type-candidate', 'b'))
        self.assertTrue(self.has_edge('b', 'extends-type-candidate', 'a'))
        self.assertTrue(any(u.get('detail') == 'types:outside' for u in self.graph['unresolved']))
        self.assertFalse(any(n['name'] == 'outside' for n in self.nodes.values()))

    def test_factory_provider_links_imported_implementation_without_evaluating_output(self):
        self.write('factory.ts', """
            import { AccountType } from './custom';
            export const configFactory = () => {
                throw new Error('A source index must never call this factory');
                return {types:[{name:'not-a-proven-registration', component: AccountType}]};
            };
        """)
        self.write('barrel.ts', "export { configFactory as makeConfig } from './factory';")
        self.write('setup.ts', """
            import { FORMLY_CONFIG } from '@ngx-formly/core';
            import { makeConfig } from './barrel';
            export const provider = {provide: FORMLY_CONFIG, multi: true, useFactory: makeConfig};
        """)
        self.scan()
        self.assertTrue(self.has_edge('FORMLY_CONFIG', 'provider-factory', 'configFactory'))
        factory = next(n for n in self.nodes.values() if n['name'] == 'configFactory')
        self.assertEqual(factory['file'], 'factory.ts')
        self.assertTrue(any(u['reason'] == 'dynamic-provider-factory' for u in self.graph['unresolved']))
        self.assertFalse(any(n['kind'] == 'registration' for n in self.nodes.values()))

    def test_inline_factory_has_source_location_but_unresolved_factory_has_no_fake_implementation(self):
        self.write('setup.ts', """
            import { FORMLY_CONFIG } from '@ngx-formly/core';
            import { externalFactory } from 'not-installed';
            const providers = [
                {provide: FORMLY_CONFIG, useFactory: () => ({types:[]})},
                {provide: FORMLY_CONFIG, useFactory: externalFactory}
            ];
        """)
        self.scan()
        links = [e for e in self.graph['edges'] if e['relation'] == 'provider-factory']
        self.assertEqual(len(links), 1)
        self.assertEqual(self.nodes[links[0]['to']]['file'], 'setup.ts')
        self.assertEqual(self.nodes[links[0]['to']]['kind'], 'inline-implementation')
        self.assertEqual(sum(u['reason'] == 'dynamic-provider-factory' for u in self.graph['unresolved']), 2)

    def test_dynamic_names_and_wrapper_lists_are_not_invented(self):
        self.write('setup.ts', """
            import { FormlyModule } from '@ngx-formly/core';
            declare function remote(): any;
            const circular = [ ...circular ];
            FormlyModule.forRoot({types:[{name:remote()}, {name:42},
                {name:'safe', extends:remote(), wrappers:remote()}]});
            const fields = [{key:'dynamic', type:'safe', wrappers:remote()},
                            {key:'cycle', type:'safe', wrappers:circular}];
        """)
        self.scan()
        self.assertEqual({n['name'] for n in self.nodes.values() if n['kind'] == 'registration'}, {'safe'})
        reasons = {u['reason'] for u in self.graph['unresolved']}
        self.assertIn('dynamic-registration-name', reasons)
        self.assertIn('dynamic-wrapper-list', reasons)
        self.assertIn('cyclic-static-array', reasons)
        self.assertFalse(any(e['relation'] == 'extends-type-candidate' for e in self.graph['edges']))


if __name__ == '__main__':
    unittest.main()

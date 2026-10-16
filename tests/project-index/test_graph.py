"""Static graph contract tests against a synthetic app, never an Angular runtime."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / 'skill/ask-formly/scripts/project_index.py'
TS = Path(os.environ.get('FORMLY_TEST_TYPESCRIPT', str(Path(__file__).resolve().parents[2] / 'node_modules/typescript/lib/typescript.js')))

@unittest.skipUnless(TS.is_file(), 'Set FORMLY_TEST_TYPESCRIPT to TypeScript lib/typescript.js')
class GraphTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        sources={
            'tsconfig.json': '{"compilerOptions":{"baseUrl":".","paths":{"@forms/*":["src/forms/*"]},"experimentalDecorators":true}}',
            'src/forms/shared.ts': "export const address = [{ key: 'postcode', type: 'warehouse', wrappers: ['panel'], validators: { validation: ['postcode'] } }];",
            'src/forms/factory.ts': "import { address } from './shared'; export function buildFields() { return [{ key: 'billing', fieldGroup: address }]; }",
            'src/forms/index.ts': "export { buildFields } from './factory';",
            'src/custom.ts': "export class WarehouseType {} export class PanelWrapper {} export function postcode(control: any) { return true; }",
            'src/setup.ts': "import { FormlyModule as FM } from '@ngx-formly/core'; import { WarehouseType, PanelWrapper, postcode } from './custom'; export const root = FM.forRoot({ types: [{ name: 'warehouse', component: WarehouseType }], wrappers: [{ name: 'panel', component: PanelWrapper }], validators: [{ name: 'postcode', validation: postcode }] });",
            'src/feature.ts': "import { FormlyModule } from '@ngx-formly/core'; import { WarehouseType } from './custom'; FormlyModule.forChild({ types: [{ name: 'warehouse', component: WarehouseType }] });",
            'src/screen.ts': "import { Component } from '@angular/core'; import { buildFields } from '@forms/index'; @Component({ selector: 'supplier-screen', templateUrl: './screen.html' }) export class SupplierComponent { fields: any[] = []; ngOnInit() { this.fields = buildFields(); } }",
            'src/screen.html': '<formly-form [fields]="fields" [model]="model"></formly-form>',
            'src/routes.ts': "import { SupplierComponent } from './screen'; export const routes = [{ path: 'supplier', component: SupplierComponent }, { path: 'lazy', loadComponent: () => import('./screen').then(m => m.SupplierComponent) }];",
            'src/dynamic.ts': "import { FormlyModule } from '@ngx-formly/core'; declare function remote(): any; FormlyModule.forChild(remote()); const fields = [{ key: 'x', type: getType() }]; // FormlyModule.forRoot({})\n",
        }
        for name,content in sources.items():
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
    def cli(self,command,*args,code=0):
        run=subprocess.run([sys.executable,str(SCRIPT),command,'--root',str(self.root),*args],capture_output=True,text=True)
        self.assertEqual(run.returncode,code,run.stdout+run.stderr);return json.loads(run.stdout)
    def scan(self):
        self.cli('scan','--typescript',str(TS));self.g=json.loads((self.root/'.agents/ask-formly/graph.json').read_text());self.nodes={n['id']:n for n in self.g['nodes']}
    def edge(self,source,relation,target):
        return any(self.nodes[e['from']]['name']==source and e['relation']==relation and self.nodes[e['to']]['name']==target for e in self.g['edges'])
    def test_connects_screen_initialization_alias_barrel_and_subconfigs(self):
        self.scan();self.assertEqual(self.g['mode'],'typescript-static')
        self.assertTrue(self.edge('supplier','route-component','SupplierComponent'))
        self.assertTrue(self.edge('SupplierComponent','renders','formly-form'))
        self.assertTrue(self.edge('formly-form','binds-fields','fields'))
        self.assertTrue(self.edge('fields','assigned-from','buildFields'))
        self.assertTrue(self.edge('buildFields','contains-field','billing'))
        self.assertTrue(self.edge('billing','references','address'))
        trace=self.cli('trace','--query','SupplierComponent','--depth','8','--limit','100')
        self.assertTrue({'fields','buildFields','address','warehouse','postcode','WarehouseType'}.issubset({n['name'] for n in trace['nodes']}))
        self.assertIn('src/setup.ts',{m['file'] for m in self.cli('find','--query','entry-point')['matches']})
    def test_scoped_duplicate_registrations_and_actual_implementation_locations(self):
        self.scan();registrations=[n for n in self.g['nodes'] if n['kind']=='registration' and n['name']=='warehouse']
        self.assertEqual(len(registrations),2);self.assertEqual({n['file'] for n in registrations},{'src/setup.ts','src/feature.ts'})
        self.assertTrue(self.edge('warehouse','implementation','WarehouseType'))
        self.assertTrue(self.edge('postcode','implementation','postcode'))
        self.assertTrue(any(e['relation']=='type-candidate' and e['evidence']=='registration-scope-unresolved' for e in self.g['edges']))
        modes={n.get('registration_mode') for n in self.g['nodes'] if n['kind']=='entry-point'}
        self.assertEqual(modes,{'forRoot','forChild'})
    def test_dynamic_and_template_ambiguity_are_reported_not_invented(self):
        p=self.root/'src/screen.html';p.write_text('<formly-form [fields]="service.getFields()"></formly-form>')
        self.scan();reasons={u['reason'] for u in self.g['unresolved']}
        self.assertIn('dynamic-registration-config',reasons);self.assertIn('dynamic-field-type',reasons);self.assertIn('complex-template-binding',reasons)
        self.assertEqual(len([n for n in self.g['nodes'] if n['kind']=='entry-point']),3)
        self.assertTrue(any(e['relation']=='lazy-import' and self.nodes[e['to']]['file']=='src/screen.ts' for e in self.g['edges']))
    def test_graph_tampering_invalidates_freshness_and_note_attestation(self):
        self.scan();p=self.root/'.agents/ask-formly/graph.json';p.write_text('{}')
        self.assertEqual(self.cli('check',code=1)['status'],'stale')
        note=self.root/'review.md';note.write_text('Reviewed source')
        self.cli('note','--id','project','--input',str(note),'--source','src/screen.ts',code=2)
    def test_provider_unkeyed_group_inline_validator_and_reusable_component(self):
        (self.root/'src/provider.ts').write_text("import { FORMLY_CONFIG } from '@ngx-formly/core'; import { WarehouseType } from './custom'; const config = { types: [{name: 'other', component: WarehouseType}] }; export const provider = { provide: FORMLY_CONFIG, useValue: config, multi: true };")
        (self.root/'src/forms/groups.ts').write_text("import { address } from './shared'; export const grouped = [{fieldGroup: address}, {key: 'confirm', validators: {same: {expression: () => true}}}];")
        (self.root/'src/parent.ts').write_text("import { Component } from '@angular/core'; @Component({selector: 'parent-screen', template: '<supplier-screen></supplier-screen>'}) export class ParentComponent {}")
        self.scan()
        self.assertTrue(self.edge('FORMLY_CONFIG','registers','other'))
        self.assertTrue(self.edge('(unkeyed group)','references','address'))
        self.assertTrue(self.edge('confirm','validates-with','same'))
        self.assertTrue(self.edge('ParentComponent','component-selector-candidate','SupplierComponent'))
    def test_500_form_graph_is_searchable_and_bounded(self):
        for i in range(500):
            (self.root/f'src/forms/form{i}.ts').write_text(f"export const form{i} = [{{key: 'name', type: 'warehouse'}}];")
        self.scan();trace=self.cli('trace','--query','form','--limit','7','--depth','3')
        self.assertGreaterEqual(trace['seed_matches'],500);self.assertLessEqual(len(trace['nodes']),7)
        self.assertTrue(trace['truncated'])
    def test_shared_registration_object_keeps_each_registration_scope(self):
        (self.root/'src/shared-registry.ts').write_text("import { WarehouseType } from './custom'; export const cfg = {types: [{name:'shared', component: WarehouseType}]};")
        for name,mode in [('a','forRoot'),('b','forChild')]:
            (self.root/f'src/{name}.ts').write_text(f"import {{FormlyModule}} from '@ngx-formly/core'; import {{cfg}} from './shared-registry'; FormlyModule.{mode}(cfg);")
        self.scan();regs=[n for n in self.g['nodes'] if n['kind']=='registration' and n['name']=='shared']
        self.assertEqual(len(regs),2);self.assertEqual(len({n['scope'] for n in regs}),2)
    def test_inline_assignment_links_bound_member_to_field_config(self):
        (self.root/'src/screen.ts').write_text("import { Component } from '@angular/core'; @Component({templateUrl: './screen.html'}) export class SupplierComponent {fields: any[]; ngOnInit(){this.fields = [{key: 'customer', type: 'warehouse'}];}}")
        self.scan();self.assertTrue(self.edge('fields','assigned-from','customer'))
        trace=self.cli('trace','--query','SupplierComponent','--depth','5','--limit','40')
        self.assertIn('customer',{n['name'] for n in trace['nodes']})
    def test_registration_spreads_follow_property_replacement(self):
        (self.root/'src/spread.ts').write_text("import {FormlyModule} from '@ngx-formly/core'; import {WarehouseType} from './custom'; const base={types:[{name:'old',component:WarehouseType}],wrappers:[{name:'kept',component:WarehouseType}]}; FormlyModule.forRoot({...base, types:[{name:'active', component:WarehouseType}]});")
        self.scan();names={n['name'] for n in self.g['nodes'] if n['kind']=='registration'}
        self.assertIn('active',names);self.assertIn('kept',names);self.assertNotIn('old',names)
    def test_keyless_types_and_array_items_remain_connected(self):
        (self.root/'src/forms/keyless.ts').write_text("export const fields=[{type:'warehouse'},{key:'tags',fieldArray:{type:'warehouse'}}];")
        self.scan();configs=[n for n in self.g['nodes'] if n['kind']=='field-config' and n['file']=='src/forms/keyless.ts']
        self.assertEqual(len(configs),3)
        self.assertTrue(any(e['relation']=='contains-field' and self.nodes[e['from']]['name']=='tags' and self.nodes[e['to']]['kind']=='field-config' for e in self.g['edges']))
    def test_shorthand_registration_list_and_implementation_references(self):
        (self.root/'src/shorthand.ts').write_text("import {FormlyModule} from '@ngx-formly/core'; import {postcode as validation} from './custom'; const validators=[{name:'short',validation}]; FormlyModule.forRoot({validators});")
        self.scan();self.assertTrue(self.edge('short','implementation','postcode'))

if __name__=='__main__':unittest.main()

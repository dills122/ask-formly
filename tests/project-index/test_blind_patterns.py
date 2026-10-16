#!/usr/bin/env python3
"""Blind static-scanner expectations. Generated fixtures use disposable temporary directories.
FORMLY_SCANNER may select another project_index.py. Converted to portable regression tests after the independent audit.
"""
import json, os, pathlib, subprocess, tempfile, unittest
REPO = pathlib.Path(__file__).resolve().parents[2]
SCANNER = os.environ.get('FORMLY_SCANNER', str(REPO/'skill/ask-formly/scripts/project_index.py'))
TS = os.environ.get('FORMLY_TEST_TYPESCRIPT', str(REPO/'node_modules/typescript/lib/typescript.js'))
HEADER = """import { Component } from '@angular/core';
import { FormlyModule, FORMLY_CONFIG, FieldType, FieldWrapper } from '@ngx-formly/core';
class OldType extends FieldType {};
class NewType extends FieldType {};
class Panel extends FieldWrapper {};
"""
def scan(name, code):
    with tempfile.TemporaryDirectory(prefix='formly-blind-') as directory:
        return scan_at(pathlib.Path(directory), code)

def scan_at(root, code):
    (root/'package.json').write_text(json.dumps({'private':True,'dependencies':{'@ngx-formly/core':'6.3.12','@angular/core':'21.2.25'}}))
    (root/'tsconfig.json').write_text(json.dumps({'compilerOptions':{'experimentalDecorators':True},'include':['app.ts']}))
    (root/'app.ts').write_text(HEADER+code)
    run = subprocess.run(['python3',SCANNER,'scan','--root',str(root),'--typescript',TS],capture_output=True,text=True)
    if run.returncode: raise RuntimeError(run.stdout+run.stderr)
    return json.loads((root/'.agents/ask-formly/graph.json').read_text())
def regs(g): return [n for n in g['nodes'] if n['kind']=='registration']
def edges(g, relation): return [e for e in g['edges'] if e['relation']==relation]
class BlindCases(unittest.TestCase):
    def test_control(self):
        g=scan('control',"""
FormlyModule.forRoot({types:[{name:'custom',component:OldType}],wrappers:[{name:'panel',component:Panel}]});
@Component({selector:'app-root',template:'<formly-form [fields]="fields"></formly-form>'})
class Screen { fields=[{key:'x',type:'custom',wrappers:['panel']}]; }
""")
        self.assertEqual({'custom','panel'},{n['name'] for n in regs(g)})
        self.assertEqual(1,len(edges(g,'binds-fields')))
        self.assertEqual(1,len(edges(g,'type-candidate')))
        self.assertEqual(1,len(edges(g,'wrapper-candidate')))
    def test_registration_item_spread_precedence(self):
        g=scan('registration-item-spread',"""
const replacement = {name:'real',component:NewType};
FormlyModule.forRoot({types:[{name:'obsolete',component:OldType,...replacement}]});
""")
        self.assertEqual(['real'],[n['name'] for n in regs(g)],'Static spread must replace obsolete registration name')
        targets={n['id']:n['name'] for n in g['nodes']}
        self.assertEqual(['NewType'],[targets[e['to']] for e in edges(g,'implementation')])
    def test_unknown_registration_item_spread(self):
        g=scan('unknown-item-spread',"""
declare function overrides(): object;
FormlyModule.forRoot({types:[{name:'possibly-obsolete',component:OldType,...overrides()}]});
""")
        self.assertFalse(regs(g),'Unknown spread can override name/component; do not assert static registration')
        self.assertTrue(any('registration' in i['reason'] for i in g['unresolved']))
    def test_shadowed_module_is_not_registration(self):
        g=scan('shadowed-module',"""
function customRegistry(FormlyModule: {forRoot(x:unknown):unknown}) {
  return FormlyModule.forRoot({types:[{name:'not-formly',component:OldType}]});
}
""")
        self.assertFalse(regs(g),'Parameter shadows FormlyModule import')
    def test_shadowed_token_is_not_provider(self):
        g=scan('shadowed-token',"""
function customProvider(FORMLY_CONFIG: unknown) {
 return {provide:FORMLY_CONFIG,useValue:{types:[{name:'not-formly',component:OldType}]}};
}
""")
        self.assertFalse(regs(g),'Parameter shadows FORMLY_CONFIG import')
    def test_field_spread_precedence(self):
        g=scan('field-spread',"""
FormlyModule.forRoot({types:[{name:'old',component:OldType},{name:'new',component:NewType}]});
const replacement={type:'new'};
@Component({selector:'app-root',template:'<formly-form [fields]="fields"></formly-form>'})
class Screen { fields=[{key:'x',type:'old',...replacement}]; }
""")
        byid={n['id']:n for n in g['nodes']}
        actual=[byid[e['to']]['name'] for e in edges(g,'type-candidate') if byid[e['from']]['name']=='x']
        self.assertEqual(['new'],actual)
    def test_template_local_does_not_bind_member(self):
        g=scan('template-local',"""
@Component({selector:'app-root',template:'<ng-template let-fields><formly-form [fields]="fields"></formly-form></ng-template>'})
class Screen { fields=[{key:'unrelated',type:'input'}]; }
""")
        self.assertFalse(edges(g,'binds-fields'),'Template-local fields shadows component member; decline or flag unresolved')
    def test_namespace_import_registration(self):
        g=scan('namespace-import',"""
import * as formly from '@ngx-formly/core';
formly.FormlyModule.forRoot({types:[{name:'namespaced',component:OldType}]});
""")
        self.assertEqual(['namespaced'],[n['name'] for n in regs(g)])
    def test_validator_spread_array(self):
        g=scan('validator-array-spread',"""
function postal(c:unknown) {return null;}
FormlyModule.forRoot({validators:[{name:'postal',validation:postal}]});
const common=['postal'];
const fields=[{key:'zip',type:'input',validators:{validation:[...common]}}];
""")
        self.assertEqual(1,len(edges(g,'validator-candidate')),'Spread in static validation array has same meaning as inline element')
    def test_known_top_level_spread_control(self):
        g=scan('top-spread-control',"""
const replacement={types:[{name:'new',component:NewType}]};
FormlyModule.forRoot({types:[{name:'old',component:OldType}],...replacement});
""")
        self.assertEqual(['new'],[n['name'] for n in regs(g)])
    def test_unknown_top_level_spread_control(self):
        g=scan('top-unknown-control',"""
declare function overrides():object;
FormlyModule.forRoot({types:[{name:'old',component:OldType}],...overrides()});
""")
        self.assertFalse(regs(g))
        self.assertTrue(any(i['reason']=='dynamic-registration-config' for i in g['unresolved']))
    def test_unknown_field_spread_does_not_keep_obsolete_type(self):
        g=scan('unknown-field-spread', """
declare function overrides():object;
FormlyModule.forRoot({types:[{name:'old',component:OldType}]});
const fields=[{key:'x',type:'old',...overrides()}];
""")
        self.assertFalse(edges(g,'type-candidate'))
        self.assertTrue(any(i['reason']=='dynamic-field-config' for i in g['unresolved']))

    def test_spread_only_registration_and_overridden_field_key(self):
        g=scan('spread-only-registration', """
const registration={name:'new',component:NewType};
const replacement={key:'newKey',type:'new'};
FormlyModule.forRoot({types:[{...registration}]});
const fields=[{key:'oldKey',type:'old',...replacement}];
""")
        self.assertEqual(['new'],[n['name'] for n in regs(g)])
        nodes={n['id']:n for n in g['nodes']}
        self.assertTrue(any(nodes[e['from']]['name']=='newKey' and nodes[e['to']]['name']=='new'
                            for e in edges(g,'type-candidate')))
        self.assertFalse(any(n['name']=='oldKey' for n in g['nodes']))

    def test_namespace_tokens_are_resolved_but_shadowed_namespace_is_not(self):
        g=scan('namespace-shadow', """
import * as f from '@ngx-formly/core';
const provider={provide:f.FORMLY_CONFIG,useValue:{types:[{name:'real',component:NewType}]}};
function local(f:any) { return f.FormlyModule.forRoot({types:[{name:'fake',component:OldType}]}); }
""")
        self.assertEqual(['real'],[n['name'] for n in regs(g)])

    def test_template_locals_are_conservative_but_explicit_this_still_binds(self):
        for prefix in ['@let fields = other;', '@for (fields of forms; track fields) {',
                       '<div *ngFor="let fields of forms">', '<div *ngIf="other as fields">',
                       '<ng-template #fields>']:
            with self.subTest(prefix=prefix):
                code='@Component({template:`'+prefix+'<formly-form [fields]="fields" />`}) class Screen {fields=[];}'
                g=scan('local-variants',code)
                self.assertFalse(edges(g,'binds-fields'))
                self.assertTrue(any(i['reason']=='template-local-binding-needs-review' for i in g['unresolved']))
        g=scan('explicit-this', '''
@Component({template:'<ng-template let-fields><formly-form [fields]="this.fields" /></ng-template>'})
class Screen {fields=[];}
''')
        self.assertEqual(1,len(edges(g,'binds-fields')))

    def test_unknown_validator_spread_retains_known_entries_and_reports_gap(self):
        g=scan('unknown-validator-spread', """
declare function remote():any[];
function inline(c:unknown) {return null;}
FormlyModule.forRoot({validators:[{name:'postal',validation:inline}]});
const common=['postal',inline];
const fields=[{key:'zip',validators:{validation:[...common,...remote()]}}];
""")
        self.assertEqual(1,len(edges(g,'validator-candidate')))
        self.assertEqual(1,len(edges(g,'validator-function')))
        self.assertTrue(any(i['reason']=='dynamic-validator-list' for i in g['unresolved']))

    def test_nested_validator_object_obeys_spreads_and_duplicate_property_order(self):
        for validators in ["{validation:['old'],...replacement}", "{validation:['old'],validation:['new']}"]:
            with self.subTest(validators=validators):
                g=scan('nested-validators', """
function check(c:unknown) {return null;}
FormlyModule.forRoot({validators:[{name:'old',validation:check},{name:'new',validation:check}]});
const replacement={validation:['new']};
const fields=[{key:'x',validators:"""+validators+"""}];
""")
                nodes={n['id']:n for n in g['nodes']}
                self.assertEqual(['new'],[nodes[e['to']]['name'] for e in edges(g,'validator-candidate')])

    def test_unknown_validator_object_spread_does_not_assert_obsolete_validation(self):
        g=scan('unknown-validator-object', """
declare function remote():any;
function check(c:unknown) {return null;}
FormlyModule.forRoot({validators:[{name:'old',validation:check}]});
const fields=[{key:'x',validators:{validation:['old'],...remote()}}];
""")
        self.assertFalse(edges(g,'validator-candidate'))
        self.assertTrue(any(i['reason']=='dynamic-validator-config' for i in g['unresolved']))

    def test_provider_spreads_respect_effective_token_and_unknown_overrides(self):
        for override in ["{provide:'OTHER'}", 'remote()']:
            with self.subTest(override=override):
                g=scan('provider-override', """
declare function remote():any;
const replacement="""+override+""";
const provider={provide:FORMLY_CONFIG,useValue:{types:[{name:'fake',component:OldType}]},...replacement};
""")
                self.assertFalse(regs(g))
                if override=='remote()':
                    self.assertTrue(any(i['reason']=='dynamic-provider-config' for i in g['unresolved']))
        for provider in ['{...base}', "{provide:'OTHER',...base}"]:
            with self.subTest(provider=provider):
                g=scan('provider-spread-positive', """
const base={provide:FORMLY_CONFIG,useValue:{types:[{name:'real',component:NewType}]}};
const provider="""+provider+";\n")
                self.assertTrue(regs(g))
                self.assertEqual({'real'},{n['name'] for n in regs(g)})
                self.assertEqual(2,len(regs(g)))

    def test_shared_registration_object_keeps_category_and_scope_identity(self):
        g=scan('shared-categories', """
const shared={name:'common',component:Panel};
const config={types:[shared],wrappers:[shared]};
FormlyModule.forRoot(config); FormlyModule.forChild(config);
const fields=[{key:'x',type:'common',wrappers:['common']}];
""")
        self.assertEqual(4,len(regs(g)))
        self.assertEqual({'types','wrappers'},{n['category'] for n in regs(g)})
        self.assertEqual(2,len({n['scope'] for n in regs(g)}))
        nodes={n['id']:n for n in g['nodes']}
        for relation,category in [('type-candidate','types'),('wrapper-candidate','wrappers')]:
            self.assertEqual(2,len(edges(g,relation)))
            self.assertTrue(all(nodes[e['to']]['category']==category for e in edges(g,relation)))

    def test_unknown_spread_over_inherited_provider_token_reports_uncertainty(self):
        for composed in ['{...base,...remote()}', '{...remote(),...base}']:
            with self.subTest(composed=composed):
                g=scan('inherited-provider-unknown', """
declare function remote():any;
const base={provide:FORMLY_CONFIG,useValue:{types:[{name:'base',component:OldType}]}};
const provider="""+composed+";\n")
                self.assertEqual(['base'],[n['name'] for n in regs(g)])
                self.assertTrue(any(i['reason']=='dynamic-provider-config' for i in g['unresolved']))
        unrelated=scan('unrelated-unknown-spread', """
declare function remote():any;
const object={name:'ordinary',...remote()};
""")
        self.assertFalse(regs(unrelated))
        self.assertFalse(any('provider' in i['reason'] for i in unrelated['unresolved']))

if __name__=='__main__': unittest.main(verbosity=2)

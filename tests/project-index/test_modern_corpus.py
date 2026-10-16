"""Static navigation regressions reduced from the pinned public corpus."""
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


class ModernCorpusTests(unittest.TestCase):
    def scan(self, source):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = temporary.name
        directory = self.root
        root = Path(directory)
        (root / 'tsconfig.json').write_text('{"compilerOptions":{"experimentalDecorators":true}}')
        (root / 'app.ts').write_text(source)
        result = subprocess.run([sys.executable, str(SCRIPT), 'scan', '--root', directory,
                                 '--typescript', TS], capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        graph = json.loads((root / '.agents/ask-formly/graph.json').read_text())
        self.assertEqual(graph['mode'], 'typescript-static')
        self.graph = graph
        self.nodes = {node['id']: node for node in graph['nodes']}

    def links(self, relation):
        return [(self.nodes[e['from']]['name'], self.nodes[e['to']]['name'])
                for e in self.graph['edges'] if e['relation'] == relation]

    def test_modern_providers_alias_namespace_arrays_and_shadowing(self):
        self.scan("""
            import {provideFormlyCore as core, provideFormlyConfig} from '@ngx-formly/core';
            import * as F from '@ngx-formly/core';
            import {provideFormlyCore as foreign} from 'another-library';
            class Input {}
            const base = {types: [{name:'input', component:Input}]};
            core([base, {wrappers:[{name:'panel', component:Input}]}]);
            F.provideFormlyConfig({validators:[{name:'valid', validation:()=>true}]});
            provideFormlyConfig();
            foreign({types:[{name:'foreign-fake'}]});
            function shadow(core:any) { core({types:[{name:'fake'}]}); }
            function other() { const provideFormlyConfig = (x:any)=>x;
              provideFormlyConfig({types:[{name:'fake2'}]}); }
        """)
        registrations = {n['name'] for n in self.nodes.values() if n['kind'] == 'registration'}
        self.assertEqual(registrations, {'input', 'panel', 'valid'})
        self.assertIn(('input', 'Input'), self.links('implementation'))
        self.assertEqual(len([n for n in self.nodes.values() if n['kind'] == 'entry-point']), 3)

    def test_factory_argument_is_navigation_only(self):
        self.scan("""
            import {provideFormlyCore} from '@ngx-formly/core';
            function makeConfig() { throw Error('must never execute');
              return {types:[{name:'not-proven'}]}; }
            provideFormlyCore(makeConfig() as any);
        """)
        self.assertIn(('provideFormlyCore', 'makeConfig'), self.links('config-factory'))
        self.assertFalse(any(n['kind'] == 'registration' for n in self.nodes.values()))
        self.assertTrue(any(u['reason'] == 'dynamic-registration-config' for u in self.graph['unresolved']))

    def test_signal_and_async_bindings_are_source_pointers(self):
        self.scan('''
            import {Component, computed} from '@angular/core';
            @Component({template: `<formly-form [fields]="fields()"></formly-form>
              <formly-form [fields]="fields$ | async"></formly-form>
              <formly-field [field]="this.field()"></formly-field>
              <formly-form [fields]="plain"></formly-form>`})
            class Example { fields = computed(()=>[{key:'name',type:'input'}]);
              fields$ = stream; field() { return {}; } plain = []; }
        ''')
        self.assertEqual(self.links('binds-fields-source'),
                         [('formly-form', 'fields'), ('formly-form', 'fields$'), ('formly-field', 'field')])
        self.assertEqual(self.links('binds-fields'), [('formly-form', 'plain')])
        self.assertTrue(all(e['evidence'] == 'runtime-value-unresolved' for e in self.graph['edges']
                            if e['relation'] == 'binds-fields-source'))
        self.assertTrue(any(u['reason'] == 'template-value-needs-review' for u in self.graph['unresolved']))

    def test_local_shadows_arguments_and_nested_expressions_stay_unresolved(self):
        self.scan('''
            import {Component} from '@angular/core';
            @Component({template: `<ng-template let-fields>
              <formly-form [fields]="fields()"></formly-form>
              <formly-form [fields]="this.fields()"></formly-form>
              <formly-form [fields]="fields(1)"></formly-form>
              <formly-form [fields]="service.fields()"></formly-form>
              <formly-form [fields]="missing$ | async"></formly-form></ng-template>`})
            class Example { fields() { return []; } }
        ''')
        self.assertEqual(self.links('binds-fields-source'), [('formly-form', 'fields')])
        reasons = {u['reason'] for u in self.graph['unresolved']}
        self.assertTrue({'template-local-binding-needs-review', 'complex-template-binding',
                         'template-member-unresolved'} <= reasons)

    def test_relation_filtered_trace_preserves_form_chain_and_reports_scope(self):
        self.scan('''
            import {Component} from '@angular/core';
            @Component({template: `<formly-form [fields]="fields"></formly-form>`})
            class Example { fields = [{key:'name',type:'input'}];
              unrelated1() {} unrelated2() {} unrelated3() {} unrelated4() {} }
        ''')
        command = [sys.executable, str(SCRIPT), 'trace', '--root', self.root,
                   '--query', 'Example', '--limit', '4', '--depth', '4']
        normal = subprocess.run(command, capture_output=True, text=True)
        self.assertTrue(json.loads(normal.stdout)['truncated'])
        relations = ['renders', 'binds-fields', 'contains-field']
        filtered = subprocess.run(command + [arg for relation in relations
                                             for arg in ['--relation', relation]],
                                  capture_output=True, text=True)
        self.assertEqual(filtered.returncode, 0, filtered.stdout + filtered.stderr)
        result = json.loads(filtered.stdout)
        self.assertEqual({n['name'] for n in result['nodes']}, {'Example', 'formly-form', 'fields', 'name'})
        self.assertFalse(result['truncated'])
        self.assertEqual(result['relations'], relations)
        self.assertTrue(result['relation_filtered'])
        self.assertTrue(all(e['relation'] in relations for e in result['edges']))

        inward = subprocess.run([sys.executable, str(SCRIPT), 'trace', '--root', self.root,
                                  '--query', 'fields', '--direction', 'in', '--depth', '1',
                                  '--relation', 'binds-fields'], capture_output=True, text=True)
        self.assertEqual(inward.returncode, 0, inward.stderr)
        self.assertEqual({n['name'] for n in json.loads(inward.stdout)['nodes']}, {'fields', 'formly-form'})
        shallow = subprocess.run(command + ['--depth', '1', '--relation', 'renders',
                                             '--relation', 'binds-fields'], capture_output=True, text=True)
        self.assertTrue(json.loads(shallow.stdout)['truncated'])
        invalid = subprocess.run([sys.executable, str(SCRIPT), 'find', '--root', self.root,
                                  '--relation', 'renders'], capture_output=True, text=True)
        self.assertEqual(invalid.returncode, 2)

"""Workspace contracts with real TypeScript resolution; no application execution."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/'skill/ask-formly/scripts/project_index.py'
TS=Path(os.environ.get('FORMLY_TEST_TYPESCRIPT',ROOT/'node_modules/typescript/lib/typescript.js'))

class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
    def put(self,name,value):
        p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(value if isinstance(value,str) else json.dumps(value));return p
    def cli(self,command,*args,code=0):
        run=subprocess.run([sys.executable,str(SCRIPT),command,'--root',str(self.root),*args],text=True,capture_output=True)
        self.assertEqual(run.returncode,code,run.stdout+run.stderr);return json.loads(run.stdout)
    def scan(self,*args):
        self.cli('scan','--typescript',str(TS),*args)
        self.g=json.loads((self.root/'.agents/ask-formly/graph.json').read_text());self.assertEqual(self.g['mode'],'typescript-static',self.g)
        self.nodes={n['id']:n for n in self.g['nodes']};return self.g
    def links(self,context):
        return {(self.nodes[e['from']]['file'],self.nodes[e['to']]['file']) for e in self.g['edges'] if e['relation']=='imports' and e['context']==context}
    def multi(self):
        projects={}
        for name,directory in [('admin','products/admin'),('portal','clients/portal')]:
            projects[name]={'root':directory,'architect':{'build':{'options':{'tsConfig':directory+'/compile.json'}}}}
            self.put(directory+'/compile.json',{'extends':'../../tsconfig.base.json','include':['src/*.ts'],'exclude':['src/*.spec.ts'],**({'compilerOptions':{'paths':{'@fields':['shared/forms/admin.ts']}}} if name=='admin' else {})})
            self.put(directory+'/src/screen.ts',"import { fields } from '@fields'; export const selected=fields;")
        projects['admin']['architect']['build']['configurations']={'production':{'tsConfig':'products/admin/prod.json'}}
        projects['forms']={'root':'shared/forms','projectType':'library'}
        self.put('angular.json',{'version':1,'projects':projects})
        self.put('products/admin/prod.json',{'extends':'./compile.json','compilerOptions':{'paths':{'@fields':['shared/forms/prod.ts']}}})
        self.put('tsconfig.base.json',{'compilerOptions':{'baseUrl':'.','paths':{'@fields':['shared/forms/default.ts']}}})
        self.put('products/admin/src/screen.spec.ts',"export const specOnly=[{key:'test',type:'input'}];")
        for name in ['admin','default','prod']:self.put('shared/forms/'+name+'.ts',f"export const fields=[{{key:'{name}',type:'input'}}];")
    def test_single_root_application_jsonc_and_arbitrary_config_name(self):
        self.put('angular.json','{/*comment*/"projects":{"app":{"root":"","sourceRoot":"src","architect":{"build":{"options":{"tsConfig":"config/application.json"}}}}},}')
        self.put('config/application.json',{'include':['../src/*.ts']});self.put('src/form.ts',"export const f=[{key:'x',type:'input'}];")
        g=self.scan();self.assertEqual(g['workspace']['kind'],'angular');self.assertEqual(g['workspace']['projects'][0]['root'],'.')
        self.assertEqual({n['context'] for n in g['nodes'] if n['kind']=='field-config'},{'config/application.json'})
    def test_multi_project_aliases_build_variants_and_excludes(self):
        self.multi();g=self.scan()
        for context,target in [('products/admin/compile.json','admin'),('products/admin/prod.json','prod'),('clients/portal/compile.json','default')]:
            self.assertIn((context.rsplit('/',1)[0]+'/src/screen.ts','shared/forms/'+target+'.ts'),self.links(context))
        self.assertNotIn(('products/admin/src/screen.ts','shared/forms/default.ts'),self.links('products/admin/compile.json'))
        self.assertTrue(all(n['context'].startswith('unconfigured:') for n in g['nodes'] if n['file'].endswith('screen.spec.ts')))
        self.assertFalse(any(c['id']=='tsconfig.base.json' for c in g['contexts']))
    def test_project_selection_preserves_shared_imports_and_file_ownership(self):
        self.multi();g=self.scan('--project','admin')
        self.assertNotIn('portal',{p for n in g['nodes'] for p in n['projects']})
        self.assertTrue(any(n['projects']==['forms'] and n['context']=='products/admin/compile.json' for n in g['nodes']))
        self.assertEqual(g['workspace']['selectedProjects'],['admin']);self.cli('scan')
        self.assertEqual(json.loads((self.root/'.agents/ask-formly/config.json').read_text())['projects'],['admin'])
    def test_reference_closure_arbitrary_names_and_array_extends(self):
        self.put('tsconfig.json',{'files':[],'references':[{'path':'modules/forms/compile.json'}]})
        self.put('config/one.json',{'compilerOptions':{'baseUrl':'..','paths':{'@helper':['shared/helper.ts']}}})
        self.put('config/two.json',{'compilerOptions':{'strict':True}})
        self.put('modules/forms/compile.json',{'extends':['../../config/one.json','../../config/two.json'],'include':['src/*.ts']})
        self.put('modules/forms/src/form.ts',"import { helper } from '@helper'; export const fields=helper;")
        self.put('shared/helper.ts',"export const helper=[{key:'shared',type:'input'}];")
        g=self.scan();self.assertIn(('modules/forms/src/form.ts','shared/helper.ts'),self.links('modules/forms/compile.json'))
        self.assertEqual(g['workspace']['configs'][0]['references'],['modules/forms/compile.json'])
    def test_nx_static_fallback_cannot_claim_plugin_resolution(self):
        self.put('nx.json',{'plugins':['./danger.cjs']});self.put('danger.cjs',"require('fs').writeFileSync('EXECUTED','bad');")
        self.put('arbitrary/admin/project.json',{'name':'admin'});self.put('packages/forms/package.json',{'name':'@test/forms','nx':{}})
        self.put('arbitrary/admin/form.ts',"export const f=[{key:'x',type:'input'}];")
        g=self.scan();self.assertEqual(g['workspace']['mode'],'static-candidates')
        self.assertEqual({p['name'] for p in g['workspace']['projects']},{'admin','@test/forms'})
        self.assertIn('nx-resolved-project-graph-required',{i['reason'] for i in g['unresolved']});self.assertFalse((self.root/'EXECUTED').exists())
    def test_nx_export_projects_targets_dependencies_and_freshness(self):
        self.put('nx.json',{'plugins':['not-installed']})
        self.put('packages/admin/src/form.ts',"import { fields } from '@forms'; export const use=fields;")
        self.put('packages/forms/src/index.ts',"export const fields=[{key:'x',type:'input'}];")
        self.put('packages/admin/tsconfig.app.json',{'include':['src/*.ts'],'compilerOptions':{'baseUrl':'../..','paths':{'@forms':['packages/forms/src/index.ts']}}})
        data={'graph':{'nodes':{'admin':{'type':'app','data':{'root':'packages/admin','targets':{'build':{'options':{'tsConfig':'{projectRoot}/tsconfig.app.json'}}}}},'forms':{'type':'lib','data':{'root':'packages/forms'}}},'dependencies':{'admin':[{'source':'admin','target':'forms','type':'static'}]}}}
        p=self.put('.agents/ask-formly/nx-project-graph.json',data)
        g=self.scan('--nx-graph','.agents/ask-formly/nx-project-graph.json','--project','admin')
        self.assertEqual(g['workspace']['mode'],'exported-graph');self.assertEqual(g['workspace']['dependencies']['admin'][0]['target'],'forms')
        self.assertIn(('packages/admin/src/form.ts','packages/forms/src/index.ts'),self.links('packages/admin/tsconfig.app.json'))
        self.assertEqual(self.cli('check')['status'],'fresh');p.write_text(json.dumps(data,indent=4));self.assertEqual(self.cli('check',code=1)['status'],'stale')
    def test_package_extends_changes_invalidate_notes_even_after_rescan(self):
        self.put('tsconfig.json',{'extends':'@test/tsconfig/base.json','include':['src/*.ts']})
        self.put('node_modules/@test/tsconfig/package.json',{'name':'@test/tsconfig','main':'evil.cjs'})
        self.put('node_modules/@test/tsconfig/evil.cjs',"throw new Error('package executed');")
        base=self.put('node_modules/@test/tsconfig/base.json',{'compilerOptions':{'strict':True}})
        self.put('src/form.ts',"export const f=[{key:'x',type:'input'}];")
        g=self.scan();self.assertIn('node_modules/@test/tsconfig/base.json',g['resolution_inputs']);self.assertEqual(self.cli('check')['status'],'fresh')
        note=self.put('review.md','Source-reviewed');self.cli('note','--id','form','--input',str(note),'--source','src/form.ts')
        base.write_text('{"compilerOptions":{"strict":false}}');r=self.cli('check',code=1)
        self.assertFalse(r['resolution_inputs_current']);self.assertEqual(r['notes']['form'],'needs-review')
        self.cli('scan');self.assertEqual(self.cli('check',code=1)['notes']['form'],'needs-review')
    def test_missing_package_config_installation_invalidates_index(self):
        self.put('tsconfig.json',{'extends':'@test/tsconfig/base.json','include':['src/*.ts']});self.put('src/form.ts','export const f=[];')
        g=self.scan();self.assertIn('tsconfig-error',{i['reason'] for i in g['unresolved']})
        self.put('node_modules/@test/tsconfig/base.json',{'compilerOptions':{'strict':True}});self.assertEqual(self.cli('check',code=1)['status'],'stale')
    def test_scope_omission_remains_explicit(self):
        self.multi();g=self.scan('--scope','products/admin','--project','admin')
        self.assertIn('import-outside-index-or-unresolved',{i['reason'] for i in g['unresolved']})
    def test_invalid_workspace_paths_and_missing_configs(self):
        self.put('angular.json',{'projects':{'bad':{'root':'../outside'},'app':{'root':'','architect':{'build':{'options':{'tsConfig':'missing.json'}}}}}})
        self.put('form.ts','export const f=[];');g=self.scan()
        self.assertTrue({'invalid-workspace-path','tsconfig-outside-index'}.issubset({i['reason'] for i in g['unresolved']}))
    def test_reference_cycles_terminate_with_evidence(self):
        self.put('tsconfig.json',{'files':[],'references':[{'path':'nested/tsconfig.json'}]});self.put('nested/tsconfig.json',{'references':[{'path':'..'}]});self.put('nested/form.ts','export const f=[];')
        g=self.scan();self.assertIn('tsconfig-reference-cycle',{i['reason'] for i in g['unresolved']})
    def test_explicit_config_selection(self):
        self.multi();g=self.scan('--tsconfig','products/admin/compile.json')
        self.assertEqual({c['config'] for c in g['contexts'] if 'config' in c},{'products/admin/compile.json'})
        self.assertTrue(any(c['evidence']=='unconfigured-source-candidate' for c in g['contexts']))

    def test_workspace_package_exports_resolve_to_indexed_source(self):
        self.put('tsconfig.json',{'compilerOptions':{'module':'ESNext','moduleResolution':'Bundler'},'include':['app/*.ts']})
        self.put('app/form.ts',"import { fields } from '@test/forms'; export const selected=fields;")
        self.put('packages/forms/package.json',{'name':'@test/forms','exports':{'.':{'types':'./src/index.ts','default':'./src/index.ts'}}})
        self.put('packages/forms/src/index.ts',"export const fields=[{key:'x',type:'input'}];")
        parent=self.root/'node_modules/@test';parent.mkdir(parents=True);(parent/'forms').symlink_to(self.root/'packages/forms',target_is_directory=True)
        self.scan();self.assertIn(('app/form.ts','packages/forms/src/index.ts'),self.links('tsconfig.json'))
        self.assertEqual(self.cli('check')['status'],'fresh')

    def test_context_filter_keeps_competing_app_aliases_separate(self):
        self.multi();self.scan()
        result=self.cli('trace','--query','selected','--context','products/admin/prod.json','--depth','4','--limit','100')
        self.assertTrue(result['nodes'])
        self.assertEqual({n['context'] for n in result['nodes']},{'products/admin/prod.json'})
        self.assertTrue(any(n['file']=='shared/forms/prod.ts' for n in result['nodes']))
        self.assertFalse(any(n['file']=='shared/forms/admin.ts' for n in result['nodes']))
    def test_root_nx_placeholder_and_duplicate_project_roots(self):
        self.put('nx.json',{})
        self.put('nx-graph.json',{'nodes':{name:{'data':{'root':'.','targets':{'build':{'options':{'tsConfig':'{projectRoot}/tsconfig.app.json'}}}}} for name in ['one','two']}})
        self.put('tsconfig.app.json',{'include':['src/*.ts']});self.put('src/form.ts',"export const f=[{key:'x',type:'input'}];")
        g=self.scan('--nx-graph','nx-graph.json');self.assertEqual(len(g['workspace']['projects']),2)
        self.assertTrue(any(c['config']=='tsconfig.app.json' for c in g['contexts'] if 'config' in c))
        self.assertIn('overlapping-project-roots',{i['reason'] for i in g['unresolved']})
    def test_retargeting_package_link_invalidates_identical_contents(self):
        self.put('tsconfig.json',{'compilerOptions':{'module':'ESNext','moduleResolution':'Bundler'},'include':['src/*.ts']})
        self.put('src/form.ts',"import { fields } from '@test/forms'; export const selected=fields;")
        for name in ['one','two']:
            self.put(name+'/package.json',{'name':'@test/forms','exports':{'types':'./index.ts'}})
            self.put(name+'/index.ts',"export const fields=[{key:'x',type:'input'}];")
        parent=self.root/'node_modules/@test';parent.mkdir(parents=True);link=parent/'forms';link.symlink_to(self.root/'one',target_is_directory=True)
        self.scan();self.assertEqual(self.cli('check')['status'],'fresh')
        link.unlink();link.symlink_to(self.root/'two',target_is_directory=True)
        self.assertFalse(self.cli('check',code=1)['resolution_inputs_current'])

"""Behavioral CLI tests; temporary synthetic projects, no Angular execution."""
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / 'skill/ask-formly/scripts/project_index.py'

class ProjectIndexTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'project'
        self.root.mkdir()
        self.put('package.json', json.dumps({'dependencies': {'@angular/core': '^21.2.0', '@ngx-formly/core': '^6.3.0', '@angular/material': '21.2.14'}, 'scripts': {'postinstall': 'touch SHOULD_NOT_EXIST'}}))
        self.put('package-lock.json', json.dumps({'lockfileVersion': 3, 'packages': {'node_modules/@ngx-formly/core': {'version': '6.3.12'}}}))
        self.put('angular.json', '{"projects":{"admin":{"root":"apps/admin"},"portal":{"root":"apps/portal"}}}')
        self.put('apps/admin/form.ts', "import { buildFields } from './shared';\nimport { extra } from '@shared/extra';\nexport const fields: FormlyFieldConfig[] = buildFields();\n// SECRET_LITERAL_DO_NOT_COPY\n")
        self.put('apps/admin/shared.ts', "export const buildFields = () => [{ key: 'code', templateOptions: { required: true }, hideExpression: 'model.hidden' }];")
        self.put('apps/admin/screen.html', '<formly-form [fields]="fields" [model]="model"></formly-form>')
        self.put('apps/admin/config.ts', 'FormlyModule.forChild({ types: [{ name: "warehouse", component: WarehouseType }] });')
        self.put('apps/admin/type.ts', 'export class WarehouseType extends FieldType {}')
        self.put('apps/portal/other.ts', 'const fields: FormlyFieldConfig[] = [];')
    def put(self, name, content):
        p=self.root/name;p.parent.mkdir(parents=True, exist_ok=True);p.write_text(content);return p
    def cli(self, command, *args, code=0):
        p=subprocess.run([sys.executable,str(SCRIPT),command,'--root',str(self.root),*args],capture_output=True,text=True)
        self.assertEqual(p.returncode,code,p.stdout+p.stderr)
        return json.loads(p.stdout)
    def index(self):return json.loads((self.root/'.agents/ask-formly/index.json').read_text())
    def test_discovers_candidates_and_local_links_without_executing_or_copying_source(self):
        self.cli('scan');d=self.index()
        self.assertEqual(d['files']['apps/admin/screen.html']['signals'][0]['kind'],'form-host')
        self.assertIn('apps/admin/shared.ts',[x['target'] for x in d['files']['apps/admin/form.ts']['references']])
        self.assertTrue(any(x['module']=='@shared/extra' and x['target'] is None for x in d['files']['apps/admin/form.ts']['references']))
        self.assertTrue(any(v['version']=='^6.3.0' and v['kind']=='declared' for v in d['versions']))
        self.assertTrue(any(v['version']=='6.3.12' and v['kind']=='npm-lock' for v in d['versions']))
        self.assertFalse((self.root/'SHOULD_NOT_EXIST').exists())
        self.assertNotIn('SECRET_LITERAL_DO_NOT_COPY',json.dumps(d))
        self.assertTrue(d['questions'])
        self.assertEqual(self.cli('check')['status'],'fresh')
    def test_changed_added_deleted_and_same_mtime_are_detected(self):
        self.cli('scan');p=self.root/'apps/admin/shared.ts';stamp=p.stat();p.write_text('export const changed = true;');os.utime(p,ns=(stamp.st_atime_ns,stamp.st_mtime_ns))
        self.put('apps/admin/new.ts','const f: FormlyFieldConfig[]=[];');(self.root/'apps/portal/other.ts').unlink()
        r=self.cli('check',code=1)
        self.assertIn('apps/admin/shared.ts',r['changes']['changed']);self.assertIn('apps/admin/new.ts',r['changes']['added']);self.assertIn('apps/portal/other.ts',r['changes']['deleted'])
    def test_scope_persists_and_excludes_unselected_forms(self):
        self.cli('scan','--scope','apps/admin','--exclude','**/type.ts')
        self.assertNotIn('apps/portal/other.ts',self.index()['files']);self.assertNotIn('apps/admin/type.ts',self.index()['files'])
        self.assertIn('package.json',self.index()['files'])
        self.cli('scan');self.assertNotIn('apps/portal/other.ts',self.index()['files'])
        self.assertEqual(self.cli('check')['status'],'fresh')
    def test_note_preserved_but_not_revalidated_by_rescan(self):
        self.cli('scan');note=self.put('note.md','Country determines region choices; source-reviewed, browser unverified.')
        self.cli('note','--id','supplier','--input',str(note),'--source','apps/admin/shared.ts')
        self.assertEqual(self.cli('check')['notes']['supplier'],'current-source')
        self.put('apps/admin/shared.ts','export const newRules = true;');self.cli('scan')
        r=self.cli('check',code=1);self.assertEqual(r['notes']['supplier'],'needs-review')
        self.assertEqual((self.root/'.agents/ask-formly/notes/supplier.md').read_text(),note.read_text())
        self.cli('note','--id','supplier','--input',str(note),'--source','apps/admin/shared.ts')
        self.assertEqual(self.cli('check')['status'],'fresh')
    def test_manual_note_edits_and_settings_changes_are_reported(self):
        self.cli('scan');note=self.put('note.md','Reviewed note')
        self.cli('note','--id','project','--input',str(note),'--source','package.json')
        (self.root/'.agents/ask-formly/notes/project.md').write_text('Human clarification to preserve')
        self.assertEqual(self.cli('check',code=1)['notes']['project'],'edited')
        p=self.root/'.agents/ask-formly/config.json';d=json.loads(p.read_text());d['exclude']=['**/shared.ts'];p.write_text(json.dumps(d))
        self.assertTrue(self.cli('check',code=1)['settings_changed'])
    def test_external_scope_and_output_symlink_rejected(self):
        self.cli('scan','--scope','../',code=2)
        self.assertFalse((self.root/'.agents').exists())
        outside=Path(self.tmp.name)/'outside';outside.mkdir();(self.root/'.agents').symlink_to(outside,target_is_directory=True)
        self.cli('scan',code=2);self.assertEqual(list(outside.iterdir()),[])
    def test_unmanaged_output_is_not_overwritten(self):
        self.put('.agents/ask-formly/index.md','Human-authored existing material')
        self.cli('scan',code=2)
        self.assertEqual((self.root/'.agents/ask-formly/index.md').read_text(),'Human-authored existing material')
    def test_scan_skips_source_symlinks_and_reports_partial_coverage(self):
        outside=Path(self.tmp.name)/'secret.ts';outside.write_text('FormlyFieldConfig SECRET')
        (self.root/'apps/admin/link.ts').symlink_to(outside)
        r=self.cli('scan');self.assertEqual(r['coverage'],'partial')
        self.assertNotIn('apps/admin/link.ts',self.index()['files']);self.assertEqual(self.cli('check',code=1)['status'],'incomplete')
    def test_git_directory_symlink_is_reported_before_extension_filtering(self):
        subprocess.run(['git','init','-q',str(self.root)],check=True)
        outside=Path(self.tmp.name)/'outside-forms';outside.mkdir();(outside/'fields.ts').write_text('const fields: FormlyFieldConfig[]=[];')
        (self.root/'shared-forms').symlink_to(outside,target_is_directory=True)
        subprocess.run(['git','-C',str(self.root),'add','shared-forms'],check=True)
        self.assertEqual(self.cli('scan')['coverage'],'partial')
        self.assertTrue(any(w['path']=='shared-forms' for w in self.index()['warnings']))
        self.assertEqual(self.cli('check',code=1)['status'],'incomplete')
    def test_oversized_file_is_not_silently_treated_as_complete(self):
        self.put('apps/admin/big.ts','x'*(1024*1024+1))
        self.assertEqual(self.cli('scan')['coverage'],'partial')
        self.assertEqual(self.cli('check',code=1)['status'],'incomplete')
    def test_large_readable_form_signal_limit_does_not_prevent_reviewed_notes(self):
        self.put('apps/admin/large.ts','const fields = ['+','.join("{key:'f%d',validators:{}}" % i for i in range(100))+'];')
        result=self.cli('scan');self.assertEqual(result['coverage'],'complete-within-scope')
        self.assertTrue(any(w['reason']=='signal-limit' for w in self.index()['warnings']))
        note=self.put('large-review.md','Reviewed the complete source; lexical preview is truncated.')
        self.cli('note','--id','large','--input',str(note),'--source','apps/admin/large.ts')
        self.assertEqual(self.cli('check')['notes']['large'],'current-source')
    def test_gitignored_files_and_default_generated_folders_excluded(self):
        subprocess.run(['git','init','-q',str(self.root)],check=True)
        self.put('.gitignore','ignored/\n');self.put('ignored/secret.ts','FormlyFieldConfig');self.put('node_modules/a/a.ts','FormlyFieldConfig');self.put('dist/a.ts','FormlyFieldConfig')
        self.cli('scan');files=self.index()['files'];self.assertNotIn('ignored/secret.ts',files);self.assertNotIn('node_modules/a/a.ts',files);self.assertNotIn('dist/a.ts',files)

    def test_root_ignored_by_parent_repository_is_not_reported_as_complete(self):
        parent=Path(self.tmp.name)
        subprocess.run(['git','init','-q',str(parent)],check=True)
        (parent/'.gitignore').write_text('project/\n')
        result=self.cli('scan',code=2)
        self.assertIn('root is ignored',result['error'])
        self.assertFalse((self.root/'.agents/ask-formly/index.json').exists())
    def test_note_cannot_attest_stale_snapshot_or_untracked_source(self):
        self.cli('scan');note=self.put('note.md','Reviewed')
        self.cli('note','--id','../escape','--input',str(note),'--source','package.json',code=2)
        self.cli('note','--id','x','--input',str(note),'--source','note.md',code=2)
        self.put('apps/admin/shared.ts','const changed=true;')
        self.cli('note','--id','x','--input',str(note),'--source','package.json',code=2)
    def test_query_is_bounded_for_large_inventory(self):
        for i in range(500):self.put(f'apps/admin/forms/form-{i:03}.ts','export const fields: FormlyFieldConfig[] = [];')
        self.cli('scan');r=self.cli('find','--query','forms/form-','--limit','7')
        self.assertEqual(r['total'],500);self.assertEqual(len(r['matches']),7);self.assertTrue(r['has_more'])
        self.assertLess((self.root/'.agents/ask-formly/index.md').stat().st_size,18000)

    def test_find_paginates_inventory_without_omitting_or_repeating_files(self):
        for i in range(23):self.put(f'apps/admin/forms/form-{i:03}.ts','export const fields: FormlyFieldConfig[] = [];')
        self.cli('scan');files=[];offset=0
        while True:
            page=self.cli('find','--query','forms/form-','--limit','7','--offset',str(offset))
            self.assertEqual(page['total'],23)
            self.assertEqual(page['offset'],offset)
            files.extend(item['file'] for item in page['matches'])
            if not page['has_more']:
                self.assertIsNone(page['next_offset']);break
            self.assertGreater(page['next_offset'],offset);offset=page['next_offset']
        self.assertEqual(files,[f'apps/admin/forms/form-{i:03}.ts' for i in range(23)])
        self.assertEqual(self.cli('find','--offset','99')['matches'],[])
        self.cli('find','--offset','-1',code=2)
        self.cli('trace','--offset','7',code=2)

if __name__=='__main__':unittest.main()

#!/usr/bin/env python3
"""Standalone validation, tests and deterministic skill packaging (Python 3.9+)."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote
import zipfile

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skill/ask-formly'
sys.dont_write_bytecode=True

def digest(data):return hashlib.sha256(data).hexdigest()

def package_files(skill):
    files={}
    for p in sorted(skill.rglob('*')):
        if p.is_symlink():raise ValueError(f'Symlinks cannot ship: {p}')
        if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':files[p.relative_to(skill).as_posix()]=p.read_bytes()
    for name in ['SKILL.md','THIRD_PARTY_NOTICES.md','scripts/project_index.py','scripts/formly_graph.cjs','scripts/workspace.cjs','references/project-indexing.md']:
        if name not in files:raise ValueError(f'Missing required bundle file: {name}')
    return files

def build(root=ROOT,output=None):
    output=Path(output or root/'dist');output.mkdir(parents=True,exist_ok=True)
    version=json.loads((root/'package.json').read_text())['version']
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[a-zA-Z0-9.-]+)?',version):raise ValueError('Invalid package version')
    files=package_files(root/'skill/ask-formly');archive=output/f'ask-formly-{version}.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as bundle:
        for name,data in files.items():
            info=zipfile.ZipInfo('ask-formly/'+name,(1980,1,1,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED
            bundle.writestr(info,data,compresslevel=9)
    checksum=digest(archive.read_bytes())
    archive.with_suffix('.zip.sha256').write_text(f'{checksum}  {archive.name}\n')
    archive.with_suffix('.manifest.json').write_text(json.dumps({'version':version,'archive_sha256':checksum,'files':{'ask-formly/'+n:digest(d) for n,d in files.items()}},indent=2)+'\n')
    return archive

def compiler():
    p=Path(os.environ.get('FORMLY_TEST_TYPESCRIPT',str(ROOT/'node_modules/typescript/lib/typescript.js'))).resolve()
    if not p.is_file():raise ValueError('TypeScript compiler missing: run npm ci (or set FORMLY_TEST_TYPESCRIPT). Graph tests must not silently skip.')
    os.environ['FORMLY_TEST_TYPESCRIPT']=str(p)
    return p

def validate():
    package_files(SKILL)
    front=(SKILL/'SKILL.md').read_text().split('---',2)[1]
    if not re.search(r'^name: ask-formly$',front,re.M) or not re.search(r'^description: .+',front,re.M):raise ValueError('Invalid skill frontmatter')
    errors=[];links=0
    for p in [ROOT/'README.md',*ROOT.joinpath('docs').rglob('*.md'),*SKILL.rglob('*.md')]:
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            target=unquote(target.strip('<>').split('#')[0])
            if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target):continue
            links+=1
            if not (p.parent/target).exists():errors.append(f'{p.relative_to(ROOT)}: {target}')
    if errors:raise ValueError('Broken local link targets: '+repr(errors))
    for p in [*SKILL.rglob('*.py'),*ROOT.joinpath('tools').glob('*.py')]:ast.parse(p.read_text(),filename=str(p))
    for p in [*SKILL.rglob('*.cjs'),*ROOT.joinpath('tools').glob('*.cjs')]:subprocess.run(['node','--check',str(p)],check=True,capture_output=True)
    for p in SKILL.rglob('*.json'):json.loads(p.read_text())
    print(json.dumps({'validation':'pass','local_link_targets':links}))

def tests():
    compiler()
    suite=unittest.TestSuite()
    suite.addTests(unittest.TestLoader().discover(str(ROOT/'tests/project-index'),pattern='test_*.py'))
    suite.addTests(unittest.TestLoader().discover(str(ROOT/'tools'),pattern='test_*.py'))
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful() or result.skipped:raise ValueError('Tests failed or skipped')
    return result.testsRun

def smoke():
    ts=compiler();archive=build()
    manifest=json.loads(archive.with_suffix('.manifest.json').read_text())
    with tempfile.TemporaryDirectory(prefix='ask-formly-bundle-') as directory:
        base=Path(directory)
        with zipfile.ZipFile(archive) as bundle:
            if set(bundle.namelist())!=set(manifest['files']):raise ValueError('Unexpected archive inventory')
            for name in bundle.namelist():
                if Path(name).is_absolute() or '..' in Path(name).parts:raise ValueError('Unsafe ZIP path')
                if digest(bundle.read(name))!=manifest['files'][name]:raise ValueError('Bundle hash mismatch')
            bundle.extractall(base)
        app=base/'app';app.mkdir()
        (app/'form.ts').write_text("export const fields=[{key:'customer',type:'input'}];")
        cli=base/'ask-formly/scripts/project_index.py'
        def call(command,*args):
            result=subprocess.run([sys.executable,str(cli),command,'--root',str(app),*args],capture_output=True,text=True,check=True)
            return json.loads(result.stdout)
        scan=call('scan','--typescript',str(ts))
        if scan['graph_mode']!='typescript-static':raise ValueError('Installed graph unavailable')
        if call('check')['status']!='fresh':raise ValueError('Installed check failed')
        trace=call('trace','--query','fields')
        if 'customer' not in {n['name'] for n in trace['nodes']}:raise ValueError('Installed trace missing field')
        note=base/'review.md';note.write_text('Synthetic source-reviewed field; browser unverified.')
        call('note','--id','form','--input',str(note),'--source','form.ts')
        if call('check')['notes']['form']!='current-source':raise ValueError('Installed note failed')
    print(json.dumps({'installed_bundle':'pass','archive':str(archive)}))

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['validate','test','build','smoke','check']);args=parser.parse_args()
    if args.command in {'validate','check'}:validate()
    if args.command in {'test','check'}:print(json.dumps({'tests_passed':tests(),'skipped':0}))
    if args.command=='build':print(build())
    if args.command in {'smoke','check'}:smoke()

if __name__=='__main__':main()

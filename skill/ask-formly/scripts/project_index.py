#!/usr/bin/env python3
"""Local Formly discovery, static connections and source-backed notes. Python 3.9+."""
from __future__ import annotations
import argparse
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import fnmatch
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

OWNER='ask-formly-project-index'
SCHEMA=1
SKIP={'.git','.agents','.codex','.angular','.nx','node_modules','dist','build','coverage','out','.next','vendor'}
EXTENSIONS={'.ts','.tsx','.js','.mjs','.cjs','.html','.json','.jsonc'}
LOCKS={'package-lock.json','npm-shrinkwrap.json','pnpm-lock.yaml','yarn.lock','bun.lock','bun.lockb'}
PACKAGES={'@angular/core','@angular/forms','@angular/material','@angular/cdk','@ngx-formly/core','@ngx-formly/material','rxjs','@playwright/test','typescript'}
SIGNALS={
 'form-host':r'<formly-form\b','field-host':r'<formly-field\b',
 'registration':r'\bFormlyModule\s*\.\s*for(?:Root|Child)\b|\bFORMLY_CONFIG\b|\bprovideFormly\b',
 'field-config':r'\bFormlyFieldConfig\b|\bfieldGroup\s*:|\bfieldArray\s*:',
 'custom-type':r'\bextends\s+(?:FieldType|FieldArrayType|MaterialFieldType)\b',
 'wrapper':r'\bextends\s+FieldWrapper\b','legacy':r'\b(?:templateOptions|expressionProperties|hideExpression)\s*:',
 'validation':r'\b(?:asyncValidators|validators|validationMessages)\s*:',
 'expressions':r'\bexpressions\s*:','schema-conversion':r'\bFormlyJsonschema\b|\btoFieldConfig\s*\(',
 'routing':r'\b(?:loadChildren|loadComponent)\s*:|\bRouterModule\s*\.\s*for',
 'playwright':r'@playwright/test|\bdefineConfig\s*\('
}
class IndexError_(Exception):
    pass

def sha(data):
    return hashlib.sha256(data).hexdigest()

def encoded(value):
    return (json.dumps(value,indent=2,sort_keys=True,ensure_ascii=True)+'\n').encode()

def load(path):
    try:
        return json.loads(path.read_text())
    except (OSError,ValueError) as exc:
        raise IndexError_(f'Cannot read JSON {path.name}: {exc}') from exc

def safe_path(root,relative):
    p=PurePosixPath(relative)
    if p.is_absolute() or '..' in p.parts or '\\' in relative:
        raise IndexError_(f'Expected project-relative path: {relative}')
    target=root.joinpath(*p.parts)
    for part in [target,*target.parents]:
        if part==root:break
        if part.is_symlink():raise IndexError_(f'Symlink path unsupported: {relative}')
    if not target.resolve().is_relative_to(root):raise IndexError_(f'Path escapes project: {relative}')
    return target

def output_dir(root):
    return safe_path(root,'.agents/ask-formly')

def settings(root,args):
    out=output_dir(root);path=safe_path(root,'.agents/ask-formly/config.json')
    config=load(path) if path.exists() else {'schema_version':SCHEMA,'scopes':['.'],'exclude':[]}
    if not isinstance(config,dict) or config.get('schema_version')!=SCHEMA:raise IndexError_('Unsupported config schema')
    for attr,key in [('scope','scopes'),('exclude','exclude')]:
        if getattr(args,attr,None) is not None:config[key]=getattr(args,attr)
    if getattr(args,'typescript',None):config['typescript']=str(Path(args.typescript).expanduser().resolve())
    for key in ['scopes','exclude']:
        if not isinstance(config.get(key),list) or any(not isinstance(x,str) or not x for x in config[key]):raise IndexError_(f'{key} must be nonempty strings in an array')
    if not config['scopes']:raise IndexError_('At least one scope required')
    for scope in config['scopes']:
        if not safe_path(root,scope).exists():raise IndexError_(f'Scope does not exist: {scope}')
    return out,config

def wanted(rel,config):
    p=PurePosixPath(rel)
    if any(x in SKIP for x in p.parts) or any(fnmatch.fnmatchcase(rel,pat) for pat in config['exclude']):return False
    if p.suffix not in EXTENSIONS and p.name not in LOCKS and p.name!='.gitignore':return False
    metadata=p.name in LOCKS|{'package.json','angular.json','nx.json','.gitignore'} or p.name.startswith('tsconfig')
    for scope in config['scopes']:
        s=PurePosixPath(scope)
        if str(s)=='.' or p==s or s in p.parents:return True
        if metadata and (p.parent==s or p.parent in s.parents):return True
    return False

def paths(root,config):
    warnings=[]
    try:
        run=subprocess.run(['git','-C',str(root),'ls-files','--cached','--others','--exclude-standard','-z','--','.'],capture_output=True,timeout=30)
    except (OSError,subprocess.TimeoutExpired):run=None
    if run is not None and run.returncode==0:
        names=sorted(set(os.fsdecode(p) for p in run.stdout.split(b'\0') if p));mode='git-tracked-and-unignored'
        # Git returns directory symlinks/gitlinks as single entries. They would
        # otherwise disappear in extension filtering without a coverage warning.
        for name in names:
            p=root/name
            scoped=any(s=='.' or name==s or name.startswith(s.rstrip('/')+'/') for s in config['scopes'])
            excluded=any(x in SKIP for x in PurePosixPath(name).parts) or any(fnmatch.fnmatchcase(name,pat) for pat in config['exclude'])
            if scoped and not excluded and (p.is_symlink() or p.is_dir()):warnings.append({'path':name,'reason':'symlink-or-gitlink-not-traversed'})
    else:
        names=[]
        def onerror(exc):warnings.append({'path':str(Path(exc.filename).relative_to(root)),'reason':'unreadable-directory'})
        for current,dirs,files in os.walk(root,followlinks=False,onerror=onerror):
            for directory in list(dirs):
                p=Path(current)/directory
                if directory in SKIP:dirs.remove(directory)
                elif p.is_symlink():
                    dirs.remove(directory);rel=p.relative_to(root).as_posix()
                    if any(s=='.' or rel.startswith(s.rstrip('/')+'/') or rel==s for s in config['scopes']):warnings.append({'path':rel,'reason':'symlink-directory'})
            names.extend((Path(current)/name).relative_to(root).as_posix() for name in files)
        names.sort();mode='filesystem-default-exclusions; gitignore-not-applied'
    return [n for n in names if wanted(n,config)],warnings,mode

def local_target(rel,module,names):
    if not module.startswith('.'):return None
    base=os.path.normpath(str(PurePosixPath(rel).parent/module)).replace(os.sep,'/')
    return next((p for p in [base,base+'.ts',base+'.tsx',base+'.js',base+'/index.ts',base+'/index.js'] if p in names),None)

def tool_identity(config,root):
    script=Path(__file__).resolve();analyzer=script.with_name('formly_graph.cjs')
    compiler=Path(config.get('typescript',str(root/'node_modules/typescript/lib/typescript.js')))
    return {'scanner':sha(script.read_bytes()),'graph_analyzer':sha(analyzer.read_bytes()) if analyzer.exists() else None,'typescript_path':str(compiler),'typescript_sha256':sha(compiler.read_bytes()) if compiler.is_file() else None}

def inventory(root,config):
    names,warnings,mode=paths(root,config)
    if len(names)>50000:warnings.append({'path':'.','reason':'file-count-limit','omitted':len(names)-50000});names=names[:50000]
    files={};versions=[];apps=[];name_set=set(names)
    for rel in names:
        try:
            p=safe_path(root,rel)
            if not p.exists():continue
            limit=16*1024*1024 if p.name in LOCKS else 1024*1024
            if p.stat().st_size>limit:warnings.append({'path':rel,'reason':'size-limit'});continue
            data=p.read_bytes();text=data.decode('utf-8')
        except (OSError,UnicodeError,IndexError_) as exc:
            warnings.append({'path':rel,'reason':type(exc).__name__});continue
        signals=[]
        for kind,pattern in SIGNALS.items():
            matches=list(re.finditer(pattern,text))
            signals.extend({'kind':kind,'line':text.count('\n',0,m.start())+1} for m in matches[:30])
            if len(matches)>30:warnings.append({'path':rel,'reason':'signal-limit','kind':kind})
        refs=[]
        if p.suffix in {'.ts','.tsx','.js','.mjs','.cjs'}:
            pattern=r'''(?:\bfrom\s*|\bimport\s*\(\s*|\bimport\s*|\btemplateUrl\s*:\s*)['"]([^'"\n]+)['"]'''
            refs=[{'module':m[1],'line':text.count('\n',0,m.start())+1,'target':local_target(rel,m[1],name_set),'evidence':'lexical-candidate'} for m in re.finditer(pattern,text)]
        files[rel]={'sha256':sha(data),'bytes':len(data),'signals':signals,'references':refs}
        if p.name in {'package.json','package-lock.json','npm-shrinkwrap.json','angular.json','project.json'}:
            try:
                doc=json.loads(text)
                if not isinstance(doc,dict):raise ValueError('Expected object')
                if p.name=='package.json':
                    for group in ['dependencies','devDependencies','peerDependencies']:
                        versions.extend({'package':n,'version':v,'kind':'declared','file':rel,'group':group} for n,v in doc.get(group,{}).items() if n in PACKAGES)
                elif p.name in {'package-lock.json','npm-shrinkwrap.json'}:
                    for key,value in doc.get('packages',{}).items():
                        name=key.rsplit('node_modules/',1)[-1]
                        if name in PACKAGES and isinstance(value,dict) and 'version' in value:versions.append({'package':name,'version':value['version'],'kind':'npm-lock','file':rel,'location':key})
                    if not doc.get('packages'):warnings.append({'path':rel,'reason':'lock-format-not-resolved'})
                elif p.name=='angular.json':apps.extend({'name':n,'file':rel,'root':v.get('root')} for n,v in doc.get('projects',{}).items() if isinstance(v,dict))
                else:apps.append({'name':doc.get('name',p.parent.name),'file':rel,'root':str(PurePosixPath(rel).parent)})
            except (ValueError,TypeError,AttributeError):warnings.append({'path':rel,'reason':'metadata-not-parsed'})
    tools=tool_identity(config,root)
    snapshot=sha(encoded({'files':{p:v['sha256'] for p,v in files.items()},'settings':config,'warnings':warnings,'tools':tools,'mode':mode}))
    questions=[]
    if len(apps)>1:questions.append('Multiple project entries: confirm target app(s) and shared libraries if not already selected.')
    if not any(f['signals'] for f in files.values()):questions.append('No recognized Formly signals: locate external schemas or nonstandard helpers before claiming coverage.')
    return {'owner':OWNER,'schema_version':SCHEMA,'snapshot':snapshot,'generated_at':datetime.now(timezone.utc).isoformat(),'settings':config,'tools':tools,'discovery_mode':mode,'coverage':'partial' if any(w['reason'] not in {'signal-limit','metadata-not-parsed','lock-format-not-resolved'} for w in warnings) else 'complete-within-scope','limitations':['Signals/references are candidates, not runtime proof.','Ignored/excluded files are outside scope; aliases/dynamic factories need AST or manual review.','Declared ranges and npm lock versions are not installed-version proof.'],'warnings':warnings,'questions':questions,'apps':apps,'versions':versions,'files':files}

@contextmanager
def writer(root):
    out=output_dir(root)
    for name in ['config.json','index.json','index.md','graph.json','.write-lock','notes']:safe_path(root,'.agents/ask-formly/'+name)
    if (out/'index.json').exists():
        old=load(out/'index.json')
        if old.get('owner')!=OWNER or old.get('schema_version')!=SCHEMA:raise IndexError_('Refusing unmanaged/unsupported index.json')
    elif (out/'graph.json').exists():raise IndexError_('Refusing unmanaged graph.json')
    if (out/'index.md').exists() and not (out/'index.md').read_text().startswith('<!-- '+OWNER):raise IndexError_('Refusing unmanaged index.md')
    out.mkdir(parents=True,exist_ok=True);lock=out/'.write-lock'
    try:fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except FileExistsError as exc:raise IndexError_('Writer or interrupted write exists; inspect .write-lock before removing it') from exc
    try:
        os.close(fd);yield out
    finally:lock.unlink()

def atomic(path,data):
    fd,tmp=tempfile.mkstemp(prefix='.tmp-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as stream:stream.write(data)
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def graph(root,current):
    if not current['tools']['typescript_sha256']:return {'mode':'unavailable','nodes':[],'edges':[],'unresolved':[{'reason':'TypeScript unavailable; use --typescript PATH or agent review.'}]}
    try:
        run=subprocess.run(['node',str(Path(__file__).with_name('formly_graph.cjs')),current['tools']['typescript_path']],input=json.dumps({'root':str(root),'files':list(current['files']),'hashes':{p:v['sha256'] for p,v in current['files'].items()}}),text=True,capture_output=True,timeout=90)
        if run.returncode:raise IndexError_(run.stderr[:500])
        return json.loads(run.stdout)
    except (OSError,ValueError,subprocess.TimeoutExpired,IndexError_) as exc:return {'mode':'unavailable','nodes':[],'edges':[],'unresolved':[{'reason':str(exc)[:500]}]}

def summary_markdown(current,mapped):
    lines=[f'<!-- {OWNER} schema={SCHEMA} snapshot={current["snapshot"]} -->','# Formly project index','',
     'Generated discovery. Reviewed context lives in `notes/`. Run check before reuse; source freshness is not UI validation.',
     f'Files: {len(current["files"])}. Coverage: {current["coverage"]}. Graph: {mapped["mode"]}.',
     f'Scopes: {current["settings"]["scopes"]}. Excludes: {current["settings"]["exclude"]}.','',
     'Use find for bounded file lookup and trace for typed connections; avoid loading the full JSON inventory.','', '## Entry points and registrations','']
    entries=[n for n in mapped['nodes'] if n['kind'] in {'entry-point','registration'}]
    lines += [f'- {n["kind"]}: `{n["name"]}` — `{n["file"]}:{n["line"]}`' for n in entries[:35]]
    if not entries:lines.append('No AST entry points resolved; inspect registration candidates. Absence is not proof.')
    if len(entries)>35:lines.append(f'{len(entries)-35} further entries; use trace.')
    lines+=['','## Candidate locations and observed naming','']
    candidates=[(p,f) for p,f in current['files'].items() if f['signals'] or f.get('ast_kinds')]
    lines += [f'- `{p}` — {", ".join(sorted({s["kind"] for s in f["signals"]}|set(f.get('ast_kinds',[]))))}' for p,f in candidates[:35]]
    if len(candidates)>35:lines.append(f'{len(candidates)-35} further candidate files; use find.')
    forms=[p for p,f in candidates if {'field-config','form-host'} & ({s['kind'] for s in f['signals']}|set(f.get('ast_kinds',[])))]
    lines+=['','Observed config/host directories (not a naming rule):']+[f'- `{p}`: {n}' for p,n in Counter(str(PurePosixPath(p).parent) for p in forms).most_common(10)]
    counts=Counter('.'.join(PurePosixPath(p).name.split('.')[-2:]) for p in forms)
    lines+=['Observed filename endings: '+', '.join(f'`{p}` ({n})' for p,n in counts.most_common(10)),'','## Unknowns and next inspection','']
    lines+=['- '+q for q in current['questions']]
    lines += [f'- {len(current["warnings"])} scan limitations; {len(mapped["unresolved"])} graph questions. Inspect detail before completeness claims.',
     '- Confirm custom behavior, registration scope and UI routes before recording notes.', '- Record user answers and form flows with note; refresh never silently approves old notes.','']
    return '\n'.join(lines).encode()

def read_index(root):
    path=safe_path(root,'.agents/ask-formly/index.json')
    if not path.exists():raise IndexError_('No index. Run scan first.')
    value=load(path)
    if value.get('owner')!=OWNER or value.get('schema_version')!=SCHEMA:raise IndexError_('Unsupported/unmanaged index')
    return value

def freshness(root,current,old):
    before=old['files'];after=current['files'];notes={}
    changes={'added':sorted(set(after)-set(before)),'deleted':sorted(set(before)-set(after)),'changed':sorted(p for p in set(before)&set(after) if before[p]['sha256']!=after[p]['sha256'])}
    directory=safe_path(root,'.agents/ask-formly/notes')
    if directory.exists():
        for p in sorted(directory.glob('*.json')):
            safe_path(root,p.relative_to(root).as_posix());meta=load(p);md=safe_path(root,p.with_suffix('.md').relative_to(root).as_posix())
            notes[p.stem]='missing' if not md.exists() else 'edited' if sha(md.read_bytes())!=meta.get('note_sha256') else 'needs-review' if meta.get('snapshot')!=current['snapshot'] else 'current-source'
        for p in directory.glob('*.md'):
            if p.stem not in notes:notes[p.stem]='untracked-note'
    artifact_ok=True
    for name,expected in old.get('artifacts',{}).items():
        p=safe_path(root,'.agents/ask-formly/'+name)
        if not p.is_file() or sha(p.read_bytes())!=expected:artifact_ok=False
    same=old['snapshot']==current['snapshot'] and artifact_ok
    status='incomplete' if current['coverage']=='partial' else 'fresh' if same and all(x=='current-source' for x in notes.values()) else 'stale'
    return {'status':status,'source_snapshot_current':same,'settings_changed':old['settings']!=current['settings'],'changes':changes,'notes':notes,'coverage':current['coverage'],'artifacts_intact':artifact_ok,'meaning':'Fresh means unchanged scoped inputs, not verified semantics or UI behavior.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['scan','check','find','trace','note']);parser.add_argument('--root',required=True)
    parser.add_argument('--scope',action='append');parser.add_argument('--exclude',action='append');parser.add_argument('--typescript',help='TypeScript lib/typescript.js; default project node_modules')
    parser.add_argument('--query',default='');parser.add_argument('--limit',type=int,default=20);parser.add_argument('--depth',type=int,default=5);parser.add_argument('--direction',choices=['out','in','both'],default='out')
    parser.add_argument('--id');parser.add_argument('--input');parser.add_argument('--source',action='append');args=parser.parse_args()
    try:
        root=Path(args.root).expanduser().resolve()
        if not root.is_dir():raise IndexError_('Root must exist')
        if not 1<=args.limit<=500 or not 0<=args.depth<=10:raise IndexError_('limit must be 1..500; depth 0..10')
        out,config=settings(root,args)
        if args.command=='scan':
            with writer(root):
                current=inventory(root,config);mapped=graph(root,current);mapped.update({'owner':OWNER,'schema_version':SCHEMA,'snapshot':current['snapshot']})
                for node in mapped['nodes']:
                    if node['kind'] in {'field-config','form-host','entry-point','registration'} and node['file'] in current['files']:
                        kinds=current['files'][node['file']].setdefault('ast_kinds',[])
                        if node['kind'] not in kinds:kinds.append(node['kind'])
                graph_data=encoded(mapped);md=summary_markdown(current,mapped);current['artifacts']={'graph.json':sha(graph_data),'index.md':sha(md)}
                atomic(out/'config.json',encoded(config));atomic(out/'graph.json',graph_data);atomic(out/'index.md',md);atomic(out/'index.json',encoded(current))
            result={'status':'indexed','files':len(current['files']),'coverage':current['coverage'],'graph_mode':mapped['mode'],'nodes':len(mapped['nodes']),'edges':len(mapped['edges']),'questions':current['questions'],'output':str(out)}
        elif args.command=='check':
            if not (out/'index.json').exists():print(json.dumps({'status':'missing'}));return 1
            result=freshness(root,inventory(root,config),read_index(root));print(json.dumps(result,indent=2));return 0 if result['status']=='fresh' else 1
        elif args.command=='find':
            old=read_index(root);query=args.query.lower();matches=[{'file':p,**v} for p,v in old['files'].items() if query in p.lower() or any(query in s['kind'] for s in v['signals']) or any(query in kind for kind in v.get('ast_kinds',[]))]
            result={'matches':matches[:args.limit],'total':len(matches),'has_more':len(matches)>args.limit,'freshness_checked':False}
        elif args.command=='trace':
            read_index(root);mapped=load(safe_path(root,'.agents/ask-formly/graph.json'));nodes={n['id']:n for n in mapped['nodes']}
            seeds=[n['id'] for n in mapped['nodes'] if args.query.lower() in (n['name']+' '+n['file']).lower()];visited=set(seeds[:args.limit]);frontier=set(visited);truncated=len(seeds)>args.limit
            for _ in range(args.depth):
                targets=set()
                for edge in mapped['edges']:
                    if (args.direction in {'out','both'} and edge['from'] in frontier) or (args.direction in {'in','both'} and edge['to'] in frontier):targets.update([edge['from'],edge['to']])
                if len(targets-visited)>args.limit-len(visited):truncated=True
                frontier=set(sorted(targets-visited)[:max(0,args.limit-len(visited))]);visited.update(frontier)
                if not frontier:break
            # Include each induced edge once; flag paths stopped by either depth or node budget.
            for edge in mapped['edges']:
                if (args.direction in {'out','both'} and edge['from'] in frontier and edge['to'] not in visited) or (args.direction in {'in','both'} and edge['to'] in frontier and edge['from'] not in visited):truncated=True
            result={'mode':mapped['mode'],'nodes':[nodes[n] for n in sorted(visited)],'edges':[e for e in mapped['edges'] if e['from'] in visited and e['to'] in visited],'bounded':True,'truncated':truncated,'seed_matches':len(seeds),'limit':args.limit,'depth':args.depth,'freshness_checked':False,'unresolved':mapped['unresolved'][:args.limit],'unresolved_total':len(mapped['unresolved'])}
        else:
            if not args.id or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}',args.id):raise IndexError_('note requires lowercase slug --id')
            if not args.input or not args.source:raise IndexError_('note requires --input Markdown and --source')
            with writer(root):
                old=read_index(root);current=inventory(root,config)
                if old['snapshot']!=current['snapshot']:raise IndexError_('Source changed; scan and review before recording note')
                if not freshness(root,current,old)['artifacts_intact']:raise IndexError_('Generated artifacts changed; scan and review before recording note')
                if current['coverage']=='partial':raise IndexError_('Partial scan: resolve or explicitly narrow scope before attesting note')
                sources={}
                for rel in args.source:
                    safe_path(root,rel)
                    if rel not in current['files']:raise IndexError_(f'Source outside inventory: {rel}')
                    sources[rel]=current['files'][rel]['sha256']
                data=Path(args.input).read_bytes()
                if len(data)>128*1024:raise IndexError_('Keep each note below 128 KiB')
                data.decode('utf-8');target=safe_path(root,f'.agents/ask-formly/notes/{args.id}.md');metadata=safe_path(root,f'.agents/ask-formly/notes/{args.id}.json');target.parent.mkdir(exist_ok=True)
                atomic(target,data);atomic(metadata,encoded({'schema_version':SCHEMA,'snapshot':current['snapshot'],'sources':sources,'note_sha256':sha(data),'reviewed_at':datetime.now(timezone.utc).isoformat(),'evidence':'agent-or-user-reviewed; not automatic runtime verification'}))
            result={'status':'recorded','note':str(target)}
        print(json.dumps(result,indent=2));return 0
    except (IndexError_,OSError,UnicodeError,ValueError) as exc:print(json.dumps({'error':str(exc)}));return 2

if __name__=='__main__':sys.exit(main())

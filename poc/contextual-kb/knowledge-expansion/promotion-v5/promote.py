"""Explicit, guarded promotion of the reviewed 79-fact candidate. Never run on import."""
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
POC = HERE.parents[1]
REPO = POC.parents[1]
TABLES = ('documents', 'facts', 'evidence', 'fact_evidence', 'fact_links')


def digest(path):
    value=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''): value.update(chunk)
    return value.hexdigest()


def safe_path(root, name):
    path=root/name
    if Path(name).is_absolute() or path.resolve()!=path or not path.is_relative_to(root):
        raise ValueError('Unsafe or aliased path: '+str(name))
    return path


def write_atomic(path, content):
    descriptor,temporary=tempfile.mkstemp(prefix='.promotion-',dir=path.parent)
    try:
        with os.fdopen(descriptor,'wb') as stream:
            stream.write(content);stream.flush();os.fsync(stream.fileno())
        os.replace(temporary,path)
    finally:
        if os.path.exists(temporary):os.unlink(temporary)


def guarded_replace(root, changes, expected, recovery, postcheck):
    """Snapshot before changes; restore on ordinary errors/interrupts. Not a multi-file FS transaction."""
    root=Path(root).resolve();recovery=Path(recovery)
    if recovery.resolve()!=recovery or not recovery.is_relative_to(root):raise ValueError('Unsafe recovery path')
    for name,sha in expected.items():
        if digest(safe_path(root,name))!=sha:raise ValueError('Precondition drift: '+name)
    for name in changes:
        target=safe_path(root,name)
        if name not in expected and target.exists():raise ValueError('New target already exists: '+name)
        if not target.parent.is_dir():raise ValueError('Target parent missing: '+name)
    recovery.mkdir(exist_ok=False)
    for name in expected:
        copy=recovery/name;copy.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/name,copy)
        if digest(copy)!=expected[name]:raise ValueError('Snapshot mismatch: '+name)
    journal={'status':'prepared','before':expected,'new_files':[n for n in changes if n not in expected],
             'after':{n:hashlib.sha256(b).hexdigest() for n,b in changes.items()}}
    (recovery/'journal.json').write_text(json.dumps(journal,indent=2)+'\n')
    try:
        for name,sha in expected.items():
            if digest(root/name)!=sha:raise ValueError('Precondition drift after snapshot: '+name)
        for name,content in changes.items():write_atomic(root/name,content)
        postcheck()
        journal['status']='installed'
    except BaseException:
        for name in changes:
            if name in expected:write_atomic(root/name,(recovery/name).read_bytes())
            else:(root/name).unlink(missing_ok=True)
        journal['status']='rolled_back'
        (recovery/'journal.json').write_text(json.dumps(journal,indent=2)+'\n')
        raise
    (recovery/'journal.json').write_text(json.dumps(journal,indent=2)+'\n')
    return journal


def check_pins(root,pins):
    for name,sha in pins.items():
        if digest(safe_path(root,name))!=sha:raise ValueError('Pin mismatch: '+name)


def rows(database):
    with sqlite3.connect(Path(database).as_uri()+'?mode=ro',uri=True) as db:
        if db.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('Broken DB references')
        return {table:set(db.execute('SELECT * FROM '+table)) for table in TABLES}


def validate_additions(accepted, candidate, draft):
    names={'validation-contracts.json','validation-group-example.json'}
    if {p.name for p in candidate.glob('*.json')} != {p.name for p in accepted.glob('*.json')}|names or {p.name for p in draft.glob('*.json')} != names:
        raise ValueError('Unexpected source set')
    for path in accepted.glob('*.json'):
        if path.read_bytes()!=(candidate/path.name).read_bytes():raise ValueError('Accepted authored drift')
    additions={}
    for name in sorted(names):
        content=(draft/name).read_bytes()
        if content!=(candidate/name).read_bytes():raise ValueError('Draft/candidate mismatch')
        additions[name]=content
    return additions


def prepare(output):
    spec=json.loads((HERE/'promotion-spec.json').read_text());batch=POC/'knowledge-expansion/validation-v1'
    check_pins(REPO,spec['pins'])
    foundation=json.loads((POC/'mcp_foundation/foundation.json').read_text())
    sources=json.loads((POC/'packaging/source-files.json').read_text())
    if foundation['id']!='formly-poc-foundation-5':raise ValueError('Expected foundation5')
    check_pins(POC,foundation['files']);check_pins(REPO,sources)
    for name in ['input-freeze.json','qualification-freeze.json']:
        pins=json.loads((batch/'test-output'/name).read_text());check_pins(batch,pins.get('files',pins))
    manifest=json.loads((batch/'candidate-build/manifest.json').read_text())
    check_pins(batch,manifest['inputs'])
    candidate=batch/'candidate-build/knowledge.sqlite';accepted=POC/'build/knowledge.sqlite'
    if digest(candidate)!=spec['candidate_sha256'] or digest(accepted)!=spec['accepted_sha256']:
        raise ValueError('DB mismatch')
    old,new=rows(accepted),rows(candidate)
    if any(not old[t]<=new[t] for t in TABLES):raise ValueError('Candidate changed accepted rows')
    if len(new['facts'])!=79 or len(new['documents'])!=17:raise ValueError('Unexpected candidate count')
    additions=validate_additions(POC/'authored',batch/'candidate-inputs/authored',batch/'draft-authored')
    # Catalog serialization may differ, but no catalog records may change in this batch.
    if json.loads((POC/'corpus/evidence-catalog.json').read_text())!=json.loads((batch/'candidate-inputs/evidence-catalog.json').read_text()):
        raise ValueError('Catalog changed')
    output.mkdir(exist_ok=False)
    authored=output/'authored';shutil.copytree(POC/'authored',authored)
    for name,content in additions.items():(authored/name).write_bytes(content)
    sys.path.insert(0,str(POC))
    from kbcompiler.structured_source import build_sources
    build_sources(authored,REPO,POC/'corpus/evidence-catalog.json',output/'reproduced.sqlite')
    if rows(output/'reproduced.sqlite')!=new:raise ValueError('Canonical reproduction differs')
    expected={str(p.relative_to(REPO)):digest(p) for p in (POC/'authored').glob('*.json')}
    for p in [accepted,POC/'corpus/evidence-catalog.json',POC/'mcp_foundation/foundation.json',POC/'packaging/source-files.json']:
        expected[str(p.relative_to(REPO))]=digest(p)
    updated=json.loads(json.dumps(foundation));updated['id']='formly-poc-foundation-6';updated['files']['build/knowledge.sqlite']=spec['candidate_sha256'];updated['knowledge']={'facts':79,'documents':17,'promotion':'knowledge-expansion/promotion-v5'}
    changes={}
    for name,content in additions.items():
        authored_name='poc/contextual-kb/authored/'+name
        sources[authored_name]=hashlib.sha256(content).hexdigest()
        changes[authored_name]=content
    changes.update({'poc/contextual-kb/build/knowledge.sqlite':candidate.read_bytes(),
             'poc/contextual-kb/mcp_foundation/foundation.json':(json.dumps(updated,indent=2)+'\n').encode(),
             'poc/contextual-kb/packaging/source-files.json':(json.dumps(sources,indent=2)+'\n').encode()})
    receipt={'candidate_sha256':spec['candidate_sha256'],'accepted_sha256':spec['accepted_sha256'],
             'counts':{t:len(new[t]) for t in TABLES},'canonical_reproduction':'equal all five knowledge tables',
             'review':str(batch/'REVIEW-FINAL.md'),'runtime_model_pins_preserved':len(foundation['files'])-1}
    (output/'preflight.json').write_text(json.dumps(receipt,indent=2)+'\n')
    def postcheck():
        check_pins(POC,updated['files']);check_pins(REPO,sources)
        if rows(accepted)!=new:raise ValueError('Installed rows mismatch')
        build_sources(POC/'authored',REPO,POC/'corpus/evidence-catalog.json',output/'installed-reproduced.sqlite')
        if rows(output/'installed-reproduced.sqlite')!=new:raise ValueError('Installed canonical rebuild differs')
    return changes,expected,postcheck,receipt


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');parser.add_argument('--name',required=True)
    args=parser.parse_args()
    if Path(args.name).name!=args.name or args.name in ('.','..'):raise ValueError('Invalid output name')
    output=HERE/'test-output'/args.name
    if output.exists() or output.is_symlink():raise FileExistsError(output)
    changes,expected,postcheck,receipt=prepare(output)
    if args.apply:
        transaction=guarded_replace(REPO,changes,expected,output/'before',postcheck)
        receipt['status']=transaction['status']
    else:receipt['status']='checked_only; installed files unchanged'
    (output/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()

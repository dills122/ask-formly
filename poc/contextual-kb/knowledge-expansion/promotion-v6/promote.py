"""Explicit, guarded promotion of the reviewed 85-fact candidate and premise planner. Never run on import."""
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
    names={'array-operations.json','array-repeat-example.json'}
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


def promoted_service(content):
    old=b'from mcp_v1.planner import CodexPlanner'
    if content.count(old)!=1:
        raise ValueError('Unexpected service composition')
    return content.replace(old,b'from condition_candidate_v2.planner import CodexPlanner')


def validate_qualification(decision, probes, q20):
    rounds=decision.get('rounds',[])
    if (decision.get('qualified') is not True or decision.get('reasons') or len(rounds)!=3
        or {r.get('round') for r in rounds}!={1,2,3}
        or any(r.get('arm')!='candidate' or r.get('usable',0)<14 or r.get('critical')!=0
               or r.get('delivery_failed_ids')!=[] for r in rounds)):
        raise ValueError('Failed answer qualification')
    if (probes.get('reviewed')!=36 or probes.get('semantic_pass')!=36
        or q20.get('reviewed')!=3 or q20.get('semantic_pass')!=3):
        raise ValueError('Failed semantic qualification')


def prepare(output):
    spec=json.loads((HERE/'promotion-spec.json').read_text())
    batch=POC/'knowledge-expansion/arrays-v1'
    qualification=POC/'knowledge-expansion/arrays-condition-v2'
    check_pins(REPO,spec['pins'])
    foundation=json.loads((POC/'mcp_foundation/foundation.json').read_text())
    sources=json.loads((POC/'packaging/source-files.json').read_text())
    if foundation['id']!='formly-poc-foundation-6':raise ValueError('Expected foundation6')
    check_pins(POC,foundation['files']);check_pins(REPO,sources)
    protected=json.loads((qualification/'baseline-state.json').read_text())['files']
    check_pins(REPO,protected)
    for name in ['input-freeze.json','qualification-freeze.json']:
        pins=json.loads((batch/'test-output'/name).read_text());check_pins(batch,pins.get('files',pins))
    check_pins(REPO,json.loads((qualification/'test-output/qualification-freeze.json').read_text()))
    validate_qualification(
        json.loads((qualification/'test-output/qualification-1/qualification-decision.json').read_text()),
        json.loads((qualification/'test-output/REVIEW-PLANNER-SEMANTICS.json').read_text()),
        json.loads((qualification/'test-output/REVIEW-Q20-PREMISES.json').read_text()))
    manifest=json.loads((batch/'candidate-build/manifest.json').read_text())
    check_pins(batch,manifest['inputs'])
    candidate=batch/'candidate-build/knowledge.sqlite';accepted=POC/'build/knowledge.sqlite'
    if digest(candidate)!=spec['candidate_sha256'] or digest(accepted)!=spec['accepted_sha256']:
        raise ValueError('DB mismatch')
    old,new=rows(accepted),rows(candidate)
    if any(not old[t]<=new[t] for t in TABLES):raise ValueError('Candidate changed accepted rows')
    if len(new['facts'])!=85 or len(new['documents'])!=19:raise ValueError('Unexpected candidate count')
    additions=validate_additions(POC/'authored',batch/'candidate-inputs/authored',batch/'draft-authored')
    if json.loads((POC/'corpus/evidence-catalog.json').read_text())!=json.loads((batch/'candidate-inputs/evidence-catalog.json').read_text()):
        raise ValueError('Catalog changed')
    service=POC/'mcp_foundation/service.py'
    service_content=promoted_service(service.read_bytes())
    output.mkdir(parents=True,exist_ok=False)
    authored=output/'authored';shutil.copytree(POC/'authored',authored)
    for name,content in additions.items():(authored/name).write_bytes(content)
    sys.path.insert(0,str(POC))
    from kbcompiler.structured_source import build_sources
    build_sources(authored,REPO,POC/'corpus/evidence-catalog.json',output/'reproduced.sqlite')
    if rows(output/'reproduced.sqlite')!=new:raise ValueError('Canonical reproduction differs')
    expected={str(p.relative_to(REPO)):digest(p) for p in (POC/'authored').glob('*.json')}
    for p in [accepted,service,POC/'corpus/evidence-catalog.json',POC/'mcp_foundation/foundation.json',POC/'packaging/source-files.json']:
        expected[str(p.relative_to(REPO))]=digest(p)
    updated=json.loads(json.dumps(foundation));updated['id']='formly-poc-foundation-7'
    updated['files']['build/knowledge.sqlite']=spec['candidate_sha256']
    updated['files']['mcp_foundation/service.py']=hashlib.sha256(service_content).hexdigest()
    updated['components']['planner']='condition_candidate_v2'
    updated['knowledge']={'facts':85,'documents':19,'promotion':'knowledge-expansion/promotion-v6'}
    for name in ['CONTRACT.md','plan.schema.json','planner.py']:
        path='condition_candidate_v2/'+name
        updated['files'][path]=digest(POC/path)
    changes={}
    for name,content in additions.items():
        authored_name='poc/contextual-kb/authored/'+name
        sources[authored_name]=hashlib.sha256(content).hexdigest()
        changes[authored_name]=content
    changes.update({'poc/contextual-kb/build/knowledge.sqlite':candidate.read_bytes(),
             'poc/contextual-kb/mcp_foundation/service.py':service_content,
             'poc/contextual-kb/mcp_foundation/foundation.json':(json.dumps(updated,indent=2)+'\n').encode(),
             'poc/contextual-kb/packaging/source-files.json':(json.dumps(sources,indent=2)+'\n').encode()})
    unchanged_protected={name:sha for name,sha in protected.items() if name not in changes}
    receipt={'candidate_sha256':spec['candidate_sha256'],'accepted_sha256':spec['accepted_sha256'],
             'counts':{t:len(new[t]) for t in TABLES},'canonical_reproduction':'equal all five knowledge tables',
             'review':str(qualification/'REVIEW-FINAL.md'),'runtime_model_pins_preserved':len(foundation['files'])-2,
             'protected_files_preserved':len(unchanged_protected),'planner':'condition_candidate_v2',
             'authorized_changed_targets':sorted(changes),'new_runtime_pins':3}
    (output/'proposed-service.py').write_bytes(service_content)
    (output/'preflight.json').write_text(json.dumps(receipt,indent=2)+'\n')
    def postcheck():
        check_pins(POC,updated['files']);check_pins(REPO,sources);check_pins(REPO,unchanged_protected)
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

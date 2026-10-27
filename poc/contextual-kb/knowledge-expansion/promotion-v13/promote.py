"""Guarded data/manifest-only promotion. No runtime implementation edits."""
import argparse
import contextlib
import io
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sqlite3
import sys
import tempfile

HERE=Path(__file__).resolve().parent
POC=HERE.parents[1]
ROOT=POC.parents[1]
BATCH=HERE.parent/'api-contracts-v1'
QUAL=BATCH
OLD='7b2cfbde35ea38a4e12dc4a208b7ffcdb4a76b7509de2d18b653d601ef7c23b0'
NEW='f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09'
TABLES=('documents','facts','evidence','fact_evidence','fact_links','applicability','applicability_evidence','evidence_releases')

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
transaction=module('promotion_transaction',HERE.parent/'promotion-v7/promote.py')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def encoded(value):return (json.dumps(value,indent=2)+'\n').encode()
def read(path):return json.loads(Path(path).read_text())

def runtime_manifest(original,db_sha,mode):
    result=copy.deepcopy(original);result['files']['build/knowledge.sqlite']=db_sha
    result['id']='formly-poc-foundation-15' if mode=='model-backed' else 'formly-model-free-discovery-7'
    result['knowledge']={'facts':192,'documents':36,'promotion':'knowledge-expansion/promotion-v13','scope':'exact Formly6.3.12 core/Material'}
    return result

def require_decision(value):
    exact = dict(passes=True, cohort_counts_valid=True, target_requests=24, controls=8,
        regression_requests=8, candidate_controls_usable=8, candidate_regressions_usable=8,
        regressions=[], critical_unsupported_claims=[], passes_each_repeat=[True]*3,
        total_tool_calls=399)
    if any(value.get(k) != v for k,v in exact.items()) or not 22 <= value.get('candidate_target_usable',0) <= 24:
        raise ValueError('Qualification failed or incomplete')

def validate_sources(accepted,candidate,drafts):
    expected={p.name for p in accepted.glob('*.json')}|set(drafts)
    if {p.name for p in candidate.glob('*.json')}!=expected:raise ValueError('Unexpected authored source set')
    if any((accepted/name).exists() for name in drafts):raise ValueError('Already installed')
    for path in accepted.glob('*.json'):
        if path.read_bytes()!=(candidate/path.name).read_bytes():raise ValueError('Existing authored source drift')
    for name,content in drafts.items():
        if (candidate/name).read_bytes()!=content:raise ValueError('New authored source drift')

def validate_catalog(accepted,candidate,extra):
    expected=copy.deepcopy(accepted)
    ids=[r['id'] for r in expected['records']+extra]
    if len(ids)!=len(set(ids)) or any(r['id'] in expected['evidence_releases'] for r in extra):raise ValueError('Catalog collision')
    expected['records'].extend(copy.deepcopy(extra))
    expected['evidence_releases'].update({r['id']:'6.3.12' for r in extra})
    if candidate!=expected:raise ValueError('Catalog drift')


def rows(path):
    with sqlite3.connect(Path(path).resolve().as_uri()+'?mode=ro',uri=True) as db:
        if db.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('Broken FK')
        return {t:set(db.execute('SELECT * FROM '+t)) for t in TABLES}

def verify_pins(root,pins,excluded=()):
    for name,expected in pins.items():
        if name not in excluded:
            p=transaction.safe_path(root.resolve(),name)
            if sha(p)!=expected:raise ValueError('Pin drift: '+name)

def load_spec():
    spec=read(HERE/'promotion-spec.json')
    if spec['accepted_sha256']!=OLD or spec['candidate_sha256']!=NEW or len(spec['protected'])!=326 or len(spec['drafts'])!=9 or len(spec['old_authored'])!=27:
        raise ValueError('Unexpected promotion specification')
    return spec


def qualification():
    # Run the unchanged historical report before promotion. Its preservation check
    # intentionally requires the old installation; post-install verification below
    # has a separate exact, pinned contract rather than relaxing that old check.
    import subprocess
    result=subprocess.run([sys.executable,str(BATCH/'report.py')],check=True,capture_output=True,text=True)
    report=json.loads(result.stdout)
    if report!=read(BATCH/'test-output/results.json'):
        raise ValueError('Saved qualification differs from actual sealed receipts')
    require_decision(report)
    return report


def canonical(authored,catalog):
    sys.path.insert(0,str(POC))
    from kbcompiler.current_source import build_sources
    scratch=HERE/'test-output'
    scratch.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=scratch) as tmp:
        path=Path(tmp)/'knowledge.sqlite'
        build_sources(authored,ROOT,catalog,path)
        if sha(path)!=NEW or rows(path)!=rows(BATCH/'candidate-build/knowledge.sqlite'):
            raise ValueError('Canonical build differs from qualified DB')


def intended_changes(spec):
    verify_pins(ROOT,read(HERE/'review-pins.json'))
    verify_pins(ROOT,spec['source_additions'])
    manifest=read(BATCH/'candidate-build/manifest.json')
    verify_pins(BATCH,manifest['inputs'])
    if sha(BATCH/'candidate-build/knowledge.sqlite')!=NEW:
        raise ValueError('Candidate DB drift')
    drafts={name:(ROOT/origin).read_bytes() for name,origin in spec['drafts'].items()}
    candidate_authored=BATCH/'candidate-inputs/authored'
    if {p.name for p in candidate_authored.glob('*.json')} != set(spec['old_authored'])|set(drafts):
        raise ValueError('Unexpected candidate authored inventory')
    verify_pins(candidate_authored,spec['old_authored'])
    for name,content in drafts.items():
        if (candidate_authored/name).read_bytes()!=content:
            raise ValueError('Draft/candidate mismatch')
    if sum(len(read(ROOT/path)['facts']) for path in spec['drafts'].values())!=68:
        raise ValueError('Unexpected additive fact count')
    catalog=BATCH/'candidate-inputs/evidence-catalog.json'
    validate_catalog(spec['old_catalog'],read(catalog),spec['extra_records'])
    new=rows(BATCH/'candidate-build/knowledge.sqlite')
    if {table:len(new[table]) for table in TABLES}!=manifest['counts'] or (len(new['facts']),len(new['documents']))!=(192,36):
        raise ValueError('Wrong candidate counts')
    changes={'poc/contextual-kb/authored/'+name:content for name,content in drafts.items()}
    changes.update({
        'poc/contextual-kb/corpus/evidence-catalog.json':catalog.read_bytes(),
        'poc/contextual-kb/build/knowledge.sqlite':(BATCH/'candidate-build/knowledge.sqlite').read_bytes(),
        'poc/contextual-kb/mcp_foundation/foundation.json':encoded(runtime_manifest(spec['old_manifests']['model-backed'],NEW,'model-backed')),
        'poc/contextual-kb/mcp_runtime/model-free.json':encoded(runtime_manifest(spec['old_manifests']['model-free'],NEW,'model-free'))})
    sources=copy.deepcopy(spec['old_source_pins'])
    sources.update(spec['source_additions'])
    sources.update({'poc/contextual-kb/authored/'+name:hashlib.sha256(content).hexdigest() for name,content in drafts.items()})
    sources['poc/contextual-kb/corpus/evidence-catalog.json']=sha(catalog)
    changes['poc/contextual-kb/packaging/source-files.json']=encoded(sources)
    return changes


def verify_installed():
    """Verify the exact promoted contract without weakening historical preservation."""
    spec=load_spec();changes=intended_changes(spec)
    for name,content in changes.items():
        if transaction.safe_path(ROOT,name).read_bytes()!=content:
            raise ValueError('Installed target differs: '+name)
    if {p.name for p in (POC/'authored').glob('*.json')}!=set(spec['old_authored'])|set(spec['drafts']):
        raise ValueError('Installed authored inventory differs')
    verify_pins(POC/'authored',spec['old_authored'])
    verify_pins(ROOT,spec['protected'],changes)
    for path in ('mcp_runtime/model-free.json','mcp_foundation/foundation.json'):
        verify_pins(POC,read(POC/path)['files'])
    verify_pins(ROOT,read(POC/'packaging/source-files.json'))
    canonical(POC/'authored',POC/'corpus/evidence-catalog.json')
    return {'status':'verified','facts':192,'documents':36,'candidate_sha256':NEW,
            'preserved_files':len(set(spec['protected'])-set(changes))}


def prepare():
    spec=load_spec()
    verify_pins(ROOT,spec['before'])
    verify_pins(ROOT,spec['protected'])
    verify_pins(ROOT,spec['old_source_pins'])
    for manifest in spec['old_manifests'].values():verify_pins(POC,manifest['files'])
    changes=intended_changes(spec)
    qualification() # mandatory seal and three audited repeats, before any installed write
    validate_sources(POC/'authored',BATCH/'candidate-inputs/authored',
        {name:(ROOT/origin).read_bytes() for name,origin in spec['drafts'].items()})
    old=rows(POC/'build/knowledge.sqlite');new=rows(BATCH/'candidate-build/knowledge.sqlite')
    if any(not old[t]<=new[t] for t in TABLES):raise ValueError('Not baseline superset')
    canonical(BATCH/'candidate-inputs/authored',BATCH/'candidate-inputs/evidence-catalog.json')
    # Snapshot precisely the existing targets. Protected assets are checked both
    # before preparation and after installation; they are never written.
    expected=dict(spec['before'])
    return changes,expected,verify_installed


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--apply',action='store_true')
    mode.add_argument('--verify-installed',action='store_true')
    parser.add_argument('--name')
    args=parser.parse_args()
    if args.verify_installed:
        print(json.dumps(verify_installed(),indent=2));return
    if not args.name or Path(args.name).name!=args.name or args.name in ('.','..'):
        raise ValueError('Invalid run name')
    out=HERE/'test-output'/args.name
    if out.exists() or out.is_symlink():raise FileExistsError(out)
    changes,expected,postcheck=prepare()
    out.mkdir(parents=True,exist_ok=False)
    (out/'preflight.json').write_bytes(encoded(dict(targets=list(changes),before=expected,
        candidate_sha256=NEW,facts=192,documents=36)))
    if args.apply:
        receipt=transaction.guarded_replace(ROOT,changes,expected,out/'before',postcheck)
        (out/'receipt.json').write_bytes(encoded(receipt));print(receipt['status'])
    else:print('Preflight passed; no installed changes')

if __name__=='__main__':main()

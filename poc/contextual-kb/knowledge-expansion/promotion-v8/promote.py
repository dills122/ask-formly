"""Guarded data/manifest-only promotion. No runtime implementation edits."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile

HERE=Path(__file__).resolve().parent
POC=HERE.parents[1]
ROOT=POC.parents[1]
BATCH=HERE.parent/'json-schema-v1'
QUAL=HERE.parent/'json-schema-model-free-v1'
OLD='a0f102f1bad83dfec7c91148925187644e3092a3ca08cdaa88f586a7e1a0c106'
NEW='8487ca97dde24daff0a9dc655111e0066b7f3ce0dccf7c65d81f6f6087fa3c6c'
TABLES=('documents','facts','evidence','fact_evidence','fact_links','applicability','applicability_evidence','evidence_releases')

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
transaction=module('promotion_transaction',HERE.parent/'promotion-v7/promote.py')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def encoded(value):return (json.dumps(value,indent=2)+'\n').encode()
def read(path):return json.loads(Path(path).read_text())

def runtime_manifest(original,db_sha,mode):
    result=copy.deepcopy(original);result['files']['build/knowledge.sqlite']=db_sha
    result['id']='formly-poc-foundation-10' if mode=='model-backed' else 'formly-model-free-discovery-2'
    result['knowledge']={'facts':99,'documents':22,'promotion':'knowledge-expansion/promotion-v8','scope':'exact Formly6.3.12 core/Material'}
    return result

def require_decision(value):
    rounds=value.get('repeats',[])
    if (not all(value.get(k) is True for k in ('passed','complete','valid_judgments','mechanical_audit_passed'))
        or value.get('delivery_failures')!=0 or value.get('criticals')!=0
        or len(rounds)!=3 or {r.get('repeat') for r in rounds}!={1,2,3}
        or any(r.get('candidate_usable',0)<14 or r.get('all_controls') is not True or r.get('regressions')!=[] for r in rounds)):
        raise ValueError('Qualification failed or incomplete')

def validate_sources(accepted,candidate,draft):
    expected={p.name for p in accepted.glob('*.json')}|{'json-schema-conversion.json'}
    if {p.name for p in candidate.glob('*.json')}!=expected:raise ValueError('Unexpected authored source set')
    if (accepted/'json-schema-conversion.json').exists():raise ValueError('Already installed')
    for path in accepted.glob('*.json'):
        if path.read_bytes()!=(candidate/path.name).read_bytes():raise ValueError('Existing authored source drift')
    if (candidate/'json-schema-conversion.json').read_bytes()!=draft:raise ValueError('New authored source drift')

def rows(path):
    with sqlite3.connect(Path(path).resolve().as_uri()+'?mode=ro',uri=True) as db:
        if db.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('Broken FK')
        return {t:set(db.execute('SELECT * FROM '+t)) for t in TABLES}

def verify_pins(root,pins,excluded=()):
    for name,expected in pins.items():
        if name not in excluded:
            p=(root/name).resolve()
            if not p.is_relative_to(root.resolve()) or sha(p)!=expected:raise ValueError('Pin drift: '+name)

def prepare():
    sys.path.insert(0,str(POC))
    from kbcompiler.current_source import build_sources
    if sha(POC/'build/knowledge.sqlite')!=OLD:raise ValueError('Installed DB drift')
    if sha(BATCH/'candidate-build/knowledge.sqlite')!=NEW:raise ValueError('Candidate DB drift')
    decision=read(QUAL/'test-output/corrected/decision.json');require_decision(decision)
    assessment=module('qualification_gate',QUAL/'assessment.py')
    audit=read(QUAL/'test-output/corrected/mechanical-audit.json')
    if audit.get('passed') is not True or audit.get('protocol_scope_failures')!=0:raise ValueError('Protocol qualification failed')
    recomputed=assessment.gate(read(QUAL/'test-output/corrected/independent-grades.json'),audit['delivery_failures'])
    for key in recomputed:
        if recomputed[key]!=decision[key]:raise ValueError('Decision differs from independent grades')
    verify_pins(QUAL,read(QUAL/'freeze.json')['files']);verify_pins(QUAL,read(QUAL/'correction-freeze.json')['files'])
    if '**Ready**' not in (QUAL/'FINAL-REVIEW.md').read_text():raise ValueError('Missing final review')
    preservation=read(QUAL/'preservation.json')['files'];verify_pins(ROOT,preservation)
    manifest=read(BATCH/'candidate-build/manifest.json');verify_pins(BATCH,manifest['inputs'])
    draft=(BATCH/'draft-authored/json-schema-conversion.json').read_bytes()
    validate_sources(POC/'authored',BATCH/'candidate-inputs/authored',draft)
    if read(POC/'corpus/evidence-catalog.json')!=read(BATCH/'candidate-inputs/evidence-catalog.json'):raise ValueError('Catalog drift')
    accepted=rows(POC/'build/knowledge.sqlite');candidate=rows(BATCH/'candidate-build/knowledge.sqlite')
    if any(not accepted[t]<=candidate[t] for t in TABLES):raise ValueError('Not baseline superset')
    if (len(candidate['facts']),len(candidate['documents']))!=(99,22):raise ValueError('Wrong candidate counts')
    free=read(POC/'mcp_runtime/model-free.json');backed=read(POC/'mcp_foundation/foundation.json');sources=read(POC/'packaging/source-files.json')
    verify_pins(POC,free['files']);verify_pins(POC,backed['files']);verify_pins(ROOT,sources)
    def canonical(authored):
        with tempfile.TemporaryDirectory(dir=HERE/'test-output') as tmp:
            path=Path(tmp)/'knowledge.sqlite';build_sources(authored,ROOT,POC/'corpus/evidence-catalog.json',path)
            if rows(path)!=candidate or sha(path)!=NEW:raise ValueError('Canonical build differs from qualified DB')
    canonical(BATCH/'candidate-inputs/authored')
    changes={'poc/contextual-kb/authored/json-schema-conversion.json':draft,
        'poc/contextual-kb/build/knowledge.sqlite':(BATCH/'candidate-build/knowledge.sqlite').read_bytes(),
        'poc/contextual-kb/mcp_foundation/foundation.json':encoded(runtime_manifest(backed,NEW,'model-backed')),
        'poc/contextual-kb/mcp_runtime/model-free.json':encoded(runtime_manifest(free,NEW,'model-free'))}
    sources['poc/contextual-kb/authored/json-schema-conversion.json']=hashlib.sha256(draft).hexdigest()
    changes['poc/contextual-kb/packaging/source-files.json']=encoded(sources)
    expected={name:sha(ROOT/name) for name in changes if (ROOT/name).exists()}
    def postcheck():
        canonical(POC/'authored')
        for name,content in changes.items():
            if (ROOT/name).read_bytes()!=content:raise ValueError('Installed target differs: '+name)
        verify_pins(ROOT,preservation,changes)
        verify_pins(POC,read(POC/'mcp_runtime/model-free.json')['files'])
        verify_pins(POC,read(POC/'mcp_foundation/foundation.json')['files'])
        verify_pins(ROOT,read(POC/'packaging/source-files.json'))
    return changes,expected,postcheck

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--apply',action='store_true');p.add_argument('--name',required=True);a=p.parse_args()
    if not a.name or Path(a.name).name!=a.name or a.name in ('.','..'):raise ValueError('Invalid run name')
    out=HERE/'test-output'/a.name;out.mkdir(exist_ok=False)
    changes,expected,postcheck=prepare()
    (out/'preflight.json').write_bytes(encoded(dict(targets=list(changes),before=expected,candidate_sha256=NEW,facts=99,documents=22)))
    if a.apply:
        receipt=transaction.guarded_replace(ROOT,changes,expected,out/'before',postcheck)
        (out/'receipt.json').write_bytes(encoded(receipt));print(receipt['status'])
    else:print('Preflight passed; no installed changes')
if __name__=='__main__':main()

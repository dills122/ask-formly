"""Guarded data/manifest-only promotion. No runtime implementation edits."""
import argparse
import contextlib
import io
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
BATCH=HERE.parent/'material-radio-native-v1'
QUAL=BATCH
OLD='417e30ce3465b6d97bd0f013ef06db2fc35963236d983b6a4c9b88858c97bb09'
NEW='7b2cfbde35ea38a4e12dc4a208b7ffcdb4a76b7509de2d18b653d601ef7c23b0'
TABLES=('documents','facts','evidence','fact_evidence','fact_links','applicability','applicability_evidence','evidence_releases')

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
transaction=module('promotion_transaction',HERE.parent/'promotion-v7/promote.py')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def encoded(value):return (json.dumps(value,indent=2)+'\n').encode()
def read(path):return json.loads(Path(path).read_text())

def runtime_manifest(original,db_sha,mode):
    result=copy.deepcopy(original);result['files']['build/knowledge.sqlite']=db_sha
    result['id']='formly-poc-foundation-14' if mode=='model-backed' else 'formly-model-free-discovery-6'
    result['knowledge']={'facts':124,'documents':27,'promotion':'knowledge-expansion/promotion-v12','scope':'exact Formly6.3.12 core/Material'}
    return result

def require_decision(value):
    rounds=value.get('repeats',[])
    if (not all(value.get(k) is True for k in ('passed','complete','valid_judgments','mechanical_audit_passed'))
        or value.get('delivery_failures')!=0 or value.get('criticals')!=0
        or len(rounds)!=3 or {r.get('repeat') for r in rounds}!={1,2,3}
        or any(r.get('candidate_usable',0)<14 or r.get('all_controls') is not True or r.get('regressions')!=[] for r in rounds)):
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
            p=(root/name).resolve()
            if not p.is_relative_to(root.resolve()) or sha(p)!=expected:raise ValueError('Pin drift: '+name)

def prepare():
    sys.path.insert(0,str(POC))
    from kbcompiler.current_source import build_sources
    if sha(POC/'build/knowledge.sqlite')!=OLD:raise ValueError('Installed DB drift')
    if sha(BATCH/'candidate-build/knowledge.sqlite')!=NEW:raise ValueError('Candidate DB drift')
    verify_pins(QUAL,read(HERE/'review-pins.json'))
    verify_pins(QUAL,read(QUAL/'freeze.json')['files'])
    verify_pins(QUAL,read(QUAL/'final-review-freeze.json')['files'])
    sys.path.insert(0,str(QUAL))
    assessment=module('choice_results',QUAL/'results.py')
    stream=io.StringIO()
    with contextlib.redirect_stdout(stream):assessment.main()
    recomputed=json.loads(stream.getvalue())
    if recomputed!=read(QUAL/'QUALIFICATION-SUMMARY.json'):raise ValueError('Saved results differ from actual receipts')
    answers=read(QUAL/'answers-candidate.json')
    judgments=read(HERE/'answer-assessment.json')
    if set(judgments)!={row['id'] for row in answers} or any(v is not False for v in judgments.values()):raise ValueError('Critical or ungraded answer')
    decision=dict(passed=recomputed['candidate_meets_numeric_gate'],complete=recomputed['total_lookup_observations']==90 and recomputed['total_tool_calls']==150,
        valid_judgments=True,delivery_failures=0,criticals=0,mechanical_audit_passed=True,
        repeats=[dict(repeat=i+1,candidate_usable=n,all_controls=recomputed['candidate_controls_pass'],regressions=recomputed['baseline_supported_regressions']) for i,n in enumerate(recomputed['candidate']['usable_each_repeat'])])
    require_decision(decision)
    if '**Ready**' not in (QUAL/'FINAL-REVIEW.md').read_text():raise ValueError('Missing final review')
    preservation=read(QUAL/'baseline-state.json')['files'];verify_pins(ROOT,preservation)
    manifest=read(BATCH/'candidate-build/manifest.json');verify_pins(BATCH,manifest['inputs'])
    drafts={name:(BATCH/'draft-authored'/name).read_bytes() for name in ('material-radio-native.json','material-common-registration.json')}
    validate_sources(POC/'authored',BATCH/'candidate-inputs/authored',drafts)
    catalog_path=BATCH/'candidate-inputs/evidence-catalog.json'
    validate_catalog(read(POC/'corpus/evidence-catalog.json'),read(catalog_path),read(BATCH/'extra-evidence.json'))
    accepted=rows(POC/'build/knowledge.sqlite');candidate=rows(BATCH/'candidate-build/knowledge.sqlite')
    if any(not accepted[t]<=candidate[t] for t in TABLES):raise ValueError('Not baseline superset')
    if (len(candidate['facts']),len(candidate['documents']))!=(124,27):raise ValueError('Wrong candidate counts')
    free=read(POC/'mcp_runtime/model-free.json');backed=read(POC/'mcp_foundation/foundation.json');sources=read(POC/'packaging/source-files.json')
    verify_pins(POC,free['files']);verify_pins(POC,backed['files']);verify_pins(ROOT,sources)
    def canonical(authored,catalog):
        with tempfile.TemporaryDirectory(dir=HERE/'test-output') as tmp:
            path=Path(tmp)/'knowledge.sqlite';build_sources(authored,ROOT,catalog,path)
            if rows(path)!=candidate or sha(path)!=NEW:raise ValueError('Canonical build differs from qualified DB')
    canonical(BATCH/'candidate-inputs/authored',catalog_path)
    changes={**{'poc/contextual-kb/authored/'+name:content for name,content in drafts.items()},
        'poc/contextual-kb/corpus/evidence-catalog.json':catalog_path.read_bytes(),
        'poc/contextual-kb/build/knowledge.sqlite':(BATCH/'candidate-build/knowledge.sqlite').read_bytes(),
        'poc/contextual-kb/mcp_foundation/foundation.json':encoded(runtime_manifest(backed,NEW,'model-backed')),
        'poc/contextual-kb/mcp_runtime/model-free.json':encoded(runtime_manifest(free,NEW,'model-free'))}
    for name,content in drafts.items():sources['poc/contextual-kb/authored/'+name]=hashlib.sha256(content).hexdigest()
    sources['poc/contextual-kb/corpus/evidence-catalog.json']=sha(catalog_path)
    for name in ('source-notes.md','sources.md'):
        source=BATCH/name;sources[str(source.relative_to(ROOT))]=sha(source)
    changes['poc/contextual-kb/packaging/source-files.json']=encoded(sources)
    expected={name:sha(ROOT/name) for name in changes if (ROOT/name).exists()}
    def postcheck():
        canonical(POC/'authored',POC/'corpus/evidence-catalog.json')
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
    (out/'preflight.json').write_bytes(encoded(dict(targets=list(changes),before=expected,candidate_sha256=NEW,facts=124,documents=27)))
    if a.apply:
        receipt=transaction.guarded_replace(ROOT,changes,expected,out/'before',postcheck)
        (out/'receipt.json').write_bytes(encoded(receipt));print(receipt['status'])
    else:print('Preflight passed; no installed changes')
if __name__=='__main__':main()

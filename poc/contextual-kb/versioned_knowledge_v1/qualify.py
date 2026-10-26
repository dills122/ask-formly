"""Repeatable isolated migration and deterministic baseline retrieval comparison."""
import argparse
import hashlib
import json
import os
import sqlite3
import sys
from pathlib import Path
POC=Path(__file__).resolve().parent.parent
ROOT=POC.parents[1]
sys.path[:0]=[str(POC),str(POC/'mcp_v1')]
from versioned_knowledge_v1.compiler import migrate,build
from versioned_knowledge_v1.index import Index,ScopeError
from kbcompiler.question_pilot import PilotIndex
from mcp_v1.backend import citations_for

TABLES=('documents','facts','evidence','fact_evidence','fact_links','facts_fts')
QUERIES=(
 'How do I register a custom Formly field type and use it?',
 'Formly resetModel defaultValue and updateInitialValue',
 'Formly hide resetOnHide preserve hidden values',
 'Formly expressions props.disabled fieldChanges expressionChanges',
 'Formly validation messages and custom validators',
 'Formly FieldArrayType add remove fieldArray',
 'Formly select labelProp valueProp groupProp disabledProp',
 'Formly select compareWith strict equality',
 'Formly select Observable options subscription cleanup',
 'Formly multiple select selectAllOption change callback',
 'Formly model keyless groups keyed fieldGroup',
 'Formly extensions presets registration priority',
)

def connect(path):return sqlite3.connect(path.resolve().as_uri()+'?mode=ro',uri=True)

def rows(db,table):return sorted(db.execute('SELECT * FROM '+table).fetchall())

def preserved(receipt):
    mismatches=[]
    for path,expected in receipt['tracked_pins'].items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=expected:mismatches.append(path)
    for path,expected in receipt['foundation_pins'].items():
        if hashlib.sha256((POC/path).read_bytes()).hexdigest()!=expected:mismatches.append(path)
    if mismatches:raise ValueError('Protected bytes changed: '+str(mismatches))
    return {'tracked_files':len(receipt['tracked_pins']),'foundation_assets':len(receipt['foundation_pins']),'unchanged':True}

def run(output):
    baseline=json.loads((output/'baseline.json').read_text())
    preserved(baseline)
    migrated=output/'migrated';candidate=output/'candidate.sqlite'
    if not migrated.exists():migrate(POC/'authored',ROOT,POC/'corpus/evidence-catalog.json',migrated)
    build(migrated/'authored',ROOT,migrated/'catalog.json',candidate)
    second=output/'reproduced.sqlite';build(migrated/'authored',ROOT,migrated/'catalog.json',second)
    assert candidate.read_bytes()==second.read_bytes(),'Non-deterministic compilation'
    os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(POC/'agent_contract/advisory_lookup_v1/test-output/embed-cache'),HF_HUB_OFFLINE='1')
    old=connect(POC/'build/knowledge.sqlite');new=connect(candidate)
    try:
        parity={t:rows(old,t)==rows(new,t) for t in TABLES}
        assert all(parity.values()),parity
        assert new.execute('SELECT DISTINCT kind,value,basis FROM applicability').fetchall()==[('exact','6.3.12','direct')]
        original=PilotIndex(old);shared=Index(new,original.embedder);scoped=shared.for_scope('6.3.12')
        queries=list(QUERIES)+[f['context'] for f in original.facts.values()]
        results=[]
        for query in queries:
            comparisons={}
            for method in ('lexical','dense','hybrid'):
                for limit in (8,20):
                    a=getattr(original,method)(query,limit);b=getattr(scoped,method)(query,limit)
                    assert a==b,(query,method,limit,a,b)
                    comparisons[f'{method}_{limit}']=a
            ids=comparisons['hybrid_8'];a=citations_for(old,ids);b=scoped.citations(ids)
            assert a=={f:{k:v for k,v in c.items() if k!='applicability'} for f,c in b.items()}
            # Related expansion remains bounded and same when there is room.
            assert original.add_links(ids[:4],8)==scoped.add_links(ids[:4],8)
            results.append({'query':query,'rankings':comparisons,'citations_equal':True})
        try:shared.for_scope('7.0.0')
        except ScopeError:pass
        else:raise AssertionError('Migrated facts unexpectedly support v7')
        report={'baseline_commit':baseline['commit'],'facts':len(shared.ids),'semantic_tables_equal':parity,'deterministic_build':True,'queries':len(queries),'ranking_comparisons':len(queries)*6,'citation_comparisons':len(queries),'v7_unsupported':True,'candidate_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),'preservation':preserved(baseline),'comparisons':results}
        (output/'comparison.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k!='comparisons'},indent=2))
    finally:old.close();new.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'test-output')
    run(parser.parse_args().output)

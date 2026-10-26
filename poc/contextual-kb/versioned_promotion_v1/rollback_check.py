"""Rehearse old source+DB together in isolation; never restore over installation."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
HERE=Path(__file__).resolve().parent
POC=HERE.parent


def check():
    out=HERE/'test-output'
    hashes=json.loads((out/'before.json').read_text())
    for name,expected in hashes.items():
        if hashlib.sha256((out/'before'/name).read_bytes()).hexdigest()!=expected:raise ValueError('Rollback source drift')
    old_manifest=json.loads((out/'before/poc/contextual-kb/mcp_foundation/foundation.json').read_text())
    if hashlib.sha256((out/'rollback.sqlite').read_bytes()).hexdigest()!=old_manifest['files']['build/knowledge.sqlite']:raise ValueError('Rollback DB drift')
    with tempfile.TemporaryDirectory(dir=out) as tmp:
        root=Path(tmp);restored=root/'poc/contextual-kb'
        shutil.copytree(out/'before',root,dirs_exist_ok=True)
        (restored/'build').mkdir(exist_ok=True)
        shutil.copyfile(out/'rollback.sqlite',restored/'build/knowledge.sqlite')
        # Use only restored source paths, with existing read-only packages/cache.
        code='''import sys,json,sqlite3,hashlib
from pathlib import Path
p=Path(sys.argv[1]);sys.path[:0]=[str(p),str(p/'mcp_v1')]
from mcp_foundation.service import make_service
from mcp_v1.backend import Backend
from kbcompiler.structured_source import lint_sources
from kbcompiler.question_pilot import PilotIndex
assert Backend.__module__=='mcp_v1.backend'
assert not lint_sources(p/'authored',p.parents[1],p/'corpus/evidence-catalog.json')
with sqlite3.connect((p/'build/knowledge.sqlite').as_uri()+'?mode=ro',uri=True) as db:
 assert db.execute('select schema_version from build_info').fetchone()==(1,)
 index=PilotIndex(db)
 expected=json.loads(Path(sys.argv[2]).read_text())['comparisons'][:12]
 for row in expected:assert index.hybrid(row['query'],8)==row['rankings']['hybrid_8']
print(json.dumps({'old_code_and_db_compatible':True,'schema':1,'facts':len(index.ids),'rankings':12}))
'''
        env=dict(os.environ,FORMLY_PILOT_EMBED_CACHE=str(POC/'agent_contract/advisory_lookup_v1/test-output/embed-cache'),HF_HUB_OFFLINE='1')
        result=subprocess.run([str(POC/'mcp_v1/.venv/bin/python'),'-I','-B','-c',code,str(restored),str(POC/'versioned_knowledge_v1/test-output/comparison.json')],env=env,text=True,capture_output=True,check=True)
        report=json.loads(result.stdout)
        report['source_files_verified']=len(hashes)
        (out/'coordinated-rollback.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report))

if __name__=='__main__':check()

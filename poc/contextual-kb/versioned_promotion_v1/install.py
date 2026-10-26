"""Guarded installation of the exact reviewed schema2 artifact and authoring inputs."""
import hashlib
import importlib.util
import json
import sqlite3
import tempfile
from pathlib import Path
from versioned_knowledge_v1.compiler import build

POC=Path(__file__).resolve().parent.parent
ROOT=POC.parents[1]
HERE=Path(__file__).resolve().parent
CANDIDATE=POC/'versioned_knowledge_v1/test-output'
EXPECTED_DB='cc67af9eba6daa5024d671dd306dfd4ada4193e2663e05737d4db2bc39d9d63d'
REVIEWED_DB='a0f102f1bad83dfec7c91148925187644e3092a3ca08cdaa88f586a7e1a0c106'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def install():
    spec=importlib.util.spec_from_file_location('guarded_promotion',POC/'knowledge-expansion/promotion-v7/promote.py')
    transaction=importlib.util.module_from_spec(spec);spec.loader.exec_module(transaction)
    if sha(POC/'build/knowledge.sqlite')!=EXPECTED_DB:raise ValueError('Installed baseline drift')
    if sha(CANDIDATE/'candidate.sqlite')!=REVIEWED_DB:raise ValueError('Candidate drift')
    before=json.loads((HERE/'test-output/before/poc/contextual-kb/mcp_foundation/foundation.json').read_text())
    # All existing pins except the deliberately edited transport/launcher remain exact.
    edits={'mcp_foundation/launcher.py','mcp_v1/server.py'}
    for name,expected in before['files'].items():
        if name not in edits and sha(POC/name)!=expected:raise ValueError('Protected asset drift: '+name)
    with tempfile.TemporaryDirectory(dir=HERE/'test-output') as tmp:
        rebuilt=Path(tmp)/'new.sqlite'
        build(CANDIDATE/'migrated/authored',ROOT,CANDIDATE/'migrated/catalog.json',rebuilt)
        if sha(rebuilt)!=REVIEWED_DB:raise ValueError('Canonical candidate differs')
    changes={str(Path('poc/contextual-kb/authored')/p.name):p.read_bytes() for p in (CANDIDATE/'migrated/authored').glob('*.json')}
    changes['poc/contextual-kb/corpus/evidence-catalog.json']=(CANDIDATE/'migrated/catalog.json').read_bytes()
    changes['poc/contextual-kb/build/knowledge.sqlite']=(CANDIDATE/'candidate.sqlite').read_bytes()
    manifest=json.loads((POC/'mcp_foundation/foundation.json').read_text())
    manifest['id']='formly-poc-foundation-9'
    manifest['components']['knowledge']='schema2 exact applicability; versioned_knowledge_v1'
    for name in ('mcp_foundation/launcher.py','mcp_v1/server.py','mcp_foundation/versioned.py','kbcompiler/structured_source.py','versioned_knowledge_v1/backend.py','versioned_knowledge_v1/index.py','versioned_knowledge_v1/context.py','versioned_knowledge_v1/compiler.py'):
        manifest['files'][name]=sha(POC/name)
    manifest['files']['build/knowledge.sqlite']=REVIEWED_DB
    changes['poc/contextual-kb/mcp_foundation/foundation.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    sources=json.loads((POC/'packaging/source-files.json').read_text())
    for name,expected_hash in sources.items():
        if name!='poc/contextual-kb/kbcompiler/__main__.py' and sha(ROOT/name)!=expected_hash:
            raise ValueError('Unexpected source drift: '+name)
    for name in sources:
        sources[name]=hashlib.sha256(changes[name]).hexdigest() if name in changes else sha(ROOT/name)
    for name in ('poc/contextual-kb/kbcompiler/current_source.py','poc/contextual-kb/versioned_knowledge_v1/compiler.py'):
        sources[name]=sha(ROOT/name)
    changes['poc/contextual-kb/packaging/source-files.json']=(json.dumps(sources,indent=2)+'\n').encode()
    expected={name:sha(ROOT/name) for name in changes}
    def verify():
        if sha(POC/'build/knowledge.sqlite')!=REVIEWED_DB:raise ValueError('Installed DB mismatch')
        with tempfile.TemporaryDirectory(dir=HERE/'test-output') as tmp:
            path=Path(tmp)/'canonical.sqlite';build(POC/'authored',ROOT,POC/'corpus/evidence-catalog.json',path)
            if sha(path)!=REVIEWED_DB:raise ValueError('Installed canonical mismatch')
    receipt=transaction.guarded_replace(ROOT,changes,expected,HERE/'test-output/recovery',verify)
    (HERE/'test-output/receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(receipt['status'])

if __name__=='__main__':install()

"""Opt-in schema 2 compiler. Never writes an existing database or source tree."""
import copy
import hashlib
import json
import os
import re
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path
from kbcompiler.structured_source import build_sources, lint_sources, load_json_strict

EXACT = re.compile(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z')
MAJOR = re.compile(r'(0|[1-9][0-9]*)\Z')


def release(value):
    if not isinstance(value,str) or not EXACT.fullmatch(value):
        raise ValueError('Expected a canonical stable exact release')
    return value


def write_json(path, value):
    path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')


def migrate(source, root, catalog_path, destination):
    """Explicit one-way conversion, retaining each legacy evidence release."""
    source,root,catalog_path,destination=map(Path,(source,root,catalog_path,destination))
    if destination.exists():raise FileExistsError(destination)
    errors=lint_sources(source,root,catalog_path)
    if errors:raise ValueError('\n'.join(errors))
    catalog=load_json_strict(catalog_path)
    release(catalog['baseline'])
    catalog['schema_version']=2
    catalog['evidence_releases']={r['id']:catalog['baseline'] for r in catalog['records']}
    docs=[]
    for path in sorted(source.glob('*.json')):
        doc=load_json_strict(path);doc['schema_version']=2
        for fact in doc['facts']:
            fact['applicability']=[{'scope':{'kind':'exact','value':doc['formly_version']},'basis':'direct','evidence_ids':list(fact['evidence_ids'])}]
        docs.append((path.name,doc))
    destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as tmp:
        staged=Path(tmp)/'converted';(staged/'authored').mkdir(parents=True)
        for name,doc in docs:write_json(staged/'authored'/name,doc)
        write_json(staged/'catalog.json',catalog)
        # Rename only into an absent destination; no existing source is modified.
        if destination.exists():raise FileExistsError(destination)
        staged.rename(destination)


def overlaps(a,b):
    ak,av=a['scope']['kind'],a['scope']['value']
    bk,bv=b['scope']['kind'],b['scope']['value']
    return av==bv if ak==bk else av.split('.')[0]==bv.split('.')[0]


def validate(documents,catalog):
    if not {'schema_version','baseline','records','evidence_releases'}<=set(catalog) or set(catalog)-{'schema_version','baseline','records','evidence_releases','source_inputs'} or type(catalog['schema_version']) is not int or catalog['schema_version']!=2:
        raise ValueError('Unsupported catalog format')
    release(catalog['baseline'])
    records=catalog['records']; releases=catalog['evidence_releases']
    if not isinstance(records,list) or not isinstance(releases,dict):raise ValueError('Invalid evidence catalog')
    ids=[r['id'] for r in records]
    if len(set(ids))!=len(ids) or set(ids)!=set(releases):raise ValueError('Evidence release identities must be unique and complete')
    for v in releases.values():release(v)
    facts={};edges={}
    for doc in documents:
        if type(doc.get('schema_version')) is not int or doc['schema_version']!=2:raise ValueError('Unsupported authored format')
        release(doc['formly_version'])
        if doc['adapter'] not in ('core','material'):raise ValueError('Unsupported adapter')
        for fact in doc['facts']:
            fid=f"{doc['id']}/{fact['id']}"
            if fid in facts:raise ValueError('Duplicate fact')
            facts[fid]=fact;edges[fid]=[]
            apps=fact.get('applicability')
            if not isinstance(apps,list) or not apps:raise ValueError('Missing applicability')
            scopes=set()
            for app in apps:
                if not isinstance(app,dict) or not {'scope','basis','evidence_ids'}<=set(app) or set(app)-{'scope','basis','evidence_ids','reason'}:raise ValueError('Invalid applicability fields')
                scope=app['scope']
                if not isinstance(scope,dict) or set(scope)!={'kind','value'}:raise ValueError('Invalid scope')
                kind,value=scope['kind'],scope['value']
                if kind not in ('exact','major') or not isinstance(value,str) or not (EXACT if kind=='exact' else MAJOR).fullmatch(value):raise ValueError('Invalid scope')
                if (kind,value) in scopes:raise ValueError('Duplicate scope')
                scopes.add((kind,value))
                if app['basis'] not in ('direct','inferred'):raise ValueError('Invalid basis')
                if app['basis']=='inferred' and not isinstance(app.get('reason'),str):raise ValueError('Inferred applicability requires rationale')
                if 'reason' in app and (not isinstance(app['reason'],str) or not app['reason'].strip()):raise ValueError('Empty rationale')
                evidence=app['evidence_ids']
                if not isinstance(evidence,list) or not evidence or any(not isinstance(x,str) for x in evidence) or len(set(evidence))!=len(evidence) or not set(evidence)<=set(fact['evidence_ids']):raise ValueError('Invalid applicability evidence')
                if not set(evidence)<=set(releases):raise ValueError('Unknown evidence')
                if app['basis']=='direct' and not any(releases[e]==value if kind=='exact' else releases[e].split('.')[0]==value for e in evidence):raise ValueError('Direct applicability needs evidence from that scope')
            for link in fact['related']:
                if link['kind']=='replaces':edges[fid].append(link['target'])
    visiting=set();ancestors={}
    def visit(fid):
        if fid in visiting:raise ValueError('Replacement cycle')
        if fid in ancestors:return ancestors[fid]
        visiting.add(fid)
        inherited=set()
        for target in edges[fid]:
            if target not in facts:raise ValueError('Missing replacement target')
            inherited.add(target)
            inherited.update(visit(target))
        for ancestor in inherited:
            if any(overlaps(a,b) for a in facts[fid]['applicability'] for b in facts[ancestor]['applicability']):
                raise ValueError('Replacement applicability overlaps an ancestor; explicit boundaries required')
        visiting.remove(fid)
        ancestors[fid]=inherited
        return inherited
    for fid in facts:visit(fid)


def build(source, root, catalog_path, database):
    """Compile only v2, validating legacy content via a temporary v1 projection."""
    source,root,catalog_path,database=map(Path,(source,root,catalog_path,database))
    if database.exists() or database.is_symlink():raise FileExistsError(database)
    paths=sorted(source.glob('*.json'))
    documents=[load_json_strict(p) for p in paths]
    catalog=load_json_strict(catalog_path)
    try:validate(documents,catalog)
    except (KeyError,TypeError,AttributeError) as exc:raise ValueError('Malformed versioned source') from exc
    if 'source_inputs' in catalog:
        inputs=catalog['source_inputs']
        if not isinstance(inputs,dict) or set(inputs)!={'upstream_path','upstream_sha256','examples_path','examples_sha256'}:raise ValueError('Invalid catalog provenance')
        for prefix in ('upstream','examples'):
            path=(root/inputs[prefix+'_path']).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=inputs[prefix+'_sha256']:raise ValueError('Catalog source provenance changed')
    database.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=database.parent) as tmp:
        tmp=Path(tmp); projected=tmp/'authored';projected.mkdir()
        for path,original in zip(paths,documents):
            doc=copy.deepcopy(original);doc['schema_version']=1
            # The legacy validator has a single-catalog baseline check. This
            # projection is only for unchanged content/provenance validation.
            # Original evidence releases and authored scopes were validated above.
            doc['formly_version']=catalog['baseline']
            for fact in doc['facts']:
                del fact['applicability']
                for link in fact['related']:
                    if link['kind']=='replaces':link['kind']='see_also'
            write_json(projected/path.name,doc)
        legacy_catalog=tmp/'catalog.json'
        write_json(legacy_catalog,{'baseline':catalog['baseline'],'records':catalog['records']})
        candidate=tmp/'candidate.sqlite'
        build_sources(projected,root,legacy_catalog,candidate)
        with closing(sqlite3.connect(candidate)) as db:
            db.execute('PRAGMA foreign_keys=ON')
            db.executescript('''
                CREATE TABLE evidence_releases (
                    evidence_id TEXT PRIMARY KEY REFERENCES evidence(id), release TEXT NOT NULL);
                CREATE TABLE applicability (
                    fact_id TEXT NOT NULL REFERENCES facts(id), kind TEXT NOT NULL CHECK(kind IN ('exact','major')),
                    value TEXT NOT NULL, basis TEXT NOT NULL CHECK(basis IN ('direct','inferred')), reason TEXT,
                    PRIMARY KEY(fact_id,kind,value), CHECK(basis!='inferred' OR (reason IS NOT NULL AND length(trim(reason))>0)));
                CREATE TABLE applicability_evidence (
                    fact_id TEXT NOT NULL, kind TEXT NOT NULL, value TEXT NOT NULL, evidence_id TEXT NOT NULL,
                    PRIMARY KEY(fact_id,kind,value,evidence_id),
                    FOREIGN KEY(fact_id,kind,value) REFERENCES applicability(fact_id,kind,value),
                    FOREIGN KEY(fact_id,evidence_id) REFERENCES fact_evidence(fact_id,evidence_id));
                DROP TABLE fact_links;
                CREATE TABLE fact_links (
                    source_fact_id TEXT NOT NULL REFERENCES facts(id), target_fact_id TEXT NOT NULL REFERENCES facts(id),
                    kind TEXT NOT NULL CHECK(kind IN ('see_also','replaces')),
                    PRIMARY KEY(source_fact_id,target_fact_id,kind),CHECK(source_fact_id!=target_fact_id));
            ''')
            for (eid,) in db.execute('SELECT id FROM evidence ORDER BY id').fetchall():
                db.execute('INSERT INTO evidence_releases VALUES (?,?)',(eid,catalog['evidence_releases'][eid]))
            for doc in documents:
                db.execute('UPDATE documents SET formly_version=? WHERE id=?',(doc['formly_version'],doc['id']))
                for fact in doc['facts']:
                    fid=f"{doc['id']}/{fact['id']}"
                    for app in fact['applicability']:
                        key=(fid,app['scope']['kind'],app['scope']['value'])
                        db.execute('INSERT INTO applicability VALUES (?,?,?,?,?)',(*key,app['basis'],app.get('reason')))
                        for eid in sorted(app['evidence_ids']):db.execute('INSERT INTO applicability_evidence VALUES (?,?,?,?)',(*key,eid))
                    for link in fact['related']:db.execute('INSERT INTO fact_links VALUES (?,?,?)',(fid,link['target'],link['kind']))
            # Length framing avoids ambiguous concatenation of authoring inputs.
            parts=[catalog_path.read_bytes(),*[p.read_bytes() for p in paths],*[(root/d['derived_from']['path']).read_bytes() for d in documents]]
            digest=hashlib.sha256(b''.join(len(p).to_bytes(8,'big')+p for p in parts)).hexdigest()
            db.execute('UPDATE build_info SET schema_version=2,input_sha256=?',(digest,))
            if db.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('Broken references')
            db.commit()
            if db.execute('PRAGMA integrity_check').fetchone()!=('ok',):raise ValueError('DB integrity failure')
        # Atomic publication with exclusive creation, including races/symlinks.
        os.link(candidate,database)

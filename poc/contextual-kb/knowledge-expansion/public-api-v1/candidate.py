"""Isolated expansion build; never selects the installed DB as output."""
import hashlib
import json
import shutil
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

HERE = Path(__file__).resolve().parent
POC = HERE.parents[1]
REPO = POC.parents[1]
sys.path.insert(0, str(POC))
from kbcompiler.current_source import lint_sources, build_sources
sys.path.insert(0,str(HERE.parent/'admission'))
from eligibility import verify_retrieval_eligibility


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def assert_digest(path, expected):
    if digest(path) != expected:
        raise ValueError(f'Preservation mismatch: {path}')


def fresh_directory(root, name):
    root = Path(root).absolute()
    if root != root.resolve() or not root.is_dir():
        raise ValueError('Root must be an existing canonical nonsymlink directory')
    if not name or Path(name).name != name or name in ('.', '..'):
        raise ValueError('Output must be a direct named child')
    target = root / name
    if target.exists() or target.is_symlink():
        raise FileExistsError(target)
    target.mkdir()  # Exclusive creation; existing directories are never reused.
    return target


def connect_ro(path):
    db = sqlite3.connect(Path(path).resolve().as_uri()+'?mode=ro', uri=True)
    db.execute('PRAGMA query_only=ON')
    return db


def compare_rows(accepted, candidate):
    old,new=connect_ro(accepted),connect_ro(candidate)
    try:
        counts={}
        for table in ('documents','facts','evidence','fact_evidence','fact_links','applicability','applicability_evidence','evidence_releases'):
            original=set(old.execute('SELECT * FROM '+table));expanded=set(new.execute('SELECT * FROM '+table))
            if not original<=expanded:raise ValueError('Candidate changed accepted '+table)
            counts[table]=len(expanded)
        return counts
    finally:old.close();new.close()


def verify_superset(accepted,candidate):
    counts=compare_rows(accepted,candidate)
    db=connect_ro(candidate)
    try:
        if db.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('Broken references')
        if db.execute('SELECT DISTINCT kind,value FROM applicability').fetchall()!=[('exact','6.3.12')]:raise ValueError('Unexpected coverage expansion')
        for path,sha,quote,start,end in db.execute('SELECT d.source_path,d.source_sha256,f.source_quote,f.source_start_offset,f.source_end_offset FROM facts f JOIN documents d ON d.id=f.doc_id'):
            source=REPO/path;assert_digest(source,sha)
            if source.read_text()[start:end]!=quote:raise ValueError('Source offset mismatch')
        return counts
    finally:db.close()


def preserved():
    state=json.loads((HERE/'baseline-state.json').read_text())
    assert_digest(POC/'build/knowledge.sqlite',state['installed_db_sha256'])
    for name,sha in state['files'].items(): assert_digest(REPO/name,sha)
    for filename in ('freeze.json','run-freeze.json'):
        freeze=HERE/filename
        if freeze.exists():
            for name,sha in json.loads(freeze.read_text())['files'].items():assert_digest(HERE/name,sha)
    return state


def accepted_inputs():
    snapshot = json.loads((HERE/'accepted-baseline.json').read_text())
    def inside(name):
        path = POC/name
        if path != path.resolve() or not path.resolve().is_relative_to(POC.resolve()):
            raise ValueError('Accepted input escapes POC or is aliased')
        return path
    authored, catalog, db = [inside(snapshot[k]) for k in ('authored','catalog','database')]
    expected_files = {str(p.relative_to(POC)) for p in authored.glob('*.json')} | {str(catalog.relative_to(POC))}
    if set(snapshot['inputs']) != expected_files:
        raise ValueError('Accepted source inventory changed')
    for name, sha in snapshot['inputs'].items():
        assert_digest(inside(name), sha)
    assert_digest(db, snapshot['sha256'])
    with closing(connect_ro(db)) as connection:
        actual = {table:connection.execute('SELECT COUNT(*) FROM '+table).fetchone()[0] for table in ('facts','documents')}
    if actual != snapshot['counts'] or actual != {'facts':176,'documents':33}:
        raise ValueError('Unexpected accepted baseline size')
    return authored, catalog, db


def checked_database(arm):
    if arm not in ('baseline','candidate'): raise ValueError('Unknown arm')
    if arm=='baseline':
        _,_,path=accepted_inputs()
        expected=json.loads((HERE/'accepted-baseline.json').read_text())['sha256']
    else:
        manifest=json.loads((HERE/'candidate-build/manifest.json').read_text())
        path=HERE/'candidate-build/knowledge.sqlite'
        if manifest['database']!='candidate-build/knowledge.sqlite' or path!=path.resolve():
            raise ValueError('Candidate must be isolated and canonical')
        expected=manifest['sha256']
        for name,sha in manifest['inputs'].items():
            source=(HERE/name).resolve()
            if not source.is_relative_to(HERE):raise ValueError('Candidate input escapes batch')
            assert_digest(source,sha)
    assert_digest(path,expected)
    return path,expected


def verify_candidate_counts(counts):
    expected=json.loads((HERE/'admission-spec.json').read_text())['expected_counts']
    if any(counts[key] != expected[key] for key in ('facts','documents')):
        raise ValueError('Unexpected candidate size')


def add_candidate_evidence(catalog, extra):
    import copy
    result = copy.deepcopy(catalog)
    ids = [r['id'] for r in result['records'] + extra]
    if len(ids) != len(set(ids)) or any(r['id'] in result['evidence_releases'] for r in extra):
        raise ValueError('Evidence ID collision')
    result['records'].extend(copy.deepcopy(extra))
    result['evidence_releases'].update({r['id']: '6.3.12' for r in extra})
    return result


def build():
    if not (HERE/"freeze.json").is_file():
        raise FileNotFoundError("Freeze inputs before building")
    state = preserved()
    baseline_authored, baseline_catalog, baseline_db = accepted_inputs()
    # Refuse any existing/aliased output before creating either directory.
    for name in ('candidate-inputs', 'candidate-build'):
        path = HERE/name
        if path.exists() or path.is_symlink():
            raise FileExistsError(path)
    inputs = fresh_directory(HERE, 'candidate-inputs')
    output = fresh_directory(HERE, 'candidate-build')
    authored = inputs/'authored'; authored.mkdir()
    for folder in (baseline_authored, HERE/'draft-authored'):
        for source in sorted(folder.glob('*.json')):
            target = authored/source.name
            with target.open('xb') as handle:
                handle.write(source.read_bytes())
    catalog = json.loads(baseline_catalog.read_text())
    catalog = add_candidate_evidence(catalog, json.loads((HERE/'extra-evidence.json').read_text()))
    catalog_path = inputs/'evidence-catalog.json'
    catalog_path.write_text(json.dumps(catalog, indent=2)+'\n')
    errors = lint_sources(authored, REPO, catalog_path)
    if errors: raise ValueError(errors)
    target = output/'knowledge.sqlite'
    build_sources(authored, REPO, catalog_path, target)
    counts = verify_superset(baseline_db, target)
    eligibility = verify_retrieval_eligibility(target, baseline_db)
    verify_candidate_counts(counts)
    preserved()
    manifest = dict(retrieval_eligibility=eligibility, database=str(target.relative_to(HERE)), sha256=digest(target),
                    accepted_sha256=digest(baseline_db), installed_sha256=state['installed_db_sha256'], counts=counts,
                    inputs={str(p.relative_to(HERE)):digest(p) for p in sorted(inputs.rglob('*.json'))})
    for source in (HERE/'source-verification.json',HERE/'freeze.json'):
        manifest['inputs'][str(source.relative_to(HERE))] = digest(source)
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest


if __name__ == '__main__':
    print(json.dumps(build(), indent=2))

"""Isolated expansion build; never selects the installed DB as output."""
import hashlib
import json
import shutil
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
POC = HERE.parents[1]
REPO = POC.parents[1]
EXPECTED_FACTS = 104
EXPECTED_DOCUMENTS = 23
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
    freeze=HERE/'freeze.json'
    if freeze.exists():
        for name,sha in json.loads(freeze.read_text())['files'].items():assert_digest(HERE/name,sha)
    return state


def checked_database(arm):
    if arm not in ('baseline','candidate'): raise ValueError('Unknown arm')
    if arm=='baseline':
        path=POC/'build/knowledge.sqlite'
        expected=json.loads((HERE/'baseline-state.json').read_text())['installed_db_sha256']
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
    if counts['facts'] != EXPECTED_FACTS or counts['documents'] != EXPECTED_DOCUMENTS:
        raise ValueError('Unexpected candidate size')


def build():
    if not (HERE/"freeze.json").is_file():
        raise FileNotFoundError("Freeze inputs before building")
    state = preserved()
    # Refuse any existing/aliased output before creating either directory.
    for name in ('candidate-inputs', 'candidate-build'):
        path = HERE/name
        if path.exists() or path.is_symlink():
            raise FileExistsError(path)
    inputs = fresh_directory(HERE, 'candidate-inputs')
    output = fresh_directory(HERE, 'candidate-build')
    authored = inputs/'authored'; authored.mkdir()
    for folder in (POC/'authored', HERE/'draft-authored'):
        for source in sorted(folder.glob('*.json')):
            target = authored/source.name
            with target.open('xb') as handle:
                handle.write(source.read_bytes())
    catalog = json.loads((POC/'corpus/evidence-catalog.json').read_text())
    extra = []  # All evidence IDs already exist in the promoted catalog.
    ids = [record['id'] for record in catalog['records']+extra]
    if len(set(ids)) != len(ids):
        raise ValueError('Evidence ID collision')
    catalog['records'] += extra
    catalog_path = inputs/'evidence-catalog.json'
    catalog_path.write_text(json.dumps(catalog, indent=2)+'\n')
    errors = lint_sources(authored, REPO, catalog_path)
    if errors: raise ValueError(errors)
    target = output/'knowledge.sqlite'
    build_sources(authored, REPO, catalog_path, target)
    counts = verify_superset(POC/'build/knowledge.sqlite', target)
    eligibility = verify_retrieval_eligibility(target, POC/'build/knowledge.sqlite')
    verify_candidate_counts(counts)
    preserved()
    manifest = dict(retrieval_eligibility=eligibility, database=str(target.relative_to(HERE)), sha256=digest(target),
                    accepted_sha256=state['installed_db_sha256'], counts=counts,
                    inputs={str(p.relative_to(HERE)):digest(p) for p in sorted(inputs.rglob('*.json'))})
    for source in (HERE/'source-verification.json',HERE/'freeze.json'):
        manifest['inputs'][str(source.relative_to(HERE))] = digest(source)
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest


if __name__ == '__main__':
    print(json.dumps(build(), indent=2))

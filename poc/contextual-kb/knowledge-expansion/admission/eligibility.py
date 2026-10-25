"""Read-only admission gate for the frozen retriever's version/adapter profile."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sqlite3

POC = Path(__file__).resolve().parents[2]
PROFILE_SOURCE = POC/'kbcompiler/question_pilot.py'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runtime_profile():
    # This module has only stdlib imports at module scope. Model dependencies are
    # lazy inside PilotIndex.__init__, which this admission check never invokes.
    spec = importlib.util.spec_from_file_location('_admission_frozen_question_pilot',PROFILE_SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not isinstance(module.BASELINE,str) or not module.BASELINE or not isinstance(module.ADAPTERS,(tuple,list)) or not module.ADAPTERS or not all(isinstance(a,str) and a for a in module.ADAPTERS):
        raise ValueError('Frozen retriever profile is malformed')
    return {'baseline':module.BASELINE,'adapters':list(module.ADAPTERS),
            'source':str(PROFILE_SOURCE),'sha256':digest(PROFILE_SOURCE)}


def read_facts(path):
    path = Path(path).resolve()
    before = digest(path)  # Also refuses missing files before SQLite connects.
    connection = sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)
    try:
        connection.execute('PRAGMA query_only=ON')
        rows = connection.execute('''SELECT f.id,d.id,d.formly_version,d.adapter
            FROM facts f LEFT JOIN documents d ON d.id=f.doc_id ORDER BY f.id''').fetchall()
    finally:
        connection.close()
    if digest(path) != before:
        raise ValueError(f'Database changed during eligibility check: {path}')
    return rows,{'path':str(path),'sha256':before}


def verify_retrieval_eligibility(candidate_db, accepted_db=None):
    """Reject unreachable candidate facts; does not replace row/provenance checks.

    Both lexical search and dense eligibility use these same frozen constants.
    This guard proves only metadata eligibility, not ranking or answer quality.
    """
    profile = runtime_profile()
    rows,candidate = read_facts(candidate_db)
    failures = []
    for fact_id,document_id,version,adapter in rows:
        if document_id is None:
            failures.append(f'{fact_id}: missing document')
        elif version != profile['baseline'] or adapter not in profile['adapters']:
            failures.append(f'{fact_id}: version={version!r}, adapter={adapter!r}')
    if failures:
        raise ValueError('Facts are ineligible for frozen retrieval: '+ '; '.join(failures))
    old_ids = set()
    accepted = None
    if accepted_db is not None:
        old_rows,accepted = read_facts(accepted_db)
        old_ids = {row[0] for row in old_rows}
    ids = [row[0] for row in rows]
    return {'ok':True,'profile':profile,'candidate':candidate,'accepted':accepted,
            'eligible_fact_ids':ids,'new_fact_ids':sorted(set(ids)-old_ids),
            'scope':'Version/adapter eligibility only; not rank, provenance, row-preservation or answer-quality proof.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate',type=Path,required=True)
    parser.add_argument('--accepted',type=Path)
    args = parser.parse_args()
    print(json.dumps(verify_retrieval_eligibility(args.candidate,args.accepted),indent=2))


if __name__ == '__main__':main()

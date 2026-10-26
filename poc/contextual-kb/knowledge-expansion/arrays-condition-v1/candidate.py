"""Read-only artifact selection and preservation; no compiler/build entry point."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
POC = HERE.parents[1]
REPO = POC.parents[1]
ORIGINAL = HERE.parent/'arrays-v1'
DB_SHA256 = 'bbb55e168cc81e60927a1bf146af767cd8ab6c9999875239ea28a879487531ff'
sys.path.insert(0, str(POC))
COPIED = ('qualification-cases.json','assess.py','summarize.py','delivery.py','GRADER.md','grade.schema.json','answer.schema.json','draft-authored/array-operations.json','draft-authored/array-repeat-example.json')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def assert_digest(path, expected):
    if digest(path) != expected:
        raise ValueError(f'Preservation mismatch: {path}')


def preserved():
    state = json.loads((HERE/'baseline-state.json').read_text())
    assert_digest(POC/'build/knowledge.sqlite',state['installed_db_sha256'])
    for name, sha in state['files'].items():
        assert_digest(REPO/name,sha)
    for name in COPIED:
        assert_digest(HERE/name,digest(ORIGINAL/name))
    return state


def checked_database(arm):
    if arm != 'candidate':
        raise ValueError('This qualification accepts only the frozen candidate')
    preserved()
    path = ORIGINAL/'candidate-build/knowledge.sqlite'
    if path != path.resolve():
        raise ValueError('Candidate DB must be canonical')
    manifest = json.loads((ORIGINAL/'candidate-build/manifest.json').read_text())
    if manifest['database'] != 'candidate-build/knowledge.sqlite' or manifest['sha256'] != DB_SHA256:
        raise ValueError('Unexpected candidate manifest')
    if manifest['counts']['facts'] != 85 or manifest['counts']['documents'] != 19:
        raise ValueError('Unexpected candidate counts')
    assert_digest(path, DB_SHA256)
    return path, DB_SHA256

"""Development-only extraction probe; never produces or executes a retrieval plan."""
import hashlib
import json
import os
from pathlib import Path
from time import perf_counter

HERE = Path(__file__).resolve().parent
POC = HERE.parent
DEVELOPMENT = POC / 'planner_cases/development.json'
DEVELOPMENT_SHA = 'f086b5b41a663a14d056499ed16f4026e8ad166afa7af6edafb0d07e2ad3d3e1'


def load_development(path=DEVELOPMENT):
    if Path(path).resolve() != DEVELOPMENT.resolve():
        raise ValueError('Only the original development fixture is permitted')
    content = DEVELOPMENT.read_bytes()
    if hashlib.sha256(content).hexdigest() != DEVELOPMENT_SHA:
        raise ValueError('Development fixture changed')
    return json.loads(content)['cases']


def validate_spans(question, result):
    """Validate native entity/relation spans without repairing or interpreting them."""
    def span(item):
        if not isinstance(item, dict):
            raise ValueError('Missing span object')
        start, end = item.get('start'), item.get('end')
        if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(question):
            raise ValueError('Invalid source offsets')
        if question[start:end] != item.get('text'):
            raise ValueError('Source text differs')
        return 1
    count = 0
    for items in result.get('entities', {}).values():
        for item in items:
            count += span(item)
    for items in result.get('relation_extraction', {}).values():
        for relation in items:
            count += span(relation['head']) + span(relation['tail'])
    return count


def check_access(event, args):
    """Defense in depth during inference, not an OS sandbox."""
    if event.startswith(('socket.connect', 'socket.getaddrinfo', 'sqlite3.connect', 'subprocess.Popen')):
        raise PermissionError('Probe forbids network, DB and subprocess access')
    if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
        path = Path(os.fsdecode(args[0])).resolve()
        if {'authored', 'corpus', 'kbcompiler', 'sealed'} & set(path.parts) or path.suffix in {'.db', '.sqlite', '.sqlite3'}:
            raise PermissionError('Probe cannot read locked knowledge or sealed cases')
        if 'planner_cases' in path.parts and path != DEVELOPMENT.resolve():
            raise PermissionError('Only development cases are available to this probe')


def build_schema(model):
    # Public API: https://github.com/fastino-ai/GLiNER2#readme
    specification = json.loads((HERE / 'schema.json').read_text())
    return (model.create_schema().entities(specification['entities'])
            .relations(specification['relations'])
            .classification('interpretation', specification['interpretation']))


def observe(question, extract):
    row = {}
    started = perf_counter()
    try:
        row['native'] = extract()
        row['validated_span_occurrences'] = validate_spans(question, row['native'])
    except Exception as exc:
        row['error'] = {'type': type(exc).__name__, 'message': str(exc)}
    row['seconds'] = perf_counter() - started
    return row

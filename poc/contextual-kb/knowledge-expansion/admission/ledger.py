"""Read-only source admission ledger: mechanical coverage, not semantic proof."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import sqlite3

REPO = Path(__file__).resolve().parents[4]
STATUSES = {'admitted', 'existing_support', 'excluded', 'pending'}
SUPPORTED = {'admitted', 'existing_support'}
SECTION_FIELDS = ('id','heading','start_line','end_line','start_offset','end_offset','sha256')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def strict_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f'Duplicate JSON key {key} in {path}')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), object_pairs_hook=pairs)


def source_path(root, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError('Source path must be repository-relative')
    path = root / value
    if path.resolve() != path.absolute() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Source path escapes root or is aliased: {value}')
    return path


def sections(text, doc_id):
    """All ATX headings outside fenced code, including a nonempty preamble.

    These pinned guides use ATX headings. Offsets count decoded characters,
    not UTF-8 bytes, consistently with authored-source quote offsets.
    """
    lines = text.splitlines(keepends=True)
    boundaries = []
    offset = 0
    fence = None
    for line_no, line in enumerate(lines, 1):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line.rstrip('\r\n'))
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
        elif marker:
            fence = marker[1]
        else:
            heading = re.match(r'^ {0,3}#{1,6}[ \t]+(.+?)\s*#*\s*$', line.rstrip('\r\n'))
            if heading:
                boundaries.append((line_no, offset, heading[1]))
        offset += len(line)
    if not boundaries or text[:boundaries[0][1]].strip():
        boundaries.insert(0, (1, 0, '(preamble)'))
    result = []
    for index, (line_no, start, heading) in enumerate(boundaries):
        end = boundaries[index+1][1] if index+1 < len(boundaries) else len(text)
        end_line = boundaries[index+1][0]-1 if index+1 < len(boundaries) else len(lines)
        result.append(dict(id=f'{doc_id}:L{line_no}', heading=heading,
                           start_line=line_no, end_line=end_line,
                           start_offset=start, end_offset=end,
                           sha256=digest(text[start:end].encode())))
    return result


def inventory(root, manifest_path):
    root = Path(root).resolve()
    manifest_path = Path(manifest_path)
    manifest = strict_json(manifest_path)
    documents = []
    ids = set()
    paths = set()
    for item in manifest['documents']:
        if item['id'] in ids or item['source'] in paths:
            raise ValueError('Duplicate manifest document or source')
        ids.add(item['id']); paths.add(item['source'])
        data = source_path(root,item['source']).read_bytes()
        units = sections(data.decode('utf-8'), item['id'])
        for unit in units:
            unit.update(status='pending', rationale='Awaiting whole-section source review.',
                        fact_ids=[], review='', decisions=[])
        documents.append(dict(id=item['id'],source=item['source'],sha256=digest(data),sections=units))
    return dict(schema_version=1,manifest_sha256=digest(manifest_path.read_bytes()),documents=documents)


def aggregate(decisions):
    values = {d['status'] for d in decisions}
    return next((s for s in ('pending','existing_support','admitted','excluded') if s in values),'pending')


def validate(ledger, root, manifest_path, authored_dirs, require_complete=False, database=None):
    """Validate source identity and declared dispositions; no semantic inference."""
    errors = []
    def need(condition, message):
        if not condition: errors.append(message)
    try:
        expected = inventory(root,manifest_path)
        need(ledger['schema_version'] == 1, 'Unsupported ledger schema')
        need(ledger['manifest_sha256'] == expected['manifest_sha256'], 'Import manifest hash mismatch')
        facts = set()
        for folder in authored_dirs:
            folder = Path(folder)
            if not folder.is_dir():
                raise ValueError(f'Authored directory missing: {folder}')
            for path in sorted(folder.glob('*.json')):
                doc = strict_json(path)
                for fact in doc['facts']:
                    fact_id = f"{doc['id']}/{fact['id']}"
                    need(fact_id not in facts, f'duplicate fact ID: {fact_id}')
                    facts.add(fact_id)
        seeded = None
        if database is not None:
            database = Path(database).resolve()
            before = digest(database.read_bytes())
            connection = sqlite3.connect(database.as_uri()+'?mode=ro',uri=True)
            try:
                connection.execute('PRAGMA query_only=ON')
                seeded = {row[0] for row in connection.execute('SELECT id FROM facts')}
            finally:
                connection.close()
            need(before == digest(database.read_bytes()), 'Database changed during read-only check')
        actual_docs = ledger['documents']
        need([d['id'] for d in actual_docs] == [d['id'] for d in expected['documents']], 'Document inventory mismatch (missing, extra, duplicate or reordered)')
        by_id = {d['id']:d for d in actual_docs}
        for document in expected['documents']:
            actual = by_id.get(document['id'])
            if actual is None: continue
            prefix = document['id']
            for key in ('source','sha256'):
                need(actual[key] == document[key], f'{prefix}: source {key} mismatch')
            source = source_path(Path(root).resolve(),document['source']).read_bytes().decode('utf-8')
            units = actual['sections']
            need([s['id'] for s in units] == [s['id'] for s in document['sections']], f'{prefix}: section inventory mismatch')
            unit_map = {s['id']:s for s in units}
            for reference in document['sections']:
                section = unit_map.get(reference['id'])
                if section is None: continue
                label = reference['id']
                for key in SECTION_FIELDS:
                    need(section[key] == reference[key], f'{label}: section {key} mismatch')
                need(section['status'] in STATUSES, f'{label}: invalid status')
                need(isinstance(section['rationale'],str) and bool(section['rationale'].strip()),f'{label}: rationale required')
                decisions = section['decisions']
                need(isinstance(decisions,list),f'{label}: decisions must be a list')
                if not isinstance(decisions,list): continue
                if section['status'] != 'pending':
                    need(bool(decisions),f'{label}: decided section requires claim decisions')
                    need(isinstance(section['review'],str) and bool(section['review'].strip()),f'{label}: whole-section review required')
                if require_complete:
                    need(section['status'] != 'pending',f'{label}: pending review')
                seen = set()
                mapped = set()
                for decision in decisions:
                    tag = f"{label}/{decision['id']}"
                    need(isinstance(decision['id'],str) and bool(decision['id']) and decision['id'] not in seen,f'{tag}: missing/duplicate decision ID')
                    seen.add(decision['id'])
                    for key in ('scope','rationale','quote'):
                        need(isinstance(decision[key],str) and bool(decision[key].strip()),f'{tag}: {key} required')
                    need(decision['quote'] in source[reference['start_offset']:reference['end_offset']],f'{tag}: quote not in this source section')
                    need(decision['status'] in STATUSES,f'{tag}: invalid status')
                    if decision['status'] != 'pending':
                        need(isinstance(decision['review'],str) and bool(decision['review'].strip()),f'{tag}: review required')
                    references = decision['fact_ids']
                    need(isinstance(references,list) and all(isinstance(x,str) for x in references),f'{tag}: fact_ids must be strings')
                    if not isinstance(references,list): continue
                    need(len(references) == len(set(references)),f'{tag}: duplicate fact_ids')
                    if decision['status'] in SUPPORTED:
                        need(bool(references),f'{tag}: supported decision requires fact_ids')
                    if decision['status'] == 'excluded':
                        need(not references,f'{tag}: excluded decision cannot claim fact_ids')
                    for fact_id in references:
                        need(fact_id in facts,f'{tag}: unknown fact {fact_id}')
                        if seeded is not None and decision['status'] in SUPPORTED:
                            need(fact_id in seeded,f'{tag}: fact not seeded in supplied database: {fact_id}')
                    mapped.update(references)
                need(section['status'] == aggregate(decisions),f'{label}: aggregate status disagrees with decisions')
                need(isinstance(section['fact_ids'],list) and len(section['fact_ids']) == len(set(section['fact_ids'])) and set(section['fact_ids']) == mapped,f'{label}: section fact_ids must equal decision union')
    except (KeyError, TypeError, ValueError, OSError, sqlite3.Error) as exc:
        errors.append(f'Malformed ledger or source inputs: {exc}')
    return errors


def render(ledger):
    counts = Counter(s['status'] for d in ledger['documents'] for s in d['sections'])
    lines = ['# Source admission checklist','',
             'Generated from the reviewed ledger. Mechanical completeness is not proof that every semantic claim was correctly interpreted.', '',
             'Section counts: '+', '.join(f'{key}={counts[key]}' for key in sorted(STATUSES))+'.','']
    for doc in ledger['documents']:
        lines += [f"## {doc['id']}", '', f"Source: `{doc['source']}`; SHA-256 `{doc['sha256']}`.",'']
        for section in doc['sections']:
            mark = ' ' if section['status']=='pending' else 'x'
            lines += [f"- [{mark}] **{section['heading']}** (lines {section['start_line']}–{section['end_line']}) — {section['status']}. {section['rationale']}"]
            for d in section['decisions']:
                links = ', '.join(f'`{x}`' for x in d['fact_ids']) or 'none'
                lines += [f"  - {d['scope']} — **{d['status']}**; facts: {links}. {d['rationale']}"]
        lines += ['']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['inventory','check','report'])
    parser.add_argument('--root',type=Path,default=REPO)
    parser.add_argument('--manifest',type=Path)
    parser.add_argument('--ledger',type=Path)
    parser.add_argument('--authored-dir',type=Path,action='append')
    parser.add_argument('--require-complete',action='store_true')
    parser.add_argument('--database',type=Path,help='Optional read-only seeded-ID coverage check; not record equality or promotion proof')
    args = parser.parse_args()
    manifest = args.manifest or args.root/'poc/contextual-kb/import-manifest.json'
    if args.command == 'inventory':
        print(json.dumps(inventory(args.root,manifest),indent=2)); return 0
    if args.ledger is None: parser.error('--ledger is required')
    ledger = strict_json(args.ledger)
    authored = args.authored_dir or [args.root/'poc/contextual-kb/authored']
    errors = validate(ledger,args.root,manifest,authored,args.require_complete,args.database)
    if errors:
        print(json.dumps({'ok':False,'errors':errors},indent=2)); return 1
    database_receipt = {'path':str(args.database.resolve()),'sha256':digest(args.database.read_bytes()),'scope':'seeded-ID coverage only; not record equality or promotion proof'} if args.database else None
    print(render(ledger) if args.command == 'report' else json.dumps({'ok':True,'database':database_receipt,'complete':not any(s['status']=='pending' for d in ledger['documents'] for s in d['sections']),'documents':len(ledger['documents']),'sections':sum(len(d['sections']) for d in ledger['documents'])},indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())

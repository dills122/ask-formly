"""Validated, read-only example sidecar. No authored facts or DB are rewritten."""
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

from pydantic import BaseModel, ConfigDict, Field, StrictInt
from typing import Annotated, Literal
from model_free_v1.response import fits_packet


class Record(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)


class Scope(Record):
    formly_version: Literal['6.3.12']
    ui_adapter: Literal['Material']


class Link(Record):
    fact_id: str = Field(min_length=1)
    support: str = Field(min_length=1)


class File(Record):
    path: str = Field(min_length=1)
    language: str = Field(min_length=1)


class Provenance(Record):
    kind: Literal['authored_fact', 'source', 'original']
    reference: str = Field(min_length=1)


Sha256 = Annotated[str, Field(pattern=r'^[0-9a-f]{64}$')]
Nonempty = Annotated[str, Field(min_length=1)]


class ExecutionEnvironment(Record):
    angular_core: Nonempty = Field(alias='@angular/core')
    angular_material: Nonempty = Field(alias='@angular/material')
    formly_core: Nonempty = Field(alias='@ngx-formly/core')
    formly_material: Nonempty = Field(alias='@ngx-formly/material')
    rxjs: Nonempty
    zone_js: Nonempty = Field(alias='zone.js')
    playwright: Nonempty
    esbuild: Nonempty
    node: Nonempty
    platform: Nonempty
    arch: Nonempty
    browser: Nonempty
    fixture_sha256: dict[Nonempty, Sha256] = Field(min_length=1)
    assertions_passed: list[Nonempty] = Field(min_length=1)


class Verification(Record):
    status: Literal['illustrative', 'source_reviewed', 'executed']
    details: str = Field(min_length=1)
    command: str | None = None
    environment: ExecutionEnvironment | None = None
    result_path: str | None = None
    result_sha256: str | None = Field(default=None, pattern=r'^[0-9a-f]{64}$')
    content_sha256: dict[Nonempty, Sha256] | None = None


class Example(Record):
    schema_version: Literal[1]
    id: str = Field(pattern=r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(min_length=1, max_length=1000)
    scope: Scope
    fact_links: list[Link] = Field(min_length=1, max_length=32)
    conditions: list[str]
    limits: list[str] = Field(min_length=1)
    prerequisites: list[str] = Field(min_length=1)
    files: list[File] = Field(min_length=1, max_length=16)
    assertions: list[str] = Field(min_length=1)
    provenance: list[Provenance] = Field(min_length=1)
    verification: Verification


def safe_file(root, name):
    path = PurePosixPath(name)
    if (path.is_absolute() or '\\' in name or ':' in name or
            any(part in ('', '.', '..') for part in name.split('/'))):
        raise ValueError('Example file must be a safe relative POSIX path')
    target = root.joinpath(*path.parts)
    within = [target]
    parent = target.parent
    while parent != root:
        within.append(parent)
        parent = parent.parent
    within.append(root)
    if any(p.is_symlink() for p in within):
        raise ValueError('Example files must not use symlinks')
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('Example file escaped its record directory')
    return target


def authored_fact_ids(authored):
    ids = set()
    for path in sorted(Path(authored).glob('*.json')):
        document = json.loads(path.read_text())
        ids.update(document['id'] + '/' + fact['id'] for fact in document['facts'])
    if not ids:
        raise ValueError('No authored fact inventory supplied')
    return ids


class Catalog:
    def __init__(self, root, fact_ids):
        self.root = Path(root)
        self.fact_ids = set(fact_ids)
        self.records = {}
        if self.root.is_symlink():
            raise ValueError('Example root must not be a symlink')
        for path in sorted(self.root.glob('*/manifest.json')):
            if path.is_symlink() or path.parent.is_symlink():
                raise ValueError('Example manifest must not be a symlink')
            record = Example.model_validate_json(path.read_text()).model_dump(exclude_none=True, by_alias=True)
            eid = record['id']
            if eid in self.records:
                raise ValueError('Duplicate example ID: ' + eid)
            links = [link['fact_id'] for link in record['fact_links']]
            if len(set(links)) != len(links) or not set(links) <= self.fact_ids:
                raise ValueError('Duplicate or unknown linked fact')
            for origin in record['provenance']:
                if origin['kind'] == 'authored_fact' and origin['reference'] not in self.fact_ids:
                    raise ValueError('Unknown provenance fact')
            verification = record['verification']
            if verification['status'] == 'executed' and not all(verification.get(k) for k in ('command', 'environment', 'result_path', 'result_sha256', 'content_sha256')):
                raise ValueError('Executed examples require command, environment, result and content hashes')
            names = [f['path'] for f in record['files']]
            if len(set(names)) != len(names):
                raise ValueError('Duplicate example file path')
            for item in record['files']:
                content = safe_file(path.parent, item['path']).read_text(encoding='utf-8')
                item.update(content=content, sha256=hashlib.sha256(content.encode()).hexdigest())
            if verification['status'] == 'executed' and verification['content_sha256'] != {f['path']: f['sha256'] for f in record['files']}:
                raise ValueError('Executed example content changed since verification')
            self.records[eid] = record
        if not self.records:
            raise ValueError('No linked examples found')

    def summary(self, record):
        result = {key: copy.deepcopy(record[key]) for key in
                  ('id', 'title', 'summary', 'scope', 'fact_links', 'verification')}
        result['available_files'] = [{key: value for key, value in item.items() if key != 'content'}
                                     for item in record['files']]
        return result

    def references(self, fact_ids):
        wanted = set(fact_ids)
        return [self.summary(record) for record in self.records.values()
                if wanted.intersection(link['fact_id'] for link in record['fact_links'])]

    def retrieve(self, *, fact_ids=None, example_ids=None, formly_version='6.3.12',
                 ui_adapter='Material', offset=0, limit=8, file_paths=None):
        if (fact_ids is None) == (example_ids is None):
            raise ValueError('Supply exactly one of fact_ids or example_ids')
        selected = fact_ids if fact_ids is not None else example_ids
        if (not isinstance(selected, list) or not 1 <= len(selected) <= 16 or
                any(not isinstance(item, str) or not item for item in selected)):
            raise ValueError('Supply 1..16 complete IDs')
        if type(offset) is not int or offset < 0 or type(limit) is not int or not 1 <= limit <= 16:
            raise ValueError('Invalid pagination')
        if file_paths is not None and (fact_ids is not None or not isinstance(file_paths, list) or
                not 1 <= len(file_paths) <= 16 or any(not isinstance(p, str) for p in file_paths)):
            raise ValueError('file_paths requires explicit example_ids and 1..16 paths')
        scope = dict(formly_version=formly_version, ui_adapter=ui_adapter)
        if formly_version != '6.3.12' or ui_adapter.lower() != 'material':
            return dict(status='unsupported_scope', candidate=True, examples=[], scope=scope)
        known = self.fact_ids if fact_ids is not None else self.records.keys()
        if not set(selected) <= set(known):
            raise ValueError('Unknown fact or example ID')
        records = (self.references(selected) if fact_ids is not None else
                   [copy.deepcopy(self.records[eid]) for eid in dict.fromkeys(selected)])
        if file_paths is not None:
            available = {f['path'] for record in records for f in record['files']}
            if not set(file_paths) <= available:
                raise ValueError('Unknown example file path')
            for record in records:
                record['available_files'] = [{k: v for k, v in f.items() if k != 'content'} for f in record['files']]
                record['files'] = [f for f in record['files'] if f['path'] in file_paths]
        packet = dict(status='ok', candidate=True, scope=scope, examples=[],
                      offset=offset, next_offset=None, total=len(records))
        for record in records[offset:offset + limit]:
            trial = copy.deepcopy(packet)
            trial['examples'].append(record)
            count = offset + len(trial['examples'])
            trial['next_offset'] = count if count < len(records) else None
            if not fits_packet(trial):
                if not packet['examples']:
                    raise ValueError('One complete example exceeds budget; list by fact_ids, then request individual file_paths. Code is never truncated.')
                break
            packet = trial
        if not packet['examples']:
            packet['status'] = 'exhausted'
        fits_packet(packet)
        return packet

    def enrich(self, packet):
        if packet.get('status') not in ('ok', 'caller_plan', 'not_decomposed', None) or not packet.get('facts'):
            return packet
        if packet.get('ui_adapter', '').lower() != 'material':
            return packet
        ids = [fact['id'] for fact in packet['facts']]
        references = [dict(id=r['id'], title=r['title'],
                           verification_status=r['verification']['status'],
                           matched_fact_ids=[l['fact_id'] for l in r['fact_links'] if l['fact_id'] in ids])
                      for r in self.references(ids)]
        if not references:
            return packet
        trial = copy.deepcopy(packet)
        trial['example_references'] = references
        trial['examples_status'] = 'isolated_candidate'
        if fits_packet(trial):
            return trial
        # Preserve all fact evidence when the reference list will not fit.
        trial = copy.deepcopy(packet)
        trial['example_discovery'] = 'Call get_formly_examples with returned fact_ids for candidate examples.'
        return trial if fits_packet(trial) else packet

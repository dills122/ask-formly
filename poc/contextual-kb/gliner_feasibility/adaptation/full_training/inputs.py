"""Exact train/dev input allowlists; evaluation is not a supported split."""
import hashlib
import json
import os
from pathlib import Path


def load_split(root, spec, role, expected_count):
    if role not in ('train','dev') or spec['path']!=f'data/{role}.json':
        raise ValueError('Only fixed train/dev paths supported')
    root=root.resolve();path=(root/spec['path']).resolve()
    if not path.is_relative_to(root/'data'):raise ValueError('Split escapes data directory')
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=spec['sha256']:raise ValueError('Split hash mismatch')
    rows=json.loads(raw)
    if spec['count']!=expected_count or len(rows)!=expected_count:raise ValueError('Split count mismatch')
    if len({r['id'] for r in rows})!=len(rows):raise ValueError('Duplicate IDs')
    return rows


def load_manifest(path):
    manifest=json.loads(path.read_text())
    required={'version','train','dev','families','annotation_receipt','custody_receipt'}
    if set(manifest)!=required or manifest['version']!=1:raise ValueError('Invalid training-only manifest')
    if any(not isinstance(manifest[k],str) or not manifest[k] for k in ('annotation_receipt','custody_receipt')):
        raise ValueError('Missing readiness receipts')
    train=load_split(path.parent,manifest['train'],'train',120)
    dev=load_split(path.parent,manifest['dev'],'dev',30)
    train_ids={r['id'] for r in train};dev_ids={r['id'] for r in dev}
    if train_ids & dev_ids:raise ValueError('Cross-split IDs')
    families=manifest['families']
    if set(families)!=(train_ids|dev_ids) or any(not isinstance(v,str) or not v for v in families.values()):
        raise ValueError('Missing family assignments')
    if {families[i] for i in train_ids} & {families[i] for i in dev_ids}:raise ValueError('Family leakage')
    if {r['question'] for r in train} & {r['question'] for r in dev}:raise ValueError('Repeated question leakage')
    return manifest,train,dev


def access_policy(repo, allowed_files, output, library_roots):
    repo=repo.resolve();output=output.resolve()
    allowed={p.resolve() for p in allowed_files};roots=[p.resolve() for p in library_roots]
    def check(event,args):
        if event.startswith(('socket.connect','socket.getaddrinfo','sqlite3.connect','subprocess.Popen')):
            raise PermissionError('No network, DB or subprocess in training worker')
        if event!='open' or not isinstance(args[0],(str,bytes,os.PathLike)):return
        path=Path(os.fsdecode(args[0])).resolve()
        mode=args[1] if len(args)>1 else ''
        flags=args[2] if len(args)>2 and isinstance(args[2],int) else 0
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
        if path.suffix in ('.db','.sqlite','.sqlite3'):raise PermissionError('Database access forbidden')
        if writing and not path.is_relative_to(output):raise PermissionError('Writes only to this run')
        if path.is_relative_to(repo) and not (path in allowed or path.is_relative_to(output) or
                                             any(path.is_relative_to(r) for r in roots)):
            raise PermissionError('Input outside training allowlist')
    return check

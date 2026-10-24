"""Anchorless pilot transport. No heuristic decomposition or semantic repairs."""
import hashlib
import json
import os
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
PILOT=HERE.parent/'pilot'
BASE=HERE.parents[1]
REPO=BASE.parents[2]
sys.path.insert(0,str(HERE.parent))
from pilot.contract import export_example as original_export, FIELDS

PILOT_SHA='bea23e707cc9bb1d7df10467eec65f33addbbce832b7c641eb9962ec21f4e67b'


def load_pilot(path=PILOT/'adjudicated-v2.json'):
    if Path(path).resolve()!=(PILOT/'adjudicated-v2.json').resolve():
        raise ValueError('Only frozen training pilot allowed')
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PILOT_SHA:raise ValueError('Pilot hash mismatch')
    rows=json.loads(raw)
    if len(rows)!=24:raise ValueError('Expected 24 pilot cases')
    return rows


def export_example(row):
    out=original_export(row)
    out['output']['record_metadata']={'request':{'mode':'anchorless'}}
    present={r['kind'] for r in row['relations']}
    for name in ('has_value','refers_to'):
        if name not in present:
            out['output']['relations'].append({name:{'head':[],'tail':[]}})
    return out


def check_access(event,args):
    """Defense in depth; parent timeout and filesystem sandbox remain necessary."""
    if event.startswith(('socket.connect','socket.getaddrinfo','sqlite3.connect','subprocess.Popen')):
        raise PermissionError('No network, DB or subprocess inside compatibility worker')
    if event!='open' or not isinstance(args[0],(str,bytes,os.PathLike)):return
    path=Path(os.fsdecode(args[0])).resolve()
    mode=args[1] if len(args)>1 else ''
    flags=args[2] if len(args)>2 and isinstance(args[2],int) else 0
    writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
    if path.suffix in {'.db','.sqlite','.sqlite3'}:raise PermissionError('No database access')
    if writing and not path.is_relative_to(HERE):raise PermissionError('Writes only inside revision')
    if path.is_relative_to(REPO) and not any(path.is_relative_to(p) for p in (HERE,PILOT,BASE/'models',BASE/'env')):
        raise PermissionError('No other project inputs or sealed cases')

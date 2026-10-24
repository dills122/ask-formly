"""Pilot agreement and process access checks; no retrieval or planning behavior."""
from collections import Counter
import os
from pathlib import Path
from contract import FIELDS

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
POC=BASE.parent
REPO=POC.parents[1]


def agreement(left,right):
    if not left or len(left)!=len(right): raise ValueError('unaligned cases')
    def features(row):
        items=[]
        for i,a in enumerate(row['aspects']):
            for role in FIELDS:
                items.extend(('aspect',i,role,s['start'],s['end']) for s in a[role])
        for role,spans in row['entities'].items():
            items.extend(('entity',role,s['start'],s['end']) for s in spans)
        items.extend(('relation',r['kind'],r['head']['start'],r['head']['end'],
                      r['tail']['start'],r['tail']['end']) for r in row['relations'])
        return Counter(items)
    overlap=nleft=nright=counts=statuses=0
    cases=[]
    for a,b in zip(left,right):
        if (a['id'],a['question'])!=(b['id'],b['question']): raise ValueError('unaligned cases')
        x,y=features(a),features(b)
        hit=sum((x&y).values());nx=sum(x.values());ny=sum(y.values())
        overlap+=hit;nleft+=nx;nright+=ny
        counts+=len(a['aspects'])==len(b['aspects']);statuses+=a['status']==b['status']
        cases.append({'id':a['id'],'left':nx,'right':ny,'intersection':hit,
                      'f1':2*hit/(nx+ny) if nx+ny else None})
    return {'cases':cases,'aspect_count_agreement':counts/len(left),
            'ambiguity_agreement':statuses/len(left),
            'span_attachment_f1':2*overlap/(nleft+nright) if nleft+nright else None,
            'left_features':nleft,'right_features':nright,'intersection':overlap,
            'definition':'micro exact role+occurrence spans, aspect index attachment and relation pairs; aspects in source order'}


def check_access(event,args):
    """Defense in depth, not an OS sandbox. Only pilot/model/env project reads."""
    if event.startswith(('socket.connect','socket.getaddrinfo','sqlite3.connect','subprocess.Popen')):
        raise PermissionError('Pilot forbids network, DB and subprocess access')
    if event!='open' or not isinstance(args[0],(str,bytes,os.PathLike)): return
    path=Path(os.fsdecode(args[0])).resolve()
    mode=args[1] if len(args)>1 else ''
    flags=args[2] if len(args)>2 and isinstance(args[2],int) else 0
    writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
    if path.suffix in {'.db','.sqlite','.sqlite3'}: raise PermissionError('No database access')
    if writing and not path.is_relative_to(HERE): raise PermissionError('Writes only inside pilot')
    allowed=(HERE,BASE/'models',BASE/'env')
    if path.is_relative_to(REPO) and not any(path.is_relative_to(p) for p in allowed):
        raise PermissionError('No other project inputs, knowledge or sealed cases')

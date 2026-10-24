"""Bounded repair of original slots; pure question-aware decisions, no gold/hints."""
import hashlib
import sys
import time
from pathlib import Path
POC=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(POC))
from agent_contract.advisory_lookup_v1.runtime import IntegrityError
DEPTH=20
LIMIT=8
MAX_REPLACEMENTS=2

def acquire(index,core,baseline):
    pool=list(baseline);queries=[]
    for qi,q in enumerate(core['formly_questions']):
        for channel in ('lexical','dense'):
            start=time.perf_counter();ids=getattr(index,channel)(q['question'],DEPTH)
            queries.append(dict(question_index=qi,text=q['question'],channel=channel,depth=DEPTH,ids=ids,seconds=time.perf_counter()-start))
            pool.extend(ids)
    return {'pool':list(dict.fromkeys(pool)),'queries':queries}

def present(core,baseline,pool,facts,source_quote):
    ordered=sorted(set(pool),key=lambda f:(hashlib.sha256(f.encode()).hexdigest(),f))
    mapping={f'c{i:03}':f for i,f in enumerate(ordered,1)}
    reverse={f:h for h,f in mapping.items()}
    rows=[dict(handle=h,**{k:facts[f][k] for k in ('claim','conditions','limits','version','adapter')},source_quote=source_quote(f)) for h,f in mapping.items()]
    return dict(questions=core['formly_questions'],condition_bindings=core['condition_bindings'],library_constraints=core['library_constraints'],baseline=[reverse[f] for f in baseline],candidates=rows),mapping

def apply_repair(decision,payload,mapping):
    if not isinstance(decision,dict) or set(decision)!={'replacements'}:raise ValueError('Expected replacements only')
    rows=decision['replacements'];baseline=payload['baseline']
    if not isinstance(rows,list) or len(rows)>MAX_REPLACEMENTS:raise ValueError('At most two replacements')
    if len(baseline)>LIMIT or len(set(baseline))!=len(baseline):raise ValueError('Invalid original packet')
    candidates={r['handle']:r for r in payload['candidates']};removals=set();additions=set();pairs=[]
    for row in rows:
        if not isinstance(row,dict) or set(row)!={'remove','add','question_indexes','support_quote','reason'}:raise ValueError('Invalid replacement schema')
        old,new=row['remove'],row['add']
        if not isinstance(old,str) or old not in baseline or old in removals:raise ValueError('Unknown or duplicate removal')
        if not isinstance(new,str) or new not in mapping or new in baseline or new in additions:raise ValueError('Unknown or duplicate addition')
        indexes=row['question_indexes']
        if not isinstance(indexes,list) or not indexes or any(type(i)is not int or not 0<=i<len(payload['questions']) for i in indexes) or len(set(indexes))!=len(indexes):raise ValueError('Invalid question binding')
        quote=row['support_quote'];record=candidates[new]
        if not isinstance(quote,str) or len(quote.strip())<8 or not any(quote in record[k] for k in ('claim','source_quote')):raise ValueError('Ungrounded support quote')
        if not isinstance(row['reason'],str) or not row['reason'].strip():raise ValueError('Missing reason')
        removals.add(old);additions.add(new);pairs.append((old,new))
    changed=dict(pairs)
    return [mapping[changed.get(h,h)] for h in baseline]

def repair(index,core,baseline,source_quote,selector):
    if not core['formly_questions']:
        return dict(ids=list(baseline),status='not_needed',replacements=[],queries=[])
    acquired={'queries':[]};start=time.perf_counter()
    try:
        acquired=acquire(index,core,baseline)
        payload,mapping=present(core,baseline,acquired['pool'],index.facts,source_quote)
        decision=selector(payload)
        ids=apply_repair(decision,payload,mapping)
        return dict(ids=ids,status='repaired' if decision['replacements'] else 'unchanged',
                    replacements=decision['replacements'],queries=acquired['queries'],mapping=mapping,
                    seconds=time.perf_counter()-start)
    except IntegrityError:raise
    except Exception as exc:
        return dict(ids=list(baseline),status='fallback',replacements=[],queries=acquired['queries'],
                    error=type(exc).__name__+': '+str(exc),seconds=time.perf_counter()-start)

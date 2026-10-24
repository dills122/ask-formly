"""Gold-blind acquisition and opaque semantic-selector boundary."""
import hashlib,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kbcompiler.question_pilot import merge_obligations

DEPTH=20
LIMIT=8

def unique(values):return list(dict.fromkeys(values))

def acquire(index,core):
    queries=[];narrow=[];wide=[]
    for qi,q in enumerate(core['formly_questions']):
        lists=[]
        for depth in (8,DEPTH):
            started=time.perf_counter();ids=index.hybrid(q['question'],depth);seconds=time.perf_counter()-started
            queries.append(dict(question_index=qi,text=q['question'],depth=depth,ids=ids,seconds=seconds))
            lists.append(ids)
        narrow.append(lists[0]);wide.append(unique(lists[1]+lists[0]))
    return dict(queries=queries,foundation=merge_obligations(narrow,LIMIT),wide_rank=merge_obligations(wide,LIMIT),
                narrow_pool=unique([f for row in narrow for f in row]),wide_pool=unique([f for row in wide for f in row]))

def present(identity,core,pool,facts):
    ordered=sorted(set(pool),key=lambda f:(hashlib.sha256(f.encode()).hexdigest(),f))
    mapping={f'c{i:03}':f for i,f in enumerate(ordered,1)}
    candidates=[dict(handle=h,**{k:facts[f][k] for k in ('claim','conditions','limits','version','adapter')}) for h,f in mapping.items()]
    return dict(id=identity,questions=core['formly_questions'],condition_bindings=core['condition_bindings'],library_constraints=core['library_constraints'],candidates=candidates),mapping

def validate_selection(rows,mapping,nquestions):
    if not isinstance(rows,list) or len(rows)>LIMIT:raise ValueError('selection must be list with at most eight')
    chosen=[]
    for row in rows:
        if not isinstance(row,dict) or set(row)!={'handle','question_indexes','reason'}:raise ValueError('selection schema')
        h=row['handle'];indexes=row['question_indexes'];reason=row['reason']
        if not isinstance(h,str) or h not in mapping or h in chosen:raise ValueError('unknown or duplicate handle')
        if not isinstance(indexes,list) or not indexes or any(type(i)is not int or not 0<=i<nquestions for i in indexes) or len(set(indexes))!=len(indexes):raise ValueError('invalid question indexes')
        if not isinstance(reason,str) or not reason.strip():raise ValueError('empty rationale')
        chosen.append(h)
    return [mapping[h] for h in chosen]

def account(raw,payload,mappings):
    def pairs(items):
        result={}
        for k,v in items:
            if k in result:raise ValueError('duplicate JSON key')
            result[k]=v
        return result
    def constant(s):raise ValueError('invalid JSON constant')
    try:
        rows=json.loads(raw,object_pairs_hook=pairs,parse_constant=constant)
        if not isinstance(rows,list) or any(not isinstance(r,dict) or set(r)!={'id','selected'} for r in rows):raise ValueError('batch schema')
        if [r['id'] for r in rows]!=[r['id'] for r in payload]:raise ValueError('batch identity/order/coverage')
    except (ValueError,TypeError) as exc:return [dict(id=p['id'],ids=[],error=str(exc)) for p in payload]
    result=[]
    for row,p in zip(rows,payload):
        try:ids=validate_selection(row['selected'],mappings[row['id']],len(p['questions']));error=None
        except (ValueError,TypeError) as exc:ids=[];error=str(exc)
        result.append(dict(id=row['id'],ids=ids,error=error))
    return result

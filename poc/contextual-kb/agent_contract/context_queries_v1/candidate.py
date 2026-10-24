"""Contextual text-query comparison; no knowledge or retrieval policy edits."""
import sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kbcompiler.question_pilot import reciprocal_rank_fusion,merge_obligations

def supplemental_queries(core,rows):
    questions=core['formly_questions']
    if not isinstance(rows,list) or len(rows)!=len(questions):raise ValueError('supplement coverage')
    queries=[]
    for i,row in enumerate(rows):
        if not isinstance(row,dict) or set(row)!={'question_index','query'} or type(row['question_index']) is not int or row['question_index']!=i:raise ValueError('supplement schema/order')
        query=row['query']
        if not isinstance(query,str) or not query.strip():raise ValueError('empty/nonstring supplemental query')
        for binding in core['condition_bindings']:
            if i in binding['question_indexes'] and binding['condition'] not in query:raise ValueError(f'missing bound condition in question {i}')
        queries.append(query)
    return queries

def retrieve(index,core,supplements=None):
    started=time.perf_counter();error=None;extras=[];queries=[];lists=[]
    if supplements is not None:
        try:extras=supplemental_queries(core,supplements)
        except ValueError as exc:error=str(exc)
    for i,q in enumerate(core['formly_questions']):
        original=index.hybrid(q['question'],8)
        queries.append(dict(question_index=i,kind='full',text=q['question'],ids=original))
        if extras and extras[i]!=q['question']:
            additional=index.hybrid(extras[i],8)
            queries.append(dict(question_index=i,kind='context',text=extras[i],ids=additional))
            ranked=reciprocal_rank_fusion([original,additional])[:8]
        else:ranked=original
        lists.append(ranked)
    return dict(ids=merge_obligations(lists,8),questions=lists,queries=queries,query_count=len(queries),query_characters=sum(len(q['text']) for q in queries),seconds=time.perf_counter()-started,supplement_error=error)

def utility_pass(base,candidate,paired_losses,batch_deltas,failures):
    return (not failures and paired_losses==0 and bool(batch_deltas) and all(d is not None and d>=0 for d in batch_deltas)
            and base['recall'] is not None and candidate['recall'] is not None and candidate['recall']-base['recall']>=.02
            and candidate['precision']>=base['precision'] and candidate['unsupported_candidates']<=base['unsupported_candidates'])

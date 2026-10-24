"""Optional text-query expansion over the unchanged POC retrieval engine."""
from contextlib import contextmanager
import math
from pathlib import Path
import sqlite3
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kbcompiler.question_pilot import reciprocal_rank_fusion, merge_obligations

@contextmanager
def readonly(path):
    # SQLite URI mode=ro: https://www.sqlite.org/uri.html
    db=sqlite3.connect(Path(path).resolve().as_uri()+'?mode=ro',uri=True)
    try:
        db.execute('PRAGMA query_only=ON')
        yield db
    finally:db.close()

def api_probe(hints,index):
    ordered=sorted((h for h in hints if h['question_index']==index and h['role']=='api_reference' and h['usable_as_filter'] is False),key=lambda h:h['start'])
    terms=list(dict.fromkeys(h['text'] for h in ordered))
    return 'Formly '+' '.join(terms) if terms else None

def retrieve(index,plan,enhanced):
    started=time.perf_counter();lists=[];queries=[]
    for i,request in enumerate(plan['search_requests']):
        text=request['query'];original=index.hybrid(text,8)
        queries.append(dict(question_index=i,kind='full',text=text,ids=original))
        probe=api_probe(plan['role_hints'],i) if enhanced else None
        if probe:
            supplemental=index.hybrid(probe,8)
            queries.append(dict(question_index=i,kind='api_probe',text=probe,ids=supplemental))
            ranked=reciprocal_rank_fusion([original,supplemental])[:8]
        else:ranked=original
        lists.append(ranked)
    return dict(ids=merge_obligations(lists,8),questions=lists,queries=queries,query_count=len(queries),seconds=time.perf_counter()-started)

def relevance(ids,case,k):
    selected=ids[:k];gold=set(case['relevant_fact_ids']);hits=[i for i,f in enumerate(selected) if f in gold]
    if not gold:return dict(precision=0.0,recall=None,ndcg=None,mrr=None,complete_groups=None,group_recall=None,unsupported_candidates=len(selected),hits=[],missing=[])
    groups=case['required_groups'];found=sum(bool(set(group)&set(selected)) for group in groups)
    dcg=sum(1/math.log2(i+2) for i in hits);ideal=sum(1/math.log2(i+2) for i in range(min(k,len(gold))))
    return dict(precision=len(hits)/k,recall=len(set(selected)&gold)/len(gold),ndcg=dcg/ideal,
                mrr=1/(hits[0]+1) if hits else 0.0,complete_groups=found==len(groups),group_recall=found/len(groups) if groups else None,
                unsupported_candidates=0,hits=[selected[i] for i in hits],missing=sorted(gold-set(selected)))

def consistency(tp,fp,fn):
    n=tp+fp;precision=tp/n if n else None;recall=tp/(tp+fn) if tp+fn else None
    interval=None
    if n:
        z=1.959963984540054;center=(precision+z*z/(2*n))/(1+z*z/n)
        radius=z*math.sqrt(precision*(1-precision)/n+z*z/(4*n*n))/(1+z*z/n)
        interval=[center-radius,center+radius]
    return dict(precision=precision,recall=recall,within_tolerance=precision is not None and precision>=.8925 and recall is not None and recall>=.8,
                target90=precision is not None and precision>=.9,wilson95=interval,
                caveat='Descriptive binomial interval; mentions within synthetic questions are correlated.')

"""Post-freeze gold accounting, never imported by selector/acquisition policy."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent_contract.retrieval_integration_v1.bridge import relevance
ARMS=('foundation','wide_rank','narrow_select','wide_select')

def mean(values):return sum(values)/len(values) if values else None

def summary(rows,cases,k):
    values=[(r,relevance(r['ids'],cases[r['id']],k)) for r in rows]
    supported=[(r,m) for r,m in values if m['recall'] is not None]
    out={key:mean([m[key] for _,m in supported]) for key in ('precision','recall','ndcg','mrr','group_recall')}
    selected=sum(len(r['ids'][:k]) for r,m in values)
    out.update(n=len(supported),complete_groups=sum(m['complete_groups'] for _,m in supported),any_hit=sum(bool(m['hits']) for _,m in supported),
               unsupported_candidates=sum(m['unsupported_candidates'] for _,m in values),selected_count=selected,
               selected_precision=sum(len(m['hits']) for _,m in values)/selected if selected else None,failures=sum(bool(r['error']) for r,_ in values))
    return out

def assess(rows,cases,traces,semantic):
    ids=[c['id'] for c in cases];case_map={c['id']:c for c in cases};expected={(i,a) for i in ids for a in ARMS}
    if len(set(ids))!=len(ids) or len(rows)!=len(expected) or {(r['id'],r['arm']) for r in rows}!=expected:raise ValueError('row coverage/identity')
    if len(traces)!=len(ids) or {r['id'] for r in traces}!=set(ids) or len(semantic)!=len(ids) or {r['id'] for r in semantic}!=set(ids):raise ValueError('trace/semantic coverage')
    if any(type(s['foundation_pass'])is not bool for s in semantic):raise ValueError('semantic boolean')
    for r in rows:
        if r['batch']!=case_map[r['id']]['batch'] or len(r['ids'])>8 or len(set(r['ids']))!=len(r['ids']):raise ValueError('batch/packet invariant')
    by={(r['id'],r['arm']):r for r in rows};batches=sorted({c['batch'] for c in cases})
    summaries={a:{str(b):{str(k):summary([r for r in rows if r['arm']==a and (b=='all' or r['batch']==b)],case_map,k) for k in (4,8)} for b in ['all',*batches]} for a in ARMS}
    per_case=[]
    for r in rows:
        for k in (4,8):
            metric=relevance(r['ids'],case_map[r['id']],k)
            metric['missing_groups']=[g for g in case_map[r['id']]['required_groups'] if not set(g)&set(r['ids'][:k])]
            per_case.append(dict(id=r['id'],arm=r['arm'],k=k,**metric))
    paired={a:[] for a in ARMS[1:]}
    for c in cases:
        base=set(by[c['id'],'foundation']['ids']);gold=set(c['relevant_fact_ids'])
        for a in ARMS[1:]:
            selected=set(by[c['id'],a]['ids'])
            paired[a].append(dict(id=c['id'],lost=sorted((base-selected)&gold),gained=sorted((selected-base)&gold),lost_groups=[g for g in c['required_groups'] if set(g)&base and not set(g)&selected]))
    pools={}
    for label in ('narrow','wide'):
        poolrows=[dict(id=t['id'],batch=case_map[t['id']]['batch'],recall=len(set(t[label+'_pool'])&set(case_map[t['id']]['relevant_fact_ids']))/len(case_map[t['id']]['relevant_fact_ids']) if case_map[t['id']]['relevant_fact_ids'] else None,size=len(t[label+'_pool']),missing=sorted(set(case_map[t['id']]['relevant_fact_ids'])-set(t[label+'_pool']))) for t in traces]
        pools[label]=dict(cases=poolrows,**{str(b):mean([r['recall'] for r in poolrows if r['recall'] is not None and (b=='all' or r['batch']==b)]) for b in ['all',*batches]})
    base=summaries['foundation']['all']['8'];joint=summaries['wide_select']['all']['8']
    gates=dict(preservation=all(not r['lost'] and not r['lost_groups'] for r in paired['wide_select']),
               utility=joint['recall'] is not None and base['recall'] is not None and joint['recall']-base['recall']>=.005-1e-12 and joint['precision']>=base['precision'],
               unsupported=joint['unsupported_candidates']<=base['unsupported_candidates'],
               batch_nonregression=all(summaries['wide_select'][str(b)]['8']['recall'] is not None and summaries['foundation'][str(b)]['8']['recall'] is not None and summaries['wide_select'][str(b)]['8']['recall']>=summaries['foundation'][str(b)]['8']['recall'] for b in batches),
               consistent_floor=all(summaries['wide_select'][str(b)]['8']['recall'] is not None and summaries['wide_select'][str(b)]['8']['recall']>=.8925 for b in ['all',*batches]),
               delivery=not any(r['error'] for r in rows),semantics=all(s['foundation_pass'] for s in semantic))
    return dict(summaries=summaries,per_case=per_case,paired=paired,pools=pools,gates=gates,qualified=all(gates.values()),semantic_failures=[s for s in semantic if not s['foundation_pass']],target90=joint['recall'] is not None and joint['recall']>=.9,
                caveat='Fresh synthetic development batches over fixed small catalog; no final-answer accuracy or population tolerance guarantee.')

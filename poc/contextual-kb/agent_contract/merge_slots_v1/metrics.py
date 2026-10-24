"""Gold is used only here, after all query rankings and packets are frozen."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]));sys.path.insert(0,str(HERE.parent/'context_queries_v1'))
from agent_contract.context_queries_v1.assessment import summary
from agent_contract.retrieval_integration_v1.bridge import relevance
ARMS=('foundation','current','protected')

def aggregate(rows,k):
    # Reuse frozen descriptive metrics, but never invent per-arm query timings.
    adapted=[dict(r,query_count=r['logical_query_count'],query_characters=r['logical_query_characters'],seconds=0) for r in rows]
    result=summary(adapted,k)
    for key in ('seconds','request_p50_seconds','request_p95_seconds'):result.pop(key)
    result['logical_query_count']=result.pop('query_count');result['logical_query_characters']=result.pop('query_characters')
    return result

def assess(rows,records,cases,semantic):
    byid={r['id']:r for r in records};expected={(i,a) for i in byid for a in ARMS}
    if len(byid)!=len(records) or len(rows)!=len(expected) or {(r['id'],r['arm']) for r in rows}!=expected:raise ValueError('record/arm coverage')
    if any(r['batch']!=byid[r['id']]['batch'] for r in rows):raise ValueError('batch identity')
    for collection in (cases,semantic):
        if len(collection)!=len(records) or {r['id'] for r in collection}!=set(byid):raise ValueError('gold/semantic coverage')
    if any(type(s[key]) is not bool for s in semantic for key in ('foundation_pass','supplement_pass')):raise ValueError('semantic verdict type')
    gold={c['id']:c for c in cases};scored=[]
    for r in rows:
        if len(r['ids'])>8 or len(r['ids'])!=len(set(r['ids'])):raise ValueError('packet budget/duplicates')
        values={}
        for k in (4,8):
            values[str(k)]=relevance(r['ids'],gold[r['id']],k)
            values[str(k)]['missing_groups']=[group for group in gold[r['id']]['required_groups'] if not set(group)&set(r['ids'][:k])]
        scored.append(dict(r,metrics=values))
    batches=sorted({r['batch'] for r in records});keyed={(r['id'],r['arm']):r for r in scored}
    summaries={a:{str(b):{k:aggregate([r for r in scored if r['arm']==a and (b=='all' or r['batch']==b)],k) for k in ('4','8')} for b in ['all',*batches]} for a in ARMS}
    paired={};gates={}
    for arm in ('current','protected'):
        paired[arm]=[];group_losses=[];fact_losses=[];fact_gains=[]
        for r in records:
            base=keyed[(r['id'],'foundation')];candidate=keyed[(r['id'],arm)];relevant=set(gold[r['id']]['relevant_fact_ids']);change=dict(id=r['id'],batch=r['batch'])
            for k in (4,8):
                old=set(base['ids'][:k]);new=set(candidate['ids'][:k])
                change[str(k)]=dict(lost_relevant=sorted((old-new)&relevant),gained_relevant=sorted((new-old)&relevant),foundation=base['metrics'][str(k)],candidate=candidate['metrics'][str(k)])
            paired[arm].append(change)
            if base['metrics']['8']['complete_groups'] is True and candidate['metrics']['8']['complete_groups'] is False:group_losses.append(r['id'])
            fact_losses.extend(dict(id=r['id'],fact=f) for f in change['8']['lost_relevant']);fact_gains.extend(dict(id=r['id'],fact=f) for f in change['8']['gained_relevant'])
        base=summaries['foundation']['all']['8'];candidate=summaries[arm]['all']['8']
        deltas=[summaries[arm][str(b)]['8']['recall']-summaries['foundation'][str(b)]['8']['recall'] if summaries[arm][str(b)]['8']['recall'] is not None else None for b in batches]
        safety=not group_losses and not fact_losses and candidate['unsupported_candidates']<=base['unsupported_candidates']
        utility=bool(fact_gains) and base['recall'] is not None and candidate['recall'] is not None and candidate['recall']-base['recall']>=.005 and candidate['precision']>=base['precision'] and all(d is not None and d>=0 for d in deltas)
        gates[arm]=dict(safety=safety,utility=utility,paired_group_losses=group_losses,lost_relevant=fact_losses,gained_relevant=fact_gains,batch_recall_deltas=deltas)
    prefix=all(keyed[(r['id'],'protected')]['ids'][:min(6,len(keyed[(r['id'],'foundation')]['ids']))]==keyed[(r['id'],'foundation')]['ids'][:6] for r in records)
    runtime=[dict(id=r['id'],arm=r['arm'],foundation_error=r['foundation_error'],supplement_error=r['supplement_error']) for r in rows if r['foundation_error'] or r['supplement_error']]
    semantic_failures=[s for s in semantic if not s['foundation_pass'] or not s['supplement_pass']]
    consistent={a:all(panel['8']['recall'] is not None and panel['8']['recall']>=.8925 for panel in summaries[a].values()) for a in ARMS}
    rescue=[]
    for r in records:
        current=keyed[(r['id'],'current')];protected=keyed[(r['id'],'protected')];g=set(gold[r['id']]['relevant_fact_ids']);change=dict(id=r['id'])
        for k in (4,8):
            before=current['metrics'][str(k)]['complete_groups'];after=protected['metrics'][str(k)]['complete_groups']
            old=set(current['ids'][:k]);new=set(protected['ids'][:k])
            change[str(k)]=dict(rescued_relevant=sorted((new-old)&g),lost_relevant=sorted((old-new)&g),current_complete_groups=before,protected_complete_groups=after,current_missing_groups=current['metrics'][str(k)]['missing_groups'],protected_missing_groups=protected['metrics'][str(k)]['missing_groups'],group_gained=before is False and after is True,group_lost=before is True and after is False)
        rescue.append(change)
    return dict(summaries=summaries,scored_rows=scored,paired=paired,gates=gates,protected_prefix_preserved=prefix,semantic_failures=semantic_failures,runtime_failures=runtime,
                consistent_floor=consistent,target90={a:all(p['8']['recall'] is not None and p['8']['recall']>=.9 for p in summaries[a].values()) for a in ARMS},protected_vs_current=rescue,
                qualified=prefix and gates['protected']['safety'] and gates['protected']['utility'] and consistent['protected'] and not semantic_failures and not runtime)

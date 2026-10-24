"""Paired, fixed-budget retrieval accounting; no prediction repair."""
import random,statistics
from candidate import utility_pass

def summary(rows,k):
    scored=[r['metrics'][k] for r in rows if r['metrics'][k]['recall'] is not None]
    mean=lambda key:statistics.mean(m[key] for m in scored) if scored else None
    values=[m['recall'] for m in scored];interval=None
    if values:
        rng=random.Random(1701)
        means=sorted(statistics.mean(rng.choices(values,k=len(values))) for _ in range(2000))
        interval=[means[49],means[1949]]
    times=sorted(r['seconds'] for r in rows)
    return dict(cases=len(rows),supported=len(scored),recall=mean('recall'),precision=mean('precision'),ndcg=mean('ndcg'),mrr=mean('mrr'),group_recall=mean('group_recall'),
                any_hit=statistics.mean(m['mrr']>0 for m in scored) if scored else None,complete_groups=sum(m['complete_groups'] for m in scored),
                unsupported_candidates=sum(r['metrics'][k]['unsupported_candidates'] for r in rows),query_count=sum(r['query_count'] for r in rows),query_characters=sum(r['query_characters'] for r in rows),seconds=sum(times),
                request_p50_seconds=times[(len(times)-1)//2] if times else None,request_p95_seconds=times[max(0,(95*len(times)+99)//100-1)] if times else None,
                recall_bootstrap95=interval,one_request_max_swing_percentage_points=100/len(scored) if scored else None,
                uncertainty_note='Descriptive request bootstrap on small related synthetic cases, not a population guarantee or evidence of subpercentage precision.')

def validate_coverage(rows,records):
    expected={(r['id'],a) for r in records for a in ('foundation','context')}
    actual=[(r['id'],r['arm']) for r in rows]
    if len(actual)!=len(expected) or set(actual)!=expected:raise ValueError('retrieval coverage')
    byid={r['id']:r for r in records}
    if len(byid)!=len(records) or any(r['batch']!=byid[r['id']]['batch'] for r in rows):raise ValueError('record identity/batch')

def assess(rows,records,semantic):
    validate_coverage(rows,records)
    if len(semantic)!=len(records) or {s['id'] for s in semantic}!={r['id'] for r in records}:raise ValueError('semantic coverage')
    if any(type(s[k]) is not bool for s in semantic for k in ('foundation_pass','supplement_pass')):raise ValueError('semantic verdict type')
    failures=[s['id'] for s in semantic if not s['foundation_pass'] or not s['supplement_pass']]
    runtime=[dict(id=r['id'],arm=r['arm'],foundation_error=r['foundation_error'],supplement_error=r['supplement_error']) for r in rows if r['foundation_error'] or r['supplement_error']]
    batches=sorted({r['batch'] for r in records});summaries={}
    for arm in ('foundation','context'):
        summaries[arm]={str(b):{k:summary([r for r in rows if r['arm']==arm and (b=='all' or r['batch']==b)],k) for k in ('4','8')} for b in ['all',*batches]}
    bykey={(r['id'],r['arm']):r for r in rows};differences=[];losses={k:[] for k in ('4','8')}
    for record in records:
        a=bykey[(record['id'],'foundation')];b=bykey[(record['id'],'context')]
        for k in losses:
            if a['metrics'][k]['complete_groups'] is True and b['metrics'][k]['complete_groups'] is False:losses[k].append(record['id'])
        differences.append(dict(id=record['id'],batch=record['batch'],foundation=a['metrics'],context=b['metrics'],added=sorted(set(b['ids'])-set(a['ids'])),lost=sorted(set(a['ids'])-set(b['ids']))))
    deltas=[summaries['context'][str(b)]['8']['recall']-summaries['foundation'][str(b)]['8']['recall'] if summaries['context'][str(b)]['8']['recall'] is not None and summaries['foundation'][str(b)]['8']['recall'] is not None else None for b in batches]
    consistent={a:all(s['8']['recall'] is not None and s['8']['recall']>=.8925 for s in summaries[a].values()) and not any(r['arm']==a for r in runtime) and all(s['foundation_pass'] and (a=='foundation' or s['supplement_pass']) for s in semantic) for a in summaries}
    return dict(summaries=summaries,semantic_failures=failures,runtime_failures=runtime,differences=differences,paired_group_losses=losses,batch_recall_deltas=deltas,
                utility_pass=utility_pass(summaries['foundation']['all']['8'],summaries['context']['all']['8'],len(losses['8']),deltas,len(failures)+len(runtime)),consistent_floor=consistent,
                target90={a:all(s['8']['recall'] is not None and s['8']['recall']>=.9 for s in summaries[a].values()) for a in summaries})

"""Inference/assessment separation and timing; no optimizer imports."""
import math
import time
from collections import Counter
from decisions import ROLES, groups, resolve, probabilities


def collect(rows,extract,score):
    records=[];ids=set()
    for row in rows:
        if row['id'] in ids:raise ValueError('duplicate dataset identity')
        ids.add(row['id']);text=row['text']
        raw=extract(text)
        if 'expected_raw' in row and raw!=row['expected_raw']:raise ValueError('frozen baseline drift: '+row['id'])
        eligible,blocked,_=groups(text,raw)
        offsets=eligible if len(eligible)<=8 else []
        # Gold is deliberately not an argument to operational extraction or scoring.
        op=score(text,offsets) if offsets else {}
        records.append(dict(id=row['id'],text=text,raw=raw,
            operational_scores=[dict(start=a,end=b,probabilities=op.get((a,b))) for a,b in offsets]))
    # Separate second pass: supplied gold/malformed spans never populate operational cache.
    for row,record in zip(rows,records):
        spans=sorted({(p['start'],p['end']) for p in row['probes']})
        supplied=score(row['text'],spans) if spans else {}
        record.update(gold=row['gold'],prior_correct_repairs=row.get('prior_correct_repairs',[]),
            probes=[dict(**p,probabilities=supplied.get((p['start'],p['end']))) for p in row['probes']])
    return records


def statistics(values):
    if not values:return dict(p50=0.,p95=0.,maximum=0.,count=0)
    ordered=sorted(values)
    return dict(p50=ordered[math.ceil(.5*len(ordered))-1],p95=ordered[math.ceil(.95*len(ordered))-1],maximum=max(ordered),count=len(ordered))


def timing(rows,extractors,scorers,threshold):
    if set(extractors)!=set(scorers) or set(extractors)!={'1701','1702'}:raise ValueError('paired timing required')
    samples=[]
    for repeat in range(-1,5):
        seeds=['1701','1702'] if repeat%2==0 or repeat==-1 else ['1702','1701']
        for seed in seeds:
            for row in rows:
                t=time.perf_counter();raw=extractors[seed](row['text']);extraction=time.perf_counter()-t
                eligible,_,_=groups(row['text'],raw)
                t=time.perf_counter();_,log=resolve(row['text'],raw,lambda offsets:scorers[seed](row['text'],offsets),threshold);added=time.perf_counter()-t
                if any(x['decision'] in ('scorer_error','invalid_raw') or x.get('reason')=='invalid_scores' for x in log):
                    raise ValueError('timing inference failure: '+seed+':'+row['id'])
                if repeat>=0:samples.append(dict(seed=seed,repeat=repeat,id=row['id'],eligible=len(eligible),extraction=extraction,verifier=added,combined=extraction+added))
    report={}
    for seed in ('1701','1702'):
        selected=[r for r in samples if r['seed']==seed]
        report[seed]={k:statistics([r[k] for r in selected]) for k in ('extraction','verifier','combined')}
        report[seed]['eligible_verifier']=statistics([r['verifier'] for r in selected if 0<r['eligible']<=8])
        report[seed]['passthrough_verifier']=statistics([r['verifier'] for r in selected if r['eligible']==0])
        report[seed]['overflow']=sum(r['eligible']>8 for r in selected)
    return dict(samples=samples,by_seed=report,budget_p95={s:max(report[s]['verifier']['p95'],report[s]['eligible_verifier']['p95']) for s in report})


def validate_fresh(rows):
    if len(rows)!=40 or len({r['id'] for r in rows})!=40:raise ValueError('fresh requires 40 unique questions')
    if any(not isinstance(r['text'],str) or not r['text'] for r in rows):raise ValueError('fresh text required')
    if len({' '.join(r['text'].lower().split()) for r in rows})!=40:raise ValueError('duplicate fresh text')
    bins=Counter(r['group'] for r in rows)
    if bins!={'cross_role':10,'boundary':10,'unfamiliar':10,'ordinary':10}:raise ValueError('fresh primary groups')
    roles=Counter(g[2] for r in rows for g in r['gold'])
    if any(roles[k]<8 for k in ROLES) or sum(not r['gold'] for r in rows)<4:raise ValueError('fresh gold coverage')
    bad=Counter(p['family'] for r in rows for p in r['probes'] if p['expected_role'] is None)
    if bad!={'clipped_path':12,'broken_quote':12,'merged_mentions':12,'nested_fragment':12,'unsupported':4}:raise ValueError('fresh negative coverage')
    for row in rows:
        gold={tuple(g) for g in row['gold']}
        if len(gold)!=len(row['gold']) or any(type(a) is not int or type(b) is not int or not 0<=a<b<=len(row['text']) or role not in ROLES for a,b,role in gold):raise ValueError('invalid fresh gold')
        probe_gold={(p['start'],p['end'],p['expected_role']) for p in row['probes'] if p['expected_role'] is not None}
        if gold!=probe_gold:raise ValueError('fresh gold/probe mismatch')
        seen=set()
        for p in row['probes']:
            a,b=p['start'],p['end'];key=(a,b)
            if type(a) is not int or type(b) is not int or not 0<=a<b<=len(row['text']) or key in seen:raise ValueError('invalid fresh probe offsets')
            seen.add(key)
    return True

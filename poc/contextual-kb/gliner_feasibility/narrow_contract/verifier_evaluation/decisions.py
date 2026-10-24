"""Pure conflict resolution and paired decision accounting; no gold in resolver API."""
import copy
import itertools
import math

ROLES=('api_reference','registration_name','model_key','value','version','ui_adapter')
GRID=tuple(itertools.product((.5,.7,.9),repeat=2))


def probabilities(p):
    return isinstance(p,(list,tuple)) and len(p)==7 and all(type(x) in (int,float) and math.isfinite(x) and 0<=x<=1 for x in p)


def tokens(text,output):
    result=set()
    entities=output['entities']
    if not isinstance(entities,dict) or any(k not in ROLES for k in entities):raise ValueError('unknown entity role')
    for role,items in entities.items():
        for item in items:
            a,b=item['start'],item['end']
            if type(a) is not int or type(b) is not int or not 0<=a<b<=len(text) or text[a:b]!=item['text'] or (a,b,role) in result:
                raise ValueError('invalid raw occurrence')
            result.add((a,b,role))
    return result


def invalid(items):
    return any(a<d and c<b for (a,b,r),(c,d,s) in itertools.combinations(items,2))


def groups(text,raw):
    items=tokens(text,raw); by_span={}
    for a,b,r in sorted(items):by_span.setdefault((a,b),set()).add(r)
    eligible=[];blocked=[]
    for span,roles in by_span.items():
        if len(roles)<2:continue
        if any(other!=span and span[0]<other[1] and other[0]<span[1] for other in by_span):blocked.append(span)
        else:eligible.append(span)
    return eligible,blocked,by_span


def resolve(text,raw,scorer,threshold):
    if tuple(threshold) not in GRID:raise ValueError('threshold outside frozen grid')
    output=copy.deepcopy(raw);log=[]
    try:eligible,blocked,by_span=groups(text,raw)
    except (ValueError,KeyError,TypeError):return output,[dict(decision='invalid_raw')]
    log.extend(dict(start=a,end=b,decision='partial_overlap') for a,b in blocked)
    if len(eligible)>8:return output,[dict(decision='overflow',groups=len(eligible))]
    if not eligible:return output,log
    try:scores=scorer(eligible)
    except Exception as exc:return output,log+[dict(decision='scorer_error',error=type(exc).__name__)]
    for a,b in eligible:
        p=scores.get((a,b));chosen=[]
        if probabilities(p):chosen=[r for r,v in zip(ROLES,p[1:]) if v>=threshold[1]]
        accept=probabilities(p) and p[0]>=threshold[0] and len(chosen)==1 and chosen[0] in by_span[a,b]
        reason=('unsupported' if p is None else 'invalid_scores' if not probabilities(p) else
                'boundary' if p[0]<threshold[0] else 'no_role' if not chosen else
                'multiple_roles' if len(chosen)>1 else 'unproposed_role' if chosen[0] not in by_span[a,b] else 'accepted')
        log.append(dict(start=a,end=b,decision='resolved' if accept else 'unresolved',reason=reason,selected=chosen[0] if accept else None,probabilities=p))
        if accept:
            for role,items in output['entities'].items():
                if role!=chosen[0]:output['entities'][role]=[x for x in items if (x['start'],x['end'])!=(a,b)]
    return output,log


def metrics(pred,gold):
    result={}
    for role in ROLES:
        p={x for x in pred if x[0]==role};g={x for x in gold if x[0]==role}
        tp=len(p&g);precision=tp/len(p) if p else None;recall=tp/len(g) if g else None
        f1=2*tp/(len(p)+len(g)) if p or g else None
        result[role]=dict(precision=precision,recall=recall,f1=f1)
    return result


def assess(cases,threshold):
    totals=dict(correct_repairs=0,wrong_repairs=0,lost_mentions=0,lost_exact=0,invalid_increase=0,errors=0,
                invalid_to_valid_wrong=0,abstentions=0,boundary_failures=0,role_failures=0,prior_repairs_lost=0,gold_probe_failures=0,gold_unsupported=0,negative_total=0,negative_rejected=0,negative_unsupported=0)
    ledger=[];old_all=set();new_all=set();old_raw=set();new_raw=set();gold_all=set();ids=set()
    for c in cases:
        if c['id'] in ids:raise ValueError('duplicate case ID')
        ids.add(c['id']);gold={tuple(x) for x in c['gold']}
        if any(r not in ROLES or not 0<=a<b<=len(c['text']) for a,b,r in gold):raise ValueError('invalid gold')
        lookup={(x['start'],x['end']):x['probabilities'] for x in c['operational_scores']}
        out,log=resolve(c['text'],c['raw'],lambda offsets:{s:lookup.get(s) for s in offsets},threshold)
        before=tokens(c['text'],c['raw']);after=tokens(c['text'],out)
        old_invalid=invalid(before);new_invalid=invalid(after)
        lost=sorted((gold&before)-after);totals['lost_mentions']+=len(lost)
        totals['lost_exact']+=before==gold and after!=gold
        totals['invalid_increase']+=new_invalid and not old_invalid
        totals['invalid_to_valid_wrong']+=old_invalid and not new_invalid and after!=gold
        totals['abstentions']+=sum(x['decision']=='unresolved' for x in log)
        totals['boundary_failures']+=sum(x.get('reason')=='boundary' for x in log)
        totals['role_failures']+=sum(x.get('reason') in ('no_role','multiple_roles','unproposed_role') for x in log)
        totals['errors']+=sum(x['decision'] in ('scorer_error','invalid_raw') for x in log)
        changes=[]
        for x in log:
            if x['decision']=='resolved':
                good=(x['start'],x['end'],x['selected']) in gold
                totals['correct_repairs' if good else 'wrong_repairs']+=1
                changes.append(dict(**x,correct=good))
        for a,b,r in c.get('prior_correct_repairs',[]):
            if {(i,j,k) for i,j,k in after if (i,j)==(a,b)}!={(a,b,r)}:totals['prior_repairs_lost']+=1
        for r in ROLES:
            old_raw.update((r,c['id'],a,b) for a,b,k in before if k==r)
            new_raw.update((r,c['id'],a,b) for a,b,k in after if k==r)
            gold_all.update((r,c['id'],a,b) for a,b,k in gold if k==r)
            if not old_invalid:old_all.update((r,c['id'],a,b) for a,b,k in before if k==r)
            if not new_invalid:new_all.update((r,c['id'],a,b) for a,b,k in after if k==r)
        probes=[]
        for p in c['probes']:
            z=p['probabilities'];supported=probabilities(z);expected=p['expected_role']
            if expected is not None:
                if expected not in ROLES:raise ValueError('unknown probe role')
                passing=[r for r,v in zip(ROLES,z[1:]) if v>=threshold[1]] if supported else []
                correct=supported and z[0]>=threshold[0] and passing==[expected]
                totals['gold_probe_failures']+=not correct;totals['gold_unsupported']+=not supported
            else:
                totals['negative_total']+=1;totals['negative_unsupported']+=not supported
                correct=supported and z[0]<threshold[0];totals['negative_rejected']+=correct
            probes.append(dict(**p,correct=bool(correct)))
        ledger.append(dict(id=c['id'],before=sorted(before),after=sorted(after),lost=lost,gained=sorted((gold&after)-before),resolutions=changes,decisions=log,probes=probes))
    old_metrics=metrics(old_all,gold_all);new_metrics=metrics(new_all,gold_all)
    regressed=[r+':'+k for r in ROLES for k,v in old_metrics[r].items() if v is not None and (new_metrics[r][k] is None or new_metrics[r][k]<v-1e-12)]
    raw_old=metrics(old_raw,gold_all);raw_new=metrics(new_raw,gold_all)
    regressed.extend('raw:'+r+':'+k for r in ROLES for k,v in raw_old[r].items() if v is not None and (raw_new[r][k] is None or raw_new[r][k]<v-1e-12))
    supported=totals['negative_total']-totals['negative_unsupported']
    return dict(**totals,negative_supported=supported,supported_rejection_fraction=totals['negative_rejected']/supported if supported else None,raw_baseline_metrics=raw_old,raw_candidate_metrics=raw_new,rejection_fraction=totals['negative_rejected']/totals['negative_total'] if totals['negative_total'] else 0.,metric_regressions=regressed,baseline_metrics=old_metrics,candidate_metrics=new_metrics,ledger=ledger)


def select_thresholds(by_seed,split):
    if split!='calibration' or set(by_seed)!={'1701','1702'}:raise ValueError('calibration with both seeds required')
    ids=[[c['id'] for c in by_seed[s]] for s in ('1701','1702')]
    if not ids[0] or ids[0]!=ids[1]:raise ValueError('paired case coverage differs')
    candidates=[]
    for pair in GRID:
        summaries={s:assess(rows,pair) for s,rows in by_seed.items()}
        eligible=all(not any(d[k] for k in ('wrong_repairs','invalid_to_valid_wrong','lost_mentions','lost_exact','gold_probe_failures','gold_unsupported','errors')) for d in summaries.values())
        rank=[min(d['correct_repairs'] for d in summaries.values()),min(d['rejection_fraction'] for d in summaries.values()),sum(d['correct_repairs'] for d in summaries.values()),*pair]
        candidates.append(dict(threshold=list(pair),eligible=eligible,rank=rank,by_seed=summaries))
    eligible=[c for c in candidates if c['eligible']]
    winner=max(eligible,key=lambda c:c['rank']) if eligible else None
    return dict(selected=winner['threshold'] if winner else None,diagnostic_only=not winner or winner['rank'][0]==0,candidates=candidates)


def qualification(groups_by_seed,p95):
    if set(groups_by_seed)!={'1701','1702'} or set(p95)!={'1701','1702'}:raise ValueError('both seeds required')
    issues=[]
    if set(groups_by_seed['1701'])!=set(groups_by_seed['1702']) or 'fresh' not in groups_by_seed['1701']:raise ValueError('paired split coverage differs')
    for s,groups_ in groups_by_seed.items():
        if not math.isfinite(p95[s]) or p95[s]>1 or p95[s]<0:issues.append(s+':latency')
        for name,d in groups_.items():
            keys=('wrong_repairs','invalid_to_valid_wrong','lost_mentions','lost_exact','invalid_increase','errors','prior_repairs_lost','gold_probe_failures','gold_unsupported')
            issues.extend(s+':'+name+':'+k for k in keys if d[k])
            issues.extend(s+':'+name+':'+k for k in d['metric_regressions'])
            if d['negative_total'] and d['rejection_fraction']<.9:issues.append(s+':'+name+':rejection')
            if name=='fresh' and d['correct_repairs']<1:issues.append(s+':no_fresh_repair')
    return dict(passed=not issues,issues=issues)

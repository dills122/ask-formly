"""Diagnostic scores on fixed extracted spans; never alters extractor outputs."""
import collections
import copy
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'verifier_evaluation'))
from decisions import ROLES, tokens, groups, probabilities, invalid


def decision(p):
    if p is None:return dict(role=None,reason='unsupported')
    if not probabilities(p):raise ValueError('invalid probabilities')
    passing=[r for r,v in zip(ROLES,p[1:]) if v>=.5]
    reason='boundary' if p[0]<.5 else 'no_role' if not passing else 'multiple_roles' if len(passing)>1 else 'accepted'
    return dict(role=passing[0] if reason=='accepted' else None,reason=reason)


def validate(rows):
    ids=set()
    for row in rows:
        if row['id'] in ids:raise ValueError('duplicate id')
        ids.add(row['id']);text=row['text'];gold=[tuple(g) for g in row['gold']]
        if not isinstance(text,str) or not text:raise ValueError('empty question')
        if len(gold)!=len(set(gold)) or invalid(gold):raise ValueError('duplicate/overlapping gold')
        if any(type(a) is not int or type(b) is not int or not 0<=a<b<=len(text) or r not in ROLES for a,b,r in gold):raise ValueError('invalid gold')
        seen=set();probe_gold=set()
        for p in row['probes']:
            a,b,r=p['start'],p['end'],p['expected_role']
            if type(a) is not int or type(b) is not int or not 0<=a<b<=len(text) or (a,b) in seen:raise ValueError('invalid/duplicate probe')
            seen.add((a,b))
            if r is not None:
                if r not in ROLES:raise ValueError('invalid role')
                probe_gold.add((a,b,r))
        if set(gold)!=probe_gold:raise ValueError('gold probe mismatch')
    return True


def collect(rows,extract,score):
    validate(rows);records=[]
    def checked(text,offsets):
        result=score(text,offsets) if offsets else {}
        if set(result)!=set(offsets):raise ValueError('score coverage differs')
        for p in result.values():decision(p)
        return result
    # Operational pass does not use gold or supplied probes for candidate generation.
    for row in rows:
        start=time.perf_counter();raw=copy.deepcopy(extract(row['text']));extract_s=time.perf_counter()-start
        raw_tokens=tokens(row['text'],raw)
        if 'expected_raw' in row and raw!=row['expected_raw']:raise ValueError('baseline cache drift')
        offsets=sorted({(a,b) for a,b,r in raw_tokens})
        start=time.perf_counter();scores=checked(row['text'],offsets);score_s=time.perf_counter()-start
        records.append(dict(id=row['id'],text=row['text'],raw=raw,operational_scores=[dict(start=a,end=b,probabilities=scores[a,b]) for a,b in offsets],seconds=dict(extraction=extract_s,all_span_verifier=score_s)))
    # Oracle pass remains separate and cannot create operational candidates.
    for row,record in zip(rows,records):
        offsets=sorted({(p['start'],p['end']) for p in row['probes']})
        start=time.perf_counter();scores=checked(row['text'],offsets);elapsed=time.perf_counter()-start
        record.update(gold=copy.deepcopy(row['gold']),probes=[dict(**p,probabilities=scores[p['start'],p['end']]) for p in row['probes']])
        record['seconds']['oracle_verifier']=elapsed
    return records


def summarize(records):
    names=('questions','baseline_mentions','baseline_correct','baseline_extra','gold_mentions','gold_missing_typed','gold_missing_exact_span','eligible_groups','partial_overlap_groups','correct_endorsed','correct_wrong_role_endorsements','correct_abstentions','wrong_role_repair_opportunities','wrong_endorsed','invalid_span_boundary_rejected','operational_unsupported','oracle_gold','oracle_gold_pass','oracle_gold_unsupported','oracle_negative','oracle_negative_rejected','oracle_negative_unsupported')
    counts=collections.Counter({n:0 for n in names});ledger=[]
    for row in records:
        gold={tuple(g) for g in row['gold']};raw=tokens(row['text'],row['raw']);lookup={(p['start'],p['end']):p['probabilities'] for p in row['operational_scores']}
        if set(lookup)!={(a,b) for a,b,r in raw}:raise ValueError('missing operational scores')
        eligible,blocked,_=groups(row['text'],row['raw']);counts['eligible_groups']+=len(eligible);counts['partial_overlap_groups']+=len(blocked)
        counts['questions']+=1;counts['baseline_mentions']+=len(raw);counts['baseline_correct']+=len(raw&gold);counts['baseline_extra']+=len(raw-gold)
        counts['gold_mentions']+=len(gold);counts['gold_missing_typed']+=len(gold-raw);counts['gold_missing_exact_span']+=sum(not any(a==i and b==j for i,j,r in raw) for a,b,k in gold)
        observations=[]
        for a,b,r in sorted(raw):
            d=decision(lookup[a,b]);expected=next((k for i,j,k in gold if i==a and j==b),None);correct=(a,b,r) in gold
            counts['operational_unsupported']+=d['reason']=='unsupported'
            if correct:
                counts['correct_endorsed']+=d['role']==r
                counts['correct_wrong_role_endorsements']+=d['role'] is not None and d['role']!=r
                counts['correct_abstentions']+=d['role'] is None
            else:
                counts['wrong_role_repair_opportunities']+=expected is not None and d['role']==expected
                counts['wrong_endorsed']+=d['role']==r
                counts['invalid_span_boundary_rejected']+=expected is None and d['reason']=='boundary'
            observations.append(dict(start=a,end=b,raw_role=r,expected_role=expected,baseline_correct=correct,verifier=d,probabilities=lookup[a,b]))
        for p in row['probes']:
            d=decision(p['probabilities']);expected=p['expected_role']
            if expected is None:
                counts['oracle_negative']+=1;counts['oracle_negative_rejected']+=d['reason']=='boundary';counts['oracle_negative_unsupported']+=d['reason']=='unsupported'
            else:
                counts['oracle_gold']+=1;counts['oracle_gold_pass']+=d['role']==expected;counts['oracle_gold_unsupported']+=d['reason']=='unsupported'
        ledger.append(dict(id=row['id'],observations=observations,missing_typed=sorted(gold-raw)))
    return dict(counts,diagnostic_threshold=[.5,.5],outputs_modified=False,ledger=ledger)

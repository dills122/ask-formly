"""Frozen-output replay. No model or DB imports."""
import hashlib
import json
import time
from collections import Counter
from pathlib import Path
from repairs import repair, ROLES, validate
from contract import tokens, counts, metrics
HERE=Path(__file__).resolve().parent
PILOT=HERE.parent/'pilot'

def stats(pairs):
    out={}
    for mode in ('diagnostic','accepted'):
        totals={k:dict(tp=0,fp=0,fn=0) for k in ('all',*ROLES)}
        for r,gold in pairs:
            e=r['envelope'];p=tokens(e['mentions']) if mode=='diagnostic' or e['status']=='ok' else set()
            g=tokens(gold['mentions'])
            for role,c in totals.items():
                a={s for s in p if role=='all' or s[0]==role}
                b={s for s in g if role=='all' or s[0]==role}
                for k,v in counts(a,b).items():c[k]+=v
        out[mode]={k:metrics(v) for k,v in totals.items()}
    out['exact']=sum(r['envelope']['status']==g['status'] and r['envelope']['issues']==g['issues']
                     and tokens(r['envelope']['mentions'])==tokens(g['mentions'])
                     and r['envelope']['status']!='extraction_error' for r,g in pairs)
    out['status_counts']=dict(Counter(r['envelope']['status'] for r,g in pairs))
    out['status_matches']=sum(r['envelope']['status']==g['status'] for r,g in pairs)
    out['questions']=len(pairs)
    out['seconds']=sum(r.get('repair_seconds',0) for r,g in pairs)
    return out

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(manifest,root=None):
    for name,h in json.loads(manifest.read_text()).items():
        p=root/name if root else Path(name)
        if digest(p)!=h:raise ValueError('changed '+str(p))
def main():
    check(HERE/'test-output/implementation-freeze.json')
    check(PILOT/'test-output/final-freeze.json',PILOT)
    # Counterexample author controls its separate freeze format, preserved verbatim.
    questions=json.loads((PILOT/'questions.json').read_text())
    gold={g['question_id']:g for g in json.loads((PILOT/'gold.json').read_text())}
    raw=[json.loads(line) for line in (PILOT/'test-output/predictions.jsonl').read_text().splitlines()]
    rowmap={(r['schema'],r['id']):r for r in raw}
    if len(rowmap)!=48 or len(raw)!=48:raise ValueError('prediction coverage')
    results={};report={}
    for schema in ('bare','described'):
        for stage in range(4):
            key=f'{schema}-{stage}';rows=[]
            for q in questions:
                start=time.perf_counter()
                r=repair(q['id'],q['question'],rowmap[schema,q['id']],stage)
                r.update(id=q['id'],repair_seconds=time.perf_counter()-start)
                validate(r['envelope'],q['id'],q['question'])
                rows.append(r)
            results[key]=rows
            pairs=[(r,gold[r['id']]) for r in rows]
            cell=stats(pairs)
            cell['operations']=dict(Counter(e['operation'] for r in rows for e in r['log']))
            cell['raw_duplicates']=sum(r['duplicate_count'] for r in rows)
            cell['groups']={}
            for field in ('origin','family','parent'):
                groups={}
                for group in sorted({q[field] for q in questions}):
                    ids={q['id'] for q in questions if q[field]==group}
                    selected=[p for p in pairs if p[0]['id'] in ids]
                    groups[group]=stats(selected)
                    if field=='parent':
                        p={(s[0],s[3]) for r,g in selected for s in tokens(r['envelope']['mentions'])}
                        g={(s[0],s[3]) for r,g in selected for s in tokens(g['mentions'])}
                        groups[group]['unique_diagnostic']=counts(p,g)
                cell['groups'][field]=groups
            cell['special']={}
            for label,predicate in {
                'compound_api':lambda s:s[0]=='api_reference' and ('.' in s[3] or '[' in s[3]),
                'quoted_names_keys_values':lambda s:s[0] in ('registration_name','model_key','value') and s[3][:1] in ("'",'"')
            }.items():
                expected=found=0
                for r,g in pairs:
                    wanted={s for s in tokens(g['mentions']) if predicate(s)}
                    expected+=len(wanted);found+=len(wanted&tokens(r['envelope']['mentions']))
                cell['special'][label]=dict(expected=expected,found=found)
            cell['empty']={}
            for status in ('ok','needs_review'):
                selected=[(r,g) for r,g in pairs if not g['mentions'] and g['status']==status]
                cell['empty'][status]=dict(total=len(selected),nonempty=sum(bool(r['envelope']['mentions']) for r,g in selected),
                    exact=stats(selected)['exact'])
            cell['changes']=[]
            for r,g in pairs:
                p=tokens(r['envelope']['mentions']);expected=tokens(g['mentions'])
                original=tokens(r['raw_mentions'])
                prior=next(x for x in results[f'{schema}-0'] if x['id']==r['id'])
                base=tokens(prior['envelope']['mentions']) if prior['envelope']['status']=='ok' else set()
                accepted=p if r['envelope']['status']=='ok' else set()
                cell['changes'].append(dict(id=r['id'],gained=sorted((p&expected)-original),
                  lost=sorted((original&expected)-p),new_wrong_delivered=sorted((p-expected)-original),
                  new_wrong_accepted=sorted((accepted-expected)-base)))
            report[key]=cell
    old=json.loads((PILOT/'test-output/scores.json').read_text())
    for schema in ('bare','described'):
        assert report[f'{schema}-0']['accepted']==old[schema]['accepted']
        assert report[f'{schema}-0']['exact']==old[schema]['exact']
    # No repairs/gold revised after this first independent execution.
    cases=json.loads((HERE/'counterexamples.json').read_text())
    counter=[]
    for c in cases:
        r=repair(c['id'],c['question'],c['row'],3)
        actual={k:r['envelope'][k] for k in ('status','mentions','issues')}
        counter.append(dict(id=c['id'],family=c['family'],passed=actual==c['expected'],
                            actual=actual,expected=c['expected'],log=r['log']))
    for name,data in [('replay.json',results),('scores.json',report),('counterexample-results.json',counter)]:
        with (HERE/'test-output'/name).open('x') as f:json.dump(data,f,indent=2)
    print(json.dumps({k:{f:v[f] for f in ('diagnostic','accepted','exact','status_counts','special','seconds')} for k,v in report.items()},indent=2))
    print('counterexamples',sum(c['passed'] for c in counter),'/',len(counter))
if __name__=='__main__':main()

"""Fixed denominators: absent/duplicate/failed assessments never disappear."""
import argparse,json,math
from pathlib import Path


def times(values):
    values=sorted(values)
    return dict(n=len(values),p50=values[math.ceil(len(values)*.5)-1] if values else None,p95=values[math.ceil(len(values)*.95)-1] if values else None)


def summary(root,cases,repeats):
    rounds=[]
    for repeat in range(1,repeats+1):
        for arm in ('baseline','candidate'):
            observed=[]
            for path in root.glob(f'r{repeat}-b*-{arm}/assessment/results.json'):
                try:observed.extend(json.loads(path.read_text())['rows'])
                except (OSError,ValueError,KeyError):pass
            rows=[]
            for case in cases:
                found=[r for r in observed if r.get('id')==case['id']]
                if len(found)!=1:
                    rows.append(dict(id=case['id'],category=case['category'],usable=False,critical=False,error='Missing/duplicate assessment'));continue
                row=found[0];assessment=row.get('assessment',{})
                rows.append(dict(id=case['id'],category=case['category'],usable=bool(row.get('usable',False)),critical=assessment.get('critical',False),delivery_errors=row.get('delivery_errors',[]),rationale=assessment.get('rationale',''),missing_aspects=assessment.get('missing_aspects',[]),pool_coverage=assessment.get('pool_coverage',0),foundation_coverage=assessment.get('foundation_coverage',0),final_coverage=assessment.get('final_coverage',0),seconds=row.get('seconds'),advisory=row.get('advisory'),selection=row.get('selection')))
            categories={}
            for category in sorted({c['category'] for c in cases}):
                subset=[r for r in rows if r['category']==category]
                categories[category]=dict(usable=sum(r['usable'] for r in subset),total=len(subset),critical=sum(r['critical'] for r in subset),**{stage:sum(r.get(stage,0) for r in subset)/len(subset) for stage in ['pool_coverage','foundation_coverage','final_coverage']})
            cold=[];warm=[]
            for job in root.glob(f'r{repeat}-b*-{arm}'):
                if not (job/'prompt.json').exists():continue
                prompts=json.loads((job/'prompt.json').read_text());audits=[json.loads(p.read_text()) for p in (job/'mcp/audit').glob('*.json')]
                for i,prompt in enumerate(prompts):
                    matches=[a for a in audits if a['request']==prompt['request']]
                    if len(matches)==1:(cold if i==0 else warm).append(matches[0]['seconds'])
            rounds.append(dict(round=repeat,arm=arm,total=len(cases),usable=sum(r['usable'] for r in rows),critical=sum(r['critical'] for r in rows),categories=categories,cold_call_seconds=times(cold),warm_call_seconds=times(warm),rows=rows))
    return dict(method='Automated separate-context semantic judgments plus deterministic delivery checks; final independent audit required. Fixed expected denominators include missing results.',rounds=rounds)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--cases',required=True);p.add_argument('--repeats',type=int,default=1);args=p.parse_args()
    root=Path(args.root);cases=json.loads(Path(args.cases).read_text())['cases'];result=summary(root,cases,args.repeats)
    (root/'summary.json').write_text(json.dumps(result,indent=2))
    for row in result['rounds']:print(row['round'],row['arm'],row['usable'],'/',row['total'],'critical',row['critical'])

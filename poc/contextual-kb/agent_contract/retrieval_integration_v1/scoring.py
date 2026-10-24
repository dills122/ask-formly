"""Fixed retrieval relevance and per-batch extraction consistency accounting."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parents[1]
sys.path.insert(0,str(POC));sys.path.insert(0,str(HERE.parent/'gliner_integration_v1'))
from agent_contract.gliner_integration_v1.assessment import metrics,extraction_coverage
from agent_contract.gliner_integration_v1.integration import map_hints
from bridge import consistency

def retrieval_summary(rows,k='8'):
    scored=[r['metrics'][k] for r in rows if r['metrics'][k]['recall'] is not None]
    mean=lambda key:sum(s[key] for s in scored)/len(scored) if scored else None
    return dict(cases=len(rows),supported=len(scored),recall=mean('recall'),precision=mean('precision'),ndcg=mean('ndcg'),mrr=mean('mrr'),group_recall=mean('group_recall'),
                complete_groups=sum(s['complete_groups'] for s in scored),unsupported_candidates=sum(r['metrics'][k]['unsupported_candidates'] for r in rows),
                query_count=sum(r['query_count'] for r in rows),seconds=sum(r['seconds'] for r in rows))

def bridge_pass(base,arm,lost_complete=0):
    return (lost_complete==0 and base['recall'] is not None and arm['recall'] is not None and arm['recall']-base['recall']>=.02 and arm['precision']>=base['precision'] and arm['complete_groups']>=base['complete_groups'] and arm['unsupported_candidates']<=base['unsupported_candidates'])

def read(p):return json.loads(p.read_text())
def jsonlines(p):return [json.loads(s) for s in p.read_text().splitlines()]
def main():
    records=read(HERE/'data/records.json');byid={r['id']:r for r in records};gold=read(HERE/'data/gold.json')
    if any(r.get('alternatives') for r in gold):raise ValueError('unresolved annotation alternatives')
    extraction={}
    for arm in ('foundation','1701','1702'):
        outputs=jsonlines(HERE/f'test-output/extraction/{arm}.jsonl')
        if [r['id'] for r in outputs]!=[r['id'] for r in records]:raise ValueError('missing/reordered extraction records')
        raw_predictions={};accepted_predictions={};errors=[];safe=0
        for out in outputs:
            record=byid[out['id']];core=record['output'];plan=out['plan']
            safe+=plan['question_plan']==core and plan['search_requests']==[{'query':q['question']} for q in core['formly_questions']]
            failures=extraction_coverage(arm,core['formly_questions'],out['extractions'])
            errors.extend(dict(id=out['id'],error=e) for e in failures)
            if failures:continue
            for i,q in enumerate(core['formly_questions']):
                key=f"{out['id']}-q{i}"
                accepted_predictions[key]=[h for h in plan['role_hints'] if h['question_index']==i]
                raw_predictions[key]=[]
            for e in out['extractions']:
                key=f"{out['id']}-q{e['question_index']}"
                if e['error']:errors.append(dict(id=key,error=e['error']))
                try:raw_predictions[key]=map_hints(e['raw'],e['question_index'])
                except (ValueError,KeyError,TypeError):pass
        panels={}
        for batch in ('all',1,2,3):
            selected=[r for r in gold if batch=='all' or r['batch']==batch]
            raw=metrics(selected,raw_predictions);accepted=metrics(selected,accepted_predictions)
            for m in (raw,accepted):m.pop('value_gate',None)
            c=consistency(**{k:accepted['typed'][k] for k in ('tp','fp','fn')})
            panels[str(batch)]=dict(raw=raw,accepted=accepted,consistency=c)
        extraction[arm]=dict(records=len(outputs),core_preserved=safe,errors=errors,panels=panels,
                             consistent=not errors and safe==len(records) and all(p['consistency']['within_tolerance'] and not p['accepted']['missing'] for p in panels.values()))
    rows=jsonlines(HERE/'test-output/retrieval/results.jsonl')
    if len(rows)!=144 or len({(r['id'],r['arm']) for r in rows})!=144:raise ValueError('retrieval coverage')
    retrieval={}
    for arm in ('foundation','1701','1702','oracle'):
        subset=[r for r in rows if r['arm']==arm]
        if {r['id'] for r in subset}!=set(byid):raise ValueError('retrieval identities')
        retrieval[arm]={'all':{k:retrieval_summary(subset,k) for k in ('4','8')},'batches':{str(b):retrieval_summary([r for r in subset if r['batch']==b]) for b in (1,2,3)}}
    baseline={r['id']:r for r in rows if r['arm']=='foundation'};differences=[]
    for r in rows:
        if r['arm']=='foundation':continue
        b=baseline[r['id']];differences.append(dict(id=r['id'],arm=r['arm'],baseline=b['metrics']['8'],enhanced=r['metrics']['8'],added=sorted(set(r['ids'])-set(b['ids'])),lost=sorted(set(b['ids'])-set(r['ids']))))
    paired_losses={arm:sum(d['baseline']['complete_groups'] is True and d['enhanced']['complete_groups'] is False for d in differences if d['arm']==arm) for arm in ('1701','1702','oracle')}
    passed={arm:bridge_pass(retrieval['foundation']['all']['8'],retrieval[arm]['all']['8'],paired_losses[arm]) for arm in ('1701','1702','oracle')}
    report=dict(paired_complete_losses=paired_losses,extraction=extraction,retrieval=retrieval,differences=differences,bridge_gates=passed,both_models_help=passed['1701'] and passed['1702'])
    with (HERE/'test-output/scores.json').open('x') as f:json.dump(report,f,indent=2)
    print(json.dumps(dict(retrieval={a:r['all']['8'] for a,r in retrieval.items()},gates=passed,consistency={a:r['consistent'] for a,r in extraction.items()}),indent=2))
if __name__=='__main__':main()

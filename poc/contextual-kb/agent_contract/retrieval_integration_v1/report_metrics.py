"""Descriptive reporting from first outputs; no prediction changes."""
import json
from pathlib import Path
from scoring import retrieval_summary,jsonlines
from agent_contract.gliner_integration_v1.integration import summarize_times
HERE=Path(__file__).resolve().parent

def main():
 rows=jsonlines(HERE/'test-output/retrieval/results.jsonl');scores=json.loads((HERE/'test-output/scores.json').read_text());report={}
 for arm in ('foundation','1701','1702','oracle'):
  selected=[r for r in rows if r['arm']==arm];panels={}
  for batch in ('all',1,2,3):
   subset=[r for r in selected if batch=='all' or r['batch']==batch];panels[str(batch)]={}
   for k in ('4','8'):
    metrics=[r['metrics'][k] for r in subset if r['metrics'][k]['recall'] is not None]
    panels[str(batch)][k]=dict(retrieval_summary(subset,k),any_hit=sum(m['mrr']>0 for m in metrics)/len(metrics))
  report[arm]=dict(retrieval=panels,retrieval_request_seconds=summarize_times([r['seconds'] for r in selected]))
  if arm!='oracle':
   outputs=jsonlines(HERE/f'test-output/extraction/{arm}.jsonl')
   report[arm]['timing']={key:summarize_times([r[key] for r in outputs]) for key in ('extraction_seconds','projection_seconds')}
   if arm!='foundation':report[arm]['model_load_seconds']=json.loads((HERE/f'test-output/extraction/{arm}-before.json').read_text())['load_seconds']
   report[arm]['count_sensitivity']={}
   for b,p in scores['extraction'][arm]['panels'].items():
    t=p['accepted']['typed'];n=t['tp']+t['fp'];report[arm]['count_sensitivity'][b]=dict(predictions=n,one_wrong_instead_of_right_percentage_points=100/n if n else None)
 report['retrieval_setup']=json.loads((HERE/'test-output/retrieval/setup.json').read_text())
 with (HERE/'test-output/report-metrics.json').open('x') as f:json.dump(report,f,indent=2)
if __name__=='__main__':main()

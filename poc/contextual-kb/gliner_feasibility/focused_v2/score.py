"""Exact typed spans and paired unique-atom recall, without boundary normalization."""
import json
from pathlib import Path
TYPES=('api','custom_identifier','literal','version','ui_adapter')
def spans(text,entities):
 if not isinstance(entities,dict) or set(entities)-set(TYPES):raise ValueError('entity map')
 out=set()
 for label,values in entities.items():
  if not isinstance(values,list):raise ValueError('entity list')
  for s in values:
   a,b=s['start'],s['end']
   if type(a)!=int or type(b)!=int or not 0<=a<b<=len(text) or text[a:b]!=s['text']:raise ValueError('invalid span')
   out.add((label,a,b,s['text']))
 return out
def counts(pred,gold):return dict(tp=len(pred&gold),fp=len(pred-gold),fn=len(gold-pred))
def metrics(c):
 t,p,n=c['tp'],c['fp'],c['fn']
 return {**c,'precision':t/(t+p) if t+p else None,'recall':t/(t+n) if t+n else None,'f1':2*t/(2*t+p+n) if 2*t+p+n else None}
def shared_recall(og,fg,op,fp):
 shared=og&fg
 return {'shared':len(shared),'original_found':len(shared&op),'focused_found':len(shared&fp)}
def prediction(text,row):
 try:
  if row is None:raise ValueError('missing prediction')
  if 'error' in row:raise ValueError(row['error'])
  output=row['output']
  if not isinstance(output,dict):raise ValueError('invalid output')
  records=output.get('request',[])
  if not isinstance(records,list):raise ValueError('invalid request records')
  interpretation=output.get('interpretation',{})
  if not isinstance(interpretation,dict):raise ValueError('invalid interpretation')
  return spans(text,output['entities']),None,len(records),interpretation.get('label')
 except (ValueError,KeyError,TypeError) as e:return set(),str(e),0,None
def main():
 here=Path(__file__).resolve().parent
 inputs=json.loads((here/'inputs.json').read_text());byid={r['id']:r for r in inputs}
 labels=sum([json.loads((here/f'gold-{i}.json').read_text()) for i in (1,2,3)],[])
 assert len(labels)==len(byid) and {r['id'] for r in labels}==set(byid)
 gold={}
 for r in labels:
  assert set(r['entities'])==set(TYPES)
  gold[r['id']]=spans(byid[r['id']]['question'],r['entities'])
 report={}
 for model in ['base','adapted']:
  for schema in ['full','entities']:
   rows=[json.loads(l) for l in (here/f'test-output/{model}-{schema}.jsonl').read_text().splitlines()]
   rowmap={r['id']:r for r in rows}
   assert len(rowmap)==len(rows) and set(rowmap)<=set(byid), 'duplicate/unknown prediction ID'
   preds={};errors=[];records=0;keys=set();interpretations={}
   for id,source in byid.items():
    r=rowmap.get(id)
    p,error,n,label=prediction(source['question'],r)
    preds[id]=p;records+=n
    if error is not None:errors.append({'id':id,'error':error})
    if label is not None:interpretations[label]=interpretations.get(label,0)+1
    if r and isinstance(r.get('output'),dict):keys.update(r['output'])
   cell={'errors':errors,'request_records':records,'interpretation_labels':interpretations,'output_keys':sorted(keys),'arms':{},'parents':{},'shared':{}}
   for arm in ['original','focused']:
    ids=[r['id'] for r in inputs if r['arm']==arm];scores={}
    for label in ['all',*TYPES]:
     c=dict(tp=0,fp=0,fn=0)
     for id in ids:
      p={s for s in preds[id] if label=='all' or s[0]==label};g={s for s in gold[id] if label=='all' or s[0]==label}
      for k,v in counts(p,g).items():c[k]+=v
     scores[label]=metrics(c)
    scores['seconds']=sum(r['seconds'] for r in rows if r['id'] in ids)
    scores['inputs']=len(ids);cell['arms'][arm]=scores
   shared_total=dict(shared=0,original_found=0,focused_found=0)
   for parent in sorted({r['parent'] for r in inputs}):
    atoms={};parent_scores={}
    for arm in ['original','focused']:
     ids=[r['id'] for r in inputs if r['parent']==parent and r['arm']==arm]
     atoms[arm]=[set((s[0],s[3]) for id in ids for s in source[id]) for source in (gold,preds)]
     c=dict(tp=0,fp=0,fn=0)
     for id in ids:
      for k,v in counts(preds[id],gold[id]).items():c[k]+=v
     parent_scores[arm]={**metrics(c),'inputs':len(ids),'agent_abstention':arm=='focused' and not ids,'seconds':sum(r['seconds'] for r in rows if r['id'] in ids)}
    shared=shared_recall(atoms['original'][0],atoms['focused'][0],atoms['original'][1],atoms['focused'][1])
    parent_scores['shared']=shared;cell['parents'][parent]=parent_scores
    for k,v in shared.items():shared_total[k]+=v
   cell['shared']=shared_total;report[model+'-'+schema]=cell
 with (here/'test-output/scores.json').open('w') as f:json.dump(report,f,indent=2)
 print(json.dumps({k:{'arms':v['arms'],'shared':v['shared'],'errors':len(v['errors']),'records':v['request_records']} for k,v in report.items()},indent=2))
if __name__=='__main__':main()

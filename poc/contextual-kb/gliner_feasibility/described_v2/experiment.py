"""Description-only GLiNER ablation; frozen inputs, no training or retrieval."""
import json,sys,os,time,hashlib,gc
from pathlib import Path
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parent/'focused_v2'
sys.path.insert(0,str(PRIOR))
from score import TYPES,spans,counts,metrics,prediction

def evaluate(inputs,gold,rows):
 byid={r['id']:r for r in inputs}; rowmap={r['id']:r for r in rows}
 if len(rowmap)!=len(rows) or set(rowmap)-set(byid):raise ValueError('duplicate/unknown prediction')
 preds={};errors=[];exact=0
 for id,r in byid.items():
  p,error,_,_=prediction(r['question'],rowmap.get(id));preds[id]=p
  if error is not None:errors.append({'id':id,'error':error})
  elif p==gold[id]:exact+=1
 def total(ids,label='all',unique=False):
  c=dict(tp=0,fp=0,fn=0)
  if unique:
   p={(s[0],s[3]) for id in ids for s in preds[id]}
   g={(s[0],s[3]) for id in ids for s in gold[id]}
   return metrics(counts(p,g))
  for id in ids:
   p={s for s in preds[id] if label=='all' or s[0]==label}
   g={s for s in gold[id] if label=='all' or s[0]==label}
   for k,v in counts(p,g).items():c[k]+=v
  return metrics(c)
 result={label:total(byid,label) for label in ['all',*TYPES]}
 result.update(errors=errors,exact_questions=exact,inputs=len(inputs),parents={})
 for parent in sorted({r['parent'] for r in inputs}):
  ids=[r['id'] for r in inputs if r['parent']==parent]
  result['parents'][parent]={'all':total(ids),'unique':total(ids,unique=True),
     'seconds':sum(rowmap[id].get('seconds',0) for id in ids if id in rowmap)}
 result['seconds']=sum(r.get('seconds',0) for r in rows)
 return result

def sources():
 return [HERE/'labels.json',HERE/'PROTOCOL.md',HERE/'experiment.py',
         PRIOR/'inputs.json',PRIOR/'score.py',*[PRIOR/f'gold-{i}.json' for i in (1,2,3)],
         *[PRIOR/f'test-output/{m}-entities.jsonl' for m in ('base','adapted')]]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check_freeze():
 for p,h in json.loads((HERE/'test-output/freeze.json').read_text()).items():
  if digest(Path(p))!=h:raise ValueError('changed source: '+p)
def inputs():
 return [r for r in json.loads((PRIOR/'inputs.json').read_text()) if r['arm']=='focused']
def run():
 os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HOME=str(HERE/'test-output/.cache'))
 sys.path.insert(0,str(HERE.parent/'adaptation/full_training'))
 from native import load_model,PeftModel
 import torch
 torch.use_deterministic_algorithms(True)
 labels=json.loads((HERE/'labels.json').read_text())
 assert list(labels)==list(TYPES)
 for p,h in json.loads((PRIOR/'input-freeze.json').read_text()).items():
  if digest(Path(p))!=h:raise ValueError('changed original: '+p)
 with (HERE/'test-output/freeze.json').open('x') as f:json.dump({str(p):digest(p) for p in sources()},f,indent=2)
 for model_name in ('base','adapted'):
  start=time.perf_counter();model=load_model()
  if model_name=='adapted':
   model=PeftModel.from_pretrained(model,str(HERE.parent/'adaptation/full_training/test-output/full-seed-1701/checkpoint-8/adapter'),is_trainable=False)
  model.eval();load_seconds=time.perf_counter()-start
  schemas={'bare':model.create_schema().entities(list(TYPES)),
           'described':model.create_schema().entities(labels)}
  assert dict(schemas['described'].schema['entity_descriptions'])==labels
  with (HERE/f'test-output/{model_name}-schemas.json').open('x') as f:
   json.dump({k:s.to_dict() for k,s in schemas.items()},f,indent=2)
  with (HERE/f'test-output/{model_name}.jsonl').open('x') as f:
   for i,r in enumerate(inputs()):
    for name in (('bare','described') if i%2==0 else ('described','bare')):
     start=time.perf_counter()
     try:
      with torch.inference_mode():
       output=model.extract(r['question'],schemas[name],threshold=.5,include_spans=True,include_confidence=True,overlap_policy='nested')
      result={'output':output}
     except Exception as e:result={'error':type(e).__name__+': '+str(e)}
     result.update(id=r['id'],schema=name,model=model_name,seconds=time.perf_counter()-start,load_seconds=load_seconds)
     f.write(json.dumps(result)+'\n');f.flush()
    if (i+1)%15==0:print(model_name,i+1,flush=True)
  del model;gc.collect()
 check_freeze()

def score():
 check_freeze();questions=inputs();lookup={r['id']:r for r in questions}
 gold={}
 for i in (1,2,3):
  for r in json.loads((PRIOR/f'gold-{i}.json').read_text()):
   if r['id'] in lookup:gold[r['id']]=spans(lookup[r['id']]['question'],r['entities'])
 assert set(gold)==set(lookup)
 report={}
 for model in ('base','adapted'):
  raw=[json.loads(l) for l in (HERE/f'test-output/{model}.jsonl').read_text().splitlines()]
  if any(r.get('schema') not in ('bare','described') for r in raw):raise ValueError('unknown schema')
  for schema in ('bare','described'):
   rows=[r for r in raw if r['schema']==schema]
   report[model+'-'+schema]=evaluate(questions,gold,rows)
  old={r['id']:r for r in map(json.loads,(PRIOR/f'test-output/{model}-entities.jsonl').read_text().splitlines())}
  bare=[r for r in raw if r['schema']=='bare']
  report[model+'-bare']['prior_exact_output_matches']=sum(r.get('output')==old[r['id']].get('output') for r in bare)
 with (HERE/'test-output/scores.json').open('x') as f:json.dump(report,f,indent=2)
 print(json.dumps({k:{x:v[x] for x in ('all','exact_questions','seconds','errors')} for k,v in report.items()},indent=2))
if __name__=='__main__':
 {'run':run,'score':score}[sys.argv[1]]()

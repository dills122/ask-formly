"""Frozen extractor baseline and separate public native attribute feasibility calls."""
import sys,os,json,time,gc
from pathlib import Path
HERE=Path(__file__).resolve().parent;NARROW=HERE.parent;OUT=HERE/'test-output';PRIOR=NARROW/'role_boundary_adaptation';PREV=NARROW/'cross_role_resolution'
sys.path.insert(0,str(NARROW/'supervised_trial'))
from train import load_model,weights,write,sha
sys.path.insert(0,str(NARROW/'pilot'))
from peft import PeftModel
from gliner2 import AttributeGroup
import torch
from policy import ROLES,native_choices,resolve
os.environ['HF_HOME']=str(OUT/'.cache')
def read(p):return json.loads(p.read_text())
def splits():return {'fresh':read(HERE/'fresh.json'),'cross':read(PREV/'fresh.json'),'boundary':read(PRIOR/'fresh.json'),'vocab':read(NARROW/'vocabulary_adaptation/fresh.json'),'target':read(NARROW/'fresh_flat/questions.json'),'challenge':read(NARROW/'challenge_adaptation/challenge.json'),'olddev':read(NARROW/'supervised_trial/dev.json')}
def extract(model,text,schema):
 start=time.perf_counter()
 try:r={'output':model.extract(text,schema,threshold=.5,overlap_policy='flat',include_spans=True,include_confidence=True)}
 except Exception as e:r={'error':type(e).__name__+': '+str(e)}
 return dict(**r,seconds=time.perf_counter()-start)
def main(smoke=False):
 labels=read(NARROW/'pilot/labels.json');torch.set_num_threads(4);torch.use_deterministic_algorithms(True)
 data={'smoke':read(PRIOR/'test-output/train.json')[-3:]} if smoke else splits()
 if not smoke:
  if sum(map(len,data.values()))!=256:raise ValueError('counts')
  train=read(PRIOR/'test-output/train.json')
  if {r['question'] for r in train}&{r['question'] for r in data['fresh']}:raise ValueError('fresh overlap')
  freeze=read(PREV/'test-output/run-freeze.json');freeze.update({str(PREV/p):h for p,h in read(PREV/'test-output/final-freeze.json').items()})
  freeze.update({str(p):sha(p) for p in HERE.iterdir() if p.is_file() and p.name!='REVIEW.md'})
  freeze.update({str(p):sha(p) for p in (OUT/'spacy-model').rglob('*') if p.is_file()});write(OUT/'run-freeze.json',freeze)
  for p,h in freeze.items():
   if sha(Path(p))!=h:raise ValueError('frozen '+p)
 for n in (1701,1702):
  model=PeftModel.from_pretrained(load_model(),str(PRIOR/f'test-output/after-{n}/epoch-6/adapter'),is_trainable=False);model.eval();expected=read(PRIOR/f'test-output/after-{n}/training-receipt.json')['final_hashes']
  before=weights(model)
  if before!=expected:raise ValueError('checkpoint')
  folder=OUT/(f'smoke-{n}' if smoke else str(n));folder.mkdir();write(folder/'parameters-before.json',before)
  baseline=model.create_schema().entities(labels);native=model.create_schema().entities(labels).entity_attributes({'target_role':AttributeGroup(list(ROLES),multi_label=False,qualify_labels=True)})
  with torch.inference_mode():
   for split,rows in data.items():
    b=[];a=[];inputs=[]
    for row in rows:
     question=row['question'];id=row['question_id'];br=dict(id=id,**extract(model,question,baseline));ar=dict(id=id,**extract(model,question,native));b.append(br);a.append(ar)
     offsets={(s['start'],s['end']) for items in br.get('output',{}).get('entities',{}).values() for s in items}
     offsets|={(m['start'],m['end']) for m in row['mentions']}
     inputs.append(dict(id=id,question=question,offsets=sorted(offsets)))
    for name,value in [('baseline',b),('native',a),('inputs',inputs)]:write(folder/f'{split}-{name}.json',value)
    if not smoke and split!='fresh':
     old=read(PREV/f'test-output/{n}/{"fresh" if split=="cross" else split}-baseline.json')
     if len(old)!=len(b) or any(x['id']!=y['id'] or x.get('output')!=y.get('output') or 'error' in y for x,y in zip(old,b)):raise ValueError('baseline drift '+split)
    print(n,split,len(rows),'native_errors',sum('error' in r for r in a),flush=True)
  after=weights(model);write(folder/'parameters-after.json',after)
  if before!=after:raise ValueError('weight mutation')
  del model;gc.collect()
 if not smoke:
  for p,h in read(OUT/'run-freeze.json').items():
   if sha(Path(p))!=h:raise ValueError('frozen '+p)
if __name__=='__main__':main(sys.argv[1]=='smoke')

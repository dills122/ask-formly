"""Frozen-extractor replay and separate native attribute adapter training."""
import json,sys,time,gc,random,hashlib,math
import numpy as np
from native import *
from transport import malformed
from resolution import resolve_scores
OUT=HERE/'test-output';PRIOR=NARROW/'role_boundary_adaptation';PREV=NARROW/'span_role_feasibility'
def read(p):return json.loads(p.read_text())
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def splits():return {'fresh':read(HERE/'fresh.json'),'span':read(PREV/'fresh.json'),'cross':read(NARROW/'cross_role_resolution/fresh.json'),'boundary':read(PRIOR/'fresh.json'),'vocab':read(NARROW/'vocabulary_adaptation/fresh.json'),'target':read(NARROW/'fresh_flat/questions.json'),'challenge':read(NARROW/'challenge_adaptation/challenge.json'),'olddev':read(NARROW/'supervised_trial/dev.json')}
def load(number,trainable=False):
 model=PeftModel.from_pretrained(load_model(),str(PRIOR/f'test-output/after-{number}/epoch-6/adapter'),is_trainable=trainable)
 if weights(model)!=read(PRIOR/f'test-output/after-{number}/training-receipt.json')['final_hashes']:raise ValueError('baseline hashes')
 return model

def baseline():
 rows=read(PRIOR/'test-output/train.json');data=splits()
 if len(rows)!=194 or sum(map(len,data.values()))!=296:raise ValueError('counts')
 if {r['question'] for r in rows}&{r['question'] for r in data['fresh']}:raise ValueError('train leakage')
 freeze=read(PREV/'test-output/run-freeze.json');freeze.update({str(PREV/p):h for p,h in read(PREV/'test-output/final-freeze.json').items()})
 freeze.update({str(p):digest(p) for p in HERE.iterdir() if p.is_file() and p.name not in ('REVIEW.md','RESULTS.md')})
 write(OUT/'run-freeze.json',freeze);verify()
 for n in (1701,1702):
  model=load(n);model.eval();folder=OUT/str(n);folder.mkdir()
  with torch.inference_mode():
   for split,qs in data.items():
    outputs=[]
    for r in qs:
     t=time.perf_counter();output=model.extract(r['question'],model.create_schema().entities(LABELS),threshold=.5,overlap_policy='flat',include_spans=True,include_confidence=True)
     outputs.append(dict(id=r['question_id'],output=output,seconds=time.perf_counter()-t))
    write(folder/f'{split}-baseline.json',outputs)
    if split!='fresh':
     old=read(PREV/f'test-output/{n}/{"fresh" if split=="span" else split}-baseline.json')
     if any(a['id']!=b['id'] or a['output']!=b['output'] for a,b in zip(old,outputs)) or len(old)!=len(outputs):raise ValueError('drift '+split)
    print('baseline',n,split,len(qs),flush=True)
   score_model(model,n,'before',data)
  del model;gc.collect()
 verify()
def verify():
 for p,h in read(OUT/'run-freeze.json').items():
  if digest(Path(p))!=h:raise ValueError('frozen '+p)

def score_model(model,number,phase,data):
 folder=OUT/str(number);model.eval()
 with torch.inference_mode():
  for split,qs in data.items():
   records=[]
   for r,b in zip(qs,read(folder/f'{split}-baseline.json')):
    if r['question_id']!=b['id']:raise ValueError('identity')
    # No gold offsets enter resolver: only frozen baseline spans.
    offsets=sorted({(s['start'],s['end']) for xs in b['output']['entities'].values() for s in xs})
    t=time.perf_counter();scores=supplied(model,r['question'],offsets);resolved,log=resolve_scores(r['question'],b,scores)
    records.append(dict(id=b['id'],scores=scores,resolved=resolved,resolution=log,seconds=time.perf_counter()-t))
   write(folder/f'{split}-{phase}.json',records)
  # Strictly separate supplied-span audit. Never feeds resolver.
  probes=read(HERE/'probe_candidates.json')['candidates'];questions={r['question_id']:r['question'] for r in data['fresh']};audit=[]
  for qid in questions:
   selected=[p for p in probes if p['question_id']==qid];scored=supplied(model,questions[qid],sorted({(p['start'],p['end']) for p in selected}));lookup={(p['start'],p['end']):p for p in scored}
   for p in selected:audit.append(dict(**p,prediction=lookup[p['start'],p['end']]))
  write(folder/f'probes-{phase}.json',audit)

def save(model,path,panel):
 path.mkdir();rng=(random.getstate(),np.random.get_state(),torch.get_rng_state());model.eval()
 def pred(m):
  with torch.inference_mode():return [supplied(m,r['question'],[(s['start'],s['end']) for s in r['mentions']]+[(s['start'],s['end']) for s in malformed(r)]) for r in panel]
 before=pred(model);params=weights(model);model.save_pretrained(str(path/'adapter'));fresh=PeftModel.from_pretrained(load_model(),str(path/'adapter'),is_trainable=False);fresh.eval();after=pred(fresh)
 write(path/'before.json',before);write(path/'after.json',after);receipt=dict(predictions_identical=before==after,parameters_identical=params==weights(fresh));write(path/'receipt.json',receipt)
 if not all(receipt.values()):raise ValueError('reload parity')
 del fresh;gc.collect();random.setstate(rng[0]);np.random.set_state(rng[1]);torch.set_rng_state(rng[2])
def train():
 verify();rows=read(PRIOR/'test-output/train.json')
 for n in (1701,1702):
  model=load(n,True);seed(n);initial=weights(model);trainable={k for k,p in model.named_parameters() if p.requires_grad}
  if any('lora_' not in k for k in trainable):raise ValueError('nonLoRA')
  folder=OUT/str(n);write(folder/'parameters-before.json',initial);batches=[prepare(model,r,malformed(r)) for r in rows];opt=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=1e-4,weight_decay=.01);step=0;t=time.perf_counter()
  with (folder/'losses.jsonl').open('x') as log:
   for epoch in range(1,7):
    order=list(range(len(rows)));random.Random(n+epoch).shuffle(order);total=0.;model.train()
    for offset in range(0,len(order),8):
     chunk=order[offset:offset+8];opt.zero_grad(set_to_none=True)
     for i in chunk:
      loss=model(batches[i],gold_injection_prob=1.).total_loss
      if not torch.isfinite(loss):raise ValueError('nonfinite loss')
      (loss/len(chunk)).backward();total+=float(loss.detach());log.write(json.dumps(dict(epoch=epoch,step=step,id=rows[i]['question_id'],loss=float(loss.detach())))+'\n')
     norm=torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad],1.)
     if not torch.isfinite(norm):raise ValueError('gradient')
     opt.step();step+=1
    log.flush();print(n,'epoch',epoch,'loss',total/len(rows),'updates',step,flush=True)
    if epoch in (1,6):save(model,folder/f'epoch-{epoch}',rows[-8:])
  final=weights(model);frozen=[k for k in initial if k not in trainable and initial[k]!=final[k]];changed=[k for k in trainable if initial[k]!=final[k]]
  write(folder/'training-receipt.json',dict(updates=step,epochs=6,seconds=time.perf_counter()-t,frozen_changed=frozen,trained_changed=changed,final_hashes=final))
  if frozen or not changed or step!=150:raise ValueError('training invariant')
  del batches,opt;score_model(model,n,'after',splits());del model;gc.collect()
 verify()
if __name__=='__main__':
 torch.set_num_threads(4);torch.use_deterministic_algorithms(True)
 {'baseline':baseline,'train':train}[sys.argv[1]]()

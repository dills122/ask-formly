"""Frozen-extractor replay and separate native attribute adapter training."""
import json,sys,time,gc,random,hashlib,math
import numpy as np
from policy import schedule,anchor_schedule,LAMBDA
from cache import anchor_backward,identity as cache_identity
from cache_contract import validate as validate_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent;NARROW=HERE.parent;PREV=NARROW/'native_attribute_training'
sys.path.insert(0,str(PREV))
from native import *
HERE=Path(__file__).resolve().parent
from transport import malformed
from resolution import resolve_scores
CONTRAST=NARROW/'native_attribute_contrast';RETENTION=NARROW/'native_attribute_retention';DISTILL=NARROW/'native_attribute_distillation'
sys.path.insert(0,str(HERE))
OUT=HERE/'test-output';PRIOR=NARROW/'role_boundary_adaptation';PREV=NARROW/'native_attribute_training'
def read(p):return json.loads(p.read_text())
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def splits():return {'fresh':read(HERE/'fresh.json'),'retention':read(RETENTION/'fresh.json'),'contrast':read(CONTRAST/'fresh.json'),'attribute':read(PREV/'fresh.json'),'span':read(NARROW/'span_role_feasibility/fresh.json'),'cross':read(NARROW/'cross_role_resolution/fresh.json'),'boundary':read(PRIOR/'fresh.json'),'vocab':read(NARROW/'vocabulary_adaptation/fresh.json'),'target':read(NARROW/'fresh_flat/questions.json'),'challenge':read(NARROW/'challenge_adaptation/challenge.json'),'olddev':read(NARROW/'supervised_trial/dev.json')}
def load_original(number):
 model=PeftModel.from_pretrained(load_model(),str(PRIOR/f'test-output/after-{number}/epoch-6/adapter'),is_trainable=False)
 if weights(model)!=read(PRIOR/f'test-output/after-{number}/training-receipt.json')['final_hashes']:raise ValueError('baseline hashes')
 return model

def load_candidate(number,trainable=False):
 model=PeftModel.from_pretrained(load_model(),str(PREV/f'test-output/{number}/epoch-6/adapter'),is_trainable=trainable)
 if weights(model)!=read(PREV/f'test-output/{number}/training-receipt.json')['final_hashes']:raise ValueError('candidate hashes')
 return model

def baseline():
 verify('training-freeze.json')
 rows=read(OUT/'train.json');data=splits()
 if len(rows)!=242 or sum(map(len,data.values()))!=416:raise ValueError('counts')
 if {r['question'] for r in rows}&{r['question'] for r in data['fresh']}:raise ValueError('train leakage')
 freeze=read(RETENTION/'test-output/run-freeze.json');freeze.update({str(RETENTION/p):h for p,h in read(RETENTION/'test-output/final-freeze.json').items()});freeze.update({str(DISTILL/p):h for p,h in read(DISTILL/'test-output/final-freeze.json').items()})
 freeze.update({str(p):digest(p) for p in OUT.glob('*.json') if p.name!='run-freeze.json'})
 freeze.update({str(p):digest(p) for p in HERE.iterdir() if p.is_file() and p.name not in ('REVIEW.md','RESULTS.md')})
 write(OUT/'run-freeze.json',freeze);verify()
 for n in (1701,1702):
  model=load_original(n);model.eval();folder=OUT/str(n);folder.mkdir()
  with torch.inference_mode():
   for split,qs in data.items():
    outputs=[]
    for r in qs:
     t=time.perf_counter();output=model.extract(r['question'],model.create_schema().entities(LABELS),threshold=.5,overlap_policy='flat',include_spans=True,include_confidence=True)
     outputs.append(dict(id=r['question_id'],output=output,seconds=time.perf_counter()-t))
    write(folder/f'{split}-baseline.json',outputs)
    if split!='fresh':
     old=read(RETENTION/f'test-output/{n}/{"fresh" if split=="retention" else split}-baseline.json')
     if any(a['id']!=b['id'] or a['output']!=b['output'] for a,b in zip(old,outputs)) or len(old)!=len(outputs):raise ValueError('drift '+split)
    print('baseline',n,split,len(qs),flush=True)
  del model;gc.collect();model=load_candidate(n);score_model(model,n,'before',data);del model;gc.collect()
 verify()
def verify(manifest='run-freeze.json'):
 for p,h in read(OUT/manifest).items():
  if digest(Path(p))!=h:raise ValueError('frozen '+p)

def score_model(model,number,phase,data):
 folder=OUT/str(number);model.eval()
 with torch.inference_mode():
  for split,qs in data.items():
   records=[];raw_baseline=read(folder/f'{split}-baseline.json')
   if len(qs)!=len(raw_baseline):raise ValueError('baseline count')
   for r,b in zip(qs,raw_baseline):
    if r['question_id']!=b['id']:raise ValueError('identity')
    # No gold offsets enter resolver: only frozen baseline spans.
    offsets=sorted({(s['start'],s['end']) for xs in b['output']['entities'].values() for s in xs})
    t=time.perf_counter();scores=supplied(model,r['question'],offsets);resolved,log=resolve_scores(r['question'],b,scores)
    records.append(dict(id=b['id'],scores=scores,resolved=resolved,resolution=log,seconds=time.perf_counter()-t))
   write(folder/f'{split}-{phase}.json',records)
   if phase=='before' and split!='fresh':
    previous=read(RETENTION/f'test-output/{number}/{"fresh" if split=="retention" else split}-before.json')
    if len(previous)!=len(records) or any(a['id']!=b['id'] or a['scores']!=b['scores'] or a['resolved']['output']!=b['resolved']['output'] for a,b in zip(previous,records)):raise ValueError('prior candidate drift '+split)
  # Strictly separate supplied-span audit. Never feeds resolver.
  for probe_name,root,question_rows in [('probes',HERE,data['fresh']),('oldprobes',PREV,data['attribute']),('contrastprobes',CONTRAST,data['contrast']),('retentionprobes',RETENTION,data['retention'])]:
   probes=read(root/'probe_candidates.json')['candidates'];questions={r['question_id']:r['question'] for r in question_rows};audit=[]
   for qid in questions:
    selected=[p for p in probes if p['question_id']==qid];scored=supplied(model,questions[qid],sorted({(p['start'],p['end']) for p in selected}));lookup={(p['start'],p['end']):p for p in scored}
    for p in selected:audit.append(dict(**p,prediction=lookup[p['start'],p['end']]))
   write(folder/f'{probe_name}-{phase}.json',audit)
   if phase=='before' and probe_name in ('oldprobes','contrastprobes','retentionprobes'):
    expected=read(RETENTION/f'test-output/{number}/{"probes" if probe_name=="retentionprobes" else probe_name}-before.json')
    if audit!=expected:raise ValueError('prior probes drift')

def save(model,path,panel,panel_bad):
 path.mkdir();rng=(random.getstate(),np.random.get_state(),torch.get_rng_state());model.eval()
 def pred(m):
  with torch.inference_mode():return [supplied(m,r['question'],[(s['start'],s['end']) for s in r['mentions']]+[(s['start'],s['end']) for s in b['negatives']]) for r,b in zip(panel,panel_bad)]
 before=pred(model);params=weights(model);model.save_pretrained(str(path/'adapter'));fresh=PeftModel.from_pretrained(load_model(),str(path/'adapter'),is_trainable=False);fresh.eval();after=pred(fresh)
 write(path/'before.json',before);write(path/'after.json',after);receipt=dict(predictions_identical=before==after,parameters_identical=params==weights(fresh));write(path/'receipt.json',receipt)
 if not all(receipt.values()):raise ValueError('reload parity')
 del fresh;gc.collect();random.setstate(rng[0]);np.random.set_state(rng[1]);torch.set_rng_state(rng[2])
def train():
 verify();rows=read(OUT/'train.json');bad=read(OUT/'training-negatives.json');plans=read(OUT/'schedules.json')
 if len(rows)!=242 or len(bad)!=242 or any(r['question_id']!=b['question_id'] for r,b in zip(rows,bad)):raise ValueError('training identity')
 for n in (1701,1702):
  for arm in ('control','treatment'):
   model=load_candidate(n,True);teacher_cache=read(OUT/f'teacher-{n}.json');validate_cache(teacher_cache,cache_identity(model),rows[:194],bad[:194]);cache_before=digest(OUT/f'teacher-{n}.json')
   seed(n);initial=weights(model);trainable={k for k,p in model.named_parameters() if p.requires_grad}
   if any('lora_' not in k for k in trainable):raise ValueError('nonLoRA')
   folder=OUT/str(n)/arm;folder.mkdir();write(folder/'parameters-before.json',initial)
   plan=plans[str(n)]['supervised'];anchors=plans[str(n)]['anchors']
   if plan!=schedule(n) or anchors!=anchor_schedule(n):raise ValueError('schedule drift')
   batches=[prepare(model,r,b['negatives']) for r,b in zip(rows,bad)]
   opt=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=1e-4,weight_decay=.01);t=time.perf_counter();seen=0
   with (folder/'losses.jsonl').open('x') as log:
    for step,(chunk,anchor_indices) in enumerate(zip(plan,anchors),1):
     model.train();opt.zero_grad(set_to_none=True);raw_supervised=0.
     for i in chunk:
      loss=model(batches[i],gold_injection_prob=1.).total_loss
      if not torch.isfinite(loss):raise ValueError('nonfinite loss')
      (loss/8).backward();raw_supervised+=float(loss.detach())/8;seen+=1
     raw_kl,anchor_counts=anchor_backward(model,teacher_cache,anchor_indices,LAMBDA[arm])
     if not math.isfinite(raw_kl):raise ValueError('KL nonfinite')
     norm=torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad],1.)
     if not torch.isfinite(norm):raise ValueError('gradient')
     opt.step()
     log.write(json.dumps(dict(step=step,supervised_ids=[rows[i]['question_id'] for i in chunk],anchor_ids=[rows[i]['question_id'] for i in anchor_indices],anchor_counts=anchor_counts,raw_supervised=raw_supervised,raw_kl=raw_kl,lambda_=LAMBDA[arm],objective=raw_supervised+LAMBDA[arm]*raw_kl,gradient_norm_before_clip=float(norm)))+'\n')
     if step%31==0:log.flush();print(n,arm,'updates',step,'examples',seen,flush=True)
     if step in (31,124):save(model,folder/f'step-{step}',rows[186:194],bad[186:194])
   final=weights(model);frozen=[k for k in initial if k not in trainable and initial[k]!=final[k]];changed=[k for k in trainable if initial[k]!=final[k]]
   write(folder/'training-receipt.json',dict(updates=step,examples=seen,anchor_row_exposures=sum(map(len,anchors)),seconds=time.perf_counter()-t,frozen_changed=frozen,trained_changed=changed,final_hashes=final,teacher_cache_unchanged=cache_before==digest(OUT/f'teacher-{n}.json'),teacher_cache_sha256=cache_before,teacher_model_not_loaded_in_training=True))
   if frozen or not changed or step!=124 or seen!=992 or cache_before!=digest(OUT/f'teacher-{n}.json'):raise ValueError('training invariant')
   del batches,opt;score_model(model,n,arm,splits());del model;gc.collect()
 verify()
if __name__=='__main__':
 torch.set_num_threads(4);torch.use_deterministic_algorithms(True)
 {'baseline':baseline,'train':train}[sys.argv[1]]()

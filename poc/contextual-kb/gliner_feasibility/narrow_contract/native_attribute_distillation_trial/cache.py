"""Training-only frozen teachers and validated detached exact-span caches."""
import sys,json,hashlib,inspect,gc,importlib.metadata
from pathlib import Path
from collections import Counter
HERE=Path(__file__).resolve().parent;NARROW=HERE.parent;DISTILL=NARROW/'native_attribute_distillation';PRIOR=NARROW/'native_attribute_training';OUT=HERE/'test-output'
sys.path.insert(0,str(DISTILL))
from native_logits import logits
from loss import preservation_kl
from native import load_model,PeftModel,weights,prepare,schema,torch,write
sys.path.insert(0,str(HERE))
from cache_contract import ROLES,targets,validate
from policy import schedule,anchor_schedule,anchor_weights

def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def state_hash(model):return {k:hashlib.sha256(v.detach().cpu().contiguous().numpy().tobytes()).hexdigest() for k,v in model.state_dict().items()}
def load(n,trainable=False):
 model=PeftModel.from_pretrained(load_model(),str(PRIOR/f'test-output/{n}/epoch-6/adapter'),is_trainable=trainable);model.eval()
 if weights(model)!=read(PRIOR/f'test-output/{n}/training-receipt.json')['final_hashes']:raise ValueError('start drift')
 return model

def identity(model):
 base=model.get_base_model();paths=[Path(inspect.getfile(type(x))) for x in (base,base.boundary_head,model.processor,model.processor.word_splitter)]+[DISTILL/'native_logits.py',DISTILL/'loss.py',HERE/'cache_contract.py',HERE/'policy.py',OUT/'train.json',OUT/'training-negatives.json',NARROW/'pilot/labels.json']
 return dict(teacher_parameters=weights(model),teacher_state=state_hash(model),source_hashes={str(p):digest(p) for p in paths},source_rows=194,source_negatives=449,tokenizer_sha256=hashlib.sha256(model.processor.tokenizer.backend_tokenizer.to_str().encode()).hexdigest(),special_tokens=model.processor.tokenizer.special_tokens_map,schema=base._build_schema_dicts_and_metadata([schema(model)])[0],roles=list(ROLES),pair_temperature=base.boundary_settings.pair_temperature,distillation_temperature=1,versions={x:importlib.metadata.version(x) for x in ('gliner2','torch','peft')})

def cached_rows(model,rows,bad):
 records=[];counts={r:Counter() for r in ROLES}
 for r,b in zip(rows,bad):
  alltargets=targets(r,b);offsets=[(x['start'],x['end']) for x in alltargets]
  if offsets:
   z,aligned,unsupported,query_ids=logits(model,r['question'],offsets);lookup={(m['start'],m['end']):m for m in alltargets};gold=[lookup[x] for x in aligned];excluded=[lookup[x] for x in unsupported];prob=z.softmax(-1).tolist()
  else:gold=[];excluded=[];prob=[];query_ids=[]
  mask=[]
  for g,p in zip(gold,prob):
   winner=max(range(7),key=lambda i:p[i]);correct=ROLES[winner]==g['role'] and p[winner]>.5;mask.append(correct)
   counts[g['role']]['total']+=1;counts[g['role']]['retained_correct' if correct else 'masked']+=1;counts[g['role']]['wrong_argmax']+=ROLES[winner]!=g['role'];counts[g['role']]['correct_low_confidence']+=ROLES[winner]==g['role'] and p[winner]<=.5
  for g in excluded:counts[g['role']]['unsupported']+=1
  records.append(dict(question_id=r['question_id'],question=r['question'],targets=gold,unsupported=excluded,query_ids=query_ids,probabilities=prob,mask=mask))
 return records,counts

def anchor_backward(model,cache,indices,coefficient):
 records=[cache['records'][i] for i in indices];counts=[sum(r['mask']) for r in records];weights_=anchor_weights(counts);raw=0.
 model.eval()
 for r,w in zip(records,weights_):
  if not w:continue
  z,aligned,unsupported,queries=logits(model,r['question'],[(m['start'],m['end']) for m in r['targets']])
  if unsupported or aligned!=[(m['start'],m['end']) for m in r['targets']] or queries!=r['query_ids']:raise ValueError('anchor identity')
  loss=preservation_kl(z,torch.tensor(r['probabilities']),torch.tensor(r['mask']))*w;raw+=float(loss.detach());(loss*coefficient).backward()
 return raw,counts

def main():
 torch.set_num_threads(4);torch.use_deterministic_algorithms(True);rows=read(OUT/'train.json');bad=read(OUT/'training-negatives.json')
 assert len(rows)==242 and len(bad)==242 and bad[:194]==read(PRIOR/'test-output/training-negatives.json') and sum(len(b['negatives']) for b in bad[:194])==449
 for n in (1701,1702):
  teacher=load(n)
  for p in teacher.parameters():p.requires_grad_(False)
  before=state_hash(teacher);ident=identity(teacher)
  with torch.no_grad():records,counts=cached_rows(teacher,rows[:194],bad[:194])
  cache=dict(identity=ident,records=records);validate(cache,ident,rows[:194],bad[:194]);write(OUT/f'teacher-{n}.json',cache)
  assert before==state_hash(teacher) and not teacher.training and all(not p.requires_grad and p.grad is None for p in teacher.parameters())
  audit=dict(seed=n,counts=counts,zero_anchor_rows=[r['question_id'] for r in records if not any(r['mask'])],masked=[dict(question_id=r['question_id'],target=t,probabilities=p) for r in records for t,p,m in zip(r['targets'],r['probabilities'],r['mask']) if not m],teacher_unchanged=True,cache_sha256=digest(OUT/f'teacher-{n}.json'))
  write(OUT/f'teacher-{n}-audit.json',audit);print(n,dict(counts),flush=True);del teacher;gc.collect()
  # Fixed no-update scale diagnostic: first two predeclared supervised/anchor batches.
  model=load(n,True);params=[p for p in model.parameters() if p.requires_grad];gen=torch.Generator().manual_seed(n)
  with torch.no_grad():
   for p in params:p.add_(torch.randn(p.shape,generator=gen)*1e-3)
  calibration=[]
  for step in (0,1):
   model.eval();model.zero_grad(set_to_none=True);sup=0.
   for i in schedule(n)[step]:
    loss=model(prepare(model,rows[i],bad[i]['negatives']),gold_injection_prob=1.).total_loss/8;sup+=float(loss.detach());loss.backward()
   gs=torch.cat([(p.grad if p.grad is not None else torch.zeros_like(p)).flatten() for p in params]).detach().clone();model.zero_grad(set_to_none=True)
   kl,available=anchor_backward(model,cache,anchor_schedule(n)[step],1.)
   gk=torch.cat([(p.grad if p.grad is not None else torch.zeros_like(p)).flatten() for p in params]).detach();assert torch.isfinite(gs).all() and torch.isfinite(gk).all()
   calibration.append(dict(batch_index=step,supervised_indices=schedule(n)[step],anchor_indices=anchor_schedule(n)[step],available_anchors=available,raw_supervised=sup,raw_kl=kl,supervised_gradient_norm=float(gs.norm()),raw_kl_gradient_norm=float(gk.norm()),fixed_lambda100_gradient_ratio=float(100*gk.norm()/gs.norm()),optimizer_updates=0))
  write(OUT/f'calibration-{n}.json',calibration);del model,params;gc.collect()
if __name__=='__main__':main()

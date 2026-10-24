"""Two-seed training-only compatibility; at most three disposable SGD steps."""
import json,sys,gc,hashlib,inspect,time,importlib.metadata
from pathlib import Path
from collections import Counter
from unittest.mock import patch
from native_logits import logits,PRIOR,ROLES,torch,schema
from native import load_model,PeftModel,weights,prepare,supplied,write
from loss import preservation_kl,correct_mask
HERE=Path(__file__).resolve().parent;OUT=HERE/'test-output'
def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def state_hash(model):
 return {k:hashlib.sha256(v.detach().cpu().contiguous().numpy().tobytes()).hexdigest() for k,v in model.state_dict().items()}
def load(n,trainable):
 m=PeftModel.from_pretrained(load_model(),str(PRIOR/f'test-output/{n}/epoch-6/adapter'),is_trainable=trainable)
 assert weights(m)==read(PRIOR/f'test-output/{n}/training-receipt.json')['final_hashes'];m.eval();return m

def targets(item):
 r=item['row'];items=[dict(start=m['start'],end=m['end'],role=m['kind']) for m in r['mentions']]+[dict(start=m['start'],end=m['end'],role='no_entity') for m in item['negative']['negatives']]
 return sorted(items,key=lambda x:(x['start'],x['end']))

def identity(model):
 base=model.get_base_model();sources={str(Path(inspect.getfile(type(x)))):digest(Path(inspect.getfile(type(x)))) for x in (base,base.boundary_head,model.processor,model.processor.word_splitter)}
 for p in (HERE/'native_logits.py',HERE/'loss.py',HERE/'prepare_panel.py',HERE.parent/'native_attribute_contrast/test-output/train.json',HERE.parent/'native_attribute_contrast/test-output/training-negatives.json',PRIOR/'native.py',PRIOR/'transport.py',HERE.parent/'pilot/labels.json',OUT/'panel.json'):sources[str(p)]=digest(p)
 schemas,_=base._build_schema_dicts_and_metadata([schema(model)])
 sources[str(Path(inspect.getfile(base._attach_entity_attributes)))]=digest(Path(inspect.getfile(base._attach_entity_attributes)))
 return dict(library_versions={x:importlib.metadata.version(x) for x in ('gliner2','torch','peft')},teacher_parameters=weights(model),teacher_state=state_hash(model),sources=sources,tokenizer_sha256=hashlib.sha256(model.processor.tokenizer.backend_tokenizer.to_str().encode()).hexdigest(),special_tokens=model.processor.tokenizer.special_tokens_map,schema=schemas,roles=list(ROLES),pair_temperature=base.boundary_settings.pair_temperature,distillation_temperature=1)

def cache_teacher(teacher,panel):
 records=[];counts={r:Counter() for r in ROLES};maxdiff=0.;unsupported_count=0
 for item in panel:
  r=item['row'];gold=targets(item);offsets=[(m['start'],m['end']) for m in gold]
  with torch.no_grad():
   scores,aligned,unsupported,queries=logits(teacher,r['question'],offsets)
   assert aligned==offsets and not unsupported
   base=teacher.get_base_model();_,metadata=base._build_schema_dicts_and_metadata([schema(teacher)])
   assert list(metadata[0]['entity_attribute_groups']['target_role'].labels)==list(ROLES)
   captured=[];native_score=base.boundary_head.score_explicit_spans
   def capture(*args,**kwargs):
    value=native_score(*args,**kwargs);captured.append(value.detach().clone());return value
   with patch.object(base.boundary_head,'score_explicit_spans',side_effect=capture):native=supplied(teacher,r['question'],offsets)
   assert len(captured)==1
   expected=captured[0][0].transpose(0,1)/base.boundary_settings.pair_temperature
   diff=float((expected-scores).abs().max());maxdiff=max(maxdiff,diff);assert torch.allclose(expected,scores,atol=1e-5,rtol=1e-5)
   probs=scores.softmax(-1);goldidx=torch.tensor([ROLES.index(g['role']) for g in gold]);mask=correct_mask(probs,goldidx)
   for i,(g,native_row) in enumerate(zip(gold,native)):
    assert (native_row['start'],native_row['end'])==offsets[i]
    assert native_row['label']==ROLES[int(probs[i].argmax())] and abs(native_row['confidence']-float(probs[i].max()))<1e-5
    counts[g['role']]['total']+=1;counts[g['role']]['retained_correct' if mask[i] else 'masked_teacher_error_or_low_confidence']+=1
    counts[g['role']]['teacher_argmax_wrong']+=int(probs[i].argmax())!=goldidx[i].item();counts[g['role']]['teacher_correct_low_confidence']+=int(probs[i].argmax())==goldidx[i].item() and float(probs[i].max())<=.5
   # Token-only probe, not a label/anchor: split inside a native word.
   tok=next((x for x in teacher.processor.word_splitter(r['question'],lower=False) if x[2]-x[1]>=3),None)
   if tok:
    bad=(tok[1]+1,tok[2]);_,_,excluded,_=logits(teacher,r['question'],offsets+[bad] if bad not in offsets else offsets)
    if bad not in offsets:assert bad in excluded;unsupported_count+=1
  records.append(dict(question_id=r['question_id'],question=r['question'],targets=gold,query_ids=queries,logits=scores.tolist(),probabilities=probs.tolist(),mask=mask.tolist()))
 return records,dict(role_counts=counts,max_native_logit_difference=maxdiff,unsupported_transport_excluded=unsupported_count)

def kl_value(student,cache,backward=False):
 total=sum(sum(r['mask']) for r in cache);assert total>0;value=0.
 for r in cache:
  mask=torch.tensor(r['mask']);count=int(mask.sum())
  if not count:continue
  z,aligned,unsupported,query_ids=logits(student,r['question'],[(x['start'],x['end']) for x in r['targets']])
  assert aligned==[(x['start'],x['end']) for x in r['targets']] and not unsupported and query_ids==r['query_ids']
  loss=preservation_kl(z,torch.tensor(r['probabilities']),mask)*count/total
  value+=float(loss.detach())
  if backward:loss.backward()
 return value

def grad_vector(parameters):return torch.cat([(p.grad if p.grad is not None else torch.zeros_like(p)).detach().flatten() for p in parameters])
def save_check(student,path,cache):
 path.mkdir();before=state_hash(student)
 with torch.no_grad():pred=[logits(student,r['question'],[(x['start'],x['end']) for x in r['targets']])[0].tolist() for r in cache]
 student.save_pretrained(str(path/'adapter'));reload=PeftModel.from_pretrained(load_model(),str(path/'adapter'),is_trainable=False);reload.eval()
 with torch.no_grad():after=[logits(reload,r['question'],[(x['start'],x['end']) for x in r['targets']])[0].tolist() for r in cache]
 receipt=dict(predictions_identical=pred==after,state_identical=before==state_hash(reload));write(path/'receipt.json',receipt);assert all(receipt.values());del reload;gc.collect()

def main():
 torch.set_num_threads(4);torch.use_deterministic_algorithms(True);selection=read(OUT/'panel.json');panel=selection['rows'];results=[]
 original=HERE.parent/'native_attribute_contrast/test-output';rows=read(original/'train.json')[:194];bad=read(original/'training-negatives.json')[:194]
 assert len(rows)==194 and sum(len(x['negatives']) for x in bad)==449 and bad==read(PRIOR/'test-output/training-negatives.json')
 assert all(item==dict(row=rows[i],negative=bad[i]) for item,i in zip(panel,selection['indices'])) and all(0<=i<194 for i in selection['indices'])
 for n in (1701,1702):
  folder=OUT/str(n);folder.mkdir();teacher=load(n,False)
  for p in teacher.parameters():p.requires_grad_(False)
  teacher.eval();before=state_hash(teacher);ident=identity(teacher);cache,receipt=cache_teacher(teacher,panel);write(folder/'teacher-cache.json',dict(identity=ident,records=cache,receipt=receipt));cachehash=digest(folder/'teacher-cache.json')
  student=load(n,True);student.eval();params=[p for p in student.parameters() if p.requires_grad]
  assert all('lora_' in k for k,p in student.named_parameters() if p.requires_grad)
  with torch.no_grad():initial=kl_value(student,cache)
  assert abs(initial)<1e-6
  generator=torch.Generator().manual_seed(n)
  with torch.no_grad():
   for p in params:p.add_(torch.randn(p.shape,generator=generator)*1e-3)
  with torch.no_grad():perturbed=kl_value(student,cache)
  assert perturbed>initial+1e-7
  batch=prepare(student,panel[0]['row'],panel[0]['negative']['negatives'])
  student.zero_grad(set_to_none=True);supervised0=student(batch,gold_injection_prob=1.).total_loss;supervised0.backward();g0=grad_vector(params).clone()
  student.zero_grad(set_to_none=True);kl_value(student,cache,True);gkl=grad_vector(params).clone()
  student.zero_grad(set_to_none=True);supervised1=student(batch,gold_injection_prob=1.).total_loss;supervised1.backward();kl_value(student,cache,True);g1=grad_vector(params)
  assert float(supervised0)==float(supervised1) and torch.isfinite(gkl).all() and float(gkl.norm())>0
  assert torch.allclose(g1,g0+gkl,atol=1e-5,rtol=1e-4) and float((g1-g0).norm())>0
  gradient=dict(supervised_loss=float(supervised0.detach()),lambda0_norm=float(g0.norm()),lambda1_norm=float(g1.norm()),preservation_norm=float(gkl.norm()),difference_norm=float((g1-g0).norm()),max_additivity_error=float((g1-g0-gkl).abs().max()))
  del g0,g1,gkl;optimizer=torch.optim.SGD(params,lr=1e-4);teacherids={id(p) for p in teacher.parameters()};assert not teacherids&{id(p) for g in optimizer.param_groups for p in g['params']}
  trace=[perturbed]
  for step in range(1,4):
   optimizer.zero_grad(set_to_none=True);kl_value(student,cache,True)
   assert all(p.grad is None or torch.isfinite(p.grad).all() for p in params)
   optimizer.step()
   with torch.no_grad():trace.append(kl_value(student,cache))
   if step in (1,3):save_check(student,folder/f'step-{step}',cache)
  assert trace[-1]<trace[0]
  finalcache,finalreceipt=cache_teacher(teacher,panel)
  preserved=state_hash(teacher)==before and finalcache==cache and all(p.grad is None and not p.requires_grad for p in teacher.parameters()) and not teacher.training
  assert preserved and cachehash==digest(folder/'teacher-cache.json')
  result=dict(seed=n,initial_kl=initial,perturbed_kl=perturbed,gradient=gradient,diagnostic_steps=3,anchor_loss_trace=trace,teacher_preserved=preserved,cache_sha256=cachehash,cache_receipt=receipt,student_frozen_state_unchanged={k:v for k,v in before.items() if 'lora_' not in k}=={k:v for k,v in state_hash(student).items() if 'lora_' not in k})
  assert result['student_frozen_state_unchanged'];write(folder/'receipt.json',result);results.append(result);print(json.dumps(result),flush=True)
  del student,teacher,params,optimizer,batch,cache,finalcache;gc.collect()
 write(OUT/'compatibility.json',results)
if __name__=='__main__':main()

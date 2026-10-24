import json,hashlib
from native import *
from transport import malformed
OUT=HERE/'test-output';PRIOR=NARROW/'role_boundary_adaptation';rows=json.loads((PRIOR/'test-output/train.json').read_text())
model=PeftModel.from_pretrained(load_model(),str(PRIOR/'test-output/after-1701/epoch-6/adapter'),is_trainable=True);seed(1701);model.eval()
# Attribute queries ONLY: ordinary extraction cannot account for gradient.
row=next(r for r in rows if r['question_id']=='D01');sample=export(row,malformed(row));entities={k:v for k,v in sample['output']['entities'].items() if k.startswith('target_role: ')}
assert len(entities)==7 and entities['target_role: no_entity']
permuted={k:list(v) for k,v in entities.items()};permuted['target_role: no_entity'],permuted['target_role: registration_name']=permuted['target_role: registration_name'],permuted['target_role: no_entity']
results=[]
for target in (entities,permuted):
 batch=model.processor.collate_fn_train([(row['question'],{'entities':target})],architecture='boundary',error_policy='raise',dedupe_contained_entity_spans=False)
 assert {q.role_name for q in batch.query_layouts[0].queries}==set(entities)
 model.zero_grad();result=model(batch,gold_injection_prob=1.);result.total_loss.backward();grads={n:hashlib.sha256(p.grad.detach().cpu().numpy().tobytes()).hexdigest() for n,p in model.named_parameters() if p.grad is not None};norm=sum(float(p.grad.abs().sum()) for p in model.parameters() if p.grad is not None)
 results.append(dict(loss=float(result.total_loss.detach()),nonzero_gradient_l1=norm,gradient_hashes=grads,targets=target,terms={k:float(v.detach()) for k,v in result.losses.items() if torch.is_tensor(v) and v.numel()==1}))
assert results[0]['loss']!=results[1]['loss'] and results[0]['gradient_hashes']!=results[1]['gradient_hashes'] and min(r['nonzero_gradient_l1'] for r in results)>0
write(OUT/'qualified-gradient-smoke.json',dict(question=row['question'],ordinary_entity_queries=0,results=results));print([dict(loss=r['loss'],gradient_l1=r['nonzero_gradient_l1']) for r in results])

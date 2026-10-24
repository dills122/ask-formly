import json,sys,gc
from pathlib import Path
from native import *
from transport import malformed
OUT=HERE/'test-output'/'ordered-smoke';OUT.mkdir();PRIOR=NARROW/'role_boundary_adaptation'
rows=json.loads((PRIOR/'test-output/train.json').read_text())
model=PeftModel.from_pretrained(load_model(),str(PRIOR/'test-output/after-1701/epoch-6/adapter'),is_trainable=True)
model.eval();seed(1701)
# Entire train-only transport first; explicit negatives must not silently realign.
batches=[];bad=[]
for row in rows:
 negatives=malformed(row);batches.append(prepare(model,row,negatives));bad.append(negatives)
write(OUT/'training-negatives.json',[dict(question_id=r['question_id'],negatives=n) for r,n in zip(rows,bad)])
write(OUT/'transport.json',dict(rows=len(rows),negative_count=sum(map(len,bad)),all_exact=True))
indices=[i for i,n in enumerate(bad) if n][:2]
panel=[rows[i] for i in indices]
def predictions():
 model.eval()
 with torch.inference_mode():return [supplied(model,r['question'],[(m['start'],m['end']) for m in r['mentions']]+[(m['start'],m['end']) for m in bad[i]]) for i,r in zip(indices,panel)]
before=predictions();initial=weights(model);opt=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=1e-4)
losses=[];grads=[]
for i in indices:
 model.train();opt.zero_grad();o=model(batches[i],gold_injection_prob=1.);o.total_loss.backward();norm=torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad],1.);grads.append(float(norm));opt.step();losses.append(float(o.total_loss.detach()))
after=predictions();model.save_pretrained(str(OUT/'smoke-adapter'));changed=weights(model)
fresh=PeftModel.from_pretrained(load_model(),str(OUT/'smoke-adapter'),is_trainable=False);fresh.eval()
with torch.inference_mode():reloaded=[supplied(fresh,r['question'],[(m['start'],m['end']) for m in r['mentions']]+[(m['start'],m['end']) for m in bad[i]]) for i,r in zip(indices,panel)]
# Public vs exact supplied scoring equality at retained native entities.
with torch.inference_mode():
 public=fresh.extract(panel[0]['question'],schema(fresh),threshold=.5,overlap_policy='flat',include_spans=True,include_confidence=True)
 items=[v for vs in public['entities'].values() for v in vs];audit=supplied(fresh,panel[0]['question'],sorted({(v['start'],v['end']) for v in items}));lookup={(v['start'],v['end']):v for v in audit}
 parity=all(v['target_role']['label']==lookup[v['start'],v['end']]['label'] and abs(v['target_role']['confidence']-lookup[v['start'],v['end']]['confidence'])<1e-6 for v in items)
receipt=dict(indices=indices,losses=losses,gradient_norms=grads,attribute_predictions_changed=before!=after,save_predictions_exact=after==reloaded,save_weights_exact=changed==weights(fresh),public_parity=parity,public_mentions=len(items),before=before,after=after,changed_parameters=sum(initial[k]!=changed[k] for k in initial))
write(OUT/'smoke.json',receipt);print(json.dumps({k:v for k,v in receipt.items() if k not in ('before','after')}))
assert receipt['attribute_predictions_changed'] and receipt['save_predictions_exact'] and receipt['save_weights_exact'] and parity and items

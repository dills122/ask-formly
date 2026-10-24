"""Training-only exposure audit and actual arm-gradient/RNG equivalence smoke."""
from cache import *
from policy import schedule,anchor_schedule,anchor_weights

def main():
 report={};exposure={}
 for n in (1701,1702):
  rows=read(OUT/'train.json');bad=read(OUT/'training-negatives.json');cache=read(OUT/f'teacher-{n}.json');supervised=schedule(n);anchors=anchor_schedule(n)
  sc=Counter(i for batch in supervised for i in batch);ac=Counter(i for batch in anchors for i in batch);roles=Counter();coefficients=Counter();zero_steps=[]
  assert set(sc)==set(range(242)) and set(ac)==set(range(194))
  for step,indices in enumerate(anchors,1):
   records=[cache['records'][i] for i in indices];counts=[sum(r['mask']) for r in records];ws=anchor_weights(counts)
   if not any(counts):zero_steps.append(step)
   for r,count,w in zip(records,counts,ws):
    for t,m in zip(r['targets'],r['mask']):
     if m:roles[t['role']]+=1;coefficients[t['role']]+=w/count
  exposure[str(n)]=dict(supervised_examples=sum(sc.values()),anchor_rows=sum(ac.values()),supervised_counts={rows[i]['question_id']:v for i,v in sc.items()},anchor_counts={rows[i]['question_id']:v for i,v in ac.items()},role_anchor_exposures=roles,unscaled_role_loss_coefficients=coefficients,zero_anchor_steps=zero_steps)
  model=load(n,True);validate(cache,identity(model),rows[:194],bad[:194]);params=[p for p in model.parameters() if p.requires_grad];gen=torch.Generator().manual_seed(n)
  with torch.no_grad():
   for p in params:p.add_(torch.randn(p.shape,generator=gen)*1e-3)
  before=weights(model);rng=torch.get_rng_state().clone();g=[];values=[]
  for coefficient in (0.,1.,100.):
   model.zero_grad(set_to_none=True);value,counts=anchor_backward(model,cache,anchors[0],coefficient);values.append(value);g.append(torch.cat([(p.grad if p.grad is not None else torch.zeros_like(p)).flatten() for p in params]).detach().clone())
   assert torch.equal(rng,torch.get_rng_state())
  assert values[0]==values[1]==values[2] and float(g[0].abs().max())==0 and torch.allclose(g[2],100*g[1],atol=1e-5,rtol=1e-4) and float(g[1].norm())>0 and weights(model)==before
  report[str(n)]=dict(raw_kl_identical=values[0],control_gradient_norm=float(g[0].norm()),raw_gradient_norm=float(g[1].norm()),treatment_gradient_norm=float(g[2].norm()),rng_unchanged=True,parameters_unchanged=True,optimizer_updates=0)
  del model,params,g;gc.collect()
 write(OUT/'exposure.json',exposure);write(OUT/'gradient-preflight.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()

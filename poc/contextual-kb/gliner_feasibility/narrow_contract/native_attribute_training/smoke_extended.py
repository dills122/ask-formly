import json
from native import *
from transport import malformed
OUT=HERE/'test-output';PRIOR=NARROW/'role_boundary_adaptation'
rows=json.loads((PRIOR/'test-output/train.json').read_text());results=[]
for number in (1701,1702):
 model=PeftModel.from_pretrained(load_model(),str(PRIOR/f'test-output/after-{number}/epoch-6/adapter'),is_trainable=False);model.eval()
 for row in rows:prepare(model,row,malformed(row))
 panel=rows[:8]+[r for r in rows if r['question_id']=='D01']+[r for r in rows if any(m['kind']=='value' for m in r['mentions'])][:4];count=0;matches=[];coverage=set()
 with torch.inference_mode():
  for r in panel:
   public=model.extract(r['question'],schema(model),threshold=.5,overlap_policy='flat',include_spans=True,include_confidence=True)
   coverage.update(k for k,vs in public['entities'].items() if vs);items=[i for vs in public['entities'].values() for i in vs];offsets=sorted({(i['start'],i['end']) for i in items});audit=supplied(model,r['question'],offsets);lookup={(i['start'],i['end']):i for i in audit}
   assert all(i['target_role']['label']==lookup[i['start'],i['end']]['label'] and abs(i['target_role']['confidence']-lookup[i['start'],i['end']]['confidence'])<1e-6 for i in items)
   count+=len(items);matches.append(dict(question_id=r['question_id'],native=public,supplied=audit))
  repeated=next(r for r in rows if r['question_id']=='D01');same=[m for m in repeated['mentions'] if m['raw']=="'badge'"]
  scores=supplied(model,repeated['question'],[(m['start'],m['end']) for m in same]);assert len(scores)==2 and scores[0]['confidence']!=scores[1]['confidence']
 assert coverage==set(ROLES[:-1]);results.append(dict(covered_roles=sorted(coverage),seed=number,all194_targets_exact=True,public_parity_mentions=count,public_matches=matches,repeated_text=repeated['question'],repeated_gold=same,repeated_scores=scores))
 del model
write(OUT/'extended-smoke-complete.json',results);print([(r['seed'],r['public_parity_mentions'],r['repeated_scores']) for r in results])

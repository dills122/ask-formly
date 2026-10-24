"""Actual paired inference with native nested/flat decoding; no output repair."""
import os,sys,json,gc,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parent/'challenge_adaptation'
SUPERVISED=HERE.parent/'supervised_trial'
sys.path.insert(0,str(SUPERVISED))
from train import load_model,weights,sha,write
from peft import PeftModel
from score import evaluate
from comparison import deltas,overlaps,decision
import torch
os.environ['HF_HOME']=str(HERE/'test-output/.cache')
OUT=HERE/'test-output'
def read(p):return json.loads(p.read_text())
def check(manifest,root=None):
 for name,h in read(manifest).items():
  p=Path(name) if root is None else root/name
  if sha(p)!=h:raise ValueError('changed frozen input '+str(p))
def run():
 torch.set_num_threads(4);torch.use_deterministic_algorithms(True)
 check(PRIOR/'test-output/final-freeze.json',PRIOR)
 labels=read(HERE.parent/'pilot/labels.json')
 splits={'challenge':read(PRIOR/'challenge.json'),'regression':read(SUPERVISED/'dev.json')}
 if any(len(rows)!=24 or len({r['question_id'] for r in rows})!=24 for rows in splits.values()):raise ValueError('coverage')
 paths=[HERE/n for n in ('PROTOCOL.md','comparison.py','test_comparison.py','run.py')]
 paths += [PRIOR/'challenge.json',PRIOR/'challenge-families.json',SUPERVISED/'dev.json']
 for n in (1701,1702):paths.extend(p for p in (PRIOR/f'test-output/after-{n}/epoch-8/adapter').rglob('*') if p.is_file())
 frozen=read(PRIOR/'test-output/run-freeze.json');frozen.update({str(p):sha(p) for p in paths})
 write(OUT/'run-freeze.json',frozen)
 all_reports={};all_changes={};summaries={}
 for number in (1701,1702):
  model=PeftModel.from_pretrained(load_model(),str(PRIOR/f'test-output/after-{number}/epoch-8/adapter'),is_trainable=False)
  model.eval();initial=weights(model)
  if initial!=read(PRIOR/f'test-output/after-{number}/training-receipt.json')['final_hashes']:raise ValueError('checkpoint parameter mismatch')
  schema=model.create_schema().entities(labels)
  reports={};changes={};summaries[number]=[]
  for split,rows in splits.items():
   previous=read(PRIOR/f'test-output/after-{number}/{split}.json')
   if [r['id'] for r in previous]!=[r['question_id'] for r in rows]:raise ValueError('prior coverage/order')
   raw={'nested':[],'flat':[]}
   with torch.inference_mode():
    for i,row in enumerate(rows):
     for policy in (('nested','flat') if i%2==0 else ('flat','nested')):
      started=time.perf_counter()
      try:
       output=model.extract(row['question'],schema,threshold=.5,include_spans=True,include_confidence=True,overlap_policy=policy)
       result=dict(id=row['question_id'],output=output,seconds=time.perf_counter()-started)
      except Exception as error:result=dict(id=row['question_id'],error=type(error).__name__+': '+str(error),seconds=time.perf_counter()-started)
      raw[policy].append(result)
   for policy,values in raw.items():write(OUT/f'{number}-{split}-{policy}.json',values)
   equality=[a.get('output')==b.get('output') and 'error' not in a and 'error' not in b for a,b in zip(raw['nested'],previous)]
   write(OUT/f'{number}-{split}-baseline-check.json',dict(exact_output_matches=sum(equality),questions=len(rows)))
   if not all(equality):raise ValueError('nested baseline mismatch')
   family=read(PRIOR/'challenge-families.json') if split=='challenge' else {r['question_id']:'old_dev' for r in rows}
   questions=[dict(id=r['question_id'],question=r['question'],parent=r['question_id'],family=family[r['question_id']],origin=split) for r in rows]
   gold={r['question_id']:r for r in rows}
   reports[split]={p:evaluate(questions,gold,v) for p,v in raw.items()}
   changes[split]={}
   for row in rows:
    identifier=row['question_id'];before=reports[split]['nested']['cases'][identifier];after=reports[split]['flat']['cases'][identifier]
    changes[split][identifier]=dict(question=row['question'],**deltas(before['raw_mentions'],after['raw_mentions'],row['mentions']),
     before_overlap=overlaps(before['raw_mentions']),after_overlap=overlaps(after['raw_mentions']),
     invalid_before=bool(before['error']),invalid_after=bool(after['error']),exact_before=before['exact'],exact_after=after['exact'])
   b,a=reports[split]['nested'],reports[split]['flat'];cases=changes[split].values()
   summaries[number].append(dict(split=split,lost_correct=sum(len(c['lost_correct']) for c in cases),
    invalid_before=b['invalid'],invalid_after=a['invalid'],new_invalid=sum(not c['invalid_before'] and c['invalid_after'] for c in cases),
    accepted_before=b['accepted']['all']['f1'],accepted_after=a['accepted']['all']['f1']))
   print(number,split,'nested',b['exact'],b['invalid'],'flat',a['exact'],a['invalid'],'rawF1',a['raw']['all']['f1'],'acceptedF1',a['accepted']['all']['f1'],flush=True)
  final=weights(model)
  write(OUT/f'{number}-weight-check.json',dict(checkpoint_exact=True,unchanged=initial==final))
  if initial!=final:raise ValueError('inference changed parameters')
  all_reports[str(number)]=reports;all_changes[str(number)]=changes
  del model;gc.collect()
 write(OUT/'scores.json',all_reports);write(OUT/'changes.json',all_changes)
 write(OUT/'decision.json',dict(useful_without_loss=decision(summaries),checks=summaries))
 check(OUT/'run-freeze.json');check(PRIOR/'test-output/final-freeze.json',PRIOR)
 print('completed',decision(summaries),flush=True)
if __name__=='__main__':run()

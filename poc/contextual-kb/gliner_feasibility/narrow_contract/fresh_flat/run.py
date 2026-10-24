"""Frozen flat-decoder evaluation on fresh independently authored questions."""
import os,sys,json,gc,time,collections
from pathlib import Path
HERE=Path(__file__).resolve().parent
NARROW=HERE.parent
PRIOR=NARROW/'challenge_adaptation'
SUPERVISED=NARROW/'supervised_trial'
sys.path.insert(0,str(SUPERVISED))
from train import load_model,weights,sha,write
from peft import PeftModel
from score import evaluate
from checks import validate_inputs,validate_predictions
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
 check(HERE/'data-freeze.json',HERE)
 check(NARROW/'native_decoding/test-output/final-freeze.json',NARROW/'native_decoding')
 check(PRIOR/'test-output/final-freeze.json',PRIOR)
 rows=read(HERE/'questions.json');families=read(HERE/'families.json')
 previous=read(PRIOR/'test-output/train.json')+read(SUPERVISED/'dev.json')+read(PRIOR/'challenge.json')
 validate_inputs(rows,families,previous)
 counts=collections.Counter(m['kind'] for r in rows for m in r['mentions'])
 if len(rows)!=48 or sorted(collections.Counter(families.values()).values())!=[6]*8:raise ValueError('family counts')
 if sum(not r['mentions'] for r in rows)<6:raise ValueError('empty coverage')
 if any(counts[k]<6 for k in ('registration_name','model_key','version','ui_adapter')):raise ValueError('role coverage')
 labels=read(NARROW/'pilot/labels.json')
 paths=[HERE/n for n in ('PROTOCOL.md','questions.json','families.json','checks.py','test_checks.py','run.py','data-freeze.json')]
 frozen=read(NARROW/'native_decoding/test-output/run-freeze.json');frozen.update({str(p):sha(p) for p in paths})
 write(OUT/'run-freeze.json',frozen)
 write(OUT/'input-check.json',dict(questions=len(rows),families=dict(collections.Counter(families.values())),roles=dict(counts),empty=sum(not r['mentions'] for r in rows),exact_reused_questions=0))
 for number in (1701,1702):
  model=PeftModel.from_pretrained(load_model(),str(PRIOR/f'test-output/after-{number}/epoch-8/adapter'),is_trainable=False)
  model.eval();initial=weights(model)
  if initial!=read(PRIOR/f'test-output/after-{number}/training-receipt.json')['final_hashes']:raise ValueError('checkpoint mismatch')
  schema=model.create_schema().entities(labels);outputs=[]
  with torch.inference_mode():
   for row in rows:
    start=time.perf_counter()
    try:result=dict(output=model.extract(row['question'],schema,threshold=.5,include_spans=True,include_confidence=True,overlap_policy='flat'))
    except Exception as error:result=dict(error=type(error).__name__+': '+str(error))
    outputs.append(dict(id=row['question_id'],**result,seconds=time.perf_counter()-start))
  write(OUT/f'{number}-predictions.json',outputs)
  final=weights(model);write(OUT/f'{number}-weights.json',dict(checkpoint_exact=True,unchanged=initial==final))
  if initial!=final:raise ValueError('inference changed weights')
  del model;gc.collect()
 # Both first-response files exist before any scoring.
 report={};gold={r['question_id']:r for r in rows}
 questions=[dict(id=r['question_id'],question=r['question'],family=families[r['question_id']],parent=r['question_id'],origin='fresh_flat') for r in rows]
 for n in (1701,1702):
  predictions=read(OUT/f'{n}-predictions.json');validate_predictions(rows,predictions)
  report[str(n)]=evaluate(questions,gold,predictions)
 write(OUT/'scores.json',report)
 check(OUT/'run-freeze.json');check(HERE/'data-freeze.json',HERE)
 check(PRIOR/'test-output/final-freeze.json',PRIOR)
 for n,r in report.items():print(n,'exact',r['exact'],'invalid',r['invalid'],'raw',r['raw']['all'],'accepted',r['accepted']['all'],flush=True)
 print('completed',flush=True)
if __name__=='__main__':run()

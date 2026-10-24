"""Fixed role/boundary continuation with actual flat baseline and final inference."""
import os,sys,json,gc,time,random,collections
from pathlib import Path
HERE=Path(__file__).resolve().parent;NARROW=HERE.parent
VOCAB=NARROW/'vocabulary_adaptation';PRIOR=NARROW/'challenge_adaptation';SUPERVISED=NARROW/'supervised_trial';OUT=HERE/'test-output'
sys.path.insert(0,str(SUPERVISED))
from train import load_model,prepare,weights,seed,write,sha
from peft import PeftModel
from score import evaluate
from data import export
from policy import chunks,gate,rate,diagnostic_failure
import torch,numpy as np
os.environ['HF_HOME']=str(OUT/'.cache')
def read(p):return json.loads(p.read_text())
def check(p,root=None):
 for name,h in read(p).items():
  f=Path(name) if root is None else root/name
  if sha(f)!=h:raise ValueError('changed input '+str(f))
def inputs():
 train=read(OUT/'train.json');splits={'fresh':read(HERE/'fresh.json'),'vocab':read(VOCAB/'fresh.json'),'target':read(NARROW/'fresh_flat/questions.json'),'challenge':read(PRIOR/'challenge.json'),'olddev':read(SUPERVISED/'dev.json')}
 if len(train)!=194 or [len(r) for r in splits.values()]!=[40,40,48,24,24]:raise ValueError('counts')
 if len({r['question_id'] for r in train})!=194 or len({r['question'] for r in train})!=194:raise ValueError('duplicate training')
 for rows in splits.values():
  if len({r['question_id'] for r in rows})!=len(rows) or {r['question'] for r in rows}&{r['question'] for r in train}:raise ValueError('split overlap')
 for row in train+sum(splits.values(),[]):export(row,{})
 families=read(HERE/'families.json')
 if set(families)!={r['question_id'] for r in splits['fresh']} or sorted(collections.Counter(families.values()).values())!=[5]*8:raise ValueError('families')
 return train,splits,read(NARROW/'pilot/labels.json')
def predict(model,questions,labels):
 if any(not isinstance(q,str) for q in questions):raise ValueError('questions only')
 model.eval();schema=model.create_schema().entities(labels);results=[]
 with torch.inference_mode():
  for q in questions:
   t=time.perf_counter()
   try:result=dict(output=model.extract(q,schema,threshold=.5,overlap_policy='flat',include_spans=True,include_confidence=True))
   except Exception as e:result=dict(error=type(e).__name__+': '+str(e))
   results.append(dict(**result,seconds=time.perf_counter()-t))
 return results
def outputs(model,folder,splits,labels):
 for name,rows in splits.items():
  predictions=predict(model,[r['question'] for r in rows],labels)
  write(folder/f'{name}.json',[dict(id=r['question_id'],**v) for r,v in zip(rows,predictions)])
def save_verify(model,folder,panel,labels):
 folder.mkdir();rng=(random.getstate(),np.random.get_state(),torch.get_rng_state())
 before=predict(model,panel,labels);write(folder/'before.json',before);original=weights(model)
 model.save_pretrained(str(folder/'adapter'))
 fresh=PeftModel.from_pretrained(load_model(),str(folder/'adapter'),is_trainable=False)
 after=predict(fresh,panel,labels);write(folder/'after.json',after)
 equal=all(a.get('output')==b.get('output') and 'error' not in a and 'error' not in b for a,b in zip(before,after))
 same=original==weights(fresh)
 write(folder/'receipt.json',dict(predictions_identical=equal,parameters_identical=same,policy='flat',adapter_hashes={str(p.relative_to(folder/'adapter')):sha(p) for p in (folder/'adapter').rglob('*') if p.is_file()}))
 del fresh;gc.collect();random.setstate(rng[0]);np.random.set_state(rng[1]);torch.set_rng_state(rng[2])
 if not equal or not same:raise ValueError('first-save mismatch')
def baseline():
 train,splits,labels=inputs();check(HERE/'data-freeze.json',HERE)
 check(NARROW/'fresh_flat/test-output/final-freeze.json',NARROW/'fresh_flat')
 check(PRIOR/'test-output/final-freeze.json',PRIOR);check(VOCAB/'test-output/final-freeze.json',VOCAB)
 frozen=read(VOCAB/'test-output/run-freeze.json')
 paths=[HERE/n for n in ('PROTOCOL.md','run.py','policy.py','test_policy.py','training_annotations.py','train-new.json','fresh.json','families.json','data-freeze.json')]+[OUT/'train.json']
 frozen.update({str(p):sha(p) for p in paths});write(OUT/'run-freeze.json',frozen)
 for n in (1701,1702):
  folder=OUT/f'before-{n}';folder.mkdir()
  model=PeftModel.from_pretrained(load_model(),str(VOCAB/f'test-output/after-{n}/epoch-6/adapter'),is_trainable=False)
  if weights(model)!=read(VOCAB/f'test-output/after-{n}/training-receipt.json')['final_hashes']:raise ValueError('baseline checkpoint')
  for row in train:prepare(model,row,labels)
  outputs(model,folder,splits,labels)
  for split,path in {split:VOCAB/f'test-output/after-{n}/{old}.json' for split,old in [('vocab','fresh'),('target','target'),('challenge','challenge'),('olddev','olddev')]}.items():
   before=read(path);now=read(folder/f'{split}.json')
   same=len(before)==len(now) and all(a['id']==b['id'] and a.get('output')==b.get('output') and 'error' not in a and 'error' not in b for a,b in zip(before,now))
   write(folder/f'{split}-baseline-check.json',dict(exact=same,questions=len(now)))
   if not same:raise ValueError('baseline mismatch '+split)
  del model;gc.collect()
 write(OUT/'transport.json',dict(train=194,both_checkpoints_exact=True));check(OUT/'run-freeze.json');assess('baseline')
def adapt():
 train,splits,labels=inputs();check(OUT/'run-freeze.json')
 if not (OUT/'baseline-scores.json').exists():raise ValueError('baseline required')
 for n in (1701,1702):
  folder=OUT/f'after-{n}';folder.mkdir()
  model=PeftModel.from_pretrained(load_model(),str(VOCAB/f'test-output/after-{n}/epoch-6/adapter'),is_trainable=True);seed(n)
  initial=weights(model)
  if initial!=read(VOCAB/f'test-output/after-{n}/training-receipt.json')['final_hashes']:raise ValueError('starting checkpoint')
  trainable={name for name,p in model.named_parameters() if p.requires_grad}
  if not trainable or any('lora_' not in name for name in trainable):raise ValueError('unexpected trainable weights')
  write(folder/'parameters-before.json',dict(hashes=initial,trainable=sorted(trainable)))
  batches=[prepare(model,r,labels) for r in train];parameters=[p for p in model.parameters() if p.requires_grad]
  optimizer=torch.optim.AdamW(parameters,lr=1e-4,weight_decay=.01);step=0;started=time.perf_counter()
  with (folder/'losses.jsonl').open('x') as log:
   for epoch in range(1,7):
    total=0.;model.train()
    for chunk in chunks(len(train),n,epoch):
     optimizer.zero_grad(set_to_none=True)
     for i in chunk:
      loss=model(batches[i],gold_injection_prob=1.).total_loss
      if not torch.isfinite(loss):raise ValueError('nonfinite loss')
      total+=float(loss.detach());(loss/len(chunk)).backward()
      log.write(json.dumps(dict(epoch=epoch,step=step,id=train[i]['question_id'],loss=float(loss.detach())),allow_nan=False)+'\n')
     norm=torch.nn.utils.clip_grad_norm_(parameters,1.)
     if not torch.isfinite(norm):raise ValueError('nonfinite gradients')
     optimizer.step();step+=1
    log.flush();print(n,'epoch',epoch,'loss',total/len(train),'updates',step,flush=True)
    if epoch in (1,6):save_verify(model,folder/f'epoch-{epoch}',[r['question'] for r in train[-8:]],labels)
  final=weights(model);frozen_changed=[name for name in initial if name not in trainable and initial[name]!=final[name]];trained_changed=[name for name in trainable if initial[name]!=final[name]]
  write(folder/'training-receipt.json',dict(epochs=6,updates=step,seconds=time.perf_counter()-started,frozen_changed=frozen_changed,trained_changed=trained_changed,final_hashes=final))
  if frozen_changed or not trained_changed or step!=150:raise ValueError('training integrity')
  outputs(model,folder,{**splits,'train':train},labels)
  del model,optimizer,parameters,batches;gc.collect()
 check(OUT/'run-freeze.json');check(PRIOR/'test-output/final-freeze.json',PRIOR);check(VOCAB/'test-output/final-freeze.json',VOCAB);assess('final')
def assess(stage):
 train,splits,labels=inputs();report={}
 for phase in (('before',) if stage=='baseline' else ('before','after')):
  report[phase]={}
  for n in (1701,1702):
   report[phase][str(n)]={}
   for split,rows in ({**splits,'train':train} if phase=='after' else splits).items():
    pred=read(OUT/f'{phase}-{n}/{split}.json');ids={r['question_id'] for r in rows}
    if len(pred)!=len(rows) or {r['id'] for r in pred}!=ids:raise ValueError('prediction coverage')
    fam=read(HERE/'families.json') if split=='fresh' else {r['question_id']:split for r in rows}
    questions=[dict(id=r['question_id'],question=r['question'],parent=r['question_id'],family=fam[r['question_id']],origin=split) for r in rows]
    report[phase][str(n)][split]=evaluate(questions,{r['question_id']:r for r in rows},pred)
 if stage=='final':
  checks=[]
  for n in (1701,1702):
   b=report['before'][str(n)];a=report['after'][str(n)];bf=b['fresh'];af=a['fresh']
   earlier=read(VOCAB/'test-output/final-scores.json')['before'][str(n)]
   regressions=[]
   for split in ('vocab','target','challenge','olddev'):
    comparisons=[('vocabulary',b[split])]
    if split!='vocab':comparisons.append(('challenge_flat',earlier[split]))
    for origin,old in comparisons:
     if diagnostic_failure(a[split],old):
      regressions.append(split+':'+origin)
   checks.append(dict(fresh_gain=af['accepted']['all']['f1']-bf['accepted']['all']['f1'],exact_gain=af['exact']-bf['exact'],
    api_recall_gain=rate(af['accepted']['api_reference']['recall'])-rate(bf['accepted']['api_reference']['recall']),invalid_gain=af['invalid']-bf['invalid'],
    empty_fp_gain=af['exact_by_gold']['clear_empty']['raw_nonempty']-bf['exact_by_gold']['clear_empty']['raw_nonempty'],diagnostic_regressions=regressions))
  report['decision']=dict(improved=gate(checks),checks=checks)
 write(OUT/f'{stage}-scores.json',report)
 for phase in ('before','after'):
  for n,ss in report.get(phase,{}).items():
   for split,r in ss.items():print(phase,n,split,'exact',r['exact'],'invalid',r['invalid'],'rawF1',r['raw']['all']['f1'],'acceptedF1',r['accepted']['all']['f1'],flush=True)
 print(report.get('decision',{}),flush=True)
if __name__=='__main__':
 torch.set_num_threads(4);torch.use_deterministic_algorithms(True)
 if sys.argv[1]=='baseline':baseline()
 elif sys.argv[1]=='adapt':adapt()
 else:raise ValueError('command')

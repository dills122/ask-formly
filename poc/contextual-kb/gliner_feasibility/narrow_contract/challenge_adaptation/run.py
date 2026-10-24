"""Isolated paired checkpoint replay and fixed continuation training."""
import os,sys,json,gc,random,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parent/'supervised_trial'
sys.path.insert(0,str(PRIOR))
from train import load_model,prepare,predict,save_verify,weights,seed,write,sha
from peft import PeftModel
import torch
from experiment import verify_splits,paired_decision,challenge_hashes
from score import evaluate
os.environ['HF_HOME']=str(HERE/'test-output/.cache')
OUT=HERE/'test-output'

def read(path):return json.loads(path.read_text())
def check(path,root=None):
 for name,digest in read(path).items():
  p=Path(name) if root is None else root/name
  if sha(p)!=digest:raise ValueError('frozen artifact changed: '+str(p))
def inputs():
 train=read(OUT/'train.json');challenge=read(HERE/'challenge.json');dev=read(PRIOR/'dev.json')
 verify_splits(train,challenge+dev)
 if (len(train),len(challenge),len(dev))!=(98,24,24):raise ValueError('counts')
 labels=read(HERE.parent/'pilot/labels.json')
 return train,challenge,dev,labels

def score(rows,predictions,families):
 ids={r['question_id'] for r in rows}
 if len(predictions)!=len(rows) or {r['id'] for r in predictions}!=ids:raise ValueError('prediction coverage')
 qs=[dict(id=r['question_id'],question=r['question'],family=families[r['question_id']],origin='challenge_adaptation',parent=r['question_id']) for r in rows]
 return evaluate(qs,{r['question_id']:r for r in rows},predictions)

def outputs(model,folder,splits,labels):
 for name,rows in splits:
  result=predict(model,[r['question'] for r in rows],labels)
  write(folder/f'{name}.json',[dict(id=r['question_id'],**p) for r,p in zip(rows,result)])

def baseline():
 train,challenge,dev,labels=inputs()
 check(HERE/'training-freeze.json',HERE)
 for name,digest in challenge_hashes(read(HERE/'challenge-freeze.json')).items():
  if sha(Path(name))!=digest:raise ValueError('challenge manifest changed '+name)
 check(PRIOR/'test-output/final-freeze.json',PRIOR)
 paths=[HERE/name for name in ('run.py','experiment.py','test_experiment.py','PROTOCOL.md','train-new.json','challenge.json','challenge-families.json')]
 paths += [OUT/'train.json',PRIOR/'train.py',PRIOR/'data.py',PRIOR/'dev.json',HERE.parent/'pilot/score.py',HERE.parent/'pilot/contract.py',HERE.parent/'pilot/labels.json']
 # Prior run freeze covers pinned model and installed source, without modifying it.
 frozen=read(PRIOR/'test-output/freeze.json');frozen.update({str(p):sha(p) for p in paths})
 write(OUT/'run-freeze.json',frozen)
 for number in (1701,1702):
  folder=OUT/f'before-{number}';folder.mkdir()
  model=PeftModel.from_pretrained(load_model(),str(PRIOR/f'test-output/seed-{number}/epoch-16/adapter'),is_trainable=False)
  for row in train+challenge+dev:prepare(model,row,labels)
  outputs(model,folder,[('challenge',challenge),('regression',dev)],labels)
  del model;gc.collect()
 write(OUT/'transport.json',dict(train=98,challenge=24,regression=24,both_checkpoints_exact=True))
 check(OUT/'run-freeze.json')
 print('baseline complete',flush=True)

def adapt():
 train,challenge,dev,labels=inputs();check(OUT/'run-freeze.json')
 before=[score(challenge,read(OUT/f'before-{n}/challenge.json'),read(HERE/'challenge-families.json')) for n in (1701,1702)]
 if all(s['exact']==len(challenge) for s in before):raise ValueError('no demonstrated adaptation need')
 for number in (1701,1702):
  folder=OUT/f'after-{number}';folder.mkdir()
  model=PeftModel.from_pretrained(load_model(),str(PRIOR/f'test-output/seed-{number}/epoch-16/adapter'),is_trainable=True)
  seed(number)
  trainable={n for n,p in model.named_parameters() if p.requires_grad}
  if not trainable or any('lora_' not in n for n in trainable):raise ValueError('unexpected trainable parameters')
  initial=weights(model);write(folder/'parameters-before.json',dict(hashes=initial,trainable=sorted(trainable)))
  batches=[prepare(model,row,labels) for row in train]
  parameters=[p for p in model.parameters() if p.requires_grad]
  optimizer=torch.optim.AdamW(parameters,lr=1e-4,weight_decay=.01)
  step=0;started=time.perf_counter()
  with (folder/'losses.jsonl').open('x') as log:
   for epoch in range(1,9):
    order=list(range(len(train)));random.Random(number+epoch).shuffle(order)
    total=0.;model.train()
    for offset in range(0,len(order),8):
     chunk=order[offset:offset+8];optimizer.zero_grad(set_to_none=True)
     for i in chunk:
      loss=model(batches[i],gold_injection_prob=1.).total_loss
      if not torch.isfinite(loss):raise ValueError('nonfinite loss')
      total+=float(loss.detach());(loss/len(chunk)).backward()
      log.write(json.dumps(dict(epoch=epoch,step=step,id=train[i]['question_id'],loss=float(loss.detach())),allow_nan=False)+'\n')
     norm=torch.nn.utils.clip_grad_norm_(parameters,1.)
     if not torch.isfinite(norm):raise ValueError('nonfinite gradient')
     optimizer.step();step+=1
    log.flush();print(number,'epoch',epoch,'loss',total/len(train),'updates',step,flush=True)
    if epoch in (1,8):save_verify(model,folder/f'epoch-{epoch}',train[-8:],labels)
  final=weights(model)
  frozen_changed=[n for n in initial if n not in trainable and initial[n]!=final[n]]
  trained_changed=[n for n in trainable if initial[n]!=final[n]]
  write(folder/'training-receipt.json',dict(epochs=8,updates=step,seconds=time.perf_counter()-started,frozen_changed=frozen_changed,trained_changed=trained_changed,final_hashes=final))
  if frozen_changed or not trained_changed or step!=104:raise ValueError('training integrity')
  outputs(model,folder,[('challenge',challenge),('regression',dev),('train',train)],labels)
  del model,optimizer,batches,parameters;gc.collect()
 check(OUT/'run-freeze.json');check(PRIOR/'test-output/final-freeze.json',PRIOR)
 print('adaptation complete',flush=True)

def assess(stage):
 train,challenge,dev,labels=inputs();report={}
 families=read(HERE/'challenge-families.json')
 for phase in (('before',) if stage=='baseline' else ('before','after')):
  report[phase]={}
  for n in (1701,1702):
   report[phase][str(n)]={}
   splits=[('challenge',challenge,families),('regression',dev,{r['question_id']:'old_dev' for r in dev})]
   if phase=='after':splits.append(('train',train,{r['question_id']:'training' for r in train}))
   for name,rows,family in splits:
    report[phase][str(n)][name]=score(rows,read(OUT/f'{phase}-{n}/{name}.json'),family)
 if stage!='baseline':
  report['decision']=paired_decision([(report['before'][str(n)]['challenge'],report['after'][str(n)]['challenge'],report['before'][str(n)]['regression'],report['after'][str(n)]['regression']) for n in (1701,1702)])
 write(OUT/f'{stage}-scores.json',report)
 for phase in ('before','after'):
  for n,splits in report.get(phase,{}).items():
   for name,r in splits.items():print(phase,n,name,{k:r[k] for k in ('exact','invalid')},'raw',r['raw']['all'],'accepted',r['accepted']['all'])
 print(report.get('decision',{}))

if __name__=='__main__':
 torch.set_num_threads(4);torch.use_deterministic_algorithms(True)
 command=sys.argv[1]
 if command=='baseline':baseline();assess('baseline')
 elif command=='adapt':adapt();assess('final')
 else:raise ValueError('unknown command')

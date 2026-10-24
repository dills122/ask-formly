"""Bounded two-seed entity-only LoRA trial; CPU, offline, no repairs."""
import os,sys,json,time,hashlib,random,gc,math
import importlib.metadata
from pathlib import Path
from data import export,combine,ROLES
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HOME=str(HERE/'test-output/.cache'))
from gliner2 import AutoExtractor
from gliner2.processor import SamplingConfig
from gliner2.training.trainer import ExtractorTrainer,TrainingConfig
from gliner2.training.data import InputExample
from peft import PeftModel
import torch
import numpy as np

def load_model():
 torch.set_num_threads(4);torch.manual_seed(1701)
 model=AutoExtractor.from_pretrained(str(BASE/'models/gliner2.5-base-v1'),local_files_only=True,map_location='cpu')
 model.float()
 model.processor.sampling_config=SamplingConfig(remove_json_structure_prob=0,shuffle_json_fields=False,
  remove_json_field_prob=0,remove_entities_prob=0,shuffle_entities=False,remove_entity_prob=0,
  synthetic_entity_label_prob=0,remove_relations_prob=0,swap_head_tail_prob=0,
  remove_classification_prob=0,shuffle_classification_labels=False,remove_classification_label_prob=0,
  synthetic_label_prob=0,include_true_label_prob=1)
 return model

def write(path,value):
 with path.open('x') as f:json.dump(value,f,indent=2,allow_nan=False)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def weights(model):
 return {name:hashlib.sha256(p.detach().cpu().contiguous().numpy().tobytes()).hexdigest() for name,p in model.named_parameters()}
def seed(n):random.seed(n);np.random.seed(n);torch.manual_seed(n)
def prepare(model,row,labels):
 sample=export(row,labels)
 obj=InputExample.from_dict(sample)
 if not obj.is_valid():raise ValueError(obj.validate())
 if obj.to_dict()!=sample:raise ValueError('native roundtrip changed schema/spans')
 batch=model.processor.collate_fn_train([(sample['input'],sample['output'])],architecture='boundary',error_policy='raise',
  on_capacity_exceeded='raise',dedupe_contained_entity_spans=False)
 seen=set()
 for query in batch.query_layouts[0].queries:
  if query.task_type!='entities':raise ValueError('nonentity target')
  kind=query.role_name;seen.add(kind)
  pairs=batch.targets.mention_pairs[0,query.query_id][batch.targets.mention_mask[0,query.query_id]]
  actual=sorted((batch.start_mappings[0][int(a)],batch.end_mappings[0][int(b)-1]) for a,b in pairs)
  expected=sorted((m['start'],m['end']) for m in row['mentions'] if m['kind']==kind)
  if actual!=expected:raise ValueError('target transport '+row['question_id']+' '+kind)
 if seen!=set(ROLES):raise ValueError('missing entity queries')
 return batch
def predict(model,questions,labels):
 if any(not isinstance(q,str) for q in questions):raise ValueError('questions only')
 model.eval();schema=model.create_schema().entities(labels);results=[]
 with torch.inference_mode():
  for q in questions:
   t=time.perf_counter()
   try:result={'output':model.extract(q,schema,threshold=.5,include_spans=True,include_confidence=True,overlap_policy='nested')}
   except Exception as e:result={'error':type(e).__name__+': '+str(e)}
   results.append({**result,'seconds':time.perf_counter()-t})
 return results
def save_verify(model,folder,panel,labels):
 folder.mkdir()
 rng=(random.getstate(),np.random.get_state(),torch.get_rng_state())
 before=predict(model,[r['question'] for r in panel],labels)
 write(folder/'before.json',before)
 original=weights(model)
 model.save_pretrained(str(folder/'adapter'))
 fresh=PeftModel.from_pretrained(load_model(),str(folder/'adapter'),is_trainable=False)
 after=predict(fresh,[r['question'] for r in panel],labels)
 write(folder/'after.json',after)
 equal=all(a.get('output')==b.get('output') and 'error' not in a and 'error' not in b for a,b in zip(before,after))
 same=original==weights(fresh)
 write(folder/'receipt.json',dict(predictions_identical=equal,parameters_identical=same,
   adapter_hashes={str(f.relative_to(folder/'adapter')):sha(f) for f in (folder/'adapter').rglob('*') if f.is_file()}))
 del fresh;gc.collect()
 random.setstate(rng[0]);np.random.set_state(rng[1]);torch.set_rng_state(rng[2])
 if not equal or not same:raise ValueError('first-save verification failed')
def main():
 torch.set_num_threads(4);torch.use_deterministic_algorithms(True)
 pilot=json.loads((HERE.parent/'pilot/gold.json').read_text())
 train=combine(pilot,json.loads((HERE/'train-new.json').read_text()))
 dev=json.loads((HERE/'dev.json').read_text())
 if len(train)!=62 or len(dev)!=24:raise ValueError('dataset count')
 if {r['question'] for r in train}&{r['question'] for r in dev}:raise ValueError('train/dev exact overlap')
 labels=json.loads((HERE.parent/'pilot/labels.json').read_text())
 write(HERE/'test-output/train.json',train)
 paths=[HERE/n for n in ('train.py','data.py','PROTOCOL.md','train-new.json','dev.json')]
 paths += [HERE.parent/'pilot'/n for n in ('gold.json','labels.json','contract.py','hardened.py')]
 paths += [p for p in (BASE/'models/gliner2.5-base-v1').rglob('*') if p.is_file()]
 import gliner2
 paths += list(Path(gliner2.__file__).parent.rglob('*.py'))
 write(HERE/'test-output/environment.json',{name:importlib.metadata.version(name) for name in ('gliner2','torch','transformers','peft')})
 write(HERE/'test-output/freeze.json',{str(p):sha(p) for p in paths})
 base=load_model()
 # Verify every actual row maps to its exact character spans before optimization.
 for row in train+dev:prepare(base,row,labels)
 write(HERE/'test-output/transport.json',dict(train=len(train),dev=len(dev),all_exact=True))
 for split,rows in (('train',train),('dev',dev)):
  output=predict(base,[r['question'] for r in rows],labels)
  write(HERE/f'test-output/base-{split}.json',[dict(id=r['question_id'],**o) for r,o in zip(rows,output)])
 del base;gc.collect()
 for number in (1701,1702):
  out=HERE/f'test-output/seed-{number}';out.mkdir()
  model=load_model();seed(number)
  trainer=ExtractorTrainer(model,TrainingConfig(output_dir=str(out/'trainer'),num_epochs=16,max_steps=128,
   batch_size=1,gradient_accumulation_steps=8,fp16=False,bf16=False,num_workers=0,
   use_lora=True,lora_r=8,lora_alpha=16.,lora_dropout=0.,
   lora_target_modules=['encoder','extractive_head'],save_adapter_only=True,
   report_to_wandb=False,eval_strategy='no',seed=number))
  model=trainer.model
  trainable={n for n,p in model.named_parameters() if p.requires_grad}
  initial=weights(model)
  write(out/'parameters-before.json',{'hashes':initial,'trainable':sorted(trainable)})
  batches=[prepare(model,r,labels) for r in train]
  opt=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=5e-4,weight_decay=.01)
  step=0;started=time.perf_counter()
  with (out/'losses.jsonl').open('x') as log:
   for epoch in range(1,17):
    order=list(range(len(train)));random.Random(number+epoch).shuffle(order)
    total=0.;model.train()
    for offset in range(0,len(order),8):
     chunk=order[offset:offset+8];opt.zero_grad(set_to_none=True)
     for index in chunk:
      output=model(batches[index],gold_injection_prob=1.)
      loss=output.total_loss
      if not torch.isfinite(loss):raise ValueError('nonfinite loss')
      total+=float(loss.detach());(loss/len(chunk)).backward()
      log.write(json.dumps(dict(epoch=epoch,step=step,id=train[index]['question_id'],loss=float(loss.detach()),
       terms={k:float(v.detach()) for k,v in output.losses.items() if torch.is_tensor(v) and v.numel()==1}),allow_nan=False)+'\n')
     norm=torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad],1.)
     if not torch.isfinite(norm):raise ValueError('nonfinite gradient')
     opt.step();step+=1
    log.flush();print(number,'epoch',epoch,'mean_loss',total/len(train),'updates',step,flush=True)
    if epoch in (1,16):save_verify(model,out/f'epoch-{epoch}',train[:8],labels)
   final=weights(model)
   frozen_changed=[n for n in initial if n not in trainable and initial[n]!=final[n]]
   trained_changed=[n for n in trainable if initial[n]!=final[n]]
   write(out/'training-receipt.json',dict(epochs=16,updates=step,seconds=time.perf_counter()-started,
    frozen_changed=frozen_changed,trained_changed=trained_changed,final_hashes=final))
   if frozen_changed or not trained_changed:raise ValueError('parameter update violation')
  for split,rows in (('train',train),('dev',dev)):
   output=predict(model,[r['question'] for r in rows],labels)
   write(out/f'final-{split}.json',[dict(id=r['question_id'],**o) for r,o in zip(rows,output)])
  del model,trainer,opt,batches;gc.collect()
 for p,h in json.loads((HERE/'test-output/freeze.json').read_text()).items():
  if sha(Path(p))!=h:raise ValueError('source mutated '+p)
 print('completed',flush=True)
if __name__=='__main__':main()

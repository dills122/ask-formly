"""One frozen NLI diagnostic run; development only, never modifies raw extractions."""
import gc,hashlib,json,os,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;NARROW=HERE.parent
os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HOME=str(HERE/'model-cache'))
sys.path.insert(0,str(NARROW/'verifier_evaluation'))
from runtime import protect,verify_manifest,read,write,load_model,PeftModel,torch,guarded_run
from decisions import tokens
sys.path.insert(0,str(NARROW/'verifier_shadow'))
from shadow import validate
from entailment import marked,HYPOTHESES,decide,assess,simulate

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def authorize():
 receipt=read(HERE/'review-ready.json')
 if receipt.get('verdict')!='ready' or receipt.get('independent') is not True:raise ValueError('independent preparation review required')
 bindings=receipt['bindings'];required={str(p) for p in HERE.glob('*.py')}|{str(HERE/'PROTOCOL.md'),str(HERE/'model-revision.json')}|{str(p) for p in (HERE/'data').glob('*.json')}|{str(p) for p in (HERE/'model').iterdir() if p.is_file()}
 if not required<=set(bindings):raise ValueError('review missing required bindings')
 verify_manifest(bindings);return bindings

def panels(seed):
 old=NARROW/'verifier_shadow';out={}
 for name,file,cache in [('shadow30','development-v1.json','new_development'),('adjudicated30','original-development-adjudicated-v1.json','legacy_adjudicated')]:
  rows=read(old/'data'/file);raw=read(old/f'test-output/frozen-shadow-v1/{seed}-{cache}-outputs.json')
  if [(r['id'],r['text']) for r in rows]!=[(r['id'],r['text']) for r in raw]:raise ValueError('cache identity mismatch')
  out[name]=[dict(r,raw=c['raw'],extraction_source='frozen_cache') for r,c in zip(rows,raw)]
 return out

class NLI:
 def __init__(self):
  from transformers import AutoTokenizer,AutoModelForSequenceClassification
  t=time.perf_counter();self.tokenizer=AutoTokenizer.from_pretrained(HERE/'model',local_files_only=True,trust_remote_code=False)
  self.model=AutoModelForSequenceClassification.from_pretrained(HERE/'model',local_files_only=True,trust_remote_code=False).float().eval()
  self.model.requires_grad_(False)
  labels={int(k):v for k,v in self.model.config.id2label.items()}
  if set(labels.values())!={'entailment','not_entailment'}:raise ValueError('unexpected label mapping')
  self.index=next(k for k,v in labels.items() if v=='entailment');self.cache={};self.times=[];self.cold=time.perf_counter()-t
 def score(self,text,a,b):
  key=(text,a,b)
  if key in self.cache:return self.cache[key]
  premise=marked(text,a,b);start=time.perf_counter()
  inputs=self.tokenizer([premise]*7,list(HYPOTHESES),padding=True,truncation=False,return_tensors='pt')
  if inputs['input_ids'].shape[1]>self.model.config.max_position_embeddings:raise ValueError('overlength pair: no truncation allowed')
  with torch.inference_mode():logits=self.model(**inputs).logits
  if logits.shape!=(7,2) or not torch.isfinite(logits).all():raise ValueError('invalid NLI logits')
  p=logits.softmax(dim=-1)[:,self.index].tolist();decide(p)
  self.times.append(time.perf_counter()-start);self.cache[key]=p;return p

def main():
 bindings=authorize();out=HERE/'test-output/run-v1';out.mkdir(exist_ok=False)
 prior=[NARROW/'verifier_shadow/test-output/final-freeze.json',NARROW/'verifier_evaluation/test-output/full-run-final-freeze.json',NARROW/'verifier_evaluation/test-output/sealed-preparation-freeze.json',NARROW/'verifier_diagnosis/test-output/final-freeze.json']
 def audits():return dict(protected=protect(),prior={str(p):verify_manifest(read(p)) for p in prior},inputs=verify_manifest(bindings),v2_sources=verify_manifest(read(HERE/'data/source-bindings.json')))
 def work():
  write(out/'before.json',audits());torch.set_num_threads(4);torch.use_deterministic_algorithms(True)
  fresh=read(HERE/'data/fresh-development.json');validate(fresh)
  usability=read(HERE/'data/usability-questions.json')
  if len(fresh)!=24 or len(usability)!=60:raise ValueError('panel size mismatch')
  allrows={};extractcost={}
  for seed in (1701,1702):
   t=time.perf_counter();model=PeftModel.from_pretrained(load_model(),str(NARROW/f'role_boundary_adaptation/test-output/after-{seed}/epoch-6/adapter'),is_trainable=False).eval();model.requires_grad_(False)
   schema=model.create_schema().entities(read(NARROW/'pilot/labels.json'));extractcost[str(seed)]={'cold':time.perf_counter()-t,'calls':0,'seconds':0.}
   bypanel=panels(seed)
   try:
    for name,rows in [('fresh24',fresh),('usability60',usability)]:
     records=[]
     for r in rows:
      t=time.perf_counter()
      with torch.inference_mode():raw=model.extract(r['text'],schema,threshold=.5,overlap_policy='flat',include_spans=True,include_confidence=True)
      elapsed=time.perf_counter()-t;tokens(r['text'],raw)
      records.append(dict(r,raw=raw,extraction_source='new_frozen_model_call',extraction_seconds=elapsed));extractcost[str(seed)]['calls']+=1;extractcost[str(seed)]['seconds']+=elapsed
     bypanel[name]=records
   finally:del model;gc.collect()
   for name,rows in bypanel.items():write(out/f'{seed}-{name}-extractions.json',rows)
   allrows[str(seed)]=bypanel
  nli=NLI();summary={};oracle={}
  try:
   # All operational scores before any oracle. No gold in score signature.
   for seed,bypanel in allrows.items():
    summary[seed]={}
    for name,rows in bypanel.items():
     records=[]
     for r in rows:
      before=sorted(tokens(r['text'],r['raw']));spans=sorted({(a,b) for a,b,k in before})
      scores=[dict(start=a,end=b,p=nli.score(r['text'],a,b)) for a,b in spans]
      records.append(dict(r,before=before,scores=scores,hypothetical_after=sorted(simulate(before,{(s['start'],s['end']):s['p'] for s in scores}))))
     write(out/f'{seed}-{name}-scored.json',records)
     if name!='usability60':summary[seed][name]=assess(records)
   for name,rows in [('fresh24',fresh),('shadow30',read(NARROW/'verifier_shadow/data/development-v1.json')),('adjudicated30',read(NARROW/'verifier_shadow/data/original-development-adjudicated-v1.json'))]:
    records=[]
    for r in rows:
     for probe in r['probes']:
      p=nli.score(r['text'],probe['start'],probe['end']);d=decide(p)
      records.append(dict(id=r['id'],**probe,p=p,decision=d))
    write(out/f'{name}-oracle.json',records)
    oracle[name]=dict(gold=sum(p['expected_role'] is not None for p in records),gold_correct=sum(p['expected_role'] is not None and p['decision']['role']==p['expected_role'] for p in records),negatives=sum(p['expected_role'] is None for p in records),negative_no_entity=sum(p['expected_role'] is None and p['decision']['reason']=='no_entity' for p in records))
   write(out/'summary.json',summary);write(out/'oracle-summary.json',oracle)
   write(out/'cost.json',dict(extraction=extractcost,nli_cold_seconds=nli.cold,nli_unique_occurrences=len(nli.times),nli_pair_count=7*len(nli.times),nli_seconds=sum(nli.times),nli_occurrence_seconds=nli.times,note='shared memoization across seeds/panels; not per-seed or production latency'))
   gate=all(sum(s['corrected_groups'] for s in panels_.values())>0 and all(s['wrong_changes']==s['lost_correct']==0 for s in panels_.values()) for panels_ in summary.values())
   return dict(training=False,sealed_evaluation=False,raw_outputs_modified=False,development_gate=gate,usability_requires_independent_review=True)
  finally:del nli;gc.collect()
 def after():write(out/'after.json',audits())
 completion=guarded_run(work,[('preservation',after)],lambda r:write(out/'completion.json',r),lambda e:write(out/'failure.json',dict(errors=e)))
 write(out/'freeze.json',{str(p):sha(p) for p in out.iterdir() if p.is_file()});print(json.dumps(completion))
if __name__=='__main__':main()

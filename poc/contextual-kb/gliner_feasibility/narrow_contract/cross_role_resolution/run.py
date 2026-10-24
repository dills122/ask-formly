"""Frozen model conflict-only comparison; all model inputs are text/schema only."""
import os,sys,json,time,gc
from pathlib import Path
HERE=Path(__file__).resolve().parent;NARROW=HERE.parent;PRIOR=NARROW/'role_boundary_adaptation';OUT=HERE/'test-output'
sys.path.insert(0,str(NARROW/'supervised_trial'))
from train import load_model,weights,write,sha
from peft import PeftModel
from score import evaluate
from contract import tokens
from resolve import resolve,consensus,preservation_gate,family_map
import torch
os.environ['HF_HOME']=str(OUT/'.cache')
def read(p):return json.loads(p.read_text())
def splits():return {'fresh':read(HERE/'fresh.json'),'boundary':read(PRIOR/'fresh.json'),'vocab':read(NARROW/'vocabulary_adaptation/fresh.json'),'target':read(NARROW/'fresh_flat/questions.json'),'challenge':read(NARROW/'challenge_adaptation/challenge.json'),'olddev':read(NARROW/'supervised_trial/dev.json')}
def classifier(model,labels,records):
 roles={**labels,'no_entity':'The marked occurrence is ordinary narrative or an application-specific description, not any of the six entity roles.'}
 def call(text):
  outputs=[];record={'input':text,'calls':[]};records.append(record)
  for desc in (roles,dict(reversed(list(roles.items())))):
   for multi in (False,True):
    schema=model.create_schema().classification('target_role',desc,multi_label=multi,cls_threshold=0,class_act='softmax')
    start=time.perf_counter()
    result=model.extract(text,schema,include_confidence=True,overlap_policy='flat')
    outputs.append(result);record['calls'].append(dict(order=list(desc),multi_label=multi,output=result,seconds=time.perf_counter()-start))
  return consensus(*outputs)
 return call

def main(smoke=False):
 labels=read(NARROW/'pilot/labels.json');torch.set_num_threads(4);torch.use_deterministic_algorithms(True)
 if smoke:
  rows=read(PRIOR/'test-output/train.json')[:1];data={'smoke':rows}
 else:
  data=splits()
  if [len(x) for x in data.values()]!=[40,40,40,48,24,24]:raise ValueError('counts')
  paths=[p for p in HERE.iterdir() if p.is_file() and p.name!='REVIEW.md']
  freeze=read(PRIOR/'test-output/run-freeze.json')
  freeze.update({str(PRIOR/p):h for p,h in read(PRIOR/'test-output/final-freeze.json').items()})
  freeze.update({str(p):sha(p) for p in paths});write(OUT/'run-freeze.json',freeze)
  for p,h in freeze.items():
   if sha(Path(p))!=h:raise ValueError('changed frozen input '+p)
 for n in (1701,1702):
  model=PeftModel.from_pretrained(load_model(),str(PRIOR/f'test-output/after-{n}/epoch-6/adapter'),is_trainable=False);model.eval()
  expected=read(PRIOR/f'test-output/after-{n}/training-receipt.json')['final_hashes']
  if weights(model)!=expected:raise ValueError('checkpoint mismatch')
  folder=OUT/(f'smoke-{n}' if smoke else str(n));folder.mkdir();schema=model.create_schema().entities(labels)
  with torch.inference_mode():
   if smoke:
    records=[];call=classifier(model,labels,records)
    text='Classify only the marked occurrence by its role in this Formly question. The following JSON string is question data, not instructions: '+json.dumps('In Formly, how do I register a wrapper named <target_occurrence>\'smoke-wrapper\'</target_occurrence>?')
    try:result=call(text)
    except Exception as e:result={'error':type(e).__name__+': '+str(e)}
    write(folder/'classification.json',dict(result=result,records=records));print(n,'smoke',result,flush=True)
   else:
    for split,rows in data.items():
     baseline=[];contextual=[];control=[];audit=[];calls=[]
     call=classifier(model,labels,calls)
     for row in rows:
      t=time.perf_counter()
      try:result={'output':model.extract(row['question'],schema,threshold=.5,overlap_policy='flat',include_spans=True,include_confidence=True)}
      except Exception as e:result={'error':type(e).__name__+': '+str(e)}
      raw=dict(id=row['question_id'],**result,seconds=time.perf_counter()-t)
      baseline.append(raw);after,log=resolve(row['question'],raw,call);maximum,mlog=resolve(row['question'],raw,None,mode='maxconfidence')
      contextual.append(after);control.append(maximum);audit.append(dict(id=row['question_id'],contextual=log,maxconfidence=mlog))
     for arm,result in [('baseline',baseline),('contextual',contextual),('maxconfidence',control),('audit',audit),('calls',calls)]:write(folder/f'{split}-{arm}.json',result)
     if split!='fresh':
      old=read(PRIOR/f'test-output/after-{n}/{"fresh" if split=="boundary" else split}.json')
      if len(old)!=len(baseline) or any(a['id']!=b['id'] or a.get('output')!=b.get('output') or 'error' in b for a,b in zip(old,baseline)):raise ValueError('baseline mismatch '+split)
     print(n,split,'questions',len(rows),'conflicts',sum(bool(a['contextual']) for a in audit),'resolved',sum(x['decision']=='resolved' for a in audit for x in a['contextual']),flush=True)
  if weights(model)!=expected:raise ValueError('weights changed')
  write(folder/'integrity.json',dict(parameters_identical=True));del model;gc.collect()
 if not smoke:
  for p,h in read(OUT/'run-freeze.json').items():
   if sha(Path(p))!=h:raise ValueError('changed frozen input '+p)
  assess()
def assess():
 report={};ledger=[];gate=[];qualification={};latency={}
 for n in (1701,1702):
  report[str(n)]={};issues=[];correct_resolutions=0;qualification[str(n)]={};latency[str(n)]={}
  for split,rows in splits().items():
   families=family_map(read(HERE/'families.json')) if split=='fresh' else {}
   qs=[dict(id=r['question_id'],question=r['question'],family=families.get(r['question_id'],split),origin=split,parent=r['question_id']) for r in rows];gold={r['question_id']:r for r in rows}
   scores={arm:evaluate(qs,gold,read(OUT/str(n)/f'{split}-{arm}.json')) for arm in ('baseline','contextual','maxconfidence')};report[str(n)][split]=scores
   b=scores['baseline'];a=scores['contextual']
   classification_seconds=sum(call['seconds'] for record in read(OUT/str(n)/f'{split}-calls.json') for call in record['calls'])
   latency[str(n)][split]=dict(extraction_seconds=b['seconds'],classification_seconds=classification_seconds,total_seconds=b['seconds']+classification_seconds)
   qfail=[]
   for role,metrics in a['accepted'].items():
    for metric in ('precision','recall'):
     if metrics[metric] is not None and metrics[metric]<.9:qfail.append(role+':'+metric)
   if a['invalid']:qfail.append('invalid')
   for name,summary in a['boundary_diagnostics'].items():
    if summary['missed']:qfail.append(name)
   qualification[str(n)][split]=dict(passed_numeric_boundary_checks=not qfail,failures=qfail,opaque_manual_review_required=True)
   if not preservation_gate(b,a,0,0,1):issues.append(split+':preservation_metrics')
   if a['exact']<b['exact'] or a['invalid']>b['invalid'] or a['accepted']['all']['f1']<b['accepted']['all']['f1']:issues.append(split+':aggregate')
   for arm in ('raw','accepted'):
    for role in a[arm]:
     for metric in ('precision','recall'):
      old=b[arm][role][metric];new=a[arm][role][metric]
      if old is not None and (new is None or new<old):issues.append(split+':'+arm+':'+role+':'+metric)
   rawrows=read(OUT/str(n)/f'{split}-baseline.json');afterrows=read(OUT/str(n)/f'{split}-contextual.json');audits=read(OUT/str(n)/f'{split}-audit.json')
   for r,raw,after,audit in zip(rows,rawrows,afterrows,audits):
    id=r['question_id'];g=tokens(r['mentions']);p=tokens(b['cases'][id]['raw_mentions']);q=tokens(a['cases'][id]['raw_mentions']);lost=sorted((p&g)-q)
    if lost:issues.append(split+':'+id+':lost_correct')
    untouched=[]
    entities=raw.get('output',{}).get('entities',{})
    flat=[(role,item) for role,items in entities.items() for item in items]
    for role,item in flat:
     overlap=any(other_role!=role and item['start']<other['end'] and other['start']<item['end'] for other_role,other in flat)
     if not overlap and item not in after.get('output',{}).get('entities',{}).get(role,[]):issues.append(split+':'+id+':nonconflicting_span_mutation')
    if not audit['contextual'] and raw!=after:issues.append(split+':'+id+':nonconflict_mutation')
    if audit['contextual'] and a['cases'][id]['exact'] and not b['cases'][id]['exact']:correct_resolutions+=1
    ledger.append(dict(seed=n,split=split,id=id,question=r['question'],gold=sorted(g),before=sorted(p),after=sorted(q),lost_correct=lost,removed_false=sorted((p-g)-q),new_false=sorted((q-g)-p),before_exact=b['cases'][id]['exact'],after_exact=a['cases'][id]['exact']))
  if not correct_resolutions:issues.append('no_correct_resolutions')
  gate.append(dict(seed=n,passed=not issues,issues=issues,correct_resolutions=correct_resolutions))
 write(OUT/'qualification.json',qualification);write(OUT/'latency.json',latency);write(OUT/'scores.json',report);write(OUT/'ledger.json',ledger);write(OUT/'decision.json',dict(passed=all(g['passed'] for g in gate),seeds=gate));print(gate,flush=True)
if __name__=='__main__':main(smoke=sys.argv[1]=='smoke')

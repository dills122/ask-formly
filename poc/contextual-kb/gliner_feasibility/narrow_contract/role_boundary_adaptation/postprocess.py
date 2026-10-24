"""Posthoc descriptive reporting only; never used for training or selection."""
import run
from contract import tokens
train,splits,labels=run.inputs();scores=run.read(run.OUT/'final-scores.json')
ledger=[];boundaries=[];qualifications={}
# Explicit posthoc inventory of all opaque code values, including non-arrow
# expressions, array/object literals and the quoted !model.enabled expression.
# This categorizes gold for reporting only; never used for model extraction.
opaque_ids={'fresh':{'rbf-31','rbf-32','rbf-33','rbf-34','rbf-35'},'vocab':{'va-f06-q04'},'target':{'fresh-flat-016','fresh-flat-018','fresh-flat-036'},'challenge':set(),'olddev':{'V12'}}
for seed in ('1701','1702'):
 failures=[]
 for split,rows in splits.items():
  before=scores['before'][seed][split];after=scores['after'][seed][split]
  if after['invalid']:failures.append(dict(split=split,criterion='invalid',count=after['invalid']))
  for role,m in after['accepted'].items():
   if m['tp']+m['fn'] and (run.rate(m['precision'])<.9 or run.rate(m['recall'])<.9):failures.append(dict(split=split,criterion='accepted_role_precision_recall',role=role,precision=m['precision'],recall=m['recall']))
  for row in rows:
   id=row['question_id'];g=tokens(row['mentions']);b=before['cases'][id];a=after['cases'][id]
   entry=dict(seed=seed,split=split,id=id,question=row['question'],before_exact=b['exact'],after_exact=a['exact'],regressed=b['exact'] and not a['exact'],improved=not b['exact'] and a['exact'],before_error=b['error'],after_error=a['error'])
   for arm in ('raw','accepted'):
    p=tokens(b['raw_mentions'] if arm=='raw' else b['envelope']['mentions']);q=tokens(a['raw_mentions'] if arm=='raw' else a['envelope']['mentions'])
    entry[arm]=dict(new_correct=sorted((q&g)-p),lost_correct=sorted((p&g)-q),new_false_positives=sorted((q-g)-p),removed_false_positives=sorted((p-g)-q),remaining_misses=sorted(g-q),remaining_false_positives=sorted(q-g))
   ledger.append(entry)
   raw=tokens(a['raw_mentions']);accepted=tokens(a['envelope']['mentions'])
   for s in g:
    kind,start,end,text=s
    categories=[]
    if kind=='api_reference' and ('.' in text or '[' in text):categories.append('compound_api')
    if kind in ('registration_name','model_key','value') and text[:1] in ('"',"'"):categories.append('quoted_name_key_value')
    if kind=='value' and id in opaque_ids[split]:categories.append('opaque_expression')
    for category in categories:
     boundaries.append(dict(seed=seed,split=split,id=id,category=category,gold=list(s),raw_exact=s in raw,accepted_exact=s in accepted))
     if s not in accepted:failures.append(dict(split=split,id=id,criterion='boundary',category=category,gold=list(s)))
 qualifications[seed]=dict(qualified=not failures,failures=failures)
run.write(run.OUT/'case-ledger.json',ledger)
run.write(run.OUT/'boundary-ledger.json',boundaries)
run.write(run.OUT/'qualification.json',qualifications)
print('ledger',len(ledger),'boundaries',len(boundaries),'qualified',{s:r['qualified'] for s,r in qualifications.items()})

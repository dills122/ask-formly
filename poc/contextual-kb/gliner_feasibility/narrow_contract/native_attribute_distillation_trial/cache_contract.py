"""Fail-closed cached-teacher occurrence/probability/provenance validation."""
import math
ROLES=('api_reference','registration_name','model_key','value','version','ui_adapter','no_entity')
def targets(row,bad):
 if row['question_id']!=bad['question_id']:raise ValueError('training identity')
 result=[dict(start=m['start'],end=m['end'],role=m['kind']) for m in row['mentions']]+[dict(start=m['start'],end=m['end'],role='no_entity') for m in bad['negatives']]
 if len({(m['start'],m['end']) for m in result})!=len(result):raise ValueError('duplicate target')
 return sorted(result,key=lambda x:(x['start'],x['end']))
def validate(cache,identity,rows,bad):
 if cache['identity']!=identity or len(cache['records'])!=len(rows) or len(bad)!=len(rows):raise ValueError('cache identity')
 for c,r,b in zip(cache['records'],rows,bad):
  if c['question_id']!=r['question_id'] or c['question']!=r['question']:raise ValueError('question identity')
  expected=targets(r,b);actual=c['targets']+c['unsupported']
  if sorted(actual,key=lambda x:(x['start'],x['end']))!=expected or len(c['targets'])!=len(c['probabilities']) or len(c['mask'])!=len(c['targets']):raise ValueError('occurrence identity')
  for g,p,mask in zip(c['targets'],c['probabilities'],c['mask']):
   if len(p)!=7 or any(not math.isfinite(x) or x<0 or x>1 for x in p) or abs(sum(p)-1)>1e-5:raise ValueError('probability integrity')
   winner=max(range(7),key=lambda i:p[i]);correct=ROLES[winner]==g['role'] and p[winner]>.5
   if type(mask)!=bool or mask!=correct:raise ValueError('teacher correctness mask')
 return cache

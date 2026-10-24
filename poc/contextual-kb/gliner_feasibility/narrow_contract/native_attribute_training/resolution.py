"""Keep original boundaries and unresolved records; only resolve identical spans."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('prior_span_resolution',Path(__file__).resolve().parent.parent/'span_role_feasibility/policy.py');prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
def resolve_scores(question,row,scores):
 choices={};lookup={}
 for s in scores:
  key=(s['start'],s['end']);lookup[key]=s
  if s['status']=='scored':choices[key]=prior.select({s['label']:s['confidence']})
 result,logs=prior.resolve(question,row,choices)
 for log in logs:
  candidates=log.get('candidates',[])
  if not candidates:continue
  keys={(s['start'],s['end']) for s in candidates}
  if len(keys)!=1:continue
  key=next(iter(keys));s=lookup.get(key)
  log['attribute_score']=s
  log['attribute_decision']='missing' if s is None else 'unaligned' if s['status']!='scored' else 'low_confidence' if choices.get(key) is None else 'learned_no_entity' if choices[key]=='no_entity' else 'role'
 return result,logs

"""Aggregate all scheduled slots; semantic judgments come only from independent review."""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'refinement_v3'))
from candidate import validate,build_plan

def summarize(cases,records,grades=None):
 ids=[c['id'] for c in cases]
 if len(ids)!=len(set(ids)):raise ValueError('Duplicate case')
 expected={(i,r) for i in ids for r in (1,2,3)}
 def index(rows):
  out={}
  for row in rows:
   k=(row['id'],row['run'])
   if k not in expected or k in out:raise ValueError('Unexpected or duplicate slot')
   out[k]=row
  return out
 saved=index(records);judgments=None if grades is None else index(grades)
 if judgments is not None:
  if set(judgments)!=expected:raise ValueError('Incomplete semantic review')
  for g in judgments.values():
   if type(g['semantic_pass']) is not bool or type(g['binding_pass']) is not bool:raise ValueError('Nonboolean judgment')
 rows=[];exact=0;all_good=0
 for case in cases:
  values=[];good=[]
  for run in (1,2,3):
   k=case['id'],run;output=saved.get(k,{}).get('output');error=None
   try:
    validate(case['request'],output)
    base=build_plan(case['request'],output)
    noisy=build_plan(case['request'],output,{'malformed':'hints'})
    if any(base[key]!=noisy[key] for key in ('question_plan','search_requests')):raise ValueError('Hint changed core plan')
   except (ValueError,TypeError,KeyError) as e:error=str(e)
   structural=error is None
   g=None if judgments is None else judgments[k]
   usable=None if g is None else structural and g['semantic_pass'] and g['binding_pass']
   rows.append(dict(id=case['id'],batch=case['batch'],run=run,structural=structural,error=error,usable=usable))
   good.append(usable)
   values.append(None if output is None else json.dumps(output,sort_keys=True,ensure_ascii=False,separators=(',',':')))
  exact+=all(v is not None for v in values) and len(set(values))==1
  all_good+=all(v is True for v in good)
 return dict(slots=len(expected),structural=sum(r['structural'] for r in rows),usable=None if judgments is None else sum(r['usable'] for r in rows),all_three_usable=None if judgments is None else all_good,exact_equal_cases=exact,rows=rows)

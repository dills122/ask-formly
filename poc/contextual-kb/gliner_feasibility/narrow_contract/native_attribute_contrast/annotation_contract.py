"""Offline explicit annotation transport; never used to label runtime spans."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('contrast_annotation',Path(__file__).resolve().parent.parent/'challenge_adaptation/experiment.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
build=module.annotation
FAMILIES={'clipped_api','merged_api_value','nested_fragment','quote_error','ordinary_prose'}
def negatives(row,specs):
 text=row['question'];gold={(m['start'],m['end']) for m in row['mentions']};result=[];seen=set()
 for raw,occurrence,family in specs:
  if not raw or family not in FAMILIES:raise ValueError('negative specification')
  starts=[];i=text.find(raw)
  while i>=0:starts.append(i);i=text.find(raw,i+1)
  if occurrence is None:
   if len(starts)!=1:raise ValueError('ambiguous anchor')
   occurrence=0
  if type(occurrence)!=int or not 0<=occurrence<len(starts):raise ValueError('missing anchor')
  a=starts[occurrence];b=a+len(raw)
  if (a,b) in gold or (a,b) in seen:raise ValueError('gold or duplicate negative')
  seen.add((a,b));result.append(dict(text=raw,start=a,end=b,family=family))
 return result

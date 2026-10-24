"""Freeze schedules/exposure from existing training-only records."""
import json
from pathlib import Path
from collections import Counter
from schedule import schedule
HERE=Path(__file__).parent;OUT=HERE/'test-output';OLD=HERE.parent/'native_attribute_contrast/test-output'
def read(p):return json.loads(p.read_text())
def main():
 rows=read(OUT/'train.json');bad=read(OUT/'training-negatives.json')
 assert rows==read(OLD/'train.json') and bad==read(OLD/'training-negatives.json')
 assert len(rows)==242 and sum(len(b['negatives']) for b in bad)==534
 plans={};exposure={}
 for n in (1701,1702):
  plans[str(n)]={};exposure[str(n)]={}
  for arm in ('control','treatment'):
   plan=schedule(n,arm);plans[str(n)][arm]=plan;counts=Counter();families=Counter();weighted=Counter()
   for chunk in plan:
    for i,w in chunk:
     counts[rows[i]['question_id']]+=1
     for negative in bad[i]['negatives']:
      family=negative.get('family',negative.get('invalid_family','unspecified'));families[family]+=1;weighted[family]+=w/8
   exposure[str(n)][arm]=dict(examples=sum(counts.values()),question_counts=counts,negative_family_exposures=families,negative_family_loss_weight_coefficients=weighted,total_loss_weight=sum(w/8 for chunk in plan for i,w in chunk),shared_replay_examples=868,contrast_examples=124 if arm=='treatment' else 0)
 for name,value in [('schedules.json',plans),('exposure.json',exposure)]:
  with (OUT/name).open('x') as f:json.dump(value,f,indent=2)
 print(json.dumps({s:{a:{k:v for k,v in d.items() if k!='question_counts'} for a,d in arms.items()} for s,arms in exposure.items()},indent=2))
if __name__=='__main__':main()

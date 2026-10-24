"""Deterministic feature coverage from authorized training rows only."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'native_attribute_contrast/test-output';OUT=HERE/'test-output'
def read(p):return json.loads(p.read_text())
def main():
 rows=read(OLD/'train.json')[:194];bad=read(OLD/'training-negatives.json')[:194]
 assert len(rows)==194 and sum(len(b['negatives']) for b in bad)==449
 features=[]
 for r,b in zip(rows,bad):
  assert r['question_id']==b['question_id'];raw=[m['raw'] for m in r['mentions']]
  features.append({m['kind'] for m in r['mentions']}|{'negative:'+x['family'] for x in b['negatives']}|({'repeated_raw'} if len(raw)!=len(set(raw)) else set()))
 required=set.union(*features);seen=set();selected=[]
 for i,f in enumerate(features):
  if f-seen:selected.append(i);seen|=f
 assert required==seen and len(selected)<=16
 for i in range(len(rows)):
  if len(selected)>=8:break
  if i not in selected:selected.append(i)
 selected=sorted(selected)
 result=dict(source_count=194,source_negative_count=449,selection='first source row adding uncovered gold role, negative family or repeated raw string; pad to8 source-order rows; max16',indices=selected,features=sorted(seen),rows=[dict(row=rows[i],negative=bad[i]) for i in selected])
 with (OUT/'panel.json').open('x') as f:json.dump(result,f,indent=2)
 print({k:v for k,v in result.items() if k!='rows'})
if __name__=='__main__':main()

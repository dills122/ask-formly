"""Serialize annotated training data before fresh-data exposure."""
import json
from pathlib import Path
from annotation_contract import build,negatives
from training_annotations import ROWS
HERE=Path(__file__).resolve().parent;NARROW=HERE.parent;OUT=HERE/'test-output'
def write(p,x):
 with p.open('x') as f:json.dump(x,f,indent=2)
def main():
 old=json.loads((NARROW/'role_boundary_adaptation/test-output/train.json').read_text());oldbad=json.loads((NARROW/'native_attribute_training/test-output/ordered-smoke/training-negatives.json').read_text());new=[];bad=[]
 assert len(ROWS)==48 and len(old)==194
 for i,(family,marked,ns) in enumerate(ROWS,1):
  row=build(f'contrast-train-{i:02}',marked);new.append(row);bad.append(dict(question_id=row['question_id'],family=family,negatives=negatives(row,ns)))
 allrows=old+new;allbad=oldbad+bad
 assert len({r['question_id'] for r in allrows})==242 and len({r['question'] for r in allrows})==242
 assert all(a['question_id']==b['question_id'] for a,b in zip(allrows,allbad))
 write(OUT/'train-new.json',new);write(OUT/'new-negatives.json',bad);write(OUT/'train.json',allrows);write(OUT/'training-negatives.json',allbad)
 print('train',len(allrows),'new_negative',sum(len(r['negatives']) for r in bad),'all_negative',sum(len(r['negatives']) for r in allbad))
if __name__=='__main__':main()

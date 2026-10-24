"""Pre-freeze training-only transport check on both prior candidate checkpoints."""
import sys,json,gc
from pathlib import Path
HERE=Path(__file__).resolve().parent;NARROW=HERE.parent;PRIOR=NARROW/'native_attribute_training'
sys.path.insert(0,str(PRIOR))
from native import load_model,weights,prepare,PeftModel,write
OUT=HERE/'test-output'
def main():
 rows=json.loads((OUT/'train.json').read_text());bad=json.loads((OUT/'training-negatives.json').read_text());results=[]
 for n in (1701,1702):
  model=PeftModel.from_pretrained(load_model(),str(PRIOR/f'test-output/{n}/epoch-6/adapter'),is_trainable=False)
  assert weights(model)==json.loads((PRIOR/f'test-output/{n}/training-receipt.json').read_text())['final_hashes']
  for r,b in zip(rows,bad):
   assert r['question_id']==b['question_id'];prepare(model,r,b['negatives'])
  results.append(dict(seed=n,rows=len(rows),negative_targets=sum(len(b['negatives']) for b in bad),all_exact=True))
  del model;gc.collect()
 write(OUT/'compatibility.json',results);print(results)
if __name__=='__main__':main()

"""Post-run paired audit only; no inference, training, or selection."""
import json
from pathlib import Path
from collections import Counter
OUT=Path(__file__).parent/'test-output'
def selected(row):
 p=row['prediction']
 return p['label'] if p['status']=='scored' and p['confidence']>.5 else None
def main():
 ledger=[];summary={}
 for seed in (1701,1702):
  for group in ('probes','oldprobes'):
   before=json.loads((OUT/str(seed)/f'{group}-before.json').read_text())
   after=json.loads((OUT/str(seed)/f'{group}-after.json').read_text())
   assert len(before)==len(after)
   counts=Counter()
   for a,b in zip(before,after):
    for key in ('question_id','start','end','text','expected_role'):
     assert a[key]==b[key],key
    x,y=selected(a),selected(b);gold=a['expected_role'];was=x==gold;now=y==gold
    transition='retained_correct' if was and now else 'lost_correct' if was else 'gained_correct' if now else 'still_incorrect'
    counts[transition]+=1
    ledger.append(dict(seed=seed,group=group,question_id=a['question_id'],start=a['start'],end=a['end'],text=a['text'],expected_role=gold,invalid_family=a.get('invalid_family'),before=x,after=y,before_prediction=a['prediction'],after_prediction=b['prediction'],transition=transition))
   summary[f'{seed}:{group}']=dict(counts)
 (OUT/'probe-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
 (OUT/'probe-transitions.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()

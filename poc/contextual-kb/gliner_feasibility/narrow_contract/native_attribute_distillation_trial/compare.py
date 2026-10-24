"""Complete paired correctness audit; no training or model selection."""
from run import *
from effect import selected,superiority
from contract import tokens
from collections import Counter

def main():
 scores=read(OUT/'scores.json');ledger=[];summary={};historical=[]
 for n in (1701,1702):
  folder=OUT/str(n)
  for group in ('probes','oldprobes','contrastprobes','retentionprobes'):
   arms={arm:read(folder/f'{group}-{arm}.json') for arm in ('before','control','treatment')}
   assert len({len(x) for x in arms.values()})==1
   for idx,b in enumerate(arms['before']):
    for left,right in (('before','control'),('before','treatment'),('control','treatment')):
     a,c=arms[left][idx],arms[right][idx]
     assert all(a[k]==c[k] for k in ('question_id','start','end','text','expected_role'))
     x,y=selected(a['prediction']),selected(c['prediction']);gold=a['expected_role']
     ledger.append(dict(seed=n,source='probe',group=group,fresh=group=='probes',comparison=f'{left}:{right}',question_id=a['question_id'],start=a['start'],end=a['end'],text=a['text'],expected_role=gold,before=x,after=y,before_prediction=a['prediction'],after_prediction=c['prediction'],before_correct=x==gold,after_correct=y==gold))
   if group!='probes':
    oldpath=RETENTION/f'test-output/{n}/{"probes" if group=="retentionprobes" else group}-treatment.json';old=read(oldpath)
    for arm in ('control','treatment'):
     for a,b in zip(old,arms[arm]):
      assert (a['question_id'],a['start'],a['end'])==(b['question_id'],b['start'],b['end'])
      historical.append(dict(seed=n,arm=arm,source='probe',group=group,question_id=b['question_id'],start=b['start'],end=b['end'],text=b['text'],expected_role=b['expected_role'],contrast_prediction=a['prediction'],current_prediction=b['prediction'],contrast_correct=selected(a['prediction'])==b['expected_role'],current_correct=selected(b['prediction'])==b['expected_role']))
  for split,rows in splits().items():
   endpoints={arm:read(folder/f'{split}-{arm}.json') for arm in ('before','control','treatment')}
   for idx,r in enumerate(rows):
    gold=tokens(r['mentions'])
    for left,right in (('before','control'),('before','treatment'),('control','treatment')):
     ca=scores[f'{n}:{right}'][split]['before' if left=='before' else 'after']['cases'][r['question_id']] if left=='before' else scores[f'{n}:{left}'][split]['after']['cases'][r['question_id']]
     cb=scores[f'{n}:{right}'][split]['after']['cases'][r['question_id']]
     lost=sorted((tokens(ca['raw_mentions'])&gold)-tokens(cb['raw_mentions']))
     ledger.append(dict(seed=n,source='operational',group=split,fresh=split=='fresh',comparison=f'{left}:{right}',question_id=r['question_id'],before_correct=ca['exact'],after_correct=cb['exact'],lost_correct_mentions=lost,before_endpoint=endpoints[left][idx],after_endpoint=endpoints[right][idx]))
     if lost:ledger.append(dict(seed=n,source='operational_mention_loss',group=split,fresh=split=='fresh',comparison=f'{left}:{right}',question_id=r['question_id'],before_correct=True,after_correct=False,lost_correct_mentions=lost))
 for row in ledger:
  k=f"{row['seed']}:{row['source']}:{row['group']}:{row['comparison']}";c=summary.setdefault(k,Counter());a=row['before_correct'];b=row['after_correct'];c['retained_correct' if a and b else 'lost_correct' if a else 'gained_correct' if b else 'still_incorrect']+=1
 write(OUT/'paired-ledger.json',ledger);write(OUT/'paired-summary.json',summary);write(OUT/'historical-probe-comparison.json',historical)
 write(OUT/'superiority.json',dict(treatment_superior=superiority([r for r in ledger if r['comparison']=='control:treatment']),definition='No lost correct outcome or mention anywhere; at least one fresh correct gain for each seed. No_entity requires a scored confidence above0.5.'))
if __name__=='__main__':main()

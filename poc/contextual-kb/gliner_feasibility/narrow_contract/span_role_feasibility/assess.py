"""Post-inference paired scoring. Gold is used here, never in resolution."""
from run import HERE,NARROW,OUT,read,splits,write
from policy import resolve,native_choices
from score import evaluate
from contract import tokens

def main():
 report={};ledger=[];gates=[];typing=[];audit=[]
 for seed in (1701,1702):
  report[str(seed)]={};issues={a:[] for a in ('native','spacy')};correct={a:0 for a in issues}
  for split,rows in splits().items():
   folder=OUT/str(seed);baseline=read(folder/f'{split}-baseline.json');native=read(folder/f'{split}-native.json');spacy=read(folder/f'{split}-spacy.json')
   if len({len(rows),len(baseline),len(native),len(spacy)})!=1:raise ValueError('output count')
   arms={'baseline':baseline,'native':[],'spacy':[]};logs={a:[] for a in issues}
   for r,b,n,s in zip(rows,baseline,native,spacy):
    if not r['question_id']==b['id']==n['id']==s['id']:raise ValueError('id')
    choices={'native':native_choices(r['question'],n.get('output',{})),'spacy':{(x['start'],x['end']):x['selected'] for x in s['rows']}}
    for arm in issues:
     result,log=resolve(r['question'],b,choices[arm]);arms[arm].append(result);logs[arm].append(log)
    gold={(m['start'],m['end']):m['kind'] for m in r['mentions']};baseoffsets={(x['start'],x['end']) for xs in b.get('output',{}).get('entities',{}).values() for x in xs};nativeoffsets={(x['start'],x['end']) for xs in n.get('output',{}).get('entities',{}).values() for x in xs}
    audit.append(dict(seed=seed,split=split,id=b['id'],baseline_spans=sorted(baseoffsets),native_spans=sorted(nativeoffsets),dropped=sorted(baseoffsets-nativeoffsets),added=sorted(nativeoffsets-baseoffsets),spacy_alignment_failures=s['alignment_failures'],native_error=n.get('error'),native_seconds=n['seconds'],spacy_seconds=s['seconds']))
    for arm in issues:
     for span in sorted(baseoffsets|set(gold)):
      typing.append(dict(seed=seed,split=split,id=b['id'],arm=arm,start=span[0],end=span[1],text=r['question'][span[0]:span[1]],gold=gold.get(span,'no_entity'),selected=choices[arm].get(span),available=span in choices[arm]))
   qs=[dict(id=r['question_id'],question=r['question'],family=split,origin=split,parent=r['question_id']) for r in rows];goldmap={r['question_id']:r for r in rows}
   scores={arm:evaluate(qs,goldmap,out) for arm,out in arms.items()};report[str(seed)][split]=scores;b=scores['baseline']
   for arm in issues:
    a=scores[arm]
    if a['exact']<b['exact'] or a['invalid']>b['invalid'] or a['accepted']['all']['f1']<b['accepted']['all']['f1']:issues[arm].append(split+':aggregate')
    for layer in ('raw','accepted'):
     for role in b[layer]:
      for metric in ('precision','recall'):
       old=b[layer][role][metric];new=a[layer][role][metric]
       if old is not None and (new is None or new<old):issues[arm].append(split+':'+layer+':'+role+':'+metric)
    for r,raw,after,log in zip(rows,baseline,arms[arm],logs[arm]):
     id=r['question_id'];g=tokens(r['mentions']);p=tokens(b['cases'][id]['raw_mentions']);q=tokens(a['cases'][id]['raw_mentions']);lost=sorted((p&g)-q)
     if lost:issues[arm].append(split+':'+id+':lost_correct')
     entries=[(role,x) for role,xs in raw.get('output',{}).get('entities',{}).items() for x in xs]
     for role,x in entries:
      if not any(role!=other and x['start']<y['end'] and y['start']<x['end'] for other,y in entries) and x not in after.get('output',{}).get('entities',{}).get(role,[]):issues[arm].append(split+':'+id+':nonconflict_mutation')
     if not log and raw!=after:issues[arm].append(split+':'+id+':nonconflict_row')
     for item in log:
      if item['decision']=='resolved':
       cand=item['candidates'];start,end=cand[0]['start'],cand[0]['end'];correct_role=next((m['kind'] for m in r['mentions'] if (m['start'],m['end'])==(start,end)),None)
       if item['selected']==correct_role and not lost:correct[arm]+=1
     ledger.append(dict(seed=seed,split=split,id=id,arm=arm,question=r['question'],gold=sorted(g),before=sorted(p),after=sorted(q),lost_correct=lost,removed_false=sorted((p-g)-q),new_false=sorted((q-g)-p),before_exact=b['cases'][id]['exact'],after_exact=a['cases'][id]['exact'],resolution=log))
    write(folder/f'{split}-{arm}-resolved.json',arms[arm])
  for arm in issues:
   if not correct[arm]:issues[arm].append('no_correct_resolutions')
   gates.append(dict(seed=seed,arm=arm,passed=not issues[arm],issues=issues[arm],correct_resolutions=correct[arm]))
 write(OUT/'scores.json',report);write(OUT/'ledger.json',ledger);write(OUT/'typing.json',typing);write(OUT/'audit.json',audit);write(OUT/'decision.json',dict(arms={arm:all(g['passed'] for g in gates if g['arm']==arm) for arm in issues},gates=gates));print(gates)
if __name__=='__main__':main()

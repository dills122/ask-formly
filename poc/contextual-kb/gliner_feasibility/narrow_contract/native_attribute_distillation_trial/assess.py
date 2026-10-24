"""Gold joins only after inference; all occurrence changes audited."""
from run import *
from score import evaluate
from contract import tokens
from collections import Counter
from gate import case_issues,paired_gate

def probe_metrics(rows):
 totals=Counter();families={}
 for p in rows:
  s=p['prediction'];unsupported=s['status']!='scored';selected=None if unsupported or s['confidence']<=.5 else s['label'];valid=p['expected_role']!='no_entity';reject=selected=='no_entity'
  totals['total']+=1;totals['unsupported']+=unsupported;totals['valid' if valid else 'negative']+=1;totals['valid_correct']+=valid and selected==p['expected_role'];totals['valid_accepted']+=valid and selected not in (None,'no_entity');totals['valid_rejected']+=valid and reject;totals['negative_rejected']+=not valid and reject;totals['abstain']+=selected is None;totals['semantic_negative']+=not valid and not unsupported;totals['semantic_negative_rejected']+=not valid and not unsupported and reject
  family=p.get('invalid_family') or 'gold_valid';d=families.setdefault(family,Counter());d['total']+=1;d['unsupported']+=unsupported;d['rejected']+=reject;d['correct']+=selected==p['expected_role']
 denom=totals['negative_rejected']+totals['valid_rejected'];totals=dict(totals)
 totals.update(rejection_precision=totals['negative_rejected']/denom if denom else None,rejection_recall=totals['negative_rejected']/totals['negative'],valid_role_accuracy=totals['valid_correct']/totals['valid'],valid_acceptance_recall=totals['valid_accepted']/totals['valid'],semantic_rejection_recall=totals['semantic_negative_rejected']/totals['semantic_negative'] if totals['semantic_negative'] else None)
 return dict(totals=totals,families=families)
def main():
 data=splits();report={};ledger=[];gates=[];probes={};prior_metric_changes=[]
 for n,arm in ((n,a) for n in (1701,1702) for a in ('control','treatment')):
  report[str(n)+':'+arm]={};folder=OUT/str(n);issues=[];correct=0;wrong=0;counts=Counter()
  for split,rows in data.items():
   b=read(folder/f'{split}-baseline.json');prior=read(folder/f'{split}-before.json');post=read(folder/f'{split}-{arm}.json');qs=[dict(id=r['question_id'],question=r['question'],family=split,origin=split,parent=r['question_id']) for r in rows];gold={r['question_id']:r for r in rows}
   arms={'baseline':b,'before':[r['resolved'] for r in prior],'after':[r['resolved'] for r in post]}
   if split!='fresh':arms['historical_retention_treatment']=[r['resolved'] for r in read(RETENTION/f'test-output/{n}/{"fresh" if split=="retention" else split}-treatment.json')]
   sc={k:evaluate(qs,gold,v) for k,v in arms.items()};report[str(n)+':'+arm][split]=sc;old=sc['baseline'];new=sc['after']
   if new['invalid']>old['invalid']:issues.append(split+':invalid_increase')
   for role in old['accepted']:
    for metric in ('precision','recall','f1'):
     x=old['accepted'][role][metric];y=new['accepted'][role][metric]
     if x is not None and (y is None or y<x-1e-12):issues.append(split+':'+role+':'+metric)
   for role in sc['before']['accepted']:
    for metric in ('precision','recall','f1'):
     x=sc['before']['accepted'][role][metric];y=new['accepted'][role][metric]
     if x!=y:prior_metric_changes.append(dict(seed=n,arm=arm,split=split,role=role,metric=metric,previous=x,current=y))
   for r,raw,after in zip(rows,b,post):
    id=r['question_id'];g=tokens(r['mentions']);p=tokens(old['cases'][id]['raw_mentions']);q=tokens(new['cases'][id]['raw_mentions']);previous=sc['before']['cases'][id];prev_tokens=tokens(previous['raw_mentions']);lost=sorted((p&g)-q)
    for issue in case_issues(g,p,prev_tokens,q,previous['exact'],bool(old['cases'][id]['error']),bool(new['cases'][id]['error']),new['cases'][id]['exact']):issues.append(split+':'+id+':'+issue)
    if lost:issues.append(split+':'+id+':lost_correct')
    entries=[(role,x) for role,xs in raw['output']['entities'].items() for x in xs]
    for role,x in entries:
     if not any(role!=other and x['start']<y['end'] and y['start']<x['end'] for other,y in entries) and x not in after['resolved']['output']['entities'].get(role,[]):issues.append(split+':'+id+':nonconflict_change')
    # Invalid-to-valid must be wholly exact, not a structurally clean wrong answer.
    wasinvalid=bool(old['cases'][id].get('error'));nowinvalid=bool(new['cases'][id].get('error'))
    for log in after['resolution']:
     counts[log['decision']]+=1;counts[log.get('attribute_decision','not_applicable')]+=1
     if log['decision']=='resolved':
      c=log['candidates'][0];expected=next((m['kind'] for m in r['mentions'] if (m['start'],m['end'])==(c['start'],c['end'])),None)
      if log['selected']==expected and not lost:correct+=1
      else:wrong+=1;issues.append(split+':'+id+':wrong_resolution')
    if wasinvalid and not nowinvalid and not new['cases'][id]['exact']:issues.append(split+':'+id+':invalid_to_valid_wrong')
    if after['resolution'] or p!=q or prev_tokens!=q:ledger.append(dict(seed=n,arm=arm,split=split,id=id,question=r['question'],gold=sorted(g),before=sorted(p),after=sorted(q),lost_correct=lost,before_case=old['cases'][id],previous_case=previous,after_case=new['cases'][id],resolution=after['resolution']))
  if not correct:issues.append('no_correct_resolution')
  probes[str(n)+':'+arm]={name:{phase:probe_metrics(read(folder/f'{name}-{arm if phase=="after" else phase}.json')) for phase in ('before','after')} for name in ('probes','oldprobes','contrastprobes','retentionprobes')}
  for probe_group in ('oldprobes','contrastprobes','retentionprobes'):
   before_probes=read(folder/f'{probe_group}-before.json');after_probes=read(folder/f'{probe_group}-{arm}.json')
   assert len(before_probes)==len(after_probes)
   for a,bp in zip(before_probes,after_probes):
    ap=a['prediction'];cp=bp['prediction'];selected_before=None if ap['status']!='scored' or ap['confidence']<=.5 else ap['label'];selected_after=None if cp['status']!='scored' or cp['confidence']<=.5 else cp['label']
    if selected_before==a['expected_role'] and selected_after!=a['expected_role']:issues.append(probe_group+':'+a['question_id']+':'+str(a['start'])+':previous_correct_lost')
  gates.append(dict(seed=n,arm=arm,passed=not issues,issues=issues,correct_resolutions=correct,wrong_resolutions=wrong,decisions=counts))
 qualification=[]
 for n,arm in ((n,a) for n in (1701,1702) for a in ('control','treatment')):
  failures=[];g=next(g for g in gates if g['seed']==n and g['arm']==arm);p=probes[str(n)+':'+arm]['probes']['after']['totals']
  if g['wrong_resolutions']:failures.append('wrong_resolutions')
  if p['rejection_recall']<.9:failures.append('rejection_recall_below_90')
  if p['valid_rejected']:failures.append('valid_spans_rejected')
  for group in ('oldprobes','contrastprobes','retentionprobes'):
   oldp=probes[str(n)+':'+arm][group]['after']['totals']
   if oldp['rejection_recall']<.9 or oldp['valid_rejected']:failures.append(group+':qualification')
  for split,arms in report[str(n)+':'+arm].items():
   score=arms['after']
   if score['invalid']:failures.append(split+':invalid')
   for role,metrics in score['accepted'].items():
    if metrics['tp']+metrics['fn'] or metrics['fp']:
     if any(metrics[k] is None or metrics[k]<.9 for k in ('precision','recall')):failures.append(split+':'+role+':below_90')
   if any(d['missed'] for d in score['boundary_diagnostics'].values()):failures.append(split+':critical_boundary')
  qualification.append(dict(seed=n,arm=arm,passed=not failures,issues=failures))
 write(OUT/'scores.json',report);write(OUT/'ledger.json',ledger);write(OUT/'probe-scores.json',probes);write(OUT/'prior-metric-changes.json',prior_metric_changes);write(OUT/'decision.json',dict(arms={arm:dict(improvement_passed=paired_gate([g for g in gates if g['arm']==arm]),full_qualification_passed=all(q['passed'] for q in qualification if q['arm']==arm)) for arm in ('control','treatment')},gates=gates,qualification=qualification));print(json.dumps(gates,indent=2))
if __name__=='__main__':main()

"""Fixed occurrence-level entailment diagnostic; no training or serving writes."""
import math
ROLES=('api_reference','registration_name','model_key','value','version','ui_adapter')
HYPOTHESES=(
 'The marked mention directly references a Formly or Angular API property, method, class, or complete code path.',
 'The marked mention is a supplied registration name for a custom field type, wrapper, or validator.',
 'The marked mention is a supplied model key or model path value identifying where field data is stored.',
 'The marked mention is supplied literal content or a complete opaque configuration expression, rather than an API reference, registration name, model key, version, or UI adapter.',
 'The marked mention explicitly identifies a Formly or Angular version.',
 'The marked mention names a Formly UI adapter, including when the adapter is excluded.',
 'The marked mention is ordinary explanatory prose or an incomplete fragment, not a complete API reference, registration name, model key, literal value, version, or UI adapter.'
)
def marked(text,start,end):
 if type(start) is not int or type(end) is not int or not 0<=start<end<=len(text) or '<mention>' in text or '</mention>' in text:raise ValueError('invalid occurrence')
 return text[:start]+'<mention>'+text[start:end]+'</mention>'+text[end:]
def decide(p):
 if len(p)!=7 or any(type(x) not in (int,float) or not math.isfinite(x) or not 0<=x<=1 for x in p):raise ValueError('invalid scores')
 order=sorted(range(7),key=lambda i:p[i],reverse=True);i,j=order[:2]
 reason='low_support' if p[i]<.8 else 'small_margin' if p[i]-p[j]<.2 else 'no_entity' if i==6 else 'accepted'
 return dict(role=ROLES[i] if reason=='accepted' else None,reason=reason,top=p[i],margin=p[i]-p[j])
def simulate(before,scores):
 before={tuple(t) for t in before}; spans={(a,b) for a,b,r in before}
 if set(scores)!=spans:raise ValueError('score coverage differs')
 after=set(before)
 for (a,b),p in scores.items():
  d=decide(p)
  if d['role'] is not None:
   after={t for t in after if t[:2]!=(a,b)};after.add((a,b,d['role']))
 return after

def assess(rows):
 counts=dict(questions=len(rows),gold=0,baseline_correct=0,baseline_extra=0,candidate_correct=0,candidate_extra=0,lost_correct=0,gained_correct=0,wrong_changes=0,corrected_groups=0,abstentions=0,baseline_exact=0,candidate_exact=0)
 ledger=[]
 for row in rows:
  before={tuple(x) for x in row['before']};gold={tuple(x) for x in row['gold']}
  lookup={(s['start'],s['end']):s['p'] for s in row['scores']}
  if len(lookup)!=len(row['scores']):raise ValueError('duplicate scores')
  after=simulate(before,lookup);changes=[]
  for (a,b),p in lookup.items():
   d=decide(p);old={t for t in before if t[:2]==(a,b)};new={t for t in after if t[:2]==(a,b)};expected={t for t in gold if t[:2]==(a,b)}
   counts['abstentions']+=d['role'] is None
   if old!=new:
    correct=new==expected
    counts['corrected_groups']+=correct;counts['wrong_changes']+=not correct
    changes.append(dict(start=a,end=b,text=row['text'][a:b],old=sorted(old),new=sorted(new),expected=sorted(expected),correct=correct,decision=d))
  for name,value in dict(gold=len(gold),baseline_correct=len(before&gold),baseline_extra=len(before-gold),candidate_correct=len(after&gold),candidate_extra=len(after-gold),lost_correct=len((before&gold)-after),gained_correct=len((after&gold)-before),baseline_exact=before==gold,candidate_exact=after==gold).items():counts[name]+=value
  ledger.append(dict(id=row['id'],changes=changes,lost=sorted((before&gold)-after),gained=sorted((after&gold)-before)))
 return dict(**counts,gate_passed=counts['corrected_groups']>0 and counts['wrong_changes']==0 and counts['lost_correct']==0,ledger=ledger)

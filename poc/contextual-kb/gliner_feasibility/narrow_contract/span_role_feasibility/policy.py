"""Occurrence-only conflict resolution. No inferred boundaries or role dictionaries."""
import copy,math
ROLES=('api_reference','registration_name','model_key','value','version','ui_adapter','no_entity')
def select(scores):
 if not scores or set(scores)-set(ROLES):return None
 if any(type(v) not in (int,float) or not math.isfinite(v) or not 0<=v<=1 for v in scores.values()):return None
 ordered=sorted(scores,key=scores.get,reverse=True)
 if scores[ordered[0]]<=.5 or len(ordered)>1 and scores[ordered[0]]==scores[ordered[1]]:return None
 return ordered[0]
def native_choices(question,output):
 grouped={}
 try:
  entities=output['entities']
  if not isinstance(entities,dict) or set(entities)-set(ROLES[:-1]):return {}
  for items in entities.values():
   if not isinstance(items,list):return {}
   for item in items:
    a,b=item['start'],item['end'];key=(a,b)
    if type(a)!=int or type(b)!=int or not 0<=a<b<=len(question) or question[a:b]!=item['text']:return {}
    attr=item.get('target_role',{})
    if not isinstance(attr,dict):return {}
    v=select({attr.get('label'):attr.get('confidence')})
    grouped.setdefault(key,[]).append(v)
 except (KeyError,TypeError,AttributeError):return {}
 return {k:vs[0] if vs and len(set(vs))==1 else None for k,vs in grouped.items()}

def resolve(question,row,choices):
 result=copy.deepcopy(row);audit=[]
 if 'error' in row:return result,audit
 try:
  if set(row['output'])!={'entities'}:raise ValueError('output')
  entities=row['output']['entities'];entries=[]
  if set(entities)-set(ROLES[:-1]):raise ValueError('role')
  for role,items in entities.items():
   for i,item in enumerate(items):
    a,b=item['start'],item['end']
    if type(a)!=int or type(b)!=int or not 0<=a<b<=len(question) or question[a:b]!=item['text']:raise ValueError('span')
    entries.append((role,i,item))
 except Exception as e:return result,[{'decision':'malformed_raw','error':str(e)}]
 pending=set(range(len(entries)));removed=set()
 while pending:
  group={pending.pop()}
  while True:
   more={j for j in pending if any(entries[j][2]['start']<entries[k][2]['end'] and entries[k][2]['start']<entries[j][2]['end'] for k in group)}
   if not more:break
   pending-=more;group|=more
  candidates=[entries[j] for j in sorted(group)]
  if len({r for r,i,s in candidates})<2:continue
  spans={(s['start'],s['end']) for r,i,s in candidates};record={'candidates':[dict(role=r,**s) for r,i,s in candidates],'decision':'abstain'};audit.append(record)
  if len(spans)!=1:record['decision']='partial_overlap';continue
  key=next(iter(spans));selected=choices.get(key)
  if selected not in {r for r,i,s in candidates} or sum(r==selected for r,i,s in candidates)!=1:continue
  for r,i,s in candidates:
   if r!=selected:removed.add((r,i))
  record.update(decision='resolved',selected=selected)
 for role,items in result['output']['entities'].items():result['output']['entities'][role]=[s for i,s in enumerate(items) if (role,i) not in removed]
 return result,audit

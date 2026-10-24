"""Exact occurrence supervision for native qualified attribute queries."""
ROLES=('api_reference','registration_name','model_key','value','version','ui_adapter','no_entity')
def malformed(row):
 text=row['question']; gold={(m['start'],m['end']) for m in row['mentions']};result={}
 def add(a,b,f):
  if 0<=a<b<=len(text) and (a,b) not in gold:result.setdefault((a,b),dict(start=a,end=b,text=text[a:b],family=f))
 ms=sorted(row['mentions'],key=lambda m:(m['start'],m['end']))
 for m in ms:
  a,b=m['start'],m['end'];s=text[a:b]
  if len(s)>2 and s[0] in "'\"" and s[-1]==s[0]:
   add(a+1,b,'broken_quote');add(a,b-1,'broken_quote')
  if m['kind']=='api_reference' and '.' in s:
   dot=s.index('.');add(a,a+dot,'truncated_path');add(a+dot+1,b,'truncated_path')
  if m['kind']=='value' and len(s)>4 and s[0] in '({[':
   add(a+1,b-1,'nested_fragment')
 for left,right in zip(ms,ms[1:]):
  if left['kind']!=right['kind'] and right['start']-left['end']<=15 and right['end']-left['start']<=80:
   add(left['start'],right['end'],'merged_mentions')
 return list(result.values())[:4]
def export(row,bad):
 text=row['question'];entities={r:[] for r in ROLES[:-1]};entities.update({'target_role: '+r:[] for r in sorted(ROLES)})
 def item(s):
  a,b=s['start'],s['end'];raw=s.get('raw',s.get('text'))
  if type(a)!=int or type(b)!=int or not 0<=a<b<=len(text) or text[a:b]!=raw:raise ValueError('invalid exact span')
  return dict(text=raw,start=a,end=b)
 for m in row['mentions']:
  value=item(m);entities[m['kind']].append(value);entities['target_role: '+m['kind']].append(value)
 gold={(m['start'],m['end']) for m in row['mentions']}
 for m in bad:
  if (m['start'],m['end']) in gold:raise ValueError('negative equals gold')
  entities['target_role: no_entity'].append(item(m))
 return dict(input=text,output=dict(entities=entities))

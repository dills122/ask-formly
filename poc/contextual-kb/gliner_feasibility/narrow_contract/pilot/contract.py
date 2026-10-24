"""Strict source-span envelope; no semantic repair or relation inference."""
ROLES=('api_reference','registration_name','model_key','value','version','ui_adapter')
def check_span(span,text):
 a,b=span['start'],span['end']
 if type(a)!=int or type(b)!=int or not 0<=a<b<=len(text):raise ValueError('span bounds')
 if span['raw']!=text[a:b]:raise ValueError('source mismatch')
def validate(e,id,text):
 if not isinstance(e,dict) or set(e)!={'question_id','question','schema_version','mentions','status','issues'}:raise ValueError('envelope shape')
 if e['question_id']!=id or e['question']!=text or e['schema_version']!='narrow-mentions-v1':raise ValueError('identity')
 if e['status'] not in ('ok','needs_review','extraction_error'):raise ValueError('status')
 if not isinstance(e['mentions'],list) or not isinstance(e['issues'],list):raise ValueError('lists')
 end=-1
 for m in e['mentions']:
  if not isinstance(m,dict) or set(m)!={'kind','raw','start','end'} or m['kind'] not in ROLES:raise ValueError('mention')
  check_span(m,text)
  if m['start']<end:raise ValueError('overlap, duplicate or order')
  end=m['end']
 if (e['status']=='ok')!= (len(e['issues'])==0):raise ValueError('status/issues')
 for issue in e['issues']:
  if not isinstance(issue,dict) or set(issue)!={'reason','start','end'}:raise ValueError('issue')
  reasons=('role_ambiguous','boundary_ambiguous') if e['status']=='needs_review' else ('invalid_output','runtime_error')
  if issue['reason'] not in reasons:raise ValueError('issue reason')
  a,b=issue['start'],issue['end']
  if a is None and b is None and e['status']=='extraction_error':continue
  if type(a)!=int or type(b)!=int or not 0<=a<b<=len(text):raise ValueError('issue span')
 return e
def envelope(id,text,mentions,status='ok',reason=None):
 return dict(question_id=id,question=text,schema_version='narrow-mentions-v1',mentions=mentions,status=status,
 issues=[] if reason is None else [dict(reason=reason,start=None,end=None)])
def tokens(mentions):return {(m['kind'],m['start'],m['end'],m['raw']) for m in mentions}
def adapt(id,text,row):
 raw=[]
 try:
  if row is None or 'error' in row:raise ValueError('missing/runtime output')
  output=row['output']
  if not isinstance(output,dict) or set(output)!={'entities'}:raise ValueError('output shape')
  entities=output['entities']
  if not isinstance(entities,dict) or set(entities)-set(ROLES):raise ValueError('entity roles')
  for kind,items in entities.items():
   if not isinstance(items,list):raise ValueError('entity list')
   for s in items:
    m=dict(kind=kind,raw=s['text'],start=s['start'],end=s['end'])
    check_span(m,text);raw.append(m)
  raw.sort(key=lambda m:(m['start'],m['end'],m['kind']))
  result=envelope(id,text,raw);validate(result,id,text)
  return result,raw,None
 except (ValueError,TypeError,KeyError) as error:
  reason='runtime_error' if row is None or 'error' in row else 'invalid_output'
  return envelope(id,text,[],status='extraction_error',reason=reason),raw,str(error)
def counts(pred,gold):return dict(tp=len(pred&gold),fp=len(pred-gold),fn=len(gold-pred))
def metrics(c):
 t,p,n=c['tp'],c['fp'],c['fn']
 return {**c,'precision':t/(t+p) if t+p else None,'recall':t/(t+n) if t+n else None,'f1':2*t/(2*t+p+n) if 2*t+p+n else None}
def score_case(gold,row):
 e,raw,error=adapt(gold['question_id'],gold['question'],row)
 g=tokens(gold['mentions']);p=tokens(raw);a=tokens(e['mentions']) if e['status']=='ok' else set()
 return dict(envelope=e,raw_mentions=raw,error=error,raw=counts(p,g),accepted=counts(a,g),
 exact=error is None and e['status']==gold['status'] and a==g and e['issues']==gold['issues'],
 status_match=e['status']==gold['status'])

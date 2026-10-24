"""Materialize manually chosen occurrences; no automatic semantic labeling."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
# Strings below are manual selections, not regex predictions. Every occurrence of
# each selection is included unless an explicit occurrence role is supplied.
a='api_reference';n='registration_name';k='model_key';v='value';ver='version';ui='ui_adapter'
chosen={
'P02-r1-q0':[("'ratingDial'",n)],
'P04-r1-q0':[("'currencyBadge'",n)],
'P06-r1-q0':[],
'P08-r1-q0':[('key',a)],
'P10-r1-q0':[],
'P12-r1-q0':[('v6.3.12',ver),('Material',ui)],
'P14-r1-q0':[('>=6.2',ver),('<7',ver),('Material',ui),('props.disabled',a)],
'P16-r1-q0':[('v6.3.12',ver),('props.placeholder',a),('Material',ui)],
'P18-r1-q0':[('defaultValue',a),('0',v)],
'P20-r1-q0':[('props.required',a),('valueChanges',a)],
'P22-r1-q0':[('FormControl',a)],
'P24-r1-q0':[('defaultValue',a),("''",v),('false',v),('undefined',v)],
'P26-r1-q0':[('v6.3.12',ver),('Material',ui),('props.required',a),("model.delivery === 'courier'",v)],
'P28-r1-q0':[("expressions['props.disabled']",a),("expressionProperties['templateOptions.disabled']",a),('options.formState.busy',a)],
'P30-r1-q0':[("'remoteCode'",n)],
'P32-r1-q0':[('modelChange',a)],
'P34-r1-q0':[],
'P36-r1-q0':[('v6',ver),('props.placeholder',a),('options.formState.region',a)],
'P38-r1-q0':[('Bootstrap',ui)],
'P40-r1-q0':[],
'P42-r1-q0':[('resetOnHide',a),('false',v),('true',v),('0',v)],
'P44-r1-q0':[('pauseExpressionsNow',a)],
'P46-r1-q0':[('resetOnHide',a),('undefined',v),('false',v)],
'P48-r1-q0':[],
'I01-q0':[('6.3.12',ver),('Material',ui),("'ssn-entry'",n)],
'I01-q1':[('6.3.12',ver),('Material',ui),("'ssn-entry'",n),('key',a),("'taxId'",k)],
'I02-q0':[], 'I02-q1':[],
'I03-q0':[('v6',ver),('props.disabled',a),('hide',a),('resetOnHide',a),('false',v)],
'I03-q1':[('v6',ver),('defaultValue',a),('undefined',v)],
'I04-q0':[("'audit-frame'",n)],
'I04-q1':[("'audit-frame'",[n,k]),('key',a)],
'I05-q0':[("expressions['props.required']",a),('model.needsReview',a)],
'I05-q1':[("expressions['props.required']",a),('model.needsReview',a)],
'I06-q0':[('options.fieldChanges',a)],'I06-q1':[],
'I07-q0':[('Bootstrap',ui),('Material',ui),('props.placeholder',a),("'Choose a region'",v),('key',a),("'regionCode'",k)],
'I08-q0':[("'positiveAmount'",[n,None]),("validation.messages['positiveAmount']",a)],
'I09-q0':[('refreshFieldOptionsNow',a)],'I09-q1':[('refreshFieldOptionsNow',a)],
'I10-q0':[('defaultValue',a),('0',v),('null',v)],
'I11-q0':[], 'I11-q1':[], 'I12-empty':[]}
rows=json.loads((HERE/'annotation-inputs.json').read_text())
assert set(chosen)=={r['id'] for r in rows}
for row in rows:
 spans=[]
 for text,role in chosen[row['id']]:
  offsets=[];start=0
  while (i:=row['text'].find(text,start))>=0:offsets.append(i);start=i+len(text)
  assert offsets,(row['id'],text)
  roles=role if isinstance(role,list) else [role]*len(offsets)
  assert len(roles)==len(offsets)
  for start,kind in zip(offsets,roles):
   if kind:spans.append(dict(start=start,end=start+len(text),text=text,role=kind))
 spans.sort(key=lambda m:m['start'])
 assert all(x['end']<=y['start'] for x,y in zip(spans,spans[1:])),row['id']
 row.update(gold=spans,alternatives=[],rationale='Manual occurrence labels under frozen six-role definitions; no extractor outputs seen.')
(HERE/'gold-initial.json').write_text(json.dumps(rows,indent=2))
print(len(rows),'annotation rows',sum(len(r['gold']) for r in rows),'mentions')

"""Independent re-annotation under v2; preserves the frozen v1 files."""
import copy
import json
from pathlib import Path
base=Path(__file__).resolve().parent
rows=copy.deepcopy(json.loads((base/'annotator-two.json').read_text()))
def span(q,text,occurrence=1):
 start=-1
 for _ in range(occurrence): start=q.index(text,start+1)
 return dict(text=text,start=start,end=start+len(text))
def replace_refs(row):
 q=row['question']
 for a in row['aspects']:
  for key in ['references','unresolved_references']:
   a[key]=[dict(text='its',start=x['start'],end=x['start']+3) if x['text'].startswith('its ') else x for x in a[key]]
 for rel in row['relations']:
  x=rel['head']
  if rel['kind']=='refers_to' and x['text'].startswith('its '): rel['head']=dict(text='its',start=x['start'],end=x['start']+3)
def cue(row,i,*specs):
 row['aspects'][i]['request_cues']=[span(row['question'],*(x if isinstance(x,tuple) else (x,))) for x in specs]
def target(row,i,*texts):
 a=row['aspects'][i]
 a['targets']=[span(row['question'],t) for t in texts]
 a['target_anchor']=min(a['targets'],key=lambda x:x['start'])
for row in rows:
 replace_refs(row)
 n=int(row['id'][1:])
 if n==1:
  row['rationale']='Two independent handling outcomes share the disabled-field condition and discontinuous how are / handled cues. Both minimal its references resolve to a field.'
 elif n==2:
  row['rationale']='Two preservation outcomes share the resetOnHide assignment and hiding action. Does and preserve are separated by setup text. Minimal possessives resolve to the field; false is a value.'
 elif n==3:
  row['rationale']='Two persistence questions share the reload condition. Each can / survive cue is interrupted by its own target.'
 elif n==4:
  for a in row['aspects']: a['conditions']=[]
  cue(row,0,'explain registration')
  cue(row,1,'explain','removal')
  row['rationale']='Registration and removal are separate operations sharing the wrapper anchor. Explain applies to both, but is adjacent only to registration. For the wrapper is topical rather than conditional.'
 elif n==5:
  cue(row,0,'How can I hide')
  row['rationale']='One hiding request is explicitly constrained by without clearing its value. Minimal its refers to the field; the adjacent interrogative and operation form one cue.'
 elif n==6:
  cue(row,0,'How can I clear')
  row['rationale']='One clearing request excludes hiding the field. The final it resolves to a field; its offset excludes the incidental letters inside without.'
 elif n==7:
  cue(row,0,'Can I disable')
  row['rationale']='One validation-disabling request has a whole coordinated without constraint. Minimal its refers to the control. Generic control and validation are not API identifiers.'
 elif n==8:
  cue(row,0,'How do I keep')
  row['rationale']='Two independent requested outcomes share when hidden. The second uses the shared How do I prefix plus retain, and alone carries not retain the control. The omitted hidden subject is treated as generic setup, not an explicit unresolved reference.'
 elif n==9:
  row['aspects'][0]['references']=[]
  row['aspects'][0]['resolved_antecedents']=[]
  row['relations']=[r for r in row['relations'] if r['kind']!='refers_to']
  row['rationale']='One question asks which supplied values are used, under two explicit paired assignments. Supplied values is a relative description rather than a reference label. Which and are used are separated by the target.'
 elif n==10:
  cue(row,0,'How do I type')
  row['rationale']='The whole generic API expression is the target. Both MyProps occurrences, including its nested occurrence, and caféLabel are custom identifiers attached to the aspect. The when clause is setup.'
 elif n==11:
  row['rationale']='One comparison jointly targets the first and second fields. The two with-key conditions identify their respective targets. Repeated key/literal occurrences retain distinct has_value pairings.'
 elif n==12:
  row['rationale']='One property-location question uses where does / appear around the target. Given introduces inline setup. This configuration resolves forward to the inline object. Literal pairings use actual object-key spans, and the final property path remains whole.'
 elif n==13:
  cue(row,0,'how do I add')
  row['aspects'][0]['conditions']=[span(row['question'],'to an input')]
  row['rationale']='One suffix-addition request has version and adapter scope only in their dedicated fields. To an input retains destination context as a condition; the target is the smallest complete suffix noun phrase. This destination-versus-condition boundary remains borderline.'
 elif n==14:
  cue(row,0,'how do I set')
  cue(row,1,'how do I show')
  for a in row['aspects']: a['conditions']=[]
  row['rationale']='Setting the placeholder and showing validation messages are independent operations. Both retain the version and adapter in dedicated scope fields without duplicate conditions.'
 elif n==15:
  target(row,0,'wrapper registration')
  row['aspects'][0]['conditions']=[]
  row['rationale']='One comparison targets wrapper registration as the compared behavior; Material and Bootstrap are adapter scope. Formly 6 is version scope rather than a condition.'
 elif n==16:
  target(row,0,'its value in the model')
  row['aspects'][0]['conditions']=[span(row['question'],'disabling a field')]
  row['rationale']='Disabling the field is the hypothetical operating condition. Its value in the model is the complete distinguishing target. Angular 21 is version scope, and minimal its resolves to a field.'
 elif n==17:
  cue(row,0,'How do I register')
  row['rationale']='It remains ambiguous between the wrapper and renderer. Setup is not another ask. The contiguous interrogative and operation precede the unresolved target.'
 elif n==18:
  cue(row,0,'How do I register')
  row['rationale']='That wrapper uniquely resolves to The wrapper. The quoted audit-shell occurrence is both custom_identifier and literal, attached to the aspect identifiers. Its naming statement supplies setup; no API/value assignment is invented.'
 elif n==19:
  target(row,0,'this')
  row['aspects'][0]['conditions']=[span(row['question'],'that setting')]
  row['rationale']='This is the removal target and that setting the operating condition. Both references remain unresolved. Stop this from being removed preserves prevention as a negative outcome, while the cue is interrupted by setup and target.'
 elif n==20:
  row['rationale']='The assignment is setup. That setting uniquely refers to props.disabled, paired with true. The field is the disabling target; Does and disable are separated by the reference.'
 elif n==21:
  row['rationale']='One comparison jointly targets both exact API spellings; the full adjacent comparison phrase is one cue.'
 elif n==22:
  cue(row,0,'Where should I register')
  row['rationale']='One registration-location ask keeps the adjacent Where interrogative and register operation together. The generic custom field type supplies no explicitly named identifier.'
 elif n==23:
  cue(row,0,'How can I render')
  row['rationale']='One rendering ask has a contiguous cue. Read-only is a target adjective rather than a separate syntactic negative constraint; label is not an exact API mention.'
 elif n==24:
  cue(row,0,'how do I set')
  for a in row['aspects']: a['conditions']=[]
  row['rationale']='Setting the property and update timing are independent asks with separate API occurrences. For the same field is shared topical context, not a condition. Same relates the two asks to one generic field and is not treated as an unresolved external reference. When does / update is interrupted by its target.'

def check(value,q):
 if isinstance(value,dict):
  if set(value)=={'text','start','end'}: assert q[value['start']:value['end']]==value['text']
  for v in value.values(): check(v,q)
 elif isinstance(value,list):
  for v in value: check(v,q)
for row in rows: check(row,row['question'])
assert len(rows)==24
(base/'annotator-two-v2.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(f'Wrote {len(rows)} independently reconsidered questions; {sum(len(r["aspects"]) for r in rows)} aspects; all Unicode spans valid.')

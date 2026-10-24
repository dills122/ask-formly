"""Independent wording-only annotations. Python offsets count Unicode codepoints."""
import json
from pathlib import Path
base=Path(__file__).resolve().parent
questions=json.loads((base/'questions.json').read_text())
fields='targets request_cues conditions negative_constraints identifiers literals versions ui_adapters references resolved_antecedents unresolved_references'.split()
rows=[]
def begin(n,rationale,unclear=False):
 global q,row
 q=questions[n-1]['question']
 row=dict(id=questions[n-1]['id'],question=q,status='needs_clarification' if unclear else 'clear',aspects=[],entities={k:[] for k in ['api','custom_identifier','literal','version','ui_adapter']},relations=[],rationale=rationale)
 rows.append(row)
def s(spec):
 text,occurrence=spec if isinstance(spec,tuple) else (spec,1)
 start=-1
 for _ in range(occurrence): start=q.index(text,start+1)
 return dict(text=text,start=start,end=start+len(text))
def a(targets,cues,**kw):
 vals=dict(targets=targets,request_cues=cues,**kw)
 item=dict(id='a'+str(len(row['aspects'])+1))
 item.update({k:[s(x) for x in vals.get(k,[])] for k in fields})
 item['target_anchor']=min(item['targets'],key=lambda x:x['start'])
 row['aspects'].append(item)
def e(**kw):
 for k,v in kw.items(): row['entities'][k].extend(s(x) for x in v)
def r(kind,head,tail): row['relations'].append(dict(kind=kind,head=s(head),tail=s(tail)))

begin(1,'Value handling and error handling are separate asks. Both possessives uniquely refer to the disabled field.')
for t in ['its value','its validation errors']:
 a([t],['how are','handled'],conditions=['When a field is disabled'],references=[t],resolved_antecedents=['a field']); r('refers_to',t,'a field')
begin(2,'Preserving the model value and the control are distinct outcomes. Hiding is the shared hypothetical action. False is a value, not negation.')
e(api=['resetOnHide','FormControl'],literal=['false']); r('has_value','resetOnHide','false')
for t in ['its model value','its FormControl']:
 a([t],['does','preserve'],conditions=['With resetOnHide set to false','hiding the field'],identifiers=['resetOnHide']+(['FormControl'] if t=='its FormControl' else []),literals=['false'],references=[t],resolved_antecedents=['the field']); r('refers_to',t,'the field')
begin(3,'Two persistence outcomes share the page-reload condition.')
e(api=['options.formState'])
a(['options.formState'],['can','survive'],conditions=['After reloading the page'],identifiers=['options.formState'])
a(['the selected tab'],[('can',2),('survive',2)],conditions=['After reloading the page'])
begin(4,'Registration and removal are separate operations on the same wrapper, deliberately sharing an anchor. The generic definite wrapper does not require an external named instance to understand the ask.')
for action in ['registration','removal']: a(['the wrapper'],['explain',action],conditions=['For the wrapper'])
begin(5,'One hiding request is constrained to preserve the field value. The constraint is not another ask.')
a(['a field'],['How can I','hide'],negative_constraints=['without clearing its value'],references=['its value'],resolved_antecedents=['a field']); r('refers_to','its value','a field')
begin(6,'Clearing is requested and hiding excluded. It uniquely refers to the field.')
a(['a field'],['How can I','clear'],negative_constraints=['without hiding it'],references=[('it',2)],resolved_antecedents=['a field']); r('refers_to',('it',2),'a field')
begin(7,'One validation-disabling request has a coordinated negative constraint. Its value refers to the control. Generic control and validation words are not APIs.')
a(['validation'],['Can I','disable'],negative_constraints=['without removing the control or changing its value'],references=['its value'],resolved_antecedents=['the control']); r('refers_to','its value','the control')
begin(8,'Keeping the answer and not retaining the control are separate requested outcomes. When hidden scopes both. Its elliptical subject could be the answer display or containing field; I treat this as a generic hiding condition, not an explicit unresolved reference. This boundary merits guideline discussion.')
a(['the answer'],['How do I','keep'],conditions=['when hidden'])
a(['the control'],['How do I','retain'],conditions=['when hidden'],negative_constraints=['not retain the control'])
begin(9,'One selection question concerns supplied values collectively. The plural reference resolves to the explicit pair of literals; identifier/value relationships are individually preserved.')
e(api=['defaultValue','props.disabled'],literal=['0','false']); r('has_value','defaultValue','0'); r('has_value','props.disabled','false')
a(['supplied values'],['which','are used'],conditions=['With defaultValue set to 0 and props.disabled set to false'],identifiers=['defaultValue','props.disabled'],literals=['0','false'],references=['supplied values'],resolved_antecedents=['0','false'])
r('refers_to','supplied values','0'); r('refers_to','supplied values','false')
begin(10,'The whole generic expression is the API target. MyProps and caféLabel are custom identifiers; nested and repeated MyProps mentions are retained. The inclusion clause is setup.')
e(api=['FormlyFieldConfig<MyProps>'],custom_identifier=['MyProps',('MyProps',2),'caféLabel'])
a(['FormlyFieldConfig<MyProps>'],['How do I','type'],conditions=['when MyProps includes caféLabel'],identifiers=['FormlyFieldConfig<MyProps>','MyProps',('MyProps',2),'caféLabel'])
begin(11,'One comparison jointly targets the ordinally distinguished fields. Repeated key and city spans remain separately paired.')
e(api=['key',('key',2)],literal=["'city'",("'city'",2)]); r('has_value','key',"'city'"); r('has_value',('key',2),("'city'",2))
a(['the first field','the second field'],['Does','differ from'],conditions=["with key 'city'",("with key 'city'",2)],identifiers=['key',('key',2)],literals=["'city'",("'city'",2)])
begin(12,'One location question targets the exact property path. This configuration resolves forward to the object. Bare object keys are exact APIs; values are linked without inventing dotted paths.')
obj='{ key: "nickname", props: { placeholder: "Café ☕" } }'
e(api=['key','props','placeholder','props.placeholder'],literal=['"nickname"','"Café ☕"']); r('has_value','key','"nickname"'); r('has_value','placeholder','"Café ☕"'); r('refers_to','this configuration',obj)
a(['props.placeholder'],['where does','appear'],conditions=['Given this configuration:\n'+obj],identifiers=['key','props','placeholder','props.placeholder'],literals=['"nickname"','"Café ☕"'],references=['this configuration'],resolved_antecedents=[obj])
begin(13,'One suffix-addition request has Formly version, Material adapter, and input destination scope. Generic suffix/input words are not APIs.')
e(version=['Formly 6.3.12'],ui_adapter=['Material'])
a(['a suffix'],['how do I','add'],conditions=['In Formly 6.3.12 with Material','to an input'],versions=['Formly 6.3.12'],ui_adapters=['Material'])
begin(14,'Setting a placeholder and showing validation messages are independent asks sharing explicit version and adapter scope.')
e(api=['props.placeholder'],version=['Formly v7'],ui_adapter=['PrimeNG'])
a(['props.placeholder'],['how do I','set'],conditions=['For Formly v7 with PrimeNG'],identifiers=['props.placeholder'],versions=['Formly v7'],ui_adapters=['PrimeNG'])
a(['validation messages'],[('how do I',2),'show'],conditions=['For Formly v7 with PrimeNG'],versions=['Formly v7'],ui_adapters=['PrimeNG'])
begin(15,'One comparison concerns wrapper registration across two adapters. The behavior noun phrase and both compared adapters are targets within one record; this target-versus-scope boundary merits discussion.')
e(version=['Formly 6'],ui_adapter=['Material','Bootstrap'])
a(['wrapper registration','Material','Bootstrap'],['Does','differ between'],conditions=['in Formly 6'],versions=['Formly 6'],ui_adapters=['Material','Bootstrap'])
begin(16,'Disabling is the hypothetical cause and value the affected target. The possessive resolves to the field. Angular version supplies framework scope only.')
e(version=['Angular 21'])
a(['its value'],['does','affect'],conditions=['In Angular 21','disabling a field','in the model'],versions=['Angular 21'],references=['its value'],resolved_antecedents=['a field']); r('refers_to','its value','a field')
begin(17,'It could refer to either wrapper or renderer; recency does not settle the registration target.',True)
a(['it'],['How do I','register'],conditions=['I have a wrapper around a renderer'],references=['it'],unresolved_references=['it'])
begin(18,'That wrapper uniquely refers to the named wrapper. Its quoted name is both a custom identifier and a string literal; wrapper is not an API. No API-name/value relation is invented.')
e(custom_identifier=["'audit-shell'"],literal=["'audit-shell'"])
a(['that wrapper'],['How do I','register'],conditions=["The wrapper is named 'audit-shell'"],identifiers=["'audit-shell'"],literals=["'audit-shell'"],references=['that wrapper'],resolved_antecedents=['The wrapper']); r('refers_to','that wrapper','The wrapper')
begin(19,'Neither that setting nor this has an in-question antecedent. Prevention of removal is preserved as negative outcome even without a literal not; this lexical-negation boundary merits discussion.',True)
a(['that setting','this'],['Can','stop','from being removed'],negative_constraints=['stop this from being removed'],references=['that setting','this'],unresolved_references=['that setting','this'])
begin(20,'That setting uniquely resolves to the explicit API assignment. The assignment is setup and disabling the field is the ask. True is a literal.')
e(api=['props.disabled'],literal=['true']); r('has_value','props.disabled','true'); r('refers_to','that setting','props.disabled')
a(['the field'],['Does','disable'],conditions=['I set props.disabled to true'],identifiers=['props.disabled'],literals=['true'],references=['that setting'],resolved_antecedents=['props.disabled'])
begin(21,'One comparison jointly targets both exact API spellings.')
e(api=['expressions','expressionProperties']); a(['expressions','expressionProperties'],['What is the difference between'],identifiers=['expressions','expressionProperties'])
begin(22,'One registration-location request retains Where in its cue. The generic custom field type supplies no exact identifier.')
a(['a custom field type'],['Where should I','register'])
begin(23,'One rendering request. Read-only describes the label, not a separate syntactically negative constraint; generic label is not an explicit API.')
a(['a read-only label'],['How can I','render'])
begin(24,'Setting the property and its update timing are independent asks with separate API occurrences. Same field relates the two asks to one shared generic field, requiring no external identity. Whether same should receive an unresolved-reference label merits discussion.')
e(api=['props.label',('props.label',2)])
a(['props.label'],['how do I','set'],conditions=['For the same field'],identifiers=['props.label'])
a([('props.label',2)],['when does','update'],conditions=['For the same field'],identifiers=[('props.label',2)])

def check(value,q):
 if isinstance(value,dict):
  if set(value)=={'text','start','end'}: assert q[value['start']:value['end']]==value['text']
  for v in value.values(): check(v,q)
 elif isinstance(value,list):
  for v in value: check(v,q)
for row in rows: check(row,row['question'])
assert len(rows)==24
(base/'annotator-two.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(f'Wrote {len(rows)} annotations and {sum(len(x["aspects"]) for x in rows)} aspects; spans verified.')

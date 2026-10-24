"""Author's independent raw labels; source phrases manually selected before predictions."""
import json
from pathlib import Path
from contract import FIELDS, ENTITY_TYPES, validate_annotation
HERE=Path(__file__).parent
rows=json.loads((HERE/'questions.json').read_text()); result=[]

def span(text):
    occurrence=0
    if isinstance(text,tuple): text,occurrence=text
    start=-1
    for _ in range(occurrence+1): start=q.index(text,start+1)
    return dict(text=text,start=start,end=start+len(text))
def aspect(targets,cues,**kw):
    r={k:[] for k in FIELDS}
    r['targets']=[span(t) for t in targets]; r['request_cues']=[span(t) for t in cues]
    for k,v in kw.items(): r[k]=[span(t) for t in v]
    r['target_anchor']=min(r['targets'],key=lambda s:s['start']); r['id']=f'a{len(aspects)+1}'
    aspects.append(r)
def ent(kind,*texts): entities[kind].extend(span(t) for t in texts)
def rel(kind,head,tail): relations.append(dict(kind=kind,head=span(head),tail=span(tail)))
for row in rows:
 q=row['question']; i=row['id']; aspects=[]; entities={k:[] for k in ENTITY_TYPES}; relations=[]; rationale='Source-grounded request; no answer inferred.'
 if i=='P01':
  for target in ['its value','its validation errors']:
   aspect([target],['how are','handled'],conditions=['When a field is disabled'],references=['its' if target=='its value' else ('its',1)],resolved_antecedents=['a field'])
  rel('refers_to','its','a field'); rel('refers_to',('its',1),'a field')
 elif i=='P02':
  for target in ['its model value','its FormControl']:
   aspect([target],['does','preserve'],conditions=['With resetOnHide set to false','hiding the field'],identifiers=['resetOnHide']+(['FormControl'] if 'FormControl' in target else []),literals=['false'],references=['its' if 'model' in target else ('its',1)],resolved_antecedents=['the field'])
  ent('api','resetOnHide','FormControl'); ent('literal','false'); rel('has_value','resetOnHide','false'); rel('refers_to','its','the field'); rel('refers_to',('its',1),'the field')
 elif i=='P03':
  aspect(['options.formState'],['can','survive'],conditions=['After reloading the page'],identifiers=['options.formState'])
  aspect(['the selected tab'],[('can',1),('survive',1)],conditions=['After reloading the page'])
  ent('api','options.formState')
 elif i=='P04':
  aspect(['the wrapper'],['explain','registration']); aspect(['the wrapper'],['explain','removal'])
  rationale='Two requested operations on the same target occurrence. Retain same anchor in two records.'
 elif i=='P05':
  aspect(['a field'],['How can I hide'],negative_constraints=['without clearing its value'],references=['its'],resolved_antecedents=['a field']); rel('refers_to','its','a field')
 elif i=='P06':
  aspect(['a field'],['How can I clear'],negative_constraints=['without hiding it'],references=['it'],resolved_antecedents=['a field']); rel('refers_to','it','a field')
 elif i=='P07':
  aspect(['validation'],['Can I disable'],negative_constraints=['without removing the control or changing its value'],references=['its'],resolved_antecedents=['the control']); rel('refers_to','its','the control')
 elif i=='P08':
  aspect(['the answer'],['How do I keep'],conditions=['when hidden'],negative_constraints=['not retain the control'])
  aspect(['the control'],['retain'],conditions=['when hidden'],negative_constraints=['not retain the control'])
  rationale='Keep answer and avoid retaining control are distinct coordinated outcomes; hidden applies to both.'
 elif i=='P09':
  aspect(['supplied values'],['which','are used'],conditions=['With defaultValue set to 0 and props.disabled set to false'],identifiers=['defaultValue','props.disabled'],literals=['0','false'])
  ent('api','defaultValue','props.disabled'); ent('literal','0','false'); rel('has_value','defaultValue','0'); rel('has_value','props.disabled','false')
 elif i=='P10':
  aspect(['FormlyFieldConfig<MyProps>'],['How do I type'],conditions=['when MyProps includes caféLabel'],identifiers=['FormlyFieldConfig<MyProps>',('MyProps',1),'caféLabel'])
  ent('api','FormlyFieldConfig<MyProps>'); ent('custom_identifier','MyProps',('MyProps',1),'caféLabel')
 elif i=='P11':
  aspect(['the first field','the second field'],['Does','differ from'],conditions=["with key 'city'",("with key 'city'",1)],identifiers=['key',('key',1)],literals=["'city'",("'city'",1)])
  ent('api','key',('key',1)); ent('literal',"'city'",("'city'",1)); rel('has_value','key',"'city'"); rel('has_value',('key',1),("'city'",1))
 elif i=='P12':
  aspect(['props.placeholder'],['where does','appear'],conditions=['Given this configuration:\n{ key: "nickname", props: { placeholder: "Café ☕" } }'],identifiers=['key','props','placeholder','props.placeholder'],literals=['"nickname"','"Café ☕"'])
  ent('api','key','props','placeholder','props.placeholder'); ent('literal','"nickname"','"Café ☕"'); rel('has_value','key','"nickname"'); rel('has_value','placeholder','"Café ☕"')
 elif i=='P13':
  aspect(['a suffix'],['how do I add'],conditions=['to an input'],versions=['Formly 6.3.12'],ui_adapters=['Material'])
  ent('version','Formly 6.3.12'); ent('ui_adapter','Material')
 elif i=='P14':
  aspect(['props.placeholder'],['how do I set'],identifiers=['props.placeholder'],versions=['Formly v7'],ui_adapters=['PrimeNG'])
  aspect(['validation messages'],['how do I show'],versions=['Formly v7'],ui_adapters=['PrimeNG'])
  ent('api','props.placeholder'); ent('version','Formly v7'); ent('ui_adapter','PrimeNG')
 elif i=='P15':
  aspect(['wrapper registration'],['Does','differ between'],versions=['Formly 6'],ui_adapters=['Material','Bootstrap'])
  ent('version','Formly 6'); ent('ui_adapter','Material','Bootstrap')
 elif i=='P16':
  aspect(['its value in the model'],['does','affect'],conditions=['disabling a field'],versions=['Angular 21'],references=['its'],resolved_antecedents=['a field'])
  ent('version','Angular 21'); rel('refers_to','its','a field')
 elif i=='P17':
  aspect(['it'],['How do I register'],conditions=['I have a wrapper around a renderer'],references=['it'],unresolved_references=['it'])
  rationale='It may refer to wrapper or renderer, both registrable concepts; no unique antecedent.'
 elif i=='P18':
  aspect(['that wrapper'],['How do I register'],conditions=["The wrapper is named 'audit-shell'"],literals=["'audit-shell'"],references=['that wrapper'],resolved_antecedents=['The wrapper'])
  ent('literal',"'audit-shell'"); rel('refers_to','that wrapper','The wrapper')
 elif i=='P19':
  aspect(['this'],['Can','stop','from being removed'],conditions=['that setting'],references=['that setting','this'],unresolved_references=['that setting','this'])
  rationale='No antecedent for the setting or removed target.'
 elif i=='P20':
  aspect(['the field'],['Does','disable'],conditions=['I set props.disabled to true'],identifiers=['props.disabled'],literals=['true'],references=['that setting'],resolved_antecedents=['props.disabled'])
  ent('api','props.disabled'); ent('literal','true'); rel('has_value','props.disabled','true'); rel('refers_to','that setting','props.disabled')
 elif i=='P21':
  aspect(['expressions','expressionProperties'],['What is the difference between'],identifiers=['expressions','expressionProperties']); ent('api','expressions','expressionProperties')
 elif i=='P22': aspect(['a custom field type'],['Where should I register'])
 elif i=='P23': aspect(['a read-only label'],['How can I render'])
 elif i=='P24':
  aspect(['props.label'],['how do I set'],conditions=['For the same field'],identifiers=['props.label'])
  aspect([('props.label',1)],['when does','update'],conditions=['For the same field'],identifiers=[('props.label',1)])
  ent('api','props.label',('props.label',1)); rationale='Same field links the two asks; no missing external antecedent is needed.'
 annotated=dict(id=i,question=q,status='needs_clarification' if any(a['unresolved_references'] for a in aspects) else 'clear',aspects=aspects,entities=entities,relations=relations,rationale=rationale)
 validate_annotation(annotated); result.append(annotated)
(HERE/'annotator-one.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print('Wrote 24 independent author annotations')

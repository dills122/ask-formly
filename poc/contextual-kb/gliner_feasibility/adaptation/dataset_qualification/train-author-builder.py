"""Raw independent TRAIN author provenance: manually specified source labels only.
No inference, lexical classification, model output, or other labels are consulted.
Occurrence tuples are zero-based among exact substrings; unindexed ambiguous
strings fail. Word edges are checked so 'it' cannot silently match 'initial'.
"""
import json
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from pilot.contract import validate_annotation, FIELDS, ENTITY_TYPES
QUESTIONS = json.loads((ROOT/'questions.json').read_text())['train']
ROWS = []

def span(q, selector):
    explicit = isinstance(selector, tuple)
    text, occurrence = selector if explicit else (selector, 0)
    starts = [m.start() for m in re.finditer(re.escape(text), q)]
    if not explicit and len(starts) != 1:
        raise ValueError(f'Ambiguous/missing selection {selector!r}: {q}')
    start = starts[occurrence]; end = start + len(text)
    if text[0].isalnum() and start and (q[start-1].isalnum() or q[start-1]=='_'):
        raise ValueError(f'Left identifier boundary {selector!r}: {q}')
    if text[-1].isalnum() and end<len(q) and (q[end].isalnum() or q[end]=='_'):
        raise ValueError(f'Right identifier boundary {selector!r}: {q}')
    return dict(text=text,start=start,end=end)

def A(t,c,co=(),n=(),i=(),l=(),v=(),u=(),r=(),ur=()):
    return dict(targets=t,request_cues=c,conditions=co,negative_constraints=n,
                identifiers=i,literals=l,versions=v,ui_adapters=u,refs=r,unresolved_references=ur)

def D(num, aspects, api=(),custom=(),lit=(),ver=(),ui=(),values=(),why='Explicit source ask; no behavioral answer inferred.'):
    src=QUESTIONS[num-1]; assert src['id']==f'T{num:03}'
    q=src['question']; out=[]; rel=[]
    for idx,a in enumerate(aspects,1):
        refs=a.pop('refs'); z={k:[span(q,s) for s in a.get(k,())] for k in FIELDS}
        for head,tail in refs:
            h=span(q,head); z['references'].append(h)
            if tail is not None:
                t=span(q,tail); z['resolved_antecedents'].append(t)
                edge=dict(kind='refers_to',head=h,tail=t)
                if edge not in rel: rel.append(edge)
        for s in z['unresolved_references']:
            if s not in z['references']: z['references'].append(s)
        z['target_anchor']=min(z['targets'],key=lambda s:s['start']); z['id']=f'a{idx}'; out.append(z)
    for head,tail in values: rel.append(dict(kind='has_value',head=span(q,head),tail=span(q,tail)))
    entities={k:[span(q,s) for s in ss] for k,ss in zip(ENTITY_TYPES,(api,custom,lit,ver,ui))}
    row=dict(id=src['id'],question=q,status='needs_clarification' if any(a['unresolved_references'] for a in out) else 'clear',aspects=out,entities=entities,relations=rel,rationale=why)
    validate_annotation(row); ROWS.append(row)

D(1,[A(['the new row'],['where is','placed'],['When an address row is inserted']),A(['field'],['which','receives focus'],['When an address row is inserted'])])
D(2,[A(['their order'],['explain'],['After adding two address rows'],r=[('their','two address rows')]),A(['focus'],['how','moves'],['After adding two address rows'],r=[('them','two address rows')])])
D(3,[A(['the change'],['how can I observe'],['If an expression changes a label']),A(['the observation'],['how can I','unsubscribe from'],['If an expression changes a label'])])
D(4,[A(['subscription setup'],['explain']),A(['cleanup'],['explain'])],why='Setup and cleanup are distinct operations for label-change observations.')
D(5,[A(["the section's model entries"],['what happens to'],['When a repeated section is removed']),A(['validation messages'],['what happens to'],['When a repeated section is removed'])])
D(6,[A(['the remaining keys'],['how are','affected'],['After deleting the middle repeated section']),A(['error messages'],['how are','affected'],['After deleting the middle repeated section'])])
D(7,[A(['their nesting order'],['explain'],['With two wrappers around an input'],r=[(('their',0),'two wrappers')]),A(['their labels'],['where','are rendered'],['With two wrappers around an input'],r=[(('their',1),'two wrappers')])])
D(8,[A(['the order'],['how do I choose']),A(['the resulting structure'],['how do I','inspect'])])
D(9,[A(['a loading indicator'],['how do I show'],['While options are loading']),A(['selection of stale options'],['how do I','prevent'],['While options are loading'],['prevent selection of stale options'])])
D(10,[A(['the choices'],['how can I replace'],['Once a remote options request completes']),A(['a request error'],['how can I','expose'],['Once a remote options request completes'])])
D(11,[A(['the form'],['explain resetting'],['Given a populated form']),A(['the reset target values'],['explain','choosing'],['Given a populated form'])])
D(12,[A(['it'],['describe how to trigger'],r=[('it','a reset action')]),A(['completion'],['describe','how to observe'])])
D(13,[A(['the group'],['how is','rendered'],['When a field group becomes visible']),A(['its child labels'],['how are','displayed'],['When a field group becomes visible'],r=[('its','a field group')])])
D(14,[A(['rendering order'],['what changes in'],['If I move a group below another group']),A(['keyboard navigation'],['what changes in'],['If I move a group below another group'])])
D(15,[A(['defaults'],[('which',0),'are combined'],['When a custom type extends another type']),A(['configuration'],[('which',1),'wins'],['When a custom type extends another type','on conflict'])])
D(16,[A(['default merging'],['explain']),A(['the effective configuration'],['how to inspect'])])
D(17,[A(['a field label'],['How can I update'],n=['without changing its key'],r=[('its','a field')])])
D(18,[A(['the displayed caption'],['Can I change'],n=['without changing the model path'])])
D(19,[A(['select choices'],['How do I populate'],n=['without making a network request'])])
D(20,[A(['locally supplied choices'],['Can I refresh'],n=['without contacting a server'])])
D(21,[A(['an error message'],['How can I hide'],n=['without disabling the validator'])])
D(22,[A(['validation text'],['Can I suppress'],n=['without treating an invalid control as valid'])])
D(23,[A(['a wrapper'],['How can I add'],n=["without editing the field type's template"])])
D(24,[A(['a surrounding wrapper'],['Can I remove'],n=['without modifying the renderer template'])])
D(25,[A(['one section'],['How do I reset'],n=['without resetting the sibling section'])])
D(26,[A(['one repeated row'],['Can I clear'],n=['without clearing the other rows'])])
D(27,[A(['a row'],['How do I add']),A(['keyboard focus'],['How do I','move'],n=['not move keyboard focus to it'],r=[('it','a row')])],why='Positive row addition and separately prohibited focus movement are separate asks.')
D(28,[A(['a new field'],['Can','appear'],n=['without taking focus from the current input'])])
D(29,[A(['a description'],['How do I compute'],n=['without mutating the source model'])])
D(30,[A(['shared state'],['Can an expression read'],n=['without writing to it'],r=[(('it',2),'shared state')])])
D(31,[A(['a field'],['How can','be optional']),A(['a field'],['How can','be'],n=['not disabled'])],why='Optionality and prohibited disabling are separate outcomes on the same field anchor.')
D(32,[A(['the required constraint'],['Can I remove'],n=['without removing the field'])])
D(33,[A(['FormlyFieldConfig<ContactProps>'],['Where do I declare'],['when ContactProps has a field named résumé'],i=['FormlyFieldConfig<ContactProps>',('ContactProps',0),('ContactProps',1),'résumé'])],api=['FormlyFieldConfig<ContactProps>'],custom=[('ContactProps',0),('ContactProps',1),'résumé'])
D(34,[A(['props.helpText'],['How do I express'],i=['props.helpText','FormlyFieldConfig<ContactProps>','ContactProps'])],api=['props.helpText','FormlyFieldConfig<ContactProps>'],custom=['ContactProps'])
D(35,[A(['choices'],['what','are displayed'],['With props.options set to []'],i=['props.options'],l=['[]'])],api=['props.options'],lit=['[]'],values=[('props.options','[]')])
D(36,[A([('0',1)],['how is','represented'],["For props.options containing { value: 0, label: 'Zero' }"],i=['props.options','value','label'],l=["{ value: 0, label: 'Zero' }",('0',0),"'Zero'",('0',1)])],api=['props.options','value','label'],lit=["{ value: 0, label: 'Zero' }",('0',0),"'Zero'",('0',1)],values=[('props.options',"{ value: 0, label: 'Zero' }"),('value',('0',0)),('label',"'Zero'")])
D(37,[A(["key 'address.zip'","key ['address', 'zip']"],['How does','differ from'],i=[('key',0),('key',1)],l=["'address.zip'","['address', 'zip']"])],api=[('key',0),('key',1)],lit=["'address.zip'","['address', 'zip']"],values=[(('key',0),"'address.zip'"),(('key',1),"['address', 'zip']")])
D(38,[A(["key ['people', 0, 'name']","key 'people.0.name'"],['Does','identify a different model location from'],i=[('key',0),('key',1)],l=["['people', 0, 'name']","'people.0.name'"])],api=[('key',0),('key',1)],lit=["['people', 0, 'name']","'people.0.name'"],values=[(('key',0),"['people', 0, 'name']"),(('key',1),"'people.0.name'")])
D(39,[A(['input behaviors'],['which','are requested'],['With props.required set to false and props.readonly set to true'],i=['props.required','props.readonly'],l=['false','true'])],api=['props.required','props.readonly'],lit=['false','true'],values=[('props.required','false'),('props.readonly','true')])
D(40,[A(['props.required'],['What does','mean'],["for an empty string ''"],i=['props.required'],l=['true',"''"])],api=['props.required'],lit=['true',"''"],values=[('props.required','true')])
D(41,[A(['an expression'],['How do I attach'],i=["expressions['props.description']"],l=["'props.description'"])],api=["expressions['props.description']"],lit=["'props.description'"])
D(42,[A(["the callback for expressions['props.required']"],['Where is','configured'],i=["expressions['props.required']"],l=["'props.required'"])],api=["expressions['props.required']"],lit=["'props.required'"])
D(43,[A(["validation.messages['postalCode']"],['How do I configure'],i=["validation.messages['postalCode']",("'postalCode'",0),("'postalCode'",1)],l=[("'postalCode'",0),("'postalCode'",1)])],api=["validation.messages['postalCode']"],custom=[("'postalCode'",0),("'postalCode'",1)],lit=[("'postalCode'",0),("'postalCode'",1)])
D(44,[A(['validators.validation'],['Where is','declared'],i=['validators.validation',"'postalCode'"],l=["['postalCode']","'postalCode'"])],api=['validators.validation'],custom=["'postalCode'"],lit=["['postalCode']","'postalCode'"],values=[('validators.validation',"['postalCode']")])
D(45,[A(['className'],['Where should','be placed'],i=['className'],l=["'col-6'"]),A(['fieldGroupClassName'],['Where should','be placed'],i=['fieldGroupClassName'],l=["'grid'"])],api=['className','fieldGroupClassName'],lit=["'col-6'","'grid'"],values=[('className',"'col-6'"),('fieldGroupClassName',"'grid'")])
D(46,[A(["className 'a' on a group","className 'a' on a child"],['What is the distinction between'],i=[('className',0),('className',1)],l=[("'a'",0),("'a'",1)])],api=[('className',0),('className',1)],lit=[("'a'",0),("'a'",1)],values=[(('className',0),("'a'",0)),(('className',1),("'a'",1))])
D(47,[A(['value'],['which','is addressed'],["Given model = { city: 'Montréal', count: 0 }"],i=['model',('city',0),'count','key',"'city'"],l=["{ city: 'Montréal', count: 0 }","'Montréal'",'0',"'city'"])],api=['model','key'],custom=[('city',0),'count',"'city'"],lit=["{ city: 'Montréal', count: 0 }","'Montréal'",'0',"'city'"],values=[('model',"{ city: 'Montréal', count: 0 }"),(('city',0),"'Montréal'"),('count','0'),('key',"'city'")])
D(48,[A(['the empty-string default'],['when is','considered'],["With defaultValue: '' and key: 'note'"],i=['defaultValue','key',"'note'"],l=["''","'note'"])],api=['defaultValue','key'],custom=["'note'"],lit=["''","'note'"],values=[('defaultValue',"''"),('key',"'note'")])
D(49,[A(['prefix text'],['where is','configured'],v=['Formly 6.3.12'],u=['Material'])],ver=['Formly 6.3.12'],ui=['Material'])
D(50,[A(['prefix content'],['how do I position'],v=['Formly 6'],u=['Material'])],ver=['Formly 6'],ui=['Material'])
D(51,[A(['fields'],['how do I arrange'],v=['Formly 6.3.12'],u=['Bootstrap'])],ver=['Formly 6.3.12'],ui=['Bootstrap'])
D(52,[A(['group layout classes'],['where should','go'],v=['Formly 6'],u=['Bootstrap'])],ver=['Formly 6'],ui=['Bootstrap'])
D(53,[A(['select options'],['how are','supplied'],v=['Formly 6'],u=['PrimeNG'])],ver=['Formly 6'],ui=['PrimeNG'])
D(54,[A(['the select placeholder'],['where is','set'],v=['Formly 6.3.12'],u=['PrimeNG'])],ver=['Formly 6.3.12'],ui=['PrimeNG'])
D(55,[A(["a field's initialization hook"],['when does','run'],v=['Angular 21','Formly 6.3.12'])],ver=['Angular 21','Formly 6.3.12'])
D(56,[A(['field cleanup logic'],['where do I attach'],v=['Angular 21','Formly 6'])],ver=['Angular 21','Formly 6'])
D(57,[A(['description placement'],['how does','differ'],v=['Formly 6.3.12'],u=['Material','Bootstrap'])],ver=['Formly 6.3.12'],ui=['Material','Bootstrap'])
D(58,[A(['error-message placement'],['compare'],v=['Formly 6'],u=['Material','Bootstrap'])],ver=['Formly 6'],ui=['Material','Bootstrap'])
D(59,[A(['custom validator registration'],['how does','differ'],v=['Formly 6','Formly 7'])],ver=['Formly 6','Formly 7'])
D(60,[A(['validator configuration'],['Compare'],v=['Formly 6.3.12','Formly 7'])],ver=['Formly 6.3.12','Formly 7'])
D(61,[A(['an input'],[('how do I configure',0)],v=['Formly 6'],u=['Material']),A(['a textarea'],[('how do I configure',1)],v=['Formly 7'],u=['Bootstrap'])],ver=['Formly 6','Formly 7'],ui=['Material','Bootstrap'])
D(62,[A(['a select label'],[('explain',0)],v=['Formly 6'],u=['Material']),A(['a checkbox label'],[('explain',1)],v=['Formly 7'],u=['PrimeNG'])],ver=['Formly 6','Formly 7'],ui=['Material','PrimeNG'])
D(63,[A(['type names'],['where are','registered'],n=['without a UI adapter'],v=['Formly 6.3.12'])],ver=['Formly 6.3.12'])
D(64,[A(['a wrapper name'],['how is','associated'],n=['without Material'],v=['Formly 6'],u=['Material'])],ver=['Formly 6'],ui=['Material'])
D(65,[A(['that group'],['How do I reset'],ur=['that group'])],why='That group can denote billing or shipping; neither is selected.')
D(66,[A(['it'],['How can I move'],ur=['it'])],why='It could denote the personal section, work section, or form.')
D(67,[A(['that group'],['How do I reset'],r=[('that group','The shipping group')])])
D(68,[A(['that section'],['How do I move'],i=["'delivery'"],l=["'delivery'"],r=[('that section',"A section named 'delivery'")])],custom=["'delivery'"],lit=["'delivery'"])
D(69,[A(['Which one'],['does','use'],ur=['Which one','this'])],why='Which one contrasts the initial and current values, while this lacks an identified consuming operation; reference interpretation remains unresolved.')
D(70,[A(['that value'],['How do I choose'],ur=['that value'])],why='That value can refer to either the default value or the server value.')
D(71,[A(['that option'],['How do I select'],i=["'weekly'"],l=["'weekly'"],r=[('that option','The option')])],custom=["'weekly'"],lit=["'weekly'"])
D(72,[A(['that validator'],['How do I attach'],i=["'businessDay'"],l=["'businessDay'"],r=[('that validator','A validator')])],custom=["'businessDay'"],lit=["'businessDay'"])
D(73,[A(['it'],['How do I remove'],ur=['it'])],why='It could denote either expression, or an outcome controlled by one; no unique referent.')
D(74,[A(['that expression'],['When does','run'],ur=['that expression'])],why='The required expression and readonly expression are competing antecedents.')
D(75,[A(['its errors'],['Where can I inspect'],r=[('its','The email control')])])
D(76,[A(['that description'],['How do I replace'],r=[('that description','a description')])])
D(77,[A(['that behavior'],['How do I stop'],['for this field'],n=['stop that behavior'],ur=['that behavior','this field'])],why='Neither the behavior nor the demonstratively identified field has an in-question antecedent.')
D(78,[A(['this'],['Can','still work'],['when that is absent'],n=['that is absent'],ur=['this','that'])],why='This and that lack antecedents, so the operation and absent prerequisite are unidentified.')
D(79,[A(['that property'],['How do I read'],i=["'subtotal'"],l=["'subtotal'"],r=[('that property',"a property named 'subtotal'")])],custom=["'subtotal'"],lit=["'subtotal'"])
D(80,[A(['that wrapper'],['Where do I register'],i=["'panel'"],l=["'panel'"],r=[('that wrapper',"A wrapper named 'panel'")])],custom=["'panel'"],lit=["'panel'"])
D(81,[A(['custom validation functions'],['Where are','configured'])])
D(82,[A(['a named validation message'],['How do I register'])])
D(83,[A(['a field key','a field type name'],['What is the difference between'])])
D(84,[A(['key','type'],['Compare the purpose of'],i=['key','type'])],api=['key','type'])
D(85,[A(['a label','a description'],['How does','differ from'])])
D(86,[A(['helper text'],['Which part of a field configuration supplies'])])
D(87,[A(['a repeated group of inputs'],['How do I define'])])
D(88,[A(['the configuration for each repeated row'],['Where is','declared'])])
D(89,[A(['related fields'],['How do I group','visually'])])
D(90,[A(['a CSS class'],['Where can I assign'])])
D(91,[A(['the model'],['What does resetting a form mean for'])])
D(92,[A(['a form reset'],['How can I invoke'],['from a button'])])
D(93,[A(['logic'],['Where can I run'],['when a field is initialized'])])
D(94,[A(['a cleanup callback'],['How do I attach'])])
D(95,[A(['an Angular control','the model property it edits'],['What distinguishes','from'],r=[(('it',0),'an Angular control')])])
D(96,[A(['the displayed input','its model property'],['How is','related to'],r=[('its','the displayed input')])])

# Additional manually reviewed source occurrences. These are explicit author
# decisions, not extracted labels or semantic defaults.
def E(num, *, custom=(), literal=(), conditions=(), cues=()):
    row=ROWS[num-1]; q=row['question']
    for kind, selections in [('custom_identifier',custom),('literal',literal)]:
        for selection in selections:
            item=span(q,selection)
            if item not in row['entities'][kind]: row['entities'][kind].append(item)
            # Each E call below concerns a one-aspect question.
            assert len(row['aspects'])==1
            field='identifiers' if kind=='custom_identifier' else 'literals'
            if item not in row['aspects'][0][field]: row['aspects'][0][field].append(item)
    for field,selections in [('conditions',conditions),('request_cues',cues)]:
        for selection in selections: row['aspects'][0][field].append(span(q,selection))

E(37,custom=["'address.zip'","'address'","'zip'"],literal=["'address'","'zip'"])
E(38,custom=["'people'","'name'","'people.0.name'"],literal=["'people'",('0',0),"'name'"])
E(46,custom=[("'a'",0),("'a'",1)])
E(50,conditions=['beside an input'])
E(51,conditions=['in two columns'])
E(79,conditions=['in an expression'])
E(90,conditions=['to a field group'])
E(94,conditions=['to a field'])
# The two independent layout asks each carry only their own CSS identifier.
for ai, token in enumerate(["'col-6'","'grid'"]):
    item=span(ROWS[44]['question'],token)
    ROWS[44]['entities']['custom_identifier'].append(item)
    ROWS[44]['aspects'][ai]['identifiers'].append(item)

assert len(ROWS)==96
assert [x['id'] for x in ROWS]==[x['id'] for x in QUESTIONS]
for row in ROWS: validate_annotation(row)
(ROOT/'train-author.json').write_text(json.dumps(ROWS,ensure_ascii=False,indent=2)+'\n')
print(f'Validated {len(ROWS)} independent TRAIN annotations; {sum(len(r["aspects"]) for r in ROWS)} aspects.')

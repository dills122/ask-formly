"""Hand-authored questions and scenario families; no model, facts or evaluation input."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
# Each line is family|question. Same-family variants remain in the same partition.
TRAIN={
'multi_aspect':'''row-insertion|When an address row is inserted, where is the new row placed and which field receives focus?
row-insertion|After adding two address rows, explain their order and how focus moves between them.
expression-observation|If an expression changes a label, how can I observe the change and unsubscribe from the observation?
expression-observation|For label-change observations, explain subscription setup and cleanup.
field-removal|When a repeated section is removed, what happens to the section's model entries and validation messages?
field-removal|After deleting the middle repeated section, how are the remaining keys and error messages affected?
wrapper-order|With two wrappers around an input, explain their nesting order and where their labels are rendered.
wrapper-order|For nested wrappers, how do I choose the order and inspect the resulting structure?
async-options|While options are loading, how do I show a loading indicator and prevent selection of stale options?
async-options|Once a remote options request completes, how can I replace the choices and expose a request error?
form-reset|Given a populated form, explain resetting the form and choosing the reset target values.
form-reset|For a reset action, describe how to trigger it and how to observe completion.
field-group|When a field group becomes visible, how is the group rendered and how are its child labels displayed?
field-group|If I move a group below another group, what changes in rendering order and keyboard navigation?
config-inheritance|When a custom type extends another type, which defaults are combined and which configuration wins on conflict?
config-inheritance|For inherited type configuration, explain default merging and how to inspect the effective configuration.''',
'negation':'''label-only|How can I update a field label without changing its key?
label-only|Can I change the displayed caption without changing the model path?
options-no-network|How do I populate select choices without making a network request?
options-no-network|Can I refresh locally supplied choices without contacting a server?
messages-preserve-validation|How can I hide an error message without disabling the validator?
messages-preserve-validation|Can I suppress validation text without treating an invalid control as valid?
wrapper-no-template|How can I add a wrapper without editing the field type's template?
wrapper-no-template|Can I remove a surrounding wrapper without modifying the renderer template?
reset-preserve-other|How do I reset one section without resetting the sibling section?
reset-preserve-other|Can I clear one repeated row without clearing the other rows?
focus-negative|How do I add a row but not move keyboard focus to it?
focus-negative|Can a new field appear without taking focus from the current input?
expression-no-mutation|How do I compute a description without mutating the source model?
expression-no-mutation|Can an expression read shared state without writing to it?
required-not-disabled|How can a field be optional but not disabled?
required-not-disabled|Can I remove the required constraint without removing the field?''',
'identifiers_literals':'''typed-config|Where do I declare FormlyFieldConfig<ContactProps> when ContactProps has a field named résumé?
typed-config|How do I express props.helpText on FormlyFieldConfig<ContactProps>?
options-track|With props.options set to [], what choices are displayed?
options-track|For props.options containing { value: 0, label: 'Zero' }, how is 0 represented?
key-path|How does key 'address.zip' differ from key ['address', 'zip']?
key-path|Does key ['people', 0, 'name'] identify a different model location from key 'people.0.name'?
required-literal|With props.required set to false and props.readonly set to true, which input behaviors are requested?
required-literal|What does props.required: true mean for an empty string ''?
expression-string|How do I attach an expression to expressions['props.description']?
expression-string|Where is the callback for expressions['props.required'] configured?
message-token|How do I configure validation.messages['postalCode'] for a validator named 'postalCode'?
message-token|Where is validators.validation: ['postalCode'] declared?
class-string|Where should className: 'col-6' and fieldGroupClassName: 'grid' be placed?
class-string|What is the distinction between className 'a' on a group and className 'a' on a child?
model-literal|Given model = { city: 'Montréal', count: 0 }, which value is addressed by key 'city'?
model-literal|With defaultValue: '' and key: 'note', when is the empty-string default considered?''',
'scope':'''mat-prefix|In Formly 6.3.12 with Material, where is prefix text configured?
mat-prefix|For Material on Formly 6, how do I position prefix content beside an input?
bootstrap-layout|Using Bootstrap with Formly 6.3.12, how do I arrange fields in two columns?
bootstrap-layout|In Formly 6 and Bootstrap, where should group layout classes go?
primeng-options|For PrimeNG on Formly 6, how are select options supplied?
primeng-options|In Formly 6.3.12 with PrimeNG, where is the select placeholder set?
angular-hooks|On Angular 21 with Formly 6.3.12, when does a field's initialization hook run?
angular-hooks|Using Angular 21 and Formly 6, where do I attach field cleanup logic?
adapter-comparison|Between Material and Bootstrap on Formly 6.3.12, how does description placement differ?
adapter-comparison|For Formly 6, compare Material and Bootstrap error-message placement.
version-comparison|Between Formly 6 and Formly 7, how does custom validator registration differ?
version-comparison|Compare validator configuration in Formly 6.3.12 and Formly 7.
scope-local|In Formly 6 with Material, how do I configure an input; in Formly 7 with Bootstrap, how do I configure a textarea?
scope-local|For Material on Formly 6, explain a select label; for PrimeNG on Formly 7, explain a checkbox label.
explicit-core|In Formly 6.3.12 core, without a UI adapter, where are type names registered?
explicit-core|For Formly 6 core without Material, how is a wrapper name associated with a component?''',
'references_ambiguity':'''two-groups-ambiguous|There is a billing group and a shipping group. How do I reset that group?
two-groups-ambiguous|The form contains a personal section and a work section. How can I move it?
one-group-clear|The shipping group contains three fields. How do I reset that group?
one-group-clear|A section named 'delivery' contains the address inputs. How do I move that section?
two-values-ambiguous|I changed the initial value and the current value. Which one does this use?
two-values-ambiguous|A default value and a server value are available. How do I choose that value?
resolved-option|The option is named 'weekly'. How do I select that option?
resolved-option|A validator is registered as 'businessDay'. How do I attach that validator?
two-expressions-ambiguous|One expression controls the label and another controls the description. How do I remove it?
two-expressions-ambiguous|I supplied an expression for required and an expression for readonly. When does that expression run?
resolved-control|The email control is invalid. Where can I inspect its errors?
resolved-control|The phone field has a description. How do I replace that description?
missing-context|How do I stop that behavior for this field?
missing-context|Can this still work when that is absent?
resolved-model|The model contains a property named 'subtotal'. How do I read that property in an expression?
resolved-model|A wrapper named 'panel' surrounds the section. Where do I register that wrapper?''',
'ordinary_comparison':'''validator-location|Where are custom validation functions configured?
validator-location|How do I register a named validation message?
key-versus-type|What is the difference between a field key and a field type name?
key-versus-type|Compare the purpose of key and type in field configuration.
label-description|How does a label differ from a description?
label-description|Which part of a field configuration supplies helper text?
array-basic|How do I define a repeated group of inputs?
array-basic|Where is the configuration for each repeated row declared?
layout-basic|How do I group related fields visually?
layout-basic|Where can I assign a CSS class to a field group?
reset-basic|What does resetting a form mean for the model?
reset-basic|How can I invoke a form reset from a button?
initialization-basic|Where can I run logic when a field is initialized?
initialization-basic|How do I attach a cleanup callback to a field?
compare-control-model|What distinguishes an Angular control from the model property it edits?
compare-control-model|How is the displayed input related to its model property?'''
}
DEV={
'multi_aspect':'''dependent-select-lifecycle|When a country selection invalidates a city choice, how do I refresh the city choices and explain why the old choice disappeared?
submit-progress|During submission, how can I display progress and prevent a second submission?
reordered-identifiers|After dragging a row to a new position, how can I identify the moved row and retain its expanded state?
server-error-routing|When a server returns errors for two fields, where can I attach each error and how can I clear those server errors later?
computed-summary|For a computed summary, explain formatting and recomputation when an input changes.''',
'negation':'''submit-no-touch|How can I check whether submission is allowed without marking every field touched?
no-duplicate-server-check|Can I report a server-side error without running the server check again?
readonly-no-copy|How can I show a read-only preview without copying the model into another object?
no-disable-parent|How do I prevent editing one cell without disabling the entire row?
no-implicit-scope|Can I reuse a configuration without assuming that Material is installed?''',
'identifiers_literals':'''update-on-blur|With modelOptions.updateOn set to 'blur', when is the model updated?
focus-boolean|How do I set focus: true on the field whose key is 'search'?
observable-exact|Where do I subscribe to options.fieldChanges to inspect an event whose type is 'expressionChanges'?
parent-path|How do I read field.parent.model['region'] inside an expression?
array-type-name|For type: 'repeat-block' and fieldArray: { type: 'input' }, which type describes the container?''',
'scope':'''new-adapter-radio|In Formly 6 with Ionic, how do I configure a radio group?
textarea-counter|With Material on Formly 6.3.12, where can I add a character counter to a textarea?
version-expression-notification|In Formly 7, how do I observe expression changes?
angular-model-update|On Angular 20 with Formly 6, when does a blur-triggered update reach the model?
different-adapter-date|Compare date-input configuration for Bootstrap and PrimeNG in Formly 6.3.12.''',
'references_ambiguity':'''two-buttons|There is a save button and a cancel button. How do I hide it?
matched-button|The save button submits the form. How do I hide that button while submission is pending?
ambiguous-container|A tab contains a panel. How do I collapse that container?
matched-panel|The panel named 'totals' contains the summary. How do I collapse that panel?
unbound-instruction|Should I apply the same rule here instead?''',
'ordinary_comparison':'''submission-owner|Which component should handle the form's submit event?
error-placement|Where can I display a form-level error banner?
field-config-array|How do I supply an array of field configurations to a form?
pristine-touched|What is the difference between a pristine control and an untouched control?
observable-vs-expression|How does observing a field change differ from defining an expression?'''
}

def rows(source,prefix):
    result=[]
    for stratum,block in source.items():
        for line in block.splitlines():
            family,question=line.split('|',1)
            result.append({'id':f'{prefix}{len(result)+1:03}', 'question':question,
                           'stratum':stratum,'family':family})
    return result

if __name__=='__main__':
    train=rows(TRAIN,'T');dev=rows(DEV,'D')
    assert len(train)==96 and len(dev)==30
    # Four new training questions per stratum; includes one variant of different families.
    double_ids=[train[base+i]['id'] for base in range(0,96,16) for i in (0,4,8,12)]
    payload={'train':train,'dev':dev,'double_annotate_training_ids':double_ids}
    with (HERE/'questions.json').open('x') as f:json.dump(payload,f,ensure_ascii=False,indent=2)
    print('Authored',len(train),'training and',len(dev),'development questions')

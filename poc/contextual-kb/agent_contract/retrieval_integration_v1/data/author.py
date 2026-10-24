import json
from pathlib import Path
P=Path(__file__).parent
# New development requests authored before foundation/extractor/retrieval outputs.
rows=[
("In Formly 6.3.12, what happens to defaultValue: 7 if a field's model value is already 0?",['defaults-and-resets/defined-value-retention','initial-values/default-value-is-fallback']),
("In Formly, what does options.updateInitialValue() save, and how is that used by options.resetModel()?",['defaults-and-resets/update-initial-value','defaults-and-resets/reset-model']),
("For a hidden Formly field with resetOnHide: false, what happens to its stored model value?",['hiding-and-visibility/reset-on-hide-false']),
("For Formly, why can hiding one of two fields with the same key leave the shared control in place?",['hiding-and-visibility/shared-key-control']),
("In Formly with Material, does extending FieldType by itself supply MatFormFieldControl support?",['material-wrapper-boundaries/core-type-needs-material-bridge']),
("In Formly, how do I register a custom type named 'risk-dial' and select it for key 'riskScore'?",['custom-types-and-wrappers/component-needs-registration','custom-component-use/registered-component-selected-by-type','custom-component-use/key-is-model-type-is-renderer']),
("For Formly 6.3.12, why can expressions['props.disabled'] behave differently from expressions['templateOptions.disabled'] under a disabled ancestor?",['expression-callbacks-and-hooks/disabled-expression-path','expression-callbacks-and-hooks/props-disabled-ancestor-composition']),
("In Formly, what argument does a modern expressions callback receive compared with a legacy expressionProperties callback?",['expression-callbacks-and-hooks/modern-callback-field-argument','expression-callbacks-and-hooks/legacy-callback-arguments']),
("In Formly, who subscribes to and disposes an Observable returned by hooks.onInit?",['expression-callbacks-and-hooks/oninit-observable-managed']),
("For FormlyFieldConfig<MyProps>, does MyProps describe props or the field's model-key schema?",['props-and-registration/props-generic-scope']),
("Does Formly provide refreshFieldOptionsNow to refetch select choices without an application HTTP service?",[]),
("Does Formly options.formState automatically persist to localStorage across a browser restart?",[]),
("In Formly v6.3.12, when can defaultValue: false fill a missing keyed model value?",['defaults-and-resets/default-eligibility','initial-values/default-value-is-fallback']),
("In Formly, does options.resetModel({amount: 0}) accept a new baseline and rebuild field controls?",['defaults-and-resets/reset-model']),
("In Formly, how can hiding a FormArray affect its child values when resetOnHide is enabled?",['hiding-and-visibility/hide-can-clear-array-children']),
("In Formly, after a keyed hidden field becomes visible, what happens to its control registration and defaultValue?",['hiding-and-visibility/show-re-registers','hiding-and-visibility/show-may-reapply-default']),
("In Formly Material, which wrapper owns mat-form-field, and can a wrapper replace a missing value accessor?",['material-wrapper-boundaries/material-form-field-owner','custom-types-and-wrappers/wrapper-decorates-not-control']),
("In Formly, can a type named 'masked-pin' extend input and provide defaultOptions instead of implementing another renderer?",['custom-types-and-wrappers/password-inheritance-example','custom-types-and-wrappers/type-registration-options']),
("For Formly 6.3.12, should constant hide: true and conditionally changing hide be configured the same way?",['expression-callbacks-and-hooks/constant-vs-conditional-hide']),
("In Formly, how do options.checkExpressions(field) and options.detectChanges(field) differ?",['expression-callbacks-and-hooks/expression-check-operations']),
("In Formly, does subscribing manually inside hooks.onInit get the same cleanup as returning an Observable?",['expression-callbacks-and-hooks/manual-subscribe-cleanup','expression-callbacks-and-hooks/oninit-observable-managed']),
("In Formly v6, are templateOptions and props unrelated configuration objects?",['props-and-registration/props-template-options-alias']),
("Does Formly options.formState encrypt payment details before writing them to a server?",[]),
("In Formly, which option configures automatic HTTP retries and exponential backoff for a remote validator?",[]),
("In Formly, should a computed initial amount available before field build go into the model or defaultValue?",['initial-values/model-preferred-for-computed-initial']),
("In Formly, what can a qualifying changed model input do to the FormlyForm field tree?",['initial-values/changed-model-input-rebuilds']),
("In Formly, are lazyRender and resetOnHide enabled in the default registry?",['hiding-and-visibility/lazy-render-default','hiding-and-visibility/reset-on-hide-default']),
("In Formly, can hiding a field unregister its control and remove its model value?",['hiding-and-visibility/hide-unregisters-control','hiding-and-visibility/hide-can-clear-model-value']),
("In Formly, what is FieldWrapper.fieldComponent used for when decorating a field?",['custom-types-and-wrappers/wrapper-insertion-point']),
("In Formly, how are defaultOptions from a registered type merged with values explicitly supplied in a field configuration?",['custom-types-and-wrappers/reverse-merged-defaults','props-and-registration/registration-adds-configuration']),
("In Formly, what is the default checkExpressionOn setting, and what does modelChange mean in that setting?",['expression-callbacks-and-hooks/model-change-check-default']),
("For Formly, which field context can FieldType access, including props, model and formControl?",['custom-types-and-wrappers/fieldtype-surface']),
("In Formly, how can options.formState supply shared context to several fields?",['props-and-registration/form-state-shared-context']),
("In Formly, can key be a number such as 0 or a path array such as ['account', 'code'] rather than a string?",['props-and-registration/key-shapes']),
("Does Formly pauseExpressionsNow stop expression updates until I call resumeExpressionsNow?",[]),
("In Formly, can resetOnHide: false automatically save hidden values in sessionStorage when I navigate away?",[]),
]
result=[]
for i,(text,ids) in enumerate(rows,1):
 result.append(dict(id=f'R{i:02}',batch=(i-1)//12+1,request=text,relevant_fact_ids=ids,expected_support='direct_or_partial' if ids else 'not_established_in_catalog'))
(P/'cases-initial.json').write_text(json.dumps(result,indent=2))
for batch in (1,2,3):
 (P/f'batch{batch}.json').write_text(json.dumps({'requests':[{'id':r['id'],'request':r['request']} for r in result if r['batch']==batch]},indent=2))

# N1 pinned source notes

Candidate-only Formly6.3.12 implementation notes; original frozen guides unchanged. Each claim is grounded in the linked full pinned implementation, not independently established by this note.

Material radio consumes props.options through formlySelectOptions and async. Each radio button binds option.value and option.disabled and displays option.label. [K50](sources.md#k50) [K15](sources.md#k15)

Material radio defaults props.tabindex to -1. After view initialization it observes field.focus; when tabindex is -1, focus is truthy and radios exist, it schedules focus on the selected radio or otherwise the first radio. It unsubscribes the focus observer on destruction. [K50](sources.md#k50)

FormlyMatRadioModule registers radio with FormlyFieldRadio and the form-field wrapper. The Material aggregate module imports FormlyMatRadioModule. [K79](sources.md#k79) [K13](sources.md#k13)

Material native-select consumes props.options through formlySelectOptions and async, renders native option/optgroup elements, binds option and child values with ngValue, and binds their disabled state. A truthy props.placeholder adds an option whose ngValue is undefined. [K55](sources.md#k55) [K15](sources.md#k15)

Material native-select binds readonly from props.readonly, required from required, name from field.name, id, errorStateMatcher, formControl and formlyAttributes on select matNativeControl. [K55](sources.md#k55)

FormlyMatNativeSelectModule registers native-select with FormlyFieldNativeSelect and the form-field wrapper. FormlyMaterialModule does not import the native-select module. [K80](sources.md#k80) [K13](sources.md#k13)

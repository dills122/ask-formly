# Pre-inference annotation panel

## P02-r1-q0
What Formly library concepts are needed to implement a new type called 'ratingDial'?
[{"start": 71, "end": 83, "text": "'ratingDial'", "role": "registration_name"}]

## P04-r1-q0
For Formly, given the current setup described as "I have not registered 'currencyBadge' yet", how do I register the type 'currencyBadge'?
[{"start": 72, "end": 87, "text": "'currencyBadge'", "role": "registration_name"}, {"start": 121, "end": 136, "text": "'currencyBadge'", "role": "registration_name"}]

## P06-r1-q0
In Formly, can a wrapper be applied without changing the field's type?
[]

## P08-r1-q0
What does the key property mean in a Formly field configuration?
[{"start": 14, "end": 17, "text": "key", "role": "api_reference"}]

## P10-r1-q0
For Formly core only, with no UI adapters, how is a field key related to a model path?
[{"start": 58, "end": 61, "text": "key", "role": "api_reference"}]

## P12-r1-q0
For Formly v6.3.12 with Material, how do I configure a label?
[{"start": 11, "end": 18, "text": "v6.3.12", "role": "version"}, {"start": 24, "end": 32, "text": "Material", "role": "ui_adapter"}]

## P14-r1-q0
For Formly >=6.2 <7 using Material, how is props.disabled configured?
[{"start": 13, "end": 16, "text": "6.2", "role": "version"}, {"start": 18, "end": 19, "text": "7", "role": "version"}, {"start": 26, "end": 34, "text": "Material", "role": "ui_adapter"}, {"start": 43, "end": 57, "text": "props.disabled", "role": "api_reference"}]

## P16-r1-q0
For Formly v6.3.12, how do I set props.placeholder with Material?
[{"start": 11, "end": 18, "text": "v6.3.12", "role": "version"}, {"start": 33, "end": 50, "text": "props.placeholder", "role": "api_reference"}, {"start": 56, "end": 64, "text": "Material", "role": "ui_adapter"}]

## P18-r1-q0
For a Formly field with defaultValue: 0, what happens at initial build if the model path is absent?
[{"start": 24, "end": 36, "text": "defaultValue", "role": "api_reference"}, {"start": 38, "end": 39, "text": "0", "role": "value"}]

## P20-r1-q0
For a Formly field, how can I observe changes to props.required without subscribing to valueChanges?
[{"start": 49, "end": 63, "text": "props.required", "role": "api_reference"}, {"start": 87, "end": 99, "text": "valueChanges", "role": "api_reference"}]

## P22-r1-q0
After a Formly field has been hidden and is visible again, how can I inspect its FormControl under the restriction "do not read the model"?
[{"start": 81, "end": 92, "text": "FormControl", "role": "api_reference"}]

## P24-r1-q0
In Formly, how does defaultValue: '' compare with defaultValue: false when the model value is undefined?
[{"start": 20, "end": 32, "text": "defaultValue", "role": "api_reference"}, {"start": 34, "end": 36, "text": "''", "role": "value"}, {"start": 50, "end": 62, "text": "defaultValue", "role": "api_reference"}, {"start": 64, "end": 69, "text": "false", "role": "value"}, {"start": 94, "end": 103, "text": "undefined", "role": "value"}]

## P26-r1-q0
Using Formly v6.3.12 with Material, how do I configure props.required to depend on model.delivery === 'courier'?
[{"start": 13, "end": 20, "text": "v6.3.12", "role": "version"}, {"start": 26, "end": 34, "text": "Material", "role": "ui_adapter"}, {"start": 55, "end": 69, "text": "props.required", "role": "api_reference"}, {"start": 83, "end": 111, "text": "model.delivery === 'courier'", "role": "value"}]

## P28-r1-q0
For Formly core only, how do expressions['props.disabled'] and expressionProperties['templateOptions.disabled'] compare for making disabled depend on options.formState.busy, including whether each supplied API spelling is supported; do not silently rewrite either spelling?
[{"start": 29, "end": 58, "text": "expressions['props.disabled']", "role": "api_reference"}, {"start": 63, "end": 111, "text": "expressionProperties['templateOptions.disabled']", "role": "api_reference"}, {"start": 150, "end": 172, "text": "options.formState.busy", "role": "api_reference"}]

## P30-r1-q0
In Formly, a field already has an async validator registered as 'remoteCode'. How do I attach the async validator registered as 'remoteCode' to a field configuration?
[{"start": 64, "end": 76, "text": "'remoteCode'", "role": "registration_name"}, {"start": 128, "end": 140, "text": "'remoteCode'", "role": "registration_name"}]

## P32-r1-q0
In Formly, how do I observe changes in validation status without subscribing to modelChange?
[{"start": 80, "end": 91, "text": "modelChange", "role": "api_reference"}]

## P34-r1-q0
Can Formly observe expression changes without polling?
[]

## P36-r1-q0
For Formly v6, how do I configure props.placeholder to depend on options.formState.region?
[{"start": 11, "end": 13, "text": "v6", "role": "version"}, {"start": 34, "end": 51, "text": "props.placeholder", "role": "api_reference"}, {"start": 65, "end": 89, "text": "options.formState.region", "role": "api_reference"}]

## P38-r1-q0
For Formly with Bootstrap, does a field accept more than one wrapper?
[{"start": 16, "end": 25, "text": "Bootstrap", "role": "ui_adapter"}]

## P40-r1-q0
For Formly, can an expression depend on form state?
[]

## P42-r1-q0
With Formly core only, how does resetOnHide: false compare with resetOnHide: true for a field whose model value is 0 when hidden? Compare model-value behavior, not rendered appearance.
[{"start": 32, "end": 43, "text": "resetOnHide", "role": "api_reference"}, {"start": 45, "end": 50, "text": "false", "role": "value"}, {"start": 64, "end": 75, "text": "resetOnHide", "role": "api_reference"}, {"start": 77, "end": 81, "text": "true", "role": "value"}, {"start": 115, "end": 116, "text": "0", "role": "value"}]

## P44-r1-q0
Does Formly expose an API called 'pauseExpressionsNow'? Verify the API name; do not correct it to something else.
[{"start": 34, "end": 53, "text": "pauseExpressionsNow", "role": "api_reference"}]

## P46-r1-q0
In Formly, how does resetOnHide: undefined compare with resetOnHide: false for the model value when hidden?
[{"start": 20, "end": 31, "text": "resetOnHide", "role": "api_reference"}, {"start": 33, "end": 42, "text": "undefined", "role": "value"}, {"start": 56, "end": 67, "text": "resetOnHide", "role": "api_reference"}, {"start": 69, "end": 74, "text": "false", "role": "value"}]

## P48-r1-q0
(no derived question; empty control)
[]

## I01-q0
In Formly 6.3.12 with Material, how do I register a custom type named 'ssn-entry'? Do not include application-specific formatting code.
[{"start": 10, "end": 16, "text": "6.3.12", "role": "version"}, {"start": 22, "end": 30, "text": "Material", "role": "ui_adapter"}, {"start": 70, "end": 81, "text": "'ssn-entry'", "role": "registration_name"}]

## I01-q1
In Formly 6.3.12 with Material, how do I use the custom type named 'ssn-entry' after registering it, for key 'taxId'? Do not include application-specific formatting code.
[{"start": 10, "end": 16, "text": "6.3.12", "role": "version"}, {"start": 22, "end": 30, "text": "Material", "role": "ui_adapter"}, {"start": 67, "end": 78, "text": "'ssn-entry'", "role": "registration_name"}, {"start": 105, "end": 108, "text": "key", "role": "api_reference"}, {"start": 109, "end": 116, "text": "'taxId'", "role": "model_key"}]

## I02-q0
In Formly, can I observe a field becoming disabled without polling?
[]

## I02-q1
In Formly, what event information would an observer of a field becoming disabled without polling provide?
[]

## I03-q0
For Formly v6, how do `props.disabled` with `hide` compare when `resetOnHide` is false?
[{"start": 11, "end": 13, "text": "v6", "role": "version"}, {"start": 23, "end": 37, "text": "props.disabled", "role": "api_reference"}, {"start": 45, "end": 49, "text": "hide", "role": "api_reference"}, {"start": 65, "end": 76, "text": "resetOnHide", "role": "api_reference"}, {"start": 81, "end": 86, "text": "false", "role": "value"}]

## I03-q1
For Formly v6, what does `defaultValue` do when the model value is undefined?
[{"start": 11, "end": 13, "text": "v6", "role": "version"}, {"start": 26, "end": 38, "text": "defaultValue", "role": "api_reference"}, {"start": 67, "end": 76, "text": "undefined", "role": "value"}]

## I04-q0
How do I register the wrapper 'audit-frame' in Formly?
[{"start": 30, "end": 43, "text": "'audit-frame'", "role": "registration_name"}]

## I04-q1
In Formly, how do I apply the wrapper 'audit-frame' after registering it to a field whose key is 'audit-frame'?
[{"start": 38, "end": 51, "text": "'audit-frame'", "role": "registration_name"}, {"start": 90, "end": 93, "text": "key", "role": "api_reference"}, {"start": 97, "end": 110, "text": "'audit-frame'", "role": "model_key"}]

## I05-q0
In Formly, can `expressions['props.required']` depend on `model.needsReview` without subscribing manually?
[{"start": 16, "end": 45, "text": "expressions['props.required']", "role": "api_reference"}, {"start": 58, "end": 75, "text": "model.needsReview", "role": "value"}]

## I05-q1
In Formly, If supported, how do I configure the dependency in which `expressions['props.required']` depend on `model.needsReview` without subscribing manually?
[{"start": 69, "end": 98, "text": "expressions['props.required']", "role": "api_reference"}, {"start": 111, "end": 128, "text": "model.needsReview", "role": "value"}]

## I06-q0
What does Formly's `options.fieldChanges` expose?
[{"start": 20, "end": 40, "text": "options.fieldChanges", "role": "api_reference"}]

## I06-q1
In Formly, how do I register a type without changing the model?
[]

## I07-q0
For Formly with Bootstrap rather than Material, how do I set `props.placeholder` to 'Choose a region' while keeping key 'regionCode'?
[{"start": 16, "end": 25, "text": "Bootstrap", "role": "ui_adapter"}, {"start": 38, "end": 46, "text": "Material", "role": "ui_adapter"}, {"start": 62, "end": 79, "text": "props.placeholder", "role": "api_reference"}, {"start": 84, "end": 101, "text": "'Choose a region'", "role": "value"}, {"start": 116, "end": 119, "text": "key", "role": "api_reference"}, {"start": 120, "end": 132, "text": "'regionCode'", "role": "model_key"}]

## I08-q0
In Formly, what is the distinction between a validator registered as 'positiveAmount' and `validation.messages['positiveAmount']`?
[{"start": 69, "end": 85, "text": "'positiveAmount'", "role": "registration_name"}, {"start": 91, "end": 128, "text": "validation.messages['positiveAmount']", "role": "api_reference"}]

## I09-q0
Does Formly provide `refreshFieldOptionsNow`?
[{"start": 21, "end": 43, "text": "refreshFieldOptionsNow", "role": "api_reference"}]

## I09-q1
If so, meaning if Formly provides `refreshFieldOptionsNow`, what arguments does `refreshFieldOptionsNow` accept, without assuming that this method exists?
[{"start": 35, "end": 57, "text": "refreshFieldOptionsNow", "role": "api_reference"}, {"start": 81, "end": 103, "text": "refreshFieldOptionsNow", "role": "api_reference"}]

## I10-q0
Can a Formly field use `defaultValue: 0` when its model value is null? I am not asking how to change our application's data loader.
[{"start": 24, "end": 36, "text": "defaultValue", "role": "api_reference"}, {"start": 38, "end": 39, "text": "0", "role": "value"}, {"start": 65, "end": 69, "text": "null", "role": "value"}]

## I11-q0
In Formly, can I observe value changes only while a field is enabled, without polling?
[]

## I11-q1
In Formly, how do I stop the proposed observer of value changes only while a field is enabled, without polling, when the form is destroyed?
[]

## I12-empty
(no derived question; empty control)
[]

# Core configuration and lifetime boundaries

Pinned Formly 6.3.12 source interpretation; fresh source inspection only. No sealed or historical evaluation artifacts were used. Source inspection does not claim execution qualification.

key: 0 is a key, while null, undefined, an empty string and an empty array are keyless. String keys split on dots and replace bracket segments matching [wordCharacters] with dot segments; array keys supply literal segments, so ["a.b"] differs from "a.b". [K39](sources.md#k39)

Control lookup first returns an existing field.formControl. Otherwise shareFormControl === false skips parent-form lookup; otherwise Formly looks up the field key path in the parent form. Thus fields at the same path can reuse a control. [K42](sources.md#k42) [K43](sources.md#k43)

When a control has multiple registered fields, Formly composes validators from participating fields whose internal hide state is false. It also collects validators through keyless child groups. Shared control validity therefore need not belong to only the widget being edited. [K43](sources.md#k43)

When a fields input change is processed with a form present, FormlyForm calls clearControl recursively, clearing synchronous/asynchronous validators and internal field registrations. The form extension can then install configured composed validators during the rebuild. [K11](sources.md#k11) [K42](sources.md#k42) [K43](sources.md#k43)

reverseDeepMerge fills destination properties that are null, undefined or an empty string by cloning source defaults. It preserves false and zero, and recursively merges objects only when both are objects with the same prototype and neither is an array. [K39](sources.md#k39) [K04](sources.md#k04)

reverseDeepMerge does not recursively merge arrays. An existing destination array, including an empty array, survives this default-filling operation; a null, undefined or empty-string destination instead receives a clone of the source value. [K39](sources.md#k39) [K04](sources.md#k04)

Formly clone preserves functions, Observables, TemplateRef and selected special values by reference; copies Dates and Uint8Array/Uint16Array/Uint32Array; shallow-copies Set elements and Map entries; maps AbstractControl to null; and recursively clones arrays and ordinary enumerable object properties while preserving getter descriptors. [K40](sources.md#k40)

With extras.immutable enabled, the host setField path combines its existing field with a clone of incoming model, fields or options data. This uses Formly specialized clone and does not freeze the resulting field or control structures. [K11](sources.md#k11) [K40](sources.md#k40)

props.attributes is applied by formlyAttributes with Renderer2.setAttribute/removeAttribute on the DOM element. Non-null entries become attributes; replacing the attributes object removes its previous keys. This does not bind arbitrary Angular component inputs or implement validators or a value accessor. [K37](sources.md#k37) [K01](sources.md#k01)

Field hooks are invoked by the outer FormlyField component: onChanges responds to its field input changes, and destruction runs cleanup and onDestroy. Lazy hiding clears the inner rendered container while the outer component can remain alive; showing renders the inner type/wrappers again. [K41](sources.md#k41)

field.template is rendered through an innerHtml binding by FormlyTemplateType. props.safeHtml selects bypassSecurityTrustHtml; it does not compile that string as an Angular template. For Angular bindings use a registered component type or a declared ng-template with formlyTemplate and a matching field.type. [K59](sources.md#k59) [K46](sources.md#k46) [K41](sources.md#k41)

Formly compiles string expressions with the JavaScript Function constructor and model, formState and field arguments. This is executable JavaScript, not a sandboxed JSON rule interpreter. [K60](sources.md#k60) [K07](sources.md#k07)

The 6.3.12 core public barrel exports FormlyModule, FormlyConfig, ConfigOption and named type/wrapper bases, alongside several integration exports prefixed with ɵ. It does not export provideFormlyConfig. The pinned core module supplies forRoot and forChild NgModule configuration. [K02](sources.md#k02) [K03](sources.md#k03)

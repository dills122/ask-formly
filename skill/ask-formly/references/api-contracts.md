# API contracts that change implementation choices

Baseline: 6.3.12. Use this reference for detailed configuration reading and authoring. [API map](api-map.md) is the entry-point index; this file covers less obvious contracts.

## Keys, model scope, and shared controls

`key: 0` is a key; null, undefined, an empty string, and an empty path array are treated as keyless. String keys containing dots are split into paths, and simple bracket segments are normalized. An array key supplies literal path segments, so `['a.b']` differs from `'a.b'`. This parser is not a general JavaScript property-expression parser. Avoid assuming quoted bracket syntax is supported. [K39](sources.md#k39)

Control lookup first honors an existing `field.formControl`, then the sharing policy, then the parent form's key path. Fields with the same path can share a control. Validators from visible participating fields can be merged onto it. Thus two visually separate fields need not have independent validity or disabled state. Inspect `shareFormControl` and registrations before changing a duplicate-key form. [K42](sources.md#k42), [K43](sources.md#k43)

Internal control registration can clear and reconstruct validators. Prefer the Formly validator configuration for persistent rules rather than assuming an ad-hoc `setValidators()` survives every rebuild. Manually supplied controls need a focused integration test. Do not call internal registration utilities as an everyday application API. [K42](sources.md#k42), [K43](sources.md#k43)

## Value changes, parsers, and modelOptions

There are several event surfaces, with different purposes:

| Surface | Meaning and caution |
| --- | --- |
| Angular `control.valueChanges` | Control change stream; do not equate it with a completed root-model transaction |
| `options.fieldChanges` with `type: 'valueChanges'` | Formly field-level update after its model-assignment path |
| `options.fieldChanges` with `type: 'expressionChanges'` | Expression result/property update; filter by field and property |
| `<formly-form (modelChange)>` | Host-level model output after Formly's expression-check path; emitted model is cloned |
| `props.change` | UI callback forwarded by the renderer/directive; not a replacement for the control binding and not a universal programmatic-value event |

Evidence: [K11](sources.md#k11), [K41](sources.md#k41), [K37](sources.md#k37), [K14](sources.md#k14).

`modelOptions.updateOn` accepts change, blur, or submit. `modelOptions.debounce` has shape `{ default: milliseconds }`, not a bare number. In the inspected field subscription, debounce applies only for absent/change updateOn. It delays Formly's model propagation; do not infer that it debounces Angular validation or HTTP requests. [K01](sources.md#k01), [K41](sources.md#k41)

Parsers run along the field value-change pipeline. Use idempotent normalization: the implementation can write a parsed value back to the control. A parser that changes its result every invocation can create repeated updates. **Observed limitation:** with `debounce.default: 5`, the probe's uppercase parser was bypassed and the model retained `abc`; without debounce it became `ABC`. Inspect this combination before using it for schema number conversion or data normalization. See R10/R11 in [runtime evidence](runtime-evidence.md). The source reassigns the pipeline to raw `control.valueChanges.pipe(debounceTime(...))`. [K41](sources.md#k41)

Do not promise that a parser keeps the typed text separate from the normalized model. With the ordinary Material input, removing debounce and typing `abc` produced `ABC` in the input, control, and model in the focused zoneless probe. If raw text must remain visible, preserve it in a deliberate draft/control representation and derive the uppercase lookup/submission value separately, or design and test a custom value accessor with distinct view/model representations. Do not silently sacrifice either requirement. Debounce backend lookups in their own stream and define when an old request becomes stale; see [request lifetime](async-and-state.md#debounced-lookups-and-immediate-invalidation) and [pilot evidence](evaluation-lessons.md).

## Defaults, merges, and cloning are different operations

The rule “defaultValue applies to undefined model values” must not be generalized to configuration merging. The `reverseDeepMerge` utility fills destination values that are null, undefined, **or empty string**; recursively merges compatible objects; and does not recursively merge arrays. Explicit false and zero survive this merge. A blank label may therefore behave differently from an intentionally false flag when type defaults are applied. [K39](sources.md#k39), [K04](sources.md#k04)

Formly's clone is specialized, not JSON stringify/parse or a guarantee of universal deep copying. It preserves functions/Observables and certain browser values, copies Dates and supported typed arrays, shallow-copies Map/Set entries, and treats AbstractControl specially. Do not retain built field configs as JSON persistence or assume `immutable` makes every nested application object deeply immutable. `extras.immutable` clones incoming host field data; the runtime still builds mutable field/control structures. [K40](sources.md#k40), [K11](sources.md#k11)

## Props, attributes, and event callbacks

Core props are a vocabulary; the renderer decides which UI component inputs it actually consumes. `props.attributes` supplies DOM attributes, not arbitrary Angular inputs, event handlers, or validators. `formlyAttributes` supplies IDs, names, focus/blur coordination, selected attributes, and callbacks. It does not implement a value accessor for a custom widget. [K01](sources.md#k01), [K37](sources.md#k37)

For a custom input, bind the provided `formControl`, use the relevant attributes directive, and expose only meaningful props. A callback such as `props.change(field, event)` is supplemental behavior; calling it alone does not update the Formly model. See [I3572](bug-ledger.md#i3572).

## Hook lifetime versus render lifetime

Field hooks belong to `FormlyField`. `onChanges` responds to changes of its field input, not every model edit. Type/wrapper components created inside it have their own Angular lifecycle. With lazy rendering, hiding clears the rendered container; do not assume that every hide/show creates a new outer FormlyField or reruns every field hook. Keep subscriptions with their actual owner. [K41](sources.md#k41)

Use the typed Observable return from `hooks.onInit` for managed subscription ownership when appropriate. An ignored `.subscribe()` is not automatically cleaned up by Formly. Inspect lifecycle behavior before putting fetching, parent registration, or repeated side effects into hooks. [K01](sources.md#k01), [K10](sources.md#k10)

## Inline templates, presets, and registration

`field.template` is rendered as HTML. It is not compiled as a new Angular template, so arbitrary component bindings inside a server-provided string do not become Angular code. Use a registered type or the declared `ng-template formlyTemplate="name"` mechanism for Angular templates. `props.safeHtml` opts into a sanitizer bypass; it is not a generic fix for dynamic rendering. [K46](sources.md#k46), [K59](sources.md#k59)

String expressions use the JavaScript `Function` constructor in this release. They are executable expressions, not a sandboxed JSON rule language. For an application with untrusted schemas or a restrictive CSP, use a controlled mapping to authored functions/approved behaviors; do not claim v6 supplies a safe expression interpreter. [K60](sources.md#k60)

Preset substitution runs at priority -300 before core's -250. It removes the preset reference type from the merge input, obtains configuration from a stored config or `getConfiguration()`, and applies reverse defaults. Use a fresh factory when presets contain runtime state. Missing preset names and recursive composition require explicit checking; presets are not a full schema language. [K44](sources.md#k44), [K03](sources.md#k03)

V6 configuration is NgModule-based. A standalone Angular host can consume modules, and the pinned FAQ points to an `importProvidersFrom` integration discussion. A user-defined helper called `provideFormlyConfig` in that discussion is not a v6 package export. Check environment/provider scope, particularly dialogs and lazy routes. [K46](sources.md#k46), [I3721](bug-ledger.md#i3721)

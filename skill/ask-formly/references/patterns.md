# Patterns and anti-patterns

These are v6.3.12-oriented engineering recommendations grounded in the linked contracts and cases. “Prefer” is contextual guidance, not an upstream guarantee. Checks are proposed unless a runtime probe is named.

## P01 — Construct fresh field configurations

Use a factory for independent forms, passing services/streams as dependencies. Built fields receive parent/control/options links and observation state. Avoid reusing one built object graph across separate form instances or persisting it as JSON. Check that editing/resetting one form leaves another independent. [K05](sources.md#k05), [K40](sources.md#k40), [I3541](bug-ledger.md#i3541)

## P02 — Separate layout from model nesting

Use keyless groups for layout and keyed groups for nested data. A layout-only key changes payload and callback scope. Check both; see [configuration](config-and-model.md) and [key contracts](api-contracts.md#keys-model-scope-and-shared-controls).

## P03 — Make hidden-data retention explicit

Use `resetOnHide: false` when hiding should preserve input; use clearing when the branch is no longer applicable. Avoid treating “hidden” as CSS-only or retaining obsolete branch values accidentally. Check hide → show, validation, and final payload. R02/R03 exercise both policies. [Expressions](expressions-and-lifecycle.md)

## P04 — Distinguish readonly, disabled, and display-only

Choose by interaction, validation, and payload requirements. Avoid swapping disabled for readonly merely to prevent edits; their form-value consequences differ. For Material widgets without a demonstrated readonly contract, use an intentional display mode or custom type. Check keyboard behavior and model/value/raw-value separately. R04 covers one disabled-group case. [Material controls](material-controls.md)

## P05 — Keep expressions cheap and repeatable

Use expressions to derive properties, with stable results and minimal side effects. Avoid HTTP requests, subscriptions, or expensive transformations inside a frequently reevaluated callback. Precompute or supply a stream when appropriate. Measure model edits and resets, not only initial render. [Performance](performance.md), [I3799](bug-ledger.md#i3799)

## P06 — Supply Observable expressions directly

Supply the Observable itself; a callback returning it is not flattened. Test initialization, subsequent emissions and teardown. See [stream contracts](async-and-state.md#expressions-a-stream-is-not-a-function-returning-a-stream); R06 verifies direct Boolean emissions.

## P07 — Give dependent selects a retention policy

Choose clear, reject or historical-value retention when options change. Preserve valid initial selections during loading; test empty parents, unavailable selections, reordered objects, stale responses and errors. See [dependent selects](async-and-state.md#dependent-remote-selects).

## P08 — Match select value identity to the domain

Prefer primitive IDs when that is the payload contract; use `compareWith` when object-valued selection is intentional. Avoid using an object comparator to conceal inconsistent ID/string/number types. Test replacing options with newly allocated objects and multiple selection. [K14](sources.md#k14)

## P09 — Match the validator return contract

Use the correct Angular null/error or named Formly Boolean contract, then test valid/invalid values and messages. See [validation](validation.md); R05 exercises both contracts.

## P10 — Place relational validation at its dependency scope

Validate siblings through their common group, or explicitly wire revalidation. Avoid a leaf rule that silently goes stale when only the other field changes. For async rules, inspect whether the chosen group includes unrelated invalid fields. Test changes to each dependency; R17 covers a synchronous group rule. [I4022](bug-ledger.md#i4022), [E04](examples.md#e04)

## P11 — Separate validation from message presentation

Inspect validity, touched/submitted/show state and message resolution separately; a validator does not imply a friendly message. See [validation](validation.md#built-ins-and-messages), [message precedence](async-and-state.md#translation-and-messages); R08 checks local override.

## P12 — Use the provided control in custom types

Bind the supplied control to a compatible accessor; do not create a parallel ngModel path or use props.change as its replacement. For Material, test the [three integration contracts](material-controls.md#custom-material-controls); R09 covers a simple custom input.

## P13 — Assign each wrapper a clear responsibility

Keep types responsible for controls and wrappers for decoration/layout. Check inherited wrappers before adding another form-field; test one correct DOM/label/error structure. See [customization](customization.md) and [Material integration](material-controls.md#custom-material-controls).

## P14 — Make build extensions idempotent

Choose prePopulate/onPopulate/postPopulate for the needed stage and explicit priority where ordering matters. Avoid appending the same wrapper/validator on every rebuild or fetching data in generic build traversal. Test initial build, rebuild, and repeated section insertion. [K06](sources.md#k06), [K35](sources.md#k35), [E06](examples.md#e06)

## P15 — Keep array operations coordinated

Use the registered FieldArrayType integration for dynamic sections. Avoid updating only model, fieldGroup, or FormArray and assuming the others follow immediately. Test insert/remove at first, middle, and last positions with row-specific state. V6.3.12 also loses falsy `initialModel` arguments in `add`; R14 demonstrates false falling through to a default. [Arrays](arrays.md), [I3957](bug-ledger.md#i3957)

## P16 — Treat reset as a product behavior

Decide whether reset restores the original load or last save. Use the intended updateInitialValue checkpoint, not raw form.reset as an assumed substitute. Test save → edit → reset and defaults. [Configuration](config-and-model.md); R07.

## P17 — Normalize without creating update loops

Use idempotent normalization and distinguish model timing, visible text and request timing. Parser plus modelOptions debounce has a reproduced limitation. Read [API contracts](api-contracts.md#value-changes-parsers-and-modeloptions) before choosing the boundary; R10/R11.

## P18 — Use explicit consent validation

When the business rule is “must be true,” express that rule with `Validators.requiredTrue` or equivalent and test false/null/true. Avoid inferring affirmative consent solely from an asterisk or generic required prop. Separate future-required decoration from present validity using a custom wrapper. [K08](sources.md#k08), [I3855](bug-ledger.md#i3855); R12 tests explicit true-only validation.

## P19 — Own subscriptions deliberately

Return a supported onInit Observable or explicitly dispose subscriptions with their owner. onChanges is not every value edit, and lazy hiding is not guaranteed outer-field destruction. Test hide/show, replacement and final teardown. [Lifecycle contracts](api-contracts.md#hook-lifetime-versus-render-lifetime).

## P20 — Use JSON Schema conversion as a UI mapping layer

Supply required renderers and test the actual generated form. Avoid claiming complete JSON Schema validation, remote-ref resolution, or automatic date/email handling from conversion alone. Treat map/widget overrides as code with its own semantics. Test branch changes and payload normalization. [JSON Schema](json-schema.md)

## P21 — Treat JSON expressions as executable policy

Keep server-provided schema declarative through a controlled mapping when trust or CSP requires it. Avoid treating v6 string expressions as a safe sandbox, or safeHtml as a general rendering fix. Use authored templates/components for Angular bindings. [K60](sources.md#k60), [K59](sources.md#k59)

## P22 — Reconcile state-store boundaries

Use fresh incoming config/model boundaries and intentional modelChange handling. Avoid assuming immutable mode freezes runtime fields, or feeding every emitted clone back into an uncontrolled rebuild loop. Test edit/reset behavior and external model replacement with the real store. [K11](sources.md#k11), [K40](sources.md#k40)

## P23 — Design tabs and steps around validation scope

Use groups to represent steps and decide whether inactive-step data remains active/validated. Avoid hiding every inactive step with default reset-on-hide when the intended behavior is preserving a draft. The official Material tabs example recursively checks groups; it is a starting pattern, not a complete async wizard. Test back navigation, invalid and pending steps, and submission. [E11](examples.md#e11)

## P24 — Diagnose with the patch history before patching internals

Match installed version, source and reproduced transition before patching internals. Issue closure or an old workaround is not current fix evidence. [Bug ledger](bug-ledger.md) and [performance](performance.md).

## Angular 21 qualification of these patterns

Selected patterns have [zoneless/AOT/browser evidence](angular21-qualification.md); they do not certify every recipe. For async options, assert focus, keyboard selection and model updates separately from option rendering.

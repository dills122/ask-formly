# Diagnose a Formly problem

Start with expected behavior, actual behavior, resolved package versions, and the smallest relevant field/model/registration slice. A visual symptom can originate in configuration, the Formly build, Angular controls, a UI adapter, or application code. Rank causes from evidence; do not call a plausible explanation a reproduced bug.

| Symptom | Inspect first | Evidence route |
| --- | --- | --- |
| Unknown type or missing renderer | Type name, module imports, registrations, JSON Schema structural types | [Customization](customization.md), [JSON Schema](json-schema.md) |
| Value disappears when hidden | `resetOnHide`, effective default, hide transitions, nesting | [Expressions](expressions-and-lifecycle.md), [K05](sources.md#k05), [K07](sources.md#k07) |
| Hidden value retained but control absent | Distinguish model retention from control registration and validation | [K07](sources.md#k07), [K09](sources.md#k09) |
| Expression reads the wrong object | Group model scope; public versus legacy callback signature | [Configuration](config-and-model.md), [Expressions](expressions-and-lifecycle.md) |
| Validator always passes/fails | Angular null/error-object contract versus named expression boolean | [Validation](validation.md) |
| Errors exist but message is absent | Touched/submitted/show state, message key, group error path | [Validation](validation.md), [E04](examples.md#e04) |
| Select fails keyboard selection after replacing the active option while open | Separate option rendering, active item, focus and model; bare Material also reproduced this case | [Q01](angular21-qualification.md#q01-replacing-the-active-select-option-while-the-panel-is-open) |
| Parser/model value differs under debounce | ModelOptions pipeline and normalization/view boundary | [API contracts](api-contracts.md#value-changes-parsers-and-modeloptions) |
| Select loses selection after reload | Value type, option identity, `compareWith`, dependent-value policy | [Material](material.md), [E02](examples.md#e02) |
| Repeater count/model diverges | FieldArrayType usage, direct array mutation, index/key handling | [Arrays](arrays.md), [K12](sources.md#k12) |
| Date constraints are ignored | Datepicker entry point, nested options, adapter/value type | [Material](material.md) |
| Reset produces an unexpected value | Initial model snapshot, updateInitialValue, default versus supplied model | [Configuration](config-and-model.md), [E07](examples.md#e07) |
| Behavior differs across v6 patches | Actual lockfile version and relevant changelog/source delta | [Version policy](version-policy.md), [K29](sources.md#k29) |
| Custom OnPush view is stale | Bound property, expression update, lifecycle, input/change-detection path | [K07](sources.md#k07), [K10](sources.md#k10); targeted investigation required |

## Evidence to retain

For a fix, record the original transition, the cause supported by inspected code or a reproduction, the smallest change, and the check that would fail without it. Inspect model and control values as appropriate; a screenshot alone cannot establish payload or validation behavior.

Separate application subscriptions from Observables returned through supported Formly hooks. Check ownership and teardown before prescribing a subscription rewrite. Preserve application services and field factories unless the diagnosis requires changing them. [K10](sources.md#k10)

For async bugs, include initial state, pending work, final state, and dependent changes. For visibility bugs, include hide → show and any retention requirement. For arrays, include insert/remove at more than the final position. For custom controls, include programmatic and user-driven updates, disabled/touched state, and reset.

For a custom numeric/money control, trace typed text → accessor emission → FormControl → Formly model → outgoing payload, recording value and JavaScript type. Inspect the effective registration/defaults, parser and `modelOptions` (including debounce/updateOn), then only the component/accessor/helper and submit mapping that participate in this path. Prop names such as `precision` or `emitMinorUnits` do not prove units or rounding policy. The v6 debounce branch can bypass parsers, while an active parser can write back to the control/view. Ask for the intended rounding boundary before proposing multiplication or rounding changes. See [API contracts](api-contracts.md) and [evaluation lessons](evaluation-lessons.md).

If execution is unavailable, report a source-supported diagnosis or hypothesis and a runnable verification plan. Never imply an upstream spec, demo, or this skill's notes were executed merely because they were read.

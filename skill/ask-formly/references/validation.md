# Validation

Scope: source-checked at 6.3.12. Upstream contract tests were inspected, not executed.

## The two return contracts

| Configuration | Expected style |
| --- | --- |
| `validators.validation: [fn]` or registered validator names | Use Angular-style null/error-object results for the public typed registration contract; the runtime adapter additionally accepts booleans (see below) |
| `validators.someName: { expression: fn, message: ... }` | Formly boolean expression: true when valid, false when invalid |

The wrapper handles named expressions differently and converts boolean results into errors. At runtime, a registered validator such as `accountCode` may return true/false: false becomes `{ accountCode: true }` when no error-path options apply. This runtime tolerance does **not** match the public `ConfigOption.validators` typing: its `FieldValidatorFn` returns `ValidationErrors | null`. A boolean-returning registration fails strict TypeScript/AOT with TS2322. For new typed registrations, return `null` or an error map; do not cast away that mismatch. An existing boolean registration is not by itself evidence of a runtime validation defect. Outside Formly, Angular's direct `ValidatorFn` also uses null/error-object. Putting an Angular error object in a named boolean expression can invert the intended meaning because a nonempty object is truthy. Inspect the registration and nesting before changing a validator [K08](sources.md#k08), [K26](sources.md#k26), [pinned public typing](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/models/config.ts#L30-L39).

```ts
// Contrasting fragments; no runtime test claimed.
validators: {
  validation: [control => control.value === 'ok' ? null : { allowed: true }]
}
// Or a named Formly expression:
validators: {
  allowed: {
    expression: control => control.value === 'ok',
    message: 'Enter an allowed value',
  }
}
```

The latter message is associated with the named field validator. The Angular-style version needs a corresponding message configuration if you want friendly display. Validity and message display are distinct concerns.

## Built-ins and messages

The extension adapts required, pattern, minLength, maxLength, min, and max props. It observes their changes and updates validity. Do not invent automatic validators for arbitrary props. Camel-case length message keys are preferred, but the inspected implementation retains compatibility behavior when lowercase message registrations exist [K08](sources.md#k08).

Default error display requires invalidity plus touched, parent submitted, or `validation.show`. A control can be invalid without displaying a message, and a missing message can be a registration problem rather than a validator problem [K04](sources.md#k04). Check `validation.messages`, global messages, the wrapper, and the actual error key.

## Async and cross-field behavior

Async expressions can return Promises or Observables. The wrapper preserves asynchronous shape and adapts the result; distinguish boolean expressions from Angular async validator contracts just as for sync validation [K08](sources.md#k08), [E03](examples.md#e03). A real API validator needs an explicit loading/error policy and verification of completion; the demo is not a production networking policy.

The official matching-fields example puts the validator on a group and supplies an `errorPath` for the confirmation control; `fieldMatch` is application-defined [E04](examples.md#e04). Cleanup in 6.3.12 looks up the validator's configured name, while routed errors are stored under their returned error keys. These must match. An anonymous `validators.validation` function returning `{ match: { errorPath: 'b' } }` can leave `b.errors.match` behind after sibling `a` makes the group rule valid. A named Boolean `match` rule with `errorPath: 'b'` cleared it in the focused probe. Use matching names or explicit application-owned routing, and test editing the non-target sibling; do not assume every routed error self-clears. [K08](sources.md#k08), [evaluation evidence](evaluation-evidence.json)

Regression checks should cover both valid and invalid values, edits to each relevant sibling, pending/settled async state, and the chosen message-display trigger. Source inspection alone cannot establish that all those transitions work in a consuming application.

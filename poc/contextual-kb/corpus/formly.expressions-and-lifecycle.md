---
id: formly.expressions-and-lifecycle
title: Expressions and lifecycle
kind: guide
formly_version: 6.3.12
adapter: core
about: 'Use for questions about Expressions and lifecycle: Callback contracts, Hiding
  is more than styling, When expressions update, Hooks and subscriptions.'
source_path: skill/ask-formly/references/expressions-and-lifecycle.md
source_sha256: b39f61a8738dc19124e9f88b6d764e616bec79a7535105224221a429b368b1ac
---
# Expressions and lifecycle

Scope: source-checked at 6.3.12; selected upstream tests read, not run.

## Callback contracts

| API | Relevant contract |
| --- | --- |
| `expressions: { 'props.disabled': fn }` | Public callback receives the field; read `field.model` and `field.options.formState` |
| Legacy `expressionProperties` / `hideExpression` function | Model, formState, optional field arguments |
| String expression | Evaluated with model, formState, field bindings |
| Observable expression | Value stream applied to the targeted field property |

Evidence: declarations [K01](sources.md#k01), evaluator [K07](sources.md#k07), tests [K25](sources.md#k25). One upstream test title still mentions the older arguments, but its assertion checks a field argument. Prefer declarations and assertions over the test title. An extra internal evaluation flag is not a reason to build application callbacks around undocumented arguments.

```ts
// Explanatory v6 fragment; assumes this leaf shares the relevant model scope.
expressions: {
  'props.disabled': field => !field.model?.country,
  hide: field => field.options?.formState?.mode === 'summary',
}
```

Do not copy a legacy `(model) => model.country` callback into `expressions` without adapting it. For constant visibility use `hide: true/false` on the field; for conditional visibility use a supported expression. The pinned `FieldExpression` type is string/function/Observable, and the evaluator does not establish arbitrary boolean entries as a general expression API [K01](sources.md#k01), [K07](sources.md#k07).

### Disabled-path migration can change behavior

In 6.3.12, `templateOptions` aliases `props`, but expression **paths are not completely interchangeable**. The evaluator combines ancestor disabled state with an expression targeting `props.disabled`; it does not apply that same ancestor branch to `templateOptions.disabled`. Both paths update disabled controls, and `expressionChanges.property` preserves the chosen path string. A parent with `props.disabled: true` and a child expression returning false produced an enabled child for the legacy path and a disabled child for the modern path in the focused zoneless probe. [K07](sources.md#k07), [pilot evidence](evaluation-lessons.md)

Do not call a mechanical rename behavior-preserving. Keep working legacy syntax when no migration is needed. If modernizing callbacks first, `expressions: { 'templateOptions.disabled': field => ... }` retains the legacy target path while using the modern field argument. Before switching to `props.disabled`, check ancestor state and any event filters; test both locked and unlocked parents. This is a compatibility caveat, not a recommendation that disabled children should override their parent.

## Hiding is more than styling

The default registry enables lazy rendering and reset-on-hide. The expression extension unregisters a hidden control when the relevant associated fields are hidden; reset-on-hide can remove its model value and clear array children. Showing the field re-registers it and may reapply defaults. `resetOnHide: false` changes value retention; it is not a promise that a hidden control remains in the active control tree [K04](sources.md#k04), [K07](sources.md#k07).

Always establish whether the requirement is preservation, validation, rendering, or submission. Do not infer the server payload from visibility alone. Inspect the application's payload selection and both its model and control values. Fields sharing a key need particular care because hiding one does not necessarily remove the shared control [K07](sources.md#k07).

## When expressions update

The default is `checkExpressionOn: 'modelChange'`. v6.3.12 also observes changes to formState in the form component and calls detectChanges. That detail is patch-sensitive; avoid old blanket advice that formState changes are never detected [K04](sources.md#k04), [K11](sources.md#k11), [K29](sources.md#k29).

`options.checkExpressions(field)` evaluates expressions; `options.detectChanges(field)` invokes expression checks and marks the relevant components. These operations do not replace inspecting the root cause of an update problem [K05](sources.md#k05), [K07](sources.md#k07). `options.fieldChanges` includes events with type `expressionChanges`, property, field, and value; filter them for the actual dependency [K07](sources.md#k07).

## Hooks and subscriptions

The public hook type specifically permits returning an Observable from `onInit`. The field component subscribes to supported lifecycle-hook returns and disposes managed subscriptions on destruction. Prefer the typed `onInit` return pattern where appropriate. A manually created `.subscribe()` is not automatically that managed return; provide corresponding cleanup [K01](sources.md#k01), [K10](sources.md#k10).

Options streams consumed by a select and subscriptions returned from a hook are different ownership paths. Read the select pipe and component if diagnosing teardown or stale options [K14](sources.md#k14), [K15](sources.md#k15). Pure property expressions are usually easier to reason about than expressions with side effects; this is design guidance, not an assertion that Formly forbids side effects.

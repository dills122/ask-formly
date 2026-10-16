# Types, wrappers, extensions, and presets

Baseline: 6.3.12. These mechanisms solve different problems; choose by responsibility.

| Mechanism | Use when | Evidence |
| --- | --- | --- |
| Type | Render a control or specialized field/group | [K30](sources.md#k30), [K04](sources.md#k04) |
| Wrapper | Decorate a field with shared markup or layout | [K31](sources.md#k31) |
| Type inheritance | Reuse a registered type with different defaults | [K04](sources.md#k04), [E09](examples.md#e09) |
| Extension | Transform or coordinate fields during the build lifecycle | [K06](sources.md#k06), [K24](sources.md#k24) |
| Preset | Apply a named reusable configuration | [K23](sources.md#k23) |

## Types and registration

Core `FieldType` exposes the field, model, form, options, props, and formControl. `FieldTypeConfig` narrows the control to `FormControl`; group types have a different control shape. Match the base class/generic and template bindings to the actual control. A component class alone does not make its string name available: inspect the application's `types` registration. [K30](sources.md#k30), [K03](sources.md#k03)

Type configuration supports `component`, `extends`, `defaultOptions`, and wrappers. The configuration service fills missing values through reverse deep merging; do not assume a field's partial `props` replaces all inherited defaults. Verify complicated inheritance against `getMergedField`, especially wrapper overrides and defaults supplied by the component. [K04](sources.md#k04)

The official password example extends `input` and sets defaults rather than reimplementing the input renderer. This is a useful pattern when behavior is already supplied by the parent type. [E09](examples.md#e09)

In v6.3.12, an interface exported by an internal model file is not necessarily exported by the package. `TypeOption` cannot be imported from `@ngx-formly/core`; derive a registration type through the public API instead:

```ts
import { ConfigOption } from '@ngx-formly/core';
type TypeOption = NonNullable<ConfigOption['types']>[number];
```

Both blind custom-control solutions failed AOT on that direct import; this alias compiled after the isolated repair. Avoid deep imports and verify the public barrel [K02](sources.md#k02), [K36](sources.md#k36).

## Wrappers and Material

`FieldWrapper` extends `FieldType` and supplies the `fieldComponent` insertion target. A custom wrapper needs the expected template insertion point. A wrapper decorates the field; it does not substitute for a missing control/value accessor. [K31](sources.md#k31)

Material's form-field wrapper owns `mat-form-field`. Check existing type wrappers before adding another. Material also has its own `FieldType` implementation for `MatFormFieldControl` integration; a plain core type does not automatically supply that bridge. See [Material control integration](material-controls.md#custom-material-controls). [K16](sources.md#k16), [K17](sources.md#k17)

## Extensions

The builder runs extension `prePopulate`, `onPopulate`, child building, then `postPopulate`. Extension hooks differ from component/field lifecycle hooks such as `onInit`. Extensions are sorted by ascending priority; the core registrations use negative priorities, while an unspecified custom priority defaults to 1. Verify dependencies rather than assuming registration order determines every stage. [K06](sources.md#k06), [K03](sources.md#k03), [K35](sources.md#k35)

The Material addons example conditionally appends a wrapper and checks whether it is already present. That guard is a useful model for idempotent transformations when a field is rebuilt. It is an example, not proof that an arbitrary extension is safe to rerun. [E06](examples.md#e06)

## Presets

The v6 guide uses `FormlyPresetModule` from `@ngx-formly/core/preset`, configuration `presets`, and a `#name` reference. The implementation substitutes configuration during prePopulate at priority -300, before core initialization. It supports a configuration provider's `getConfiguration()`. Complex/recursive composition remains unqualified. Read [API contracts](api-contracts.md) for merge semantics before relying on empty/null overrides. [K23](sources.md#k23), [K44](sources.md#k44)

## Verification when extending

Compile the consuming app with its template strictness. Render the registered type, exercise value updates in both directions, and check touched/disabled/error behavior. For wrappers, check insertion and duplicate form-field decoration. For extensions, rebuild and change inputs to detect duplicate registrations or subscriptions. These are recommended checks, not checks already performed for this draft.

## Strict Angular 21 fixture

A standalone host with v6 NgModule registration, a `MaterialFieldType<FieldTypeConfig>` custom input, and a `FieldArrayType` repeat renderer passed strict AOT and selected browser interactions. Keep template control types explicit; an empty typed FormGroup is not a suitable inferred type for arbitrary runtime keys. See [qualification lessons](angular21-qualification.md#strict-compilation-lessons).

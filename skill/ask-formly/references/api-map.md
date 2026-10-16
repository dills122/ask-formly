# API and runtime map

Scope: source-checked at 6.3.12. This is a task-oriented map, not an exhaustive generated API reference.

For non-obvious semantics, continue with [API contracts](api-contracts.md). For design choices use [patterns](patterns.md); for actual bug/version history use the [ledger](bug-ledger.md).

| Surface | What to reach for | Evidence |
| --- | --- | --- |
| Form host | `<formly-form>` receives fields, model, form, options and emits modelChange | [K11](sources.md#k11), [K01](sources.md#k01) |
| Field definition | `FormlyFieldConfig<Props>` configures keys, types, props, validation, expressions, groups, arrays, hooks | [K01](sources.md#k01) |
| Setup | `FormlyModule.forRoot(config)` supplies core configuration; `forChild(config)` supports additional registration | [K03](sources.md#k03) |
| Registries | `FormlyConfig` manages types, wrappers, validators, messages, extensions, presets | [K04](sources.md#k04) |
| Custom leaf/group | Core `FieldType`, `FieldTypeConfig`, `FieldGroupTypeConfig` | [K02](sources.md#k02), [K30](sources.md#k30) |
| Repeaters | `FieldArrayType`, `FieldArrayTypeConfig` and registered application component | [K02](sources.md#k02), [K12](sources.md#k12) |
| Wrapper | `FieldWrapper` with a `#fieldComponent` insertion point | [K31](sources.md#k31) |
| Form-level operations | `options.resetModel`, `updateInitialValue`, `build`, `checkExpressions`, `detectChanges` | [K01](sources.md#k01), [K05](sources.md#k05), [K06](sources.md#k06) |
| JSON Schema | `FormlyJsonschema` from `@ngx-formly/core/json-schema`; `toFieldConfig` | [K20](sources.md#k20), [JSON Schema notes](json-schema.md) |
| Material | Aggregate `FormlyMaterialModule`; additional secondary modules for specialized controls | [K13](sources.md#k13), [Material notes](material.md) |

The core public export file includes internal-looking `ɵ` exports for package integration. Exported does not automatically mean suitable as an application extension API. Prefer the named public mechanisms above [K02](sources.md#k02).

## How a config becomes a form

The form host builds an internal root field. The builder runs all extensions' `prePopulate`, then `onPopulate`, recursively builds children, and finally runs `postPopulate` for the current field. The default extension order is core, validation, form controls, expressions; priority sorting allows additional extensions [K03](sources.md#k03), [K06](sources.md#k06), [K35](sources.md#k35).

Core initializes field props/options/model access. The form extension creates or finds controls. The expression extension evaluates dynamic properties and hiding. `FormlyField` renders wrappers and types and manages field hook/value subscriptions [K05](sources.md#k05), [K09](sources.md#k09), [K07](sources.md#k07), [K10](sources.md#k10).

Use this layering to decide where to inspect: a missing type starts at registration, a wrong nested value at model/key scope, and a stale custom display at props/control/change detection. Do not diagnose everything as an Angular change-detection problem.

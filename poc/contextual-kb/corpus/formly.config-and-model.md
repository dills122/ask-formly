---
id: formly.config-and-model
title: Configuration and model
kind: guide
formly_version: 6.3.12
adapter: core
about: 'Use for questions about Configuration and model: Distinguish the objects,
  Keys and scope, Defaults and resets, Props and registrations.'
source_path: skill/ask-formly/references/config-and-model.md
source_sha256: 74505b90d0ce0611ad2355dc2560c9428b9aed81171171b97b104c82c7c0d7db
---
# Configuration and model

Scope: source-checked at 6.3.12; examples below are explanatory fragments, not runtime-qualified applications.

## Distinguish the objects

`fields` describe structure/behavior. `model` stores application values. Angular controls track value/validation/interaction state. `options.formState` carries shared form context. A built field also receives runtime links such as `parent`, `options`, and `formControl`; it is not merely the original JSON-shaped object [K01](sources.md#k01), [K05](sources.md#k05), [K09](sources.md#k09).

The generic parameter of `FormlyFieldConfig<Props>` describes props, not the entire model's key schema. Its `key` accepts string, number, or path-array forms, and its default props allow extra properties. TypeScript acceptance alone does not prove a key exists in your domain model or a Material component consumes an extra prop [K01](sources.md#k01).

## Keys and scope

A group without a key can provide layout while sharing the parent's model/control scope. A keyed group provides a nested scope. Core's model getter uses the keyed group's value for a field with both key and fieldGroup; otherwise it exposes the parent model. Leaf `field.model` is therefore not a synonym for the leaf's scalar value [K05](sources.md#k05), [K09](sources.md#k09).

```ts
// Explanatory field fragment; assumes 'input' is registered.
{
  key: 'address',
  fieldGroup: [
    { key: 'city', type: 'input', props: { label: 'City' } }
  ]
}
// Intended model shape: { address: { city: 'Toronto' } }
```

When reading an expression, trace the nearest model scope first. Use the target release's key utilities for tricky dotted/bracket/path-array behavior instead of guessing that every field sees the root model. `field.parent`, `field.get`, and explicit shared formState can help, but must match the actual hierarchy [K01](sources.md#k01), [K05](sources.md#k05).

## Defaults and resets

A default is applied when the keyed value is undefined and the field is not hidden under the relevant build conditions. It does not universally overwrite null, false, zero, or an existing value [K05](sources.md#k05). Arrays and JSON Schema have additional default behavior; read their references before generalizing.

`options.updateInitialValue()` records a cloned baseline; `options.resetModel()` restores that baseline (or an explicit supplied model), rebuilds, and resets controls. A raw `form.reset()` should not be assumed equivalent. The official reset demo exposes both operations [K05](sources.md#k05), [E07](examples.md#e07).

## Props and registrations

Core aliases `templateOptions` to `props`. New code can use `props`, while a small legacy fix need not rename every field [K05](sources.md#k05). The `type` string resolves through registrations, which may contribute defaults, inheritance, and wrappers [K04](sources.md#k04). Read those registrations before concluding that a supplied config is incomplete or invalid.

Prefer a fresh field factory when creating independent forms: built fields acquire runtime state. This is engineering guidance inferred from the mutation/linking in core and the builder, not a guarantee that all reuse is invalid [K05](sources.md#k05), [K06](sources.md#k06).

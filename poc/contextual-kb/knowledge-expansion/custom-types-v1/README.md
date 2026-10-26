# Custom field types and registration: proposed first batch

Status: independent plan/source review **Ready**, with no findings; see [review decision](REVIEW.md). **An isolated candidate DB has now been built after the authorized safety review; the installed DB remains unchanged.** See [execution protocol](EXECUTION.md), [development results](DEVELOPMENT-RESULTS.md), and [qualification results](RESULTS.md). Final comparison: candidate30/24/30 useful versus baseline11/11/11, out of30 per repeat. [Final independent review](FINAL-REVIEW.md) confirmed the knowledge gain but **not readiness for adoption**, because repeat2 missed the frozen gate. This directory is not an input to the accepted launcher or compiler CLI.

## What the inventory found

The accepted source contains 46 facts in nine documents. [existing-facts.json](existing-facts.json) inventories every claim, condition, limit, adapter and evidence reference. This is an inventory of authored support, not measured retrieval success. Existing examples are already overlapping in registration/name selection; adding more copies of that claim would not fill the main gaps.

| Capability | Existing authored support | Gap / proposed addition |
| --- | --- | --- |
| Register a name and select it with `type` | `custom-component-use/registered-component-selected-by-type`, `custom-types-and-wrappers/component-needs-registration`, `props-and-registration/type-name-registration`, `custom-type-use-example/field-uses-registered-name` | Covered conceptually. Add Angular setup detail, not another alias-selection fact. |
| Distinguish model key from renderer name | `custom-component-use/key-is-model-type-is-renderer`, `props-and-registration/key-shapes` | Covered; reuse existing facts. |
| Define the custom component/template | `custom-types-and-wrappers/fieldtype-surface` | Partial: add `custom-control-template`, including concrete control and field bindings. |
| Explain `formlyAttributes` | No dedicated claim | Add `attributes-directive-purpose`; distinguish it from control binding. |
| Declare and import the custom component | Alias registration is covered, Angular declaration/import steps are not | Add `ngmodule-declaration-and-imports`, scoped to the pinned NgModule demo. |
| Choose scalar versus group control typing | Existing source quote mentions this, but the authored claim only lists the FieldType surface | Add `scalar-and-group-control-types`. Existing quotation availability is partial support, not a claim that the runtime cannot ever find it. |
| Use a component class directly | Existing facts discuss string type names | Add `component-reference-or-alias`; registration of an alias is not mandatory for the direct component route. |
| Root versus feature configuration | No dedicated provider-contract fact | Add `root-and-child-configuration`; defer universal injector-visibility advice. |
| Diagnose an unknown type | String resolution is covered | Add `unknown-string-type`, with the exact getType error/return condition. |
| Reuse an existing renderer through defaults | `custom-types-and-wrappers/password-inheritance-example`, `reverse-merged-defaults`, `type-registration-options`, `props-and-registration/registration-adds-configuration` | Covered at mechanism level; defer comprehensive merge-order/null/array semantics. |
| Configure wrappers | `wrapper-insertion-point`, `wrapper-decorates-not-control` in `custom-types-and-wrappers`; type options also covered | Add only `registered-wrapper-fallback`, including the empty-array boundary. Not a complete wrapper-authoring tutorial. |
| Use Material correctly | `material-wrapper-boundaries/material-form-field-owner`, `core-type-needs-material-bridge` | Partial: add the concrete `material-input-pattern`; no universal third-party-widget recipe. |
| Type registration objects through public API | No dedicated authored claim (retained reference prose already discusses it) | Add `public-registration-type`, grounded in the public barrel and ConfigOption declaration. |
| Supply props | `props-and-registration/props-generic-scope`, `extra-prop-not-automatic`, `props-template-options-alias` | Retain existing support; the custom-input example demonstrates explicitly consuming props. No claim that arbitrary props render automatically. |

## Proposed knowledge batch

**10 additions: nine core facts and one Material fact, in two draft documents.** If accepted without changes, the combined input would contain **56 facts across 11 documents**. This is a proposed count, not an installed change.

- [Core draft](draft-authored/custom-type-recipe-core.json)
- [Material draft](draft-authored/custom-type-recipe-material.json)
- [Authored source summaries](proposed-source.md), with exact citation syntax expected by the existing compiler
- [Pinned source excerpts](sources.md) and [machine-readable evidence](source-evidence.json)
- [Development requests and scoring expectations](development-cases.json)
- [Build and qualification plan](PLAN.md)

Each draft fact has a claim, conditions, limitations, retrieval context and links to existing facts. The `source_quote` field quotes our authored source summary, just as the current compiler expects; it is not mislabeled as a verbatim upstream quote. Separate evidence records preserve exact upstream excerpts, paths, line ranges and SHA-256 hashes.

All inspected upstream files matched members of the local archive whose SHA-256 matches the already pinned Formly commit `5f099fddea6426b46a453866adf0fede5be0bcd7`. Online raw-source fetching failed; the verified local upstream archive supplied the evidence. No upstream implementation was imported or wired into the POC. Excerpts are provenance only. Upstream attribution remains applicable: [retained notices](../../../../skill/ask-formly/THIRD_PARTY_NOTICES.md).

The code graph was stale (16 October) and excluded the upstream snapshot; structural search found no compiler symbols. Coverage checks reported untracked compiler files and excluded upstream paths. All relied-on code was read directly, including compiler validation/build signatures. No graph absence was treated as evidence of missing behavior.

## Deliberate limits

This batch does not implement SSN masks/validation, inspect an application's form, invent a `CitySelector`, establish arbitrary CVA correctness, cover all lazy-injector topologies, or claim current Formly versions behave like 6.3.12. Standalone setup recipes, new adapters, arrays, wrappers as a full topic, and exhaustive defaults precedence are deferred. The existing concepts and these additions together support library guidance; Angular compilation and behavior of generated recipes still need qualification before we claim tested recipes.

The current active records, catalog, compiler, launcher, model assets, installed DB and sealed evaluation remain untouched. The future DB comparison keeps all runtime components fixed; only a separately selected database differs.

# Next imported-guide knowledge groups

Status: source-backed proposal, not built, qualified, or installed. Prepared separately while custom-types-v1 runs its frozen comparison. A failed delivery gate in that experiment must remain visible; this proposal does not redefine its success criteria.

## Scope and sequence

Finish gaps in the three already imported guides before importing broader retained references. Keep the accepted DB, models, question foundation and runtime unchanged. Start with **model scope**, then **expression values/notifications**, then **extensions/presets**. Qualify each increment so a regression can be attributed to one group. Do not combine all groups merely to maximize fact count.

The table below is a claim outline, not final authored compiler input. Each row needs a source quote, conditions, limits, related-fact links and a source-to-existing-fact duplicate check before authoring. `source-verification.json` preserves fourteen exact pinned source excerpts, file hashes and comparison against the original upstream archive. Graph coverage excludes this upstream directory; the evidence was read directly. Source reads are not Angular runtime tests.

| Proposed addition | Evidence | Required boundary |
| --- | --- | --- |
| Built field configuration receives runtime parent/options/control links; distinguish configuration, model values, control state and shared formState. | K01, K05, K09 | Built fields, not a promise that raw JSON already has these links. Avoid duplicating the existing shared-formState fact. |
| A keyless fieldGroup shares its parent's model/control scope; a keyed group uses the nested model value and receives a group control when needed. | K05, K09 | Explain existing-control reuse and ordinary groups; do not generalize to arbitrary fieldArray behavior. |
| A leaf field.model exposes its enclosing model scope, not necessarily its scalar value. | K05 | Nested groups change that scope; field.model is not universally the root model. |
| String expressions use model, formState and field bindings. | K07, K25 | Distinguish strings from modern field-argument callbacks and legacy callbacks. No security/sandbox guarantee. |
| A direct Observable expression supplies values for the targeted property. | K07 | Do not confuse this with a callback returning an Observable, a select options stream or an onInit subscription. |
| The form component observes formState and invokes detectChanges. | K11; K05 for detectChanges | Pinned 6.3.12 component path; not universal change detection for every arbitrary mutation/version. |
| options.fieldChanges emits expressionChanges events carrying field, property and value. | K07 | Preserve the exact property path; do not promise an event on every evaluation. |
| Builder extension phases run prePopulate, onPopulate, child builds, then postPopulate. | K06 | Distinct from field/component lifecycle hooks such as onInit. |
| Extensions are sorted by ascending priority; omitted priority defaults to 1 and default core registrations use negative values. | K03, K35 | Do not promise numeric priority semantics for every unusual name/key or arbitrary dependency arrangement. |
| Presets require FormlyPresetModule and configured presets; a #name pseudo-type selects a named reusable configuration. | K23 | Pinned NgModule setup, not an assumed built-in renderer or standalone recipe. |
| Preset substitution uses prePopulate at priority -300 and supports getConfiguration providers. | K44, K03 | No claim of recursive composition safety or application injector behavior. |
| The Material addons example guards against adding an existing addons wrapper and appends it only for configured addon props. | E06a, E06b | Example-specific registered wrapper; no general idempotence guarantee for arbitrary extensions. |

## Proposed development requests

These are visible development material, never sealed evaluation. Final expected aspects should be written before a candidate build.

1. In Formly 6.3.12, how do fields, model, formControl and options.formState differ, and which links appear on built fields?
2. Does a keyless Formly fieldGroup create another model object and FormGroup, or share its parent's scope?
3. For a keyed address group containing a city leaf, does the leaf's field.model mean the city string, the address object or the root model?
4. Which names are available in a Formly string expression, and is that the same callback signature as expressions functions?
5. Can I assign an Observable directly to expressions['props.label'], and does that mean a callback returning an Observable is the same contract?
6. In Formly 6.3.12, is the statement that formState changes are never detected correct?
7. How do I observe expression changes, and what are the event's type, property, field and value fields?
8. Does postPopulate run before or after children are built, and is it an onInit hook?
9. Does adding an extension last force it to run last, and what happens if I omit priority?
10. How do I register and reference a Formly preset, and is #name a normal registered renderer name?
11. When does preset substitution happen, and can a provider supply configuration via getConfiguration?
12. How does the official Material addons example avoid appending its wrapper twice? Does that prove my own extension is safe to rerun?

Add controls covering custom types, hiding/defaults and explicit unsupported application-specific asks in each group. Fresh qualification questions must be prepared and frozen only after development and review. Reuse the same quantitative gates unless explicitly changed before running, with per-group and regression denominators reported separately.

## Explicit exclusions from imported-guide finalization

- Fresh field factory advice and pure-expression advice are inferred engineering guidance, not new universal Formly rules.
- Application-specific payload selection, module discovery and custom component behavior remain outside the library KB.
- Historical Angular 21 fixture results remain historical evidence, not a universal compatibility promise.
- Arrays, validation, JSON Schema and select ownership are linked topics requiring separate imported-source review; mentioning them is not coverage.
- Complex inheritance, recursive presets and arbitrary extension reruns remain explicitly unqualified.

## Build and audit gate

First complete and review custom-types-v1, including its observed missing-tool delivery failure. A positive knowledge-only result does not turn a failed end-to-end gate into a pass. Preserve that distinction in any follow-on decision.

For each next group: author only verified missing claims; independently review evidence and cases; build a new explicit-path DB preserving every prior row; retain separate baseline and candidate manifests; run real-agent MCP cases and equal-plan replays; judge complete grounded answers and gap handling; independently audit failures and source support. Never overwrite the first frozen harness or candidate, change installed launch paths, or repin production manifests. A subsequent experiment may fix a demonstrated harness reliability problem under a new version, with its own tests and freeze, without rewriting the failed run.

# Dependency evidence without changing the fact set

**2026-10-28 — version-scoped source guidance.** ask-formly's admitted facts
describe Formly 6.3.12 core/Material. Some answers also depend on Angular or an
application's controls and save code. Rephrasing those questions repeatedly in
Formly discovery does not supply a missing dependency contract.

This guide supplies two inspected **Angular 13.3.11** mechanisms. That version is
an explicit source example, not an inferred consumer installation: Formly's
development range starts at `^13.3.11`, and its peer range does not determine an
exact runtime. Nothing here expands the DB's applicability, admits new facts,
or qualifies other Angular versions. No Angular/browser fixture ran for this guide.

## Follow the dependency boundary

1. State the unresolved behavior precisely: for example, whether a committed
   child update reruns its parent validator, or which disabled values enter the
   chosen payload.
2. Reuse delivered Formly facts for Formly-owned behavior. Fetch a relevant unseen
   fact or page when there is a concrete reason; a dependency-looking name alone
   does not prove no Formly evidence exists.
3. For the dependency-owned part, inspect the consuming project's exact resolved
   package version and relevant configuration. A package range or Formly version
   is not an exact Angular version. If unavailable, request it or clearly label
   any version-specific illustration instead of substituting the latest docs.
4. Consult official documentation or source matching that version. Record the
   version, URL, mechanism, conditions and remaining application assumptions.
   Keep external evidence distinguishable from facts returned by ask-formly.
5. Continue answering supported branches. When exact dependency evidence is not
   available, name that narrow gap rather than refusing the whole design or
   inventing a guarantee. A scoped search miss is not a whole-library absence claim.

The calling agent owns this lookup and application inspection; ask-formly does
not acquire a new web-fetch tool, dependency database or repository scanner.

## Group validation after a child changes

In Angular 13.3.11, `FormControl.setValue` calls `updateValueAndValidity`.
For an enabled control, that operation runs its validator and propagates to its
parent unless `onlySelf: true`. The parent repeats its own value/validity update,
including its own validator. This explains why a rule attached to a common
group can reevaluate when a registered child commits a change. It does **not**
mean Angular reruns every sibling's leaf validator.

Sources: [setValue](https://github.com/angular/angular/blob/13.3.11/packages/forms/src/model.ts#L1371-L1383),
[validation and ancestor propagation](https://github.com/angular/angular/blob/13.3.11/packages/forms/src/model.ts#L885-L906).

| Condition | Consequence in the inspected version |
| --- | --- |
| Ordinary view update using `updateOn: 'change'` | The value-accessor change pipeline commits through `setValue`. Unspecified strategy inherits from the parent, falling back to `change`. |
| `updateOn: 'blur'` or `'submit'` | Visible input can be pending; do not promise a group recheck on every keystroke. |
| `onlySelf: true` | This call does not propagate validation to the parent. A deliberate later parent update may be needed by the application's batching design. |
| `emitEvent: false` | Suppresses value/status stream emission, not the validation work or ordinary ancestor propagation. Event-driven application subscriptions can nevertheless be skipped. |
| Disabled control/group | Disabled status skips its own validator execution in this path. Do not equate disabled with valid. |

Sources: [strategy inheritance](https://github.com/angular/angular/blob/13.3.11/packages/forms/src/model.ts#L483-L492),
[view and blur pipelines](https://github.com/angular/angular/blob/13.3.11/packages/forms/src/directives/shared.ts#L201-L225),
[validation branch and event guard](https://github.com/angular/angular/blob/13.3.11/packages/forms/src/model.ts#L885-L906).

For a Formly date relationship, this dependency mechanism complements existing
group-validator, errorPath and message facts. Use the actual common control group
and preserve Formly's validator-name/error-key cleanup conditions. Date adapter
comparison, empty-value policy, error placement and custom callbacks remain
separate decisions. A group-level design does not need an extra sibling
subscription merely to satisfy a preferred recipe, but its concrete application
transitions should be tested before claiming execution evidence.

## Disabled values and the chosen save payload

Angular 13.3.11's `FormGroup` reduces its **registered** children as follows:

| Value source | Inspected behavior |
| --- | --- |
| Enabled group's `.value` | Includes enabled children; disabled children are omitted. |
| Disabled group's `.value` | Includes all its registered children. Therefore “disabled values are always absent from form.value” is too broad. |
| Group's `.getRawValue()` | Recursively gathers registered child values including disabled descendants. It does not recreate removed controls. |
| Formly model or application mapper | A different data source. Inspect the actual synchronization and serializer; Angular group aggregation alone does not establish the outgoing payload. |

Sources: [group value reduction](https://github.com/angular/angular/blob/13.3.11/packages/forms/src/model.ts#L1942-L1950),
[recursive raw values](https://github.com/angular/angular/blob/13.3.11/packages/forms/src/model.ts#L1883-L1895),
[raw-value helper](https://github.com/angular/angular/blob/13.3.11/packages/forms/src/model.ts#L185-L187).

Disabling sets `DISABLED`, clears current errors in that operation, disables
children and updates ancestors subject to the options; it is not a read-only
presentation setting. Re-enabling recalculates validity. See
[disable/enable](https://github.com/angular/angular/blob/13.3.11/packages/forms/src/model.ts#L764-L843).
Neither disabling nor `getRawValue()` enforces authorization: the application and
server must apply their intended update policy.

For a permissions question, inspect effective ancestor/control state, the custom
extension and wrapper, and whether saving uses the model, `.value`, raw values or
a mapper. Choose payload inclusion deliberately. “Use getRawValue everywhere”
can preserve values the application intended to exclude. Conversely, controls
removed by Formly hiding are absent from this tree even when their model values
are retained. No universal serializer recommendation follows.

## Verification and limits

The source copies and hashes are recorded in ignored
`test-output/dependency-recovery-v1/dependency/sources.json`. They reuse the prior
exact-version downloads. Graph coverage reported those local copies excluded;
the cited ranges were inspected directly. This is source evidence, not a
browser, arbitrary custom-control, all-version or complete-workflow test.

Useful focused consumer checks distinguish change/blur/submit, normal versus
`onlySelf` updates, and event suppression from validation. For payloads, compare
an enabled group containing a disabled child, a disabled group, raw values and
the final application payload. Keep model/control state and actual outgoing data
as separate assertions. These are proposed checks, not passed runs.

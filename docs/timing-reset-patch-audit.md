# Timing, reset-state and patchValue audit

**2026-10-28 — investigation only.** Ruflo coordinated three source audits of the
remaining S05, S09 and F01 partial answers. The installed 192-fact DB and isolated
195-fact Material/reset candidate remain unchanged. No new facts were admitted,
retrieval behavior changed, or application runtime qualified.

The audit uses the actual fresh answers and delivered evidence from the
[Material/reset comparison](material-errors-reset-candidate.md). It preserves
those grades and the earlier generated experiment, whose different F01 answer
was complete. These are exposed development cases, not unseen evaluation.

## Findings and ownership

| Gap | What the caller already had | What is still needed |
| --- | --- | --- |
| S05 validation timing | Update strategy, Formly propagation debounce, error visibility and async validation contracts | Angular-version-specific commit/pending evidence and an application policy connecting immediate feedback, remote checks and submission. |
| S09 reset state | Reset baseline and resetModel mechanisms; candidate adds the conditional submitted-state operation and reset sequence | Precise dependency evidence for dirty/touched and validation recomputation, plus clear language separating clean interaction state from valid data. |
| F01 patchValue loading | Hide/unregister/retention, expression checking and model propagation mechanisms | Explain registered-control patching versus model storage, then qualify a model-aware loading recipe for hidden fields. |

The existing evidence reached these callers. The observed misses do not currently
justify another ranking change. A precise missing mechanism can deserve a fact;
a multi-step application policy should remain caller guidance with explicit
assumptions and test evidence.

## Timing: define what “fixed” means

S05 asks for validation after blur and immediate clearing once a value is fixed.
Those requirements need an explicit interpretation: locally well-formed, changed
since a rejected value, and remotely confirmed available are different states.
Formly's propagation debounce does not defer validators or HTTP requests.

In inspected Angular 13.3.11 source, blur controls retain pending view input until
blur. Submit synchronization commits submit-strategy controls; it is not a general
flush of blur inputs. Pending and invalid are distinct states. A handler that only
checks invalid can miss pending work, and even checking both does not establish
that the latest visible blur value was committed and checked.

Offer bounded choices: strict blur validation with stale-message presentation
handled separately, or immediate local updates with first-blur display gating
and separately scheduled remote checks. The second changes the literal
blur-only validation policy and must say so. Put submission checks in the actual
handler and associate a completed remote result with the current submitted value.

## Reset: clean interaction state does not mean valid data

Angular 13.3.11 reset marks controls pristine and untouched and recomputes
validation. Invalid restored values can remain invalid, and asynchronous
validation can become pending. Default error visibility and explicit
`validation.show` are separate from that validity. A bare FormGroup reset also
is not the directive's submitted-state reset.

The isolated Formly fact already preserves the `!isSignalRequired()` condition.
The pinned helper selects the signal-required branch at Angular 18.1 and later;
that boundary does not prove what every newer form directive does. Keep the
candidate's conditional wording. A version-qualified dependency appendix is
safer than admitting Angular semantics under Formly-only applicability.

The current S09 answers already satisfy saved-baseline replacement and qualified
country/state restoration. Do not invent another missing fact for those parts.
Guidance should distinguish restoring a saved selection from a user changing its
parent selection. Future checks should separately assert values, pristine,
untouched, submitted, validity and displayed errors, including invalid restored
data and save-then-edit-then-Cancel. Async option races are optional robustness
coverage, not a new requirement imposed on the old answer.

## patchValue: distinguish model storage from the active control tree

In the inspected source, Angular FormGroup.patchValue visits currently registered
controls. Formly can remove hidden controls while retaining their model values.
When showing a field, Formly's registerControl reads the model and patches a
differing **FormControl** value before attachment. This is a concrete, narrowly
scoped Formly fact proposal; the existing show/re-register fact does not explain
that reconciliation in comparable detail. It is not a recursive FormGroup patch
or an automatic synchronization guarantee for arbitrary model mutations.

The application recipe should first define complete replacement versus partial
merge and retain hidden data in the authoritative Formly model. Then coordinate
normal-event patching and expression refresh on the built root field. Patching
still matters for already-visible controls; visibility refresh alone does not
copy every model value into them. Compare the shorter model-update → patch →
refresh sequence with explicit pre-patch registration refresh, and document the
smallest sequence that passes the fixture. Do not teach two refreshes as a
requirement before testing them.

Freeze hidden→visible, visible→hidden, hidden→hidden and visible→visible cases,
asserting model data, control registration, control values and validation
separately. Define omitted-key merge semantics. Keep silent patches, positive
debounce, parsers and immutable input replacement as separately scoped probes.
The original F01 asks for ordinary patchValue: substituting resetModel does not
resolve that request, and can change interaction state. The old complete answer
and new partial answers remain distinct historical results.

## Next work and acceptance boundaries

1. Prepare a small dependency appendix and one application recipe per gap before
   expanding the fact set. Keep exact Angular evidence separate from unconditional
   Formly claims. Retain the three existing candidate facts unchanged.
2. Freeze a named Angular/Material/Formly environment and required assertions.
   Use deterministic async responses for timing, and actual browser events for
   mouse/Enter/focus ordering. Source review alone cannot qualify those sequences.
3. Compare a guidance-only arm first where facts were already delivered. Admit
   only independently reviewed, narrowly scoped missing library mechanisms to a
   new isolated candidate if needed. Rerun fresh callers with the same requirements
   and independent grading; retain earlier failures.

Required timing checks cover first blur, subsequent correction without per-key
remote requests, untouched-field errors on actual submission, pending dispatch
blocking, and the current submitted value. Timeout/retry and destruction checks
are useful robustness controls, not retroactive requirements of S05.

Examples, standards/patterns and repository-specific knowledge remain deferred.
This work does not require creating a new knowledge primitive.

## Evidence and limits

Formly source is pinned to 6.3.12 commit
`5f099fddea6426b46a453866adf0fede5be0bcd7`. Its development dependency range starts
at Angular 13.3.11, but that is not a resolved consumer runtime. The audit inspected
Angular 13.3.11 source explicitly; it does not establish all supported versions.
Downloaded sources, URL/hash receipts, delivery inventories and detailed reports
are retained under ignored `test-output/timing-reset-patch-audit/`.

Key primary sources inspected:

- [Formly registration reconciliation](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/utils.ts#L47-L100)
  and [signal branch](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/utils.ts#L385-L387).
- [Angular 13.3.11 blur/change pipeline](https://github.com/angular/angular/blob/13.3.11/packages/forms/src/directives/shared.ts#L201-L225)
  and [submit/reset directive](https://github.com/angular/angular/blob/13.3.11/packages/forms/src/directives/reactive_directives/form_group_directive.ts#L268-L292).
- [Angular 13.3.11 FormControl reset](https://github.com/angular/angular/blob/13.3.11/packages/forms/src/model.ts#L1436-L1445),
  [FormGroup patch](https://github.com/angular/angular/blob/13.3.11/packages/forms/src/model.ts#L1800-L1814)
  and [group reset](https://github.com/angular/angular/blob/13.3.11/packages/forms/src/model.ts#L1873-L1879).

No Angular/browser application tests ran. The required maintenance check cannot
complete because this worktree lacks its compiler environment. Documentation and
preservation checks are recorded alongside the audit; neither qualifies the
installed runtime or model-backed mode. Historical browser B06/B13 failures and
all earlier caller grades remain unchanged.

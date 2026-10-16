# Performance and change detection

Baseline: 6.3.12. No benchmark or universal field-count limit is established by this corpus.

## Distinguish the costs

| Cost | Inspect | Avoid the misleading diagnosis |
| --- | --- | --- |
| Build/registration | Field count/depth, extensions, defaults, validator composition, array rebuilds | “Every pause is Angular rendering” |
| Expression evaluation | Callback cost, number of dependencies, checkExpressionOn, object-valued results | “An expression runs exactly once per keystroke” |
| Observed state | Size/depth of props/formState and mutation frequency | “All application state should live in formState” |
| Rendering | Components/wrappers, option counts, hidden/lazy content, layout | “A source-level optimization proves browser speed” |
| Async work | Request duplication, stale responses, validation scheduling, subscriptions | “Debouncing model output automatically debounces requests” |

The builder traverses fields and extensions; field components observe props and subscribe to expressions; the form host observes formState. Object-valued expression results may be compared through JSON serialization. These mechanisms make repeated computation, large observed state, and unnecessary rebuilds worth measuring. [K06](sources.md#k06), [K07](sources.md#k07), [K11](sources.md#k11), [K40](sources.md#k40), [K41](sources.md#k41)

## Historical fixes matter

- **6.2.1:** large-array work reduced by validator/build changes; I3791 reported 6.1.8. Reporter timing is not a reusable performance claim. [I3791](bug-ledger.md#i3791)
- **6.2.2:** expression-call optimization following I3799. Maintainer suggested direct Observable expressions and virtual scroll as possibilities; those comments do not guarantee a particular call count or supply a turnkey virtualized Material form. [I3799](bug-ledger.md#i3799)
- **6.3.8:** formState observation moved from individual field components toward the form host following I3984. Removing observers manually was an intermediate user workaround, not the recommended baseline design. [I3984](bug-ledger.md#i3984)
- **6.3.11:** the follow-up formState fix initializes the host observer outside model-change subscription callbacks. The reviewed patches show why stopping at the earlier workaround/fix can miss later correctness work. [I4018](bug-ledger.md#i4018)

Release links are corroborated by [K29](sources.md#k29). Exact patch reviews are indexed in [discussions](discussions.md).

## Practical investigation

Measure separately: initial build/render, one ordinary edit, external formState update, reset, and insertion/removal in a populated array. Keep the same dependency versions, field structure, and data while changing one factor. Record browser timings for visual performance; the jsdom probes here establish selected behavior, not speed.

Use pure/cheap expressions, explicit streams for expensive external dependencies, and a focused formState. If expensive work is unrelated to a form, keep it in the appropriate service/store and project only required state. This is design guidance inferred from the observation path, not a prohibition on richer formState.

Preserve the default model-change expression mode unless requirements justify otherwise. Moving to changeDetectionCheck to repair one stale closure broadens the checking schedule. Prefer making that dependency explicit first. [I3820](bug-ledger.md#i3820)

Lazy rendering reduces rendered hidden content but has lifecycle and subscription implications. Virtualization/pagination can reduce DOM cost, but requires checking focus, validation, value retention, accessibility, and teardown across unrendered rows. Do not recommend either without preserving the intended form behavior.

Do not disable core observation, copy private `_updateTreeValidity` workarounds, or install no-op validator mutations solely because an old issue comment suggested them. Inspect the current baseline and reproduce the remaining cost. Keep private performance mechanisms as diagnostic evidence, not public configuration advice. [K43](sources.md#k43), [I3791](bug-ledger.md#i3791), [I3984](bug-ledger.md#i3984)

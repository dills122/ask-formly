# Source-ledger review corrections

2026-10-25, independent review instance 1 (ongoing).

- **Accept P2:** `formly.expressions-and-lifecycle:L44:D2` had incorrectly mapped select-stream ownership to `oninit-observable-managed`. That fact does not support the claimed limitation. Removed the fact mapping and changed this decision to an explicit scope-bound exclusion/deferment to the later Material/select source review. It is no longer counted as admitted or equivalent support. The quotation now ends before the separately accounted pure-expression design advice.
- Updated three decisions spanning all four `expressions-notifications` records from pending to admitted after the parent promoted the exact reviewed 64-fact candidate (`promotion-v3/test-output/install-1`). Extensions/presets decisions remain pending.
- Recomputed aggregate section statuses and fact-ID unions, regenerated CHECKLIST.md, and validated the ledger against canonical authored records, the pending extension draft, and the installed DB read-only.

These corrections do not change source bytes, facts, compiler, runtime, DB, models or evaluation. No new knowledge expansion was introduced.

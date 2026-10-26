# Promotion review preliminary

Review instance: 1 of 3 (promotion scope; separate from candidate review).

Independent source/test pass completed before reading the author explanation. The dispatch disclosed intended architecture and reported results, so full blindness was not possible. Branch `codex/material-select-knowledge`, HEAD `c232620632e5a35b5770ea7bdb8ca8e7ee9ba32f`; new candidate/promotion directories and two tool-suite edits are uncommitted.

No actionable defect found in the inspected promotion transaction, source-addition validation, qualification guards, lookup-only runner, or source-suite wiring. The five intended targets are explicit, old rows must remain a subset, all five knowledge tables must reproduce, and postcheck failure rolls back the transaction. Crash durability across multiple filesystem writes remains explicitly outside the transaction guarantee; snapshots and journal support recovery.

Executed independently: promotion fixture suite 15/15, tools/test_project.py 4/4. Examined fixed 15 smoke cases, including all ten select cases, E05, A06, Q20, Q21 and Q24. Canonical preflight receipt reports 93 facts/21 documents, 88 preserved non-DB pins and 628 preserved other baseline files. Independent preflight and author/plan reconciliation remain pending.

Graph coverage was checked for all seven Python files used in this pass: tools paths excluded; promotion paths not tracked at indexed generation 2026-10-25T14:19:41Z. Conclusions use direct source reads rather than graph completeness. Installation, delivered smoke answers, final documentation and final preservation proof remain unverified. No final readiness verdict is issued yet.

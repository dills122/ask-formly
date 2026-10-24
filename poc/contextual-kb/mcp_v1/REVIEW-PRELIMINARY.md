# Preliminary independent review
Review instance: 1 of 3. Recorded before reading AUTHOR-EXPLANATION.md or author qualification results.

Scope: mcp_v1 only on dirty main c3091328f49d53de6b41a49c4fe5aa8f1c45e516. Unrelated working-tree changes excluded. Inspected protocol, plan, cases, tests before implementation, then service/planner/backend/server/qualification/preservation/smoke sources and relevant frozen dependency paths. Graph generation 2026-10-16 has no tracked coverage for these paths; conclusions use direct source reads.

No confirmed blocking implementation defect in the first pass. Eleven deterministic tests passed (one ResourceWarning from the in-memory citation test's unclosed SQLite connection). Raw requests remain verbatim, strict planner output is validated before backend initialization, the same worker thread owns SQLite and native resources, ordinary cancellation drains work, integrity failures latch, full-question retrieval remains unchanged, and citations are attached separately from original fact records.

Verified protected snapshot equality across 50 entries and qualification freeze equality across 17 entries. Sealed evaluation was hashed only. No model/provider reruns.

Open evidence needed before verdict: actual three-round tool delivery and answer grading, per-plan full-query/fact parity, source-citation traceability, both adapter checks, and usable setup instructions. Current task checklist remains unchecked while qualification runs. New backend tests cover citation mapping but do not directly exercise Backend integrity/degradation branches; inspect retained native evidence and inherited tests before assessing that gap. Planner timeout retains event/stderr files but skips receipt creation; this is an observability limitation, not currently a blocking functional finding.

The ten-case protocol counts warranted partial/gap responses as usable, so 90% usability must never be called 90% answer accuracy. No semantic verdict yet.

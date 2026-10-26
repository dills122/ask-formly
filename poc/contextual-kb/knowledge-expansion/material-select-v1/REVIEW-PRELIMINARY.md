# Preliminary independent review

Review instance: 1 of 3. Scope: untracked material-select-v1 batch on codex/material-select-knowledge, HEAD c232620632e5a35b5770ea7bdb8ca8e7ee9ba32f. No author explanation read before this record. Parent supplied scope and target counts, so this is an implementation-first pass, not an absence-of-context experiment.

Inspected canonical repository guidance, PLAN, 15 visible cases, isolation/batch tests, eight draft facts, full cached K14/K15/K28 source, candidate builder, experiment composition, replay and evaluation. Graph generation 2026-10-25T14:19:41Z has no tracked coverage for new batch Python files; direct source reads are the review basis.

No blocking source-mapping issue found in the inspected claims. K15 distinguishes supplied Observable mapping from its internal BehaviorSubject/fieldChanges subscription; facts preserve that ownership boundary. K14 supports strict equality, multiple/change forwarding and select-all length/cache semantics. Group nesting is explicitly limited to one renderer level. K28 source tests were inspected, not executed; the grouped fixture only asserts lengths and has id/name mappings against value/label records, so it cannot establish correct selected values. Proposed facts do not make that claim.

The two source checklists retain 11 pending sections, including partially mapped sections, and explicitly exclude cascade/application policy; no whole-Material coverage claim is made. S01–S10 test the proposed source boundaries and five controls retain existing behavior/gaps.

Pending before a prebuild verdict: author packet reconciliation, independently recomputed hashes and provenance lint, focused fixtures and verification evidence, qualification input-freeze procedure. No build or hosted inference performed by reviewer. No promotion authorization.

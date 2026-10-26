# Broader retained source backlog

This is prioritization, not admission or a fact-count estimate. These references are outside the three imported-guide ledger. They must receive source/evidence review and isolated qualification before promotion. No source bytes were changed.

| Priority | Retained reference | Initial review scope | Boundary |
| --- | --- | --- | --- |
| Admitted in validation-v1 | validation.md | Boolean expression versus Angular validator return contracts; built-in constraints and messages; async/cross-field behavior | Separate field validators, messages and application validation policy; do not infer async lifecycle guarantees without source. |
| 2 | arrays.md | Repeat/array creation, add/remove, model/control alignment and limits | Avoid custom repeat component recipes unsupported by pinned examples. |
| 3 | material.md and material-controls.md | Entry points, select option identity/streams and teardown, datepicker, custom control bridge, required/read-only presentation | Explicitly include select ownership deferred from the expressions guide. Existing wrapper/input facts are not full Material coverage. |
| 4 | json-schema.md | Conversion versus renderer registration, overrides/map callbacks, references, supported mappings and failure modes | Do not infer full JSON Schema compliance or arbitrary reference support. |
| Cross-cutting when needed | api-contracts.md | Keys/parsers/modelOptions, merges/cloning, events and hook lifetime, preset overrides | Use to resolve explicit gaps; no automatic ingestion of the whole file. |

Order is based on filling ordinary library-use gaps after the current imported-guide milestone. It is not a measured user-demand ranking. Each future batch should add a ledger with admitted/equivalent/excluded/pending decisions, preserve existing rows, and compare realistic requests against the accepted foundation. Avoid duplicating already represented facts just to increase counts.

Validation admission is now recorded in its separate [installed checklist](../validation-v1/CHECKLIST.md); arrays is the next batch. This backlog retains the original ordering for context.

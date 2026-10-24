# Candidate v3 plan

User authorized fixing shared-condition preservation and optional role hints in a new candidate; tests and independent review required. Scope only this folder. A,v2,both GLiNER baselines, data/DB and sealed evaluation remain unchanged.

- [x] Independent development-test preparation; known H07 regression plus fresh scope/condition cases.
- [x] TDD candidate validation, prompt packaging and optional-hint envelope.
- [x] Freeze candidate and inputs; actual v2/v3 agent generations on identical development requests, no repairs.
- [x] Independent implementation/semantic review; report failures without tuning on test results.
- [x] Preserve artifacts and compare protected hashes; finish evidence report.

Design: source-anchored condition bindings associate verbatim meaningful clauses with question indices. Validator verifies each declared binding is grounded in request and present in every assigned standalone question; semantic completeness and proper scope still require review. Hint transport is optional and advisory; text-only search-request projection excludes all hints. Invalid hint data must not invalidate an otherwise valid plan. No retrieval, model training, answering, application investigation or serving changes. No claims that schema validation proves all conditions were discovered.

Bound: known H07 plus12 fresh development cases, one independently executed batch per v2/v3; one semantic grader/engineering reviewer, max3 fresh review instances only if material fixes require. Existing v2 cached results are diagnostics only, not a paired control. No generation retry or best-run selection.

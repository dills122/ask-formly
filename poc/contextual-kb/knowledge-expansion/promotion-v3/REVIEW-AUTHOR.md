# Author explanation: promotion mechanism

Intent: make the already approved64-fact promotion reproducible rather than an ad hoc copy. Scope is promotion-v3 only; no installed files were changed during implementation.

promote.py provides a narrowly pinned CLI and a filesystem transaction helper. promotion-spec.json freezes expected current/reviewed artifacts. The helper captures recoverable originals, enforces preconditions and exclusive recovery directories, writes per-file atomic replacements, and rolls back caught failures. Candidate correctness/provenance continue to use the existing compiler and frozen source metadata; this does not invent a second compiler. run.py is a byte-for-byte copy of promotion-v2/run.py with its path-relative behavior intact. cases.json selects the parent-approved ten original cases; no case/rubric content changed.

Eight fixture tests pass. Read-only actual-assets preflight passed and generated a disposable rebuild. These do not prove hosted MCP behavior; real smoke execution and independent audit are still pending. The helper is deliberately small and specific to this reviewed transition, not a generic migration framework.

Challenge points: verify exactly four intended targets; no prior runtime/model pins changed; snapshots cover oldDB/all authored/catalog/manifests; mutable source hash preconditions; partial-write rollback; no claim of multi-file crash atomicity. Power-loss recovery requires inspecting retained journal/snapshots. Parent owns documentation count changes and later smoke results.

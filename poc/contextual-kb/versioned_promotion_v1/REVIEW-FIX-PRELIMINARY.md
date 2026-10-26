# Preliminary independent promotion review

Review instance: 2 of 3

Scope verified at HEAD d5a82fac7d03136137fbafa7c7faeeb15dbfa1c2 on
codex/versioned-knowledge: complete working-tree changes and new candidate/promotion
directories. No staging or code changes performed.

The assignment disclosed the prior two findings and summary of their fixes, so
this was not fully blind. Neither author explanation packet has been read yet.

Inspected canonical versioning plan, candidate/promotion plans, compiler/context/
retrieval/promotion tests, active compiler and launcher wiring, candidate compiler,
index/backend/context, installation guard, recovery allowlist and rollback rehearsal.
Source was read directly; no stale graph inference was used.

No confirmed actionable defect at this stage. The recovery allowlist now includes
the legacy compiler required by the versioned index import. Its isolated import
test uses only allowlisted Python files. Coordinated rollback now restores old
source plus DB into an isolated tree and checks legacy provenance and rankings.
The recovery instructions explicitly require matching code/DB/manifests.

Remaining verification: execute maintenance checks; inspect promotion/preservation,
rollback and live-smoke receipts; reconcile author claims; verify semantic
preservation and exact version scope independently. Tests alone do not establish
new release coverage or clean-machine installability.

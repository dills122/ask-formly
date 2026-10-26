# Versioned setup promotion

Status: **installed, qualified and independently reviewed — Ready (review2 of3)**.
Foundation9 retains 93 facts/21documents and exact Formly6.3.12 coverage only.
No newer/older release or general-major coverage was enabled.

The stable launcher now uses the reviewed scoped index/backend and the existing
MCP tool surface/audit path. Canonical authored/catalog inputs use schema2. The
active compiler validates schema2 and only builds to a new explicit isolated path.
Existing DB outputs and the installed path cannot be overwritten by the build CLI.

Installed artifact: a0f102f1bad83dfec7c91148925187644e3092a3ca08cdaa88f586a7e1a0c106.
Previous artifact: cc67af9eba6daa5024d671dd306dfd4ada4193e2663e05737d4db2bc39d9d63d.
Canonical compilation reproduced the reviewed artifact before and after guarded
installation. Recovery includes pre-promotion source/code/manifests, DB snapshot
and per-file replacement journal under private test-output/. No prior readers were
found before switching; existing stale backend objects fail closed on DB hash drift.

Candidate qualification remains historical:630ranking/105citation comparisons,
13tests, both frozen native seeds and isolated rollback checks. Promotion checks
add installed compiler/launcher wiring and stable-launcher live calls. Initial
maintenance failures were an outdated factory expectation and its test import
path; both retained in private logs and corrected before final qualification.

Models and sealed evaluation are unchanged. No final calling-agent answer-quality
score is inferred from transport/runtime checks. B06/B13 and other historical
failures retain their original status. See independent review reports in this folder.

## Final qualification and review

- 176 source tests, 149 runtime tests and 95 doctor pins passed.
- Six supported stable MCP calls returned eight facts each across seeds 1701/1702;
  two v7 calls returned unsupported_version before planning. Model checks passed.
- All 86 prior runtime pins outside the authorized DB/launcher/server changes
  remain unchanged. All 95 current pins pass. Models/evaluation remain unchanged.
- Review1 found missing legacy-compiler recovery import and coordinated rollback
  gaps. An isolated import test failed first, then passed after the dependency was
  included and pinned. The old source/DB rehearsal verified 712 snapshot files,
  schema1/93 facts, source provenance and 12 public query rankings.
- Review2 independently repeated maintenance and checked semantic preservation,
  import closure, rollback snapshots and all eight raw live receipts: **Ready**,
  no actionable findings. See REVIEW-FIX-FINAL.md.

Byte-identical DB reproduction is qualified with provisioned Python3.13 / SQLite
3.53.1. Different SQLite versions may produce different bytes; this does not justify
repinning without separate qualification. All old semantic tables are preserved.
The full rollback source/DB snapshots and raw results remain private, outside Git.

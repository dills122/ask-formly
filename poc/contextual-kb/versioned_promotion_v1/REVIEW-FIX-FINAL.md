# Independent promotion review

Review instance: 2 of 3

Reviewed complete working-tree promotion and candidate changes against
`d5a82fac7d03136137fbafa7c7faeeb15dbfa1c2`, branch `codex/versioned-knowledge`.
The preliminary report was saved before reading either promotion author packet.
The assignment itself disclosed prior findings and claimed fixes, so the pass
was not fully blind. Direct source and actual checks supplied the evidence;
no conclusions depend on the stale code graph. No implementation edits, hosted
calls, sealed evaluation access, staging or commits were performed.

## Findings

No actionable findings remain in the reviewed scope.

The prior recovery-import P2 is resolved. `packaging/runtime-files.json` includes
`kbcompiler/structured_source.py`, and `foundation.json` pins it. The new
`RuntimeImportTests` regression copies only allowlisted Python files and imports
the compiler with `-I -S`, preventing checkout/site-package leakage. Independently,
I copied only allowlisted Python/JSON/Markdown files into a disposable tree and
successfully imported `mcp_foundation.versioned` and `mcp_v1.server` under `-I`
with the provisioned interpreter. This checks the broader composition import
closure while retaining the documented dependency on installed third-party packages.

The prior coordinated-rollback P2 is resolved. The promotion README requires
restoring old source, authored/catalog inputs and manifests together with the
schema1 DB, with readers stopped and subsequent work preserved. `rollback_check.py`
validates snapshot hashes, creates an isolated old tree, imports the old composition,
lints old provenance and checks 12 legacy rankings against the rollback DB.
The retained successful receipt records schema1, 93 facts and 712 source files.
I independently verified all 712 snapshot hashes and the rollback DB hash.

## Plan Review

The implementation satisfies the current exact-6.3.12 migration and promotion
plan. The active compiler validates schema2 through the existing provenance
validator's temporary schema1 projection; exclusive output publication and the
CLI's explicit isolated path prevent ordinary builds from overwriting installation.
Normalized applicability/evidence relationships and replacement-chain validation
preserve the intended distinction between evidence release and authored scope.

The scoped index filters lexical and dense candidates before limits and retains
scope checks through expansion and citation delivery. Stable launcher composition
uses the existing settings/coverage gate and distinct adapter services; the release
catalog still rejects v7. Existing models and semantic knowledge are preserved.
The guarded installer is deliberately a one-time baseline-specific operation,
with matching source/DB rollback documented separately from per-file journaling.

Future major coverage, new releases, fine-grained version boundaries and clean-machine
distribution remain outside this promotion. Rejecting overlapping replacement
scopes is consistent with that bounded plan; it does not silently invent support.
The README diagram-only update during review accurately reflects the inspected flow.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status | Review consequence |
| --- | --- | --- | --- |
| Recovery import defect fixed | Allowlist, foundation pin, isolated regression and independent full-composition import | Confirmed | Prior P2 closed |
| Coordinated rollback rehearsed | `rollback_check.py`, recovery instructions, successful receipt, independent snapshot/DB hashes | Confirmed from source and retained execution evidence | Prior P2 closed; installation was not rolled back during review |
| 176 source / 149 runtime tests, 95 doctor pins | Fresh `python3 -B tools/project.py check` | Confirmed | Current checkout qualifies for these local checks |
| Same 93 facts / 21 documents and content | Independent read-only comparison of all five old semantic tables and all 21 authored JSON records after removing only added schema metadata | Confirmed | No semantic expansion introduced |
| Exact 6.3.12 only | Installed applicability rows, coverage gate, all eight raw MCP receipts | Confirmed | No general-v6 or v7 claim |
| Old models/pins unchanged except authorized DB/launcher/server | Independently hashed every prior manifest pin | Confirmed | All 86 other prior pins unchanged |
| Both seeds work over stable MCP | Six supported raw packets and two unsupported-v7 packets; smoke runner | Confirmed from retained evidence | No hosted calls repeated; not an answer-quality score |
| SQLite bytes are toolchain-specific | Promotion README qualifies reproducibility to provisioned Python/SQLite | Appropriately bounded | No cross-toolchain byte reproducibility assumed |

## Verification Performed

- `git rev-parse HEAD`, `git branch --show-current`, `git status --short`, diff review:
  scope and baseline match the bootstrap; changes remain uncommitted.
- `git diff --check`: passed.
- `python3 -B tools/project.py check`: exit 0, 176 source tests, 149 runtime tests,
  95 doctor pins. A database ResourceWarning appeared in an existing test group;
  it did not fail the suite or establish a promotion regression.
- Inline read-only Python checks using `mcp_v1/.venv/bin/python -I -B`: compared
  `documents`, `facts`, `evidence`, `fact_evidence`, `fact_links` between rollback
  and installed DBs; all equal. All 21 authored documents preserve previous fields.
  Installed scope is exclusively exact 6.3.12/direct; counts and SQLite integrity/
  foreign-key checks passed. Prior manifest changes are exactly the authorized three.
- Disposable allowlist-only tree, provisioned Python `-I -B`: full installed
  composition/server imports passed.
- Independently parsed all eight saved MCP response packets: six have eight facts,
  unchanged DB/model checks, correct selected version and exact applicability;
  explicit/saved core calls contain only core facts; both v7 requests reject.
- Independently verified 712 rollback source hashes and the accepted schema1 DB hash.

## Open Questions And Residual Risks

No blocking open questions. Recovery requires the retained private snapshots or
matching accepted commit and DB; this is not a self-contained public install.
The rollback rehearsal's execution is supported by its saved receipt and inspected
code, rather than a second execution during this pass. Hosted runtime evidence is
similarly retained evidence, not fresh reviewer inference. These bounded checks
do not establish unseen answer quality, whole-library support, other releases or
cross-toolchain DB byte identity. Historical B06/B13 outcomes remain unchanged.

## Verdict

**Ready.** Both prior P2 findings are resolved and the complete promotion meets
the current plan with the documented operational limits.

## Recommended Next Actions

The initiating task should record acceptance of this report, finalize promotion
status documentation, then perform the already-authorized commit/push/PR workflow.
Inspect the exact staged file list to exclude private test-output, models, DBs,
environments and sealed archives. No third review instance is required for the
reviewed implementation absent a material subsequent change.

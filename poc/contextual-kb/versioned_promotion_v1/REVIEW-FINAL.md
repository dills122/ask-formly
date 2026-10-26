# Independent promotion review

Review instance: 1 of 3. Reviewed base/HEAD d5a82fac7d03136137fbafa7c7faeeb15dbfa1c2 and the uncommitted candidate/promotion working tree. Preliminary recorded before REVIEW-AUTHOR.md. No implementation fixes or further reviewers dispatched.

## Findings

1. **P2 — Include the newly required compiler dependency in runtime recovery.** `packaging/runtime-files.json:108` includes `versioned_knowledge_v1/compiler.py`, imported by the runtime index, but omits `kbcompiler/structured_source.py`. Compiler line 11 imports that file at module load. Copying exactly the allowlisted Python files to a clean temporary directory and importing `versioned_knowledge_v1.compiler` fails with `ModuleNotFoundError: No module named 'kbcompiler.structured_source'`. Thus the documented runtime restoration can fail before serving even with environments/assets restored. Include the runtime dependency closure (and appropriate runtime integrity pins), with an isolated import test that cannot fall back to the source checkout. The complete compiler provenance distribution can remain separately required.

2. **P2 — Complete coordinated rollback instructions and rehearsal before closing the promotion.** `versioned_promotion_v1/install.py:54-60` passes only data/input/manifests to guarded replacement, while launcher/server/compiler dispatch changed outside that transaction. Restoring its journal alone pairs schema1/manifests with schema2 dispatch and fails startup/compilation. The separate 712-file source snapshot and matching schema1 DB are present and hash-valid, so this is recoverable; however, the planned coordinated old-code/data restoration procedure and promotion-level rehearsal are not yet recorded. Document and exercise restoration into an isolated location, including the source dispatch, launcher/server, matching manifest and DB, then verify compatibility. Existing candidate legacy-reader rehearsal does not by itself verify the new promotion rollback procedure. Author explicitly acknowledges this remaining gate.

## Plan Review

Implementation substantially follows the approved migration and promotion plan: schema2 normalized applicability/evidence links, exact-only migration, separate compiler publication, scope filtering before ranking, additive citation metadata, unchanged evidence releases and unchanged model pins. Unsupported v7 stays rejected at the gate. Stable launcher composition retains the original MCP tool and audit surface. Major/boundary expansion remains deliberately deferred rather than implied by migration. Recovery completeness is the remaining delivery gate; no architectural pivot is required.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status | Review consequence |
| --- | --- | --- | --- |
| Same 93 facts/21 documents, exact6.3.12 only | All authored JSON compared to HEAD after removing only schema/applicability additions; installed applicability query | Confirmed | No broadened compatibility claim |
| Canonical compilation equals reviewed installed artifact | Independent disposable build in the provisioned MCP environment, SHA256 a0f102f1bad83dfec7c91148925187644e3092a3ca08cdaa88f586a7e1a0c106 | Confirmed | Source/data reproduction established |
| Five original semantic tables preserved | Read-only installed versus rollback table comparison | Confirmed | Existing facts/provenance/links preserved |
| Models unchanged and runtime additions pinned | Foundation old/new comparison; doctor validates current pins | Confirmed for existing pins | Only prior DB/launcher/server pins changed; new compiler runtime dependency needs recovery treatment |
| Source/runtime checks pass | Independent full check and stdlib-only compiler test run | Confirmed | Local qualification succeeds |
| Six supported/two unsupported stable-launcher smokes | All eight raw call receipts plus summary, both seeds | Confirmed | Runtime/transport and scope behavior established, no answer-quality score inferred |
| Recovery allowlist complete | Clean allowlisted-module import | Contradicted/accepted by author | Finding 1 |
| Rollback preservation and forthcoming rehearsal | All 712 snapshot hashes; prior DB hash; journal; author packet | Preservation confirmed; procedure/rehearsal pending | Finding 2 |
| No legacy readers at switch | Author testimony; no contemporaneous independent process observation | Unverified | No claim of independent verification of past process state |

## Verification Performed

- `python3 -B tools/project.py check` — exit 0; source tests, doctor and active regressions pass. Full independent log: `test-output/reviewer-maintenance.log`.
- `python3 -B -S -m unittest discover -s poc/contextual-kb/versioned_knowledge_v1 -p test_compiler.py` — 8/8 pass without site packages.
- Disposable canonical build using `mcp_v1/.venv/bin/python` (SQLite 3.53.1) — byte-identical hash to installed/reviewed DB. Initial system `python3` attempt (SQLite 3.53.3) produced f0a00a7ca5dbf33e00a3f0f84406dc2df24dfc0eba08b0c3f8d7eb1bc2bc9d0e and failed the byte-equality assertion; byte reproducibility is environment-dependent, so the provisioned environment must be used for artifact qualification.
- Read-only integrity check — `ok`; foreign-key check — no violations; schema 2; 93 facts; only exact6.3.12 applicability.
- Original documents/facts/evidence/fact_evidence/fact_links — identical to rollback tables.
- Every before.json snapshot entry — 712/712 hashes valid; rollback DB hash cc67af9eba6daa5024d671dd306dfd4ada4193e2663e05737d4db2bc39d9d63d.
- All eight raw hosted smoke receipts inspected: six eight-fact packets, native parameter integrity, DB unchanged, advisory available, exact applicability, core settings preserved; two unsupported-v7 packets contain no facts. No hosted calls repeated.
- Isolated allowlist-only compiler import — fails as described in Finding 1.

Graph coverage checked for relied-on code. Generation 2026-10-25T14:19:41Z is stale/untracked for the target, so conclusions rely on direct source reads and executed checks, not graph completeness.

## Open Questions And Residual Risks

Fresh-machine/model-enabled recovery and general library answer quality remain unqualified. The factory unit test asserts planner type, while installed backend routing is established primarily by inspected composition and live packet evidence. Existing candidate rollback tests remain historical after promotion and must not be run by repinning their baseline. Sealed archives were not opened. Earlier failures, including B06/B13, retain their historical status.

## Verdict

**Not ready** to close promotion/publish as fully reviewed until both bounded recovery gates are resolved. No additional runtime correctness finding was identified in the current provisioned checkout.

## Recommended Next Actions

Accept or dispute each finding with evidence. Add the recovery dependency/import regression, finish the coordinated rollback procedure and isolated rehearsal, rerun affected checks, then request the next independent pass within the remaining two-instance budget. No heavy pivot or scope expansion is needed.

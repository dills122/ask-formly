# Pre-apply independent review

Review instance: 1 of 3

## Preliminary review (before author explanation)

Scope verified at HEAD `250f83da2d93aababf27f169078807ff66f183ee`, branch `codex/n1-radio-native-promotion`. The promotion-v13 directory is untracked; the backlog modification and unrelated untracked experiments/configuration are excluded. No installation was performed.

Direct inspection covered the plan, mechanism and smoke contracts, both new implementation files, their tests, the reused promotion-v7 transaction and api-contracts-v1 report. Graph lookup returned no promotion-v13 symbols; coverage marked relevant source untracked, so conclusions rely on direct source inspection rather than graph completeness.

No blocking defect identified in this first pass. The exact DB digest and eight-table checks, old-source byte preservation, additive catalog validation, qualification seal/report gate, fixed replacement construction and post-install canonical reproduction align with the contract. The reused transaction snapshots before replacement and restores on BaseException. Thirteen focused tests passed with the qualification interpreter.

Items requiring reconciliation: establish that the fixed specification accurately carries the five old target hashes and both original manifests; confirm review-pin and provenance inventories; distinguish transport equality from semantic qualification; retain the documented lack of multi-file crash atomicity and require post-install model-backed evidence assessment. Live installed smoke is necessarily pending promotion.

## Findings

No actionable findings in the bounded pre-apply mechanism and smoke-runner scope. The preliminary reconciliation items are resolved below. This is readiness for the authorized guarded application, not a claim that installation or installed qualification has already succeeded.

## Plan Review

The plan orders the work appropriately: review and immutable candidate verification precede installed writes; the transaction performs postchecks before success; exact installed transport replay, bounded hosted smoke, doctors/full maintenance, current documentation and final independent review precede publication. The mechanism changes only nine new authored files and five existing data/manifest targets. Inspection of `intended_changes`, `prepare`, `verify_installed`, and promotion-v7 `guarded_replace` supports that boundary. Both runtime manifests are deep-copied and change only identity, knowledge metadata and the DB pin.

The five specification snapshots match the currently installed target bytes. The embedded old catalog, old runtime manifests and old source-preservation map match the current originals. The 27 source additions comprise original drafts and their source-note/provenance companions; nine canonical authored targets and the updated catalog pin are added to the resulting preservation map. All 299 review pins verified independently. The executed dry run additionally checks all 326 protected pins, the old authored inventory, additive catalog, 68 new facts, full eight-table superset and exact canonical SQLite bytes.

The unchanged historical report is run as a subprocess before installation and verifies the complete assessment inventory/hash seal, receipts and repeated packet equality. Its current saved result reports 24/24 targets, 8/8 controls and 8/8 regression requests, three passing fixed-plan repeats and 399 calls. The pinned prior semantic review separately supports the bounded judgments. This review verifies continuity with that prior review; it does not repeat an independent semantic assessment of all 80 historical answers.

`installed_smoke.py` loads all 44 sealed candidate packets in report order, removes only the caller plan for the five specified model-backed requests, and uses the stable launcher. Model-free execution requires the offline marker and equality of complete result objects; receipts retain attempted/unattempted calls and errors. The model-backed path intentionally records delivery only: actual returned evidence still needs human/agent assessment under SMOKE-PLAN.md.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status | Review consequence |
| --- | --- | --- | --- |
| Exact192 DB, nine new documents/68 facts, old27 unchanged | `prepare`, `intended_changes`, `rows`, `canonical`; reviewer dry run | Confirmed | Canonical byte and eight-table checks passed with the qualification interpreter. |
| Only five existing targets change; runtime/models preserved | Fixed changes construction, actual specification snapshots, protected pins and manifest reconstruction | Confirmed pre-apply | Post-install verification remains mandatory and is wired into the transaction. |
| 299 review/input pins,326 protected pins | Independent hash script and executed preflight | Confirmed | Review and qualification continuity is bound to checked artifacts. |
| Qualification recomputed with mandatory seal | `qualification`, unchanged `report.main`/`verify_assessment_seal`, successful dry run, pinned final review and saved report | Confirmed | Supports bounded fixed-plan results, not general accuracy. |
| 44-call model-free replay and five calls per hosted seed | `candidate_rows`, `launcher_args`, `run`, tests and SMOKE-PLAN | Confirmed implementation | Live post-install execution remains pending. |
| Six mechanism and seven smoke tests pass | Reviewer executed discovery with qualification interpreter | Confirmed | Thirteen tests pass, including interrupt rollback and fail-closed checks. |
| Historical red-first tests/system-Python failure | Author account and mechanism notes | Not independently reproduced | No present readiness dependency; reviewer used the prescribed interpreter and strict equality passed. |
| No multi-file crash atomicity | Reused transaction source | Confirmed limitation | Retain snapshots/journal and avoid concurrent installed mutation during application. |

## Verification Performed

From repository root:

- `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/promotion-v13 -p 'test*.py'` — 13 tests pass.
- Read-only Python SHA-256/JSON comparisons — all five original target hashes, original catalog/manifests/source map and all299 review pins agree with current files.
- `poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v13/promote.py --name reviewer-preapply-instance1` — exit0, `Preflight passed; no installed changes`. The bootstrap explicitly allowed this dry run; its preflight artifact is retained under this promotion's test-output. Temporary canonical DB is cleaned up.
- Graph status/search and coverage for both implementations/tests, reused transaction and qualification report — no usable graph coverage for the new scope; direct source fallback used. No graph completeness claim.

No `--apply`, hosted inference, sealed global archive access, staging, commit or publication occurred. Full local maintenance and actual installed smoke were not rerun in this pre-apply review; they remain required in the plan after installation.

## Open Questions And Residual Risks

No unresolved question blocks application. The transaction is designed for a single local operator and ordinary exceptions/interrupts, not concurrent writers, abrupt process death or machine failure across its multiple files. Preserve the recovery journal/snapshots. Exact canonical bytes depend on the qualification Python/SQLite environment, which was used successfully here. Installed model-backed output may still expose omissions; delivery receipts alone cannot qualify those answers. The knowledge remains exact Formly6.3.12 core/Material with bounded evidence, not whole-library coverage.

## Verdict

**Ready** for the authorized pre-apply promotion step. No blocking or non-blocking code finding remains in this review scope. This is review instance1of3; no further reviewer was created.

## Recommended Next Actions

Apply with a fresh output name using the qualification interpreter, then run `--verify-installed`, the44-call model-free replay, both five-request hosted seeds with evidence assessment, both doctors and full maintenance. Preserve all failures and snapshots. Complete the planned current documentation and final independent review before commit/push/PR update.

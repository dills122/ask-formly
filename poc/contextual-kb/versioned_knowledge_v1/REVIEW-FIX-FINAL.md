# Independent review — ancestor fix and complete candidate

Review instance: 2 of 3.

## Findings

No actionable findings remain in the reviewed isolated candidate. The prior P2 transitive replacement overlap is resolved: `compiler.py:97`–`112` recursively collects all ancestors, retains cycle and missing-target rejection, and compares every ancestor's applicability with the descendant before accepting it. `test_compiler.py:93` exercises exact 6.3.12 -> major 7 -> major 6 and requires failure without a published DB. The retained RED receipt shows that this test failed before the correction; the current 13-test suite passes. Scope overlap is rejected at authoring time, consistent with the explicit boundary policy.

## Plan Review

Ready against the candidate PLAN.md and the pre-promotion portion of docs/versioned-knowledge-plan.md. Baseline is foundation8, 93 facts / 21 documents, commit d5a82fac7d03136137fbafa7c7faeeb15dbfa1c2 on codex/versioned-knowledge. Git status contains only the untracked candidate directory and no tracked diff.

The implementation provides explicit format/schema 2, normalized applicability and evidence links, preserved source/provenance validation via a temporary legacy projection, deterministic one-way migration to exact 6.3.12 scopes, exclusive candidate publication, and an opt-in read path. Scoped IDs and vectors apply eligibility before lexical/dense truncation; inherited related expansion is constrained by the scoped fact dictionary. Selector-pool/fallback testing and citation/source-quote guards cover downstream escape paths. Existing response fields remain, with additive applicability and actual evidence release metadata.

Accepted settings/version gates run before candidate dispatch. The backend deliberately provisions only the accepted 6.3.12 baseline. General major/minor boundary routing, new release admission, installed migration, CI integration and promotion remain outside this candidate. This is consistent with the agreed isolated implementation boundary; candidate readiness does not authorize promotion. README documents coordination of schema, readers, pins and rollback for that later step. Historical failures and the unsuccessful sandbox smoke remain retained.

## Author-Claim Reconciliation

| Claim | Evidence inspected | Status | Consequence |
| --- | --- | --- | --- |
| Ancestor-overlap defect fixed with RED/GREEN | compiler.py DFS; test_compiler.py regression; ancestor-red.txt; independently run 13 tests | Confirmed | Prior P2 closed |
| Selector cannot admit foreign-scope candidates | test_retrieval.py:52; scoped index; inherited repair integration | Confirmed for tested boundary | Supports downstream eligibility contract |
| Six live supported calls and two unsupported v7 calls across both seeds | All eight raw smoke-1701/1702 call JSON files; advisory/selection/runtime fields, facts/adapters/citations | Confirmed | Operational smoke completed, not answer-quality scoring |
| Native parameters and DB unchanged on supported calls | Raw runtime.model_checks and db_unchanged fields, plus independent asset-pin checks | Confirmed | Both native seeds exercised without recorded parameter drift |
| Post-fix rebuild matches tested DB | Independently compiled migrated copies into a temporary directory and compared complete bytes | Confirmed | Compiler fix does not change tested candidate artifact |
| Preserved source and installed assets | Independent qualify.preserved(baseline) | Confirmed: 690 tracked files / 89 foundation assets | Installed state remains intact |
| Old/new semantic and retrieval parity | Independent six-table comparison; comparison.json; fresh 12 public queries across all six ranking configurations and citations | Confirmed for observed inputs | 630 ranking / 105 citation comparisons recorded; 72 / 12 independently repeated |
| Rollback compatible with old reader | final-verification.json and independent PilotIndex against rollback.sqlite for 12 public queries | Confirmed | Isolated recovery evidence, not installed switch rehearsal |

The original author packet's pending-live/11-test statements are superseded by REVIEW-FIX-AUTHOR.md and observed receipts. Its statement that runtime code did not change after the live run is author testimony; no immutable pre-run source snapshot was supplied. The current source, candidate byte identity, raw receipts and independent checks agree with the claimed outcome.

## Verification Performed

- `PYTHONPATH=poc/contextual-kb:poc/contextual-kb/mcp_v1 poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/versioned_knowledge_v1 -p 'test_*.py'`: 13 tests passed.
- `python3 -B tools/project.py check`: exit 0, source checks and local foundation checks passed, doctor verified 89 assets. Existing test output included a ResourceWarning and intentional invalid-seed CLI rejection without failing the suite.
- Independent read-only Python verification: all 690 tracked/89 foundation hashes match; documents, facts, evidence, fact_evidence, fact_links and facts_fts equal across installed, candidate and rollback DBs; disposable rebuild byte-identical.
- Independent offline model verification: 12 fixed public queries, lexical/dense/hybrid at limits 8 and 20 (72 comparisons), 12 citation comparisons and 12 legacy rollback-reader rankings passed. ONNX emitted a telemetry persistence warning and used an in-memory identifier; results passed.
- Checked raw hosted receipts without repeating provider calls: six supported calls each returned eight facts, available advisory, successful selection and unchanged parameters; two v7 calls returned unsupported_version without facts.
- Inspected existing 105-query comparison and final-verification receipts, retained failed sandbox receipt, and RED regression evidence.

Graph Tier 2: generation 2026-10-25T14:19:41Z; candidate search returned no symbols, and coverage flags all 11 candidate Python files not_tracked. Supporting legacy index/backend/integration files report metadata_changed. All relied-on code was directly read; no claim rests on graph completeness. Preliminary report was written before reading either author explanation. Initial assignment disclosed the prior finding, so the first pass was not blind to the known defect.

## Open Questions And Residual Risks

No blocking question remains for this isolated candidate. The visible public queries and operational smokes do not establish unseen accuracy, whole-library compatibility, new-release support or calling-agent answer quality. Candidate code depends on preserved internal legacy interfaces and recomputes embeddings per adapter service; broader adoption needs its own integration review and operational qualification. Overlapping replacement boundaries are intentionally rejected rather than conditionally resolved. No sealed evaluation was opened, no installed database rebuilt, and no code was edited by this review.

## Verdict

**Ready** for the agreed isolated, opt-in candidate scope. This verdict is not approval to install or promote schema 2 or to enable additional Formly releases.

## Recommended Next Actions

Return this report to the implementation task and retain the candidate and receipts. Close the accepted P2 finding. No third review instance is needed absent a material further change. Treat any future promotion as the separately reviewed coordinated code/data operation required by the plan.

# Independent review

Review instance: 1 of 3.

This verdict covers the pre-fix implementation independently inspected in this pass (11-test suite). The author subsequently reported a compiler fix and 13 tests; those later changes are not reviewed here and require instance 2. Final live receipts and protected-byte checks were reconciled before closing.

## Findings

### P2 — Check scope overlap across the whole replacement ancestry

`compiler.py:102–105` checks applicability overlap only between each fact and its immediate replacement target. An intermediate fact can therefore hide an overlapping ancestor. Independently reproduced with `three` (major 6) replacing `two` (major 7), which replaces `one` (exact 6.3.12): compilation succeeds and `Index.for_scope('6.3.12')` returns both `sample/one` and `sample/three`.

These represent a changed-behavior chain, yet the retrieval layer has no precedence or ambiguity contract to choose between the overlapping versions. This bypasses the candidate plan's explicit rejection of overlapping changed-behavior applicability. The migrated baseline has no replacements and is unaffected, but the newly implemented authoring contract is incomplete.

Smallest correction: reject overlapping applicability with every reachable replacement ancestor, retaining cycle detection and fail-closed behavior. Add a three-node regression, including a disjoint valid chain. No architecture pivot is needed.

No additional actionable defects were established in this pass. Rollback rehearsal evidence below should still be closed before final readiness.

## Plan Review

The isolated implementation fits the authorized scope: no tracked implementation files changed, no installed DB or model was modified, no real release coverage was added, and sealed evaluation remained unopened. The accepted baseline is foundation8 at d5a82fac7d03136137fbafa7c7faeeb15dbfa1c2, with 93 facts and 21 documents.

The normalized applicability tables, explicit format/schema versions, exact-only migration, foreign keys, provenance projection, exclusive candidate publication and scope filtering address the central proposal. Inherited dense ranking uses only eligible vectors; lexical eligibility precedes LIMIT; inherited related expansion sees a restricted fact dictionary. Selector acquisition/presentation consumes that same scoped index, source quotes are guarded, and final citations reject out-of-scope IDs. Existing response fields survive with additional applicability metadata.

Reusing the accepted ContextLookup is safe for the current single-release catalog: its explicit selected-release check blocks future catalog entries from silently reaching the hardcoded 6.3.12 backend. Restricting real routing to the accepted baseline and rejecting overlapping boundaries is a defensible deliberate limitation. That rejection needs the ancestry fix above.

The opt-in package avoids disturbing the installed compiler and runtime. Separate indexes per adapter service and recomputed in-memory embeddings are disclosed costs, acceptable for this bounded candidate. Promotion remains a separately authorized code/data operation.

## Author-Claim Reconciliation

The preliminary report was recorded before reading REVIEW-AUTHOR.md. The author explanation was then checked against source and receipts.

| Claim | Evidence | Status and consequence |
| --- | --- | --- |
| All baseline semantics preserved | Independently compared documents, facts, evidence, fact_evidence, fact_links and facts_fts | Confirmed |
| Protected bytes unchanged | Recomputed all 690 tracked pins and 89 foundation pins | Confirmed |
| Deterministic candidate | candidate.sqlite equals reproduced.sqlite byte for byte | Confirmed |
| 630 rankings and 105 citations match | comparison.json and qualification source; independently repeated 72 rankings and 12 citations | Receipt confirmed; independent subset passed |
| Replacement validation fails closed | Compiler source, two-node tests, independent three-node fixture | Contradicted for transitive overlap; P2 above |
| Scope enforced through selector and citations | Index, inherited policy/integration/backend, direct source_quote guard | Confirmed by source; synthetic selector integration coverage could be strengthened but no bypass found |
| Catalog expansion cannot enable backend | Accepted ContextLookup selected-release guard | Confirmed |
| Rollback preserved | rollback.sqlite hash equals accepted baseline hash; old code and installed DB unchanged | Preservation confirmed; an isolated old-code/copy reopen rehearsal remains appropriate before promotion |
| Live/native verification complete | Final smoke-summary.json: six supported calls and two unsupported calls across seeds 1701/1702 | Confirmed operational success and unchanged native parameter checks |

## Verification Performed

- `PYTHONPATH=poc/contextual-kb:poc/contextual-kb/mcp_v1 poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/versioned_knowledge_v1 -p 'test_*.py'`: 11 tests passed.
- `python3 -B tools/project.py check`: passed, including source checks, foundation8 doctor and installed runtime regressions. A ResourceWarning appeared in existing tests; no test failed.
- Independent read-only baseline checks: 690 tracked files and 89 foundation assets unchanged; rollback hash matches baseline; candidate/reproduction bytes match; all six semantic tables equal.
- Independent real local embedding comparisons: 12 public prepared queries, each lexical/dense/hybrid at limits 8 and 20, for 72 exact rankings; 12 citation packets match after removing only added applicability metadata.
- Independent temporary fixture reproduced the three-node replacement overlap described above. Temporary resources cleaned up; no candidate or installed artifact edited.
- Inspected seed1701 raw stdio receipts: legacy, explicit core and saved-project core each return eight facts; native parameter checks are unchanged, selection is unchanged, and v7 returns unsupported_version without facts. This is operational evidence, not answer-quality scoring.
- Checked Git scope: sole untracked candidate directory on codex/versioned-knowledge; HEAD matches bootstrap.

Graph coverage was checked for all relied-on candidate and legacy source paths. Candidate paths were untracked and legacy paths had metadata freshness gaps. Conclusions rely on direct source reads, not graph completeness. No hosted calls were duplicated and no sealed questions were read.

## Open Questions And Residual Risks

Before closing this report, smoke-summary.json became available: all six supported calls and two unsupported v7 calls passed across seeds 1701 and 1702. Native parameter checks passed. The reviewer repeated all protected-byte comparisons after completion; all remained unchanged. The retained initial sandbox failure is accurately disclosed and must stay in history.

The rollback copy is verified, but restoration against the installed path was intentionally not attempted. An isolated reopen of that copy with compatible old code is sufficient rehearsal for this unpromoted candidate; actual deployment restoration belongs to separately authorized promotion work.

Synthetic and public regression queries establish structural correctness and baseline parity, not general v6/v7 compatibility or universal answer accuracy. Historical B06/B13 failures remain untouched.

## Verdict

**Not ready.** Correct the replacement-ancestry validation defect. Existing baseline behavior and preservation have strong evidence; no heavy pivot is required.

## Recommended Next Actions

1. Accept/dispute/defer the P2 with evidence; add the regression and fix ancestor overlap validation.
2. Record an isolated rollback reopen with the legacy index; completed native-seed live receipts and final preservation checks already pass.
3. Use review instance 2 of 3 after the compiler behavior changes, with this report and completed receipts available. Do not promote or add release coverage as part of the fix.

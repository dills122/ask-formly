# Independent review

Review instance: 1 of 3. Scope: additive retrieval_repair_v1 implementation and assessment/native diagnostic addenda on dirty main at c3091328f49d53de6b41a49c4fe5aa8f1c45e516. Unrelated repository changes excluded. Tests and implementation inspected before AUTHOR-EXPLANATION.md; preliminary ledger saved first. Graph coverage reported inspected Python files not_tracked, so review used direct source reads. No provider/model reruns initiated by reviewer; sealed evaluation was not interpreted.

## Findings

No unresolved actionable serving-code defect identified. The independent review found that experiment.py:score compared covered-group counts rather than identities, which could hide loss of one group behind acquisition of another. Author accepted this finding and added assessment.py:compare_groups plus two discriminating tests. The frozen experiment and its coarse summary remain provenance. The authoritative identity audit and independent recomputation both report zero group losses.

The frozen promotion acceptance criteria are not met: F01's first foundation plan fails exact-copy validation, leaving F01-1/2/3 unavailable. This is a real qualification failure, even though the underlying foundation is outside this patch. Retain the candidate as opt-in and do not claim the original gate passed. This finding does not call for an unauthorized foundation redesign or further tuning loop.

## Plan Review

The bounded repair architecture follows the agreed scope: unchanged foundation/advisory path, same full-question strings at lexical/dense depth 20, complete candidate union plus baseline, opaque selector handles, at most two atomic replacements, and original stored facts/citations. Deterministic checks prove membership, bounds and quote correspondence, not semantic relevance. Failed optional selection retains baseline; IntegrityError propagates and new DB drift is checked after selection. Empty-question selection is bypassed.

All 84 slots were retained: 77 actual provider selections, four empty-question bypasses and three F01 upstream failures. Nine packets changed. Original M03 callback support was recovered 3/3. Six valid fresh callback slots already had callback support and retained it; they are not fresh recovery gains. Historical labeled relevant gains total three; labeled losses and per-group losses are zero. All nine changed decisions were inspected, including their removals and reasons. Unsupported cases remain unchanged.

The ASSESSMENT-ADDENDUM explicitly broadens diagnostic continuation after conditional retrieval success despite the failed overall gate. This is a disclosed deviation from the original native-test prerequisite, not promotion evidence or a replacement for F01. Both adapter smoke runs completed. All six live selections were unchanged: these runs establish new-launcher integration and supported answer handling, not live replacement execution or causal answer improvement.

## Author-Claim Reconciliation

| Claim | Evidence | Status / consequence |
| --- | --- | --- |
| Bounded slots and original records preserved | policy.py, integration.py, all 84 persisted decisions replayed through apply_repair | Confirmed; no sparse reselection or packet overflow |
| Foundation/query/advisory behavior unchanged | immutable hashes, integration tests, all panel query strings, six live plans and runtime checks | Confirmed within inspected boundary |
| Ordinary failure falls back; integrity remains fatal | nine original new tests, inherited suites, mocked subprocess failure probes | Confirmed; semantic nonregression still depends on labels and selector judgment |
| No useful baseline fact lost | strict historical/fresh labels and independent group-identity audit | Confirmed on measured valid plans only; no general guarantee |
| Callback retrieval repaired | three original M03 replacements | Confirmed there; fresh valid and native callback packets already supported context |
| Native answers remain appropriately qualified | two complete caller outputs, all six audited packets | Confirmed: M03 partial with missing required recipe; M05 unsupported validator/message; M07 preserves value/control distinction |
| Overall acceptance completed | original summary and final-gate.json | Contradicted if asserted: strict gate false, conditional retrieval gate true |

## Verification Performed

Independent commands used poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover with test_*.py for retrieval_repair_v1 (9 original tests) and mcp_v1 (11). python3 -B ran the prior advisory_lookup_v1 suite (35). The new test_assessment.py suite passed two additional tests. Logs are test-output/review-unit.txt, review-original-mcp.txt, review-advisory.txt and review-assessment.txt.

Reviewer-only mocked subprocess probes passed spawn-failure receipt preservation, timeout process-group termination/reaping, valid response, tool rejection, duplicate-key rejection and incomplete response rejection. A mocked serve.py entrypoint verified the new Backend/Selector, seed 1702 and stdio wiring. The first launcher probe omitted an import path before patching and failed; corrected harness setup mirrors the actual launcher and passed. No production source was changed by reviewer.

review-input-audit.json validates all saved plans and full deep-query strings. review-panel-audit.json independently checks all 84 decisions against their separate files, deterministic repair validation, unique eight-slot/two-replacement limits, frozen relevant labels and per-group identities. review-native-audit.json checks all six real packets against the original read-only DB facts/citations, validates plans, and verifies both native adapter parameter checks. Frozen design hashes and preserve.snapshot match protected-before after native completion.

Final README.md, RESULTS.md, native_audit.py and its completed audit-summary were inspected after evidence completion. Their distinction between conditional retrieval success, native integration checks and failed overall promotion matches the evidence. The author audit additionally checks client/server packet delivery identity and original baseline replay parity.

## Open Questions And Residual Risks

F01 remains unavailable and R26's historical semantic plan limitation remains disclosed. Gold labels are development evidence, not held-out accuracy. A matching source substring cannot establish semantic relevance or correctness of a removal. There is no proof of broad answer accuracy, full knowledge coverage, provider determinism or improved whole-answer latency. The extra hosted selection call adds latency. Mocked timeout cleanup is verified, but no native timeout was induced. New live requests happened not to execute a replacement; the real-provider packet panel and integration unit test cover that branch separately.

## Verdict

**Not ready for promotion.** The bounded implementation and measured conditional retrieval behavior are sound enough to retain as an opt-in diagnostic candidate, but the original all-slot acceptance gate failed. Do not collapse that distinction into a passing readiness claim.

## Recommended Next Actions

Retain the original default MCP, preserve the failed F01 slots and all first outputs, report conditional gains with their exact denominator, and close this bounded experiment without further tuning. Any future foundation investigation or new qualification protocol is a separately scoped decision. No heavy pivot or additional review instance is requested by this review.

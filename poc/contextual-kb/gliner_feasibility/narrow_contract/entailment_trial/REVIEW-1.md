# Independent preparation review

Review instance: 1 of 3. Scope: entailment_trial and BEST-QUESTION-CONFIGURATIONS.md. Fresh delegated reviewer context; author explanation not read before this preliminary ledger. Parent bootstrap includes test history and scope constraints, not the author rationale.

## Preliminary ledger (recorded before author explanation)

- All 24 authored questions and 25 gold occurrences inspected: substrings/Unicode/repeated occurrence offsets match intended role labels. Twelve contrast pairs include explicit negation and repeated identical literals with distinct roles. No actionable annotation defect identified.
- NLI-18 has no gold and no supplied negative probe: the fresh oracle cannot measure no-entity rejection there. Operational extraction still includes this question. Treat fresh oracle results as gold-only, and retain old-panel negative counts separately.
- Fixed policy, same-span grouping, no-entity abstention, exact-offset preservation and change/damage accounting appear consistent with protocol. Ten pure tests pass independently.
- Need verify all 30 original requests and 60 focused questions against frozen source, caches/manifests and model identity before readiness.
- Need reconcile preservation dependencies: runner imports existing helper modules; additional source/cache/label bindings should be in readiness receipt.
- Graph generation is stale (2026-10-16); search returns no matching POC symbols and relevant paths are not tracked. Direct source inspection is the basis for this bounded review.

## Findings

No actionable blocking findings in the frozen preparation scope. No fixes made. The fresh oracle has 25 positive probes and zero negative probes; its scores must not be described as a fresh negative-rejection test. Existing shadow/adjudicated panels supply separate negative diagnostics, consistent with the author explanation.

## Plan Review

Ready to execute the bounded diagnostic, not qualified for serving. The plan separates raw extraction, operational occurrence scoring, supplied-span oracle, and manual usability. The fixed absolute 0.8/margin 0.2 policy, retention on abstention/no-entity, all-span damage accounting and both-seed aggregate gate implement the declared experiment. The whole request and exact offsets survive. No raw extraction is replaced, new candidate span created, optimizer invoked, retrieval called or DB opened by the runner. Usability60 is deliberately not included in the labelled development gate; its annotation safety remains a mandatory subsequent independent review.

The 30 original requests and full beta1 output objects exactly equal their frozen sources, and the 60 derived rows exactly preserve question text, reason, request association, original request and global constraints. H11 remains in usability-plans with an empty question list; it must still receive manual assessment. The fresh24 annotations follow the reviewed shadow rule: prose component/model-address terms are not APIs, quoted supplied names/values retain quotes, backticks are excluded, complete paths/opaque expressions suppress inner mentions, repeated occurrences are distinct. All 12 pairs/25 positive spans were inspected.

## Author-Claim Reconciliation

| Claim | Evidence | Status and consequence |
| --- | --- | --- |
| Ten pure tests pass | Independent unittest discovery, ten tests | Confirmed; historical red run is parent testimony, not independently replayed. |
| No gold enters operational scoring | run.py score signature and operational-before-oracle loops | Confirmed; gold remains attached to stored rows only for later assessment. |
| Both seeds and old raw caches are retained | panels(), both epoch-6 paths, four exact cache ID/text comparisons | Confirmed; old panels are replay, not new extraction. |
| Fresh negatives are not new malformed probes | prepare.py, all fresh rows, explanation | Confirmed; fresh oracle has no negative probes of any kind. |
| Preservation is checked before/after, including failure | audits(), guarded_run() and verify_manifest() | Confirmed statically and current manifests verified. |
| v2 questions/constraints are unchanged | Exact equality against cases.json/beta1.json and reconstruction of all derived question rows | Confirmed, including H11. |
| Best configurations are a bounded evidence inventory | Numeric comparisons against the cited v2, role-boundary, flat-decoding, A/B and shadow reports | Confirmed; no promoted serving/answer accuracy claim. |
| Download uses a pinned model | model-revision.json plus local config/model assets | Locally frozen; remote download provenance is author testimony. Config declares entailment=0 and not_entailment=1. |
| Overlap audit reports no normalized duplicates against 302 prior questions | overlap-audit.json | Not independently reproduced across all source panels; conceptual overlap and author-generated nature remain explicit. No unseen/generalization claim is permitted. |

## Verification Performed

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s poc/contextual-kb/gliner_feasibility/narrow_contract/entailment_trial -p test_entailment.py -v`: 10/10 pass.
- Standard-library equality check of every original request/full output and derived focused-question row: 30 originals, 30 plans, 60 focused questions, empty plan H11.
- Exact ID/text equality for both seeds' shadow30 and adjudicated30 cached extraction sources: four panels pass.
- Streaming SHA256 verification of inherited preservation manifests plus shadow37/full-run54/sealed-preparation85/diagnosis5: 38,106 entries checked unchanged, plus the two v2 source bindings. Sealed content was hashed only, never parsed or shown.
- Direct source inspection of scoped Python modules and relevant imported runtime/load_model/token/validation/preservation helpers; no inference, tokenizer loading, training, application execution or sealed evaluation performed.
- Git boundary: branch main, HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516, extensive unrelated pre-existing tracked/untracked changes excluded. Scope is the new entailment_trial directory and BEST-QUESTION-CONFIGURATIONS.md, not the full working tree.
- Graph status/search/coverage checked; stale generation and untracked POC sources required direct-source fallback. No exhaustive repository graph claim made.

## Open Questions And Residual Risks

A small author-written development sample cannot establish generalization, calibration, production latency or answer correctness. Seven hypotheses may fail to resolve semantic roles; this is what the diagnostic tests. The ten tests cover pure decisions/accounting rather than real model loading; runtime compatibility remains a first-run uncertainty. Model scores are shared across seeds/panels and must retain cache-labelled aggregate timing. Full text-plan usability and structured-hint safety require subsequent review of original requests and both seeds' actual raw annotations. No numeric usability score is approved here.

## Verdict

**Ready** for the one frozen no-training development run only. Review instance: 1 of 3. A hash-bound review-ready.json authorizes the exact reviewed inputs and dependencies. No serving adoption, sealed evaluation, tuning, label revision, or post-result retries are authorized by this verdict.

## Recommended Next Actions

Run once with bytecode writes disabled, preserve all outputs/failure receipts, and complete the independent result/usability assessment. Report fresh oracle positives and old-panel negatives separately. Preserve both seeds and keep hints optional; a development gate pass cannot stand in for final usability approval.

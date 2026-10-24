# Verifier evaluation wiring results

Implemented fixed shared threshold selection, same-offset conflict resolution, raw and accepted-output metrics, preservation gates, sealed evaluation stage ordering, and repeated latency measurement. Existing training harness and all prior components remain unchanged.

## Executed evidence

- 32 unit/integration tests pass. Initial implementation and both review correction rounds include saved failing-test evidence before fixes.
- Real native smoke: both frozen extractors with existing disposable one-update verifier adapters, 30 development/calibration questions. No optimizer ran. No qualifying shared threshold was selected; diagnostic only. This is not evidence of improved extraction.
- Synthetic end-to-end integration covers paired selection, evaluation and repeated timing; mocked CLI tests exercise failed preparation and denied evaluation. Synthetic outcomes are not Formly accuracy results.
- Current pure decision logic replayed the frozen smoke predictions: selected=null, diagnostic_only=true (test-output/smoke-replay-final.json).
- Final protected audit: 37,925 checks unchanged (test-output/protected-final-3.json). Both baselines, A, v2, data/DB and prior experiments remain protected.

## Remaining execution

An independently authored and reviewed sealed 40-question fresh set with hash-bound review receipt is still needed. Preparation checks coverage, train/calibration leakage and native span transport before optimization. Then the explicit full-training stage may run both 124-update adapters, calibration selects a shared threshold, and only a valid frozen decision permits historical/fresh evaluation and timing. No full training, real historical evaluation or fresh evaluation ran in this implementation turn. Native transport and full-model efficacy remain experimental.

Independent review status is recorded separately in REVIEW-1.md, REVIEW-2.md and the final review report when returned.

## Final review disposition

Three independent passes found bounded issues, all addressed. The last pass found a timing failure-path issue; its correction passed a new failing-then-passing regression and the complete 32-test suite, but has not had another independent review. Last independent verdict: Not ready on the pre-fix version. Review budget reached; full training remains unstarted. See REVIEW-3.md.

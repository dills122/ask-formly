Review instance: **1 of 3**

## Findings

No actionable findings remain for the bounded compatibility experiment.

The preliminary P2 evidence gap in `check.py::verify`—comparison of emitted probabilities only, with potentially truncating `zip`—is closed by `check_all_logits.py`. Its completed results cover all seven logits and assert native output counts for all four adapters across eight questions. Maximum observed logit difference was **5.73e-6**. The original frozen implementation and evidence remain unchanged.

## Plan Review

The implementation follows `PROTOCOL.md`: exact supplied spans, independent sigmoid role decisions, boundary veto, unsupported-offset reporting, two frozen baselines, and two fresh disposable one-step LoRA adapters. No full training or operational integration occurs.

The protocol correctly separates mechanical compatibility from semantic usefulness and identifies the further dataset, threshold, nonregression, repair, and latency work required before full training.

## Author-Claim Reconciliation

| Claim | Assessment |
|---|---|
| Public explicit-span scoring matches native attribute scoring | Confirmed against installed GLiNER source and supplemental runtime results. |
| Eight training questions, 60 spans: 37 gold and 23 malformed; all six roles represented | Confirmed from retained panel and membership-check implementation. |
| Nonzero finite gradients; only LoRA parameters change | Confirmed by harness and completed receipts: norms 3.0474/2.7678, 99 changed LoRA tensors each. |
| Exact first-save parameter/output parity | Confirmed by executed assertions and receipts. |
| Protected artifacts unchanged | Both recorded checks cover 37,824 entries with zero differences. |
| Eleven tests failed before implementation | Wording is imprecise: retained red evidence shows a module-import failure preventing test execution; green evidence and my rerun show eleven passing tests. |

## Verification Performed

- Read protocol and tests before implementation and author explanation.
- Checked branch/HEAD and explicit working-tree boundary.
- Independently ran the supplied unittest command: **11 tests passed**.
- Inspected installed native encoding, explicit-span scoring, temperature adjustment, and multilabel sigmoid attachment.
- Independently recomputed original and supplemental freeze hashes: unchanged.
- Inspected completed initial and supplemental runtime evidence without rerunning write-once checks.

Graph coverage reported examined paths as untracked; conclusions use direct source inspection.

## Open Questions And Residual Risks

Private GLiNER schema/attachment APIs remain pinned dependencies. Frozen-state assertions cover named parameters, not all buffers; the author explicitly acknowledges this limitation. Synthetic logits establish decision mechanics, and gold-supplied spans establish transport compatibility—not extraction quality, calibration, or learned boundary/role accuracy.

## Verdict

**Ready** for the bounded compatibility conclusion only. This verdict does not approve full training or operational adoption.

## Recommended Next Actions

Retain both evidence runs and describe the result as mechanical compatibility. Review training labels, threshold selection, and operational acceptance gates before undertaking full training.

---
Author response: Accept the parity-evidence finding; supplemental assertions and evidence
address it. Accept the wording correction; the author explanation now explicitly says
the red run failed at import before test execution. No behavior changed after review.

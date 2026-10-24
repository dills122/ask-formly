# Author explanation

Scope is verifier_evaluation only; existing main HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516
and unrelated dirty files preserved. User requested remaining threshold/resolution/eval
wiring with TDD and independent review before full training. Frozen plan is authoritative.

Pure decisions module separates same-offset routing, accepted-envelope metrics, raw
correct-mention preservation, supplied probes, fixed-grid paired threshold selection,
prior correct repairs and final qualification. Pipeline performs baseline-only inference
first and oracle probes in a separate second pass; no gold offsets reach resolver.
Timing is one warmup/five alternating repeated passes; all/eligible/passthrough latency
and cold loads separately recorded. Runtime reuses POC models/scoring transport, checks
full verifier state hashes and frozen baseline replay, then maps historical416/622 data.
Stages/CLI enforce a preparation/training/calibration binding and reject smoke or absent
thresholds before evaluation loaders. Existing training harness remains frozen and is
invoked only by explicit later train stage. No optimizer exists in the evaluation code.

TDD import-red then12tests, pipeline-red then16tests, stages-red then19tests. Actual smoke
used both existing one-update disposable verifiers and frozenextractors on30development
questions; no new training. selected=null, diagnostic_only=true: no qualifying threshold
on these smoke models; this is expected to be reported as insufficient, not efficacy.
No real historical/fresh contents read or evaluated this turn; old run source inspected
only to construct the deferred historical adapter. No new fresh data authored yet.

Review1 preliminary concerns accepted for correction: prepare must require a bound
independent seal-review receipt and validate fresh coverage/transport before optimizer;
raw metrics must be separately reported/gated alongside accepted-envelope metrics;
unresolved decisions need explicit boundary/role/unsupported reasons. These are bounded
wiring fixes, no architecture change. Old smoke artifacts remain unchanged. A fresh
review after material corrections is required before readiness claims.

Limits: actual full-trained models and full416+40question regression/timing run are not
executed. Synthetic orchestration and old smoke demonstrate mechanics only. Independent
fresh dataset/review receipt remains an execution prerequisite, not a claimed existing
artifact. Private pinned GLiNER schema transport persists. Stage hashes enforce artifact
consistency, not cryptographic proof of human review; independent review is the process
that produces the bound receipt. No data/DB/retrieval/answer work is in scope.

Review corrections complete: independently bound review receipt plus structural/native
transport qualification before train; raw metrics/gates alongside accepted metrics;
specific abstention reasons and boundary/role counts. Nonfinite native probabilities
now raise a runtime failure, distinct from unsupported alignment. Added invalid-to-valid
wrong gate. Supplemental synthetic40case end-to-end test and real CLI with mocked
external I/O verify gate order without models/evaluation. These are not efficacy tests.

Review2 corrections: finite checks now occur on native logits before sigmoid, with
positive/negative infinity and NaN regressions. Supported-only negative rejection is
explicit alongside unchanged total-denominator gates. Both new tests failed first;
31 tests now pass. No additional model or held-out run occurred for these corrections.

Review3 found swallowed timing scorer failures. Accepted and fixed after failing warmup
and measured-pass regressions; 32 tests pass. Material correction has not received a
further independent review because the three-instance limit is reached. No full training.

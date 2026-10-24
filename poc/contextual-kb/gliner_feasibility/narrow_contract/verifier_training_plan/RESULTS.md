# Verifier training design preparation

Prepared labels and a fixed decision protocol; no full training, model predictions,
threshold choice, or operational extraction comparison was executed.

## Labels and data

Seven independent binary targets: complete plus six complete-and-role labels. Valid
mentions have complete and one role positive; malformed spans have all seven zero.
Exact role and boundary rules, ambiguity handling and plain API-property inventory are
in LABEL-CONTRACT.md. Existing training-only inputs are preserved, not rewritten.

- 242 source training questions,580valid mentions,534malformed spans.
- 216 occurrence-bearing questions eligible for optimizer exposure;26 empty questions
  retained as no-mention/passthrough checks, not undefined or zero-diluted BCE rows.
- 30 newly authored development/calibration questions,71valid mentions,30malformed spans.
- Native collate-only qualification: all1,215 training/calibration spans exactly
  representable,zero unsupported; no encoder forward or model predictions.
- Zero normalized exact training/calibration duplicates. Maximum nearest-question
  character similarity0.6932. Thematic Formly overlap is accepted; this small author-
  created calibration set is not held-out and does not establish generalization.
- All37,856 inherited protected-file checks passed, including the frozen verifier
  compatibility experiment, both baselines, A, v2 and locked data/DB chain.

## Selection and acceptance

Nine predetermined boundary/role threshold pairs, one shared pair across both seeds.
Calibration first filters unsafe/lossy pairs, then ranks worst-seed repairs/rejection
with deterministic tie breaks. Exactly gold role must pass on each supported gold probe;
multiple-role abstention does not evade the gate. No eligible pair means stop, not a
post-evaluation threshold search. Zero operational repairs means diagnostic-only result.

Historical diagnostics and independent fresh evaluation cannot select thresholds or
supply training targets. Fresh evaluation includes fixed negative families/counts.
Gates prohibit new wrong repairs/lost correct mentions, preserve established correct
repairs, require >=90% malformed rejection (unsupported included in denominator),
>=1 actual fresh conflict repair per seed, and bounded added verifier latency. Raw
passthrough, rejection, unresolved outcomes and correct repair remain distinct.

## Review corrections and limits

First review identified empty-row loss, incomplete calibration API inventory, permissive
calibration abstention and unspecified fresh negative counts. Each was accepted and
amended before the fresh second review. Initial collate qualification stopped at an
empty-row assertion; qualification.log retains it. Revised qualification passed.
Initial review-freeze is historical and intentionally differs after amendments;
review-2-freeze freezes the amended design and datasets.

The training harness is not implemented here. Next work is TDD implementation of the
fixed loss/schedule, threshold selection, conflict-only resolution and regression gates,
with an independent implementation review before full training. Private pinned GLiNER
schema transport remains a dependency; calibrated accuracy and latency are untested.

Independent review2: Ready for design preparation only; no actionable findings remain.
See REVIEW-2.md. Full training and operational adoption are not approved by this verdict.

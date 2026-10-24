# Author explanation for design review

Scope: only verifier_training_plan; no training/resolution code changes. Branch main,
HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516; unrelated dirty repository preserved.
User requested finalized training labels, threshold selection, regression criteria and
independent review before full training. POC AGENTS/STEERING and PROTOCOL are governing.

LABEL-CONTRACT fixes seven binary targets: complete plus six complete-and-role claims.
Malformed spans have all-zero targets, avoiding inconsistent role positives on rejected
boundaries. Ambiguity is a labeling failure, not no_entity. Shared parameters remain a risk.
PROTOCOL fixes data splits, later training budget, routing, nine-pair threshold grid,
shared pair across seeds, lossless regression criteria, fresh improvement and timing gates.
The latency budget is explicitly an experimental choice, not a user-provided SLA.

Materialized training labels preserve exactly242 prior training questions,580gold mentions
and534 prior malformed negatives with exact offsets. There is no new supervision from
old evaluation. Thirty newly authored calibration questions contain71gold and30explicit
negative spans, including quoted role reuse and complete bracketed API paths. All are
visible development material. Conversion was a one-off standard-library artifact-writing
command, not a runtime dependency. Artifacts and source hashes are the reproducible target;
no training pipeline has been implemented. Exact source-slice and membership assertions
ran during conversion. A delimiter-parser issue with trailing brackets was corrected
before the review freeze; assertions checked expressions['props.required'] and [] exactly.

qualification.json records native collate-only offset alignment and character-nearest
training comparisons; no encoder forward, predictions, thresholds or optimizer is run.
protected-after.json extends the prior protected chain including verifier compatibility.
review-freeze.json freezes initial reviewed plan/labels. Final-freeze will capture reports.

New calibration examples are small and author-created; they cannot prove generalization.
Character similarity audits do not establish semantic independence. The fresh evaluation
must be independently prepared and held back from tuning. Abstention is separate from
correct repair, unsupported boundaries are not learned rejections, and preserving files
is separate from preserving final operational correctness. Strict gates may reject all
nine pairs; that is an explicit negative result, not grounds to tune on diagnostics.

Next implementation must TDD the label loader, loss denominator, seeded exposure schedule,
threshold tie breaks, fail-closed decisions and regression accounting. Independent
implementation review remains before training. This design review neither certifies an
unbuilt harness nor authorizes a new model promotion. Please challenge annotation context,
threshold leakage, unsafe acceptance, oracle-span mixing, and hidden regression tradeoffs.

Accepted review findings:26 no-mention rows excluded from optimizer,216eligible remain;
calibration inventory revised to include explicit plain property names; calibration
requires exactly gold role; fresh negative families/counts fixed. Initial native
qualification stopped on an empty-row assertion; retained log records the failure.

# Frozen verifier training and decision design

Preparation only in this directory. Full training is NOT executed by this plan.
Keep both original role_boundary_adaptation after-1701/1702 epoch-6 adapters, A, v2,
all historical experiments and data/DB unchanged. New adapters start independently
from the existing local pretrained gliner2.5-base-v1 checkpoint, not a continued
experimental scorer. No outside project imports, library changes or downloads.

## Data and leakage boundary

Training: exactly the 242 questions and matching 534 negative occurrences in
native_attribute_contrast/test-output/{train.json,training-negatives.json}; do not
reuse any old fresh/evaluation questions for training or threshold choice. Materialize
seven binary targets using LABEL-CONTRACT.md; preserve source IDs, offsets and hashes.
Frozen originals remain unedited. Review conversion membership and exact slices.

Calibration: 30 newly authored Formly-only questions in calibration-marked.txt, with
inline role annotations converted to exact offsets in test-output/calibration.json.
These are development data, exposed to authors/reviewer, NEVER called held-out.
Gold is annotated without seeing verifier outputs. They may not enter gradient training.
For malformed calibration probes use only explicitly marked negatives in the resulting
artifact, never operational oracle spans. Review labels before training. Before run,
check normalized-question duplicates and near-template overlap against training;
record any accepted thematic overlap. No existing sealed evaluation contents are opened.

Fresh final evaluation: independent 40-question set written/annotated and frozen by a
fresh reviewer after training/calibration inputs and code are frozen, before examining
candidate predictions. Keep it inaccessible to training/threshold tuning. Include at
least 10 repeated-spelling cross-role questions, 10 quoted/bracketed boundary cases,
10 unfamiliar API/registration names and 10 ordinary mixed Formly requests. These
four bins are disjoint primary groups; roles and syntax may overlap. Include at least
eight gold occurrences per role across the set and four no-mention questions. Fresh
supplied probes comprise all gold occurrences plus exactly48 semantic negatives:
12 clipped API paths,12 broken quoted literals,12 merged adjacent mentions,12 nested
code fragments; plus4 deliberately unsupported inside-token negatives,52 negatives total.
Annotate each negative against its question context before model outputs, verify it is
not a valid alternate mention, and record family/offsets. Never feed these oracle spans
to operational resolution. If family/coverage requirements cannot be satisfied, fix
annotations before exposure and review the frozen set; never resample after outputs. Include all six
roles, no-mention questions and partial-overlap conflicts. If baseline outputs offer
no resolvable conflicts, record insufficient operational evidence; do not manufacture
oracle candidates or change evaluation questions after seeing predictions.

Historical regression panel: use all 416 operational questions and 622 supplied probes
from native_attribute_distillation_trial as diagnostics only. Once code and thresholds
are frozen, reproduce frozen baseline outputs before comparison. Never turn their
observed failures into new training/threshold tuning within this experiment.

## Training recipe to implement later

Two new seeds 1701/1702. LoRA r8/alpha16/dropout0 on encoder and extractive_head;
CPUfloat32, four threads, deterministic algorithms. AdamW lr1e-4, weight_decay .01,
gradient clipping1, 124 updates, eight question exposures/update (992 total). Exactly216 occurrence-bearing
training rows enter the optimizer; the26 no-mention rows remain frozen passthrough/
no-mention diagnostic checks and never dilute the BCE denominator. A seeded cyclic
shuffle of those216 rows consumes across cycle boundaries and logs each exposure;
every eligible row must be covered. Record all26 excluded IDs and their explicit reason. No checkpoint/seed selection, scheduler or early stopping.
For each question: mean BCE over all supported supplied occurrences × seven binary
labels; mean those eight question losses per update. No teacher, KL, continued old
adapter, native proposal loss, hard-negative mining or reweighting in this first trial.
Unsupported-only row is an error in preparation, not a silent zero-loss batch.
Save/reload at update1 and124: full state_dict hashes (parameters AND buffers), exact
panel logits, restore all RNG states. Optimize only newly created LoRA parameters.
Verify original model file hashes, baselines and all protected manifests before/after.

## Operational scope and resolution

Use each frozen extractor's existing flat-decoded output, with unchanged extraction
schema/threshold. Only groups of >=2 different proposed roles at EXACT same offsets
are eligible. Never generate new mentions, resize spans, process nonconflicting mentions,
or resolve partial overlaps. If a group overlaps another distinct span, retain it raw.
Score all six roles plus complete on original text at those offsets. Accept only when
complete >= t_boundary, exactly ONE of all six role scores >= t_role, AND that role is
among the original proposed roles. If multiple roles pass (including unproposed roles),
none pass, alignment fails, or any score is nonfinite: retain original raw unresolved
group with a diagnostic reason. Never delete the whole group to improve precision.
If accepted, retain that one original mention; no invented text/offset/role allowed.
Thus some originally correct mentions in conflict groups can still be lost by a wrong
resolution: regression gates below explicitly prohibit this. Safe abstention is not repair.

## Threshold selection (development only)

Fixed grid: t_boundary × t_role, each in {0.50,0.70,0.90}: nine pairs, no later grid
expansion. Apply EACH pair to BOTH seeds on calibration outputs and supplied probes.
The same pair must be used by both seeds. Eligible only if, for each seed: zero wrong
operational resolutions, zero lost originally correct mentions/whole-exact questions,
zero rejected supported gold probes, and exactly the gold role (and no other role)
passing on every supported gold probe. Multi-role abstention on gold fails eligibility.
Unsupported gold is coverage failure, never success. All unsupported counts reported.

Rank eligible pairs lexicographically: maximize minimum correct operational repairs
across seeds; maximize minimum malformed rejection fraction across seeds; maximize
sum correct operational repairs; then choose higher boundary threshold, then higher
role threshold. Malformed rejection means boundary fails, distinct from merely no role
passing. Log all nine candidates and exact tie-break values. If none eligible, STOP
with no calibrated candidate. If all eligible pairs make zero repairs, keep best pair
for diagnostic reporting only; no operational improvement claim or adoption.
Freeze selected pair and code before fresh evaluation; never pick per-seed thresholds.

## Regression and improvement gates

Report separate raw extraction, operational resolution, supplied-span role decisions,
boundary rejection and abstention metrics; no aggregate score may hide a lost occurrence.
For each seed, each historical/fresh set, require:
1. Zero new wrong resolutions, zero lost baseline-correct exact (offset,role) mentions,
   zero lost baseline-wholly-exact questions, no increase in invalid outputs or errors.
   Every nonconflicting raw mention is byte-identical by construction and replay check.
2. Preserve every correct operational repair from the original native_attribute_training
   epoch-6 scorer where it was actually correct on shared historical cases; its wrong
   repairs may revert to raw unresolved. Do not require imitating wrong teachers.
3. On supplied probes: zero supported gold boundary failures; exactly the gold role
   passes for every supported gold occurrence; reject >=90% malformed spans via boundary
   on EACH set. Report total denominator including unsupported and supported-only rate;
   the 90% gate uses total denominator, so unsupported is not learned success.
4. Per-role operational precision/recall/F1 cannot decrease from baseline (undefined
   after previously defined fails); zero new critical boundary/role errors. List every
   gain/loss with original and candidate decisions, never net away losses.

A promising operational improvement additionally requires >=1 correct resolution of
an ACTUAL fresh baseline conflict PER seed, zero fresh wrong resolution, and all gates
above. Failure is a negative result, not permission to tune on the fresh set.
A case without candidate conflicts is a passthrough test, not evidence verifier repairs.
Probe gates are stringent evidence for this trial, not a guarantee on unseen inputs.

## Latency and decision

Measure cold model load separately. Measure frozen extraction, verifier-only eligible
work, and combined question-layer time on same CPU with no concurrent jobs. One warmup,
five alternating repeated passes per seed; report p50/p95/max and conflict counts.
Experimental budget: added verifier warm p95 <=1 second per question with <=8 eligible
groups. More than8 eligible groups causes whole-question passthrough/unresolved, reported
as overflow (no partial selective processing). This is a new bounded experiment gate,
not an asserted user SLA or end-to-end target. No-conflict inputs must skip verifier
inference; report overhead. Adoption requires all functional gates and budget per seed.

## Required order

1. Review label contract, data provenance, calibration annotations and these gates.
2. Implement training/resolution/selection/evaluation harness with TDD and independent
   implementation review. Qualify token coverage and duplicate audit; freeze executable
   config and complete inputs before optimization. No pending annotation exclusions.
3. Run fixed training; calibrate only on development. Freeze decision before fresh tests.
4. Run diagnostics/fresh evaluation and timing; independently review results. No promotion
   unless every gate passes. The present design review does not certify unbuilt harnesses.

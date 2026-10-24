# Anchorless adaptation experiment — execution protocol v1

Status: prepared for review; not executed. This document specifies the next
experiment, not a completed implementation or permission to open evaluation.
It updates the original ADAPTATION-EXPERIMENT-DESIGN.md for the reviewed
identity revision. Prior design, annotations, runs and review evidence remain
unchanged. User scope: prepare the experiment and improvement criteria before
running it. No new training, annotation, inference or evaluation in preparation.

## Question and comparison

Can supervised encoder adaptation improve complete question frames, including
separate requested aspects sharing a target, without introducing critical errors
or losing responsiveness? Better entity extraction alone is not success.

Compare G0 (untouched local base) with G1 and G2 (fresh independent adaptations,
seeds 1701 and 2903). All three use the same frozen anchorless schema, descriptions,
public inference settings, validation and scoring. G0 uses anchorless records too;
otherwise changes to representation would be confounded with training.
Neither seed starts from the pilot's trained adapter. A remains unchanged and is
not run here. This experiment does not establish superiority over A.

Only question frames are trained/scored. No retrieval-plan adapter, generated
search queries, retrieval, evidence, answer assembly or MCP changes. No knowledge
labels, facts, answer labels or fact IDs. Data/DB/corpus/compiler/index remain
locked. New code, third-party environment, caches, datasets and artifacts stay in
this POC; no outside-project implementation imports. Execution artifacts belong
in a new, exclusive full_training/test-output/<run-id>/ directory. Do not overwrite
prior evidence. The earlier 24 pilot cases are training-exposed forever.

## Frozen representation and model

Use existing GLiNER2 2.1.0 and local GLiNER2.5 base revision
54785d51df8d86a0d8f2eb212fec15871aad2c4d. Freeze actual installed package/runtime
versions, model hashes and schema bytes before execution; no upgrades or downloads.

Use native anchorless request records and the checkpoint's existing 32 instance
queries. `target_anchor` remains a source field, never the identity key. Two
records may share it. Preserve the canonical pilot guide and its adjudicated v2
clarifications, source occurrences, all record fields, typed entities, explicit
has_value/refers_to endpoint pairs, and clear/needs_clarification classification.
Absent relation types remain explicit zero-edge tasks. Do not rewrite gold to
fit model output, merge records by anchor, add repair heuristics, or infer APIs.

Freeze schema serialization and descriptions from the reviewed revision. Native
training preprocessing is strict: no silent dropped labels or truncation. More
than 32 gold records is a capacity failure, not a case to silently discard. Report
coverage limits. Prediction uses real public inference with threshold .5, nested
overlap and classification argmax. No gold candidates, gold injection or oracle
assignments in development predictions, G0 predictions or eventual evaluation.
Native decoding must preserve repeated source occurrences; conversion cannot
silently select the first occurrence of an equal string.

## Data and isolation

Retain the original proposal: 120 training, 30 development, 60 sealed evaluation.
Training includes the existing 24 pilot questions plus 96 new questions, not 120
additional questions. No new questions are authored by this preparation document.
The existing pilot gold SHA256 is
bea23e707cc9bb1d7df10467eec65f33addbbce832b7c641eb9962ec21f4e67b.

Group scenario/template families before partitioning. Paraphrases, minimal
positive/negative pairs, punctuation variants and API-name substitutions stay
in one partition. Allocate primary strata exactly as the parent design: 20/5/10
per train/dev/evaluation stratum, across multi-aspect/shared context, negation,
exact APIs/literals, version/adapter scope, references/ambiguity, and ordinary
clear questions/comparisons. Apply the parent's overlapping evaluation quotas;
include same-target distinct asks, shared action, repeated occurrences, Unicode,
code and clear controls. A family may have several cases, but never cross splits.

Preserve original independent pilot annotations/agreement and corrections.
Double-annotate all dev/evaluation cases and a stratified 24 of the remaining
training cases; audit the other 72. Annotators see no predictions. Resolve
ambiguity and define acceptable semantic boundary variations before predictions.
Before training require >=90% raw agreement on aspect counts and ambiguity and
>=.90 span/attachment F1 on each double-annotated pool, then adjudicate. If the
threshold fails, revise the guide with a new version and reannotate affected
training/dev cases before freeze; preserve first-pass agreement. Evaluation
custodian applies the same rule without revealing content to implementation.

A separate custodian must prepare/check and seal evaluation, including family
contamination checks against exposed diagnostics and training/dev. The trainer
receives only train/dev allowlists and opaque evaluation manifest metadata.
Neither evaluation text nor gold is available to trainer, annotators of train/dev,
or implementation workers. No claim that an existing folder alone establishes
separation. If separate custody is unavailable, mark readiness blocked; do not
read the set or rename exposed cases as held out. All existing evaluation remains
sealed during preparation and training. Custody creation/release is a later step.

The original 12 development diagnostics and exposed A/B cases are excluded from
fresh splits and checkpoint selection. No diagnostic expansion is needed here.

## Training choices and fixed budget

| Setting | Fixed choice |
| --- | --- |
| Initialization | Fresh pinned base for each seed; no pilot adapter |
| Parameters trained | Encoder LoRA only; all task heads/base parameters frozen |
| LoRA | rank 8, alpha 16, dropout 0 |
| Optimizer | AdamW, learning rate 1e-5, weight decay .01, constant LR |
| Device | CPU, float32, four threads; no cloud or hardware substitution |
| Batch / accumulation | 2 examples / 8 microbatches (effective 16 except final group) |
| Duration | Exactly 8 epochs unless a safety/compatibility failure stops the run |
| Update limit | 8 updates per 120-case epoch, at most 64 per seed |
| Gradient clipping | Global norm 1.0, once per optimizer step |
| Sampling | No random task/field dropping or shuffling; freeze full SamplingConfig |
| Training proposals | Full gold injection (1.0), as compatibility-tested |
| Inference | Actual predicted proposals only; fixed threshold .5 |
| Resource bound | Parent controller: four-hour wall-clock cap per seed worker |

These are experimental choices, not library recommendations. Encoder-only is the
configuration actually tested; there is no task-head learning rate or implicit
head unfreezing. Changing trainable heads requires a separately revised experiment.

Implement an explicit bounded loop extending the reviewed native-forward/AdamW
smoke, using native trainer LoRA setup. Do not claim ExtractorTrainer.train has
been qualified. Add epoch shuffling, accumulation, dev inference and checkpoint
selection as tested POC harness behavior. Normalize accumulated losses by the
actual example count: the final eight examples form a partial group, not a group
of sixteen. Freeze/test the reduction against equivalent microbatch gradients
with stochasticity disabled. Never carry residual gradients across epochs.

Seed Python random, NumPy where used, and PyTorch. Record RNG state, order and
batch fingerprints. Use no parallel data-loader workers. Request deterministic
algorithms; unsupported nondeterminism is a failure to investigate, not a reason
to weaken equality checks. Preserve RNG states around verification so verification
does not change training order/dropout sequences. Disabled schema-drop settings
do not eliminate Python random choice of example presentation, as the pilot showed.

Require expected task losses, finite values/gradients, exact trainable inventory,
and unchanged frozen parameters. Log every update, all task losses, elapsed time,
example IDs and failures. Timeout/cancellation/invalid targets/nonfinite values
stop the seed; do not silently retry, exclude cases or launch a replacement seed.
Keep all artifacts. Offline human grading is outside the worker time cap and its
time is reported separately. No sweep or performance-based early stopping.

## Close the first-save gap before it can recur

The prior run's missing pre-first-save losses remain missing. This experiment
must capture the original in-memory state before the first write of EACH seed's
first trained checkpoint, and before every epoch checkpoint eligible for selection.
A second save/reload of an already saved artifact is not a substitute.

Use the fixed 24 training pilot cases as the verification panel, never dev or
sealed evaluation. For each checkpoint:

1. Pause optimization and snapshot model mode and all RNG states. Persist a
   pre-save receipt containing step/epoch/seed, schema/config hashes and a digest
   of every parameter tensor (including frozen base and heads).
2. Before saving model weights, record full prepared-batch fingerprints and each
   named loss plus total loss on all 24 cases. Use model.train() under no_grad()
   with per-case Python/NumPy/PyTorch seeds; require record and relation losses
   rather than accidentally omitting them by switching to eval mode. Separately
   capture deterministic public predictions, including confidences and spans,
   in eval mode. Verification performs no optimizer step or gradient accumulation.
3. Write an immutable pre-save receipt and outputs/losses. Then save the adapter
   into a new checkpoint directory. Record manifest order and checkpoint hashes.
4. Load an entirely fresh pinned base plus that adapter. Recreate identical
   batches and RNG states and compare every parameter hash, every named scalar
   loss, total loss, and every decoded output EXACTLY on all 24 cases. Record
   per-case differences, not just a boolean. No tolerance relaxation on failure.
5. Check the original model's parameters remain unchanged by verification; restore
   training mode/RNG states. Mark checkpoint verified only after all comparisons
   pass. An unverified checkpoint cannot enter selection or evaluation. Stop the
   seed on a failed first-save check, preserving pre-save evidence and failure.

This verifies inference and objective transport, not optimizer resumption.
Automatic resume is outside this experiment; no claim of resumable training.
First-save instrumentation must be demonstrated with TDD and a bounded pilot-only
preflight before either full seed starts. A preflight uses disposable state and
is never the initialization for G1/G2. Its execution is not part of this preparation.

## Selection without touching evaluation

Record public predictions on all 30 development cases after each epoch. Run G0
once with exactly the same schema/decoding. Preserve all eight checkpoints and
outputs per completed seed. Blind/randomize dev outputs for two graders using the
frozen rubric below; reconcile disagreements before joining arm/epoch metadata.
Select each seed's highest semantic complete-frame count, then fewer cases with
critical errors, then earliest epoch. No test-set checkpoint selection, threshold
search, schema edits or cherry-picking one seed. Require selected checkpoint
verification receipts and freeze selection before any evaluation release.

A failed run yields an incomplete experiment, not a selected partial success.
Do not use evaluation to decide whether to continue training. Before eventual
release, freeze both selected artifacts, G0, runtime/schema/decoder/scorer hashes,
data manifests, rubric, hardware, run logs, development decisions and thresholds.

## Improvement criteria fixed before running

Retain the original thresholds. They are proposed feasibility gates, not claims
of statistically proven deployment safety. Primary metric is complete question
frames out of 60 for G0, G1 and G2 separately. A complete case must have all and
only the requested aspects with correct targets, requests, attached shared/local
conditions, negation, identifier/literal spelling, scope, occurrence-specific
pairings and ambiguity handling. Record order/IDs do not matter; one-to-one
semantic matching is required. Correct count alone and whole-question copying
receive no completeness credit. Hallucinated aspects fail completeness.

Exact metrics match source offsets, entity types, record attachments and relation
endpoints. Semantic grading may accept an adjudicated harmless span-boundary
variation; never accept a dropped negator, altered API/literal, wrong occurrence,
wrong condition attachment or guessed antecedent. Ambiguous cases need the correct
status and grounded unresolved reference; unwarranted clarification fails clear
cases. Two blinded graders adjudicate semantic scores before arm/timing disclosure.
No after-the-fact rubric exceptions. Keep exact and semantic scores distinct.

Both seeds must independently pass ALL gates:

| Gate | Required result |
| --- | --- |
| Complete frames | >=48/60 AND >=10 additional complete cases versus G0 |
| Critical errors | Zero observed polarity/condition inversions, silent scope substitutions, necessary identifier/literal corruptions |
| Runtime/structure | Zero backend errors and invalid outputs; these count as failed cases, never excluded |
| Exact identifiers/literals | Micro precision >=.95 and recall >=.90 |
| Conditions/negation/scope attachments | Micro precision AND recall >=.90 for EACH category |
| Ambiguity classification | Precision AND recall >=.90 for needs_clarification |
| Stratum regression | No primary stratum loses more than one complete case versus G0 |
| Warm frame latency | p95 <=500ms AND <=1.5 times G0 on identical host/runtime |

Also report aspect precision/recall, typed API and literal metrics separately,
relation-pair precision/recall and exact case accuracy, ambiguity confusion matrix,
invented-aspect counts, each stratum and all failures. Relation co-membership never
counts as a correct edge. Use N/A for empty denominators; an absent required
category means the dataset is not ready, not that the gate passed. Omission always
fails completeness even if it is not one of the defined critical-error categories.

For future evaluation: one fixed pass supplies semantic outputs; after three dev
warmups collect five paired passes rotating arm order, batch one, no concurrent
work. Include parsing/validation in latency; report cold loading separately.
Use nearest-rank p95 over all 300 request times per arm. Repeats are not independent
questions. Report output variation; any critical/runtime/invalid-output error in
any repeated pass fails its corresponding zero-error gate. No retries to improve
latency or correctness. Preserve failures and timeouts in reported counts.

Report paired wins/losses against G0 and family-clustered bootstrap 95% intervals
for completeness differences (10,000 resamples, seed 4109; resample whole families,
keep paired arms together). Report sample/family counts and individual-seed results.
Do not present two seeds as 120 independent questions. Threshold passing with wide
intervals remains limited feasibility evidence. Zero observed critical errors in
60 questions does not imply zero population risk.

If only entities improve: entity-only research finding. If one seed passes:
unstable adaptation. If quality passes but latency fails: unsuitable for this
responsiveness gate. If both pass: recommend a separate retrieval-plan adapter
study and a fresh comparison against unchanged A; do not automatically integrate.
No frame score establishes usable search requests, retrieval or answer accuracy.

## Preparation and execution checkpoints

See READINESS.md for work units, failing-test requirements and evidence required
before execution. All gates currently remain unexecuted. The fourth independent
review was used for identity compatibility, not this full training harness.
No new independent review is silently allocated by this document. Obtain explicit
scope for any further review instance before assigning it. Full training and
custodian evaluation release remain separate later actions, not part of the
current preparation request.

Evidence basis: ../identity_revision/FINDINGS.md and
../identity_revision/evidence/independent-review.md; prior proposal
../../ADAPTATION-EXPERIMENT-DESIGN.md and pilot annotation guide/clarifications.
Installed-version compatibility takes precedence over main-branch API assumptions.

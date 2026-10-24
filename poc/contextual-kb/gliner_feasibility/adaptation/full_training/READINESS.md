# Implementation and readiness checklist

Prepared protocol only. No full training harness, new dataset, new independent
review, first-save preflight or evaluation run has been performed in this step.
Existing original first-save losses cannot be recovered retrospectively.

## 1. Freeze inputs and annotations

Files: data manifest, guide reference, split/custody receipts, validation tests.
Depends on: accepted protocol and separately arranged evaluation custody.

- Retain pilot gold and its hash; annotate 96 additional training and 30 dev cases
  under the protocol. Custodian alone handles 60 evaluation cases.
- Verify family-disjoint partitions, quotas, independent annotation agreement and
  adjudication before any predictions. Preserve raw labels and provenance.
- Freeze train/dev bytes and allowlists, package/model/schema manifests, and
  protected A/data/DB/prior evidence hashes. Deny worker access to other sets.

Acceptance: all counts/labels valid, no dropped targets, no contamination findings,
no evaluation content available to training/implementation. Test guards with
synthetic forbidden paths; never open actual evaluation to test its denial.

## 2. Implement and prove first-save verification (TDD)

Files: checkpoint verifier, first-save tests, evidence serializer.
Depends on: frozen schema/pilot; does not require new data or full training.

Write failing tests before implementation for:

- Losing an unsaved adapter parameter, task loss or record field must fail.
- A verifier that compares only a saved adapter with its own resave must fail the
  receipt-order requirement. Original in-memory receipt must precede first save.
- Equal predictions with unequal losses must fail; missing record/relation losses
  must fail; torch-only RNG seeding must reproduce the preprocessing mismatch.
- Wrong batches, changed frozen parameters, wrong base/schema hashes, nonfinite
  values and metadata serialization failures must fail without a success receipt.
- Successful exact comparison restores model mode and all RNG states and changes
  neither parameters, accumulated gradients nor optimizer-step count.
- Existing output paths cannot be overwritten; incomplete/failed receipts cannot
  qualify a checkpoint. Synthetic fixtures must include duplicate target records.

Acceptance: retained red/green tests and real 24-case first-save preflight receipt
from a disposable locally adapted model, at most 24 updates / 30 minutes, with
actual original pre-save losses/parameters/outputs and fresh-base parity. Do not
reuse this adapter as either seed. This preflight awaits implementation/run scope.

## 3. Implement bounded training and dev selection (TDD)

Files: runner, fixed configuration, accumulation tests, selection tests.
Depends on: 1 and 2.

- Prove 120 cases produce 8 updates per epoch, 64 total maximum; partial groups
  use actual example counts. Test finite-loss and missing-task failures.
- Verify only encoder LoRA changes; heads/base stay frozen; fresh base per seed.
- Prove checkpoint verification gates selection, seed reproducibility, timeout
  termination and failure retention. No silent restart or overwrite.
- Dev inference uses predicted proposals only; test that no gold reaches inference.
- Selection must use frozen blinded semantic grades: completeness, critical-error
  count, then earliest epoch. Show tie behavior and reject incomplete runs.

Acceptance: unit tests plus bounded native preflight; source review must distinguish
manual loop from untested library scheduling/resume features. No full run yet.

## 4. Implement scorer and isolated eventual comparison (TDD)

Files: scorer, scorer tests, runner, latency/report tests.
Depends on: rubric frozen; can use synthetic cases without evaluation access.

- Complete-frame scoring must reject extra/missing records, condition leakage,
  negator loss, identifier mutation, swapped literals, wrong duplicate occurrence,
  guessed references, unwanted clarification and unsupported whole-question copying.
- Score order-invariant one-to-one record matching, exact versus semantic boundaries,
  each attachment category, explicit relation endpoints and zero denominators.
- Demonstrate that one passing seed cannot promote the pair; critical errors or
  latency failure override completeness gains. Test exactly-on-threshold cases.
- Test blinded output packaging, immutable grade receipts, family-level paired
  uncertainty, p95 definition, all-run failure accounting and protected-path denial.

Acceptance: known synthetic score tables match expected counts, no retrieval/DB
calls or A execution, no real evaluation content read. Evaluation release remains
unavailable to ordinary run commands and requires separate custodian scope.

## 5. Pre-run review and later execution

Depends on: 1–4 completed and frozen.

- Current independent review budget: four used of four authorized. A further review
  of the new full harness needs explicit authorization; none is started here.
- Review receipt must cover original first-save evidence, real trained parameter
  inventory, accumulation, scoring/selection, isolation and run limits.
- Only after readiness and execution authorization run both full seeds. Retain
  all epochs and dev-selection evidence. Do not open evaluation during training.
- Before any later evaluation release, freeze selected checkpoints plus every
  scoring/inference dependency and confirm protected hashes. Further evaluation
  requires separate scope; it is not implied by preparing or training models.

Prepared protocol does not mean implementation-ready evidence exists. Remaining
work is visible above; no checks are marked passed before they actually run.

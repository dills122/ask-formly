# Verifier training harness author explanation

Scope: new verifier_harness only, existing main working tree at
c3091328f49d53de6b41a49c4fe5aa8f1c45e516 with unrelated dirty files preserved.
User requested training harness implementation using TDD and independent review before
full training. Frozen verifier_training_plan/PROTOCOL.md governs training semantics.
This implements its training component, not later operational/evaluation orchestration.

harness.py: validates exact seven-target rows; separates216optimizer/26coverage rows;
seeded cyclic schedules124×8; per-question then per-batch BCE; LoRA-only optimizer guard;
full-state parameter/buffer hashes; save/reload predictions and CPU RNG restoration;
step logging; first/final frozen-state checks. guarded_run ensures setup/work and final
integrity failures are recorded, attempts both final audits, and publishes completion
only on success. run.py orchestrates offline frozen input checks, native collate-only
preflight, fresh adapters, AdamW and new-only output directories. Calibration is checked
for transport/split integrity but never passed to gradients or checkpoints.

TDD: initial missing module red then9 passing tests; loop import red then11pass;
finalization import red then13pass. Tiny actual Torch model exercised124steps/992
exposures; that is not GLiNER full training. Actual GLiNER smoke-001 ran one update
per seed with8training rows each,198trainable states changed and no frozen changes;
564state entries and exact panel predictions matched reloads. All37,873 protected
checks passed. Smoke is disposable, not an efficacy test. No sealed evaluation reads.

First independent review confirmed a reporting bug: completion could be written before
a failing final audit, and final input drift could skip the protected audit. Accepted:
guarded_run and tests now retain phase-specific failures, execute independent final
checks, and forbid completion on failure. New CLI preflight exercises corrected
orchestration without model forward or optimizer; original smoke evidence retained.

Full training has NOT run. --mode full exists as explicit later operation, never the
default. No run resume/overwrite or checkpoint selection. Existing native exact-span
transport is reused inside POC, no copied external project code. Third-party dependencies
remain pinned local gliner2/PEFT/Torch. Exceptions are not repaired by mutating knowledge.

Limits: full124-update GLiNER completion and final checkpoint have not been exercised;
first checkpoint uses identical helper and tiny test covers scheduling to124. Runtime
calibration selection, conflict routing, historical/fresh evaluation and timing harness
remain required by the reviewed plan before the full experiment can be qualified or
started under its pretraining sequence. Current scope is training harness only. Review
should challenge failure receipts, frozen preservation, leakage and RNG/loss weighting.

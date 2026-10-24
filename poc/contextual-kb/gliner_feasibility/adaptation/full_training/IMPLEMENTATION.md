# Training harness implementation and limits

The user authorized harness/first-save implementation, TDD, the pilot preflight,
and one additional independent review. Full training/evaluation do not follow.
Review accounting is now fifth of five total authorized instances; the fourth
covered identity compatibility. No reset of the previous budget.

## Implemented

- `checkpoint.py`: strict JSON evidence, parameter hashes, RNG/mode/gradient
  preservation, original in-memory before receipt, first save, fresh reload,
  exact 24-case batches/losses/outputs and all parameter equality. Failure receipt
  blocks checkpoint eligibility. Unsupported serialization and NaNs fail closed.
- `harness.py`: encoder-only inventory, shuffled fixed epochs, actual-example
  accumulation, finite gradients, frozen weights, per-epoch verifier gate and dev
  output capture. Full budgets are fixed to120 cases/eight epochs/64 updates;
  pilot is24 cases/one epoch/two updates. Selection helper applies the predeclared
  complete/error/earliest tie break to complete externally adjudicated dev grades.
- `native.py`: existing pinned POC exporter/preprocessor and GLiNER/PEFT setup,
  native loss presence validation, anchorless public inference, strict metadata
  fingerprints and encoder LoRA. No existing source files edited.
- `inputs.py`: hash-frozen fixed train/dev names and counts, family/ID/question
  separation, explicit annotation/custody receipt references and audit allowlists.
  Receipt references are provenance for human readiness review, not independently
  verified evidence of annotation quality. No evaluation loader exists.
- `worker.py` and `controller.py`: offline run-bound cache/artifacts, strict native
  transport checks before optimization, immutable run outputs, subprocess hard
  timeout and error logs. No retries/resume or hardware change. Direct worker
  execution bypasses parent timeout; supported execution is controller.py only.

## Explicit implementation choice

Logical microbatch2 evaluates two native single-example forwards and means their
losses, then accumulates8 such microbatches (16 examples). Native losses aggregate
across different counts of labels/fields/edges; this avoids treating that as a
uniform example mean. The last8 examples use their actual count. This choice is
recorded as native_forward_batch_size1 in every config, rather than claiming
native vectorized batch2 throughput. It preserves the intended update count and
per-question weighting. Tests compare accumulation with a true example mean.

## Evidence and TDD

Retained missing-module failures: test-output/01-red.txt (verifier/harness),
03-input-red.txt (input/controller), 05-worker-red.txt (native entry point).
The first input-denial test used the full-training folder as repository root,
so a sibling POC path was outside its stated boundary. Corrected the test root
rather than weakening the production policy; failed log06 remains. Supplementary
API/evidence tests extend coverage and are not claimed as separate red cycles.

The real pilot preflight used seed1701, exactly24 exposed pilot cases and two
optimizer updates. Its first save is verified against the original in-memory
model on all24 cases, including named losses, batches, outputs and478 parameter
hashes.144 adapter tensors changed; zero frozen parameters changed. Controller
completed in41.27 seconds (loop/verification26.43 seconds), below30-minute cap.
These are compatibility timings, not accuracy, planner latency or throughput claims.
Original historic missing pre-first-save losses remain missing; this NEW run
captures them correctly. All prior source and evidence remain unchanged.

## Not executed or claimed

No full training, no new annotation, no evaluation reads, no A execution, no
retrieval or DB work. The120/30 dataset, independent annotation/custody checks,
blinded grade collection and complete semantic scorer/evaluation runner remain
future prerequisites. The selection helper does not itself perform grading or
prove that supplied grades are blinded. Annotation/custody receipt IDs must be
verified by the readiness review; mere nonempty strings do not establish custody.
Full-training runtime/performance and eight real native epochs are untested;
synthetic tests exercise those control-flow budgets. No full Trainer.train or
optimizer-resume claim. No automatic promotion or model selection from pilot loss.

## Commands

From this directory using the existing POC environment:

```
PYTHONDONTWRITEBYTECODE=1 ../../env/.venv/bin/python -m unittest test_harness test_inputs test_native test_evidence
```

The retained preflight used controller.py preflight --run-id preflight-01. Output
names are exclusive: do not rerun it over existing evidence. A future full seed
requires the fixed training-manifest.json and data/train.json/data/dev.json plus
human readiness review. No dataset is created here. Do not run train mode during
this implementation/review task.


## Additions during the fifth review

Persist entry Python/NumPy/PyTorch RNG values, module modes and gradient hashes
in state-before.json before capture/save. The original native preflight predates
this extra receipt; the core parity code is unchanged. Focused small-model tests
prove the added persistence and preserved RNG/mode/gradients. No optimization
rerun was needed. Also reject more than32 request records explicitly before native
preprocessing. Retained red logs10/11 and green12 show both additions. All original
preflight artifacts and the initial review freeze remain historical evidence.

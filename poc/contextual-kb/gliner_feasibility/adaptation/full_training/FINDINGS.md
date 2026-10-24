# Training harness and first-save verification findings

Status: requested bounded implementation complete. No full training or evaluation
run. Independent review5/5 accepted the frozen core harness with non-blocking
follow-ups. Subsequent small safeguards and expanded negative tests are locally
verified but not covered by that frozen review verdict. No sixth review started.

## Observed results

| Check | Result |
| --- | --- |
| Latest small-model/guard/retained-evidence suite |18 tests pass, no skips; includes multiple corruption subcases |
| Native pilot preflight |Same24 exposed cases, one pass, two optimizer updates |
| First-save ordering |Original in-memory receipt written and fsynced before saving adapter |
| Fresh-base parity |All24 batches, named losses, decoded outputs and478 parameter hashes identical |
| Trainable/frozen |144 encoder-adapter tensors changed; zero frozen tensors changed |
| Resource limit |Controller41.27 seconds, below1,800-second cap |
| Protected files |208 hashes unchanged, including A/data/prior pilot and identity evidence |

The eight-epoch/64-update full loop is tested with a small real torch model,
not a120-question GLiNER run. The native preflight establishes compatibility,
not frame accuracy, generalization, latency qualification or superiority over A.
Original historical first-save losses remain unavailable; the new preflight
captures its own original first-save evidence correctly.

## First-save gap addressed

The verifier captures the original in-memory model before its first checkpoint
save, reloads a fresh base plus adapter, compares exact batches/losses/outputs and
all parameter tensors, and refuses checkpoint eligibility on failure. Tests cover
parameter, loss, batch and output corruption, missing task losses, nonfinite values,
unsupported serialization, path overwrite and state restoration. Seeds and actual
batch/order evidence are retained; an additional state-before.json now records
entry Python/NumPy/PyTorch RNG values, module modes and gradient hashes.

The native preflight predates that additional state receipt. New state persistence
and explicit early32-record rejection are covered by focused small tests, not a
second native optimization run. Native loss already rejects capacity overflow;
the new guard moves the error before any training updates.

## Review disposition

See test-output/independent-review.md. Accept the P3 RNG-evidence finding; its fix
and early capacity check were implemented with retained red/green tests. The final
review verdict applies to test-output/review-freeze.json, before these additions.
Keep that boundary explicit. Subsequent output-corruption/serialization tests
increase coverage without changing production behavior. No claim that every
future readiness/scorer negative test has been implemented.

Defer qualified dataset/custody validation, immutable blinded grade binding,
semantic scoring and eventual evaluation to the next authorized preparation
scope. The harness accepts annotation/custody receipt references and the selection
helper consumes supplied grades; neither independently proves blinding or custody.
An independently frozen expected model/config/schema manifest is also required
before full execution. Do not treat these helper inputs as automatic readiness.

## Evidence

- Protocol and readiness: PROTOCOL.md, READINESS.md (preserved unchanged).
- Implementation and commands: IMPLEMENTATION.md.
- TDD: test-output/01-red.txt,03-input-red.txt,05-worker-red.txt;
  review follow-ups10-review-fixes-red.txt,11-capacity-red.txt,
  12-review-fixes-green.txt; final13-completion-tests.txt.
- Native preflight: test-output/preflight-01/run.json, controller.json,
  checkpoint-1/before.json, after.json and receipt.json.
- Independent review: test-output/independent-review.md.
- Integrity/final source freeze: test-output/completion.json.

A unchanged and not executed. Evaluation unopened. Data/DB/corpus/compiler/index
untouched. All new implementation/artifacts remain inside this POC. No publication.

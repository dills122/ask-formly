# Author explanation

Review instance 1 of 3. New working-tree scope only: this directory. Repository main,
HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516, substantial unrelated dirty tree.
No staging/commits. Canonical requirements: user-requested bounded GLiNER verifier
compatibility before full training, POC AGENTS/STEERING, and PROTOCOL.md here.

## Intent, plan, and flow

Test whether exact-span GLiNER queries can support a separate binary boundary and
independent six-role verifier. This is compatibility, not trained usefulness.
verifier.py contains offset validation/mapping, two native multi-label schema groups,
public encode/score_explicit_spans scoring, independent sigmoid decisions, and binary
cross entropy. No production caller or resolver invokes it.

check.py verifies the inherited protection manifests, selects the already exposed
training-only eight-row panel with exact membership checks, freezes inputs, tests the
new schema against each frozen extractor, and then creates a fresh disposable LoRA
adapter from the local pretrained checkpoint for each seed. One SGD update per adapter
checks gradients; save/reload checks exact parameters and logits on the panel. It
compares native attachment outputs with explicit scoring, repeated occurrence identity,
unaligned offsets, and synthetic native zero/one/multiple role decisions/boundary veto.
check_all_logits.py supplements the initial runtime with all seven logits, including
below-threshold scores, and explicit native output counts. No optimizer in supplement.

## Verification

The initial test discovery failed to import missing verifier.py (red.txt), so the tests
did not execute in that red run. After implementation, all 11 tests passed (green.txt).
Both runtime seeds completed: eight training questions, 60 spans (37 gold/23 malformed),
all six roles represented. Finite nonzero gradient norms: 3.0474 and 2.7678. Each updated
99 LoRA tensors and zero frozen tensors. First-save parameter/output parity passed.
37,824 inherited protected-file checks passed before and after. All artifacts remain
write-once. The supplemental run is separately frozen and its log/results report outcome.

## Choices and boundaries

Uses native GLiNER span attributes and public explicit scoring; private pinned schema
serialization and native attachment are still dependencies. POC-only reuse is load_model,
weights, seed/write helpers from supervised_trial/train.py; no outside project code.
Third-party code is the existing local environment, without installs/downloads.
Independent sigmoid means decisions do not normalize against one another, NOT that
parameters, contextual queries, or learned representations are independent. Threshold
0.5 is only a mechanics setting. Synthetic logits prove decoder semantics, not real
prediction success. The gold-supplied offset panel is not an extraction evaluation.
Fresh LoRA copies do not reuse or update baseline extractor adapters.

## Limits, costs, and deferrals

No accuracy improvement, calibration, latency, operational integration, production
readiness, or forgetting claim. No full training. Single-update files are disposable
compatibility artifacts. Frozen model tensors are compared through named_parameters;
full state_dict buffer preservation was not asserted by this harness. File manifests
protect original on-disk models/artifacts. Full training would require reviewed labels
for complete/compatible roles, fixed threshold selection, fresh operational tests,
regression transitions and timing. Groups share trainable parameters. Unknown offsets
are reported unsupported, never treated as learned rejection. Review should challenge
native parity, row isolation, real versus synthetic evidence and preservation scope.

## Sources

- https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/13-span_attributes.md
- https://github.com/fastino-ai/GLiNER2/blob/main/gliner2/models/boundary/model.py
- https://github.com/fastino-ai/GLiNER2/blob/main/gliner2/models/boundary/engine.py

Installed gliner2/torch/peft versions are recorded in test-output/environment.json.
Graph tools initially failed (Transport closed); relevant source was read directly.

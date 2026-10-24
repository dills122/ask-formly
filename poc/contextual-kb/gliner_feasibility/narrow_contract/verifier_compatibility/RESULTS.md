# GLiNER verifier compatibility results

The bounded compatibility checks passed for both seeds. Exact-span scoring and
independent binary role decisions are technically usable. This is not evidence that
the verifier improves extraction, rejects malformed spans reliably, or avoids all
forgetting tradeoffs. No full training or operational integration occurred.

## Executed checks

- 11 unit tests: initial missing-module failure retained, then all passed.
- Eight existing training-only questions, 60 supplied spans: 37 valid and 23 malformed.
  Valid role counts: API 16, registration 4, model key 4, value 4, version 5, adapter 4.
  Selection membership checked against the original training material. Evaluation
  cases were not opened.
- Both frozen extractor adapters tested read-only with the experimental verifier schema.
- Two fresh disposable LoRA verifiers, one SGD compatibility update each. Gradient norms
  3.0474 / 2.7678; 99 LoRA tensors changed in each, zero frozen parameter tensors changed.
  Both first-save/reload checks passed exact parameter and panel-logit parity.
- Four adapters × eight questions: explicit-span scoring agrees with native attribute
  scoring for all seven logits, including below-threshold values, within 1e-5 absolute/
  relative tolerance. The maximum observed absolute discrepancy is under 6e-6.
- Repeated identical text at different offsets retains occurrence identity. Offsets
  inside a token are reported unsupported, without snapping or counting rejection.
- Native decoder tests with synthetic logits demonstrate zero, one, and multiple role
  outputs. The experimental acceptance rule requires a boundary pass and exactly one
  supported role. These synthetic checks do not establish learned semantic accuracy.
- 37,824 inherited protected-file checks passed before and after the primary run.
  The final audit after the supplemental run also passed all 37,824 checks, recorded
  separately in test-output/protected-final.json.

## Review and scope

The independent reviewer identified a parity-evidence gap: the first check compared
only emitted probabilities and used zip without asserting output count. The separate
check_all_logits.py adds all-score parity and explicit count checks without rewriting
the initial frozen run. See REVIEW.md for the final independent verdict.

Both baseline extractors, A, v2, previous experiments and the data/DB remain unchanged.
The runtime reports baseline parameter preservation; on-disk manifests cover the
protected files. In-memory non-parameter buffers were not independently compared.
The supplied gold/malformed offsets are diagnostic inputs, not an operational pipeline.

## What remains before full training

Freeze and review the complete verifier target contract and training/development
annotations, including whether malformed spans should have all roles unsupported.
Set development-only threshold selection and operational gates before fresh evaluation.
Require correct conflict repairs without new wrong repairs or lost correct mentions on
both extractor outputs; report abstentions separately and measure added latency.
A single synthetic sigmoid threshold is not calibration. Multiple attribute groups
share parameters, so the new verifier itself can still suffer task interference.

Evidence: test-output/{red.txt,green.txt,runtime.log,all-logit-runtime.log}, per-seed
baseline-schema-check.json, verifier-schema-check.json and step-receipt.json;
all-logit-parity.json; input-freeze.json and supplemental-freeze.json. Disposable
adapters are compatibility artifacts and are not candidates for deployment.

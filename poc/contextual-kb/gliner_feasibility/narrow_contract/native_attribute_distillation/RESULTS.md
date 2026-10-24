# Frozen-teacher distillation — compatibility demonstrated, no full training

Both seeds passed the bounded compatibility check. The existing native boundary scorer can supply a differentiable preservation penalty, and adding that penalty measurably changes student LoRA gradients while leaving the teacher frozen. This establishes a mechanism for a separately designed experiment; it does not establish better extraction, retention on unseen questions, or readiness for adoption. No evaluation/fresh/probe datasets were read and no full training was run.

## What was checked

Each teacher and disposable student started from the same seed's original native-attribute epoch-six candidate. The teacher was entirely frozen, in eval mode, called under no_grad, and excluded from the student optimizer by parameter identity. The student used existing LoRA parameters only. The installed versions are GLiNER2 2.1.0, torch 2.14.1 and PEFT 0.21.2; implementation source hashes are included in each cache.

The adapter uses public boundary `encode()` and `score_explicit_spans()` for differentiable scores. Schema serialization remains the existing private transport. It selects the seven qualified role queries and applies the native pair temperature before the role softmax. Test instrumentation independently captured all seven logits produced by the existing native attribute scorer to verify parity; no library code was edited or new head added.

The deterministic panel contained eight original training questions selected before teacher outputs, with 60 exact labeled occurrences: 16 API references, four registration names, four model keys, four values, five versions, four UI adapters and 23 malformed/no_entity targets. It covers repeated identical strings at distinct offsets, whole and clipped paths, merged spans and broken quotes. Eight additional mid-token coordinates per seed were excluded as unsupported transport, never treated as learned rejection or preservation anchors.

Both teachers happened to classify all 60 panel targets correctly above 0.5 confidence. Therefore all 60 were retained; zero actual teacher errors or low-confidence targets were masked on this panel. Masking wrong/low-confidence teachers was tested with explicit synthetic unit cases, including zero gradient for a masked wrong target. We did not search for more favorable or erroneous teacher examples. Native gold supervision remains independent of this mask.

## Gradient and preservation evidence

| Check | Seed 1701 | Seed 1702 |
| --- | --- | --- |
| Maximum public/native logit difference | 5.72×10⁻⁶ | 4.77×10⁻⁶ |
| Identical student/teacher KL | −1.72×10⁻⁹ | −4.32×10⁻⁹ |
| KL after fixed student perturbation | 1.26560×10⁻⁵ | 2.37196×10⁻⁵ |
| Preservation-gradient norm | 0.008944 | 0.014014 |
| Maximum combined-gradient additivity error | 6.84×10⁻⁷ | 3.25×10⁻⁷ |
| KL after three fixed diagnostic steps | 1.26325×10⁻⁵ | 2.36620×10⁻⁵ |

The tiny negative initial KL values are float32 roundoff around zero. After the fixed 1e-3 Gaussian LoRA perturbation, both KL losses and their gradients were finite and nonzero. On an identical native supervised batch and unchanged perturbed student state, the λ1 gradient equaled the λ0 supervised gradient plus the separately computed KL gradient within the recorded tolerance. The teacher target distributions are detached.

Exactly three fixed SGD steps per seed, lr 1e-4, minimized only cached-anchor KL in dropout-free eval mode. The final loss was slightly below its initial perturbed value for both seeds. The decreases are small; seed 1701 has a slight intermediate increase at float32 precision. This is a limited local-descent check, not evidence that joint supervised/distillation training preserves boundaries or improves generalization. Temperature 1 and λ1 remain compatibility choices, not selected training hyperparameters.

All four student save/reload checks (at steps 1 and 3 for both seeds) reproduced exact logits and state hashes. Teacher full-state hashes, cached probabilities, eval/frozen status and absence of gradients were unchanged after the diagnostic steps. Student non-LoRA state remained unchanged. Cache identity includes teacher hashes, exact targets/query IDs, native schema, tokenizer serialization/special tokens, implementation sources and training-source provenance; cache bytes also remained unchanged.

## Limits, review and next decision

Eight TDD tests pass. The first runtime attempt exposed a list-versus-dict token-mapping assumption before any optimizer update; its log was preserved, a RED→GREEN regression test added, and the adapter corrected. The successful run stayed within the original three-step-per-seed limit. The [protected audit](test-output/protected-after.json) checked 37,548 entries unchanged, including the previous 211-file retention freeze and baseline/A/v2/data/DB chains.

The [two-seed receipts](test-output/compatibility.json), per-seed caches and step parity receipts provide the raw evidence. The independent reviewer inspected the plan/code before the author rationale and completed final evidence and report reconciliation in [REVIEW.md](REVIEW.md), with no actionable findings. The verdict is ready for designing a separately authorized and reviewed controlled training experiment only.

What remains before full training is a separate reviewed design: choose a training-only preservation anchor policy and cache-validation lifecycle, define the matched control and fixed joint-training budget/weights, and freeze fresh evaluation and retention gates. This compatibility check does not authorize that run. The original extractors, agent layer, previous candidates and data/DB remain unchanged.

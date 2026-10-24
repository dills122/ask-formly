# Paired challenge and targeted adaptation

User authorizes fresh failure-focused testing, improvement and independent review.
Only this new directory may change. A, v2, corpus/DB, retrieval, prior experiment
artifacts and old sealed evaluation remain untouched. No service integration.

A fresh reviewer authors 24 clear-input challenge questions without reading
training examples or previous outputs: eight repeated values, eight same-string
role contrasts, eight quoted claims versus configuration literals. Freeze gold
and family metadata before inference. No ambiguous-status qualification claimed.
The implementation author separately prepares 36 new training questions (12 per
failure family) before inspecting challenge predictions. Reserved custom surface
names differ. These are synthetic, related-family tests, not human qualification.

First evaluate BOTH saved supervised_trial epoch16 checkpoints on the challenge,
using unchanged labels, threshold .5, nested decoder, exact-span contract/scorer.
Record all outputs; evaluate old dev24 as exposed regression diagnostics. Do not
select a seed or a best checkpoint. Confirm failures before adaptation. If all
challenge envelopes are exact for both, stop adaptation and report no demonstrated
need. Otherwise run exactly one fixed adaptation experiment, no tuning afterward.

Continue each corresponding saved adapter for eight epochs on original62 + new36
training rows (98), AdamW lr1e-4 wd.01 clip1, serial gradient accumulation8 with
lastchunk2 averaged by2, LoRA architecture unchanged, CPUfloat32 fourthreads.
Seeds1701/1702, reset optimizer, finalepoch8 only,104updates perseed. Validate all
native target spans before optimization. First-save epoch1 and finalepoch8 checks
must compare original outputs/parameter hashes against fresh reload. Require
changed adapter tensors and unchanged frozen weights. Keep training-panel outputs,
losses and full receipts. No development/challenge labels enter gradients.

After adaptation, evaluate both final models on challenge24 and olddev24. Also
score training98 separately as fit evidence. Use raw exact typed-span and accepted
whole-envelope P/R/F1, per-role/family breakdown, exact envelopes, invalid counts,
negative FPs, timings. Raw spans in invalid envelopes do not imply usable outputs.

Improvement gate: BOTH paired seeds gain at least3 percentage points accepted
challenge F1 AND improve exact-envelope count; no challenge family accepted F1
regresses by more than5 points; olddev accepted F1 drops by no more than2 points
and invalid count does not rise. If baseline challenge is near ceiling, the gate
may correctly fail; do not lower it after seeing scores. Qualification separately
requires >=90% precision/recall for every nonempty role and overall, zero invalid
outputs, and no critical whole-path/quoted/opaque boundary misses. Even passing
this synthetic test cannot qualify real traffic or ambiguity detection.

Independent review checks annotations, leakage, native transport, training and
save integrity, scoring, every remaining failure and decision interpretation.
Use at most three review instances for this round, default one fresh reviewer
with followups. Preserve first evidence if any repair is required. No expanding
the contract or adding postprocessing rules to make scores improve.

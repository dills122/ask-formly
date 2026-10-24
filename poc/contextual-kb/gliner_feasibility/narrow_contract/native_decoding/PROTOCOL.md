# Native flat decoding comparison

User authorized testing GLiNER native nonoverlapping decoding on both models,
checking conflict removal versus lost correct mentions, and independent review.
All writes only this directory. A,v2,data/DB, previous evidence and old sealed
evaluation remain unchanged. No training, schema/label change, rule repair,
threshold tuning, dependency upgrade, integration or seed selection.

Models: both latest adapted challenge_adaptation/after-{1701,1702}/epoch-8 adapters,
loaded on the same local pinned base. Each evaluated on challenge24 plus exposed
olddev24. Same six described labels, threshold.5, spans/confidence, CPUfloat32,
fourthreads, deterministic eval. Only overlap_policy differs: nested vs flat.
Both are actual model calls, alternate order per question;192calls total.
Replay nested output must exactly match prior outputs (excluding timing); halt
on mismatch. Model parameter hashes before/after inference must match saved
training receipt. Freeze all inputs/code before any inference.

Source inspection: installed gliner2/inference/overlap.py maps flat to disallow,
a maximum-total-score nonoverlapping set. models/boundary/engine.py applies its
resolver per entity query/label. Do not assume cross-role exclusivity. Official
API source: https://github.com/fastino-ai/GLiNER2 and its overlap_policy docs.
Pinned installed sources, not an upgrade, determine this experiment's behavior.

Use unchanged exact typed-span scorer and whole-envelope acceptance. Report raw
and accepted metrics, per-role/family/exact/invalid, EVERY lost/new correct mention
and removed/new false positive, invalid->valid and valid->invalid transitions,
within-role versus cross-role overlapping pairs, and timings. Do not confuse
suppressing conflicts with semantic correctness or boundary correctness.

Useful-without-loss gate: BOTH seeds lose ZERO previously correct raw mentions
across challenge+olddev, reduce total invalid envelopes, introduce zero invalid
envelopes and do not reduce accepted F1 on either split. Failure is reported even
if aggregate score improves. No policy selection per case. Qualification remains
separate: >=90% P/R every nonempty role and overall, zero invalids and no critical
boundary misses. These are exposed synthetic diagnostics, not fresh evaluation,
real v2 traffic qualification, generalization or final answer accuracy.

Independent fresh reviewer checks code, policy plumbing, unchanged baseline,
all removals/losses, source behavior and decision. At most3review instances for
this round; preserve first failures and explain corrections if any.

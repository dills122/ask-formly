# Role and boundary adaptation results

The contrast examples substantially improved fresh-question extraction in BOTH models.
The fixed replacement gate still fails: one older diagnostic retains a cross-role
conflict in both models, and seed 1701 retains another challenge conflict. These
are useful experimental checkpoints, not promoted replacements or a qualified layer.

## Experiment and evidence

Continued both vocabulary-adaptation epoch 6 adapters for six fixed epochs with
48 new explicit contrasts plus all 146 unchanged replay questions (194 total).
New examples distinguish ordinary nouns from API references, registrations from
keys/values/adapters, Markdown from quoted literals, and complete opaque code values.
This changes learned contextual supervision, not an inference-time allow-list.

An independent author created 40 fresh synthetic questions in 8 families, without
training questions or previous outputs. A separate reviewer checked all 40 fresh
and all 194 training annotations before freeze. Native target compatibility passed
on both starting checkpoints. Both reproduced all 136 prior diagnostic outputs
exactly, including confidence values, before training. Fresh cases became exposed
at baseline; the final result is paired evaluation, not a second unseen holdout.
No questions, labels, threshold, optimizer settings or gates changed after baseline.

Both runs used native flat decoding, threshold 0.5, the same six described roles,
AdamW 1e-4, frozen base weights, serial accumulation 8 (final chunk 2), six epochs and
150 updates. No checkpoint/seed selection or post-result tuning occurred.

## Paired results

F1 scores accepted typed spans after contract validation. Exact means the whole
extraction matched; neither measure establishes final-answer correctness.

| Set | Seed | Exact before → after | Accepted F1 before → after | Invalid before → after |
| --- | --- | --- | --- | --- |
| Fresh 40 | 1701 | 31 → 35 | 87.92% → 97.14% | 1 → 0 |
| Fresh 40 | 1702 | 33 → 36 | 91.00% → 98.10% | 0 → 0 |
| Prior vocabulary 40 | 1701 | 29 → 34 | 86.84% → 95.54% | 2 → 1 |
| Prior vocabulary 40 | 1702 | 31 → 34 | 87.50% → 94.87% | 1 → 1 |
| Prior target 48 | 1701 | 43 → 45 | 96.48% → 98.51% | 1 → 0 |
| Prior target 48 | 1702 | 45 → 46 | 98.51% → 99.00% | 0 → 0 |
| Prior challenge 24 | 1701 | 17 → 18 | 94.02% → 94.42% | 1 → 1 |
| Prior challenge 24 | 1702 | 18 → 19 | 94.47% → 96.64% | 1 → 0 |
| Prior development 24 | Both | 24 → 24 | 100% → 100% | 0 → 0 |

Fresh gold has 104 mentions. Seed 1701 has 102 true positives,4 false positives and 2
misses; seed 1702 has 103 true positives,3 false positives and 1 miss. Fresh accepted
API recall is 97.62% for both (up 2.38 points for 1701, unchanged for 1702). All 19 fresh
registrations,16 values and 6 adapter mentions are exact for both. Seed 1701 has 14/15
correct model keys; seed 1702 has 15/15. Six clear-empty cases remain exact for both.

Fresh quoted name/key/value misses fell 11→1 and 7→0. All 13 compound API mentions
remain exact. All 10 opaque code values across the five evaluation splits are exact
in both raw and accepted output for each model, including non-arrow expressions,
array/object literals and quoted expressions. The reviewer caught an incomplete
posthoc opaque-category predicate; the corrected explicit gold inventory is retained
in postprocess.py and boundary-ledger.json. This reporting correction did not change
training, inference, gold, or the frozen decision gate.

## Remaining failures and regressions

Native flat decoding still permits overlapping labels across roles. Both models
emit the registration 'Material' additionally as a value in va-f03-q04, invalidating
that envelope. Seed 1701 also labels the placeholder-value occurrence 'amber-pivot' as a
registration in roles-04; its separate model-key occurrence remains correct. It also
introduces a false model-key label on 'moss-compass' in the already-incorrect
roles-07 case. All predicted/gold spans and contract errors are retained.

Both still over-extract ordinary `type` in fresh rbf-12 and rbf-14, and miss the
explicit API `key` in rbf-13. Seed 1701 also over-extracts `type` in rbf-25 and absorbs
`: ` into the model key in rbf-30. Seed 1702 introduces `core` as a version in rbf-40;
its fresh version precision is 6/7 (85.71%), below qualification. It also regresses
on va-f05-q05 by including Markdown in `v6**`. Additional lost correct mentions on
already-incorrect cases include API `type` in va-f04-q03 and literal 'cedar-latch'
in roles-02 for 1702. The full ledger includes these losses, not just whole-case
regressions. Seed 1702 challenge quoted misses increase 2→3 despite aggregate gains.

Whole-case repairs/regressions for seed 1701 are fresh 4/0, vocabulary 5/0, target 2/0,
challenge 1/0, development 0/0. For 1702 they are 4/1,4/1,1/0,1/0,0/0 respectively.

Both satisfy fresh improvement criteria. Both fail the frozen diagnostic requirement
of zero invalid outputs because va-f03-q04 remains invalid. Seed 1701 additionally
fails challenge zero-invalid and the comparison against the earlier challenge-flat
baseline:94.42% accepted F1 versus 97.07%, a 2.65-point drop. Seed 1702 challenge 96.64%
versus earlier 97.46% is within tolerance, but does not excuse its vocabulary invalid.
Both also fail separate qualification; do not select the better seed or loosen gates.

The next focused step should investigate cross-role conflict handling and the few
remaining contextual/boundary errors with preserved raw outputs and explicit failure
behavior. This is preferable to another broad vocabulary expansion: most fresh
boundary errors are repaired, while same-span competing roles still invalidate
otherwise useful output. Any conflict-resolution change needs its own bounded
comparison proving it does not discard the correct role. No such decoder change
or further training was performed in this round.

## Verification and limits

Four policy tests pass with retained failing-before/passing-after evidence. Each
model logged 1164 examples and 150 updates, changed 202 adapter tensors and changed
zero frozen tensors. Epoch 1 and 6 saved adapters reload with identical named weights
and flat predictions on the fixed training panel. Library compatibility/deprecation
warnings are retained in logs; successful native target checks, checkpoint identity
and reload parity are concrete compatibility evidence, not suppressed warnings.

Fresh warm inference averaged 188/190 ms after training versus 198/189 ms before.
These sequential CPU measurements are descriptive, not controlled latency benchmarks.
Training fit is 192/194 and 194/194 exact, which is not generalization evidence.

The 352-row paired case ledger covers every evaluation question for both seeds;
boundary and qualification ledgers retain all reported misses and decision details.
The independent review is recorded in REVIEW.md. Protected byte checks cover 36,708
entries with zero changes. A, v2, data/DB, sealed prior evaluation and downstream
layers remain unchanged. All new files are within this experiment directory.
Expanded extraction has not expanded stored knowledge or demonstrated answer accuracy.

Evidence: PROTOCOL.md, REVIEW.md, test-output/final-scores.json,
test-output/case-ledger.json, test-output/boundary-ledger.json,
test-output/qualification.json, test-output/protected-after.json,
test-output/run-freeze.json, and per-seed training/save receipts.

# Expanded vocabulary and role adaptation results

Both continued models recognize substantially more API mentions, but neither
passes the frozen replacement gate. Retain the preceding flat-decoding candidates;
these new checkpoints are experimental artifacts, not promoted replacements.

## Experiment

Added 48 original supervised questions to the previous 98 (146 total): 24 broader
API/formatting cases, 12 role contrasts, and 12 mixed/negative cases. Expanded
coverage uses contextual annotations, not a runtime name list. API spellings were
grounded through read-only pinned Formly 6.3.12 declarations; explicitly hypothetical
references remain valid extraction targets without asserting their API existence.
The annotation coverage count includes formatting variants and hypothetical names;
it is not a complete public-API inventory.

An independent author supplied 40 fresh questions, with a separate gold review
before freezing. Both existing seed checkpoints were evaluated before continuation.
Each then received the fixed six epochs, 114 updates, identical described labels,
threshold 0.5 and native flat decoding. No checkpoint selection or tuning followed
the baseline. Fresh questions became exposed at baseline; this is paired evaluation,
not a second unseen evaluation after training. All cases are synthetic.

## Paired results

F1 below scores accepted typed spans, including contract rejection of invalid outputs.
Exact means the entire extraction matches, not final-answer correctness.

| Set | Seed | Exact before → after | F1 before → after | Invalid before → after |
| --- | --- | --- | --- | --- |
| Fresh 40 | 1701 | 25 → 29 | 80.82% → 86.84% | 0 → 2 |
| Fresh 40 | 1702 | 27 → 31 | 81.88% → 87.50% | 0 → 1 |
| Prior target 48 | 1701 | 38 → 43 | 92.63% → 96.48% | 0 → 1 |
| Prior target 48 | 1702 | 39 → 45 | 93.40% → 98.51% | 0 → 0 |
| Prior challenge 24 | 1701 | 17 → 17 | 97.07% → 94.02% | 0 → 1 |
| Prior challenge 24 | 1702 | 19 → 18 | 97.46% → 94.47% | 0 → 1 |
| Prior development 24 | Both | 24 → 24 | 100% → 100% | 0 → 0 |

Fresh raw API recall rose 65.85% → 90.24% and 70.73% → 92.68%.
API precision changed 100% → 94.87% and 96.67% → 88.37%: coverage gains came
with some over-extraction. All six fresh empty questions remained exact for both.
Fresh version and UI-adapter raw mentions retained perfect precision and recall.
Contract rejection still drops otherwise correct mentions in invalid envelopes:
accepted fresh API recall is 85.37%/92.68%, and accepted adapter recall is 87.5%
for both. Raw mention gains must not obscure these unusable outputs.
Quoted name/key/value boundary misses decreased only 7 → 6 and 7 → 5;
all seven compound-API gold mentions remained exact for both. All four evaluated
opaque expression values remained exact in raw and accepted outputs for both.

Fresh inference averaged approximately 187 ms/question after training for both,
versus 201/185 ms before. These sequential CPU measurements are descriptive,
not a controlled latency benchmark. Training-set exact scores were 144/146 and
143/146; these are fitting diagnostics, not generalization evidence.

## What failed and what follows

Native flat decoding does not enforce exclusivity across the six roles. New failures
include the same registration name also emitted as a value, model keys also labeled
as registrations, and a model-key span absorbing its API context. Ordinary words
such as key, wrappers, defaults or wrapper can be promoted to API references.
Markdown/quote boundaries remain difficult. The full 272-row paired case ledger
records every lost/gained correct mention, false positive, regression and remaining
miss; no aggregate score substitutes for these regressions.

Fresh exact gains comprise 5 repairs/1 regression and 6 repairs/2 regressions.
Target gains comprise 7 repairs/2 regressions and 7 repairs/1 regression.
Challenge changes comprise 1 repair/1 regression and 1 repair/2 regressions.

Both fail the frozen gate because challenge accepted F1 drops more than two points
and invalid counts increase; seed 1701 also increases target invalids. They also
fail separate qualification on role precision/recall, invalids and quoted boundaries.
Do not select a favorable seed, loosen the gate, or treat better recall as readiness.

The evidence supports expanding contextual vocabulary coverage, but the next bounded
experiment should emphasize contrasting roles and boundaries: the same spelling as
an ordinary noun versus API, a registration versus literal value, and quoted or
backticked names/keys in explicit contexts. Use independent fresh examples and the
existing regression gate. Another breadth-only expansion is not justified yet.
No such next experiment was run in this round.

## Verification and scope

Four policy tests passed with retained failing-before/passing-after evidence.
Both starting checkpoints reproduced all 96 diagnostic outputs exactly, including
confidence values. All 146 annotations passed native target-span compatibility.
Each seed has 876 logged training examples, 114 optimizer updates, frozen base
weights, and epoch-1/6 parameter and flat-output save/reload equivalence checks.
The independent review is recorded in REVIEW.md; all review findings rejecting
promotion are accepted. No post-result changes to training or scoring were made.

The protected audit checked 36,627 entries with zero changes. A, agent v2, data/DB,
old sealed evaluation, prior artifacts and all downstream layers remain unchanged.
All new artifacts are confined to this directory. No outside-project code was
imported or wired in. Expanded extraction does not add knowledge facts, retrieval
coverage, app investigation, or evidence about final answers.

Evidence: PROTOCOL.md, REVIEW.md, test-output/final-scores.json,
test-output/case-ledger.json, test-output/run-freeze.json,
test-output/protected-after.json, and per-seed training/save receipts.

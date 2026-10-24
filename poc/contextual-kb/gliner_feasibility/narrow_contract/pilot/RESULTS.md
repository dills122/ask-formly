# Narrow-contract annotation pilot and schema comparison

The annotation pilot is consistent enough to study this contract, but neither
zero-shot extraction schema passes it. Descriptions improve raw span recall while
increasing conflicts between roles. More training was not run.

## Pilot and annotation evidence

24 development questions, four per planned family: 18 exact saved v2 question
strings plus six explicitly marked developer diagnostics. The latter cover
same-spelling roles, empty string/null, escaping, correction and genuine ambiguity.
These are not 24 new v2 outputs and are not held-out evaluation.
Selection was frozen before annotation; gold and schemas before inference.

Two independent agents annotated all 24 without predictions or each other's labels.
Initial agreement: 24/24 complete envelopes and all 90 typed spans. No adjudication
changes were needed. Parent inspected all lists before inference. D05 and D06
were independently marked needs_review. Both annotators noted that the general
contract leaves the extent of an unterminated-literal issue unspecified; both used
opening quote through question end for D06, accepted for this pilot.
Agent agreement is not expert-human accuracy.

## Real model test

48 local calls: 24 × bare/described six-role schema, same pinned base model,
threshold 0.5, nested overlap, CPU float32/four threads, fixed seed.
No old adapter, fine-tuning, threshold sweep, postprocessing repair or dependency
upgrade. All calls completed without inference exceptions.

Raw metrics count exact typed source spans, even within structurally conflicting
outputs. Accepted metrics require the whole output to satisfy the non-overlap
contract; invalid outputs are rejected, receiving zero accepted recall.
Both views are reported so rejection does not conceal raw false positives.

| Measure | Bare | Described |
|---|---:|---:|
| Raw correct / predicted / expected occurrences | 23 / 59 / 90 | 43 / 109 / 90 |
| Raw precision | 39.0% | 39.4% |
| Raw recall | 25.6% | 47.8% |
| Raw F1 | 30.9% | 43.2% |
| Structurally invalid outputs | 6/24 | 16/24 |
| Accepted correct occurrences | 12/90 | 9/90 |
| Accepted precision / recall / F1 | 42.9% / 13.3% / 20.3% | 45.0% / 10.0% / 16.4% |
| Fully exact output envelopes | 2/24 | 1/24 |

Descriptions gain 20 correct occurrences and lose none, but introduce 38 new false
positives while removing eight. Every invalid actual output contains overlapping
or duplicate-role spans. The configured nested decoder permits this; descriptions
do not enforce the new mutual-exclusion rule. The experiment deliberately retained
that setting to isolate schema effects, rather than silently repair outputs.

The saved-v2-only raw F1 is 35.4% bare versus 47.3% described. Developer diagnostics
are 16.7% versus 31.4%. These scores are NOT directly comparable to prior five-label
experiments: the taxonomy, selected questions and quote rules have changed.

## Per-role raw recall and precision

| Role | Expected | Bare exact | Described exact | Described precision |
|---|---:|---:|---:|---:|
| API reference | 37 | 2 | 13 | 43.3% |
| Registration name | 8 | 0 | 0 | 0.0% |
| Model key | 10 | 0 | 0 | 0.0% |
| Value | 13 | 8 | 8 | 27.6% |
| Version | 11 | 11 | 11 | 100% |
| UI adapter | 11 | 2 | 11 | 84.6% |

Zero exact quoted names/keys does not mean the model found none of their content.
A separate post-run boundary diagnostic, not a relaxed score, checks for the same
role and exact inner substring with only quote delimiters missing:
- Model keys: 10/10 bare, 9/10 described.
- Registration names: 2/8 in either schema.
- Quoted values: 1/3 bare, 2/3 described.
None of the 21 quoted names/keys/values had the required full quoted boundary.
Thus model keys have a strong boundary-convention problem; registration names
also have substantial role/recognition failure. This distinction matters before
deciding what to train.

Compound API paths: only 1/8 exact bare, 3/8 described.
R04/focused/1 returns expressions fragments instead of complete bracket paths.
H01/focused/1 finds the interiors of postal-choice and zip, but described output
labels zip both model_key and value, violating mutual exclusivity.
D03 finds the interior of the escaped string as a value, but also labels Sam as
a registration name and choice inside that string as a model key.
Version boundary behavior improves in this schema: all 11 version occurrences
are exact and no extra version spans are emitted in described output.

Deduplicating (kind,raw) within each original parent leaves 72 gold atoms:
bare recovers 19 with 26 false positives; described recovers 34 with 46 false
positives. Repeated context is not the entire reason for the raw gain.

## Empty inputs and ambiguity

Of two clear no-mention questions, bare emits false positives for one; described
does so for both. Exact envelopes with gold mentions: 1/21 in either schema.
The remaining exact bare envelope is one clear empty case.

Neither schema handles the two gold needs_review cases correctly. Bare emits
structurally valid but unsupported labels and says ok. Described emits conflicting
labels and is rejected as extraction_error. Neither is an ambiguity-aware answer.
A flat entity-only schema has no mechanism to emit the semantic needs_review
status or issue-region judgment. It cannot qualify that part of the contract
merely by doing better entity tagging; the capability gap must remain explicit.

## Timing

Total inference plus envelope validation: 1.61 seconds bare and 4.16 seconds
described, about 67 ms and 174 ms per question. Model load is recorded separately
in raw rows. One CPU pass with alternating order, not service-latency qualification
or repeatability evidence.

## Gate and next decision

Both fail the proposed >=90% precision and recall per role/overall, structural
validity and critical path/value fidelity gates. The contract can be annotated
consistently on these cases; the model does not yet implement it reliably.
No training or integration is justified as complete by these results.

The next bounded design decision should separate:
1. Source boundaries: quoted model-key interiors were usually recognized.
   Decide whether model span selection plus a generic, tested source-boundary
   serializer is acceptable, or whether full quoted spans must be learned.
   Do not silently change this pilot's gold or call an adjusted score a pass.
2. Role conflicts and path completeness: these need a separately tested decoder
   or targeted six-role supervision. The old broad-frame adapter is not evidence
   for solving them.
3. Ambiguity responsibility: retain an explicit unresolved capability rather than
   training flat entities and claiming needs_review is solved.

Before a training proposal, choose these responsibilities and freeze any contract
revision. The data/DB and v2/A remain outside that decision. This is a focused
next-step recommendation, not permission to implement changes or begin training.

## Implementation and independent review

TDD produced 15 initial validator/scorer tests. Independent review found a
malformed-input bug: a non-object row could cause the frozen adapter's exception
handler to raise. It did not occur in the 48 actual object predictions.

hardened.py is the reviewed adapter entry point for future use; it guards malformed
rows without modifying the inference-frozen implementation. Three added tests
exercise the guard, recall penalties, and exact adapter/scoring parity over all
48 saved predictions. All 18 tests pass. Historical contract.py/run.py/score.py
remain frozen reproduction code; do not adopt them as the hardened runtime API.
The experiment has no production integration.

See REVIEW.md for independent findings and verification. Inference/scoring hashes,
both raw annotations, adjudication, raw predictions and before/after test logs are
retained. test-output/integrity.json confirms 36,222 protected prior files and 155
additional frozen agent/experiment artifacts unchanged. No sealed evaluation
content was read and no data/DB, A, v2, retrieval or answer component was edited.

## Reproduction

From repository root:
python3 -B -m unittest discover -s poc/contextual-kb/gliner_feasibility/narrow_contract/pilot -p 'test_*.py'

run.py and score.py use exclusive output creation to preserve first-run evidence.
Do not overwrite stored predictions or grades to rerun. Future comparisons need a
separate directory/protocol. Full per-family, per-parent, per-origin and per-case
metrics are in test-output/scores.json; raw gained/lost spans in differences.json.

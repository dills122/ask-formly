# Bounded repair replay — decision: reject adoption

Completed implementation, tests, four-stage replay and independent counterexample
execution. The hybrid improves recoverable spans, but fails the declared no-harm,
completeness and counterexample gates. Do not integrate this repair pipeline, train
against its repaired outputs as gold, or expand it into a general prose parser.
No new training or model inference was run.

## What ran

The same 48 saved GLiNER predictions (24 questions × bare/described labels) were
replayed through four variants: hardened baseline, quote repairs, quotes plus
API paths, and all repairs including local roles/ownership. This produces 192
replay outputs without regenerating questions or model predictions. Original
90-span gold is unchanged. Inputs remain 18 saved v2 questions and six marked
developer diagnostics, not independent held-out model evidence.

An independent author prepared 12 safe/unsafe counterexamples without reading
implementation or pilot outputs. Their bytes and implementation were frozen before
first execution. No extractor edits followed scored replay or counterexample
inspection. The counterexamples test normalization of hand-authored candidate
spans, not GLiNER model generalization. Raw outputs and first failures are retained.

17 development tests pass. Independent review reproduced all 192 outputs/core
scores and confirmed source hashes. Counterexamples pass 11/12. These results
are consistent: passing unit tests did not establish that the implementation was
complete or safe.

## Accepted-output comparison

Only status ok outputs contribute accepted spans. Needs_review retains useful
mentions diagnostically but is not counted as a complete usable result. A rejected
or review output receives zero accepted recall against its full gold. This is
intentionally stricter than showing the F1 of surviving partial mentions.

| Source / stage | Accepted precision | Accepted recall | Accepted F1 | Exact envelopes | ok / review / error |
|---|---:|---:|---:|---:|---|
| Bare baseline | 42.9% | 13.3% | 20.3% | 2/24 | 18 / 0 / 6 |
| Bare quotes | 66.7% | 20.0% | 30.8% | 2/24 | 17 / 7 / 0 |
| Bare quotes + paths | 66.7% | 20.0% | 30.8% | 2/24 | 17 / 7 / 0 |
| Bare full | 73.3% | 24.4% | 36.7% | 2/24 | 18 / 6 / 0 |
| Described baseline | 45.0% | 10.0% | 16.4% | 1/24 | 8 / 0 / 16 |
| Described quotes | 55.0% | 12.2% | 20.0% | 2/24 | 8 / 16 / 0 |
| Described quotes + paths | 72.7% | 17.8% | 28.6% | 4/24 | 9 / 15 / 0 |
| Described full | 88.9% | 35.6% | 50.8% | 4/24 | 13 / 11 / 0 |

Exact envelopes include correct needs_review cases; they are not all successful
extraction envelopes. The described full result has three exact ok envelopes and
one exact needs_review envelope. Structural validity after repairs is achieved
partly by omitting disputed regions; it does not establish completeness.

## What improved

For described/full, retained mentions including review outputs have 52 correct,
4 false-positive and 38 missing occurrences: 92.9% precision, 57.8% recall, 71.2%
F1. This is a PARTIAL diagnostic, not its accepted F1 or an answer-quality score.
The original described raw predictions had 43 correct and 66 false positives.
Only 32 correct occurrences survive in whole-output ok envelopes after repair.

- Whole compound API paths: 3/8 original raw → 7/8 retained after full repairs.
- Quoted names/keys/values: 0/21 original raw → 18/21 retained.
- Model keys: 10/10 correct retained, with one additional wrong model-key span.
- Registration names: 6/8 correct retained, no false positives.
- APIs overall: only 13/37 correct retained. Path repairs cannot recover all
  APIs the model never proposed.
- Values: only 5/13 correct retained; conflict rejection withholds sound values
  along with competing wrong labels.

Relative to original described raw spans, full repair gains 23 correct occurrences
and loses 14 already-correct occurrences. It introduces no new wrong delivered
span in those 24 cases, but violates the declared no-loss criterion. Bare/full
introduces one new wrong delivered/accepted span and loses seven original correct
occurrences. These are gate failures even though aggregate scores improve.

After per-parent deduplication, described/full retains 43/72 gold atoms with four
false positives; bare/full retains 28/72 with eight false positives. Gains are not
solely repeated context. Both clear-empty described cases still contain incorrect
mentions; the repair does not remove every semantic false positive.

Concrete examples:
- R04/focused/1 now returns both exact expressions[...] paths and no fragments.
- H01/focused/1 now preserves 'postal-choice' and 'zip' with correct roles, but
  still lacks the key API property because the model did not propose it.
- H13/focused/1 repairs key '0' versus defaultValue 0 and key 'false' versus
  defaultValue false; later unbound prose occurrences remain role conflicts.
- D05 described output correctly becomes needs_review with no guessed role.
  Bare output still has an unconflicted, wrong model-key prediction; it remains
  wrong. This is not a general ambiguity classifier.
- D06 described output detects the missing quote but also withholds props.label
  due to a competing model-key label; its full gold envelope is still not met.

## Why adoption is rejected

1. Independent CX-PA-S fails on a valid path at sentence end:
   Inspect widgetMap['pane'].height.
   The parser treats the final punctuation dot as an unfinished member access,
   discards the API root and leaves a wrong value fragment. This is a concrete
   implementation bug, not evidence that the reference expectation is wrong.
2. Independent review found an additional root-boundary bug: a prediction for
   widgetMap inside otherwidgetMap.height can be expanded into widgetMap.height.
   It lacks an alphanumeric left-boundary check and can manufacture a partial API.
3. Review found audit-log aliasing: stored prediction_ids share a mutable list
   with merged nodes, so an earlier event can incorrectly acquire a later ID.
   Before/after spans and recomputed final scores are available, but event-ID
   provenance is not fully reliable. Do not claim every repair lineage is sound.
4. Described/full still has 11/24 review outputs and withholds 14 correct raw
   occurrences; the >=90% per-role/overall recall gate is far from met.

The no-tuning commitment is honored: failures and code remain unchanged after
independent execution. No patches were slipped into the recorded candidate.
These bugs are documented rejection grounds, not deferred issues in a promoted
runtime. See REVIEW.md for severity, reproductions and independent findings.

## Clear next decision

Stop adding source rules to this GLiNER pipeline. Keep v2 as the unchanged working
question-decomposition layer. Retain the gold, validator, raw failures and replay
as evidence; retain repair code only as a rejected experiment.

If continuing with GLiNER, the next useful step is one narrowly scoped supervised
feasibility trial for the six mention roles and exact source boundaries, with a
separate frozen development split and a fixed budget. It should target missing
API/property mentions, whole paths, quoted names/keys, and mutually exclusive
roles. Compare against the original described raw model using identical new gold;
do not train on repaired predictions or resurrect broad request-frame training.
Score raw model output and contract validity separately, and stop that direction
if it does not materially improve both. Training is a testable next hypothesis,
not a promised fix or something executed in this task.

Semantic needs_review detection remains a separate capability gap. A six-role
entity training result must not claim to solve it. No full-training run, integration
or readiness claim follows from this replay. A has not been replaced.

## Cost, artifacts and boundaries

Full repair/validation of 24 saved outputs measured about 0.96 ms bare and 1.11 ms
on described predictions in one local Python pass. These are tiny replay-only
measurements, excluding inference; no robust service-latency claim is made.

- PROTOCOL.md: frozen grammar and execution limits.
- repairs.py: rejected normalization candidate, no gold/model/DB access.
- replay.py: baseline equality checks, scoring, per-group metrics and first outputs.
- test-output/implementation-freeze.json: implementation/input hashes.
- test-output/replay.json: all envelopes, actions, timing and issues.
- test-output/scores.json: full role/group/parent metrics and gained/lost spans.
- counterexamples.json / counterexamples-freeze.json: independently authored tests.
- test-output/counterexample-results.json: preserved 11 passes and one failure.
- REVIEW.md: independent code and evidence review.

Integrity check: 36,222 protected prior files plus 191 frozen agent/prior-experiment
artifacts unchanged. v2, A, data/DB, pilot gold, prior outputs, retrieval, evidence
and answer layers remain unchanged. No old sealed evaluation content was read.
Everything added stays under this POC.

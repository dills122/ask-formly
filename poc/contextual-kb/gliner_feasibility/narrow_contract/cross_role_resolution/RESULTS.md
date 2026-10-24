# Cross-role resolution results

The new contextual-classification candidate does not repair the remaining conflicts.
Reject it as a replacement. Both frozen models retain all prior gains because the
candidate abstained on every conflict and changed zero outputs. This is a useful
negative result, not a successful fix or qualified question layer.

## Actual comparison

Ran 432 flat extractions: both fixed role/boundary epoch-6 models on 40 fresh
independently authored questions and 176 prior diagnostic questions each. The
352 prior predictions reproduced exactly, including scores. No training, label,
threshold, question, prompt or gate changed after fresh inference. Four native
classification calls per eligible conflict retained both label orders, native
single-label outputs and complete softmax score vectors. Three eligible model/case
conflicts produced 12 classifier calls. One partial-overlap conflict abstained
without a classifier call. All original outputs and all classifier evidence persist.

| Set | Model 1701 exact | Model 1702 exact | Candidate change |
| --- | --- | --- | --- |
| Fresh 40 | 37/40 | 40/40 | None |
| Prior role/boundary 40 | 35/40 | 36/40 | None |
| Prior vocabulary 40 | 34/40 | 34/40 | None |
| Prior target 48 | 45/48 | 46/48 | None |
| Prior challenge 24 | 18/24 | 19/24 | None |
| Prior development 24 | 24/24 | 24/24 | None |

Fresh accepted F1 is 96.97% and 100%; fresh invalid envelopes 1 and 0. These scores
characterize these synthetic extraction questions, not final answers or universal
reliability. Previously learned performance remains unchanged in every split and
role; zero correct raw mentions were lost. Both frozen replacement gates fail
because correct conflict resolutions equal zero. Full qualification also remains
failed across the diagnostic suite; opaque boundary review is separately explicit. Fresh opaque-literal envelopes
are correct on 4/5 and 5/5; the nested-key conflict invalidates one model-1701 case.

## Why the proposed fix fails

The installed library supports document classification and described labels.
We tested using that classifier to decide the role of an explicitly marked
occurrence in the whole question. Native API compatibility and one synthetic
registration smoke succeeded, but the semantic targeting assumption did not.

- For the quoted registration 'Material', model 1701 chooses ui_adapter instead
  (probabilities .457 forward and .643 reversed). Model 1702 chooses value with
  .396/.426. Both abstain under the fixed .5/eligible-role gate.
- For the placeholder occurrence 'amber-pivot', model 1701 chooses API with .926
  in the forward order, not an existing registration/value candidate. It abstains.
- A fresh object literal has an overlapping model-key fragment in model 1701.
  Different boundaries deliberately remain unresolved; selecting a role would not
  establish which complete span to keep.

The simple maximum extraction-confidence control is unsafe: it repairs two older
model-1701 conflicts, but model 1702 keeps the incorrect value role and discards
the correct 'Material' registration. Making an envelope nonoverlapping does not
make its semantics correct. It is not promoted as a fallback.

Fresh model-1701 errors are a quoted default value misclassified as registration,
a trailing colon included in defaultValue's API span, and the nested key inside
an otherwise correct opaque object literal. Model 1702 is exact on these 40 but
retains older errors. No favorable seed selection is justified.

## Training diagnosis and next direction

Read-only inspection confirms the existing training transport already emits all
six entity labels including absent-role empty targets. prepare() checks all six
native queries and exact positive offsets. Library boundary losses include binary
negative supervision per query/candidate, with configured hard-negative mining;
the model is not simply missing negative-role labels. Those independent binary
entity decisions nevertheless do not impose a mutually exclusive cross-role
choice. The previous fine-tuning examples supervise entity spans only; they do not
supervise the marked-occurrence document classification task tested here.

A next bounded design should test occurrence-aligned role supervision or native
span attributes, with a compatibility check that the target is the exact supplied
span and that competing roles are genuinely supervised. It should not assume a
longer prompt or lower threshold fixes targeting. No such new training, native
attribute wiring or loss change was attempted in this experiment. Existing base,
adapters, A, v2 and data/DB remain fixed.

Source basis: supervised_trial/data.py export and train.py prepare; installed
gliner2 2.1.0 models/boundary/losses.py candidate_pair_loss, models/boundary/model.py
_classification_loss, inference/runtime.py _decode_classification_probabilities;
pinned model config hard_negatives_per_positive=20 and minimum_hard_negatives=16.
Official classification API: https://github.com/fastino-ai/GLiNER2#2-text-classification.
These source facts explain architectural limits; they do not prove a single causal
training defect or that a proposed next design will work.

## Verification

Independent precomparison review identified hardening/reporting problems, fixed
with retained red/green evidence. Fourteen tests passed, including exact occurrence,
partial overlap, malformed spans/confidences, arbitrary classifier errors, marker
collision, label-order agreement, nonconflict preservation, and gate rejection.
Both checkpoint parameter hashes match before/after; run-freeze hashes match.
Warm extraction totals were 41.50s and 40.96s across 216 questions each. Additional
classification cost was 1.786s for model 1701's two eligible conflicts and .880s for
model 1702's one. These CPU observations sum extraction and classification calls only; they exclude
Python validation/resolution overhead and model loading and are not controlled
latency benchmarks. Unresolved classifier decisions remain in all denominators.

Evidence: PROTOCOL.md, REVIEW.md, test-output/scores.json, ledger.json, decision.json,
qualification.json, latency.json, run-freeze.json, per-model raw/control/contextual
outputs, all classification calls, integrity receipts, and TDD logs. Independent
final review and the parent protected-file audit are recorded separately.

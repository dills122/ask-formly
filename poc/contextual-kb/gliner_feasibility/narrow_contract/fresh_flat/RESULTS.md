# Fresh realistic Formly question evaluation

The trained models with native flat decoding retain useful performance on fresh
questions:38/48 and39/48 complete exact envelopes, with zero invalid outputs.
They still fail strict qualification. The main remaining weaknesses are API
recall and role discrimination, rather than overlapping spans.

## Independence and execution

An independent author produced48 focused Formly library questions without reading
prior training/test examples, predictions, failure analyses or implementations.
A separate reviewer inspected all48 annotations before inference. Eight families
have six questions each; eight questions correctly contain no extractable mentions.
The dataset contains100goldmentions:52API,9registration names,8keys,13values,
10version tokens and8adapter mentions. Three values are complete opaque expressions.

Review caught intermediate annotation-boundary issues and two wording ambiguities;
all were resolved, documented and validated before freeze or model inference.
No exact question duplicates occur against146exposed train/dev/challenge questions.
There is expected conceptual/library-API overlap. These are synthetic focused
questions, not sampled production traffic, actual newly generated v2 outputs,
or deliberately ambiguous inputs. Several final-family questions concern source
scope rather than implementation. Do not claim representative general accuracy.

Both fixed latest epoch8 adapters ran flat decoding at threshold.5 with unchanged
six-role descriptions, CPUfloat32 and fourthreads.96actual model calls; both raw
prediction files saved before scoring. No retraining, tuning, rule repairs,
seedselection or gold changes after inference. Saved checkpoint parameter hashes
matched exactly and were unchanged afterward. Only question text and shared label
descriptions entered inference. Prior sealed evaluation was not opened.

## Fresh results

| Metric | Seed1701 | Seed1702 |
|---|---:|---:|
| Completely correct envelopes | 38/48 (79.2%) | 39/48 (81.3%) |
| Exact typed-span precision | 97.8% | 94.8% |
| Exact typed-span recall | 88.0% | 92.0% |
| Exact typed-span F1 | 92.6% | 93.4% |
| Invalid/runtime-error outputs | 0 | 0 |
| Correct / extra / missed mentions | 88 / 2 / 12 | 92 / 5 / 8 |
| Correct empty envelopes | 8/8 | 6/8 |

Raw and accepted metrics are identical because there are no invalid envelopes.
This validates the observed structural improvement on another set; native flat
is still per-label and cannot universally guarantee global mutual exclusion.

Both models extract all8modelkeys,13values and10version tokens exactly without
false positives in those roles. This includes the array-form key and all three
complete opaque expressions. Both find all8actual adapter mentions, but emit
extra adapter labels elsewhere. Role recall is weaker for API references
(80.8%/86.5%) and registration names(77.8%/88.9%). Adapter precision is88.9%/72.7%.

| Family: completely correct out of6 | Seed1701 | Seed1702 |
|---|---:|---:|
| Custom types/wrappers | 3 | 3 |
| Validation/errors | 4 | 4 |
| Expressions/visibility | 5 | 4 |
| Defaults/model/reset | 6 | 6 |
| Repeat/nesting/layout | 4 | 6 |
| Lifecycle/options | 4 | 5 |
| Adapter/version scope | 6 | 6 |
| Conceptual/claim distinctions | 6 | 5 |

The models produce identical envelopes on41/48questions;35of those are fully
correct and six are jointly wrong.42questions have at least one correct model,
but this oracle count does not implement or qualify an ensemble. Different
checkpoint agreement is not repeat-run determinism, and neither seed is selected.

## Every remaining failure

Both models:

- 003: assign wrapper name 'billing-frame' to ui_adapter instead of registration_name.
- 005: omit the configuration API wrappers.
- 010: omit validation.messages.
- 012: omit validators and asyncValidators.
- 017: omit expressions and expressionProperties.
- 033: include Markdown backticks in the API span for model, instead of returning
  just the identifier. This is an exact-boundary error, not a missing concept.

Seed1701 additionally omits registration 'postal-lookup' in002, FieldArrayType in027,
FormGroup in029 and hooks.onInit in032.

Seed1702 additionally labels Angular as ui_adapter in the empty cases001and013,
and labels the ordinary type noun in046as an API property. These are false
positives, not structural conflicts.

All exact missing/extra spans and full questions are preserved in
`test-output/failures.json`. CompoundAPI recovery is17/19 and18/19; quoted
name/key/value recovery is17/19 and18/19. Complete opaque expressions016/018/036
are exact for both. The current run retains original gold and all failures.

## Decision and verification

Fresh evidence supports continuing with narrow supervision plus native flat.
It does not qualify either model: per-role90%P/R thresholds fail, seed1701 overall
recall is below90%, and critical compound/name coverage misses remain. Zero
invalids and high aggregate F1 do not make the remaining20% incomplete or wrong
outputs disappear. These extraction scores do not establish answer accuracy.

A next bounded improvement should target API names versus ordinary nouns,
registration names versus adapter names, and formatting boundaries. Keep these
48questions as exposed diagnostics; use another frozen independent set for any
subsequent generalization decision. Do not weaken or silently relabel this test.
No further training or integration occurred in this round.

Five harness checks passed after recorded RED tests. Independent review covers
pre-inference gold, code, complete scoring, failures and frozen inputs; see
REVIEW.md. Measured total extraction time was9.58/9.26seconds for48questions
(about200/193ms each), excluding load time. One sequential local CPU pass per
model is not a service latency or repeat-determinism benchmark.

All files remain under fresh_flat. Protected hashes are retained in
`test-output/protected-after.json`; A,v2,data/DB and all earlier evidence remain
unchanged. Questions and full annotated expectations are in questions.json;
model outputs, timings, freeze receipts and scores remain in test-output.

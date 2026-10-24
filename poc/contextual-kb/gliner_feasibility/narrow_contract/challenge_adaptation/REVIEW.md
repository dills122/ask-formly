# Independent review — instance 1 of at most 3

## Preliminary verdict before adaptation

No remaining blocker to the fixed continuation training after the manifest-reader
repair. This is permission to conduct the bounded experiment, not approval of
model quality or integration. Final evidence review remains pending. This review
was written before reading RESULTS.md or any model predictions/scores. The
reviewer independently authored and froze challenge gold before inspecting the
training annotations or implementation; that earlier exposure boundary is in
CHALLENGE-NOTES.md. The later review necessarily reads both splits.

## Finding and repair

**Required, resolved before inference:** the initial run.py applied its flat
path-to-digest checker to the structured challenge-freeze-v1 manifest. It would
open a nonexistent schema_version filename. The corrected challenge_hashes helper
explicitly extracts files[*].sha256 after checking the schema version. run.py
now checks those repository-relative paths. The current correction and added
unit test were inspected. The implementation author reports preserving the
initial failed baseline.log and using baseline-retry.log; runtime chronology will
be checked with final receipts. No frozen challenge annotations were changed.

## Evidence reviewed

Read PROTOCOL.md, test_experiment.py, experiment.py, run.py,
training_annotations.py, all 36 train-new.json annotations, and all 98 combined
training annotations; compared reused supervised_trial/train.py and data.py and
the unchanged pilot contract/scorer. Checks made independently:

- All 36 compiled rows equal annotation(question_id, authored_markup), and the
  combined training set is exactly original62 followed by new36.
- Split validation accepts training98 and challenge24; there is no duplicate
  question or ID between these. No reserved challenge registration surface
  occurs in training98. Training and challenge freeze hashes match.
- Manual semantic review found no clear mislabeled or missing mention in new36.
  Claim-only quoted spans are excluded; quoted configuration strings, repeated
  values, and negative occurrences are preserved. Original62 retain their
  original annotations; no correction to frozen legacy data was made.
- Both epoch16 adapters are loaded by corresponding seed, without best-seed
  selection. Continuation makes only LoRA tensors trainable and resets AdamW.
  Eight epochs over 98 rows in chunks of eight yield 13 updates per epoch and
  104 per seed. The final two-row chunk divides by two, not eight. Clip1,
  learning rate 1e-4, weight decay .01, CPU float32 and four threads match plan.
- Native training preparation checks every role's mapped target offsets against
  explicit gold and requires all six queries. Only training batches enter the
  gradient loop. Preparing challenge/dev targets before baseline is a transport
  check, not optimization. Inference receives only original question strings.
- First and final save checks compare predictions and every named parameter
  hash with a fresh load, restoring RNG afterward. End receipts reject changed
  frozen parameters, unchanged adapters, or a wrong update count. No threshold,
  label-description or overlap-decoder tuning occurs here.
- Scoring retains exact typed occurrence spans and rejects invalid envelopes
  separately from raw diagnostics. Prediction coverage is checked. Paired
  improvement requires both seeds, the predeclared F1 and exact-count gains,
  each family guard, and dev regression/invalid guards. Regression diagnostics
  are exposed old dev data, not an independent new holdout.
- Seven local standard-library unit tests pass with python3 -B -m unittest
  discover -s poc/contextual-kb/gliner_feasibility/narrow_contract/challenge_adaptation
  -p 'test_*.py'. These do not themselves validate neural training or inference.

## Final-review obligations and limits

Qualification is a separate judgment from paired_decision's improvement Boolean.
The current harness does not automate all qualification criteria. Final reporting
must inspect every per-role precision/recall, invalid count and critical boundary
miss, and explicitly count false positives on quoted behavioral claims. Overall
F1 or training fit alone is insufficient. Inspect actual checkpoint receipts,
104-update loss logs, unchanged-file hashes, all residual challenge/dev failures,
and both seed decisions before concluding. Preserve original failed attempts.

This synthetic, related-family challenge does not qualify ambiguity detection,
application discovery, downstream retrieval, answer correctness, or production
traffic. Familiar short literals/APIs and deliberately similar behavioral themes
are expected shared vocabulary; distinct custom surfaces and exact-question
separation do not make the entire distribution independent. The design measures
transfer within three named failure families. No further model tuning is approved
by this review. The reviewer has run no inference or training and edited only
this review during this phase.

## Baseline evidence review during fixed adaptation

Independently recomputed the complete baseline challenge and old-dev report
objects from saved prediction JSON using the unchanged scorer; all four objects
exactly equal baseline-scores.json, including per-case diagnostics. Read every
nonexact challenge case. No current-run data/config changes recommended.

| Seed | Exact / 24 | Invalid | Raw TP / FP / FN | Accepted TP / FP / FN | Raw F1 | Accepted F1 |
| --- | --- | --- | --- | --- | --- | --- |
| 1701 | 9 | 6 | 113 / 23 / 6 | 75 / 7 / 44 | .886275 | .746269 |
| 1702 | 5 | 11 | 112 / 27 / 7 | 46 / 6 / 73 | .868217 | .538012 |

All invalid cases are overlap/duplicate/order contract rejections, not runtime
errors. Source inspection shows overlapping spans or conflicting roles, not a
mere serialization ordering problem (adapt sorts the raw output). Seed1701
invalid cases: repeat-02, repeat-05, repeat-08, roles-02, roles-04, roles-06.
Seed1702 invalid cases: repeat-01, repeat-02, repeat-04, repeat-05, repeat-07,
repeat-08, roles-02, roles-04, roles-05, roles-06, roles-07. Invalid envelopes
are empty accepted outputs; 38/66 otherwise-correct raw mentions respectively
are lost this way. High raw recall therefore overstates usable extraction.

Both models omit hide in repeat-03 and omit defaultValue and key in roles-03.
Both confuse the props.label value in roles-02 with a key/registration, and the
props.label value in roles-07 with a registration. Further misses: seed1701
mislabels the type registration in roles-04 as value; seed1702 mislabels the
first Pending value in repeat-07 and the placeholder value in roles-04 as
registrations. These account for all six/seven raw false negatives.

False positives in invalid outputs often extend an API across its adjacent
literal or connecting word, or extend a version across the Formly prefix.
Examples include props.label followed by its empty-string value, props.rows 3,
Formly 6.3.12, and a value span extended through “and key”. roles-06 also shows
same-string cross-role duplicates. The many correct raw spans do not cancel
these source-boundary or role exclusivity violations.

Each model produces six false positives on excluded quoted behavioral claims,
and all six remain accepted because they do not overlap valid mentions. Seed1701
extracts claims-02,03,05,06,07,08 as value. Seed1702 extracts claims-02,03,05,07,08
as value and claims-04 as api_reference. Some omit quote delimiters; all are
wrong regardless of boundary because the occurrence is a claim, not supplied
configuration content. Both extract every actual gold mention in the claims
family (19 TP, 0 FN), including the four positive literal strings. Their error
is over-extraction of claims, not failure to extract the supplied strings.

Baseline old-dev recomputation is exact to the saved report for both seeds.
This replay remains exposed regression evidence and is not counted as fresh
qualification. The baseline clearly establishes non-perfect challenge behavior
for both models; the protocol's adaptation-need condition is met.

## Seed1701 integrity check before paired results

The 564 starting parameter hashes exactly match seed1701's original epoch16
final hashes. Of 230 trainable tensors, 202 changed; all 334 frozen tensors
remain unchanged. The receipt's changed-tensor list agrees with the independent
hash comparison. The protocol requires adapter change, not every trainable
tensor changing, so the 28 unchanged trainable tensors do not violate it.

The loss log has exactly 784 rows: each of eight epochs contains each of the
98 training IDs once. Every epoch has twelve eight-row update groups and one
two-row group, sequentially totaling 104 updates. Mean losses by epoch are
20.3620, 19.7588, 19.4522, 19.0590, 19.1221, 19.2471, 19.0357, 18.8537;
not monotonically decreasing, with no claim that loss predicts qualification.
Receipt time is 281.701 seconds and includes intermediate/final save verification
inside the training block; it is not pure optimization or end-to-end latency.

Both epoch1 and epoch8 save receipts report identical parameter hashes and
predictions. Independently compared all eight before/after output pairs for
each save and verified all three saved adapter-file hashes against each receipt.
The live model hashes themselves were recorded by the harness; this review
checks those records rather than loading or running a model again.

All 127 run-freeze entries, 72 prior final-freeze entries, four training-freeze
entries, and five structured challenge-freeze entries match current bytes.
The paired outcome verdict remains pending seed1702 and final scoring.

## Final independent verdict

The bounded experiment is valid evidence of gains within these synthetic
failure families, but **fails the predeclared paired improvement gate and does
not qualify either model for use**. Do not select seed1702 afterward or describe
this as a readiness pass. No further training, inference, implementation or gold
changes were made by this reviewer. Final review used the raw saved artifacts,
not an implementation-author results narrative.

Independently recomputed all ten report objects (two baseline splits and three
final splits for each seed) and the paired decision; every object matches
final-scores.json. A separate direct set tally from native entities and gold
confirmed all four challenge raw TP/FP/FN totals without the shared scorer.
The original baseline.log confirms the structured-manifest failure occurred at
the guard before model loading/inference; the retry and adaptation logs retain
completion and score summaries. The initial failure has not been concealed.

| Seed | Challenge exact | Challenge invalid | Accepted F1 | Raw F1 | Old-dev exact | Old-dev invalid |
| --- | --- | --- | --- | --- | --- | --- |
| 1701 | 9 → 14 / 24 | 6 → 4 | .746269 → .875576 | .886275 → .943089 | 23 → 23 / 24 | 0 → 1 |
| 1702 | 5 → 17 / 24 | 11 → 3 | .538012 → .883721 | .868217 → .954357 | 21 → 24 / 24 | 1 → 0 |

Both gain more than three accepted-F1 points and improve exact count. Neither
has a family F1 decline greater than five points. Old-dev accepted F1 improves
by .008400 and .050000 respectively. Nevertheless, seed1701's old-dev invalid
count rises from zero to one, violating the explicit guard. That alone makes
the paired gate false; unchanged old-dev exact count does not override it.

Seed1701 fixes six challenge envelopes (repeat-05, repeat-08, roles-02, roles-04,
claims-02, claims-06) but newly breaks roles-05. Seed1702 fixes twelve
(repeat-01, repeat-04, repeat-05, repeat-07, repeat-08, roles-02, roles-05,
claims-02, claims-03, claims-04, claims-05, claims-08), with no previously exact
challenge case becoming nonexact. These are genuine paired improvements, not
only changes in aggregate precision/recall or in acceptance treatment.

### Every residual challenge failure

| Case | Seed1701 | Seed1702 |
| --- | --- | --- |
| repeat-02 | Extra version spans include library prefix/punctuation and overlap correct version | Extra version includes library prefix and overlaps correct version |
| repeat-03 | Missing API hide | Missing API hide |
| roles-03 | Missing API key | Missing API key |
| roles-04 | Exact | Placeholder API expands through quoted value, supplied value missing, ordinary word text falsely labeled value; invalid |
| roles-05 | Extra value expands through and key, overlapping valid spans; newly invalid | Exact |
| roles-06 | Extra version spans include prefix/sentence text or truncate version; invalid | Extra version spans include prefix/sentence text; invalid |
| roles-07 | Missing quoted props.label value | Missing quoted props.label value |
| claims-03 | Extra quoted claim value plus overlapping prefixed version; invalid | Exact |
| claims-05 | Extra behavioral claim labeled value | Exact |
| claims-07 | Extra behavioral claim labeled value | Extra behavioral claim labeled value |
| claims-08 | Extra behavioral claim labeled value | Exact |

All other challenge cases are exact. Raw quoted-claim false positives decline
from six to four for seed1701 and six to one for seed1702. Accepted quoted-claim
FPs are three/one: seed1701's fourth is discarded because claims-03 is invalid,
so that particular accepted reduction is not correct claim discrimination.
All 19 gold mentions in the claims family remain present in raw outputs.

The sole final old-dev error is **V10 in seed1701**, not V07: an additional
value span omits the opening quote of an escaped quoted string and overlaps
the correct value span. Its two correct mentions are discarded from the
accepted envelope. Seed1701 fixes V20 but newly breaks V10. Seed1702 fixes V07,
V20 and V24 and has no final old-dev failures.

Both final challenge accepted recalls are 95/119 = 79.83%, below the 90% gate.
Accepted per-role recall for seed1701 is API78%, registration75%, key75%,
value83.78%, version66.67%, adapter100%; seed1702 is API78%, registration75%,
key75%, value83.78%, version77.78%, adapter85.71%. All accepted precisions are
at least90%, but this does not offset recall failures, invalid envelopes, or
quoted-boundary/claim mistakes. Even raw precision/recall success would not
qualify unusable envelopes. Raw compound-path recall being24/24 for both does
not mean boundary problems disappeared: extra overlapping path/value spans
and quoted-string misses remain. Opaque-expression behavior has only exposed
regression coverage here, not a new targeted challenge family.

Training fit is reported separately: seed1701 reaches96/98 exact, with two
invalids; seed1702 reaches97/98 exact and no invalids. All319 gold training
mentions occur in each raw output set. Seed1701 adds three overlapping value
spans around the literal in H14/focused/1 and a combined version span in T27.
Seed1702 falsely tags the ordinary noun type in T15 as an API. These are fit
diagnostics, not fresh generalization evidence or ignored perfect-training claims.

### Final integrity confirmation

Seed1702's564 initial hashes exactly match its corresponding original epoch16
final hashes. Its202 changed tensors are all within230 trainable tensors; all
334 frozen tensors are unchanged. Its784 loss rows contain98 unique IDs in
each of8 epochs, twelve chunks of8 and a final chunk of2, with104 sequential
updates. Receipt time is306.848 seconds, with the same save-verification timing
scope as seed1701. Rechecked both seeds' epoch1/epoch8 before/after predictions,
parameter-equality receipts, and saved adapter file hashes. All pass.

Run, prior-final, training and challenge freeze manifests still match every
recorded file after both runs. No checkpoint selection, postprocessing repair,
threshold adjustment or additional adaptation round was used. The final result
supports retaining this experiment as bounded diagnostic evidence and keeping
the models unqualified; it does not support integration or a claim of universal
Formly/question-layer reliability.

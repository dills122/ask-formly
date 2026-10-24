# Bounded foundation/GLiNER integration results

The foundation remained usable through this integration: all three arms preserved every core question, condition ledger and full-text search request on all 174 inputs. Both frozen extractors ran successfully, but neither met the predeclared annotation precision gate. Keep the accepted foundation as the default question layer; keep GLiNER optional and experimental rather than a dependency for producing searches. Final independent review is recorded separately.

## What ran

The same 174foundation objects were supplied to three arms: foundation alone; foundation plus epoch-6 seed 1701; foundation plus epoch-6 seed 1702. Inputs comprise all 162 previous qualification outputs and12 new first-generation development requests. These produce295 actual derived questions; empty abstentions never invoke extraction. Both models processed all 295 questions once, sequentially, using the unchanged described six-role labels, threshold0.5, native flat decoding, CPU float32 and four threads. No verifier, training, model selection, changed threshold, response repair or retry.

The native package is gliner2 2.1.0 with local GLiNER2.5 base-v1 and retained role_boundary_adaptation adapters. Both loaded models' parameter hashes matched the frozen training receipts before inference and stayed identical afterward. Raw native outputs, plans, per-call timings and console warnings remain saved. Library load warnings did not replace identity checks or native execution evidence.

## Core plan safety

| Arm | Records delivered | Core plans and search requests preserved | Extraction failures |
| --- | --- | --- | --- |
| Foundation alone |174/174|174/174|Not applicable|
| Foundation +1701|174/174|174/174|0/295|
| Foundation +1702|174/174|174/174|0/295|

Advisory hints cannot alter queries or become filters. Error-injection tests demonstrate continued query availability for exceptions, malformed envelopes, invalid offsets, unknown roles and overlaps. Invalid core objects remain errors. Validly anchored but semantically wrong hints are deliberately not claimed to be repaired.

Preflight independently assessed all 12fresh request/output pairs without finding a material semantic failure. This small one-run batch extends integration development evidence; it is not another repeatability qualification.

## Annotation quality

The preselected and reviewed annotation panel contains44 rows:42 actual questions and2 no-question controls, with87 gold mentions. It uses the first question from each even-numbered fresh qualification case at run 1, plus every new derived question. These metrics do not cover all 295 questions.

| Metric | Seed 1701 | Seed 1702 |
| --- | --- | --- |
| Correct exact typed spans |77|77|
| False positives |9|8|
| Missed gold spans |10|10|
| Precision |89.53%|90.59%|
| Recall |88.51%|88.51%|
| F1 |89.02%|89.53%|
| Entire annotation set exact |34/44|35/44|
| Gold-nonempty questions with a correct hint |32/34|32/34|
| Gold-empty rows with false positives |0|0|
| Fixed advisory value gate |Fail|Fail|

Both exceed the80% recall and50% nonempty-coverage thresholds but fall short of95% precision. Raw and accepted scores are identical on this annotation panel. Foundation-alone has no hints by design: its annotation precision is undefined and annotation recall 0; that does not invalidate its174 usable full-text plans.

Saved-panel precision/recall are89.58%/89.58% for both models. Fresh-panel precision is89.47%/91.89%, recall87.18% for both. Per-role metrics and every individual miss/extra are preserved in test-output/scores.json and annotation-comparisons.md. Registration names(10), model keys(3) and adapter mentions(9) were all exact on this small panel; those small counts do not establish general reliability. API references and values account for most errors.

## Failure patterns and ambiguity

Both models merge or split some boundaries incorrectly: version range 6.2 <7 becomes a value; model.delivery === 'courier' becomes separate API/value fragments; defaultValue:0 becomes one API span; a quoted hypothetical API includes external quote delimiters. They also miss configuration-key references. Additional extras include generic type or model-value prose tagged as APIs.

Two I05 mentions depend on a prospectively declared role convention: model.needsReview is treated as a supplied model-data expression/value, whereas paths rooted at named Formly configuration APIs remain API references. Both models choose api_reference for I05. This was adjudicated before predictions, remains genuinely convention-sensitive, and is not presented as an undisputed universal error. Numeric-only compared-version boundaries and quoted-narrative interpretation were likewise documented before inference; see ANNOTATION-ADJUDICATION.md. Gold and thresholds were not tuned afterward.

Across the full safety panel,1701 retained555/555raw mentions and1702 retained523/529. The six rejected 1702 mentions are overlapping API/value spans in the second P26 question across three runs. They are outside the frozen annotation subset, so no all-panel precision or zero-correct-loss claim is made. Inspection also exposes clipped props. spans in those longer questions. The authoritative full question survives regardless; optional hints are still imperfect.

## Cost

| Measured extraction overhead | Seed 1701 | Seed 1702 |
| --- | --- | --- |
| Median per derived question |187.6ms|189.4ms|
| p95 per derived question |201.4ms|203.4ms|
| Median per original request |367.3ms|370.6ms|
| p95 per original request |571.5ms|573.2ms|
| Total 295 question calls |55.68s|56.11s|
| Model load/schema setup |3.77s|3.65s|

One-time imports took 8.44s. Model-load timing excludes parameter-hash verification. These are single-pass local diagnostics, not a latency SLA. They exclude foundation generation, retrieval, answer assembly and serving transport. Original-request summaries include empty abstentions as zero extraction work. Projection timing is separately recorded, and must not be mistaken for question-generation time.

## Review and preservation

Preflight 1 was not_ready: it found annotation ambiguities and missing-extraction accounting that could credit an absent attempt as an empty success. Initial artifacts are preserved. Gold was adjudicated prospectively; scorer coverage was fixed with failing regression tests, including a full assessment fixture. Independent review 2 verified the corrections and 22 passing tests before inference. Design/source freeze predates fresh generation; the final 54-file run freeze predates extraction. No scoring criterion changed during inference.

Parent audits before and after inference match 43 protected manifests/39,289 overlapping entries, including existing candidates, both baselines, foundation, and data/DB. Sealed evaluation stayed unopened except byte-hash preservation. All code and results belong to this new POC directory. No serving integration, retrieval execution, staging, commit or publication occurred.

## Decision and limits

The experiment demonstrates a safe optional-annotation boundary and a usable foundation-alone search-plan path. It does not demonstrate that annotations improve retrieval: search text is deliberately identical across arms, and retrieval was not run. Both extractors fail the fixed annotation value gate; do not require either downstream or silently use its hints as filters. Preserve both configurations without selecting a seed from this panel.

The useful next step is a separately authorized read-only retrieval test of foundation-generated full-text plans, with GLiNER remaining a shadow annotation stream if retained. This experiment does not authorize or implement that downstream work. Synthetic development cases, exposed diagnostics, correlated repetitions and contract-sensitive labels limit generalization. There is no sealed-evaluation, final-answer-accuracy or production-readiness claim.

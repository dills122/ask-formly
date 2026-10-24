# Span role feasibility results

Neither resolver passes the paired replacement gate. Both preserve every correct raw baseline mention and every nonconflicting output, but both make a malformed fresh output look valid in seed 1702. Keep both extractors and baseline extraction behavior unchanged.

The positive finding is that a trained occurrence classifier can distinguish roles substantially better than zero-shot attributes in this bounded setup. spaCy correctly types 97/101 gold spans on the 40 fresh questions (96.0%); native attributes type 44/101 and 53/101 correctly, counting unavailable/uncertain outputs as unsuccessful. This is not an equal-training comparison: spaCy trained 194 Formly questions, while native attributes received no attribute training. It does not show GLiNER cannot learn the task.

## Actual runs and preservation

- Frozen role_boundary_adaptation epoch 6 checkpoints 1701/1702, flat decoding, threshold 0.5. No GLiNER training.
- Each model: 40 fresh independently authored questions plus 216 exposed diagnostic questions. 512 baseline calls and 512 separate native attribute calls; zero native runtime errors. All 432 historical baseline outputs reproduced exactly.
- One separate spaCy 3.8.16 blank-English spancat_singlelabel classifier, fixed seed 1701, 30 epochs, 750 updates; 194 existing training questions, 488 positive mentions and 2755 uncovered single-token negatives. All positives align strictly to the standard tokenizer. Training fit 488/488 positive, 2755/2755 negative; exact save/reload scores on training panel. Same classifier tested against both extractors' candidates; no evaluation-based selection.
- Both extractors' full named parameter hashes match before/after and prior receipts. Frozen 367 input hashes match. Protected artifact audit: 36,899 checks, zero changes. A, v2, data/DB and previous artifacts unchanged.
- Seven pure resolver tests and two spaCy alignment/negative-choice tests pass, with initial failure evidence retained.

## Conflict-only end-to-end extraction scores

Fresh 40 questions contain 101 gold mentions. Model 1701 has no fresh cross-role conflict; model 1702 has one. Consequently fresh gains cannot be inferred from unchanged exact counts.

| Model / split | Baseline exact | Native exact | spaCy exact | Accepted F1 baseline / native / spaCy | Invalid baseline / native / spaCy |
|---|---:|---:|---:|---|---|
|1701 fresh 40|32|32|32|92.75 /92.75 /92.75%|0/0/0|
|1702 fresh 40|32|32|32|94.06 /93.14 /93.14%|1/0/0|
|1701 vocab 40|34|35|35|95.54 /96.86 /96.86%|1/0/0|
|1702 vocab 40|34|34|35|94.87 /94.87 /96.20%|1/1/0|

All other diagnostic splits preserve their complete baseline outputs:

| Split |1701 exact|1702 exact|
|---|---:|---:|
|cross 40|37|40|
|boundary 40|35|36|
|target 48|45|46|
|challenge 24|18|19|
|olddev24|24|24|

Native correctly repairs one conflict in 1701 and none in 1702. spaCy correctly repairs one in each model. Both arms pass the 1701 preservation/improvement gate and fail 1702; no promotion or seed selection. Full qualification also fails: remaining misses, boundary errors, and invalid outputs persist.

## What was fixed and what failed

Both arms correctly choose registration_name for the quoted custom name 'Material' in va-f03-q04 for 1701; spaCy also does so for 1702. The later unquoted Material UI adapter remains unchanged. Native 1702 abstains on the competing role.

New srf-026 asks whether `key: 'entry[2]'` is a model path while `props.label: 'entry[2]'` is text. The gold separates API names and their values. Model 1702 instead extracts the entire `props.label: 'entry[2]'` fragment as both API and value, and another oversized model-key fragment. Both resolvers remove one conflicting role but keep the wrong boundary: native chooses API, spaCy chooses value. Neither is a correct entity at that boundary. The row becomes structurally valid but semantically wrong. Its false spans enter accepted scoring, so accepted precision/F1 falls even though no correct raw mention was removed. This is a genuine safety-of-acceptance regression, not a recovered answer.

Partial overlaps still abstain; neither arm attempts boundary repair. No selected threshold, schema, model, or training data changed after fresh results.

## Occurrence typing audit, separate from resolution

The audit supplies the union of gold and baseline proposal offsets solely to measure typing coverage. Resolver mutation remains restricted to conflicting baseline proposals; gold offsets never add or change extractor candidates.

| Arm/model | Fresh gold correct /101 | Prior diagnostic gold correct /565 | Fresh non-gold proposals rejected / total |
|---|---:|---:|---:|
|native 1701|44|227|0/10 (5 abstain)|
|native 1702|53|278|0/8 (1 abstain)|
|spaCy paired 1701|97|526|4/10|
|spaCy paired 1702|97|526|3/8|

Native schema retains exact gold boundaries for 96/101 and 95/101 fresh mentions; the 44/53 correct totals include confidence abstentions as failures. spaCy receives all 101 gold boundaries in this diagnostic audit. Same spaCy gold-span predictions across both pairings are expected: it is the same classifier and the same supplied gold spans, not two independent replications. Non-gold proposal sets differ by extractor. Perfect training fit alongside remaining false-span acceptance means generalization needs more representative negative spans; it is not an argument to simply train longer.

Native attributes depend on retained entities under the extended schema. Native span drift occurred in 3/256 questions for 1701 (2 dropped, 2 added offsets) and 4/256 for 1702 (3 dropped, 2 added). None of these new/deleted spans was applied to the baseline. Native output is top-only, with an uncalibrated score; strict>0.5 avoids a two-way 0.5 tie but does not supply a calibrated correctness guarantee. spaCy had zero strict-alignment failures on evaluation proposals.

Additional per-question audit inference median: native~216 ms; spaCy~1.7–1.9 ms. Native time is a full entity-plus-attribute re-extraction; spaCy time is typing supplied baseline-plus-gold diagnostic spans. These are not equivalent end-to-end replacement latency. Both exclude load time and are not a production throughput benchmark.

## Decision and next supported step

Preserve the extractors. The narrower next experiment should teach the occurrence classifier to reject an invalid span before allowing it to select a role: multi-token merged API/value fragments, truncated API paths, quote-delimiter mistakes, and embedded keys inside object literals, generated only from training cases. The no_entity class currently sees simple uncovered token negatives and does not adequately represent these proposal errors. Test rejection separately from role accuracy and require no invalid-to-valid-wrong transitions. Native span-attribute training would be a separate fairer comparison, not assumed supported by these zero-shot results. No such follow-up is implemented in this experiment.

## Evidence and review

Protocol and source links: PROTOCOL.md. Runtime artifacts in test-output/: scores.json, decision.json, ledger.json (all 1024 arm/case rows), typing.json, audit.json, summary.json, qualification.json, spacy-receipt.json, per-seed first outputs and parameter hashes. REVIEW.md contains independent preflight and final review.

Compatibility/reporting defects are retained: initial spaCy config serialization failed before optimization (compatibility-attempt-1), then used dict(config); reviewer required malformed-native fail-closed handling and count guards before freeze. Initial protected-audit resolver mistakenly compared two artifact-relative README entries to the repository README; original script/false-failure receipt remain frozen. Added reporting-only protect_corrected.py resolves explicit poc paths from repository root and other relative paths from manifest root. Corrected receipt protected-after-corrected.json reports zero changes; audit-path-regression.txt documents the collision check. No experiment rerun or inference/scoring edits followed these results.

### Fresh qualification detail

Precision/recall below are accepted mentions; all values are percentages. Passing an overall F1 does not satisfy the per-role/boundary gates.

|Model/arm|Role failures below 90%|Boundary diagnostics|
|---|---|---|
|1701/native|api_reference precision 86.0%; ui_adapter precision 88.9%; ui_adapter recall 88.9%|compound_api: 1 missed, quoted_name_key_value: 3 missed|
|1701/spacy|api_reference precision 86.0%; ui_adapter precision 88.9%; ui_adapter recall 88.9%|compound_api: 1 missed, quoted_name_key_value: 3 missed|
|1702/native|api_reference precision 87.5%; version precision 80.0%; ui_adapter recall 88.9%|compound_api: 1 missed, quoted_name_key_value: 3 missed|
|1702/spacy|api_reference precision 89.4%; version precision 80.0%; ui_adapter recall 88.9%|compound_api: 1 missed, quoted_name_key_value: 3 missed|

Independent review inspected the five fresh opaque-expression cases (srf-031–035): complete expression/maximal-API boundaries were preserved by both extractors and both arms. This does not establish universal correctness; numeric and quoted/compound failures still reject qualification.

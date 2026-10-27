# Diagnosis of the 36 library-focused misses

The accepted knowledge is the main remaining limit, but the earlier grading also produced false negatives. Independent review: **Ready**, with no actionable findings; see REVIEW.md. All findings are limited to the unchanged 176-fact candidate and these known requests.

| Whole-request finding | Count | Cases |
| --- | ---: | --- |
| Already fully supportable from old packets; earlier grading/caller omission |4|FQ-050, FQ-131, FQ-143, FQ-208|
| Newly supportable with caller-derived plans and bounded recovery |4|FQ-031, FQ-043, FQ-078, FQ-082|
| Still has at least one missing accepted-knowledge requirement |28|See CASE-DIAGNOSES.md|
| Additional complete answers found only in the full fact inventory |0|None|

This does not mean retrieval is universally optimal. It means the full accepted-fact inventory did not supply a complete answer for any of the remaining 28 cases after the tested flow. Some individual parts were already supported; missing parts may require limitation facts rather than implementation recipes. Do not assume each case needs one new fact or that Formly supports every premise.

## What changed in our understanding

- **Real planning benefit:** FQ-043 now receives hide/reset retention evidence. The other newly sufficient cases concern expression targets/restrictions, row-count validation plus explicit caller guards, and runtime-link availability after population.
- **Grading corrections:** FQ-050 already had scoped shared-key precautions in old citation text. FQ-131 already had enough evidence for a bounded draft/keyword answer; demanding exhaustive compliance exceeded that interpretation. FQ-143's old packet included the Material integration excerpt. FQ-208 already had control/message/disabled/render observations.
- **Conservative new grading:** the frozen new answers marked FQ-031 and FQ-082 partial. The audit found they demanded extra exhaustiveness or earliest internal assignment proof. Those historical scores are not rewritten; the audit correction is separate.
- **Knowledge gaps:** representative gaps include field.get versus formControl.get, field id/name meaning, global/local hide-reset precedence, state-preserving row reorder, full lifecycle ordering, FieldArrayTypeConfig details, wrapper nesting, CSS class targets, duplicate registration resolution and partial preset overrides.

Across 68 frozen requirements: 24 were already supported, five gained sufficient delivered support, and 39 remain unsupported by accepted knowledge. Requirement causes overlap within cases; do not add overlapping case counts as if they were separate questions.

## Recorded test versus later evidence audit

New caller plans contained 79 focused questions for the same 36 original requests. No repairs were needed. Three repeats produced identical arguments and results. The scored stage recorded 2/36 full initially and 6/36 full after recovery, with 26 partial and four unsupported. Only after those answers were frozen did the complete inventory audit identify eight cases supported by evidence actually delivered in the new run. Four of those were also supportable before replanning.

This is targeted diagnosis, not a rerun of all 102 library questions or all 260 bank questions. Do not present an adjusted broad accuracy number or count repeated packets as independent semantic samples.

## Budget failure retained

There were 453 scored MCP calls, including three identical FQ-131 first-fetch rejections. Sixteen requested IDs exceeded the separate evidence-byte budget. The smaller second fetch succeeded within the original two-attempt limit. Failed calls supplied no evidence. A separately tested and pinned diagnostic auditor preserves the failures, counts attempts and rejects unknown errors; the original frozen evaluator is unchanged. See BUDGET-ERROR.md.

The later oracle inventory used 176 singleton fetches, all complete and successful. These calls were never credited to retrieval scores. Total diagnostic calls:629, of which three were rejected as described. The full inventory contains accepted facts and their delivered quotes/excerpts; this audit does not claim all unadmitted upstream source has been exhausted.

## Verification and next step

All 38 focused tests passed, as did full local maintenance and preservation checks. Both runtime implementations/manifests, models, installed 124-fact DB and isolated 176-fact candidate remain unchanged. Evaluation stayed sealed. No admission, promotion, commit or publishing occurred.

Next, correct the grading guidance to allow evidence-backed composition and bounded answers while preserving real conditions. Then scope a small source-backed batch for public API/configuration contracts (lookup, CSS targets, wrapper order, registration and preset precedence). Keep Angular/application integration and unsupported-feature boundaries explicit rather than expanding the MCP into application investigation. No new batch was implemented here.

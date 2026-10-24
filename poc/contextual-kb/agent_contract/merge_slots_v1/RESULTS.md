# Eight-slot combination: results and decision

**Reject the protected-six candidate. Keep foundation-only as the working setup.** Reserving six original slots did not stop useful facts from being lost. It preserved irrelevant high-ranked facts as well as relevant ones, while useful facts in the final two slots remained exposed.

## Experiment

36 fresh development requests in three batches produced 46 first foundation questions and 46 supplemental queries. One supplement was identical to its original, leaving 45 additional queries. We acquired the 91 distinct-per-question query calls once and shared the saved rankings across all three policies:

1. Foundation: existing interleaving of original query results, eight slots.
2. Current fusion: existing original/supplement RRF and interleaving, eight slots.
3. Protected six: preserve the first six foundation IDs; fill remaining slots in current-fusion order, then original fallback.

Six was fixed before generation and results. No parameter sweep, exception, post-result tuning, query repair, training or rerun occurred. Existing engines, candidates, models and DB were unchanged. The user authorized this separate combination-policy experiment; it is not wired into serving.

Independent prospective review labeled all 36 requests against the 46-fact catalog: 30 directly supported, six unsupported. Generation used fresh native contexts and the unchanged contracts; this is not a pinned hosted-model benchmark or unseen-topic evaluation.

## Retrieval results

Recall and precision are macroaverages over the 30 supported requests, ten per batch. Recall measures all labeled relevant facts found. Complete required groups measures minimum aspect coverage with predeclared alternatives. Neither measures final answers.

| Metric at eight results | Foundation | Current fusion | Protected six |
|---|---:|---:|---:|
| Relevant-fact recall |92.07%|92.55%|92.07%|
| Precision |23.75%|24.17%|23.75%|
| nDCG |83.76%|86.24%|83.76%|
| MRR |85.00%|89.44%|85.00%|
| Mean required-group coverage |95.00%|95.00%|95.00%|
| Complete required groups |28/30|28/30|28/30|
| Any relevant hit |30/30|30/30|30/30|
| Relevant baseline facts lost |—|1|2|
| Relevant facts gained |—|2|2|
| Logical query calls |46|91|91|

All six unsupported requests returned eight candidates in every arm: 48 exposures per arm, not measured false answers. No abstention or answerer was tested.

| Batch recall at eight | Foundation | Current fusion | Protected six |
|---|---:|---:|---:|
|1|92.50%|92.50%|92.50%|
|2|85.71%|87.14%|85.71%|
|3|98.00%|98.00%|98.00%|

**No arm meets the 89.25% floor consistently.** All pooled means exceed 90%, but batch 2 does not. Protection does not improve any batch over the foundation.

At four results, recall is 84.54%, 85.37% and 84.54%, respectively; all arms complete 26/30 required-group sets. Prefix protection deliberately keeps the foundation's first four results, so it cannot improve that ranking when at least four originals exist. Full per-batch/top-four metrics are in scores.json.

## Exact losses and gains

Only M01 and M13 change their relevant fact sets relative to the foundation. The protected candidate changes packet contents or order on 21 requests, so equal aggregate scores do not mean identical packets.

**M01 — use an already registered type.** Both augmented policies lose `props-and-registration/type-name-registration`, originally in slot eight, and gain `custom-component-use/registered-component-selected-by-type`. An acceptable substitute remains, so required-group coverage and recall stay unchanged. The strict fact-level safety gate correctly reports the lost useful fact rather than hiding the exchange.

**M13 — register an input-derived type with defaults, then use it.** Current fusion adds `custom-component-use/registered-component-selected-by-type` and retains the original useful facts. Protected six gains that same fact but drops `custom-types-and-wrappers/component-needs-registration`, originally in slot eight. The protected prefix retains unrelated model-rebuild and key-shape results; the fill then admits default eligibility before reaching the useful registration fact. Compared with current fusion, protected six loses this relevant fact and rescues none.

Neither augmented policy loses a complete required-group set in this panel. That weaker aggregate/group measure would miss the regressions above. Protected six preserves its first-six invariant in all 36 requests, yet fails the stronger zero-lost-relevant-facts gate.

Two requested groups remain missing in every arm: M14's reverse-merged-defaults fact and M19's wrapper-decorates-not-control fact. Exact missing groups for every request/arm at four and eight are retained in scores.json.

## Gates and input quality

- **Prefix invariant:** passes 36/36.
- **Observed fact-preservation safety:** fails, with two relevant baseline facts lost.
- **Utility:** fails; protected six gains no pooled recall over foundation. Current fusion gains 0.4762 percentage points, below the predeclared 0.5-point utility criterion, and independently fails fact-preservation safety.
- **Consistent 90% target with 89.25% floor:** fails batch 2 for every arm.
- **Runtime/delivery:** no missing records, structural failures or runtime errors.
- **Meaning preservation:** 35/36 foundation plans pass. M36's standalone database-migration follow-up loses the source's server-side SQL-schema scope. Supplements pass 36/36 relative to their saved plans, so M36 inherits the foundation omission. This unsupported request remains in the experiment; it was not repaired or excluded.

The merger safety and consistency failures stand independently of M36. Query semantics and conditional merger performance are separate findings. No candidate is qualified for promotion.

## Cost, uncertainty and verification

Shared query acquisition took 0.602 seconds, including the frozen contextual candidate's existing fusion overhead. Computing all three packets from the acquired lists took 0.000439 seconds total. Shared index setup took 0.787 seconds. These are local timings; native generation cost is unmeasured. We did not run three independent query services and cannot claim per-arm end-to-end latency. Foundation logically needs 46 calls/5,510 characters; each augmented policy needs 91 calls/11,513 characters.

Descriptive request-bootstrap intervals for pooled recall are 85.14–97.67% for foundation/protected and 85.88–97.67% for current fusion. Small, related synthetic batches cannot establish population accuracy to within ±0.75 points. One request can move a ten-request batch mean by as much as ten points. These are fresh wordings and conditions over the same bounded catalog, not unseen Formly topics.

22 TDD tests and independent preflight's 2,500 randomized policy checks passed. The two preflight reporting gaps—missing groups and paired group changes versus current fusion—were fixed and retested before retrieval. 128 code/input/artifact/dependency-metadata hashes were frozen before execution. All 36 shared acquisition traces and 108 packets were saved once, and their manifest was verified before scoring. Read-only SQLite and the unchanged DB hash were checked. Evaluation remained sealed; all 46 prior protection manifests are verified separately.

The completed independent review is recorded in COMPLETED-REVIEW.md. Hashes establish current artifact integrity; historical fresh-context isolation/no-retry provenance additionally relies on retained first-save records and task history. No model or live retrieval rerun is required for review.

## What this rules out

A fixed reserved prefix is not a substitute for judging relevance. It can protect irrelevant early results and still discard useful late results. Increasing or decreasing the reserved count after seeing these cases would be tuning; none was performed.

Keep the foundation baseline. The next hypothesis worth evaluating is whether selecting candidates by their relevance to the requested Formly aspects can distinguish useful late facts from irrelevant early facts. This result does not establish which relevance method would work, and no such new selector was implemented here. These requests are now diagnostics, not fresh qualification data.

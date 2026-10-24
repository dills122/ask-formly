# Retrieval integration: completed first run

Foundation alone is the strongest tested retrieval arm here. Neither frozen GLiNER model passes the prospective retrieval-benefit gate or annotation-consistency gate. Do not promote the API-only probe bridge. Gold API probes also fail the retrieval gate, so improving extraction alone is insufficient for this bridge on these cases.

## Scope and evidence

36 fresh development requests in three disjoint batches of12;45 derived questions;78 prospectively reviewed exact typed mentions. Same first foundation outputs in every arm. No repair retries, training, tuning, candidate edits or sealed evaluation access. Native foundation was run once perbatch, not repeatedly qualified here. Both frozen epoch6 adapters use CPUfloat32/fourthreads/threshold0.5/flat decoding with unchanged labels. Every model parameter matches its training receipt before inference and remains unchanged after. All36 core plans remain identical perarm; zero extraction errors or missing records. This tests a new optional API-query bridge, not every possible use of annotations.

Existing hybrid retrieval, RRF, obligation merge and eight-result cap are unchanged. Database accessed mode=ro/query_only; all46 fact vectors transient. Full original questions always queried; accepted API mentions add a separate query, which can displace full-question hits after fusion. No answerer or evidence acceptance assessment. The30 supported cases comprise28direct and2partial: R14 does not establish durable future reset-baseline capture; R31 does not fully establish expression trigger boundaries. Six other cases lack catalog support, not necessarily library support.

## Retrieval results

Metrics average across30 cases with nonempty relevance gold, not across all36. Required groups allow predeclared alternative facts; complete groups does not mean every relevant fact, every caveat, or a correct final answer.

| Arm | Recall@8 | Precision@8 | nDCG@8 | MRR@8 | Complete groups@8 | Complete groups@4 | Queries |
|---|---:|---:|---:|---:|---:|---:|---:|
| Foundation |92.22%|22.50%|91.32%|98.33%|30/30|30/30|45|
| +1701 |91.67%|22.08%|86.75%|93.89%|30/30|27/30|82|
| +1702 |91.67%|22.08%|88.10%|96.11%|30/30|27/30|82|
| Gold API diagnostic |91.67%|22.08%|87.54%|96.11%|30/30|27/30|84|

All arms have100% any-hit@4/@8 on these30 cases. Recall@4:88.61%,86.94%,86.94%,85.28% respectively. Low precision reflects an eight-slot packet containing many nonrelevant facts; it is not90% answer accuracy. Each arm returned48candidates across six unsupported cases at8,24at4. No abstention was implemented, so these are exposure counts, not false answers.

Foundation recall@8 bybatch:98.33%,84.17%,94.17%. Both GLiNER arms:96.67%,84.17%,94.17%. Thus pooled retrieval recall clears90%, but does not clear89.25% in everybatch. Complete required-group coverage is100% perbatch at8; this narrower measure must not replace all-relevant-fact recall. Full top4/top8 perbatch summaries and timing in test-output/report-metrics.json.

Only R06 changes relevant-fact recall@8: all three annotation arms lose custom-type-use-example/field-uses-registered-name, add defaults-and-resets/default-eligibility, and fall from5/6 to4/6 relevantfacts. Required groups still have alternatives. No request gains recall@8. Ranking and top4 group losses matter despite30/30complete at8. No annotation arm reaches the frozen minimum+2percentage-point recall improvement; precision also drops.

## Annotation results and90% consistency

Exact typed spans under the pre-inference conventions, including method name without invocation syntax. Raw and accepted metrics, perrole errors and every case retained in scores.json. The foundation does not attempt annotations: its machine consistency=false is not a foundation quality failure and must not be compared as an extraction candidate.

| Model | TP/FP/FN | Pooled precision | Recall | Batch1 precision | Batch2 precision | Batch3 precision |
|---|---|---:|---:|---:|---:|---:|
|1701|66/12/12|84.62%|84.62%|81.48%|85.71%|86.96%|
|1702|67/10/11|87.01%|85.90%|82.14%|92.31%|86.96%|

Both fail minimum89.25%precision in everybatch and pooled.1701also misses80%recall inbatch1 (78.57%).1702batch recalls82.14%,88.89%,86.96%. One right-to-wrong prediction moves batchprecision3.57–4.35percentagepoints; these panels cannot resolve populationprecision to±0.75points. Descriptive pooled Wilson95%intervals:1701[75.01%,90.97%],1702[77.72%,92.79%]; correlated synthetic mentions limit binomial inference. No seed selection or retrospective relabeling.

Five boundary errors shared bybothmodels: R02-q0/q1 andR20-q0 include invocation parentheses/arguments in methodAPI spans. Shared errors also include custom generic MyProps tokens treated as APIs, missed key/props/FormlyForm references, modelChange value misclassified asAPI, numeric0 modelkey classified asvalue, and sessionStorage incorrectly included in Formly/AngularAPI scope. R18built-in input registration is missed by1702, misclassified by1701, which also tags generic type. R18and invocation/generic boundaries remain convention-sensitive and are disclosed, not regraded after predictions. API-role precision80.36%/83.64% is the main weakness. The5invocation boundary mismatches alone account for5FP+5FN each, but no hypothetical corrected score is a measured improvement.

## Costs

Across36requests: foundation retrieval0.277s;1701retrieval0.404s plus9.990s extraction;1702retrieval0.402s plus10.236s extraction. Model loading3.923s/3.750s separately; projection totals0.00194s/0.00185s. Request extraction p50/p95:1701 0.225/0.443s,1702 0.233/0.467s. Retrieval setup recorded separately in report-metrics.json. These are local observed timings, not service SLAs; foundation generation latency is not measured as an online model service here. The modelarms nearly double querycalls and add extraction cost without observed retrieval benefit. ONNX telemetry persistence warning retained; initialization and144retrieval records completed.

## Next bounded step toward a consistent90%

Keep the accepted foundation as the working path and both extractors available experimentally. Separate goals: annotation exact precision and retrieval coverage are different metrics. Retain89.25%minimum perbatch, bothseeds, with recall and no-regression safeguards for annotation qualification; do not relabel92.22%retrievalrecall as annotation success.

Before more GLiNER training, test a new context-preserving query candidate against foundation-only, using the frozen engine/DB and same resultbudget. The present API-only probe drops the requested relationship (e.g. registration/selection) and gives broad identifiers another vote. A candidate should preserve the requested operation and conditions in any supplemental query. Compare foundation-generated contextual probes and gold-guided contextual probes first; only involve the extractors if gold guidance adds value. Freeze new cases/criteria before predictions; use current36only as diagnostics. This is a proposed next experiment, not an implemented or proven improvement.

For extraction itself, concentrate any later bounded adaptation on the five invocation-boundary patterns, generic type arguments and the observed role contrasts, with replay protection and fresh disjoint cases. Do not broaden vocabulary or retrain merely to raise an unused score. Both models must preserve previous gains and clear the floor acrossbatches. A larger independently authored panel is needed for meaningful consistency evidence; rerunning identical deterministic extraction does not supply independent evidence.

No engine/data redesign is justified by this result. The missed background/qualification facts (R15/R16/R18/R19/R28/R30), despite satisfied minimumgroups, are the retrieval diagnostic targets. Verify context-preserving queries can recover them without losing existingfacts before deciding on further extraction investment.

## Verification

13 local tests passed before inference, and independent preflight passed. Extraction and retrieval output manifests verified before downstream use.329 input/artifact/dependency hashes frozen before inference. Prior44protectionmanifests verified before run; final preservation and completed independent review recorded separately. No sealed semantic contents read. Full rawoutputs, counts, percase gains/losses and timings remain in test-output. This report is subject to the final independent review.

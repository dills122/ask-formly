# Candidate retrieval and relevance selection: results

**Deeper retrieval recovered useful candidates, but this selector is not ready to replace the foundation.** The joint arm improved minimum catalog-supported aspect coverage while losing labeled relevant facts. No promotion criteria were relaxed after seeing the results.

## Fixed experiment and integrity

36 fresh requests in three batches produced59 focused questions using the unchanged qualification_v3 contract. All first submissions passed structural validation. Preflight independently labeled18 direct,12 partially supported and6 unsupported requests BEFORE retrieval, and identified one foundation meaning failure (R26). That failure was retained. Partial catalog gaps remain explicit in data/cases.json; retrieving their known facts cannot establish full answers.

Four arms shared the saved query results. Foundation used hybrid depth8 and existing interleave into8. Wide rank used hybrid depth20 plus original candidates, then existing interleave. Narrow select and wide select used separate fresh native contexts and the same selector contract over their corresponding pools, with opaque handles and no retrieval ranks, gold or source requests. The selector saw only focused questions and candidate claims/conditions/limits/version/adapter. Depth20 was fixed prospectively, with no query expansion, sweep, tuning or retries.

The engine's existing depth argument changes both component lists before fusion; top20 need not prefix top8. Each wider pool therefore retains original candidates explicitly. There were118 actual calls (59 per depth),36 acquisition traces,144 final packets and288 per-case metric sets. All acquisition inputs and first responses were frozen before scoring. Existing code/models/DB remained unchanged; the sealed evaluation was accessed only through preservation hashes.

## Results at eight slots

Recall is mean coverage of all prospectively labeled relevant facts across30 supported/partially supported requests. Complete groups requires at least one acceptable fact for every catalog-supported aspect. These are different metrics; neither is final-answer accuracy.

| Metric | Foundation | Wide rank | Narrow select | Wide select |
|---|---:|---:|---:|---:|
| Relevant-fact recall |76.89%|78.11%|73.44%|74.78%|
| Precision@8, fixed denominator |29.58%|30.83%|27.50%|28.33%|
| nDCG |73.26%|73.82%|80.00%|81.01%|
| MRR |85.00%|84.44%|96.67%|96.67%|
| Mean supported-group coverage |91.39%|91.39%|93.61%|96.67%|
| Complete supported groups |25/30|25/30|26/30|29/30|
| Any labeled relevant hit |29/30|29/30|29/30|29/30|
| Unsupported candidate exposures |48|48|0|0|
| Total facts selected, all36 |288|288|75|91|
| Relevant / all selected facts |24.65%|25.69%|88.00%|74.73%|
| Relevant baseline facts lost / gained |—|2 /5|8 /3|11 /8|

The shorter selected packets explain why selected-fact precision can rise while recall and fixed-denominator precision@8 fall. Selecting nothing for six unsupported cases is useful observed behavior, not proof of generally correct abstention. No final answer was generated.

| Batch recall | Foundation | Wide rank | Narrow select | Wide select |
|---|---:|---:|---:|---:|
|1|78.50%|74.67%|79.00%|81.00%|
|2|74.17%|74.17%|65.83%|64.17%|
|3|78.00%|85.50%|75.50%|79.17%|

**None meets the89.25% floor.** These are new requests and new prospective labels; the earlier92% result does not describe this panel. Do not combine them into a claim of consistent performance. Small, topic-correlated development batches do not establish population accuracy within±0.75 percentage points.

At4 slots, recall is62.22%,62.89%,73.44%,73.28%, respectively; complete supported-group counts are17,18,26,28 of30. Semantic selection improves placement of a small set of useful facts near the front, but it does not preserve all labeled relevant material.

## What retrieval fixed

Candidate-pool available recall rose from82.56% to94.72%. By batch, original pools contain88.83%,76.67%,82.17% of labeled relevant facts; wider pools contain94.17%,90.00%,100%. These are availability bounds over unions averaging9.86 and22.56 candidates, not eight-slot packet scores or deployable performance.

Only three supported requests still lack relevant facts anywhere in their wider pool:
- R02 and R07 lack props-and-registration/registration-adds-configuration.
- R20 lacks custom-types-and-wrappers/fieldtype-surface, its sole prospectively labeled supporting fact. Its requested Material label/placeholder details are independently outside this catalog.

The joint selector completes groups missed by the foundation in R03 (hidden control caveat), R04 (wrapper versus control responsibility), R26 (reverse-merged defaults) and R27 (shared-key hidden control caveat). R26 also has the retained foundation semantic failure; its conditional retrieval gain must not be treated as a valid complete source-request plan. No complete foundation group is lost by wide selection.

## What selection still loses

Wide selection loses11 relevant baseline fact occurrences across10requests and gains8 occurrences. All ten loss cases leave unused slots: their packets contain only1–4facts. **The eight-slot cap is not what caused these losses.** The selector chose a sparse set rather than retaining every useful corroborating fact.

Some losses retain alternate coverage: R01 replaces a registered-name usage example with another registered-type usage fact; R10/R34 replace registration-adds-configuration with type-registration-options. Others omit corroborating eligibility/default, field-surface, key-shape or registration facts while a minimum group remains covered. R13 loses two relevant type-use/registration facts. Every exact loss and gain is preserved in scores.json; these are not erased because substitutes remain.

The selector prompt favors useful support and avoids duplicate filler. The strict evaluation also values all prospectively relevant corroborating facts. This distinction helps explain the split between29/30 minimum-group coverage and74.78% broad recall, but it is not grounds to regrade labels or change the success criterion afterwards. Wider context also lowers selected-fact precision versus narrow selection (74.73% versus88.00%). A larger pool alone does not make the relevance decisions reliable.

## Gates and retained failures

The joint arm fails fact preservation, pooled utility (−2.11 percentage points of recall), batch nonregression and consistent floor. It passes delivery/runtime checks and unsupported-exposure nonincrease. It independently fails source meaning preservation: R26's inherited-defaults follow-up drops the input-renderer scope and its ledger binding. Structural validity does not catch this omission.

The pipeline therefore reports qualified=false. Keep the existing foundation unchanged; do not promote this experimental selector or claim the foundation itself consistently clears90%.

## Cost and reproducibility limits

Local index setup took0.770seconds. Depth8 queries took0.352seconds total and depth20 took0.347seconds total, acquired in alternating order; this is one local run, not evidence that deeper search is faster. The complete experiment acquired both. Foundation/narrow selection logically require59querycalls; wide arms require118because they preserve original pools as well as depth20 lists.

The three narrow selector payloads total142,392bytes and outputs18,227bytes. Wide payloads total289,707bytes and outputs20,970bytes. Payload bytes exclude the selector contract and orchestration messages. Narrow batch dispatch-to-first-output wall times were40.01–58.33seconds; wide46.04–48.16seconds. These include agent scheduling/tools and cannot be presented as isolated model inference latency or deployed end-to-end performance. Native model settings were not pinned; no repeated-run stability claim is made.

17tests pass. Core candidate/assessment tests followed red/green TDD; first-save/hash checks were added around reused orchestration primitives. Prospective review instance1 approved diagnostic execution, not candidate promotion. Completed fresh-context review instance2 is recorded separately in COMPLETED-REVIEW.md. Byte manifests verify current integrity; historical fresh-context/no-retry provenance also depends on retained receipts and task history.

## Decision and next hypothesis

This experiment supports deeper acquisition as a useful source of candidates. It does not support this sparse native selector as the replacement packet builder. Future work should explicitly distinguish minimum aspect coverage from retaining all material corroboration, and test a selection rule that uses remaining slots for useful support without inventing relevance from shared vocabulary. It should keep the fixed eight-slot budget and validate both losses and gains on fresh data. That is an untested hypothesis, not an implemented change or a request to broaden the DB.

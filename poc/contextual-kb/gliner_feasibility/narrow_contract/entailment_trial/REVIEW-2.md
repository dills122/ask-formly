# Independent result and usability review

Review instance: 2 of 3. Same reviewer across text-only and annotation/result phases; no additional review instance or delegation. Reviewed working-tree artifacts on main at c3091328f49d53de6b41a49c4fe5aa8f1c45e516. POC is untracked amid unrelated working-tree changes; those changes were not reviewed or modified.

## Findings

1. **P1 — Do not continue or adopt the NLI alternative under the declared gate.** Both seeds have zero correct operational repairs and one wrong change/lost correct mention on the labelled development panels. In `test-output/run-v1/{1701,1702}-adjudicated30-scored.json`, VCAL-015 changes `'account.id'` at [58,70) from model_key to registration_name despite the sentence explicitly calling it the field key. Independently recomputed top support 0.947811 and margin 0.220417 meet the fixed rule: the model suggestion, not arithmetic, is wrong. On the actual usability questions NLI also makes 13 harmful changes across eight questions per seed. H03-q1, H07-q1/q2, H21-q3/q4, H22-q2, H24-q4 and R03-q1 replace correct version/adapter/key/name/literal roles with api_reference. Minimal action: record failure and stop this branch as prescribed; do not tune or adopt it. This is an experiment outcome, not a request to replace the architecture.

2. **P2 — Raw role hints are unsafe as authoritative filters.** Manual inspection of all 120 question/seed rows found visible defects in eight questions per seed. H01-q1, H13-q1, H14-q1 and H21-q1..q4 tag registered-component prose `type` as api_reference, contrary to the shadow rule's explicit category/property distinction. H15-q1 puts exact registration names SSN/ssn under value; seed 1702 additionally includes malformed boundaries and an overlap with an API span. `R05-q1` detects Material correctly as an adapter mention, but the request excludes it: this is a polarity/filter hazard, not a false entity role. Minimal action: retain only optional, non-authoritative hints alongside original question text, with no hard filtering. No annotation defect prevents formulating a text query from the unchanged question. Flat role inventories also do not encode pairings, requested-versus-protected API roles or conditional existence.

3. **P2 — H07 first focused question loses an explicitly shared condition.** `data/usability-plans.json`, H07 question 1 omits that the selected value still appears among replacement options, although the original request explicitly applies its conditions to both questions. Question 2 retains it. Broad text search remains possible, but this is not a fully faithful focused plan. The original request's presence cannot excuse the missing condition. Minimal action now is to report this frozen v2 limitation; do not edit the baseline. This finding was frozen before model inference.

## Plan Review

The bounded design distinguishes text preservation, optional hint quality, and operational relabeling. That separation is necessary and supported by the observations. The full 30-request/60-question v2 panel was preserved; H11's empty plan is appropriate because the request does not justify a Formly library need. Text review found 29/30 plans fully usable under the requested preservation criteria. This is one independent qualitative pass over exposed diagnostic material, not a statistical production estimate.

The no-training/no-tuning diagnostic reaches its declared stop outcome. No heavy pivot is needed to conclude it. The historical best-configuration inventory explicitly disclaims promotion and notes the earlier learned verifier's failures; it should be supplemented with the current negative NLI outcome and scope caveats, without rewriting the earlier results.

## Author-Claim Reconciliation

| Claim / artifact | Independent evidence | Status |
| --- | --- | --- |
| Unchanged v2 requests and outputs | Full object equality against refinement_v2/cases.json and test-output/beta1.json; all 30 requests and 60 questions | Confirmed |
| Raw annotation output preserved | Every scored before-set equals raw emitted typed spans; every annotation offset slices its actual question text | Confirmed |
| Fixed hypothetical policy and summary | Separate Python recomputation from stored probabilities, raw spans and gold; all counters and hypothetical after-sets agree | Confirmed |
| development_gate=false | Zero correct repairs and one lost-correct/wrong change per seed | Confirmed |
| Preserved protected/source inputs | before.json equals after.json; frozen run hashes verified | Confirmed at artifact level; no sealed contents read |
| Current composition qualified | BEST-QUESTION-CONFIGURATIONS.md explicitly makes no such claim | Appropriately limited |

## Verification Performed

Read AGENTS.md, POC AGENTS/STEERING, trial PROTOCOL and shadow annotation rule. Assessed every request and focused text before predictions; then every raw annotation before NLI results. No prior usability grades were consulted. Text ledger SHA256 remains `715d9c88f0f68d9c0f72d980c28e12aa90cd24191df08a73c26123b374bc6803`. Raw annotation ledger was saved before NLI inspection with SHA256 `ac22aa959a4f604f6cc546da9adb3a8c51805ad9a1ee6aadc8bf24ffc5bc1466`.

Independent Python checks reproduced all reported baseline/candidate correct and extra counts, exact-case counts, abstentions, gained/lost mentions and changed-group judgments. Labelled counts (correct / emitted; recall denominator in parentheses):

| Seed | Panel | Baseline | NLI alternative | Exact cases before/after |
| --- | --- | --- | --- | --- |
| 1701 | shadow30 | 28/29 (30) | 28/29 (30) | 27/27 |
| 1701 | adjudicated30 | 57/61 (65) | 56/61 (65) | 20/20 |
| 1701 | fresh24 | 25/27 (25) | 25/27 (25) | 23/23 |
| 1702 | shadow30 | 29/29 (30) | 29/29 (30) | 29/29 |
| 1702 | adjudicated30 | 56/58 (65) | 55/58 (65) | 22/22 |
| 1702 | fresh24 | 23/23 (25) | 23/23 (25) | 22/22 |

Supplied-span oracle accepted correct roles: fresh24 0/25, shadow30 1/30, adjudicated30 2/65. Explicit no-entity decisions: 0/0, 1/18, 1/36 negative probes respectively; abstention is not a correct no-entity decision. These are policy-qualified accepted-role counts, not an unconstrained argmax accuracy metric.

Verified 326 unique (text,start,end) NLI calls across extraction and supplied-span inputs, consistent cached probabilities, 2,282 hypothesis pairs, and per-occurrence times summing to 50.927966832 seconds. These mixed cached/uncached experiment totals do not establish per-seed or production latency. All frozen run files matched recorded SHA256 values. No model inference, training, search, DB call, application investigation or baseline modification was performed by this reviewer.

## Open Questions And Residual Risks

The usability questions have no independently authored exhaustive mention gold. The manual annotation ledger records visible defects and missing role hints, not six-role precision/recall certification. Questions such as R05 can have correct entities while unsafe filter semantics. Text query usability does not demonstrate executable retrieval, corpus answerability or answer accuracy. Preparation/model-loading and full implementation correctness were covered by the separate preparation review rather than repeated here. Graph tools were reported unavailable; limited policy source inspection was direct, without a graph-coverage claim. No sealed evaluation contents were read.

## Verdict

**Ready with non-blocking follow-ups** to close and report this bounded negative experiment, preserving frozen evidence and adding its outcomes to the configuration inventory. **The NLI alternative is not ready for continuation or adoption** under the predeclared gate, and raw annotations are not approved for hard filtering. The text plan remains a useful experimental candidate with the H07 limitation explicitly recorded.

## Recommended Next Actions

Record the negative gate, 13 harmful usability relabelings per seed, and the separation between 29/30 text preservation and unreliable role hints. Keep both frozen extractors, v2, A and data/DB unchanged. Do not start another review or tuning loop for this result. Per-request and per-question evidence is in usability-text-review.json, usability-annotation-review.json, usability-nli-change-review.json and review-2-arithmetic.json under test-output/.

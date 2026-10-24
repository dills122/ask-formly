# Completed integration independent review

Review instance: 3 of 3 (final permitted). Scope: untracked gliner_integration_v1 at dirty main c3091328f49d53de6b41a49c4fe5aa8f1c45e516. Unrelated root edits excluded. Independent-review and code-review-and-quality reviewer workflows applied. The preliminary report was written before RESULTS-AUTHOR.md was read; implementation conversation was not supplied. No inference, training, implementation fixes, prior-artifact changes, or additional review instances.

## Findings

No actionable implementation defect found in the completed experiment. The principal negative result is real: **neither model passes the frozen annotation value gate**. This blocks required integration/promotion, not acceptance of the completed experiment as evidence.

| Model | TP / FP / FN | Accepted precision | Accepted recall | Exact rows | Correct coverage | Empty-control FP |
|---|---|---|---|---|---|---|
|1701|77 / 9 / 10|89.53%|88.51%|34/44|32/34|0/10|
|1702|77 / 8 / 10|90.59%|88.51%|35/44|32/34|0/10|

Both miss the fixed precision >=95% criterion. Both satisfy recall >=80%, coverage >=50%, no extraction failures, and no accepted hints on empty controls. Baseline precision is undefined and recall zero because it deliberately supplies no annotations; this does not imply its full-text plans are useless or wrong.

Inspected all 44 gold rows and all 88 per-model case comparisons; independently reconstructed both raw and accepted sets from JSONL, checked exact offsets, every miss/extra, typed and untyped aggregates, saved/new splits, all six role metrics, and gate arithmetic. Results agree with scores.json. Errors include P14 version-range merging/role, P26 fragmented opaque expression, P44 quote boundaries, I10 merged API/value, missed key, generic type/model-value tags, and I05 role convention. I05's model.needsReview label is prospectively adjudicated operational gold, not universal semantic truth. No posthoc gold adjustment is justified here.

Raw and accepted scores match on the annotated panel. All-panel counts are 555/555 for1701 and529/523 for1702. Six removed1702mentions lie outside the scored gold panel; their semantic correctness remains unmeasured. Zero same-span cross-role conflicts and zero scored correct spans lost to filtering were independently verified. Structural acceptance does not certify semantic correctness.

## Plan Review

The bounded plan is fulfilled: freeze requirements and requests, freeze complete inputs/annotations and implementation before inference, run unchanged foundation versus both retained epoch6models, retain first deliveries/raw predictions, compare advisory annotations, preserve previous artifacts, and obtain final independent review. Safety passes174/174for every arm; 295derived questions were actually extracted once per model, including gold-empty actual questions. Empty plans correctly cause no synthetic extraction. Full question plans, ledgers, constraints, search queries and advisory flags are preserved.

Implementation is small and follows the frozen foundation projection. Extraction exceptions and malformed envelopes fail open; invalid core input still fails. Native evidence and confidence remain in raw evidence, while only exact role spans reach the existing optional-hint validator. No retrieval, DB access, answer synthesis, threshold selection, or seed selection is introduced. The runner loads models sequentially, freezes parameters, uses inference_mode, and verifies identity; tests cover the stated faults. Nested overlap validation is quadratic in hints but inherits the existing bounded POC behavior and is not a demonstrated problem for this run.

## Author-Claim Reconciliation

| Author claim | Inspected evidence | Status |
|---|---|---|
|174records per arm;295extractions per model; unchanged core|records.json, all3JSONL files, pure replay using retained native results|Confirmed|
|Both models match retained epoch6 and do not train|run.py,564parameter digests per model before/after and retained training-receipt final_hashes|Confirmed for retained evidence|
|Both annotation gates fail|Independent per-row set arithmetic, fixed PROTOCOL.md|Confirmed|
|No scored filtering loss; six unscored1702mentions removed|All raw/accepted sets and gold intersection|Confirmed|
|Single-pass diagnostic timings|run.py perf_counter boundaries, raw seconds and recomputed sums/nearest-rank quantiles|Confirmed; not end-to-end latency|
|Prior artifacts preserved|43manifest maps,39289overlapping byte-hash entries|Confirmed|
|No resampling or repair|Exclusive-create runner, first-save/completion receipts, frozen literal/output correspondence|Consistent with retained provenance; local artifacts cannot prove absence of unrecorded work|

Fresh source provenance is a saved literal delivery passed through qualification_v2/runner.py, not an independently timed model-service generation invocation. Its packet/source/runner/output hashes match the receipts; the12fresh objects match delivered outputs exactly and combined records equal saved records plus fresh records. This supports a bounded development comparison, not a new foundation qualification claim. Import/setup and extractor timings exclude fresh generation.

## Verification Performed

- `PYTHONDONTWRITEBYTECODE=1 python3 .../test-output/review3-verify.py`: passed after correcting the review script's own relative-manifest resolution; first attempt failed before completing preservation because relative entries resolve from each experiment root, not CWD. No product defect or changed evidence resulted.
- Independently checked design/run/inference/results freezes:4/54/10/3entries, all unchanged.
- Independently byte-hashed all43protected manifests'39289overlapping payload entries, including sealed files without parsing them. Protected-before/pre-inference/after-inference summaries agree. No drift.
- Replayed projection only, without models, for every saved native result and compared complete plan equality.174records per arm;295extractions per model; exact question identity/order; no errors; input unchanged assertions passed.
- Verified564parameter digests per model before/after against retained training receipts.
- Ran all22integration/assessment tests: pass. Temporary test data used review3-prefixed directories and was removed; bytecode disabled. Log: test-output/review3-tests.txt.
- Verified all44row comparisons per model in raw and accepted modes, typed/untyped/split/role scores, coverage and gate arithmetic. Evidence: test-output/review3-checks.json and review3-additional-checks.json.
- Exact-path coverage query returned not_tracked for new/imported source against October16graph. Read source directly; no graph completeness inference or reindex.

Per-question p50/p95 are187.590/201.434ms and189.410/203.368ms; per-request p50/p95 are367.285/571.533ms and370.597/573.174ms. Actual extraction totals are55.683/56.113seconds. CPUfloat32/fourthreads recorded; import8.436seconds and model load saved separately. Projection clocks exclude extraction, and enhanced projection clocks do not include the initial baseline validation; do not present these clocks as complete wrapper overhead. No latency SLA or retrieval/agent latency conclusion follows.

## Open Questions And Residual Risks

Only44prospectively annotated rows/87mentions support precision claims; saved repeated outputs are correlated. Role support is small (three model-key mentions, ten registration names). Value recall is13/17=76.47% despite overall recall passing. New-panel precision is89.47%/91.89%, recall87.18%; neither gives a hidden passing subgroup argument for promotion. The foundation12fresh single deliveries are development checks, not independent repeated qualification. Unknown/unscored mentions and future application traffic have no proven semantics. This review establishes code/evidence consistency and safe advisory behavior in the tested boundary, not production robustness or retrieval lift.

## Verdict

**Ready** as a completed, safely bounded integration experiment and evidence package. **Not accepted for required annotation integration:** both frozen value gates fail. Retain the foundation-alone default; both adapters may remain explicitly optional experimental metadata. Hints remain advisory_only and usable_as_filter=false. There is no evidence for automatic promotion, selecting the better seed, or changing acceptance criteria.

## Recommended Next Actions

Finish the human report and final preservation freeze while retaining these negative gates and limitations. No implementation fixes or additional review instance are requested. The maximum3of3review instances is reached; this review loop ends here. Any future development/criterion changes require a separately authorized experiment, not revision of this run's gold or frozen evidence.

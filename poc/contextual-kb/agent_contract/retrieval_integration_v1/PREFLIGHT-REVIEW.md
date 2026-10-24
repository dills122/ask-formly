# Independent preflight review

Review instance: 2 of 3. Verdict: **Ready for the frozen experiment, with non-blocking reporting follow-ups**. Machine verdict: `ready`. This is not a verdict on retrieval usefulness or extraction accuracy.

## Findings

No material blocker found in the reviewed implementation or prospective labels. The new bridge retains the full derived question, adds only accepted API-reference text in source order, reuses the existing reciprocal_rank_fusion and merge_obligations, and keeps the eight-result budget. The full-question candidates can be displaced after fusion; no false preservation guarantee is made. No filters, link expansion, answerer or engine changes were introduced. Both model arms must pass independently; paired complete-group losses block the gate even when another case recovers the aggregate count.

1. **P3 — Complete the promised reporting fields.** `scoring.py:10` summarizes MRR but not explicit any-hit rate; `scoring.py:45` retains TP/FP/FN and Wilson intervals but no explicit one-count sensitivity; `scoring.py:52` omits extraction/projection timing summaries. Top4 is pooled while batch summaries at line 60 default to top8. Raw question/request timings, per-case hits/MRR, and counts are retained, so these can be computed without rerunning or changing outputs. The completed report must show these fields and distinguish extraction load, extraction, projection, retrieval setup and query costs. Do not interpret retrieval-only elapsed seconds as total added annotation cost.
2. **P3 — Verify downstream output freezes in orchestration.** `retrieve.py:12` verifies the input run-freeze and checks extraction completion, but does not read extraction-freeze. `scoring.py:22` checks cardinality/identity but does not check extraction/retrieval output manifests. Before consuming and reporting outputs, explicitly verify the relevant immutable manifests, in addition to verifying them again in completed review. This is a bounded local harness with exclusive-create output files, not an exposed ingestion service; no observed drift makes this a blocker now.

## Plan review

The design freeze's five hashes match current protocol and initial request files. All 36 first foundation envelopes validate against the unchanged qualification_v3/refinement_v3 contract. The 45 questions match their gold rows byte for byte. All 78 mentions have exact source offsets, source order and no overlap; all 36 relevance rows reference existing catalog IDs, and every required-group alternative is relevant. The gold contains 28/27/23 mentions by batch. The 46-fact catalog was inspected, including claims, conditions and limits; the 36 case judgments are reasonable prospective relevance judgments under the declared policy.

Method references exclude invocation syntax, object arguments are whole opaque values, generic application type arguments are untyped, and platform/RxJS APIs are outside the narrower pilot API role. The built-in input registration in R18 follows the narrow named-registration contract despite the pilot description's custom-only wording. These are disclosed prospective conventions, not retrospective adjustments. Retain convention-sensitive errors in the final diagnosis.

R14 and R31 are explicitly partial. Their required-group completion means completion of catalog-backed groups, not full answerability. The six unsupported-in-catalog cases measure candidate exposure; they cannot establish that Formly lacks the feature, that an answer hallucinates, or that evidence was falsely accepted. Other 28 cases are directly supported. No material substitute-group defect found.

The preflight stage precedes the complete run-freeze by design. The parent must include new/reused transitive code and contracts, all request/foundation/gold/case/catalog files, the database, both model artifacts/receipts, embedding artifacts, runtime dependencies and this decision before inference. Existing candidates, models, prior outputs and database remain immutable. No training or repair retry is authorized by this readiness decision. Final independent review remains instance 3 of 3.

## Author-claim reconciliation

| Claim | Evidence | Status |
| --- | --- | --- |
| Full questions plus optional API probe; unchanged RRF/merge/top8 | bridge.py; question_pilot.py source; probe/full-query/no-hint tests | Confirmed |
| 13 tests pass, including paired-loss regression | Independent run retained in test-output/preflight-tests.txt | Confirmed: 13 pass, zero errors/failures |
| 45 rows, 78 gold mentions, 36 cases | Full data inspection and mechanical validation | Confirmed |
| Supported/partial cases separated from six unsupported exposures | relevance and retrieval_summary distinguish 30 nonempty-gold cases from six empty cases | Confirmed; partial-versus-direct class remains in cases.json and must accompany final interpretation |
| Errors, missing counts, unchanged core tracked | integrate, extraction_coverage, metrics and scoring source | Confirmed for the emitted schemas; malformed external files are outside this local runner's tested boundary |
| Read-only DB; transient index only | readonly URI/query_only and denial test; PilotIndex source | Confirmed structurally and via disposable fixture. Real compatibility log reports 46 transient vectors/no questions; reviewer did not repeat it |
| No inference/retrieval results yet | Artifact inventory has no extraction/retrieval run directories | Confirmed at review time |
| Model weights unchanged before/after | Extractor disables training, uses inference_mode, compares complete parameter hashes against receipt and afterwards | Enforcement inspected; actual checkpoint/runtime equality remains a run-time check, not independently executed here |
| All relevant timings and failure evidence retained | integrate emits raw timings/errors; retrieval emits query counts/timing; parent process logs still needed for catastrophic errors | Confirmed at raw-record level; final aggregate reporting remains follow-up |

## Verification performed

- Read tests before implementation and wrote PREFLIGHT-PRELIMINARY.md before opening AUTHOR-EXPLANATION.md.
- Verified repository main/HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516 and broad dirty state; only new-directory review scope considered.
- Used codebase-memory coverage for all twelve relied-on Python files. October 16 generation reports not_tracked; read direct source, without reindexing or treating graph absence as evidence.
- Ran `python3 -B` unittest discovery for the two test modules: 13 pass. A wrapper sets TemporaryDirectory prefix to preflight- so the disposable write-denial fixture stays within the explicitly allowed review-output namespace. No production DB or model was used.
- Validated all gold offsets/order/nonoverlap/question identities, catalog membership and required-group subsets; validated all 36 foundation envelopes through frozen build_plan; checked all five design-freeze hashes.
- Inspected compatibility log only: 46 facts, 46x384 transient vectors, no question queries. A telemetry persistence warning is visible in that log and does not demonstrate failed read-only DB access.
- No model or real retrieval run, optimizer, training, sealed-content read, Git mutation, dependency installation or code/data edit occurred. Only the three named review artifacts and preflight test log were written.

## Residual risks and next actions

Unit coverage is proportionate to this local bridge but does not exercise full model loading, actual retrieval or a complete scoring run. Readiness permits that experiment; it does not certify those pending runtime stages. Snapshot and verify the complete dependency/input freeze, preserve process stdout/stderr and first outputs, execute without retries/repair, verify output freezes, and report both models and oracle independently. Tiny correlated synthetic batches can support observed consistency only; they cannot resolve true precision to within 0.75 percentage points.

No further review instance was spawned. The parent owns completion and the final instance-3 review.

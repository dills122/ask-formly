# Qualification v3 results

The new candidate passes the frozen experimental qualification and the strict perfect gate. Independent review found no actionable defect or material intent failure in this bounded panel. This establishes eligibility for consideration as an experimental foundation; no promotion or integration was performed.

## Change

The new contract preserves restrictions defining a referenced observer, callback or operation on linked follow-up questions, in both standalone question text and ledger bindings. For example, asking what information **that observer** receives retains the observer's **without polling** requirement. It does not propagate local restrictions onto explicitly independent or general questions, or invent eligibility gates. The prior contract is preserved as an exact prefix with one new rule appended. The validator, projection and qualification_v2 delivery harness are reused unchanged. There is no training or semantic output repair.

## Fixed results

| Measure | Fresh questions | Prior diagnostics |
| --- | --- | --- |
| Unique cases | 48 | 6 |
| First outputs across three repetitions | 144 | 18 |
| Structural validity | 144/144 | 18/18 |
| Question text correctness | 144/144 | 18/18 |
| Semantic correctness, including global scope | 144/144 | 18/18 |
| Mandatory binding correctness | 144/144 | 18/18 |
| Joint correctness | 144/144 | 18/18 |
| All three outputs usable | 48/48 | 6/6 |
| Meaning stability | 48/48 | 6/6 |
| Mandatory ledger stability | 48/48 | 6/6 |
| Exact whole-output JSON equality | 2/48 | 0/6 |

Every fresh group passed 24/24; every fresh repetition passed 48/48. There were zero observed material intent failures and zero missing or unassessable slots. All fixed thresholds in PROTOCOL.md passed, as did the separate strict perfect gate. Exact JSON equality occurred only on the two empty controls; stable meaning does not require identical wording, decomposition or optional grounded ledger entries.

The previous observer-information failure, N21, preserves both the invalid-transition purpose and no-polling restriction in all three diagnostic runs. Fresh cases also cover linked observer identity, cleanup without inventing a stopping gate, local restrictions on conditional follow-ups, and explicitly general or independent questions. No restriction leakage was found under the frozen policy.

## Evidence and review

All 21 first-response packets were delivered and reconstructed successfully. The independent reviewer manually assessed all 162 source/rubric/output slots and all 54 triplets, then audited literal-to-JSON byte identity, saved receipts, record reconstruction, candidate/input/raw freezes and optional-hint invariance. Parent aggregation agrees with the independent gate assessment. See [review](REVIEW-2.md), [machine results](test-output/results.json), and [every request and its outputs](test-output/all-questions.md).

All 36 tests pass: eight candidate tests, 20 frozen delivery tests and eight scorer tests. Selector development used a failing test before implementation. Tests establish transport and contract-selection invariants; semantic judgments come from the actual generated outputs and full review.

Two input-read calls were rejected before execution or response generation. The same workers resumed their first input read and first submission; no generated response was discarded, repaired, retried or resampled. These operational recoveries are disclosed in [execution notes](EXECUTION-NOTES.md). Saved hashes verify retained bytes, not unseen tool history.

Two independent authors prepared the fresh panel before outputs existed. Five prospective rubric corrections were recorded in [case review](case-review.md) before freezing and generation; original submitted rubrics remain preserved. No tuning or rubric change occurred during qualification. Review instance 1 covered preflight; instance 2 covered complete results. No third review was needed.

Final preservation verifies 42 inherited manifests covering 39,086 overlapping entries, including existing candidates, baselines and data/DB. Sealed evaluation remains unopened; preservation checks used byte hashes only. Final artifacts are recorded in test-output/final-freeze.json.

## Interpretation and limits

This is a synthetic, policy-informed development qualification. Fresh authorship does not establish semantic disjointness from previous Formly capabilities. Repetitions may be correlated; native model revision, temperature and seed were uncontrolled. Diagnostics were already exposed. Old and new fresh sets differ, so these totals are not a controlled causal comparison with qualification_v2.

The result supports moving forward with this candidate as a question-layer experimental foundation instead of treating perfect wording equality as the target. It does not establish deployed API reliability, production readiness, retrieval usefulness, answer accuracy, latency, cost or universal Formly compatibility. Sealed evaluation and any integration remain separate work.

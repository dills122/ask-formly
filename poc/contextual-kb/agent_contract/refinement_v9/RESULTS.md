# V9 exact-source and shared-context results

V9 completed the bounded trial and independent review. All generated questions preserved their requested meaning, and every declared condition passed literal source/question checks. One fresh response omitted required unknown-adapter scope from its ledger. V9 therefore does not pass the declared perfect repeated-pass gate and is not promoted. Evidence is complete; no saved output was repaired or resampled.

| Measure | Fresh | Diagnostics |
| --- | --- | --- |
| Requests × repeats | 24 × 3 | 3 × 3 |
| Structural / declared literal-copy validity | 72/72 | 9/9 |
| Question text and global scope | 72/72 | 9/9 |
| Complete bindings and joint pass | 71/72 | 9/9 |
| Requests passing all three repeats | 23/24 | 3/3 |
| Question meaning stable across repeats | 24/24 | 3/3 |
| Ledger meaning stable across repeats | 22/24 | 3/3 |
| Canonical JSON identical across repeats | 2/24 | 0/3 |

Fresh joint scores by repeat:24/24,24/24,23/24. Diagnostic repeats:3/3 each. Panels are selected by their explicit case-ID sets, not prefixes. All81 scheduled outputs are retained.

## What improved in this trial

The original C12 exact-copy failure did not recur in any of its three diagnostic runs. The previously invalid output remains rejected by the unchanged validator; v9 changes generation instructions, not acceptance rules. Across the fresh panel there were no declared non-source or missing-in-question excerpts.

Q03/Q04/Q05 contrast grounded same-referent history, explicit independence, and real conditional eligibility. All nine outputs pass. C14 also passes3/3 under the prospectively clarified shared-history rule. This criterion changed; its result is not purely evidence of model improvement. F23 event/restriction diagnostic passes3/3. No earlier results were regraded.

## Remaining failure and variation

Q19 run3 asks about probably6.3.x with an unknown UI adapter and correctly keeps global adapter null, but omits that explicit unknown-adapter scope from condition_bindings. Prose meaning is preserved; structured completeness fails. This requirement was added during pre-generation rubric review, retaining the original author rubric. Null alone cannot distinguish supplied uncertainty from unspecified scope. The failed slot remains counted.

Q06 run1 includes supplied existing-value background on both meaning and configuration, while runs2/3 bind it only to configuration. Independent review accepts the background as nonrestrictive but records ledger variation. Thus question meaning stability is not equivalent to ledger determinism. No fixed question-count or minimum-ledger heuristic was used.

## Implementation and review

New candidate only: original-source selection/check instructions and shared-context/eligibility clarification, retaining frozen v3 schema/transport. Prompt19,532bytes, versus16,098 in v8. No training, dependencies, downstream wiring or answer evaluation. Seven new transport tests pass; six frozen v8 regressions and eight aggregation tests pass. The TDD red was a missing candidate module, not evidence of a semantic model failure. Actual generation and independent all81-output review supply semantic evidence.

Fresh-context review1 found the Q19 omission and no additional actionable code defect. Its verdict is Not ready under the declared gate. Parent accepts the finding and interpretive decisions; no replacement review or scoring waiver. See REVIEW-1.md, REVIEW-RESPONSE.md, test-output/semantic-review.json, stability-review.json, aggregate.json and all-questions.md.

## Decision and limits

Retain v9 as a tested candidate demonstrating good question meaning and literal-copy results in this bounded sample, with one explicit ledger-completeness failure. Existing candidates stay frozen. Do not promote it as a fully reliable structured ledger or claim exact determinism. If another candidate is authorized, unknown-scope ledger completeness is the concrete remaining defect; avoid another broad redesign.

These are targeted, policy-informed synthetic development cases and correlated native-agent repeats with uncontrolled model revision/temperature/seed. No measured latency/cost, contemporaneous v8 comparison, production distribution, retrieval coverage or final-answer accuracy. Hashes preserve saved bytes, not unseen execution history or independent proof of chronology. Sealed evaluation remains unopened. Protected candidates, baselines and data/DB are unchanged, verified across37 inherited manifests/38,565 overlapping hash entries. Everything new is inside this POC directory.

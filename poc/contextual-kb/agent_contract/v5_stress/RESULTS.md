# Frozen v5: fresh stress results

24 fresh realistic requests, three batches of eight, each repeated three times: 72 first-submitted responses, 145 library questions and 218 condition bindings. No candidate changes, repairs, retries or tuning. Inputs and rubric frozen before generation; raw outputs frozen before independent review.

**The full gate failed: 62/72 responses passed both semantic and binding requirements; 19/24 requests passed all three repeats.** This qualifies the earlier smaller positive result: v5 is a useful foundation, but complete condition preservation is not yet reliable across broader requests.

| Measure | Result |
| --- | ---: |
| Structural validity | 72/72 |
| Useful question text only | 67/72 |
| Semantic correctness including global scope | 66/72 |
| Complete condition bindings | 65/72 |
| Combined pass | 62/72 |
| Combined pass by repeat | 22/24, 20/24, 20/24 |
| Requests passing all three repeats | 19/24 |
| Same question meaning across repeats | 23/24 |
| Same ledger meaning across repeats | 22/24 |
| Exactly equal canonical JSON across repeats | 2/24 |

Stability is not correctness: two requests failed consistently. The T18 scope defect affects metadata, while its question text remains useful. T17 retains a logically meaningful inner support condition, but misses the explicit outer source gate required by the contract.

## Failures retained

- T03, repeats 2–3: asks how to invoke an API if single-field use is supported, but omits asking whether that support exists.
- T11, all repeats: a message lookup loses the shared corrected dependency `props.required from model.needsReceipt` in both question and ledger.
- T17, all repeats: a nested message lookup omits the outer `If so` eligibility excerpt and binding; inner conditional meaning remains useful.
- T18, repeat 3: uncertain version `6.3.x or 6.4.x` remains in text and ledger but becomes null in global metadata.
- T21, repeat 2: custom-rule exclusion remains in the text but disappears from the ledger.

## Independent review and decision

[Review instance 1](REVIEW-1.md) found no actionable harness defect and rated the evidence Ready **as a record of a failed experiment gate**, not approval of v5 for deployment. All seven unchanged v5 tests and eight unchanged aggregation tests passed. Optional hints preserve the core plan across all72 outputs. All33 inherited manifests/38,342 hash entries verified; entries can overlap. Sealed evaluation was never interpreted.

Accept all five findings. Keep v5 frozen and retain this panel as diagnostic evidence. Further exact-wording tuning is not supported by these results: semantic stability is already high, while condition coverage and scope transfer remain the issue. A bounded next proposal would test explicit per-request obligation auditing in a new candidate, including support checks, inherited conditions and global scope consistency, using separately authored development cases and fresh confirmation. That proposal is not implemented here; no automatic completeness guarantee is claimed.

This is a synthetic development test using isolated native-agent contexts with uncontrolled model revision, temperature and seed. Repeats are correlated. There is no current comparator arm, deployed API qualification, latency measurement, retrieval test or final-answer test. The sealed evaluation stays closed. All existing candidates, baselines and data/DB remain unchanged.

## Evidence

- Frozen design and inputs: PROTOCOL.md, data-review.md, data/cases.json, data/rubric.json, test-output/input-freeze.json.
- Nine original batches: test-output/b{1,2,3}-r{1,2,3}-raw.json; hashes in raw-freeze.json.
- Complete records and scores: test-output/records.json, semantic-review.json, stability-review.json, aggregate.json.
- Protection snapshots: test-output/protected-before.json and protected-after.json.
- Final artifact hashes: test-output/final-freeze.json.

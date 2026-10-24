# V10 explicit unknown-scope results

The targeted unknown-scope ledger omission did not recur: Q19 includes unknown-adapter scope in both questions and ledger in3/3 reruns, and independent review found all active explicit-unknown scope statements covered across the fresh panel. The full candidate gate nevertheless fails. Retain v10 as experimental evidence, not a promoted replacement.

24 fresh requests in3batches8 repeated3, plus4 unchanged diagnostics repeated3:84 first responses. No retries, output repairs, resampling or post-freeze tuning. All prior candidates/baselines/data/DB unchanged; evaluation sealed.

| Primary frozen-rubric measure | Fresh | Diagnostics |
| --- | --- | --- |
| Question text | 69/72 | 12/12 visible-text |
| Semantic including globals | 68/72 | 12/12 visible-text |
| Condition bindings | 69/72 | 12/12 visible-text |
| Per-request structural validity | 72/72 | 11/12 |
| Joint usable | 68/72 | 11/12 |
| Requests passing all3 repeats | 22/24 | 3/4 |
| Joint by repeat | 23,23,22 of24 | 4,3,4 of4 |

Diagnostic semantic counts include manual inspection of one invalid serialized response; they are not usable-plan counts. Combined primary joint79/84. Whole-packet transport accepts11/12 files. Counting all4 slots in the invalid packet as unusable gives diagnostic8/12, combined76/84. Exact original row slicing and both accounting views are documented in transport-observation.md; no malformed text was repaired. Slice handling is post-observation, not preregistered.

## What remains

**U22, three repeats:** the second question carries the same field's read-only presentation without disabling its control into the return-to-editability question. Frozen rubric expected that restriction only on configuration. Reviewer keeps these primary failures, but agrees a supplied-history reading is defensible under inherited v9 rules: no invented only-if or causal relationship appears. This is not an unambiguous behavioral regression. Parent accepts primary rubric scoring and disputes treating the attachment as a proven misunderstanding; source/contract interpretation needs precision before another experiment.

**U10, repeat3:** version metadata is the string "unknown" instead of rubric-required null. Unknown version is correctly preserved in questions and ledger, with all nested gates. Contract language preserving uncertain version strings leaves ambiguity for wholly unknown versions. This is a normalization mismatch, not missing scope or a guessed release.

**F23, repeat2:** a literal backslash-n outside a JSON string makes the saved response invalid. Visible questions/ledger pass manual review, but structure and usability fail. The entire diagnostic packet is invalid as a whole. Original bytes retained; exact neighboring row slices can parse independently but cannot make the packet valid.

Accepting the two semantic interpretations as a clearly labeled sensitivity produces fresh72/72 and combined83/84 per-request (80/84 whole-packet). These figures do not replace frozen grades, and the full gate still fails. The fresh score must not be presented as evidence that v10 is causally worse or better than v9 on different requests.

## Repeatability and implementation

Reviewer finds requested question/ledger meaning equivalent across all28 cases, including stable disputed U22 attachment. F23 stability is visible-text only; U10 global normalization differs null/null/unknown. Requiring normalization-inclusive equivalence gives27/28. Requiring valid structured outputs on every repeat excludes F23 as well. Exact canonical JSON identical only for2/28 empty controls. Stable failure is still failure.

Only contract heading and a focused explicit-unknown-scope section changed from v9; same v3 schema/transport, no deterministic omission checker or repair, no new dependencies/training/downstream integration. Eight v10 transport tests, seven v9 regressions and eight scorer tests independently pass (23/23). TDD red was missing module; semantic behavior is established by generation/review, not that unit-test failure. Prompt grows from19,532 to20,999bytes; latency/cost unmeasured.

One fresh-context independent review inspected all84 source/output pairs, tests, packets, exact slice reconstruction and preservation. Verdict Not ready for full gate; evidence ready for reporting. No replacement review to seek a different verdict. See REVIEW-1.md, REVIEW-RESPONSE.md, test-output/aggregate.json and all-questions.md.

## Decision

The unknown-scope target is supported by this bounded trial. Remaining work is precise scope normalization/attachment policy and reliable serialized delivery, not more unknown-scope training or a broader redesign. No additional implementation or candidate promotion in this trial. Any future experiment should specify wholly-unknown version normalization explicitly, distinguish historical setup from restrictions on a new operation using unambiguous contrasts, and test structured delivery prospectively. Do not use those changes to rewrite this evidence.

Policy-informed synthetic development; native model revision, seed and temperature uncontrolled; repeats correlated. No production, sealed-evaluation, latency, retrieval, final-answer or contemporaneous baseline superiority claim. Hashes establish preserved bytes, not unseen attempt history or independent chronology. Protected snapshot38 manifests/38,625 overlapping entries remains unchanged. Only new refinement_v10 artifacts written.

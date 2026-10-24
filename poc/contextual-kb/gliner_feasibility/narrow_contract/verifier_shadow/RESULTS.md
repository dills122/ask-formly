# Frozen verifier diagnostic results

Decision: retain the frozen extractors; do not enable the current verifier as a role-correction stage or continue training this unchanged design. This development diagnostic found no successful wrong-role repair opportunities and found verifier disagreements that would damage correct extraction if substituted. No output substitution occurred.

## Preparation and review

The annotation rule distinguishes explicit configuration-member references from component concepts and model-address prose. For example, a named/registered type does not itself make the prose word `type` an API mention; `model key` denotes an address concept, whereas configuration shorthand `key 'x'` refers to the member. Six supplied training occurrences and six development occurrences of `type` were adjudicated as concept negatives in separate artifacts. Training data and models were not changed. The original development inventory remains intact.

The separate training ambiguity audit covers all 195 whole-word occurrences of type/key/model/wrappers/expressions across 242 training rows. It is not a full annotation certification, and unsupervised occurrences are not assumed negative.

The new 30-question development panel contains 12 contrast pairs across six families and six controls, with 30 gold mentions across all six roles, 12 semantic negatives and six malformed-span negatives. No normalized question duplicates occur against the 272 prior training/development questions; thematic and template overlap is disclosed in provenance. The adjudicated legacy panel retains all 30 original question texts, IDs, order and probe coordinates, with 65 gold and 36 negative probes instead of 71 gold and 30 negatives.

[Independent review](REVIEW-1.md) accepted the rule, inspected both inventories and harness, and issued a hash-bound Ready receipt before inference. Eleven tests passed. Native collate-only verification aligned all 149 probes across the new and adjudicated panels, including all 95 gold spans, without encoder inference. The receipt binds 17 preparation artifacts.

## Execution

Both seed 1701 and seed 1702 frozen role/boundary extractors and their frozen update-124 verifier adapters ran on all three panels: new development, legacy original, and legacy adjudicated. Operational verifier scoring used every unique extractor-emitted span; supplied oracle probes were scored separately. Diagnostic boundary/role thresholds stayed fixed at 0.5/0.5; these are not selected serving thresholds. No optimizer, training, output repairs or sealed evaluation was used.

### New development results

These counts measure mentions, not questions answered correctly.

| Metric | Seed 1701 | Seed 1702 |
| --- | ---: | ---: |
| Correct baseline mentions / 30 gold | 28 | 29 |
| Extra baseline mentions | 1 | 0 |
| Missing gold spans | 2 | 1 |
| Correct baseline mentions endorsed by verifier | 19 | 20 |
| Correct baseline mentions given a wrong role by verifier | 4 | 4 |
| Correct baseline mentions with verifier abstention | 5 | 5 |
| Same-span cross-role conflict groups | 1 | 0 |
| Successful wrong-role repair opportunities | 0 | 0 |
| Oracle gold accepted with correct role | 20/30 | 20/30 |
| Oracle malformed spans rejected | 6/6 | 6/6 |
| Oracle semantic negatives rejected | 4/12 | 3/12 |

No operational or oracle span was unsupported. Both verifiers misclassified literal values `'cedar-calendar'` and `"iris-border"` as registration names, and two opaque expression values as API references. Both abstained on five otherwise correct mentions. Abstention is not itself a lost extraction: a retain-original policy could preserve it. Likewise the four wrong endorsements are potential harm, not applied edits.

The actual conflict was seed 1701 emitting both `value` and `registration_name` for `"wrappers"` in SDEV-008. The value role was correct, but the verifier abstained instead of resolving the conflict. Seed 1702 emitted only the correct value. Conflicts are therefore possible with native flat decoding, but this panel supplies no demonstrated verifier repair benefit.

Boundary rejection on six malformed probes did not establish semantic discrimination: only four or three of the twelve semantic negatives were rejected. The distinction between syntax-like text and its role in context remains the weakness.

### Legacy replay, kept separate

| Panel and metric | Seed 1701 | Seed 1702 |
| --- | ---: | ---: |
| Original correct baseline / 71 gold | 60 | 56 |
| Original baseline extras | 1 | 2 |
| Original oracle gold accepted / 71 | 59 | 62 |
| Original negatives rejected / 30 | 30 | 29 |
| Adjudicated correct baseline / 65 gold | 57 | 56 |
| Adjudicated baseline extras | 4 | 2 |
| Adjudicated oracle gold accepted / 65 | 58 | 58 |
| Adjudicated negatives rejected / 36 | 30 | 29 |

Neither legacy panel has eligible conflict groups or successful wrong-role repairs. Neither verifier rejects any of the six newly adjudicated concept-negative occurrences at the boundary gate. Revised denominators are annotation changes, not model improvement. Original predictions and oracle probabilities exactly replay the previous calibration cache; the previous failed calibration result is not rewritten as a pass.

## Verification, preservation and limits

The run completed successfully with before/after preservation checks: 37,925 protected manifest entries unchanged, plus 54 prior full-run, 85 sealed-preparation and five diagnosis bindings verified. Both baselines, A, v2 and the knowledge/data/DB layer remain unchanged. Sealed evaluation content was not inspected or used for predictions; preservation hashing does not open it for evaluation.

Evidence is in `test-output/frozen-shadow-v1/` (raw outputs, per-mention score ledgers, costs, completion and preservation records). A second standard-library arithmetic calculation in `test-output/independent-arithmetic-check.json` reproduced counts and legacy replay equality. That calculation is author verification, not an independent results review; the independent review was the pre-execution preparation/harness review.

This is a small controlled development contrast panel, not held-out generalization evidence or final-answer accuracy. Six malformed probes cannot establish broad rejection reliability. Recorded single-pass costs are not a latency qualification. No thresholds or labels were tuned after observing these results.

The practical next decision is to leave this verifier out of the active design. Any future role-training experiment needs a different stated objective and evidence of useful corrections on actual extractor errors while preserving correct mentions; another unchanged training run is not justified by this result. Evaluation remains sealed.

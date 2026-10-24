# V8 results: targeted event and follow-up fixes

V8 retains the v7 ledger policy and schema. It adds checks for events inside capability noun phrases and assigns scenario, method restriction, eligibility and scope separately. A shared method restriction cannot by itself make a follow-up conditional; a genuine conditional descendant still retains its gates. The implementation remains a prompt candidate using unchanged same-POC v3 transport, with no data/DB or downstream change.

## Test and result

24 fresh requests in three batches of eight, each run three times: 72 fresh responses. Three unchanged v7 diagnostics (F04, F05 and F23) also run three times: nine diagnostic responses. All 81 first submissions retained; no output repair, feedback, retry, resampling or tuning after freeze.

| Measure | Fresh | Diagnostics |
| --- | ---: | ---: |
| Structural validity | 71/72 | 9/9 |
| Useful text and semantic scope | 69/72 | 9/9 |
| Complete grounded bindings | 68/72 | 9/9 |
| Full contract pass | 68/72 | 9/9 |
| Full pass by repeat | 22/24, 23/24, 23/24 | 3/3, 3/3, 3/3 |
| Requests passing all three repeats | 22/24 | 3/3 |
| Question-meaning stability | 24/24 | 3/3 |
| Ledger source/attachment stability | 23/24 | 3/3 |
| Exact canonical JSON equality | 2/24 | 0/3 |

The targeted diagnostic gate passes, including every repeat of F23, the previous event-binding and independent-follow-up failure. Diagnostic inputs and grading criteria are unchanged from v7. The fresh full gate does not pass, even under the alternative interpretation below. Exact wording equality is not required; stable errors remain failures.

## One definite failure and one interpretation-sensitive case

**C12 run 1: definite exact-source failure.** Its ledger uses `a wrapper can be reused`; the source says `can a wrapper be reused` and `If yes`. The question meaning is useful, but the unchanged validator correctly rejects the non-source excerpt. This invalid slot stays in every denominator. Optional hints cannot bypass validation.

**C14, all three runs: scope-sensitive finding.** The user asks about late options arrival, then asks what happens when “that select” is disabled. Generated questions describe the disabled select as one “whose options arrive after the field has been initialized,” and bind that context to both questions. The reviewer judged this an added prerequisite under the frozen rubric. However, “that select” also permits a natural shared-context reading. The pre-generation data review allowed harmless history but not a requirement for disabled behavior; the reviewer found the wording restrictive. This is explicitly an interpretive judgment, not an unambiguous meaning failure.

**Sensitivity only:** accepting C14 as harmless shared context gives 72/72 useful text and 71/72 full passes, with 23/24 requests passing all three repeats. The full gate still fails because of C12. Primary grades remain 68/72 and 22/24; no rubric or output was rewritten.

## Review and decision

[Independent review 1](REVIEW-1.md) inspected all 81 outputs, reconstructed every slot, checked hints and preservation, and ran all 20 required tests: six v8, six frozen v7 and eight aggregation tests. All passed. It also ran eight older metric tests, which passed but do not replace the required suites. For all 80 structurally valid outputs, hints preserve core plans; the invalid C12 output consistently rejects before hint handling.

Verdict: **evidence ready; candidate not ready to adopt as meeting the full gate**. The targeted fixes worked in this diagnostic replay, and no additional clear event-binding or independent-gate defect was identified on the fresh panel. Exact source selection remains a definite failure mode. Ambiguous same-subject context needs clearer prospective grading or explicit uncertainty handling. Keep v8 as an experimental candidate; do not claim universal reliability or repair these frozen outputs.

This is transport TDD plus semantic generation testing: the initial unit failure was the missing new candidate module, then six selector/transport tests passed. Those tests do not prove prompting is correct. Actual generated outputs and independent judgments supply the semantic evidence.

## Preservation and limits

All 36 inherited manifests, covering 38,506 hash entries with possible overlaps, match before and after. Sealed evaluation payloads were byte-hashed only, never interpreted. All new writes stay inside refinement_v8. Existing candidates, baselines, extractors, knowledge, DB, retrieval and answer layers remain unchanged. No staging, commits or publication.

The prompt is 16,098 UTF-8 bytes versus 13,979 for v7; no latency or cost measurement. Native model revision, temperature and seed are uncontrolled. Repeated contexts and targeted synthetic requests are correlated and do not establish production reliability. There is no contemporary comparator arm, so fresh percentages cannot establish causal improvement or regression against older panels. No retrieval utility or final-answer accuracy was tested. Hashes establish content preservation, not unseen generation history.

## Evidence

- Candidate: CONTRACT.md, CHANGE.md, candidate.py, test_candidate.py.
- Design: PROTOCOL.md, AUTHOR.md, data-review.md; original author rubric retained, C06 setup addition recorded before generation.
- Inputs: data/fresh-cases.json, fresh-rubric.json, diagnostic-cases.json, diagnostic-rubric.json and four full contract/request packets.
- Outputs and grades: test-output/records.json, semantic-review.json, stability-review.json, aggregate.json and 12 original raw files.
- Review: REVIEW-1-preliminary.md, REVIEW-1.md, REVIEW-RESPONSE.md.
- Integrity: test-output/candidate-freeze.json, input-freeze.json, raw-freeze.json, protected-before.json, protected-after.json and final-freeze.json.

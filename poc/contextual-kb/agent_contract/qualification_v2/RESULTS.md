# Qualification2 results

**142/144 fresh responses passed the complete contract (98.6%); all 15 diagnostic responses passed. The fixed experimental acceptance gate nevertheless failed on two material intent errors.** The delivery harness worked on all 21 first attempts, and the prior ledger omissions were absent from their repeated diagnostics. No tuning, repair, retry, resampling or output salvage occurred during qualification.

## Changes made in this new candidate

- Fixed parent-owned transport replaces generator-written producer imports. Workers submit one literal response list. runner.py uses ast.literal_eval and standard JSON serialization, never generated code execution, semantic filtering or repair. It refuses output overwrite.
- execution.py reserves each attempt exclusively before launching the runner, records first-save source/packet/runner hashes, captures stdout/stderr/completion, and enforces integrity plus whole-packet ID/count/order validity after saving. A failed attempt cannot be retried at the same path. The fixed schedule and independent audit also constrain procedural resampling.
- The inherited question contract and settled interpretation policy remain unchanged except an appended ledger completion audit for supplied stages, methods/channels and explicit lookup restrictions, including no-substitution. The structural validator still cannot prove semantic completeness; no custom regex completion or training was introduced.

All implementation and evidence live in qualification_v2. Prior candidates, both baselines, A/v2, knowledge/data/DB and downstream remain unchanged. Sealed evaluation was not opened; byte hashes only.

## Fixed test and scores

Two independent authors supplied48 fresh synthetic development requests, six groups of eight. Parent source/rubric review resolved three issues before freezing: N43's missing no-substitution condition, and optional same-field attachment allowances for N28/N38. Original submissions remain intact. Five exposed diagnostics (K19,K23,K46,V04,V24) are reported separately. All 53 requests ran three times in isolated contexts,21 packets/159 scheduledresponses. No prompt/rubric changes after freeze.

| Measure | Observed | Fixed requirement |
|---|---:|---:|
| Fresh structural validity | 144/144 | 144/144 |
| Fresh text / semantic / binding / joint | 142/144 each | Joint at least137/144 |
| Fresh cases joint-usable all three times | 47/48 | At least44/48 |
| Fresh meaning stability | 47/48 | At least44/48 |
| Fresh mandatory-ledger stability | 47/48 | Report separately |
| Observed material intent errors | 2 | Zero |
| Diagnostic joint | 15/15 | 15/15 |
| Diagnostic meaning / ledger stability | 5/5 each | Report separately |

Group joint scores: basic discovery24/24; scope24/24; states/events22/24; expressions/dependencies24/24; support/conditions24/24; mixed/literals24/24. Every group meets22/24 minimum. Fresh per-repeat joint:47/48,47/48,48/48. Across both panels157/159 joint. Exact JSON equality:2/48 fresh and 0/5 diagnostics; meaning consistency is stronger than exact wording consistency.

Every preregistered gate passes except zero observed material intent errors. Experimental qualification and strict-perfect gates are both false. No candidate was promoted or integrated.

## What failed and what improved

N21 asks how to observe a field becoming invalid without polling, then what information is available to **the observer** at that transition. Runs 1 and 2 preserve the no-polling restriction only in the first question. The second asks about an unspecified observer, and its ledger likewise omits the method restriction. Run 3 retains it on both questions. The frozen rubric required both attachments before generation; no interpretation rule was added after seeing results.

These are two instances of one remaining failure pattern: a follow-up referring to the just-requested observer loses that observer's method restriction when converted to a standalone lookup. It is a question-meaning and ledger failure, not merely bookkeeping. Actual downstream answer impact was not measured. See FOLLOWUP-CONDITION-FINDING.md and independent REVIEW-3.md.

All three prior omission cases now retain initialization, model-update method and exact-name no-substitution restriction in all three diagnostics. V04/V24 also pass all repeats under the unchanged settled interpretation policy. This supports those targeted corrections on exposed cases, not universal elimination of omissions.

The previous generated-import mechanism is removed. All 21 fixed-runner executions returned0, all 159 outputs passed structural validation, and all saved JSON bytes equal standard serialization of the original literal objects. Fresh questions differ from qualification 1, so the numerical improvement is descriptive evidence across experiments, not a controlled causal baseline comparison.

## Verification and review

TDD: missing runner/selector failed first, then 14 tests passed; execution guard tests failed before implementation; integrity-load test failed before addition; final 20 newtests passed. Independent review also reran8 frozen qualification 1 regressions and 8 scorer tests:36 total passing. CLI tests run from unrelated working directories and verify overwrite/retry rejection, nonexecution of generated expressions, malformed/short/duplicate/wrong-ID batch failure, integrity mismatches and preservation of semantically defective objects.

Review 1 identified a procedural whole-packet/first-save enforcement gap before any generation. Parent accepted it and added the tested execution guard. Review 2 found Ready for freeze/generation. Review 3 independently read all 159 source/output pairs and 53 triplets, verified artifacts/tests and returned Not ready for experimental advancement because of N21. All three instances are complete; no replacement review or further tuning was started.

Candidate/input/three-round/raw manifests verified. Forty-one inherited protected manifests cover 38,869 overlapping entries and match before/after. Original literals, first-save receipts and outputs remain frozen. These hashes establish saved bytes, not unseen chronology or adversarially immutable execution history.

## Decision and limits

The requested harness and targeted ledger improvements were implemented and tested. Most of the new fixed qualification holds up, with one concrete residual follow-up-context failure. Keep this candidate and evidence as a promising experimental result; it has not passed the agreed acceptance gate. A future narrow change would need to preserve method restrictions across reference-linked follow-ups while still keeping genuinely independent operations and local exclusions separate. No new candidate or experiment is authorized by this report alone.

Cases are synthetic and policy-informed; fresh authorship is not conceptual disjointness from all past library questions. Native model revision, temperature and seed were uncontrolled, and repeats are correlated. This is not sealed evaluation, production or deployed-API delivery qualification. No retrieval, final-answer accuracy, latency/cost or universal Formly compatibility claim follows.

Machine metrics: test-output/results.json. Every request and primary response: test-output/all-questions.md. Individual judgments: test-output/semantic-review.json and stability-review.json. Final independent findings: REVIEW-3.md.

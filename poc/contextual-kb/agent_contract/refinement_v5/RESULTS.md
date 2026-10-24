# v5 conditional-follow-up and event-history results

## Outcome

v5 passes the complete predeclared development-panel gate: all16 requests pass useful question text and complete ledger handling in all3 repeats. Independent review is Ready, with no actionable findings. This is a positive bounded development result, not a production or universal-determinism guarantee.

## Measurements

| Measure | Result |
| --- | --- |
| Fresh requests | 12, each repeated3times:36 responses |
| Exposed diagnostic requests | 4, each repeated3times:12 responses |
| Total batches/runs/responses | 2 batches of8,3 runs each,48 responses |
| Useful question text | 48/48 |
| Complete ledger compliance | 48/48 |
| Fresh semantic/ledger passes | 36/36 each |
| Diagnostic semantic/ledger passes | 12/12 each |
| All-three passing requests | 16/16 |
| Equivalent question meaning across repeats | 16/16 |
| Equivalent ledger meaning/attachment across repeats | 16/16 |
| Identical canonical JSON across repeats | 1/16 |
| Generated question/binding occurrences | 75 /134 |
| v5 tests and unchanged v4 tests | 7/7 each |

## What changed and what held up

- Conditional-follow-up eligibility is now an explicit ledger category. A meaningful source excerpt must appear in both the dependent question and its binding, independently of any no-substitution exclusion. Existence/support checks remain ungated.
- Earlier-event history is distinguished from the outcome being requested. Same-field prior history may be included without turning a show-outcome question into a hide-outcome question. Explicit earlier prerequisites remain mandatory. Unrelated field conditions and local restrictions must not be imported.
- G01/G02 repair the prior missing eligibility bindings in all6 diagnostic responses while retaining the original exclusions. Fresh N01–N03 also handle only-if, unless and support-gated observation correctly in all9 responses.
- G03 and N06 preserve return-transition meaning without requiring redundant history entries. N05 retains its explicit mandatory preceding event. N07 keeps different-field scenarios separate. G04 retains its controlling dependency.
- New code only selects the v5 prompt. Same POC v3 schema, structural validator, strict parser and advisory-hint handling remain unchanged. No detector, postprocessor, retry loop, training, retrieval or DB changes.

## Independent boundary judgments

The reviewer read all48 outputs, including questions, reasons, scope and every ledger entry, and checked the frozen rules/rubrics. N02 runs1/2 include a redundant support-independence binding; the predeclared policy permits grounded interpretation restrictions and does not require a minimal ledger. This does not invent a scenario or self-gate the support lookup. N07 run1 generalizes custom field labels while preserving the two independent library scenarios; those labels were not supplied configuration values. Optional history and equivalent excerpt segmentation were judged under the v5 policy fixed before generation, not the old v4 ambiguity. No posthoc rubric changes or sensitivity exception was needed to pass.

The independent reviewer verified raw reconstruction, every slot, input/raw hashes, all32 prior manifests, both test suites, prompt sections and optional-hint isolation. Findings/claims are retained in REVIEW-1.md and row-level grading files. No fixes or replacement review followed.

## Decision

Use v5 as the candidate for the next question-layer development step. This panel no longer shows the conditional-follow-up or preceding-event problems that motivated it. Keep older candidates/evidence frozen; no deployment or production integration was performed. Before relying on a particular production model/API, qualify that execution path and its latency separately. The ledger remains an audit/advisory record, not an authoritative retrieval filter or mechanical completeness proof. More extractor training is not indicated by these results.

## Method, limits and costs

12 fresh requests were independently authored from scope and declared ledger policy without seeing the candidate prompt or prior outputs. Four old cases are explicitly exposed diagnostics, with new v5 rules fixed before scoring. Two full-contract request packets were each generated3times in separate fresh native-agent contexts. Every first-submitted output was retained; no feedback, repairs, resampling or same-panel tuning. Raw bytes frozen before independent grading. Artifacts support reproducible grading/preservation; absence of unseen attempts and generation isolation are orchestration provenance, not something hashes alone prove.

This is synthetic development evidence with correlated repeats and shared context within each8-request batch. Native provider revision,temperature and seed were uncontrolled; fresh-context roles are not independent model vendors. There was no new v4 comparison arm, causal accuracy comparison, real user-traffic sample, retrieval/answer test, sealed qualification or latency benchmark. Semantic consistency is not identical JSON and three successful repeats do not prove universal determinism. Structural validation still accepts omitted undeclared constraints; a unit test explicitly preserves this limitation.

Prompt UTF-8 size grew from10,843 bytes in v4 to13,491 in v5 (about24%). Latency/token-price impact was not measured. Derivation and Output sections remain unchanged apart from the version heading; only ledger instructions were expanded.

## Preservation

All new work is isolated in refinement_v5. All existing candidates, both extractor baselines,A,v2,v3,v4,data/DB and downstream code remain unchanged. Evaluation stayed sealed: byte hashing only, no case inspection. Protection covers32 prior manifests and38,295 hash entries (overlap possible), plus15 frozen current inputs and6 raw output files. Final audit matches preflight.

## Artifacts

- [Independent review](REVIEW-1.md)
- [Ledger rules](LEDGER-RULES.md)
- [Full candidate contract](CONTRACT.md)
- [All requests and repeated question texts](test-output/all-questions.md)
- [Semantic grades](test-output/semantic-review.json)
- [Question/ledger stability grades](test-output/stability-review.json)
- [Aggregate metrics](test-output/aggregate.json)
- [Protocol](PROTOCOL.md)

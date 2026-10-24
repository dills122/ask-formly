# Candidate v3 results

Completed 2026-10-23. **Independent review: Ready for this bounded candidate experiment.** V3 adds auditable shared-condition assignments and optional advisory role hints. All local gates passed; no baseline was replaced or promoted. Both fresh v2 and v3 runs passed13/13 common semantic cases, so this trial does not demonstrate a comparative accuracy improvement.

## Implemented behavior

`CONTRACT.md` retains v2 derivation rules and adds a pre-output audit of active shared/local conditions and explicit corrections. `condition_bindings` maps meaningful verbatim source excerpts to zero-based question indices. The validator rejects a declared condition missing from any assigned question and rejects ungrounded excerpts, nonexistent/duplicate targets and duplicate bindings. Standalone question text must carry the condition; reasons/metadata cannot substitute for it.

This check guarantees only declared source bindings. A generator can still omit a condition from the ledger or assign it to the wrong question; semantic coverage and attachment are assessed separately. No mechanical algorithm is claimed to discover all user conditions. Source excerpts with pronouns may produce awkward text; the model must resolve the antecedent within the question without dropping the copied condition.

`candidate.build_plan` returns a deep-copied question plan and text-only `search_requests`, with optional role hints in a separate advisory envelope. Omitting hints is valid. Invalid indices/roles/slices and overlapping/duplicate hints produce explicit warnings and are ignored; they cannot invalidate an otherwise valid core plan. Structurally valid hints have `usable_as_filter: false` and never enter the text-only projection. Incorrect-but-valid role labels therefore cannot rewrite, suppress or filter queries within this candidate. This does not prevent an external consumer from violating the documented contract. Invalid core plans remain errors regardless of hints.

No models are trained or loaded by this component. It packages the request/instruction and validates the returned generation. Search strings are not executed. No retrieval, DB, application investigation, answering or serving integration was added.

## Tests and actual generation

An independent test author saw unchanged v2 and the exact historical H07 request, but no candidate implementation or outputs. The panel contains that known regression plus12 fresh development requests. Cases cover all-question sharing, local-only constraints, asymmetric versions/adapters, negation, exact literal pairings, corrections, retractions, ambiguous custom-component references, subset sharing and an empty no-library request. Parent inspected cases/rubrics before freezing inputs.

One isolated generation agent received unchanged v2 and the13requests; a separate fresh agent received v3 and the identical ordered requests. No rubric, other-arm outputs or author history was supplied. Each run shared context across13requests. Raw outputs were frozen before validation. No generation repair, retry, post-result prompt change or seed selection occurred. Exact provider model revision, sampling settings and seed were not controlled. This is a single development batch per arm, not a production per-request API test or repeatability experiment.

| Metric | Unchanged v2 control | V3 candidate |
| --- | ---: | ---: |
| Structural validation |13/13|13/13|
| Independent common-semantic assessment |13/13|13/13|
| Fresh development cases |12/12|12/12|
| Historical H07 request, newly generated |Pass|Pass|
| Focused questions generated |23|23|
| Candidate binding coverage, nonempty cases |Not applicable|12/12|
| Correctly assigned candidate bindings |Not applicable|45/45|
| Common semantic regressions |Reference|0|
| Mean compact JSON bytes/output |544.38|837.46|

The candidate keeps H07's selected-value-still-present condition in both questions. A unit regression also demonstrates that the saved earlier v2 omission fails when that condition is declared for both questions. Fresh control v2 passed H07 this time: neither result rewrites the earlier failure, and the current tie does not show that v3 reduces failure frequency. The new mechanism makes the declared assignment inspectable and mechanically enforceable.

Candidate size is about54%larger on this panel, primarily audit metadata plus some more literal wording. No retrieval effect, generation latency improvement or production cost estimate was measured.

## Optional-hint evidence

The first12 policy/transport tests failed for the absent candidate module, then passed after implementation. A saved-H07 declared-binding regression was added; final13tests pass. Tests cover shared-target omissions, source grounding, local-only scope, empty plans, invalid/duplicate indices, strict JSON duplicate keys, hint absence, wrong valid roles, corrupt payloads, offset/text mismatch, conflicts and core-plan failure isolation.

The replay uses120 actual saved annotation rows (60questions for each frozen extractor) from the prior entailment trial. Each was placed in a single-question synthetic envelope with empty condition bindings solely to test transport. Absent hints, present hints and injected malformed hints all preserved the full plan/query and scope. This does not qualify those empty-ledger envelopes as semantically complete new candidate plans or establish entity accuracy. Of294input hints,292survived structural/overlap checks; all retained hints stayed non-authoritative.

The independent reviewer reconstructed all120rows, verified all ledger values, and tested14additional JSON-compatible malformed/conflicting/Unicode variants. All preserve core plan and text-only query output. No frozen extractor inference or weight changes were necessary for this transport test.

## Independent review and preservation

Review instance1of3 completed; no actionable findings or further review required. The reviewer recorded preliminary findings before reading the author explanation, inspected all26outputs/46questions/45bindings against frozen rubrics, reran13tests, and independently reconstructed hint transport. Arm schemas/names were visible, so grading is independent but not blinded.

The reviewer verified77hash entries (11input,2raw-output,64prior-entailment). Parent separately traversed37,925inherited protected entries and additional prior manifests before/after; results exactly match, including all inputs. Do not conflate the reviewer's77entry check with the parent's full preservation traversal. A,v2,both frozen extractors,data/DB and prior evidence remain unchanged. Evaluation contents stayed sealed; only preservation hashes were verified. No staging, commits or publication.

## Decision and limits

Use v3 as a separate experimental candidate when explicit condition audit and optional hints are desired. Do not claim it outperforms v2, guarantees semantic completeness, improves retrieval or produces accurate final answers. This run meets the planned local gate: H07 is preserved, no fresh semantic regression, all structural/declared-binding checks pass, all reviewed applicable bindings are complete, and hints cannot affect text-only projection in the tested scope.

The remaining validation need is broader fresh/repeated evidence of condition discovery and attachment, especially with complex corrections and pronouns. That is a limitation, not permission to tune or rerun this now-exposed panel. No further experiment or baseline promotion was performed.

Evidence: `README.md`, `PROTOCOL.md`, `CONTRACT.md`, `candidate.py`, `test_candidate.py`, `data/`, `REVIEW-1.md`; `test-output/{input-freeze,raw-freeze,validation,semantic-review,hint-replay,reviewer-check,size-summary,protected-before,protected-after}.json`, raw output files and red/green test logs. `test-output/reviewer-check.py` reproduces the independent mechanical checks. All artifacts are frozen in final-freeze.json.

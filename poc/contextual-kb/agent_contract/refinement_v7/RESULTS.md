# v7 results: ledger clarification and paired construction

V7 clarifies the ledger prospectively and generates each condition's question text and index assignment together. Observed events, settings, dependencies, scope, exclusions and eligibility remain required conditions. Mere API/operation targets are not additional conditions. Prospective use after registration need not repeat obsolete unregistered state. Local usage limits must not narrow unrestricted support checks; explicitly restricted support retains them.

The clarification is saved in [LEDGER-RULES.md](LEDGER-RULES.md). Prior candidates, rubrics and scores remain unchanged. V7 preserves the existing three-field JSON, same-POC v3 structural/advisory transport and library-only scope. No downstream integration or DB change.

## Executed test and outcome

24 fresh requests in3batches of8, each repeated3times:72fresh responses. Six previous v6failure cases replayed3times:18diagnostic responses. All90first submissions retained without feedback, repairs, retries or tuning. Raw/input/candidate hashes frozen at checkpoints. The policy-informed author did not read previous requests/results or the fullv7prompt.

| Measure | Fresh | Diagnostics |
| --- | ---: | ---: |
| Structural validity | 72/72 | 18/18 |
| Useful question text | 71/72 | 18/18 |
| Meaning including global scope | 71/72 | 18/18 |
| Complete correctly attached bindings | 69/72 | 18/18 |
| Full contract pass | 69/72 | 18/18 |
| Full pass per repeat | 23/24,23/24,23/24 | 6/6,6/6,6/6 |
| Requests passing all3repeats | 23/24 | 6/6 |
| Question-meaning stability | 23/24 | 6/6 |
| Ledger-meaning stability | 23/24 | 6/6 |
| Exact canonical JSON equality | 2/24 | 0/6 |

The diagnostic gate passes. The full fresh gate narrowly fails: required24/24requests across all3repeats, observed23/24. Exact wording equality is not a requirement. All global scope metadata passed. The fresh panel includes paired restricted/unrestricted support, targets versus explicit execution limits, stage-specific setup, shareddependencies, observedtransitions and empty controls.

## Remaining failure

All failed fresh slots are **F23**, whose source requests restricted expression-change observation support/use, then an independent property-value read after the expression changes using the same method restriction.

- All3runs preserve observation meaning in question text but omit the observation-event binding for support/use. A post-change binding on the later read does not cover those earlier questions.
- Run3 additionally gates the independent property-value read on observation support. The source shares a restriction, not eligibility. Runs1/2 correctly keep the read independent.

These failures are retained. No ambiguous-rubric waiver or sensitivity adjustment is used. Paired text/index construction reduced neither requirement to a mechanical guarantee; undeclared omissions still pass structural validation.

## Independent review and decision

[Review1](REVIEW-1.md) read all90outputs and30sources/rubrics, checked reasons/scope/bindings, reconstructed allslots, audited preservation and ran20tests:6v7,6frozenv6,8scorer tests. All passed. Optional missing/malformed/valid/conflicting hints preserve all90core plans; valid-span trials apply to84nonempty outputs. The TDD red was missing newcandidate module; green proves selector/transport behavior, not semantic prompting.

Verdict: **evidence ready; candidate not ready for adoption against the declared full gate**. V7 is a promising experimental foundation, with the remaining observed failures concentrated in one request. Keep it frozen and retain the specific independent-followup/event-binding defect for any next authorized experiment. Do not claim universal condition preservation or production readiness.

N09/N14diagnostics use prospective target/stage clarifications, so their scores cannot all be credited to generation improvements. Prior tests stay unchanged. Fresh panels differ from v6 and no contemporary comparator exists: percentages do not establish a controlled model improvement.

## Preservation and limits

35inherited manifests covering38,447hash entries (overlap possible) match before/after. Sealed evaluation payloads byte-hashed only, never interpreted. All newwrites within refinement_v7; no staging/commits/publication. Existing candidates, baselines, extractors, authoreddata, DB and downstream code unchanged.

Prompt13,979UTF-8bytes versus17,485forv6. No measured latency or cost claim. Native modelrevision/temperature/seed uncontrolled; repeats correlated. Synthetic targeted development and separate-context review cannot establish production accuracy, retrieval utility or final-answer quality. File hashes prove retained contents, not unseen attempt history.

## Artifacts

- Policy/candidate: LEDGER-RULES.md, CONTRACT.md, candidate.py, test_candidate.py.
- Design/provenance: PROTOCOL.md, AUTHOR.md, data-review.md; originalauthorrubric retained, F06filterrelationship added beforefreshgeneration.
- Inputs: data/fresh-cases.json, fresh-rubric.json, diagnostic-cases.json, diagnostic-rubric.json and four batchpackets.
- Alloutputs/grades: test-output/records.json, semantic-review.json, stability-review.json, aggregate.json and12original rawfiles.
- Review: REVIEW-1-preliminary.md, REVIEW-1.md, REVIEW-RESPONSE.md.
- Integrity: test-output/candidate-freeze.json, input-freeze.json, raw-freeze.json, protected-before.json, protected-after.json, final-freeze.json.

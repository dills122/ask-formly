# Independent review
Review instance: 1 of 3

## Findings

No actionable correctness findings within the declared bounded grammar and strict-validation scope. The exact full-question match preserves case-sensitive ordered dotted paths and the dependency verb. Only question text is rewritten; the ledger, reasons, constraints and unrelated questions remain unchanged. The original validator runs after rewriting, so another missing bound condition, malformed schema or ungrounded binding still rejects. The planner returns raw decoded JSON, allowing this adapter to run before LookupService validates and initializes its backend.

Review target: new wording_candidate_v1 candidate.py, serve.py, replay.py, test_candidate.py and test_service.py, plus PLAN.md, on dirty main at c3091328f49d53de6b41a49c4fe5aa8f1c45e516. Other working-tree changes are excluded. Reviewed source hashes are retained in review-verification.json. Graph coverage for inspected POC dependencies was not_tracked; conclusions rely on direct source reads, not graph completeness. No implementation changes were made.

## Plan Review

The implementation matches the planned opt-in deterministic adapter, preserves strict-valid plans, uses existing source-grounded bindings, records detached original and rewritten text, and leaves the prior pipeline unchanged. Tests cover the stated grammar family, idempotence, non-mutation, semantic changes, other lost conditions, malformed inputs and service rejection before backend initialization. The 84-slot structural replay meets the stated parity criterion. The three repaired slots represent one distinct saved plan, not three independent successes.

The narrow scope is coherent: generic paraphrase equivalence, undeclared condition detection, model changes and answer qualification are excluded explicitly. Opt-in composition makes rollback simply selecting the prior launcher. No architectural pivot or further review instance is required for this reviewed state.

## Author-Claim Reconciliation

| Claim | Evidence | Status | Consequence |
| --- | --- | --- | --- |
| Bounded passive-to-active rewrite retains paths and relation | candidate.py CONFIGURATION and normalize; adversarial cases | Confirmed | Supports syntactic equivalence within this grammar |
| Original validation remains authoritative | refinement_v3/candidate.py validate/build_plan; service.py _lookup | Confirmed | Bound conditions and schema checks remain enforced |
| Raw planner output survives and normalization is audited | planner.py CodexPlanner; NormalizingPlanner; service test | Confirmed by source and injected service test | No new real hosted-generation claim |
| 81 unchanged plans and three copies of one F01 repaired | Independent in-memory replay; review-verification.json | Confirmed | Structural acceptance only |
| Old artifacts/models/DB/sealed evidence preserved | Original final-freeze verification and recursive protected snapshot equality | Confirmed at review time | Sealed bytes hashed only, not interpreted |
| Prior regression suites pass | Retained prior-repair, prior-mcp and prior-advisory logs | Confirmed as retained execution evidence | 11, 11 and 35 tests respectively; not independently rerun |
| No broad semantic/answer improvement claimed | PLAN.md and AUTHOR-EXPLANATION.md | Confirmed | Prior qualification remains unchanged |

## Verification Performed

- Executed `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/wording_candidate_v1 -p 'test_*.py'`: nine tests passed.
- Independently replayed all 84 exposed panel inputs in memory using normalize and original build_plan, checking non-mutation and strict-valid equality: 81 unchanged; F01-1, F01-2 and F01-3 repaired; one distinct repaired input.
- Eight additional rejection checks passed: extra declared subscription/readiness/reset conditions, identifier case changes, longer controller paths, newline/punctuation variants and inline comments.
- Verified retrieval_repair_v1/test-output/final-freeze.json and recursive snapshot equality against its protected-before.json before and after replay. No generation, training, database edits or semantic reads of sealed evaluation were performed.
- Inspected the later local native harness, summary and both result JSON files, verifying the stated availability, preservation, rewrite and expected fact-ID assertions. Did not rerun native extraction or invoke hosted services.
- Recorded REVIEW-PRELIMINARY.md before opening AUTHOR-EXPLANATION.md, then reconciled the explanation against inspected source and executed checks.

## Open Questions And Residual Risks

The original validator checks declared substrings, not semantic completeness: undeclared conditions and misleading surrounding text remain pre-existing limitations. Path grammar does not prove API existence. A strict-valid unsupported phrasing passes unchanged by design; unsupported phrasing that needs repair remains rejected. Inspected native_replay.py and retained native results for seeds 1701/1702 after the initial review: both report available advisory extraction, unchanged DB/model parameters, one audited rewrite and retrieval containing conditional-disabled-target. The harness uses the saved planner output and an explicit no-op selector. These are local integration diagnostics, not independent retrieval-relevance or final-answer grading. Reviewed runtime hashes still match. Hosted selector execution was reported unavailable because automatic approval review rejected external payload transfer; no hosted result is assumed. The service test uses an injected backend, so it does not establish full native/hosted end-to-end qualification.

Replay's distinct_repaired_outputs count is hardcoded, but independent comparison confirms the asserted value for the frozen inputs. Reusing that harness for different inputs would require computing the count or retaining this explicitly fixed scope.

## Verdict

**Ready** for the declared opt-in bounded wording candidate. This is neither a general paraphrase-equivalence verdict nor a new retrieval/answer-accuracy qualification. Existing failed qualification evidence must remain unchanged.

## Recommended Next Actions

Retain the independent artifacts with the candidate freeze. Report any subsequent native diagnostic separately with its selector limitations; do not elevate it into hosted or whole-answer evidence. Material changes to the reviewed runtime would require another independent pass within the existing maximum of three.

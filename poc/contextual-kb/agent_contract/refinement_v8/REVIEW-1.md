# Independent review of refinement_v8

Review instance: 1 of 3. Verdict: **Not ready for candidate adoption; evidence ready for honest reporting.**

Reviewed on dirty `main`, HEAD `c3091328f49d53de6b41a49c4fe5aa8f1c45e516`. Scope is only new `poc/contextual-kb/agent_contract/refinement_v8`; unrelated dirty work is excluded. Fresh reviewer context received the neutral bootstrap, not the implementation conversation. `REVIEW-1-preliminary.md` was saved before reading `AUTHOR-EXPLANATION.md` and `AUTHOR.md`. Applied independent-review and code-review-and-quality; graph coverage returned `not_tracked`, so code conclusions use direct source reads. Wrote only the four authorized reviewer artifacts. No source, input, raw output, old score or sealed payload edits; no sealed semantic reads, commits, subagents or replacement review.

## Findings

1. **P2 — C12 run 1 emits a non-source ledger excerpt.** `test-output/b2-r1-raw.json:48`, C12, `condition_bindings[2]`, declares `a wrapper can be reused`. Source C12 instead says `can a wrapper be reused` and `If yes`. The output question correctly asks contingent restricted attachment, so text and semantic meaning pass; binding/source provenance and structure fail. The unchanged validator rejects it with `condition not grounded in source`. Preserve this failed submission. A future candidate must select an actual meaningful source gate such as `If yes` while resolving its antecedent in question wording; repairing this saved output would invalidate the trial.

2. **P2 — C14 carries the late-options scenario into the separate disabled lookup in all three runs under the frozen rubric.** `test-output/b2-r1-raw.json:76`, `b2-r2-raw.json:76`, and `b2-r3-raw.json:76`, C14 question index 1, say `for a select whose options arrive after the field has been initialized`. The corresponding `options arrive after the field has been initialized` binding has indexes `[0, 1]`. Runs 1–2 continue `what happens to the select value when that select is disabled?`; run 3 says `what happens to its value when that select is disabled?`. This restrictive “for a select whose” qualification makes late arrival part of the disabled lookup's eligibility/scenario. It is not identified as optional history. The frozen rubric assigns that event only to the first lookup and expressly forbids making it a prerequisite for the disabled scenario. Text, semantics and bindings therefore fail for these three slots in the primary grade.

   **Interpretive limitation:** The original phrase `that select` can reasonably identify the same late-loading select; the source is less decisive than an explicitly independent request. `data-review.md`, written before generation, tolerates harmless historical mention on the second question *if it does not require that event for the disabled behavior*. That tolerance is real and was considered; the generated restrictive clause plus ledger attachment crosses it in this reviewer's judgment. This is a rubric-sensitive finding, not proof the only natural reading of the source is independent scenarios. See sensitivity counts below. A future trial should make intended scenario independence explicit or preserve genuine ambiguity; this review does not change the frozen rubric.

No additional actionable implementation findings. The prompt-only change and transport reuse are appropriately bounded. Source validation is deliberately not a completeness detector. Readability includes awkward exact-excerpt wording, but no subjective wording failure was assigned. No new dependencies, runtime integration, SQL, application execution, or security-sensitive flows were introduced. Performance and operational reliability were not measured.

## Plan Review

The scoped plan is appropriate: separate prompt candidate, transport regression checks, independently authored fresh cases, unchanged diagnostics, input/candidate freezes before generation, three retained repetitions, semantic review and separate aggregation. The diff preserves v7's rules apart from its title and the added v8 section. It addresses event-bearing phrases and per-category condition attachment without replacing the validator with an ungrounded semantic heuristic.

The data and outputs are complete for the planned experiment. Evidence supports reporting a targeted improvement on the retained diagnostics, not declaring the full fresh gate met. Parent-owned final reporting, final preservation audit and final evidence freeze remain to be completed after this review; this report does not mark those pending plan items done. No heavy architectural pivot is required by these bounded failures.

## Author-Claim Reconciliation

| Author claim | Evidence checked | Status and consequence |
| --- | --- | --- |
| v8 preserves v7 and adds event/gate guidance | Direct contract diff, CHANGE.md, candidate.py | Confirmed; title plus one added section. |
| Same schema and same-POC v3 transport | candidate imports; v3 candidate and base contract source | Confirmed. The validator cannot detect omitted or misattached semantic content. |
| 16,098 versus 13,979 prompt bytes | Direct UTF-8 byte lengths | Confirmed; no inference about token cost or latency. |
| Six v8, six v7, eight scorer regressions pass | Independently executed suites | Confirmed. Tests exercise transport and aggregation, not semantic success. |
| 24 fresh and three diagnostic cases, three repeats | Four packet comparisons, 12 strict raw JSON parses, records reconstruction | Confirmed: 81 unique scheduled slots, no dropped invalid slot. |
| Diagnostic requests/rubrics unchanged except scheduling | Direct comparison with v7 fresh cases/rubrics for F04/F05/F23, removing batch metadata | Confirmed. No old score was changed. |
| Candidate/input/raw checkpoints and protected prior evidence unchanged | SHA-256 verification and preservation snapshot | Confirmed for current contents; not proof of unseen attempt history. |
| Independent author read only permitted materials; no feedback/retry/repair | AUTHOR.md and bootstrap/protocol testimony; first-output files retained | File artifacts are consistent, but complete execution history cannot be independently established from these files. |
| C14 historical-context tolerance predates outputs | Frozen data-review.md and rubric | Confirmed. Does not automatically approve restrictive scenario wording; ambiguity and sensitivity reported explicitly. |
| Native model revision/temp/seed uncontrolled; repeats correlated | Protocol/author limitation | Retained as a limitation, not repaired by hashes or these scores. |

## Verification Performed

Executed from repository root with bytecode disabled:

- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v8 -p test_candidate.py`: 6/6 passed.
- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v7 -p test_candidate.py`: 6/6 passed.
- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/v3_stress -p test_assess.py`: 8/8 passed.
- Also ran the earlier refinement_v2 `test_metrics.py`: 8/8 passed; this extra suite is not substituted for the required v3_stress scorer tests.
- Imported v8 preservation under `python3 -B`: 36 manifest results, 38,506 overlapping hash entries, exactly equal to `protected-before.json`.
- Independently verified SHA-256 entries in candidate (9), input (18), raw (12), diagnostic raw (3), round 1 (3), and round 2 (3) freezes: no mismatches.
- Four packets contain the exact complete current contract and the exact assigned `{id, request}` records: three packets of eight fresh requests, one of three diagnostics. An initial inspection tested an absent `cases` key; checking the actual `requests` key confirmed all four matches.
- Strict duplicate-key/nonfinite-value-aware JSON parsing passed for all 12 raw files. Nine fresh files each contain eight assigned IDs; three diagnostic files each contain three. Reconstructed records equal `records.json` exactly: 81 unique `(id, run)` slots.
- All 81 outputs checked with missing, malformed, valid and conflicting optional hint forms: 80 valid outputs have identical core question plans/search projections; C12 run 1 consistently rejects before hint handling. Empty-output controls cannot have a valid question-index span; their supplied spans are correctly ignored. Input objects remain unchanged. This is invariance of acceptance/rejection and core projections, not a claim that 81 valid plans exist.
- Read all 27 source requests/rubrics and all 81 outputs, including every reason, question, scope and ledger. Independently recorded 81 semantic grades and 27 cross-run stability judgments. Global constraints pass in all slots, including faithful uncertain-version variants.
- Reused the unchanged v3_stress `summarize` on the independent grades to verify counts below.

### Scores

`semantic_pass` covers question meaning plus global scope; `text_pass` isolates question/reason meaning. `binding_pass` covers required conditions, source grounding and attachment. Joint success requires structure, semantics and binding success. All denominators include every scheduled slot.

| Panel | Structure | Text | Scope | Semantics | Bindings | Joint | All-three joint cases |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Fresh | 71/72 | 69/72 | 72/72 | 69/72 | 68/72 | 68/72 | 22/24 |
| Diagnostics | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 | 3/3 |

| Panel/run | Structure | Text/semantics | Bindings | Joint |
| --- | ---: | ---: | ---: | ---: |
| Fresh 1 | 23/24 | 23/24 | 22/24 | 22/24 |
| Fresh 2 | 24/24 | 23/24 | 23/24 | 23/24 |
| Fresh 3 | 24/24 | 23/24 | 23/24 | 23/24 |
| Diagnostic 1 | 3/3 | 3/3 | 3/3 | 3/3 |
| Diagnostic 2 | 3/3 | 3/3 | 3/3 | 3/3 |
| Diagnostic 3 | 3/3 | 3/3 | 3/3 | 3/3 |

Fresh all-three text/semantic cases: 23/24; scope: 24/24; binding: 22/24; structure: 23/24. Diagnostic all-three counts are 3/3 throughout. Fresh full gate **fails** (required 24/24 all three); diagnostic full gate **passes** (3/3 all three).

Question-meaning stability is 24/24 fresh and 3/3 diagnostic. Ledger source/attachment-meaning stability is 23/24 fresh and 3/3 diagnostic: C12 run 1 replaces conditional source provenance with a non-source affirmative fragment. C14 is a stable failure under the primary rubric interpretation. Exact full JSON equality is only 2/24 fresh cases (C08, C24) and 0/3 diagnostic; reason and harmless phrasing variations do not count as semantic instability.

**Sensitivity only — accepting C14 as harmless shared history:** fresh text/semantics would be 72/72, bindings/joint 71/72, all-three joint 23/24, and joint per repeat 23/24, 24/24, 24/24. The fresh full gate still fails because of definite C12 run 1. The saved primary grades are unchanged; this alternative does not silently waive a frozen criterion. Diagnostic counts are unchanged.

## Open Questions And Residual Risks

C14's source supports an alternative shared-context reading; the exact wording and sensitivity are preserved for adjudication. The other failures and full-gate outcome do not depend on that adjudication. Targeted synthetic development cases and correlated repeats cannot establish population reliability. Native provider revision, temperature and seed are uncontrolled. There is no contemporary comparator arm. No result here establishes retrieval quality, answer accuracy, production readiness, latency, cost or universal Formly compatibility. Hashes establish saved content and preservation, not unseen-attempt provenance.

## Verdict

**Not ready** for adopting v8 as meeting the declared full gate. The event-binding and independent-follow-up diagnostics are 9/9, but the fresh gate is not met even under the generous C14 interpretation. The experiment's evidence is complete and ready to be reported with these failures and limitations. This distinction is essential: a completed negative experiment is useful evidence, not an incomplete success.

## Recommended Next Actions

Parent should retain all first outputs and primary grades, finish separate-panel reporting and the final preservation/freeze, and explicitly retain the C14 sensitivity. Do not repair saved responses or rerun the unchanged candidate to replace failures. Any subsequent candidate needs a material change and a newly declared evaluation; another independent review is justified only after material remediation within the existing maximum of three instances. This reviewer does not dispatch another review or implement fixes.

# Independent review of v4 ledger candidate

Review instance: 1 of 3. Verdict: **Not ready** for the full candidate gate. Evidence/implementation verdict: **Ready** as a faithfully bounded experiment, with valid negative results; no new runtime-code defect found. No production approval implied.

## Findings

**P1 — Mandatory existence contingencies remain unaudited in all six applicable responses.** In `test-output/b1-r1-raw.json`, `b1-r2-raw.json` and `b1-r3-raw.json`, D12 Q1 and F01 Q1 preserve conditional existence in question meaning but omit its source-excerpt ledger binding. D12 binds only the exclusion; F01 binds version, hiding and exclusion. `data/diagnostic-rubric.json` D12 explicitly requires meaning contingent on existence; `data/fresh-rubric.json` F01 explicitly requires the same, with `If it exists` as an example. Neither paraphrased condition is present as a meaningful source excerpt in the question. This violates the source-to-output audit contract despite 48/48 structural validation. The smallest credible behavioral correction must preserve a meaningful source contingency excerpt in Q1 and bind it to Q1. Do not repair frozen responses or tune on this panel: retain failure and use a separately authorized new experiment if continued work is desired.

**P2 — F07 run 1 spreads a locally assigned transition binding.** `test-output/b2-r1-raw.json`, F07, binding `goes from visible to hidden` has indexes `[0,1]`. The frozen F07 rubric attaches the visible-to-hidden transition locally to model question 0; runs 2/3 use that attachment. The question text remains useful: question 1 asks the FormControl outcome when becoming visible again, not on hiding. Frozen `data-review.md` expressly permits prior hiding as transition context in this question. Thus there is a reasonable boundary ambiguity between mentioning prerequisite context and binding a local requested transition. The strict frozen attachment grade fails run 1; a permissive reading would pass it. This ambiguity cannot rescue the six clear contingency omissions and must not be used to rewrite the panel policy. Future policy should distinguish preceding-state context from the transition whose outcome is sought.

Observed totals: **48/48 useful question texts**, **41/48 strict ledger passes**, **13/16 cases passing both dimensions all three times**, **15/16 cases equivalent across repeats including ledger attachment**. Question meaning alone is equivalent for all 16 cases. If the F07 ambiguity were accepted, ledger results would be 42/48 and 14/16 cases; full gate still fails. D12's specific original missing-exclusion symptom is repaired **3/3**, but D12 overall is **0/3** ledger-complete. D16/D17/D22 pass **3/3** each. Fresh panel: **36/36 useful**, **32/36 strict ledger passes**, **10/12 fully passing cases**.

## Plan review

The bounded plan is implemented as declared: v4 changes the ledger instructions and prompt selector, reuses same-POC v3 transport, retains schema and advisory-hint behavior, freezes policy/cases before generation, and retains all 48 outputs. The seven new tests honestly distinguish declared-binding validation from semantic completeness. The old omission remains a passing structural negative fixture, correctly exposing the validator's limit. No detector, regex classification, retry repair, retrieval or data-layer mechanism is introduced.

The explicit all-cases/all-repeats gate is not met. The experiment should close with that negative result; no replacement review is warranted merely to obtain a favorable verdict. Final reporting/freezing was still pending in task_plan.md when reviewed and belongs to the initiating author after this review.

## Author-claim reconciliation

| Author claim | Evidence | Status / consequence |
| --- | --- | --- |
| Only ledger section and version heading change | Independently compared v3/v4 derivation prefixes and Output suffixes; LEDGER-RULES equals inserted section | Confirmed |
| Frozen v3 structural/advisory transport reused | Complete direct reads of candidate.py, v3 candidate.py and base contract.py | Confirmed; no semantic completeness guarantee |
| Seven v4 and thirteen v3 tests pass | Reviewer reran both suites | Confirmed |
| All raw responses retained and structurally checked | Reconstructed ordered records from six files; checked batches, identity and count | Confirmed 48/48 |
| Input policy explicitly adds F01 contingency before generation | Frozen rubric and data-review inspected; input freeze verified | Confirmed artifact content; temporal author/generator isolation remains process testimony |
| Prior artifacts unchanged | preserve.py executed successfully; protected-before summary comparison | Confirmed against byte manifests, not a semantic inspection of sealed material |
| No empirical production or v3 comparative gain claimed | Protocol and explanation | Appropriately bounded |
| Prompt improves known omission reliably enough for full gate | No such final claim made; independent grading | Specific exclusion repaired, full gate fails |

Review began from the neutral bootstrap in a separate fresh-context agent, with no implementation conversation inherited; preliminary concerns were recorded before AUTHOR-EXPLANATION.md. This is context separation, not vendor independence. No agents or extra review instances were created.

## Verification performed

- From refinement_v4: `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_candidate`: **7 passed**.
- From refinement_v3: same command: **13 passed**.
- From refinement_v4: `python3 -B preserve.py`: **31 manifest verifications passed** (30 inherited manifests plus prior stress final-freeze with 46 entries). Only byte hashing of protected payloads; no sealed case, database or weight semantic inspection.
- Independently recomputed SHA-256: input-freeze **15/15**, raw-freeze **6/6**, wave1-freeze **3/3**.
- Reconstructed records from all six raw batches, requiring expected ordered eight IDs per batch and 48 total; exact equality with saved records.
- Parsed/validated all 48 plans, checked absent, malformed, empty and valid advisory hints preserve question_plan/search_requests and do not mutate outputs. Supplied full-question role hints were intentionally semantically noisy to verify advisory isolation.
- Compared unchanged v3/v4 derivation and output sections and exact inserted LEDGER-RULES text; passed.
- Read every request, frozen rubric, question, reason, scope value and binding; grades recorded separately in `test-output/semantic-review.json` (48 rows) and `test-output/stability-review.json` (16 rows).
- Graph coverage queried for six relied-on Python files: untracked/no freshness evidence. Complete direct source reads provided verification; no graph completeness claim.
- Initial login shell emitted a startup parse warning before successful test/audit commands; Python suites and audit completed with exit 0. Subsequent independent checks used a non-login shell.

The root working tree is dirty and the POC untracked; unrelated edits are not reviewed or attributed to v4. No staging, commits, code fixes, baseline changes or output edits were performed. Only this review's four artifacts were written.

## Open questions and residual risks

F03's extra `as 'postalEntry'` binding is acceptable: it preserves an active registration-name relationship on registration/use, rather than inventing a restriction. The policy says a custom name is not automatically an extra condition; it does not prohibit every meaningful value pairing. F12's differing uncertainty strings are explicitly allowed. Combined scope/exclusion excerpts and duplicate-semantic polling excerpts are acceptable when grounded and correctly attached; exact word or binding counts are not gold.

The native generation setup has uncontrolled model revision/seed/temperature, shared context within each eight-case batch, and correlated repetitions. Frozen files demonstrate preservation and grading reproducibility, not independent reproduction of the original generation sessions. No answer accuracy, retrieval success, latency, universal prevention or production compatibility is established.

## Verdict

**Not ready** against the full candidate gate. **Ready** to archive the bounded implementation and evidence as a valid negative experiment. Useful text and repaired exclusions coexist with incomplete ledgers. Preserve both facts.

## Recommended next actions

Accept and publish this review outcome within the local experiment report, retain all raw evidence, complete the planned final freeze, and stop this panel without repairs or retries. Any further candidate requires a separately scoped experiment and fresh cases; no new review instance is justified by this unfavorable result alone.

# Independent final candidate review

Review instance: 2 of 3. Verdict: **Ready**, for the isolated candidate only.

The preliminary review was saved before reading FINAL-AUTHOR.md and RESULTS.md. Scope was independently confirmed as the new material-input-textarea-v1 directory on codex/material-input-textarea at e5027e77c4807636db3ea943ff8edd561065d6cf. Unrelated untracked work was excluded. No author conversation was inherited.

## Findings

No actionable blocking or non-blocking defect found in the frozen candidate. All 30 completed answers and 30 initial assessments were reviewed semantically against saved actual MCP packets, rather than expected fact IDs alone. No critical unsupported claim or baseline-supported regression was found.

| Cases | Independent semantic judgment |
| --- | --- |
| Q01 | Candidate correctly distinguishes renderer type from props.type and falsy fallback to text. Baseline completes this answer using the fetched K74 full implementation. |
| Q02 | Dedicated numeric branch is supported in both completed arms; neither answer infers locale-independent parsing, precision or serialization. |
| Q03 | Both completed arms correctly give props.placeholder, props.tabindex and field.name in both input branches. |
| Q04 | Both completed arms support readonly in both branches and reject an inference of disabled state or payload exclusion. |
| Q05 | Candidate supports props.rows/cols and both defaults of 1. Baseline lacks the concrete textarea contract. |
| Q06 | Candidate preserves the four-row scenario and refuses a universal pixel-height guarantee under CSS/autosize. Baseline input source does not establish textarea rows. |
| Q07 | Candidate gives the three autosize properties and CDK bindings without promising timing or conflicting-bound handling. Baseline lacks these bindings. |
| Q08 | Candidate separates rows and autosize and preserves hidden-container uncertainty. Baseline has no textarea-specific relationship evidence. |
| Q09 | Candidate supplies placeholder/tabindex and the renderer required binding without inventing an application-validation recipe. Baseline lacks these bindings. |
| Q10 | Candidate supports readonly forwarding without disabled/payload equivalence. Baseline lacks textarea readonly evidence. |
| C01 | Both arms preserve resetOnHide false and the control-registration limitation. |
| C02 | Both arms use nested datepickerOptions.min/max and preserve adapter boundaries. |
| C03 | Both arms preserve array membership/removal identity and do not import select compareWith. |
| C04–C05 | Both arms stop on actual unsupported version/adapter packets without substituting Material 6.3.12 support. |

Initial candidate support is 15/15; initial baseline support is 5/15. Completed candidate is 15/15 and baseline 9/15. These same results hold across all three exactly equal packet repeats. The six additional completed successes are textarea questions. The two new input records improve initial structured delivery of behavior already recoverable from K74. K74's returned excerpt is the entire input implementation and matches retained K47 source. Candidate K47/K51 citation objects contain pinned metadata rather than full excerpts; their detailed delivered authored claims supply the answer contracts and were independently checked against retained implementations.

## Plan Review

The implemented sequence and boundaries match PLAN.md: separate source interpretation, isolated build, protected baseline, frozen questions/plans, guarded real stdio transport, bounded recovery, separate initial/completed judgments, repeat equality and independent semantic review. Five new facts produce 116 facts/25 documents, with exact 6.3.12 Material scope. The source ledger marks only the input/textarea rows proposed and leaves unrelated paragraphs pending; it does not claim the whole table is newly admitted.

Manual raw-call audit closes the prebuild budget concern: baseline Q05–Q10 each used two discovery calls at offsets 0 and 16 with limit 16. Baseline Q01–Q04 each fetched one ID observed in initial omitted_ids. Candidate used no recovery. No repair attempts changed frozen plans. Scope, original full questions and their conditions remain intact. There are 90 lookup observations, 36 discovery calls and 12 fetches: 138 successful calls. Thirty completed answers and thirty initial assessments were reused only after exact structured packet/argument equality; this is not 90 independent generations or a planner evaluation.

## Author-Claim Reconciliation

| Claim | Evidence | Status |
| --- | --- | --- |
| Five grounded facts; two input records overlap recoverable evidence | Draft claims, K47/K51 retained implementation, actual K74 returned excerpt | Confirmed |
| 116/25 candidate preserves installed 111/24 | Eight-table superset checks and isolated canonical rebuild with equality in both directions | Confirmed |
| 15/15 versus 9/15 completed, 15/15 versus 5/15 initial | All saved answers, actual packets/citations and independent semantic audit above | Confirmed |
| 138 successful calls; no candidate recovery or repairs | Receipts, frozen calls, raw arguments and exact repeat comparison | Confirmed |
| Source, wiring and final artifacts frozen; 321 protected paths unchanged | SHA256 verification of 18 source-freeze entries, 3 wiring entries, 197 final-freeze entries, installed DB and baseline pins | Confirmed |
| Maintenance, lint and eligibility pass | Reviewer-executed checks below | Confirmed |
| Runtime/model changes absent | Protected pins, clean tracked Git diff, injected existing server factory | Confirmed; neither model-backed inference nor browser runtime was exercised |

## Verification Performed

- Batch unittest discovery in the existing MCP environment: all 18 tests passed. Read all eight helper/test Python files directly; graph search returned no symbols and coverage reported those untracked paths, so graph absence was not used as correctness evidence.
- python3 tools/project.py check: exit 0; source/provenance, compiler/package/regression checks and both launcher doctors passed. One non-failing SQLite ResourceWarning appeared. This command does not exercise hosted inference or sealed evaluation.
- candidate.preserved(), checked_database() for both arms, verify_superset(), verify_candidate_counts(), source lint and retrieval eligibility: passed. Retained K47/K51 hashes match the existing evidence catalog. Source quote offsets/hashes and foreign keys passed.
- Canonical build from candidate-inputs into a new temporary directory: all eight knowledge tables equal the frozen candidate in both directions. Temporary output was removed; no existing DB was rebuilt.
- results.main() and independent raw recovery-budget checks: passed, including receipts, offline-guard markers, canonical calls, observed-ID fetch provenance, citation membership, initial/completed separation and exact repeat equality.
- Direct inspection of returned evidence found no baseline textarea implementation excerpt supplying Q05–Q10; baseline input full-source credit was retained.

## Open Questions And Residual Risks

The mechanical auditor is intentionally not a semantic grader and does not enforce recovery caps itself. Those caps and unsupported-claim requirements were manually audited for this frozen run. Future changed calls require renewed auditing. No browser geometry, CDK timing, hidden-container behavior, hydration, numeric parsing, payload policy, module-alias coverage, general v6/v7 compatibility or autonomous planner quality is established. Both model-free and model-backed implementations remain preserved; only the model-free supplied-plan candidate transport was exercised here. Historical failures and sealed archives were not reopened or requalified.

## Verdict

**Ready** as a qualified isolated 116-fact candidate for the bounded exact-6.3.12 Material input/textarea scope. All specified candidate gates pass, including all five controls and zero baseline-supported regressions. This is not installation or promotion approval and does not establish whole-library accuracy.

## Recommended Next Actions

Return this review and preserve the frozen candidate artifacts. Any installation must be a separately authorized promotion with its own guarded equivalence and smoke checks. No production edits, promotion, staging, commit, publication, sealed-evaluation access or additional review instance occurred in this review.

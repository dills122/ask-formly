# Independent final review
Review instance: 2 of 3

## Preliminary blind ledger (recorded before AUTHOR)

- Verified HEAD 250f83da2d93aababf27f169078807ff66f183ee and the untracked batch boundary. Unrelated untracked files and the existing backlog modification are excluded.
- Read PLAN, GRADING, cases/adjudication, completed caller answers, report/audit/builder source, and targeted actual packet citations before the author explanation. Graph coverage reports the four inspected implementation paths untracked; conclusions use direct source, not graph absence.
- Frozen report reproduces 21/24 targets, 8/8 controls, 8/8 preservation cases; all three repeats fail the 22/24 gate. 35 tests pass. These are identical-packet repeats, not independent semantic generations.
- Potential scoring erratum: candidate API-12 says updateInitialValue takes no argument, whereas frozen adjudication specifies an optional model argument and nullish/current-root fallback. Check the delivered quote before final grading judgment; do not edit frozen answers.
- CONFIG-08's delivered wrapper citation supplies a replacement/throwing claim but no signature excerpt; partial judgment appears justified. API-09 and CONFIG-12 retain explicit missing support.
- Report validates freeze/run pins but preserved() does not load assessment-freeze.json. Independently verify that assessment seal before relying on scores.

## Findings

1. **P2 — API-12 overcredits an incorrect argument contract (proposed scoring erratum).** `test-output/assessment/API/completed-candidate-API.json:124` and `completed-baseline-API.json:118` say `updateInitialValue()` “takes no argument” and award full support. `cases.json:180` requires the relevant arguments, and `adjudication.json:172` fixes the optional model and nullish fallback obligation. The pinned implementation at `api/test-output/upstream/core.ts:123` accepts `(model?: any)` and clones `model ?? field.model`; the declaration at `api/test-output/upstream/config.ts:260` agrees. The actual fetched `defaults-and-resets/update-initial-value` citation supplies a no-argument example and reset-baseline role, with K05 coordinates but no implementation excerpt. That example cannot establish an exclusive no-argument contract or supply the missing optional-model behavior. Both arms should be **Partial**, `usable=false`, `critical_unsupported_claim=false`: this is a bounded argument error, not a critical unsafe assertion. Keep all frozen judgments unchanged and publish an explicitly separate erratum. Derived reviewed positives become baseline **4/24**, candidate **20/24**; totals become 19/40 and 36/40. Preservation and controls remain 8/8 candidate; no baseline-supported regression is introduced. The gate still fails every repeat.

2. **P3 — Report recomputation does not enforce the assessment seal.** `report.py:76` calls `preserved()`, but `candidate.py:76` only checks `freeze.json` and `run-freeze.json`. Neither path validates `assessment-freeze.json`. A future edit to an answer's boolean and rationale could therefore be reported as a fresh score without detecting broken assessment provenance. The smallest follow-up is an explicit assessment-pin validation step before report recomputation, with a mismatch regression test. This does **not** invalidate this run: this reviewer separately verified all 282 assessment pins successfully. Do not retrofit the frozen code for this completed experiment.

No additional actionable defect was established in the inspected build isolation, preserved-row comparison, call provenance, recovery-budget accounting, scope controls, or repeat comparison. Missing positive support is a failed experimental result, not a reason to relax its criteria.

## Plan Review

The experiment follows the bounded plan: 176-fact/33-document baseline, 12 additive records, isolated 188-fact/35-document candidate, original runtime and assets preserved, 40 frozen cases, identical initial plans, caller-selected recovery, three packet-identical repeats, and no installed promotion. The positive gate was not met; completing the experiment does not mean completing admission.

The source ledgers and CHECKLIST distinguish added records from existing coverage and exclusions. Their three original failed requests are primarily **missing answerable knowledge contracts**, not demonstrated ranking-only losses:

- **API-09:** `custom-types-and-wrappers/fieldtype-surface` is actually delivered but only lists the surface. It does not establish all getter forwarding or the props fallback. The inspected candidate authored inventory has no dedicated complete getter contract. K30 coordinates alone do not repair that gap.
- **CONFIG-08:** the candidate's duplicate-wrapper fact is delivered initially and fetched again. It establishes replacement and unknown-name throwing, but neither its authored claim nor its delivered evidence contains the wrapper signature/no-suppression contract. The locally pinned `K04.ts:189` supplies that signature for authoring verification, not retroactive caller credit. This is a representation gap despite successful retrieval of the relevant fact.
- **CONFIG-12:** the preset facts describe configured/matching presets. The authored inventory does not state missing-name behavior, and the delivered packets do not establish it. This is an omitted contract, not proof that the requested behavior has no source evidence.
- **API-12 (review erratum):** the baseline and candidate share an incomplete reset-baseline fact for the requested arguments. The inaccurate final answer compounds that knowledge gap.

These classifications are bounded to the inspected candidate inventory and actual packets; they are not whole-library completeness claims. No runtime/model pivot is supported by this experiment. A separately authorized frozen follow-up could address the missing contracts, but no such follow-up or new review was started here.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status and consequence |
| --- | --- | --- |
| 188/35 preserves the 176 baseline across eight tables | Read-only `verify_superset`, DB and input hashes, manifest | Confirmed; 188 facts, 35 documents, original rows retained. |
| Frozen 21/24 candidate versus 5/24 baseline | `report.py`, sealed judgments and actual packet citations | Reproduced as historical scores; API-12 overcredit requires separate reviewed 20/24 versus 4/24 erratum. |
| 432 calls, no tool errors, identical repeats | `read_run`, receipts, arguments, offline stderr marker, `validate_observation`, `compare_repeats` | Confirmed by recomputation; no independent-generation claim warranted. |
| No supported-baseline loss; candidate controls/preservation all pass | Completed answers, frozen cases, delivered claims, aggregate gates | Confirmed within reviewed obligations; API-12 correction is symmetric. |
| All source and asset pins intact | 15 upstream-file hashes, 326 protected-file pins, installed DB hash, accepted inputs, three seals | Confirmed at review time. Hash consistency is not a fresh upstream runtime test. |
| Maintenance passed and both runtimes preserved | Preserved assets and author's retained maintenance claim | Preservation verified; full maintenance was not rerun by this reviewer. Model-backed inference remains unqualified. |

## Verification Performed

- `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/public-api-v1 -p 'test*.py'`: **35 tests pass**.
- `poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/public-api-v1/report.py`: success; original counts 21/24 candidate, 5/24 baseline; `passes_each_repeat=[false,false,false]`; 432 calls.
- Read-only Python hash verification: all **55 pre-run**, **1 run**, **282 assessment** pins match; all **15** source-verification files match; **326** protected pins plus installed DB preserved.
- Read-only `checked_database`/`verify_superset`: all eight original canonical row sets retained; counts 35 documents, 188 facts, 98 evidence records, 293 fact-evidence rows, 81 links, 188 applicability rows, 293 applicability-evidence rows, 98 releases; exact 6.3.12 and stored source offsets validated.
- Compared completed answers with frozen requests/obligations and the actual delivered facts, examining supporting quotes/excerpts for disputed API typing, expression access, API-12 and wrapper lookup. Source URLs were not used to fill caller gaps.
- Graph search found no batch symbols; coverage marked relied-on implementation/upstream files untracked. Direct reads supplied the fallback. No reindex, build, live qualification calls, DB edits, model edits, sealed global archives, staging, or publishing occurred.

## Open Questions And Residual Risks

Source behavior is statically grounded; upstream Angular tests were not executed. Three identical packets do not increase the number of independent semantic observations. The historical report script continues to reproduce its immutable original grades; reviewed corrections must remain visibly distinct. Full maintenance execution is inherited evidence, not a reviewer-run check. The proposed report-seal enforcement remains a non-blocking follow-up for future experiments.

## Verdict

**Completed experiment: Ready with non-blocking follow-ups**, as a retained **failed qualification experiment**, with the API-12 erratum kept separate and prominently linked from current reporting. The experiment is reproducible and the negative gate is valid; the original 21/24 must not be presented as the independently confirmed score.

**Promotion eligibility: Not ready.** Both the historical 21/24 and reviewed 20/24 are below the immutable 22/24 threshold. No installed-data promotion is approved or implied.

## Recommended Next Actions

Retain the sealed run and original scores. Link a separate API-12 erratum and reviewed totals from current results. Preserve the failed gate and isolated candidate status. Keep assessment-seal enforcement as a prospective tooling follow-up. Any new admission attempt needs separately authorized scope and a fresh frozen run, not edits to this run or weakened obligations. Review instance 2 of 3 ends here; no additional reviewer was created.

## Same-instance closeout reconciliation

The author accepted API-12 and added `SCORE-ERRATA.json` plus `test-output/reviewed-results.json`, without changing the frozen answers. This reviewer inspected both and the updated RESULTS.md, independently recomputed the corrected summary in memory, and verified every summary field against reviewed-results.json. All 282 assessment pins still match. The separate correction satisfies finding 1 for current reporting; finding 2 remains accepted as a prospective non-blocking follow-up. The final experiment verdict is **Ready with non-blocking follow-ups**; promotion remains **Not ready**. No additional review instance is needed for this reporting-only correction.

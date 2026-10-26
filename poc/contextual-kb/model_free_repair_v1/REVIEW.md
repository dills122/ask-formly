# Independent repair-loop review

Review instance: 2 of 3.

## Findings

No actionable findings in this isolated feasibility increment. This is not approval to promote it or a qualification of arbitrary caller harnesses.

Reviewed the untracked model_free_repair_v1 boundary at HEAD 8e8d02e, including the frozen model_free_v1 dependency. Other untracked JSON-schema candidates were excluded. Recorded REVIEW-PRELIMINARY.md before reading REVIEW-AUTHOR.md. The initiating handoff disclosed expected outcomes, so the initial inspection was independent of the author packet but not wholly blind to results. Exact-path coverage checks report all 11 relied-on Python files as not tracked by the 2026-10-25 graph generation; conclusions use direct source inspection.

## Plan Review

The adapter follows PLAN.md: typed shape failures remain SDK errors; shaped-plan defects get bounded structured issues; absent plans get normal PLAN_REQUIRED feedback; unsupported coverage stops; absent records do not establish nonexistence. Operational/integrity exceptions propagate instead of inviting plan weakening. The server completes each call and delegates retrieval to the unchanged earlier service. The caller owns reasoning and the retry budget.

The three repair sequences preserve the original request, necessary question roles and conditions. R01 changes the seeded version constraint to null because the actual user request contains no version; its final answer explicitly limits evidence to 6.3.12. R02 retains false/zero and R03 restores the requested 6.3.12 Material scope. R04 stops after unsupported Formly 7; R05 needs one lookup. The additional fact fetch uses the resolved 6.3.12 scope and supplies control-unregistration/shared-key qualifications.

The post-live INVALID_SCOPE path correction is narrowly implemented and covered by a retained failing test and a passing current test. The original live snapshot remains available. No new hosted coverage is claimed for that branch. This is a justified bounded deviation, with no architecture pivot required.

## Author-Claim Reconciliation

| Claim | Evidence inspected | Status and consequence |
| --- | --- | --- |
| Structured/text/error feedback survives transport | serve.py, test_repair_transport.py, all caller-2 completed tool events and audit records | Confirmed; invalid shaped plans appear as failed calls with readable structured feedback; missing-plan feedback remains normal. |
| Three repairs, unsupported stop, one-call valid case | scenarios.json; raw caller-2 arguments, packets and answers; local replay | Confirmed: lookup counts 2, 2, 2, 1, 1. |
| First caller did not exercise recovery | caller-1 raw events | Confirmed: it corrected the three defects before submission; excluded from recovery success. |
| Caller did not receive expected outcomes | public_scenarios and its test; harness prompt construction | Confirmed; only IDs, requests and initial arguments are projected. |
| Citations and answers supported | All five final answers compared with delivered claims, conditions, limits and K05/K07/K14/K15 provenance | Confirmed for these cases. Mere ID membership is insufficient; manual semantic inspection supports the answers. |
| Installed and prior candidate bytes unchanged | baseline-state.json, freeze.json, freeze-current.json and live-revision-1 | Confirmed: 769 baseline, 22 prior-candidate and 13 current pins match; retained live snapshot matches its original pins. |
| Current code reproduces live packets | audit_live.py executed with only its summary-file write removed in memory | Confirmed: all eight lookups and one fact fetch reproduce exactly. |
| No server inference or retry enforcement | feedback.py, serve.py and unchanged candidate.py; guarded real stdio test | Confirmed within inspected implementation and tested guard environment; external harness remains a separate model caller. |
| Maintenance passed | retained test-output/maintenance.log | Confirmed as retained evidence, not independently rerun in this review. |

## Verification Performed

Executed `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/model_free_repair_v1 -p 'test_*.py'`: 18 tests pass, including guarded real stdio. Executed the existing audit_live.py logic through an in-memory copy suppressing its audit-summary write: all nine packets match and transition/first-input assertions pass. Independently computed SHA-256 matches for the 769 baseline pins, 22 earlier-candidate pins, 13 current pins and available retained live snapshot files.

Inspected all five caller-2 initial submissions, actual feedback, repaired plans, final answers and the fact follow-up; inspected caller-1's pre-correction behavior and retained RED/GREEN diagnostic-path evidence. No hosted calls, rebuilds, sealed evaluation, source fixes, staging or publication were performed.

## Open Questions And Residual Risks

Only explicit declared structure is validated. A condition omitted from both the questions and binding ledger can evade checks. Retry limits and preserving intent remain caller responsibilities. Three seeded repairs under explicit test instructions establish neither spontaneous-error frequency nor universal caller compliance. The replay audit's citation membership uses a global returned-ID union; the manual per-answer inspection above is necessary to establish support for this fixed run. New scenarios require their own semantic review.

SDK schema errors and operational failures have different transport presentations from structured repair packets. The new malformed explicit-scope branch has fixture coverage only. Kiro/Claude interoperability, repeated fresh caller qualification, clean-machine packaging and promotion are outside this review.

## Verdict

Ready — for the stated isolated repair-loop feasibility milestone only. The implementation and retained evidence satisfy its bounded plan. No promotion or general runtime/harness qualification is implied.

## Recommended Next Actions

Retain the candidate, first-run failure and live revision history together. Present the bounded feasibility result and limitations to the user. Any broader qualification or promotion requires separately agreed scope; this review does not authorize it. One review instance remains within the existing maximum of three.

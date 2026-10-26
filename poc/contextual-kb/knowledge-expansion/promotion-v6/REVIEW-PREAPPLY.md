# Independent promotion review

Review instance: 1 of 3. Deployment scope only; completed candidate review 4 of 4 is not reopened.

## Findings

No actionable findings. Preliminary independent inspection is recorded separately in REVIEW-PRELIMINARY.md, before reading the author explanation.

## Plan Review

The plan faithfully promotes the exact qualified database and planner without retraining or retuning. Six installed targets are authorized: two authored additions, DB, service import, foundation manifest and source preservation manifest. All existing authored inputs remain byte identical; canonical compilation is against a disposable DB, not the installed destination. Snapshot/recheck/rollback sequencing is appropriate for the documented stopped-service deployment. The plan explicitly handles the non-transactional crash boundary and requires reconnecting old processes.

The stable launcher path is used for the fixed 15-case smoke; explicit lookup-only authorization preserves the base approval policy. Source tests gain the promotion suite; local runtime checks gain the unchanged planner suite and a failure-sensitive default-service composition assertion. Installation smoke, documentation and final checks remain future gates, not completed evidence.

## Author-Claim Reconciliation

| Claim | Evidence | Status and consequence |
| --- | --- | --- |
| Exact qualified planner is promoted | qualification freeze pins, promoted_service(), service import comparison and new runtime pins | Confirmed; no planner rewrite |
| 85 facts / 19 documents preserve existing knowledge | Independently executed prepare preflight; old-row inclusion and canonical equality for documents/facts/evidence/fact_evidence/fact_links | Confirmed |
| Other runtime and protected files preserved | Preflight validates current manifest and prior preservation hashes; postcheck retains 84 runtime pins and 261 unaffected protected pins | Confirmed pre-apply; installed postcheck still required |
| 14 fixture tests pass | Reviewer reran unittest discovery | Confirmed |
| Cases match qualified cases | Direct byte comparison | Confirmed |
| Three qualifying answer rounds, 36 semantic probes and three Q20 premises pass | Pinned qualification JSON and validate_qualification | Confirmed as existing qualification evidence, not new installation evidence |
| Preflight leaves installed state unchanged | CLI lacked --apply; prepare only writes exclusive output tree | Confirmed |

## Verification Performed

- `python3 -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/promotion-v6 -p 'test_*.py'`: 14 passed.
- `poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v6/promote.py --name independent-preflight-1`: passed, checked-only receipt. Counts: 19 documents, 85 facts, 51 evidence rows, 130 fact/evidence links, 81 fact links. Five-table canonical equality and accepted-row preservation passed.
- Direct byte assertions: fixed cases equal qualification cases; proposed service differs only in the CodexPlanner import.
- Read source for promotion/tests/runner, service, planner and maintenance integrations. Tier 2 graph had no new symbols and incomplete coverage; direct source fallback used for every affected implementation path.

## Open Questions And Residual Risks

Per-file atomic writes do not protect against a killed process or machine failure between files. The plan documents recovery and prevents simultaneous serving operationally. No hosted calls, sealed evaluations, installed mutations, fixes or commits were performed by this reviewer. The future 15-answer semantic/citation audit, Q20 ledger, installed composition/doctor/maintenance and final preservation checks remain required. Current default composition test is intentionally red until installation.

## Verdict

Ready for guarded apply. This is not final publication approval.

## Recommended Next Actions

Apply with services stopped, run local maintenance/doctor and the single fixed installation smoke, then return all answers, delivered citation packets and Q20 premise ledger to this same reviewer. Finish current documentation and preservation evidence before publication.

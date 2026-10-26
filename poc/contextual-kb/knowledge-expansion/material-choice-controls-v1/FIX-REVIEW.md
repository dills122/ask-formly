# Independent bounded audit-fix review

Review instance: 2 of 3. Verdict: **Ready** for freezing and the planned isolated build/comparison, subject to the operational gates already in PLAN.md. This is not a qualification or promotion verdict.

## Findings

No actionable findings remain in the three reviewed audit fixes. The earlier discovery/fetch rejection, unfrozen initial-call acceptance and initial/completed evidence conflation are resolved.

`results.read_run` now records discovered IDs per case before fetch, rejects recovery version/adapter drift, and rejects changed discovery requests/plans. Every initial lookup must exactly equal the shared canonical lookup list, so both accepted arms necessarily use the same initial arguments. Initial packet content is deep-copied before fetch completion. `results.main` separately validates initial and completed assessments and reports both score series while retaining exact repeat comparison.

The additional bounded `candidate.preserved` change checks run-freeze.json when present, including database wiring pinned after the candidate exists. Its regression test passes and detects a changed wiring file. Because this manifest is optional in code, creating and retaining it before transport remains an explicit execution gate; this review does not claim that absent run-freeze.json is rejected automatically.

## Plan Review

The fixes implement the existing plan without adding a workstream or changing its experiment design. The identical frozen-plan check supplies cross-arm equality by transitivity; a redundant direct cross-arm comparison is unnecessary. Separate initial judgments now permit the planned distinction between initial and completed evidence support. Source mapping/build design conclusions remain those of review instance 1; this bounded pass did not repeat the full upstream mapping audit.

Freeze the inspected inputs before candidate build. After build, verify candidate counts, superset, applicability, source evidence and preservation, then populate and freeze actual database wiring before transport. The fifteen cases, acceptance criteria and manual semantic assessment remain required. Final semantic/outcome review is instance 3 of 3.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status | Review consequence |
| --- | --- | --- | --- |
| Discovered IDs can be fetched; unseen IDs remain rejected | read_run; AuditTests; executed suite | Confirmed | Earlier P1 resolved |
| Both arms use the frozen initial calls | read_run exact canonical equality; altered request/version/plan tests | Confirmed | Earlier P2 resolved |
| Initial and completed packets/judgments are separate | deep copy; main dual validation/reporting; fetched-only initial citation probe | Confirmed | Earlier P2 resolved |
| 17 tests pass | Reviewer first execution | Confirmed | Later wiring addition increases suite to 18 passing tests |
| Runtime wiring drift is detected when run freeze exists | candidate.preserved; test_runtime_database_wiring_freeze_detects_drift | Confirmed | Pin actual wiring before comparison |
| Red failures were retained before fixes | Author response | Not independently verified | Not relied on for readiness |

## Verification Performed

- Verified branch codex/material-choice-controls, HEAD eb53f184faccffc1de1ec349c0df1a29bd65091a and untracked batch boundary; excluded unrelated untracked work.
- Recorded FIX-PRELIMINARY.md before reading REVIEW-RESPONSE.md and REVIEW-AUTHOR.md. Reviewer context did not include author implementation history.
- Executed `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/material-choice-controls-v1 -p 'test_*.py'`: initially 17 passed, then 18 passed after the explicitly disclosed wiring-freeze addition.
- Executed four temporary-fixture negative probes: fetched-only citation rejected against initial evidence (accepted against completed evidence), and discovery adapter/request/plan changes rejected.
- Directly inspected results.py, test_audit.py, existing batch tests and candidate.py. Exact-path graph coverage reported these Python files not tracked, so direct source reads provide the evidence; no graph completeness claim.
- No candidate build, installed DB modification, implementation edits, sealed evaluation access, staging, commits or publishing. Full project maintenance was not rerun by this bounded reviewer; the initiating task must retain its current check result.

## Open Questions And Residual Risks

Mechanical checks cannot establish answer truth or semantic completeness. Independent semantic assessment must inspect actual packets and answers, including initial support, recovery provenance/budgets, controls and unsupported claims. The initial packet snapshot is isolated from completion mutation, not an immutable Python type. The runtime wiring guard checks a present manifest; existence and correct contents must be verified before the run. Freeze/build/transport artifacts were not executed or qualified here. Existing historical failures and limits remain intact.

## Verdict

**Ready** for freezing and isolated comparison. All three reported blockers are corrected with meaningful regression coverage. This verdict is bounded to the inspected audit changes and newly disclosed wiring guard; installed knowledge remains unchanged until separately authorized promotion.

## Recommended Next Actions

Freeze inputs, build only the isolated candidate, pin generated wiring in run-freeze.json before transport, execute the fixed comparison and separate initial/completed assessments, run the required project maintenance check, then use review instance 3 for final outcomes. Do not tune frozen facts/cases/criteria in response to comparison results.

# Independent merged-foundation review

Review instance: **2 of 3**. Reviewer: `/root/merged70_review`, 25 October 2026. Scope: working-tree merge of `3607c17358d006574e543c3a89060426156981ac` into `57be6be9192faa39de9b56ac61a871b3ce307e9b` on `codex/knowledge-admission-70`, plus the bounded merged-run wrapper. No additional reviewers created. Only this report was written by this reviewer. A blind first pass was impossible because the bootstrap included author claims; those claims were independently checked against both parents before relying on the prior promotion review.

## Findings

No unresolved actionable merge or wrapper findings. The first merged live run failed all 15 cases before successful MCP delivery: the remote lookup annotation is now `readOnlyHint=false`, and the original caller's approval policy rejected calls. `test-output/merged-live` retains that 0/15 result. It is not counted as successful qualification.

The separate `merged_run.py` invocation explicitly enables and approves only `lookup_formly`, preserves the base approval policy, requires an explicit authorization flag, and uses an exclusive output directory. It does not edit global configuration or the frozen runner/cases. The approved run is recorded separately as `test-output/merged-live-approved`.

## Plan Review

The merge preserves the local foundation5 knowledge promotion and the remote project/worktree settings feature. Comparison of every remote-changed path found all remote runtime, test, CI and packaging bytes preserved. The six differing remote paths are intentional combined resolutions: `.gitignore`, README, development guide, foundation README, foundation manifest and project checker. The checker retains both promotion/admission fixture suites and the context suite; its wiring test includes both.

Against the local parent, foundation changes are limited to `server_packages` and `files`: semantic-version is added, server/requirements hashes change, and five remote file pins are added. Foundation identity, knowledge metadata, DB pin, all model pins and other prior runtime pins remain intact. Direct hashing confirmed installed DB equality with the local parent. Completed doctor evidence verifies all 86 installed file pins. The original promotion's recovery limitations and sealed-evaluation boundary remain applicable.

## Author-Claim Reconciliation

| Claim | Evidence | Status |
| --- | --- | --- |
| Remote functionality retained | Byte comparisons against merge parent; direct source and test reads | Confirmed |
| Local 70-fact foundation retained | Manifest comparison against HEAD, direct installed DB hash, doctor receipt | Confirmed |
| Both source suites retained | `tools/project.py`, wiring test, completed source log | Confirmed |
| Approval adaptation is invocation-local and lookup-only | Wrapper code, two command-boundary tests, unchanged frozen runner/cases | Confirmed |
| Approved merged smoke succeeds | All 15 actual answers, delivered audit facts, deterministic delivery checks and assessor records | Confirmed |

## Verification Performed

Directly ran the four project guard/wiring tests and two wrapper tests: all passed. `git diff --check HEAD` passed at the reviewed merge boundary. Checked graph coverage for relied-on code; the graph was stale or excluded for new/changed files, so conclusions use direct source reads rather than graph completeness claims.

Inspected the implementation task's completed maintenance receipt: 104 source tests before the two wrapper tests, 114 runtime tests, doctor `ok: true` with 86 files and foundation5, and a separate passing real stdio fixture transport test. The implementation task subsequently reported 106 source tests passing after adding the wrapper tests. The maintenance log contains a non-failing unclosed-SQLite ResourceWarning; no failure was suppressed.

Read all 15 approved-run answers and compared their claims, conditions and limits with the frozen case criteria and cited facts in the actual returned audit packets. X01–X10 correctly cover extension phases/priorities, guarded wrapper insertion, configured preset/provider behavior and its limits. E05, M03 and Q20 preserve expression, model-scope and public-type behavior. Q21 and Q24 explicitly reject unsupported application-private and Formly 7 conclusions. No unsupported answer claims or missing required aspects were found.

Independently executed the existing assessor's delivery-only `prepare()` for all three batches in the MCP environment: 15 unique expected answers, no delivery errors, delivered packets equal saved audits, and citations present in returned packets. Each caller receipt has exit zero, no error and five calls. All 15 packet DB/model integrity checks pass; advisory extraction is available for 14 and not needed for the private-application gap case. Automated assessments independently report 15/15 usable, zero critical and zero delivery failures. The earlier rejected run remains 0/15 usable with 15 delivery failures. No hosted inference was invoked by this reviewer. An initial delivery-check import with system Python lacked MCP; rerunning with the provisioned MCP interpreter succeeded.

## Open Questions And Residual Risks

The live run qualifies the legacy request-only lookup path on the merged runtime. Project persistence, worktree inheritance and coverage gating are covered by the remote context tests and fixture transport test; the live smoke does not separately qualify every settings combination. The approval-dependent behavior remains relevant to clients: noninteractive clients using the old policy must explicitly authorize lookup. These visible cases are installation regressions, not unseen evaluation, whole-library coverage or Angular application validation. Sealed evaluation was not opened. Final staged/publication inventory and CI remain the implementation task's responsibility.

## Verdict

**Ready** for the reviewed merge and explicitly authorized lookup-only smoke path. No unresolved actionable findings.

## Recommended Next Actions

Retain both failed and successful run records, document the client approval requirement, keep current test counts at 106 source / 114 runtime / 86 doctor checks, and complete the requested publication checks without staging private runtime assets or raw generated output.

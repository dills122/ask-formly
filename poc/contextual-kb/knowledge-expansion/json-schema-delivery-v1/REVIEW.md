# Independent delivery investigation review

Review instance: 3 of 3. Reviewed 2026-10-26, HEAD `8e8d02e82c01e3f0e6e0b74a31b8c7346ca22830`, branch `codex/versioned-knowledge`.

## Findings

No actionable findings in the bounded investigation. **Investigation verdict: Ready. Candidate promotion verdict: Not ready.** Ready means the evidence and stop decision can be accepted; it does not mean delivery is repaired or qualification passed.

Independent reconstruction preceded reading REVIEW-AUTHOR.md; see REVIEW-PRELIMINARY.md. Scope is the new delivery batch and sibling `json-schema-v1/test-output/delivery-serial-smoke-1`. Both JSON Schema directories are untracked; tracked `git diff --stat` is empty. Earlier candidate review is not repeated here.

## Plan Review

The plan's four direct-call bound was respected. Serial C01/C02 completed in 7.13/10.27 seconds; paired C01 completed in 7.91 seconds and paired C02 timed out at 180.02 seconds. `test-output/probe.py` retains each attempt, catches the timeout into an explicit outer receipt, marks aggregate health false, and uses exclusive output creation. The frozen planner itself rethrows timeouts after process-group termination, so absence of its inner receipt is expected.

The additional serial real-caller diagnostic was explicitly recorded in PLAN.md. Baseline delivered two answers; candidate was deliberately stopped after a renewed throttle before invoking MCP. Stopping short of all four planned deliveries and the conditional 90-answer run is justified by this evidence. The result is an aborted smoke, not a pass. A full run, grading and replay remain unexecuted in this investigation. No product fix or changed timeout is claimed.

## Author-Claim Reconciliation

| Claim | Evidence inspected | Status and consequence |
| --- | --- | --- |
| Prior failures lack explicit throttle evidence | Saved inventory and all eight raw missing-receipt attempt directories under sibling `test-output/qualification-1` | Confirmed: only thread/turn start events, empty stderr, no receipt. Their cause remains unknown. |
| Prior successful timing medians are 16.09/19.71/16.98s | Recomputed from all 90 inventory rows: 30/30/22 successful receipts per repeat | Confirmed; successful timings do not explain failed requests. |
| New planner timeout involves HTTP429 exceeding its deadline | `test-output/probe-1/paired-C02/5e85bb91040f4711a39c75d83233b100/stderr.txt:2`, outer paired-C02 receipt, planner source | Confirmed: 13:45:34Z plus approximately 437s retry delay exceeds unchanged 180s deadline. This explains this attempt, not all prior failures. |
| Serial baseline recovered and delivered two answers | Smoke baseline stderr, receipt, answers, events and aggregate result | Confirmed: 202s CLI retry, 269.82s caller elapsed, exit 0, two MCP calls/audits and completed turn. C01 preserves defined false/zero; C02 uses resetOnHide:false without promising control registration. This is bounded inspection, not full qualification. |
| Candidate interrupted before MCP | Smoke candidate stderr, receipt and events | Confirmed: HTTP429 with 533s delay, exit -15 at 118.35s, only start events, zero audits and no answers. Logs establish interruption, while its deliberate operator origin is author testimony. It is not a planner timeout or knowledge miss. |
| No harness retry; CLI retry occurred | Probe/serial diagnostic sources and raw stderr | Confirmed distinction. No evidence establishes concurrency as causal or serial scheduling as a fix. |
| Installed and candidate assets preserved | Independent `preserved()` and both `checked_database()` calls | Confirmed against saved manifests, including 769 baseline file pins and candidate freeze/input hashes. |
| Maintenance passed | `test-output/maintenance.log` ending with local-foundation success | Supported by retained log, not independently rerun by reviewer. Does not establish hosted availability. |

The general external error-guidance link is not needed for this verdict and was not independently validated. Local raw logs support the actual throttle claims.

## Verification Performed

- Inspected repository guidance, README, development/knowledge-pipeline documentation, bootstrap, PLAN, diagnostic scripts and raw evidence; wrote preliminary report before reading author explanation and RESULTS.
- Ran read-only Git status/branch/HEAD/diff commands. No tracked changes were present.
- Ran `poc/contextual-kb/.venv/bin/python -B` with sibling batch import to call `candidate.preserved()` and `candidate.checked_database('baseline'/'candidate')`; all passed. Installed SHA256: `a0f102f1bad83dfec7c91148925187644e3092a3ca08cdaa88f586a7e1a0c106`; candidate: `8487ca97dde24daff0a9dc655111e0066b7f3ce0dccf7c65d81f6f6087fa3c6c`.
- Recomputed inventory counts/medians and inspected all eight historical raw failure directories. Checked smoke event types and audit counts: baseline two audits, candidate zero.
- Checked graph coverage for the six relied-on Python sources; all reported not_tracked at generation 2026-10-25T14:19:41Z. Used direct source inspection for diagnostic scripts, preservation functions and relevant planner/caller/grader timeout code. No graph completeness claim.
- No hosted requests, grading, replay, builds, installed writes, sealed evaluation/archive access, staging or publication performed. Review writes are limited to the preliminary and final reports.

## Open Questions And Residual Risks

The account/model/request/token/window scope of throttling is unknown. Sequential probing confounds elapsed time and shared capacity with concurrency. Candidate delivery remains untested in this smoke; prior silent failures remain unresolved individually. Manifest checks prove consistency with pinned assets, not whole-library accuracy. There is no demonstrated runtime remedy.

## Verdict

**Ready — bounded investigation and decision to stop.** The retained evidence supports the claims made and accurately discloses limits and the interrupted smoke.

**Not ready — candidate promotion.** Neither the aborted diagnostic nor maintenance replaces a complete eligible qualification, grading and replay result. The candidate remains isolated.

## Recommended Next Actions

Retain every failed attempt and the unchanged installed foundation. Await adequate hosted capacity before any separately frozen visible-case run; retain the unchanged gates and separate calling, grading and replay phases. Do not interpret this review as authorization to promote or launch another run.

This is review instance 3 of 3; the current independent-review loop is exhausted. No further reviewer is started. Any later work requiring another independent review must return to the human for an explicit revised review limit rather than silently resetting the counter.

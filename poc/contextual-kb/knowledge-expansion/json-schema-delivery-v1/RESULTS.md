# JSON Schema delivery investigation

**Hosted throttling reproduced; full requalification not started.** The99-fact
candidate remains isolated and unqualified for promotion. Installed foundation9
remains93facts/21documents. No product code, knowledge, model or DB change was needed
or made during this investigation.

## What the evidence shows

The prior90planner attempts include82successes and8timeouts. Successful planner
medians by repeat were16.09,19.71and16.98seconds. The8failures stopped after
thread.started/turn.started with empty stderr; their root cause was not recorded.

| New diagnostic | Outcome |
| --- | --- |
| C01 planner alone | Passed7.13s |
| C02 planner alone | Passed10.27s |
| C01 paired planner | Passed7.91s |
| C02 paired planner | Timeout180.02s; stderr HTTP429, scheduled retry437s |
| Serial baseline caller, C01/C02 | Initial HTTP429, CLI waited202s, then2/2MCP calls and answers passed;269.82s total |
| Serial candidate caller, C01/C02 | HTTP429 with533sretry delay before any MCP call; deliberately interrupted after118.35s, exit-15 |

At13:45:34UTC the437second delay and at13:49:30UTC the202second delay pointed to
approximately13:52:52UTC. The baseline caller recovered after that wait. At13:54:00UTC
the next caller was throttled again. Serial scheduling alone therefore does not
establish healthy delivery. The candidate arm delivered0of2planned smoke requests;
this aborted diagnostic must not be counted as a pass or as a semantic knowledge miss.

The reproduced429delay exceeded the unchanged180second planner deadline. This
explains the new planner timeout. It is consistent with, but does not prove the
cause of, all eight older silent failures. Account/model/window/token/request scope
is unknown; concurrency is not established as the sole cause.

## What stays fixed

No increased deadline, model switch, changed facts, weakened gate, promotion or
publication. Harness-level retries:0. CLI transport retries occurred and remain in
logs. Sealed evaluation was not opened. Frozen source/runtime/model/DB hashes were
checked before and after diagnostics. Original qualification-1 remains unchanged;
new smoke outputs are in its sibling delivery-serial-smoke-1 directory.

[Official error guidance](https://developers.openai.com/api/docs/guides/error-codes#python-library-error-types)
recommends pacing requests and respecting Retry-After. This is general guidance;
our local CLI logs are the evidence for the observed delays.

## Decision

Do not run another90answer qualification while this throttle persists. Once adequate
hosted capacity is available, use the unchanged frozen15cases/gates in a new run:
serial caller jobs, grading after all calls, replays after grading. Retain failure
history and describe this as a fresh run of visible development cases, not unseen
evaluation. Passing that complete run and review remain prerequisites to promotion.

See REVIEW.md for the final independent investigation verdict. Maintenance and
preservation results are recorded in test-output; no test result claims live service
availability under throttling.

Final local check: `python3 -B tools/project.py check` passed (exit0), including
source checks,95doctor pins and active regressions. Independent preservation check
verified769baseline files, freeze and both DB hashes. These are local integrity
checks, not a claim that hosted throttling has cleared.

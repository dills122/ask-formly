# Fresh independent review bootstrap

Review instance: 5 of 5 total authorized (one new review explicitly allowed by
user for this implementation). Earlier fourth review covered identity revision.

## Objective

Independently review training-harness and original first-save verification against
PROTOCOL.md/READINESS.md and user scope. No full training or evaluation execution.
Start with code/tests/protocol; send preliminary findings BEFORE reading
IMPLEMENTATION.md (author explanation). Then reconcile claims and final evidence.

## Repository and boundary

Repository /Users/dsteele/repos/ask-formly. Working-tree boundary exclusively
poc/contextual-kb/gliner_feasibility/adaptation/full_training. This folder is
untracked; prior files here were protocol/readiness/preparation-checks only.
All new Python sources/tests, implementation doc, test-output logs, preflight-01
and manifests are in scope. Other POC code is reference only, unchanged. Read
AGENTS.md and poc/contextual-kb/AGENTS.md/STEERING.md. Do not inspect or import
outside-POC implementation. Do not read evaluation data, knowledge/DB/corpus,
other case sets or external attachments. Only prior pilot/adjudicated-v2.json
may be read as question data. Hashing protected bytes is permitted.

No staging/commits. Read git status/head and retained review freeze to establish
state. No code edits. Your report may be written to test-output/independent-review.md.

## Verification and constraints

Use existing ../../env/.venv/bin/python, PYTHONDONTWRITEBYTECODE=1, login:false.
May run unittest test_harness test_inputs test_native test_evidence (small torch,
no real GLiNER checkpoint loading). Temporary test directories are inside
full_training/test-output and removed on completion. Inspect native preflight
artifacts instead of rerunning optimization. Do not run worker.py/controller.py
preflight or train, do not create data, do not allocate another reviewer.

Focus on loss reduction/partial accumulation, actual first-save ordering,
original in-memory capture versus a resave, exact parity/RNG/mode/gradients,
checkpoint gating, input isolation, timeout bounds and honest readiness limits.
Protocol expects eventual 120/30/60 design; this change does not supply those
annotations or evaluation/scoring pipeline. Confirm what is implemented versus
merely specified and whether any gap blocks accepting this bounded harness.

## Final report

Findings first with evidence, plan adherence, author-claim reconciliation,
verification performed, residual risks and Ready / Ready with non-blocking
follow-ups / Not ready / Unable to verify. Distinguish bounded harness acceptance
from authorization/readiness to start full training. Send report to parent.
If a heavy pivot is needed, stop at evidence/proposal; no execution or new review.

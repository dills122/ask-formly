# Independent safeguard review bootstrap

Review instance: 6 of 6 total authorized. User explicitly authorized one additional
independent review of the two later safeguards and an explanation of prerequisites.

Review only the changes added after review5's freeze:
1. checkpoint.execution_state and state-before.json write in verify_first_save:
   persist Python/NumPy/PyTorch RNG values, module modes and gradient hashes before
   capture/save, while preserving runtime state.
2. native.prepare: reject >32 requested aspects before native preprocessing and
   therefore during the worker's pre-optimization scan.
Include tests and downstream call sites. Expanded output/serialization negative
tests are context. Do not redesign or claim full-training readiness. Earlier
review: test-output/independent-review.md. Current source freeze:
test-output/safeguards-review-freeze.json.

Repository /Users/dsteele/repos/ask-formly. Scope exclusively
poc/contextual-kb/gliner_feasibility/adaptation/full_training.
Read applicable AGENTS.md and POC STEERING.md. Follow independent-review skill.
Inspect sources/tests first; send preliminary findings before reading FINDINGS.md
and IMPLEMENTATION.md author explanations. Reconstruct claims independently.

Read-only except report to test-output/safeguards-review.md. No code edits,
staging, commits, optimization, model load/preflight/training rerun, additional
reviewers or datasets. Do not read evaluation or knowledge/DB/corpus content.
Hashing protected bytes against test-output/protected-before.json permitted.
Use only POC sources and installed POC third-party dependencies.

Allowed suite with login:false:
PYTHONDONTWRITEBYTECODE=1 ../../env/.venv/bin/python -m unittest test_harness test_inputs test_native test_evidence -v
Additional bounded non-optimizing checks may validate RNG serialization/restoration
including exception paths, and capacity boundary with a stub at native preprocessing.
Temp files only in this directory's test-output. Preserve prior artifacts. Do not
attribute old native preflight to new state receipt/capacity behavior.

Report findings, verification, plan/claim reconciliation and Ready / Ready with
non-blocking follow-ups / Not ready / Unable to verify. Separate safeguard verdict
from full experiment readiness. List remaining full-training prerequisites;
dataset/scorer/custody production is out of scope. Only this additional reviewer.

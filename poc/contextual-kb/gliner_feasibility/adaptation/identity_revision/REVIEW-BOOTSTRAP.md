# Independent review bootstrap

Review instance4 of4. User explicitly authorized one additional review after the
previous3-instance flow, and targeted record-identity revision plus compatibility
checks on the same24 training pilot cases. Review findings before full training.

Repo /Users/dsteele/repos/ask-formly; main HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516.
Extensive existing dirty/untracked files; no staging/commit. Scope is new directory
`poc/contextual-kb/gliner_feasibility/adaptation/identity_revision/` excluding cache.
Prior pilot is reference/read-only; do not fix or overwrite it. Code/run manifest
is evidence/review-freeze.json; docs added afterwards are also review scope.

Requirements: project/POC AGENTS, STEERING; parent ADAPTATION-EXPERIMENT-DESIGN.md;
this directory PLAN.md and latest user authorization. A unchanged, all code/data
inside POC, knowledge data/DB locked, evaluation sealed, no full-training approval.
Bounded optimizer smoke is compatibility-only on the same24 examples.

Use independent-review and code-review-and-quality. Read tests, code and retained
evidence first. Send preliminary findings before AUTHOR-EXPLANATION.md/FINDINGS.md.
Then reconcile. No additional reviewers. No fixes or architectural workstreams.

Read-only commands from this directory:
`PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 ../../env/.venv/bin/python -m unittest test_revision test_compatibility`
This loads only the existing local model; no training or output writes intended.
Do NOT rerun test_training: it performs optimization and reserves exclusive
smoke-run/ output. Inspect its recorded execution/code/artifacts instead. Can
verify pre/post reload JSON equality, step counts, code/artifact/protected hashes.
No sealed/evaluation/corpus contents; read-only protected hashing allowed.

Review both plan and implementation. Distinguish representation/mechanical
compatibility from semantic learning quality and full-training readiness. Return
evidence-backed verdict, limits and any required decision gate. May write report
only to evidence/independent-review.md; otherwise send it. Read author explanation
only after recording the preliminary pass. No review beyond4/4 without user action.

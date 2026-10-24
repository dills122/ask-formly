# Fresh review bootstrap

Review instance: 3 of 3 for the GLiNER feasibility flow. Review the bounded pilot
and whether its evidence supports the reported stop/continuation decisions.

Repository /Users/dsteele/repos/ask-formly, main at
c3091328f49d53de6b41a49c4fe5aa8f1c45e516. Many pre-existing dirty/untracked files;
see evidence/git-state.json. No commit/staging. Review target is the new directory
`poc/contextual-kb/gliner_feasibility/adaptation/pilot/` only, excluding .cache.
Code and annotation hashes are in evidence/*freeze-v2.json. Earlier versions are
retained evidence, not current implementations.

Requirements: POC AGENTS/STEERING and
`gliner_feasibility/ADAPTATION-EXPERIMENT-DESIGN.md`. Latest user authorizes only
the 24-question annotation pilot and compatibility check with TDD; review findings
before full training. A unchanged, all work inside POC, DB locked and evaluation
cases sealed. No training/new evaluation or edits to other layers are authorized.

Read tests, annotations, implementation and evidence first. Record preliminary
findings before reading AUTHOR-EXPLANATION.md or FINDINGS.md. Then reconcile them.
Use independent-review and code-review-and-quality skills. No further reviewers.

Non-mutating verification from pilot:
`PYTHONDONTWRITEBYTECODE=1 ../../env/.venv/bin/python -m unittest test_contract test_analysis`
and `... -m unittest test_native_contract`. Preprocessing can be rerun offline
with `... -m unittest test_preprocessing` and PILOT_WRITE_EVIDENCE unset; imports
only local package/model. Do not read sealed/old evaluation cases or knowledge
contents. Hash verification of protected files is allowed.

Verify relevant source behavior using installed third-party package if needed.
Do not run training, make predictions, alter labels, implement fixes or pivot.
Return preliminary notes, then final evidence-backed report and verdict. Distinguish
accepting pilot findings from readiness for full training. If a material design
revision is needed, return the decision gate; do not implement it. This is the
last review instance in this flow.

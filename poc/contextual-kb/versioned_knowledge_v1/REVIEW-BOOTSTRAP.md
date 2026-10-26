# Fresh Review Bootstrap

Review instance: 1 of 3.

Objective: independently assess the opt-in versioned knowledge candidate against
this directory's PLAN.md and docs/versioned-knowledge-plan.md. Existing installed
DB/models/runtime, authored inputs, source provenance and sealed evaluation must
remain unchanged. No real new release coverage is authorized.

Repository: /Users/dsteele/repos/ask-formly. Branch codex/versioned-knowledge.
Base/HEAD: d5a82fac7d03136137fbafa7c7faeeb15dbfa1c2 (merged PR8).
The entire change is untracked versioned_knowledge_v1/, not committed. No other
paths are in implementation scope. Private test-output/ contains baseline pins,
rollback DB, candidate DB, migrated copies, logs and deterministic comparison.
Do not read sealed evaluation/qualification archives. Test-output in THIS new
candidate is development evidence and may be inspected.

First inspect plan/code/tests and write preliminary concerns before reading
REVIEW-AUTHOR.md (provided after your initial pass). Review remains read-only
except your review reports in this directory. No fixes or additional reviewers.

Available checks:
PYTHONPATH=poc/contextual-kb:poc/contextual-kb/mcp_v1 poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/versioned_knowledge_v1 -p 'test_*.py'
python3 -B tools/project.py check

Do not rerun qualify.py in its existing output: it intentionally refuses to
replace a candidate. Inspect comparison.json and independently reproduce selected
read-only comparisons. Live smoke is being run by author; do not duplicate hosted
calls. Verify final receipts before verdict.

Graph Tier2: project ask-formly; generation 2026-10-25T14:19:41Z; search_graph
returned no compiler/backend matches. Coverage flags all inspected legacy files
metadata_changed and candidate files untracked. Parent directly read compiler,
PilotIndex, backend/citations, repair policy/integration, bridge, service and
context wrapper. Use source fallback for this candidate; no graph completeness
claim. Installed service still uses original modules.

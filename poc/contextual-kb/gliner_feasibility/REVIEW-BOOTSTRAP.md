# Fresh Review Bootstrap

Review instance: 1 of 3 for the new user-authorized GLiNER2 feasibility flow (separate from completed A/B fixes review).

## Objective
Independently assess the bounded development-only GLiNER2 probe and findings before any full comparison. No promotion or implementation pivot authorized.

## Repository and working boundary
/Users/dsteele/repos/ask-formly, main with broad pre-existing dirty/untracked changes. No new commits. In scope only poc/contextual-kb/gliner_feasibility (new files), existing POC STEERING.md and planner_cases/development.json read-only. Protected manifest includes previous A/B freeze and locked bytes. No other project code reused.

## Requirements and plan
Read root AGENTS.md, POC AGENTS.md/STEERING.md, gliner_feasibility/PLAN.md. User: bounded GLiNER2 feasibility with development cases only; A unchanged; everything inside POC; data/DB locked; review findings before a full comparison.

## Review order
Inspect schema.json, tests/test_probe.py, probe.py, run.py and evidence/raw.jsonl + runtime.json and protected/probe hashes first. Record preliminary observations before reading FINDINGS.md and AUTHOR-EXPLANATION.md. Do not read any held-out fixture or A/B raw outputs.

## Safe checks
From gliner_feasibility: PYTHONDONTWRITEBYTECODE=1 env/.venv/bin/python -m unittest discover -s tests. Recompute evidence aggregates and hashes; never execute run.py (already completed and exclusive output). No network/model calls, DB connections, compiler or data tests. Reading bytes for integrity hashes permitted.

## Output
Write evidence/independent-review.md. Use independent-review skill in reviewer mode. Verdict must distinguish sound feasibility evidence from readiness for a full comparison. Do not fix code, alter raw evidence, create further agents/reviews or expand scope.

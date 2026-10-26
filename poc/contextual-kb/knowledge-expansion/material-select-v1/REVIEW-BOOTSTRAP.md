# Fresh Material select review bootstrap

Review instance: 1 of 3 for this isolated Material select admission batch.

## Review objective

Independently review pinned source verification, proposed mappings/facts, ledger decisions, candidate construction, frozen comparison cases and harness before build/inference. After qualification, audit outputs and preservation in the same scope. Do not promote, commit, publish, modify old candidates or access sealed evaluation.

## Repository and boundary

Repository: /Users/dsteele/repos/ask-formly. Branch codex/material-select-knowledge starts from merged main c232620632e5a35b5770ea7bdb8ca8e7ee9ba32f. In-scope working-tree boundary: poc/contextual-kb/knowledge-expansion/material-select-v1 only. The parent/source mapper may still be completing artifacts: verify actual readiness with the initiating task before treating them as frozen.

## Canonical requirements

Read AGENTS.md, README.md, docs/development.md, docs/knowledge-pipeline.md, then this batch's PLAN.md. Current accepted baseline is foundation7, 85 facts / 19 documents; the AGENTS sample count may lag this recorded promotion. Models and installed setup remain unchanged; evaluation sealed. Eight source-reviewed proposals target 93 facts / 21 documents, not a preapproved full Material corpus. Review exact boundaries/exclusions in source mappings and drafts.

## Tests and available evidence

- `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/material-select-v1 -p 'test_*.py'`
- `python3 -B tools/project.py check` (existing local maintenance; does not qualify new hosted behavior).
- Read baseline.json/baseline-state.json and privately retained source cache/hash verification. Never recurse into sealed or qualification archives.
- Parent owns qualification-cases.json. It must stay fixed once reviewed/frozen:15cases×3repeats×2arms and45directional saved-plan replays.
- Build and hosted calls are deliberately not review commands until approved at their gates.

## Author explanation

Inspect implementation/tests before HARNESS-REVIEW-AUTHOR.md and proposed-source.md when feasible. The latter necessarily provides source interpretation but must be verified against exact upstream bytes. Record preliminary concerns and any blindness limitation. Source graph generation ask-formly 2026-10-25T14:19:41Z does not cover this new batch; prior arrays harness exact-path coverage was not_tracked, so use direct source fallback and do not claim graph completeness.

Use independent-review in reviewer mode. This is review instance 1 of 3. Work from the bootstrap first and record preliminary review before reading the author explanation. Verify implementation and plan, run proportionate non-mutating checks, and return an evidence-backed verdict. Do not implement fixes, create further review instances or split workstreams.

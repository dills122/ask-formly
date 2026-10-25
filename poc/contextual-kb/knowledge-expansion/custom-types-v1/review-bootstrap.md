# Fresh Review Bootstrap

Review instance: 1 of 2 (second only if material fixes need verification).

## Objective and canonical request

User: “Proceed with the coverage inventory and first knowledge batch for custom field types and registration. Keep the working setup, models and installed DB unchanged, and evaluation sealed. Review the plan before building the candidate DB.”

Read POC AGENTS.md and STEERING.md; this explicit request allows separate proposal artifacts, not changes to active data or runtime. Read docs/development.md and docs/knowledge-pipeline.md.

## Repository and boundary

Repository /Users/dsteele/repos/ask-formly. Branch codex/readme-verified-branches, HEAD 881afd2 at preparation. This review targets only untracked additions under poc/contextual-kb/knowledge-expansion/custom-types-v1/. No implementation code changed; this is the batch and pre-build plan review. Check Git state yourself. Do not commit, stage, push, build any DB, change a file or open any sealed evaluation material. Models are out of scope and must not be changed.

## Independent first pass

Inspect README.md, PLAN.md, draft-authored/*.json, development-cases.json and actual accepted authored facts before reading review-author.md. Verify claims against upstream sources and code, not just our prose. Source-evidence.json includes archive hashes and exact file excerpts; the local upstream archive is local/ask-formly/upstream/5f099fddea6426b46a453866adf0fede5be0bcd7.tar.gz with matching snapshot directory. Do not execute upstream code. Read-only inspection is allowed outside POC; code import/wiring is not.

Record preliminary findings before reading author rationale. Review completeness, semantic support, no duplicate expansion, qualifications, comparison fairness, candidate isolation feasibility, and whether the plan stays bounded. Final report can be returned as text for the author to save.

## Coverage evidence

Graph Tier 2, project ask-formly: index dated 2026-10-16T13:38:17Z, unwatched. search_graph getMergedField|build_sources returned zero. check_index_coverage found the two compiler files untracked and upstream subtree excluded; exact upstream path checks confirmed excluded status. All cited compiler and upstream lines were read directly. Do not interpret graph absence as code absence; use direct source fallback for these paths.

## Proportionate verification

Source gate: python3 -B tools/project.py source (temporary-fixture tests; no installed DB rebuild). Batch lint can run by copying original nine authored files plus two draft files into a temporary directory, combining existing catalog records with source-evidence.json records, and invoking existing lint_sources with explicit paths. No build calls. Logs already under this proposal's test-output/. Hashes in baseline-state.json establish unchanged active authored/catalog/DB for this checkpoint. Do not read evaluation fixtures.

## Author explanation

Read review-author.md only after first-pass notes.

Use $independent-review in reviewer mode. This is review instance 1 of 2. Work from this bootstrap first and record a preliminary review before reading the Author Explanation. Then verify the explanation against the repository, review both the batch and its plan, run proportionate non-mutating checks, and return an evidence-backed verdict. Do not implement fixes, create further review instances, or split the work into new workstreams.

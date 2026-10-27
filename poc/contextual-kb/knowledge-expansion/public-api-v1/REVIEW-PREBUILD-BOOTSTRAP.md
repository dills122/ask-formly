# Fresh Review Bootstrap
Review instance: 1 of 3
## Review Objective
Review new public API/configuration source mappings, grading/cases and isolated build/test machinery BEFORE build. Return actionable findings and Ready/Not ready verdict. Do not build or run qualification.
## Repository And Worktree
/Users/dsteele/repos/ask-formly
## Base, Head, Branch, And Dirty State
Branch codex/n1-radio-native-promotion; HEAD250f83da2d93aababf27f169078807ff66f183ee. New batch is untracked; docs/knowledge-completion-backlog.md modified previously; many unrelated untracked old artifacts excluded.
## In-Scope Paths
poc/contextual-kb/knowledge-expansion/public-api-v1 only; compare copied helpers to completion-v1 as needed. Source verification and authored docs under api/ and configuration/; aggregate draft-authored and extra-evidence. Include adjudication.json when ready.
## Canonical Requirements And Plan
User: clarify grading rules and public API/configuration batch; verify pinned sources, isolated build/test/review; both runtimes/models/installed DB unchanged; evaluation sealed. PLAN.md, GRADING.md, cases.json, admission-spec.json.
## Exclusions
No existing candidate/runtime/model/DB/compiler/source changes. No global evaluation/qualification contents. Baseline is176 completion-v1 candidate, installed124 unchanged. No promotion/publish.
## Verification Commands
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/public-api-v1 -p 'test*.py'
Read cached exact-commit sources and verify authored claims/line hashes. No candidate build until review.
## Author Explanation
REVIEW-PREBUILD-AUTHOR.md; inspect scope/tests/code/source claims first and record preliminary notes before reading explanation. Write REVIEW-PREBUILD.md only; no implementation edits.

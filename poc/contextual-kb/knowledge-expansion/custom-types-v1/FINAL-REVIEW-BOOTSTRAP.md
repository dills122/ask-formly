# Fresh Review Bootstrap

Review instance: 3 of 3 for the isolated candidate build/comparison implementation flow. Final results are still being collected; perform the implementation/source audit now and wait for the author to supply the completed result report before issuing a final verdict.

## Review objective

Audit whether the isolated 46-to-56-fact expansion and its real-agent MCP comparison faithfully implement the frozen plan, preserve the accepted setup, and support the claimed result. Independently inspect source support, complete denominators, failures, answer judgments and equal-plan diagnostics. Do not turn a knowledge gain into an end-to-end pass if the predefined gate fails.

## Repository and worktree

`/Users/dsteele/repos/ask-formly`; branch codex/readme-verified-branches, HEAD 881afd2. Verify these values. All task work is untracked under poc/contextual-kb/knowledge-expansion/. No commits or publication requested.

## Scope and requirements

Read applicable AGENTS, README, docs/development and POC STEERING. User explicitly permits isolated candidate construction and tests, while preserving working setup/models/installed DB and sealed evaluation. PLAN.md and EXECUTION.md define the comparison contract. In scope: this custom-types-v1 directory, source drafts/evidence, build/harness/tests/reports, and the next-source inventory/proposal in ../SOURCE-COVERAGE.md and ../imported-guides-v1/. That next proposal has not been built and must not be represented as qualified.

## Exclusions

Do not read any sealed evaluation. Do not execute builds, training, hosted inference or change files. Never modify accepted code/models/authored inputs/DB. Do not create another reviewer or workstream. The existing test-output/qualification-1 is this experiment's fresh visible qualification, not the sealed evaluation; it is in scope. Avoid broad searches into other archived evaluation material.

## Verification

Read tests first. Run `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/custom-types-v1 -p 'test_*.py' -v` if appropriate. Source archive/hash checks, SQL read-only comparisons, freeze verification and packaged doctor checks are available. Hosted processes are still running; do not rerun them. Raw successful and failed development and qualification outputs are retained. Check current completeness before interpreting denominators.

## Author explanation

Record preliminary concerns before reading FINAL-REVIEW-AUTHOR.md. Completed report will be supplied in a follow-up during this same review instance. Return interim findings if useful, but do not declare final readiness while outcomes are pending.

Use $independent-review in reviewer mode. This is review instance 3 of 3. Work from this bootstrap first and record a preliminary review before reading the author explanation. Verify implementation and plan with proportionate non-mutating checks. Do not implement fixes, create further review instances, or split into new workstreams.

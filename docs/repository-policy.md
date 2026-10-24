# Repository policy

The primary project is the accepted Formly library MCP. This policy keeps routine changes reviewable without requiring a second maintainer for every PR.

## Branches and merges

| Setting | Policy |
| --- | --- |
| Default branch | `main` |
| Changes to main | Pull requests required, including for administrators |
| Required check | `source-checks`, emitted by the GitHub Actions app |
| Base freshness | Branch must be up to date before merging |
| Review approvals | Zero mandatory approving reviewers; no required code-owner or last-push approval |
| Review conversations | Must be resolved |
| Main history | Linear; force pushes and deletion disabled |
| Merge method | Squash only |
| Merged branches | Automatically deleted |
| Auto-merge | Available for eligible PRs, but must be explicitly enabled per PR |

Use descriptive short-lived branches (`docs/`, `fix/`, `feat/`, `chore/`); agent-created branches use `codex/`. Branch prefixes are conventions, not server-enforced name rules. Do not bypass a failing check by renaming it, changing required contexts, or weakening preservation checks.

Source checks do not run private models or qualify the live MCP. Runtime changes also need local checks in a provisioned checkout, as described in [development](development.md). GitHub protection settings are applied on the repository; this document records them but does not configure them automatically.

## Scope and artifacts

Keep models, installed DBs, environment directories, sealed evaluation and private archives out of public Git. Current frozen source/data boundaries remain in [AGENTS.md](../AGENTS.md). Historical failures remain in the history even when an approach is retired.

Use Issues for bugs and scoped proposals, and pull requests for code/documentation changes. Repository topics describe discovery categories, not supported-version guarantees. No release tags or public binary distributions are created until release criteria and original-code licensing are settled.

Maintainer reference: [GitHub's branch-protection API](https://docs.github.com/en/rest/branches/branch-protection).

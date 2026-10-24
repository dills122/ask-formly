# Contributing to ask-formly

ask-formly's primary implementation is the Formly library MCP under `poc/contextual-kb/`. Start with the [README](README.md), [knowledge pipeline](docs/knowledge-pipeline.md), and [development guide](docs/development.md).

## Open a useful issue

Use the bug-report or proposal form. Include the Formly version/UI adapter, a synthetic request or reproduction, expected behavior, and actual evidence. Distinguish missing knowledge from retrieval or answer failures when possible. Do not publish credentials, private application data, model weights or sealed evaluation material.

Propose scope before changing frozen knowledge, compiler inputs, model assets or the installed DB. A missing answer is not permission to rebuild or retrain them. Older application-inspection tools are retired; discuss a new need before restoring old experiments.

## Work in a branch

Branch from current `main` and use a short descriptive name: `docs/...`, `fix/...`, `feat/...`, or `chore/...`. Agent-created branches use `codex/...`. Open a PR with the problem, resulting behavior, tests run, and limitations. Draft PRs are welcome while work is incomplete.

Run source checks for documentation/source changes:

```sh
python3 tools/project.py source
```

Use a provisioned checkout for changes affecting runtime behavior and run:

```sh
python3 tools/project.py check
```

The [development guide](docs/development.md) lists prerequisites and explains the difference. Record checks you actually ran; do not claim model or answer quality from a source-only pass. Tests that compile knowledge use temporary fixtures, never the locked installed DB.

## Review and merge

`main` requires a PR, the GitHub Actions `source-checks` check on an up-to-date branch, and resolved conversations. A second approving reviewer is not mandatory at this stage. Maintain and Admin roles have a PR-only emergency CI bypass for runner outages; document the reason and local checks when using it. Other main-branch protections still apply. Review still matters: assess the change, preserve frozen boundaries and record independent review when the work calls for it. Squash merge keeps one focused commit per PR; merged branches are deleted automatically. See [repository policy](docs/repository-policy.md).

The project has not selected a license for its original code. Discuss contribution and licensing expectations with the maintainer before submitting substantial new code; upstream notices remain in force for their respective material.

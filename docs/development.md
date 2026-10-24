# Development

The repository has two separate implementations: the accepted library MCP under poc/contextual-kb, and the portable reference/indexing skill under skill/ask-formly. Do not copy implementation code between them as part of routine maintenance.

## Accepted local MCP

Use the existing POC environment:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/mcp_foundation/launcher.py doctor
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/packaging/check.py
```

The first command checks pinned runtime assets and local prerequisites. The second runs active unit/transport regressions without hosted model calls. Installed models/DB remain locked; do not rebuild or retrain them to make a check pass. See the [MCP setup guide](../poc/contextual-kb/mcp_foundation/README.md) for client configuration, authentication, latency and limitations.

## Portable skill

Use the repository's pinned Node/TypeScript versions and existing lockfiles. Standard commands remain:

```sh
npm ci --ignore-scripts --no-audit --no-fund
npm run check
```

The full check validates documentation links and portable source, runs applicable regressions, builds a bundle and exercises it. Follow the current script's explicit prerequisite errors for optional search/MCP environments. Do not skip missing dependencies or hide failed tests. Active tests live under tests/project-index, tests/mcp and tests/search; runtime and supplier fixtures remain separate from static evidence.

The historical Angular browser qualification retains two known failures, B06 and B13. Cleanup is not a new browser qualification and does not change those results. See [coverage](../skill/ask-formly/references/coverage.md) and [repository history](history/experiments.md).

## Evidence and cleanup

Keep concise current setup and conclusions in docs; keep new generated output under test-output. Repeats, annotations, retrieval metrics and final-answer quality are different measures. Preserve failures and uncertainty instead of regrading an old experiment after tuning.

Superseded POC implementations are recoverable from remote checkpoint e1e4e9c and verified local archives. Large raw runs, caches and older model variants are not part of the active source deliverable. Root evaluation/qualification and the sealed POC evaluation stay protected. Current accepted models/DB/code hashes are checked separately from archived whole-history freeze chains.

Do not regenerate removed experiments merely to satisfy historical scripts. Use the active regression runner; consult [packaging/recovery](../poc/contextual-kb/packaging/README.md) when a historical reproduction is actually needed. Keep credentials and provider output logs out of Git. No environment or package upgrades are implied by cleanup.

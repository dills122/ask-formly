# Development

The accepted library MCP and knowledge pipeline are under `poc/contextual-kb/`. The old application-inspection product is retired. See [knowledge sources and transpilation](knowledge-pipeline.md) before touching data-related code.

## Local qualification

From the repository root:

```sh
python3 tools/project.py check
# Equivalent convenience command:
npm run check
```

This verifies preserved source hashes and authored provenance, checks current documentation links, runs the compiler's temporary-fixture tests and packaging tests, runs the launcher doctor, and executes the 97 active MCP regression tests. It requires the existing compiler and MCP environments and installed runtime assets. It neither trains models nor calls hosted generation nor opens sealed evaluation. Models, DB and compiler inputs remain unchanged.

The separate model-worker environment is checked by doctor. A source-only clone must not silently skip missing runtime assets and claim local qualification.

## Source-only CI

```sh
python3 -m pip install 'markdown-it-py>=3,<5' 'PyYAML>=6,<7' -r poc/contextual-kb/mcp_v1/requirements-context.txt
python3 tools/project.py source
```

CI uses Python 3.13 and this narrower check. It validates source/provenance and compiler/package behavior and project settings/version resolution using temporary fixtures. CI separately runs real stdio transport against a fixture service. It does not qualify model inference, the installed DB, MCP transport or hosted generation. No models or sealed data are downloaded. The local compiler dependency specification and lockfile remain in the POC unchanged.

The new context tests use the MCP environment when present, otherwise the invoking Python environment. Install the context requirements there. See [project settings and version matching](project-settings.md) for focused asset-free commands.

For the real service, use the [setup guide](../poc/contextual-kb/mcp_foundation/README.md). For local recovery packaging, use [packaging guidance](../poc/contextual-kb/packaging/README.md). There is no active portable-skill release workflow.

## Boundaries

The data/DB layer and models remain locked. Do not run `python -m kbcompiler build` or `all` against the installed POC during maintenance. Compiler regressions build disposable fixture databases only. Any future authorized source change must explicitly update its preservation manifest; do not update hashes to conceal unexpected drift.

Retain fresh results under test-output and concise conclusions in docs. Historical B06/B13 browser failures remain historical failures; this cleanup does not requalify them. Repeated outputs, extraction scores, retrieval coverage and final-answer quality remain distinct measures.

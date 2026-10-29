# Development

The accepted library MCP and knowledge pipeline are under `poc/contextual-kb/`. The old application-inspection product is retired. See [knowledge sources and transpilation](knowledge-pipeline.md) before touching data-related code.

## Local qualification

From the repository root:

```sh
python3 tools/project.py check
# Equivalent convenience command:
npm run check
```

This verifies preserved source hashes and authored provenance, checks current documentation links, runs the compiler's temporary-fixture tests and packaging tests, runs both launcher doctors, and executes the 161 active MCP regression tests. It requires the existing compiler and MCP environments and installed runtime assets. It neither trains models nor calls hosted generation nor opens sealed evaluation. Models, DB and compiler inputs remain unchanged.

The separate model-worker environment is checked by doctor. A source-only clone must not silently skip missing runtime assets and claim local qualification.

## Source-only CI

```sh
python3 -m pip install 'markdown-it-py>=3,<5' 'PyYAML>=6,<7' -r poc/contextual-kb/mcp_v1/requirements-context.txt
python3 tools/project.py source
```

CI uses Python 3.13 and this narrower check. It validates source/provenance and compiler/package behavior and project settings/version resolution using temporary fixtures. The source command also runs the default model-free contract, ranking, response-budget, discovery and offline stdio fixture suites. CI separately runs settings transport against a fixture service. It does not qualify model inference, the installed DB, installed-service MCP transport or hosted generation. No models or sealed data are downloaded. The local compiler dependency specification and lockfile remain in the POC unchanged.

The new context tests use the MCP environment when present, otherwise the invoking Python environment. Install the context requirements there. See [project settings and version matching](project-settings.md) for focused asset-free commands.

For the real service, use the [dual-mode setup guide](../poc/contextual-kb/mcp_runtime/README.md). The new launcher defaults to model-free; the old model-backed launcher and runtime remain unchanged. Local check validates both doctors; source CI also runs the asset-free mode-selection tests. Consequently full local maintenance still requires the old model assets, even though running the model-free server does not. For local recovery packaging, use [packaging guidance](../poc/contextual-kb/packaging/README.md). There is no active portable-skill release workflow.

## Identifying a local package

Local packages identify themselves as development candidates, independently of
the published RC version. Compare `build_identity` in `ALPHA-MANIFEST.json`,
`doctor` and `help_formly`; MCP initialization reports the same `build_id`. The
runtime fingerprint hashes the canonical runtime manifest. Use the archive
SHA-256 to identify the complete distribution, including installer and docs.
The installed self-test checks handshake/help agreement with package metadata.
These identifiers establish which artifact is connected, not its qualification.

## Boundaries

The data/DB layer and models remain locked. Do not run `python -m kbcompiler build` or `all` against the installed POC during maintenance. Compiler regressions build disposable fixture databases only. Any future authorized source change must explicitly update its preservation manifest; do not update hashes to conceal unexpected drift.

Retain fresh results under test-output and concise conclusions in docs. Historical B06/B13 browser failures remain historical failures; this cleanup does not requalify them. Repeated outputs, extraction scores, retrieval coverage and final-answer quality remain distinct measures.

Versioned authoring uses schema2 through `kbcompiler/current_source.py`. Source CI
includes eight versioned compiler tests; local runtime checks also include scoped
retrieval/context and promotion wiring tests. Build only to a new isolated path:
`python -m kbcompiler build --database /path/to/new-candidate.sqlite`. Existing
outputs and the installed path are rejected; promotion is a separate operation.

## Alpha packaging checks

Source checks also run the asset-free package/installer regressions in `poc/contextual-kb/alpha/`. Building the [model-free alpha](../poc/contextual-kb/alpha/README.md) requires the provisioned DB; installing it downloads pinned dependencies into a new environment. Neither operation is a DB rebuild. Clean-install and caller smoke evidence is separate from source-only CI.

## Keep the working tree lean

The [linked examples candidate](linked-examples.md) adds asset-free catalog,
transport and regression-harness tests to source CI. Its separate browser fixture
and full-corpus replays are opt-in checks; the installed runtime and RC package do
not load the candidate.

Completed experiment runners and duplicate review handoffs belong in Git history,
not an ever-growing active test tree. Keep required source provenance at its
pinned path, source dispositions, current regression dependencies and concise
outcomes. Use ignored `test-output/` for raw runs and review handoffs, and a verified
local archive before removing uncommitted experiments. See [the knowledge cleanup
and history](history/knowledge-expansion.md). Do not prune a version-named module
solely because its name looks historical: current tests and runtimes may import it.

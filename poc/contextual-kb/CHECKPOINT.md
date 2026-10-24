# Remote POC source checkpoint

Start with [the accepted MCP foundation](mcp_foundation/README.md). It combines the frozen library-question planner, bounded wording adapter, advisory GLiNER extraction, full-question retrieval and bounded hosted selection. See [usability results](mcp_foundation/RESULTS.md) and [historical summary](history/EXPERIMENTS.md).

This checkpoint preserves POC source, contracts, tests, dependency locks and concise reports before cleanup. No experimental files were removed to create it. It excludes environments, model binaries, caches, raw run logs, generated DB build outputs and sealed evaluation. The diagnosed F01 regression fixture is retained explicitly because the wording tests require it.

The existing working checkout remains the qualified runtime. The pinned model/DB assets are recorded in mcp_foundation/foundation.json and preserved in a verified local recovery archive. They are not backed up by this source commit. See [packaging boundaries](packaging/README.md). Do not treat a source-only fresh clone as an already provisioned MCP server.

No global MCP configuration is changed. No models or DB were edited. Sealed evaluation was not opened. Repository-wide cleanup is a separate follow-up after this checkpoint is visible remotely.

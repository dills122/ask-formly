# Formly library MCP foundation

This is the primary implementation of ask-formly. The directory name is retained to preserve pinned paths. Start with [model-free alpha installation](alpha/README.md), [dual-mode development MCP setup](mcp_runtime/README.md), [knowledge sources and transpilation](../../docs/knowledge-pipeline.md), and [development checks](../../docs/development.md). Model-free is the new launcher's default; the original model-backed launcher remains available and unchanged.

Authored knowledge, corpus/evidence, compiler code and tests, installed DB, both frozen GLiNER adapters and the accepted runtime remain preserved. Data and models stay locked. Original source references under skill/ask-formly/references remain frozen provenance; the old application-inspection implementation is retired.

See [experiment history](history/EXPERIMENTS.md) for tested approaches, results and failed gates, and [packaging/recovery](packaging/README.md) for archived artifacts. Historically named runtime dependency directories remain because accepted code is pinned. Old whole-history harnesses require restoring their archived dependencies; use the current regression entry point for maintenance.

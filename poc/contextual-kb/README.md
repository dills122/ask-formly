# Contextual Formly knowledge POC

Use the [accepted MCP foundation](mcp_foundation/README.md). It preserves library questions and conditions, adds frozen advisory GLiNER spans, performs full-question retrieval and bounded selection, and returns stored evidence for the calling agent.

- [Current setup](mcp_foundation/README.md)
- [Results](mcp_foundation/RESULTS.md) and [independent review](mcp_foundation/REVIEW.md)
- [Experiment history](history/EXPERIMENTS.md)
- [Packaging and recovery](packaging/README.md)

The active runtime intentionally retains several historically named directories because their code or artifacts are dependencies. Other experiment branches and generated runs have been retired after a remote source checkpoint and verified recovery archive. Old report/script references to raw test-output or whole-history freeze chains refer to archived evidence, not files required by the current launcher.

The authored knowledge, compiler/DB layer, accepted models and sealed evaluation remain protected. No model training or DB changes are part of cleanup. The portable skill elsewhere in the repository is not a runtime dependency.

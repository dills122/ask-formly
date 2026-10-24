# ask-formly

A source-grounded information service for the **Formly library**, with a working local MCP POC and a separate portable skill.

## Current MCP foundation

Start with [setup and usage](poc/contextual-kb/mcp_foundation/README.md). The stable entry point is:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/mcp_foundation/launcher.py doctor
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/mcp_foundation/launcher.py serve
```

The MCP exposes `lookup_formly(request)`. It derives focused library questions, retains conditions, adds advisory GLiNER annotations, retrieves full questions and returns stored facts with citations. The calling agent explains the supported information and any gaps. It does not investigate application-specific components.

The current knowledge sample contains 46 authored facts for **Formly 6.3.12, core/Material**. The accepted setup passed bounded real-agent integration and local usability checks; that does not establish whole-library accuracy or production readiness. Model/DB assets and two installed Python environments are required. A source-only clone is not an already provisioned server.

- [Setup and client configuration](poc/contextual-kb/mcp_foundation/README.md)
- [Usability results](poc/contextual-kb/mcp_foundation/RESULTS.md) and [independent review](poc/contextual-kb/mcp_foundation/REVIEW.md)
- [POC experiment history](poc/contextual-kb/history/EXPERIMENTS.md)
- [Packaging and recovery boundaries](poc/contextual-kb/packaging/README.md)

## Portable skill and earlier indexing work

[skill/ask-formly](skill/ask-formly/SKILL.md) remains the separate portable Formly reference and application-indexing codebase. Its active source, regression tests and fixtures remain available; the library MCP POC does not import it. Do not confuse application source discovery with library knowledge coverage.

## Development and history

See [development](docs/development.md), [repository history](docs/history/experiments.md), and [documentation index](docs/README.md). Obsolete trial implementations, duplicate caches and generated run trees have recovery checkpoints rather than remaining in the active working tree. Known failed gates remain part of the history; sealed evaluation is not opened by cleanup.

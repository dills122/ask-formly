# ask-formly

A source-grounded **Formly library MCP**, built around the accepted implementation in `poc/contextual-kb/`. This is the primary project; the directory keeps its existing name to preserve runtime paths and pinned assets.

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/mcp_foundation/launcher.py doctor
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/mcp_foundation/launcher.py serve
```

`lookup_formly(request)` derives library questions, preserves conditions, adds advisory GLiNER annotations, retrieves using full questions, and returns selected stored facts with citations. The calling agent explains what the evidence supports and what is missing. It does not investigate application components.

The knowledge sample contains **46 authored facts across 9 documents for Formly 6.3.12 core/Material**. The authored knowledge, evidence corpus, transpilation/compiler code, DB, frozen models and current runtime are retained. Models and DB remain locked. Source-only clones require local asset provisioning; they are not ready-to-run servers.

- [Setup and agent configuration](poc/contextual-kb/mcp_foundation/README.md)
- [Knowledge sources and transpilation process](docs/knowledge-pipeline.md)
- [Development and checks](docs/development.md)
- [Readiness and limits](docs/readiness.md)
- [Experiment history and results](poc/contextual-kb/history/EXPERIMENTS.md)
- [Retired approaches and recovery](docs/history/experiments.md)

Older application-inspection tooling, supplier demos and competing knowledge-engine experiments are retired. Their high-level lessons remain in documentation; full historical artifacts are archived. The remaining `skill/ask-formly/references/` files are frozen knowledge provenance, not a second supported product.

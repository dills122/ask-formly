# Linked examples v1 — isolated candidate

**Deferred as of 2026-10-28.** Retain this candidate and its tests while current
facts and retrieval are refined. Further storage implementation and promotion
are deferred; see the [recorded proposal and priorities](../../../docs/linked-examples.md).

An opt-in example catalog and MCP entry point. Nothing here is loaded by the
released launcher or included in its package. The original fact database is
opened read-only and checked against a supplied SHA-256; examples are separate
reviewable JSON records and TypeScript files.

## Run the candidate

Use a Python environment with the repository's MCP context dependencies. Supply
the path and trusted SHA-256 of an existing baseline DB and a separate scratch
settings path. Do not rebuild the installed DB.

```sh
python poc/contextual-kb/linked_examples_v1/serve.py \
  --database /absolute/path/to/knowledge.sqlite \
  --sha256 f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09 \
  --settings /absolute/path/to/test-output/examples-settings.sqlite
```

This is a stdio MCP entry point for a separately configured development client.
It is not an installation or promotion command. Do not replace the demo client's
RC configuration. The candidate adds `get_formly_examples` to the existing four
tools. See [caller instructions](CALLER.md) and the tool schemas for selectors,
scope and pagination.

## Contents

- `examples/`: three original illustrations with fact links, conditions,
  prerequisites, limitations, complete code and verification metadata.
- `catalog.py`: strict record/link validation, bounded list/fetch and optional
  small references attached to fact packets without dropping evidence.
- `serve.py`: explicit candidate wrapper; the active MCP is unchanged.
- `fixtures/`: pinned browser harness for the example factories.
- [regressions/](regressions/README.md): public fixed-plan replay, separate grader
  and a single-call CLI for independent callers.

Run the asset-free candidate tests with the MCP Python environment:

```sh
python -B -m unittest discover -s poc/contextual-kb/linked_examples_v1
```

Source CI includes these tests. Actual Angular execution and read-only full-corpus
replays are separate checks requiring their respective dependencies/assets.
Generated output belongs in ignored `test-output/`.

See [candidate scope and promotion boundary](../../../docs/linked-examples.md).

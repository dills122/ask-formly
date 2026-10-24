# Knowledge sources and transpilation

The knowledge pipeline is part of the primary Formly MCP, not retired experimental material. Its inputs and implementation remain byte-preserved during cleanup.

## Preserved components

| Component | Responsibility |
| --- | --- |
| `poc/contextual-kb/authored/` | Nine controlled JSON knowledge documents containing 46 facts, conditions, limits, exact source quotes, evidence IDs and related-fact links. |
| `poc/contextual-kb/corpus/` | Imported source material and the pinned evidence catalog, including additional source documents used by the authored facts. |
| `skill/ask-formly/references/` | Original reference documents at the paths pinned by authored records. These are frozen provenance; their older application-workflow instructions are historical. |
| `poc/contextual-kb/kbcompiler/structured_source.py` | Validates controlled records, exact source hashes/quotes and evidence links, then compiles them into SQLite when explicitly authorized. |
| `poc/contextual-kb/kbcompiler/__main__.py` | Existing `lint`, `build`, `all` and read-only `inspect` CLI. The installed DB remains locked; only lint/inspection is permitted in routine maintenance. |
| `poc/contextual-kb/kbcompiler/pipeline.py` | Preserved Markdown import/transpilation path and its dependencies: source sections, citations, candidate blocks and proposals. This earlier import path is distinct from the controlled authored-fact compiler used by the installed DB. |
| `poc/contextual-kb/import-manifest.json` | Original source-import provenance. It is not permission to overwrite the current corpus. |
| `poc/contextual-kb/build/knowledge.sqlite` | Locked installed knowledge DB consumed by read-only retrieval. |
| `poc/contextual-kb/tests/` | Preserved compiler and earlier POC regressions. Current source checks explicitly run `test_pipeline.py` and `test_structured_source.py`; archived experiment tests are not treated as new qualification. |

The authored-source compiler checks the Formly version against the evidence baseline, rejects missing or changed origins, verifies exact quotes and citations, and validates related-fact targets. Compilation stores documents, facts, conditions, limits, source offsets and evidence relationships. Retrieval and the calling agent retain responsibility for selecting and explaining evidence; compilation does not prove that every possible Formly question is covered.

## Safe verification now

```sh
cd poc/contextual-kb
.venv/bin/python -B -m kbcompiler lint
```

`python3 tools/project.py check` from the repository root also validates these inputs and runs compiler tests against temporary synthetic fixtures. It does not regenerate the installed database. `packaging/source-files.json` pins the preserved source/provenance bytes; the accepted foundation manifest separately pins runtime assets.

Any future knowledge expansion must be an explicitly authorized change with source review, compiler tests, a separately generated candidate database and a comparison against the accepted DB before promotion. That expansion is not part of this cleanup.

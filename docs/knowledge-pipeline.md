# Knowledge sources and transpilation

For current coverage, remaining admission packages and the stopping criteria, use the [knowledge completion backlog](knowledge-completion-backlog.md). The batch histories below retain their original scope; their pending entries are not a combined outstanding-work count.

The knowledge pipeline is part of the primary Formly MCP, not retired experimental material. Its inputs and implementation remain byte-preserved during cleanup.

## Preserved components

| Component | Responsibility |
| --- | --- |
| `poc/contextual-kb/authored/` | Thirty-six controlled JSON knowledge documents containing 192 facts, conditions, limits, exact source quotes, evidence IDs and related-fact links. |
| `poc/contextual-kb/corpus/` | Imported source material and the pinned evidence catalog, including additional source documents used by the authored facts. |
| `skill/ask-formly/references/` | Original reference documents at the paths pinned by authored records. These are frozen provenance; their older application-workflow instructions are historical. |
| `poc/contextual-kb/kbcompiler/current_source.py` | Active schema2 lint/build interface, using the versioned compiler for applicability and evidence-release validation. The legacy `structured_source.py` validates an internal content/provenance projection and supports historical fixtures. |
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

## Admission and promotion

Future expansion requires explicit authorization: review pinned sources and dispositions; freeze cases and grading; compile to a new isolated output; compare against the installed baseline; independently review; then separately authorize guarded promotion. Use the [admission runbook](../poc/contextual-kb/knowledge-expansion/admission/RUNBOOK.md). Semantic curation remains a reviewed decision; reproducible compilation does not infer which claims should be admitted.

The foundation15 / discovery7 knowledge checkpoint contains 192 facts in 36 documents. The current model-free source manifest is discovery16; the published RC uses discovery8. The [response and retrieval changes](issue-21-followup.md) preserve those knowledge bytes and do not install a new DB. Its canonical inputs reproduce the installed DB bytes and all eight tables. See the [installed checkpoint](../poc/contextual-kb/knowledge-expansion/promotion-v13/RESULTS.md) and [source checklist](../poc/contextual-kb/knowledge-expansion/promotion-v13/CHECKLIST.md).

N1–N7 and the public API follow-ups are complete for the bounded retained-source milestone. See the [coverage and exclusions](knowledge-completion-backlog.md). Batch-local pending entries are historical and must be reconciled against this current coverage before proposing another addition.

Earlier batch counts, failures and lessons are summarized in [knowledge expansion history](history/knowledge-expansion.md). Full historical runners and review packets remain in Git; they are not current setup instructions. Required source provenance, compiler/seeding code and active regression helpers remain in place.

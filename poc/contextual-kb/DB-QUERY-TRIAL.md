# Direct database query trial

## Purpose and boundary

This follow-up tests database operations a future Formly MCP could issue after
it has chosen search terms. It does **not** choose those terms from a question,
generate an answer, or measure an MCP. The [ten questions](QUESTION-TRIAL-CASES.md)
and [explicit query fixture](DB-QUERY-TRIAL-CASES.json) remain separate: each
fixture entry contains two designer-supplied FTS5 `MATCH` expressions and the
fact IDs considered necessary for this narrow reachability check.

The two earlier content gaps received five new facts. The pinned default-value
demo supports model initialization as the preferred starting point, and core
default logic supplies the undefined-value condition. A qualifying changed
model input can trigger a Formly rebuild; the source does not make a field
default reactive or require a hook. The pinned introduction demo shows a custom component
registered under `types`, selected by a field's `type`, with `key` linking its
value to the model. These additions are in `authored/initial-values.json` and
`authored/custom-component-use.json`; their source text and evidence IDs are
local to this POC. They are source-data additions, not an AI extraction system.

## Query shapes exercised

1. FTS5 indexes each fact's claim, context, conditions, limits, document title,
   and summary at seed time. It does not index the source quote. The candidate
   query uses a parameterized `MATCH`, exact Formly version and adapter filters,
   `bm25(facts_fts)` order, and a five-row limit per expression.
2. For each candidate, a second SQL read follows outgoing `see_also` links one
   hop. The trial does not infer new links or traverse inbound links.
3. The packet read joins the selected fact to its document metadata, then reads
   its cited evidence records and outgoing links. It retains claim, conditions,
   limits, source quote and offsets, version, adapter, and source hash.

The executable SQL is in [db_query_trial.py](kbcompiler/db_query_trial.py).
Its input is the frozen fixture, not the natural-language question text.
The [machine result](../../test-output/contextual-kb-db-query-trial.json) retains
every returned packet for inspection.

## Observed result

The active seed contains **9 authored documents, 46 facts, 46 FTS rows, 20
cited evidence records, and 32 fact links**. All 46 indexed rows match their
authored inputs in the read-only audit. A fresh rebuild was logically identical
to the active DB across normalized tables and FTS rows. All 20 cited evidence
records matched their file hashes (18 pinned upstream file records and two records in
the portable examples reference). The isolated suite passed **38 tests**;
older fact-trial tests still emitted SQLite `ResourceWarning` messages. The
repository-wide `npm run check` gate also passed.

| Check | Result |
| --- | ---: |
| Required fact IDs in direct candidates | 6/10 questions |
| Required fact IDs after one outgoing link hop | 7/10 questions |
| Returned packets with cited evidence | 56/56 packets |

The three remaining required-ID misses were:

| Question | Miss after one hop | Diagnostic probe, outside frozen score |
| --- | --- | --- |
| Q2, hide and disable | `conditional-hide-target` | `expressions hide` directly retrieves it; broad `hide` filled the five-row candidate limit first. |
| Q4, custom props and Material | `core-type-needs-material-bridge` | `Material FieldType` retrieves it. The frozen `Material prop` expression requires a `prop` term that this fact lacks. |
| Q9, inherited defaults | `type-registration-options` | `defaultOptions` directly retrieves it; the frozen expressions did not. |

The diagnostic probes did not change the fixture or the 7/10 result. An exact
fact-ID miss is a reachability failure under these supplied terms and limits;
it does not by itself prove that a generated answer would be wrong. Conversely,
finding the IDs does not prove a generated answer would include every condition
or be correct. This trial does not establish question-dissection quality,
semantic retrieval, agent accuracy, or end-to-end latency.

## Reproduce

From `poc/contextual-kb/`:

```sh
.venv/bin/python -m unittest discover -s tests -q
.venv/bin/python -m kbcompiler all
.venv/bin/python -m kbcompiler.structured_audit
.venv/bin/python -m kbcompiler.db_query_trial > ../../test-output/contextual-kb-db-query-trial.json
```

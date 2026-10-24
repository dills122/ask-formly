# Contextual knowledge POC: data foundation and DB status

**Status (21 October 2026):** The source-format, compilation, seeding, and
direct DB-query layer is **workable for this POC and paused for now**. We have a
repeatable way to turn controlled Formly knowledge records into one queryable
SQLite database. This is a bounded result for the selected Formly v6.3.12
material, not a claim that open-ended questions or MCP answers work yet.

This document records what we built, why the source format changed, how each
layer works, and what the trials actually established. The isolated implementation
lives under [`poc/contextual-kb/`](README.md). It uses compiled Formly knowledge
from the portable skill as source material; it does not reuse code from earlier
knowledge-engine POCs.

## The path through this working session

| Stage | What we tried and learned | Result |
| --- | --- | --- |
| Import existing material | Imported three Formly knowledge guides and their K/E evidence catalog into a uniform Markdown corpus. The first script preserved source spans, citations, and headings. | 16 heading units and 43 smaller candidate blocks, but those blocks were not reliably single facts. See the [extraction spike](EXTRACTION-SPIKE.md). |
| Try structural decomposition | Table rows yielded nine fact *proposals*. Thirty-four blocks stayed unresolved. Some rows had no direct evidence link, and mixed prose could detach a condition from its claim. | We did not promote these proposals to authoritative facts. |
| Define controlled sources | Introduced one JSON document per topic/version/adapter with narrow `facts`, explicit conditions, limits, retrieval context, exact source quote, evidence IDs, and `see_also` links. | The first two-topic trial seeded 13 facts with matching spans and valid links. See the [format trial](SOURCE-FORMAT-TRIAL.md). |
| Expand the sample | Reworked selected source passages into seven authored topic files and 41 facts spanning defaults, expressions, hiding, props, registration, hooks, wrappers, and Material boundaries. | Manual examination of ten developer questions found eight supported by the stored facts and two partially covered. This assessed data coverage, not retrieval. See the [expanded trial](EXPANDED-SOURCE-TRIAL.md). |
| Fill the two data gaps and query the DB | Added two POC-local source documents grounded in pinned Formly examples and five facts about initial values and custom component use. Built an FTS5 row for every fact and ran supplied queries against the DB. | Current seed: nine documents and 46 facts. The [direct-query trial](DB-QUERY-TRIAL.md) reached all required IDs for 6/10 questions directly and 7/10 after one link hop. |

The current `authored/*.json` files are the **controlled source of truth for
compilation**. Creating those fact records from prose was a bounded authoring and
review exercise. The active compiler does **not** automatically turn arbitrary
Markdown into semantically correct facts. The older Markdown block compiler
remains in [`kbcompiler/pipeline.py`](kbcompiler/pipeline.py) for the historical
trial and regression tests; it is not the active CLI or DB path. There are no
hand edits to the generated database.

## The current data flow

```text
Pinned Formly v6 source/examples
         │
         ▼
Compiled knowledge passages + evidence catalog
         │ selected, source-grounded authoring
         ▼
authored/*.json  ──► strict lint ──► validated fact records
                                          │
                                          ▼
                               atomic SQLite rebuild
                                          │
                                          ▼
                   documents + facts + evidence + links + FTS5
                                          │
                            read-only audit and DB trial
```

### 1. Knowledge and evidence inputs

Seven topic records derive from selected passages in the portable
[`skill/ask-formly/references/`](../../skill/ask-formly/references/) material.
Two more derive from the POC-local
[`initial-values.md`](corpus/initial-values.md) and
[`custom-type-use.md`](corpus/custom-type-use.md), which cite pinned Formly
examples and implementation. The [`evidence-catalog.json`](corpus/evidence-catalog.json)
maps K/E IDs to the pinned v6.3.12 source/reference snapshot; the
[`sources.md`](corpus/sources.md) file documents the added evidence links.

Each authored document names its exact `derived_from.path` and SHA-256. Each
fact carries a verbatim `source_quote` from that file and one or more cited
evidence IDs. The quote gives us an exact location in the compiled source; the
K/E record points to the underlying Formly source or example. Matching both is
a provenance check. It cannot prove by itself that the underlying code entails
every word of the claim.

### 2. Controlled authored format

The active inputs are the nine files in [`authored/`](authored/). A document has
`id`, `title`, `formly_version`, `adapter`, `summary`, `derived_from`, and `facts`.
A fact has:

| Field | Role |
| --- | --- |
| `id`, `claim` | Stable fact identity and the narrow statement to return. The DB ID is `document-id/fact-id`. |
| `conditions`, `limits` | Qualifications and explicit boundaries that travel with the claim. |
| `context` | Fact-specific search text; it does not become evidence. |
| `source_quote`, `evidence_ids` | Exact compiled passage and its K/E references. |
| `related` | Explicit `see_also` pointers to other facts; no links are inferred. |

For example, [`initial-values.json`](authored/initial-values.json) separates
model initialization, `defaultValue` fallback, and later changed-model behavior
into three facts. The later-model fact carries the condition that the changed
input passes Formly's change check and the limit that this does not establish
reactivity for arbitrary `defaultValue` changes. This is the intended fact size:
one useful behavior or rule with its necessary qualification, with links when
another fact supplies adjacent detail.

Document summaries and fact context are search aids. The claim, condition,
limit, source quote, and evidence record remain distinct so retrieval can use
extra wording without silently upgrading that wording into authority. We use
JSON because the compiler can parse and validate an exact object shape; this
trial has not shown that JSON is the best future authoring interface.

### 3. Lint and compilation

The active CLI is [`kbcompiler/__main__.py`](kbcompiler/__main__.py), calling
[`structured_source.py`](kbcompiler/structured_source.py). `lint` checks without
writing. `build` validates and seeds. `all` runs both. The current checks reject:

- malformed JSON, duplicate JSON keys, missing or unknown fields, invalid IDs,
  duplicate document/fact IDs, and unsupported schema versions;
- a document version different from the evidence catalog baseline, a source
  path outside this repository, a missing source, a changed source hash, or
  non-UTF-8 source text;
- a quote that is absent or appears more than once in its source, missing or
  duplicate evidence IDs, evidence IDs not cited in that quote, and broken,
  self-referential, or unsupported fact links.

Validation reads the source files again on each build. A source change therefore
requires a corrected authored record and a full rebuild, followed by the audit.
The script locates the exact quote offsets in the source and writes them into
the DB. It does not split claims, generate summaries, judge claim truth, or
choose which concepts a user question means.

### 4. Database and search index

`build` creates a temporary SQLite file under `build/`, enables foreign-key
checks, populates it, checks references, commits, then atomically replaces
`build/knowledge.sqlite`. If validation or seeding
fails, the previously built DB remains in place. The DB is generated and
ignored by Git; it is not a second authored source.

| Table | Stored purpose |
| --- | --- |
| `build_info` | Schema version and digest of the catalog, authored JSON, and source bytes used for this build. |
| `documents` | Topic title, version, adapter, summary, source path, and source hash. |
| `facts` | Claim, conditions, limits, context, exact quote/offsets, and `authored` status. |
| `evidence`, `fact_evidence` | Only cited catalog records and their fact links. |
| `fact_links` | Explicit directed `see_also` edges. |
| `facts_fts` | SQLite FTS5 index using `unicode61` over claim, context, conditions, limits, document title, and summary. `fact_id` is unindexed. Source quotes are kept for evidence packets, not indexed. |

This is **one** database containing both authoritative records and a derived
lexical search index. There are no embeddings, vector index, or separate search
database in this POC. Current documents are scoped to Formly 6.3.12, with
`core` or `material` adapter labels. The direct query filters version and
adapter before ranking, so the stored scope is part of query behavior.

### 5. Read-only audit and direct DB queries

[`structured_audit.py`](kbcompiler/structured_audit.py) independently compares
the DB's documents, facts, source offsets, FTS rows, evidence, links, and input
digest to the authored files. It also runs SQLite integrity and foreign-key
checks. The current audit reports **9 documents, 46 facts, 46 indexed facts, 20
cited evidence records, 63 fact-evidence links, and 32 fact links**, with all 46
quotes at the expected offsets. A fresh rebuild produced the same logical rows;
this is a logical repeatability claim, not a byte-for-byte SQLite-file claim.

The separate [`db_query_trial.py`](kbcompiler/db_query_trial.py) exercises the
read path a future MCP could use. Its fixture supplies two FTS5 `MATCH`
expressions per question, an exact version, permitted adapters, and a five-row
limit **per expression**. SQL uses parameterized `MATCH`, `bm25` order, and an
ID tie-break. It unions the candidate IDs, follows one outgoing `see_also` hop,
then reads a packet with the claim, qualifications, source span and hash,
evidence records, and links. The ten natural-language prompts are kept in
[`QUESTION-TRIAL-CASES.md`](QUESTION-TRIAL-CASES.md); the actual supplied query
strings and required fact IDs are in
[`DB-QUERY-TRIAL-CASES.json`](DB-QUERY-TRIAL-CASES.json).

| Current check | Observed result | Interpretation |
| --- | ---: | --- |
| Required fact IDs found directly | 6/10 questions | With designer-selected terms and the frozen row limits. |
| Required fact IDs found after one link hop | 7/10 questions | Explicit links rescued one more case. |
| Returned packets with cited evidence | 56/56 packets | Packet provenance was present; answer correctness was not assessed. |
| Isolated POC tests | 38 passing | Structural, seeding, audit, and direct-query regressions. Older trial tests still emit SQLite `ResourceWarning` messages. |

The recorded direct-query trial also checked the source-file hashes for all 20
cited evidence records and passed the repository-wide `npm run check` gate.
Those checks support the selected seed's provenance and integration; they are
not a semantic proof of every natural-language claim.

The remaining misses are specific: a broad `hide` query filled Q2's candidate
limit before the conditional-hide fact; Q4's `Material prop` terms excluded the
Material-bridge fact; Q9's terms missed type-registration options. Targeted
diagnostic searches could retrieve each missed fact, but they did not alter the
frozen 7/10 result. These observations motivate the next question-to-query
layer; they are not evidence that a question planner already exists.

## What is settled for now, and what is still unproved

**Workable data/DB baseline:** controlled fact records can be validated,
re-seeded, audited, searched lexically, expanded through explicit links, and
returned as evidence-bearing packets. We are pausing changes to this foundation
while testing the next layer against it. Source corrections remain possible
when an actual factual error is found.

**Unproved:** automatic source-to-fact extraction; semantic entailment of every
claim by its cited code; coverage of the full Formly corpus or other versions;
open-ended question decomposition; semantic/vector retrieval; MCP transport;
fact selection by an agent; final answer completeness, concision, accuracy, or
end-to-end latency. The two answerability trials and DB trial measure different
parts of that path and should not be combined into an answer-accuracy score.

## Reproduce the current foundation

From `poc/contextual-kb/` (Python 3.10+ and `uv`; the project is defined in
[`pyproject.toml`](pyproject.toml) and locked in [`uv.lock`](uv.lock)):

```sh
uv sync --frozen
.venv/bin/python -m unittest discover -s tests -q
.venv/bin/python -m kbcompiler all
.venv/bin/python -m kbcompiler.structured_audit
.venv/bin/python -m kbcompiler.db_query_trial > ../../test-output/contextual-kb-db-query-trial.json
```

The last command writes a local, ignored trial artifact; create `test-output/`
if it is absent. `all` replaces the generated database from the controlled
inputs. `inspect` can print the seeded facts without changing it. The current
[review boundary](REVIEW-SCOPE.md) keeps this foundation separate from the
question-planning and answer-generation work that follows.

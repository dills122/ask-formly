# Question-layer bounded iteration

## Boundary

This slice changes only the isolated POC's question-to-query code, its tests,
trial harness, and this record. It reads the existing seeded SQLite database;
it does not change authored facts, schema, seeding, or the database file. It is
not an MCP serving path and does not assemble a cited answer.

The question layer preserves the full question for the existing hybrid
FTS5/dense retrieval, creates parameterized FTS5 probes for individual and
paired question terms, keeps exact API spellings, and optionally reranks small
probe hit lists with a local FastEmbed cross-encoder. It returns at most eight
**unverified candidate IDs**. The FTS5 probes filter to pinned Formly 6.3.12
core/Material facts; explicit mismatched Formly versions and named unsupported
UI adapters stop retrieval. The adapter names come from the [pinned v6 getting
started guide](https://v6.formly.dev/docs/guide/getting-started/). Its gate
covers those named adapters and package paths, not arbitrary custom renderers.
The final candidate list is also filtered against the eligible index IDs. The
cross-encoder uses `Xenova/ms-marco-MiniLM-L-6-v2` from a local cache.

This architecture follows [Microsoft's hybrid retrieval and reciprocal-rank
fusion guidance](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking/)
for combining lexical and vector candidate lists, and [Qdrant's FastEmbed
reranker guidance](https://qdrant.tech/documentation/fastembed/fastembed-rerankers/)
for reranking a retrieved subset. Those references justify the retrieval
pattern; the trial below determines whether this implementation works here.

## Fixed trials and results

The exposed `QUESTION-PILOT-CASES.json` was already used during implementation.
The separate `QUESTION-LAYER-FRESH-CASES.json` was authored from the source
facts by a second agent without seeing question-layer code or trial outputs,
then saved before the first run. `QUESTION-LAYER-CORRECTED-CASES.json` preserves
a correction to exposed Q2's required IDs without editing the old fixture:
Q2 asks about the hidden control, so the control-unregistration fact is required.
All three v6 results were run against the same code and database hashes,
recorded in each JSON artifact under `test-output/`.

| Set | Complete required-ID sets | Negative empty results | Query-call total | Startup |
| --- | ---: | ---: | ---: | ---: |
| Exposed pilot | 13/13 | 2/2 | 0.597 s / 15 cases | 0.907 s |
| Fresh transfer | 2/5 | 0/1 | 0.368 s / 6 cases | 0.832 s |
| Corrected Q2 | 0/1 | n/a | 0.009 s / 1 case | 0.873 s |

The timing covers this local layer's calls, not MCP transport, fact-packet
assembly, or final answer generation. Required-ID coverage is retrieval
coverage, not factual answer accuracy. Exposed Q2 is still counted complete
under its original incomplete gold set; the corrected result misses
`hiding-and-visibility/hide-unregisters-control`.

The fresh misses are:

- F1: `defaults-and-resets/reset-model` was found by a FTS pair probe but did
  not survive the eight-ID selection.
- F2: `hiding-and-visibility/hide-unregisters-control` was found by the
  `control` probe but did not survive selection.
- F5: `custom-component-use/registered-component-selected-by-type` appeared
  in the larger hybrid list and is linked from another selected fact, but did
  not survive selection.
- F6 asks for an HTTP/RxJS prescription absent from the authored facts. The
  layer returned related initial-value IDs with `candidates_unverified`.

As a diagnostic only, the union of the first 16 hybrid IDs and all FTS probe
hits contains every required fact for F1-F5 and corrected Q2. Those unions
contain 17-37 IDs per question, so they are not viable concise packets. This
distinguishes **query reachability** from **candidate selection**. The current
selection reserves too much of its eight-ID budget for a broad full-question
ranking and cannot establish whether topical matches answer an unsupported
question. The next substantive design step is obligation-aware selection and
answerability checking, evaluated on new questions before claiming a gain.
Do not tune the ranking against these now-exposed cases and call it validated.

## Checks and reproduction

Run from `poc/contextual-kb` with the existing seed and local model cache:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -q
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m kbcompiler.question_layer_trial --output ../../test-output/contextual-kb-question-layer-v6-exposed.json
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m kbcompiler.question_layer_trial --cases QUESTION-LAYER-FRESH-CASES.json --output ../../test-output/contextual-kb-question-layer-v6-fresh.json
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m kbcompiler.question_layer_trial --cases QUESTION-LAYER-CORRECTED-CASES.json --output ../../test-output/contextual-kb-question-layer-v6-corrected.json
```

The isolated suite passed 60 tests. The scope bugs found in read-only
review were reproduced as failing tests before their fixes: minor/patch
Formly version conflicts were silently answered as 6.3.12, and link expansion
could include an off-scope fact; explicit unsupported UI adapters also passed
through. These now pass. The SQLite SHA-256 before and
after this work is `3cdef0fc65e7afd747d3283adfdc47346ecfd64abd7d555d469fb982a2f84ea3`.

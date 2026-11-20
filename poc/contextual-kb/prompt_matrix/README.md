# Prompt matrix: our own model-free flow check

A small, repeatable harness for asking "does the real model-free flow actually
find the right fact for a question a developer would plausibly ask?" It is
**not** sealed evaluation — `planner_cases/sealed/`, `evaluation/` and
`qualification/` stay separate and untouched. This is an informal dev tool we
can extend and re-run as retrieval, the question layer, or the repair/discovery
wrapping changes.

## What it exercises

`run.py` drives the exact composition the real launcher serves for model-free
mode (traced while building this):

```
mcp_runtime.launcher.start_model_free
  -> parity_v1.serve_discovery.create_discovery_server
     -> model_free_repair_v1.serve.create_server
        -> model_free_v1.candidate.Store / Service
```

For each case in `cases.json` it calls `service.lookup(request, plan)` exactly
as a calling agent would, then — if the expected fact wasn't on the first
page — calls `discover()` to check whether a real caller following the
documented protocol (`lookup_formly` then `discover_formly_candidates`) would
still find it. Three outcomes per case:

- **direct_hit** — the expected fact came back on the first `lookup_formly` call.
- **discoverable_only** — not on the first page, but present among discovery's
  omitted candidates. The flow works, but costs the caller an extra round trip.
- **missed** — not found either way. A real retrieval gap.

Read-only against the installed DB; no model-backed/hosted calls, no provider
usage.

## Running it

```sh
cd poc/contextual-kb
.venv/bin/python -B prompt_matrix/run.py
```

Prints a summary and a list of anything that wasn't a direct hit; full detail
lands in gitignored `test-output/results.json`.

## Adding cases

Each entry in `cases.json` is a `{id, request, adapter, expected_fact_ids}`
object. Pick `expected_fact_ids` by reading the actual claim text in
`poc/contextual-kb/authored/` or querying `build/knowledge.sqlite` directly —
don't guess. Phrase `request` the way a developer would actually ask, not as
a restatement of the stored claim text; otherwise lexical retrieval is being
tested against itself.

## Findings from the first run (18 cases, 2026-11-19)

**17/18 direct hits, 1 discoverable_only, 0 missed.** The one weak case:
`json-schema-conversion-entrypoint` ("What function do I call to convert a
JSON Schema into Formly field config, and what module does it come from?")
didn't surface `json-schema-conversion/conversion-api` on the first page.
Investigated and traced to two separate causes in `model_free_v1/candidate.py`:

1. `Service.lookup` interleaved ranked candidates at a fixed depth of 4 per
   question, regardless of `max_facts`. For this single-question plan the
   correct fact actually ranked 11th (confirmed by calling `store.search`
   directly) but the first page only ever looked at the top 4 per question.
2. The FTS index (`tokenize='unicode61'`, no stemming) doesn't connect the
   query's "convert" with the document's "conversion" — different tokens,
   no match. Tested switching to `tokenize='porter unicode61'`: it fixes the
   `field`/`fields` plural mismatch but does *not* fix `convert`/`conversion`,
   since Porter doesn't unify irregular derivational forms.

Fixed (1) — see STEERING.md's 19 November 2026 authorization — by scaling
depth to `ceil(max_facts/len(questions))` instead of a fixed 4, so a
single-question plan can use its full budget while multi-question plans keep
the same fairness they had before. Re-run after the fix: **18/18 direct
hits.**

(2) is also now fixed, query-side: `candidate.py`'s `expression()` expands a
query word to an FTS `(... OR ...)` group over a small table of irregular
verb/noun pairs mined from the authored corpus itself — `convert`/`conversion`,
`extend`/`extension`, `emit`/`emission`, `retain`/`retention`,
`subscribe`/`subscription` — gated to the `improved` strategy only (the frozen
`basic` comparison arm is untouched). `conversion-api`'s rank for the same
question improved from 11th to 8th. Not a general stemmer: the table is
bounded to confirmed corpus cases, so a different irregular pair elsewhere
would still need its own mining pass before it's covered. Rank 8 clears the
current single-question depth of 16, but would still miss a narrower
per-question depth (e.g. a 2-question plan's depth-8 cutoff) — flagged, not
chased further, since no case found so far actually needs it.

**Unrelated but real: `model_free_v1/baseline-state.json`'s `installed_db_sha256`
is stale.** It doesn't match the actual `build/knowledge.sqlite` on disk
(confirmed by hash), while `mcp_runtime/model-free.json`'s pin for the same
file does match. The real launcher is fine — it reads the second file. But
`model_free_v1/server.py`'s and `model_free_repair_v1/serve.py`'s own `main()`
CLI entrypoints default `--sha256` from the stale file, so running either
standalone today raises `IntegrityError` even though the installed DB is
correct. This harness works around it by reading `mcp_runtime/model-free.json`
directly (see `build_service()`). Not fixed here — surfacing it, since fixing
a pin file touches exactly the kind of manifest-sync question that deserves
its own look rather than a silent edit.

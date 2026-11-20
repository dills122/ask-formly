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
still find it. Three outcomes per fact-seeking case:

- **direct_hit** — the expected fact came back on the first `lookup_formly` call.
- **discoverable_only** — not on the first page, but present among discovery's
  omitted candidates. The flow works, but costs the caller an extra round trip.
- **missed** — not found either way. A real retrieval gap.

Two more case shapes exercise paths a single-question lookup never touches:

- A case with `"questions": [{"question": ..., "expected_fact_ids": [...]}, ...]`
  instead of a single `request`/`expected_fact_ids` builds a real multi-question
  plan and checks each sub-question's own delivered/discoverable/missed outcome
  (the case's overall result is the worst of its sub-results). This is the only
  way any case exercises `Service.lookup`'s per-question depth split with more
  than one question.
- A case with `"expect_status"` instead of `expected_fact_ids` (optionally with
  `"formly_version"` to force an unsupported one) checks the packet's `status`
  directly — **status_match**/**status_mismatch** — for questions that should
  never return a fact at all (genuinely out-of-corpus, or an unsupported version).

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

Each entry in `cases.json` is normally a `{id, request, adapter, expected_fact_ids}`
object; see "What it exercises" above for the `questions`/`expect_status`
variants. Pick `expected_fact_ids` by reading the actual claim text in
`poc/contextual-kb/authored/` or querying `build/knowledge.sqlite` directly —
don't guess; a fact that doesn't exist, or exists under a different doc/adapter,
is a silent no-op in `store.records`'s scope check, not a loud error, so verify
mechanically (doc exists, fact id exists under that doc, adapter matches) before
trusting a case. Phrase `request` the way a developer would actually ask, not as
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

## Findings from the expanded run (115 cases, 2026-11-19)

Grew the matrix from 18 to 115 cases: at least 1-2 cases per authored document
(covering all 36, not just 15), each fact-seeking case checked against the real
corpus mechanically (doc exists, fact id exists under that doc, adapter matches
— 0 errors across all 92 added cases) before being trusted, plus 5 cases testing
scenarios the original 18 never touched: 2 multi-question plans (exercising
`Service.lookup`'s per-question depth split for real, not just single-question),
one deliberately out-of-corpus nonsense probe and one realistic-but-uncovered
question (both `expect_status: "no_evidence"`), and one explicitly unsupported
Formly version (`expect_status: "unsupported_scope"`).

**Result: 111/115 direct_hit, 1 discoverable_only, 2 status_match, 1
status_mismatch, 0 missed.** Two new findings, both genuine, neither fixed here:

1. **`field-key-type-independence` (discoverable_only, rank 18).** "Do a field's
   key and type have to match, or are they actually unrelated settings?" against
   `custom-component-use/key-is-model-type-is-renderer` ("A field key links its
   value to the model, while a string type selects a registered field type
   name."). None of "match", "unrelated", "settings", or "they" appear in the
   claim at all — this isn't a vocabulary/synonym gap like `convert`/`conversion`,
   it's the question asking the claim's *implication* rather than sharing its
   words. No lexical trick closes this; it's the actual ceiling of pure
   lexical/BM25 retrieval without semantic embedding, which is exactly what the
   model-free pivot traded away. Reported, not chased.

2. **`signature-pad-not-covered` (status_mismatch: `ok` with 16 facts, not
   `no_evidence`).** A realistic question about a feature genuinely absent from
   the corpus ("Does Formly ship a built-in signature-pad field type...")
   returned 16 fully unrelated facts (`public-api-contracts/wrapper-lookup-missing-name`,
   `model-scope/built-field-links`, ...) as `status: "ok"` candidates instead of
   `no_evidence`, because the broad-OR fallback route matches on any single
   shared word and words like "field"/"type"/"built" are in nearly every fact.
   Confirmed how permissive this is: even nonsense sentences return `ok` with
   several facts as long as they contain one real corpus word (e.g. "provide");
   only a sentence built entirely from words absent from the corpus's ~1,962-word
   vocabulary (the nonsense probe case) actually produces `no_evidence`. In
   practice this means a calling agent essentially never gets an honest "nothing
   relevant exists" signal — it always has to do its own relevance judgment, even
   for a fully out-of-scope ask. This is a real recall-vs-precision tradeoff in
   the existing "candidates, not answers, caller assesses relevance" design, not
   a bug — flagged as retrieval behavior that would need its own authorization
   to tighten (e.g. a minimum relevance floor on the broad route), same as the
   ranking-cap and stemming fixes above.

   **Investigated a fix (2026-11-19), didn't ship one.** Tried two gates on the
   broad-OR route, calibrated against all 112 real single-question cases plus 9
   deliberately-irrelevant probes, not just the one signature-pad example:
   - *Require ≥2 shared words instead of any single word*: doesn't work. `field`
     alone matches 104/192 facts and `type` matches 49/192; two maximally-generic
     words co-occurring still clears a ≥2 threshold on completely unrelated facts.
   - *Gate on the broad route's best bm25 score* (lower = better match): the
     worst score among the 112 genuine cases is -8.50 (`form-state-purpose`);
     the best (least-bad) score among the irrelevant probes is -5.59 — looks
     separable at first. But pulling more irrelevant samples breaks it: "does
     Formly support drag-and-drop array reordering" scores -10.41 and "built-in
     undo and redo" scores -10.24, both *more negative* (better-looking) than our
     worst genuine case. The genuine and irrelevant score ranges overlap. Any
     threshold strict enough to catch those two also kills real cases like
     `expression-controls-disabled` (-10.50) and `default-value-eligibility`
     (-10.68); any threshold loose enough to spare those lets several irrelevant
     probes through anyway.

   No safe numeric or structural gate was found. For this corpus's vocabulary,
   bm25 magnitude alone doesn't reliably separate "weak match" from "no real
   match" — this is the architectural cost of zero-inference lexical retrieval,
   not a parameter to tune. Decision: leave as documented behavior rather than
   trade real recall for partial, unreliable precision. Don't re-attempt a
   bm25-threshold or word-count-overlap gate on this route without new evidence
   that changes this calibration.

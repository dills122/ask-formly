# Local form search

Automatically generated, cited form profiles support Orama lexical and local hybrid retrieval through `lookup_form` or retrieval-only `search_forms` in the [local MCP server](local-mcp.md), and through the standalone CLI. Select a cited form, then request related authored source evidence to answer the question; use focused context for relationship or navigation gaps. Results do not establish resolved form shape or exhaustive dependencies. Serena/codebase-memory are optional follow-up tools for remaining gaps.

## Install

Use Node 22 and Python 3.9+. From the installed skill directory:

```sh
npm ci --prefix search --ignore-scripts --no-audit --no-fund
python3 scripts/project_index.py scan --root /absolute/path/to/app
node search/cli.mjs search --root /absolute/path/to/app --query "Find the form for automatic backups"
```

The scan uses the application's trusted TypeScript compiler, or an explicit `--typescript` path. It generates profiles without installing search dependencies, downloading a model, running application factories or requiring source reviews. See [project indexing](project-indexing.md).

Orama 3.1.18 and Transformers.js 4.3.1 are pinned in `search/package-lock.json`. The bundle includes source and lockfiles; it excludes `node_modules`, model files and caches. Install search dependencies into the skill's `search/` directory, not into the Angular application's package.

For lexical-only use, add `--omit=optional` to the install command to omit Transformers.js and its native inference dependencies. Re-run the full install before hybrid preparation. The measured macOS full dependency installation occupied about 484 MiB, plus 23 MiB for the model; Orama-only installation is much smaller.

## Enrich names and labels

Optionally add a `search` object to the consuming project's `.agents/ask-formly/config.json`, retaining its other settings:

```json
{
  "translations": ["src/assets/i18n/en.json"],
  "aliases": [
    {"alias": "OTW", "name": "oneTimeWithdrawal", "file": "src/app/withdrawal/form.ts"}
  ]
}
```

The snippet is the value of `search`, not the entire configuration. Replace the example with actual project mappings, then rescan. An alias can include `context` to distinguish compiler scopes. Unmatched aliases are reported; names are matched against generated form identities rather than guessed.

Translation paths must be in the scanned inventory. Flat or nested JSON dictionaries are supported. A static property whose literal value matches a configured dictionary key gains the translated text with the property/constant citation and a JSON pointer into the hashed translation file. No locale, runtime interpolation or translation precedence is inferred. Multiple dictionaries remain candidate evidence.

Profiles include canonical names, field keys, static titles/labels/descriptions and reachable shared fields. Search text strips markup, decodes HTML entities and separates code identifiers; raw cited property values remain in the facts. Facts carry their authored graph `owner_id` and `owner_kind`, and a hashed `source_span` with available line/offset metadata. Offsets use the reported encoding (TypeScript uses UTF-16). The span identifies the owning source node; property and resolved-constant citations identify the value's sources. Repeated keys on different fields retain distinct owners. Translation facts retain the original property and `source_value` plus both source and dictionary citations. None of this metadata evaluates a factory or resolves field shape.

Profiles also distinguish authored handler references, hooks, and literal
`modelOptions.updateOn`/`debounce` values. These bounded behavior facts retain
the property, original value and source citation; a discovery preview reserves
space for one when available. A handler reference establishes what was authored,
not whether it runs. Direct `expressions` / `expressionProperties` entries and
`hideExpression` also retain bounded authored source (at most 256 characters),
marked `authored-expression`. Identifier tokenization preserves comparison
operands; expressions are never evaluated into effective labels, requiredness or
runtime behavior. Oversized or unavailable expressions and unsupported behavior
values remain explicit source follow-ups. Template event wiring is not inferred
from a handler name. Rescan existing indexes to gain these distinctions, then prepare embeddings
again if using hybrid search. Restart the MCP server after updating its installed
skill files.

For MCP lookup/search, candidate ranking uses compact profiles, then query-matched
supporting facts are selected from the returned candidates' full indexed facts.
This reads the already loaded graph, without rebuilding the index or running
application code. Up to three actual cited facts are returned per candidate;
when the query names an authored behavior property, its cited fact takes priority
over descriptive labels. Exact field ownership keeps paired evidence coherent.
Distinct authored values named in the query, such as blur and submit updates,
retain their own source evidence even when they belong to different fields.
Bounded authored expressions retain up to 256 characters so their final branch
is not silently lost. The response distinguishes hydrated evidence from the
original preview and retains explicit truncation or hydration gaps. When extra
facts would crowd out ranked choices, the compact response reduces the per-card
allowance from three to two or one while preserving each card's best matching
fact. Remaining space is used for extra facts in candidate order, without losing
candidate cards or alias resolutions. Packet omissions remain separate from indexed-source gaps. Source and
artifact freshness are checked again before the response is returned. A cited
expression shows authored syntax, not proof of effective runtime behavior.

Direct class/member relationships also supply cited qualified names such as
`SampleComponent.fields`. Matching qualified names retain both owner and member
source citations. The relationship must be present in the same compiler context;
the index does not infer an owner from a filename or a matching suffix. Identical
qualified names in different files remain choices to disambiguate.

Generic objects with only a `type` property are excluded from search profiles unless their owner is a form host. This reduces ordinary HTTP/action objects appearing as forms; structural candidates are still not proof of Formly usage. Keyless type-only fragments can be omitted. Dynamic text, composition gaps and all output bounds remain explicit.

Configured aliases are authoritative project mappings. Automatically derived initials are provisional candidates. Colliding configured aliases return `ambiguous`. An unknown uppercase acronym alone returns `not_found`; matching name/title words or supported description terms can permit candidate retrieval while the unknown acronym remains explicitly unresolved. Supporting facts favor query-matched, distinct evidence, including normalized field keys and configured translations. A search score is not identity confidence.

Query wording and indexed evidence use the same English stemming and identifier
boundary normalization. Compound spellings are connected using authored camel-case
boundaries, while original words remain available for spelling tolerance. These
rules help match inflections and code-style words; they do not supply business
synonyms or acronym expansions. Exact identities and configured aliases retain
their literal matching rules, and returned citations keep the authored values.

Literal abbreviations in cited field wording, such as CSV or PDF, can match that
wording without inventing an acronym expansion. Profiles also index cited literal
field types and `props.required: true` / `templateOptions.required: true`.
The small control vocabulary maps “mandatory” to “required” and
“selector”/“dropdown” to “select” only beside a matching descriptive word and
an authored control property. These matches stay candidates; they do not establish
effective runtime validation or map business terms such as “category” to “type”.
Dynamic expressions and false required values do not supply these positive
control terms. Detailed literal facts and citations are restored when a candidate
is selected; discovery previews continue to favor human wording. Existing indexes
need a rescan to gain these control facets.

## Prepare hybrid retrieval once

```sh
node search/cli.mjs prepare --root /absolute/path/to/app --allow-download
node search/cli.mjs search --root /absolute/path/to/app --mode hybrid --query "Where can I schedule recurring work?"
```

Only `prepare --allow-download` permits model downloads. It retrieves the public Apache-2.0 [MiniLM model](https://huggingface.co/Xenova/all-MiniLM-L6-v2) at revision `751bff37182d3f1213fa05d7196b954e230abad9`. Inference runs locally; source and queries are not uploaded. Model and vector files are stored under the consuming project's `.agents/ask-formly/.search-cache/`. Re-run `prepare` without the download flag to rebuild embeddings using cached model files.

This adapter uses CPU q8 inference, 384 dimensions, normalized mean pooling and a 256-token input limit. Long profiles may lose later details in embeddings; lexical search retains up to 12,000 characters. These are initial benchmark choices, not a claim that this model is optimal for code or every language.

Hybrid mode requires fresh prepared vectors. It does not silently fall back to lexical mode or download missing models. Changes to the source snapshot, generated records or model configuration invalidate vectors. Rescan and prepare again. Lexical mode needs no model setup.

Both lexical and hybrid candidates require indexed source support. Incidental
words in directory paths do not substantiate a natural-language description;
exact cited file/symbol identities and configured aliases remain available.
Full source-qualified control terms remain eligible anchors even when absent
from a profile's short fact preview; generic control words alone remain insufficient.
Conservative spelling tolerance uses authored words, not directory names.

Within a prepared hybrid search, lexical and semantic candidates are combined
and checked against indexed source evidence. Exact cited identities remain
eligible; descriptive matches need an anchor beyond generic form/control words.
Supported lexical matches retain their description and control ranking priority.
This is a retrieval
fallback, not an automatic model installation or a declaration that the form
matches every requested behavior. Keep alternative candidates and unresolved
acronyms explicit; a refusal means insufficient indexed support, not proof that
the application has no such form.

## Reuse a process

For repeated agent requests, connect the [MCP server](local-mcp.md#install-and-connect).
Call `lookup_form(query="Find the form for automatic backups", mode="hybrid")`
after preparing embeddings, or omit `mode` for lexical search. Compact lookup
candidates include `context_choices` pairing exact IDs with compiler contexts,
bounded supporting facts and `citation_refs`. Resolve citations through the
response's `citations` and `files` tables; select an explicit ID/context pair.
Then call `get_form_evidence(target="ID", selection="related", view="brief")`,
pinning the lookup's source snapshot. Preserve relevant authored values and scoped
registration/component/template candidates in the answer. `get_form_answer` and
`check_form_answer` remain opt-in experiments: reusable blocks and exact-text
diagnostics have not demonstrated faster or reliably more complete answers, and
full behavioral enumeration can be bulky. The checker never establishes semantic completeness.
Use `get_form_evidence(selection="helpers", view="source")` for referenced
helper bodies or `selection="models"` for authored type declarations. These
bounded follow-ups avoid enumerating unrelated source pages. Related source or
targeted reads still cover renderer attributes and template guards. Exact identities may already include
context; ranked matches remain explicit choices even when the limit is one.

Use `get_form_context` when a relationship or navigation gap needs its role
summary, or `detail="graph"` for expanded paths. Its `nodes` table also supplies
actual graph IDs for focused `get_form_evidence(selection="selected", node_ids=[...])`
reads; omitting IDs in selected mode reads the definition. Continue related
source with its evidence snapshot and `next_offset` only when missing lines are
relevant. See [evidence limits and snapshot rules](local-mcp.md#authored-source-evidence).

Read the authored facts and any needed numbered source, then retain requested facts with their supporting
path/range and snapshot in a small internal session ledger. Reuse valid evidence,
then check the final answer preserves relevant constraints, conditions and
relationships with citations. An import or node pointer locates source without
proving its body. Expand only gaps relevant to the question; exhaustive paging,
all renderer types and code-tool rediscovery are not prerequisites. Only claims
derived from a separate code graph need that graph's coverage checks; byte-fresh
MCP source can stand on its own. The [answer guidance](../SKILL.md#deliver-the-answer)
describes the internal check without requiring extra visible prose.
Use `search_forms` for retrieval-only results. Search requires the search dependencies; the older
navigation tools also work without them.

The server reuses one Python index, one Node worker, both Orama engines and the
local embedding model. Profiles cross the process boundary only on first use,
after an index replacement or after a worker restart. Source/config/artifact
bytes are still verified on every request. The response's `cache` flags and
`freshness_ms`, `setup_ms`, `elapsed_ms` (ranking), `context_ms` (matched lookup) and `total_ms` expose reuse and
cost. `total_ms` excludes MCP serialization/transport. Querying never prepares
embeddings or downloads packages/models. A failed worker returns `unavailable`
with no candidates; retry starts a fresh worker.

For a standalone CLI session:

```sh
node search/cli.mjs search --root /absolute/path/to/app --mode hybrid --stdio
```

Send one JSON request per line, for example `{"query":"Find the OTW form","limit":5}`. Responses are JSON lines. This is a reusable CLI process, not the MCP wire protocol. It keeps the model and search index in memory but invokes the Python profile exporter for every request; MCP avoids that repeated startup and parsing cost. Both check source/artifact freshness before every request. `mode`, `limit` (1–100) and `context` can be supplied per request. `FORMLY_PYTHON` can select the CLI exporter's Python executable.

Retrieval responses include identities, source citations, compiler contexts, match reasons, supporting facts, unresolved scope and timing. Matching definitions at the same source location are grouped while their compiler contexts/profile IDs remain listed. Compact `lookup_form` additionally preserves ID/context pairs and reports omitted candidates/evidence and unresolved counts instead of repeating full gap paths; `search_forms` and the CLI retain the fuller retrieval representation. The common configured-alias case skips semantic ranking after the search session is initialized. General lexical/hybrid matches require selecting the intended cited identity.

Compact `lookup_form` format 2 uses each candidate's `context_choices` as the
canonical list of selectable ID/context pairs. When that mapping is complete,
the redundant `profile_ids` and `contexts` arrays are omitted. If a legacy result
cannot supply a complete mapping, those arrays remain with
`context_mapping_unavailable: true`; do not infer their pairing. `search_forms`
retains the full retrieval representation. This prevents repeated IDs from
crowding lower-ranked candidates out of the bounded lookup response.

## Bounds and limitations

Discovery profiles are generated independently of the navigation-record limit,
with at most 4,000 profiles and a 5 MiB collection budget reserved within the
24 MiB generated-record budget. Definitions receive capacity before host summaries,
with compiler contexts taking turns. Each profile traverses at most 256 relevant
nodes and derives at most 128 facts for searchable text. Stored discovery entries
keep up to three cited preview facts; omitted details are explicit. Selecting a
form restores its bounded full profile from the same attested graph and caches it
for the current source/artifact snapshot. The detailed context and source tools
share that evidence, including owner IDs beyond the ordinary navigation depth.
Navigation records retain their separate 1,000-record cap. Omitted profiles/records
and unresolved aliases remain reported; per-context profile coverage is available
in the profile export. Existing registration and runtime limitations still apply.
The larger discovery reserve leaves less room for precomputed navigation records
inside the same total budget. Selected context can still traverse the full graph;
omitted cached records are reported explicitly.

The implementation uses [Orama's public search APIs](https://github.com/oramasearch/orama) and [Transformers.js feature extraction](https://huggingface.co/docs/transformers.js/en/pipelines). Dependencies provide ranking and model inference; ask-formly supplies Formly evidence, identity handling and freshness. This milestone does not measure whole-agent development speed.

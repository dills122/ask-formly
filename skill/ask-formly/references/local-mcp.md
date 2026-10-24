# Local MCP navigation

The optional MCP server supplies cited project context and bounded authored source
for form questions. The ask-formly skill supplies version-specific Formly guidance.
Source-reviewed [form records](form-records.md) remain optional reusable knowledge.
Resolved field shape, runtime usage and injector precedence are outside the index contract.

## Install and connect

Install the whole portable skill first. The server uses the
[official Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk), pinned
to **2.1.0** with a transitive lockfile. It requires Python **3.10+** and
[uv](https://docs.astral.sh/uv/getting-started/installation/). The index CLI still
works separately with Python 3.9+, Node and a trusted TypeScript compiler.

```sh
ASK_FORMLY=/absolute/path/to/ask-formly
FORM_PROJECT=/absolute/path/to/application
uv sync --project "$ASK_FORMLY/mcp" --frozen
python3 "$ASK_FORMLY/scripts/project_index.py" scan --root "$FORM_PROJECT"
```

For description/acronym lookup with `lookup_form` or `search_forms`, also install the search
dependencies using Node 22:

```sh
npm ci --prefix "$ASK_FORMLY/search" --omit=optional --ignore-scripts --no-audit --no-fund
```

This enables lexical search. For hybrid search, omit `--omit=optional` and follow
[one-time local embedding preparation](semantic-search.md#prepare-hybrid-retrieval-once).
Search defaults to lexical; request `mode="hybrid"` for meaning-based ranking.
No download occurs on a tool call. Exact-symbol lookup and context/navigation tools need no
search packages, and remain available if search is unavailable.

Check that the scan reports `graph_mode: typescript-static` and complete inventory
coverage. A lexical-only index cannot serve these tools. If necessary, supply the
scan's `--typescript /absolute/path/to/typescript/lib/typescript.js` option. The
normal agent indexing workflow stops at useful static navigation. Full source
reviews are optional; `review.status: pending` does not block starting-point queries.

In your MCP-capable agent's server settings, add a **stdio** server:

| Setting | Value |
| --- | --- |
| Name | `ask-formly` |
| Command | Absolute path to your `uv` executable |
| Arguments | `run`, `--project`, `/absolute/path/to/ask-formly/mcp`, `--frozen`, `--offline`, `python`, `/absolute/path/to/ask-formly/mcp/server.py`, `--root`, `/absolute/path/to/application` |

Use each argument as a separate array entry if the client uses JSON configuration.
Paths must be absolute; shell variables in the examples are not client settings.
After the initial sync, `--offline` prevents dependency downloads at launch. Keep
the generated environment local; it is not part of a skill ZIP. One server process
serves one application root. No listening port or application-side package is needed.

For overlapping compiler contexts, append `--context`, `src/tsconfig.app.json`
(use your index's actual context). A query can specify another context explicitly;
the server never changes its application root. Without a default, ambiguous symbols
return choices rather than merging contexts. Restart/reconnect after upgrading the
server. Disconnect/remove its client entry to stop using it.

## Handoff to code tools

1. Use `lookup_form(query="We need to update the OTW form", mode="hybrid")`
   after embedding preparation, or omit `mode` for lexical search. Exact canonical
   symbols/IDs and unique configured aliases can return a matched `form_context`.
   Ranked descriptions and provisional initials return explicit `candidates` with
   `status="ambiguous"`; similarity alone never confirms identity, even at `limit=1`.
2. Choose a cited target/compiler context. For engineering questions about its
   configuration and parts, call `get_form_context(target="ID",
   context="src/tsconfig.app.json", sections=["composition","hosts","authored"],
   snapshot="SEARCH_SNAPSHOT")`. The authored section preserves indexed source
   properties beyond the discovery preview. Use `sections=["authored"]` when
   only values are missing, or `get_form_evidence(selection="related", view="brief")`
   for the existing role-grouped evidence view.
   Retain relevant cited facts in the answer, keeping scoped renderer/component/template
   associations together. Keep alternatives explicit until evidence or the user
   resolves them. `search_forms` remains retrieval-only.
3. Interpret the authored values against the requested facts. Use `view="source"`
   or targeted source reads for helper bodies, renderer attributes and enclosing
   template guards; the fact checklist never proves those were inspected.
   `detail="graph"` context paths can resolve a relationship/navigation gap;
   `get_form_starting_points` offers smaller hints.
   To focus a read, pass actual graph IDs from the summary's `nodes` table to
   `get_form_evidence(selection="selected", node_ids=["GRAPH_ID"])`.
   Follow evidence continuation only for relevant missing lines. Neither a full
   review nor exhaustive paging is required.
4. For remaining gaps, use returned file, name and line hints with available
   tools. For Serena, discover the actual name path with
   `find_symbol`/`get_symbols_overview`, then inspect bodies/references. For
   codebase-memory, select the matching root, discover qualified names with
   `search_graph`, then use `trace_path` and `get_code_snippet`; check coverage for
   claims derived from that graph and read source for its gaps. Byte-fresh MCP
   source needs no separate graph rediscovery or coverage check. An empty graph
   result does not prove absence.

Maintain a small internal ledger of requested facts and their supporting source
ranges/snapshots, distinguishing actual source from pointers. Reuse still-current
source across the session instead of rereading it. Before finishing, verify the
requested signature/model types, field constraints and full guard expressions,
direct helper purposes/locations, scoped registrations and renderer/template
associations, and host fields/model forwarding. Inspect enclosing template
conditions as well as the host element: a nearby binding window can omit an
ancestor guard. A pointer/import can support a location claim without proving the
target body. Carry relevant supported facts into the answer with citations and
state remaining gaps; the ledger and check need not appear as extra prose.

ask-formly lines are 1-based; Serena lines are 0-based. Symbol names can include
synthetic field/registration labels, so they are search hints, not interchangeable
tool IDs. Source hashes, context, limits and unresolved counts remain in the output.
Follow `has_more`/`next_offset` only when another page is relevant, with the same
snapshot and query arguments; a bounded shortest path is a navigation lead, not a
complete dependency explanation.

Lookup groups physical definitions while preserving exact ID/compiler-context
pairs in each candidate's `context_choices`. Select a pair rather than guessing a
mapping from displayed names. Its compact `candidates` retain up to three
supporting facts and `citation_refs`; resolve each reference through `citations`
and then its `file_id` through `files` for the path and hash. Coverage counts,
`candidates_omitted`, truncation and unresolved acronyms expose omitted evidence.
Exact selection occurs before this projection; a compact or single-row result
does not remove ambiguity. Use `search_forms` for the full retrieval projection.
Search returns up to `limit` (default 5, maximum 100); `truncated` and `coverage` expose
bounds. Pass the selected ID to a dependency/usage tool with no snapshot on its
first call, then use that tool's returned pagination snapshot. Search snapshots
can pin `get_form_starting_points`; record pagination uses a different token.

The optional code-tool handoff requires no direct integration or automatic tool
invocation; the agent uses the tools already available. Without MCP, run:

```sh
python3 "$ASK_FORMLY/scripts/project_index.py" start --root "$FORM_PROJECT" \
  --target withdrawalFields --file src/forms/withdrawal.ts --intent usages
```

## Focused form parts (experimental)

Indexing builds lightweight discovery profiles independently of the larger
navigation-record budget. Descriptions search the bounded source-derived text;
the candidate response shows a few cited facts and explicitly marks omitted
preview evidence. Selecting a form through `get_form_context` or `get_form_parts`
restores its bounded detailed profile from the current index and reuses it while
that source/artifact snapshot remains fresh. This does not perform a source review.
Profile count and byte limits still apply; check reported omissions before
treating an unsuccessful lookup as evidence that no form exists.

After selecting a lookup candidate, use `get_form_parts` for a change-planning
map of its definition and statically related parts:

```json
{"target":"SELECTED_ID","context":"src/tsconfig.app.json","source_aspects":[]}
```

The result includes `parts`, cited relationship witnesses, `source_gaps`, and a
directly readable `text` view. Keep the reason each part belongs to the selected
form: composition/reference, host use, or scoped renderer candidate. A nearby
declaration is not automatically a dependency. An indexed relationship and
owner-declaration citation are static evidence, not a reviewed behavioral claim
or an exact reference-token citation. Scope and unresolved candidates remain
explicit; runtime shape and exhaustive usage discovery are not supported.

The text leads with the selected definition and page scope, then groups observed
static subparts, consumers/hosts, and candidates requiring confirmation. Named
relationship paths retain their witnesses; authored values appear on separate
cited lines. Source status and follow-ups distinguish unread or partial evidence
from acquired source, which still does not verify behavior. Use the portions
relevant to the engineering question; copying every candidate into a final answer
can obscure the useful details. Coverage warnings and continuation remain explicit.

In response format 2, each part's `path` is an ordered list of keys into that
response's `relationships` dictionary. Each dictionary entry retains the complete
relationship and its source witness. Resolve keys within the same page; keys are
not stable across pages. The readable `text` still names the relationship chain.
This removes repeated evidence without requiring another tool call. Clients that
read the earlier experimental format must expand these references before treating
`path` entries as edge objects.

Default requests report missing source without fetching every body. Request only
the relevant `source_aspects`: `helpers`, `models`, or `hosts`. These acquire
bounded declarations or lexical template guards/bindings. An unavailable
consuming-project parser, unsupported syntax, unresolved reference or source
budget leaves a visible gap. The server does not install dependencies or silently
substitute another application's Angular version.
If model source was requested but no linked model declaration was collected,
the first page reports that explicitly and points to host `[model]` bindings.
It does not establish that the application has no model. Field-shaped data
inside custom renderer options is also a cited source gap when its owning field
is on the selected dependency path; interpreting it requires renderer source.

Host ancestry currently supports external HTML with a standalone installed
Angular compiler bundle and Node loader hooks (Node 22.15+). Inline-template
ranges, split compiler modules and missing loader hooks remain explicit gaps.
Other form-parts navigation works without that optional parser capability.

`source-complete` describes acquisition of the declared source ranges only.
It does not prove that the client displayed them, the agent understood them,
transitive effects were traced, or the engineering question is fully answered.
Use precise source/code-tool follow-ups for remaining answerable gaps; explicit
uncertainty is useful but does not make an unfinished task complete.

Responses are bounded to 24 KiB by default and 48 KiB with source aspects. Follow
only relevant continuation pages using the returned snapshot and unchanged
target, file, context, source aspects and limit. Every request checks freshness.
This view is experimental; the brief/source workflow remains available.
These bounds cover the serialized result payload, including its text view;
MCP transport may also duplicate structured data in a text content block.

## Focused static context

`get_form_context` defaults to `detail="summary"` and accepts
`sections=["composition", "hosts", "fields"]`, `depth`
(default 12, maximum 24), `limit` (default 20, maximum 100), `offset` and `snapshot`.
Its first call can pin the source snapshot from lookup/search. Continue with its
returned **context** snapshot and unchanged target, compiler context, sections,
depth and detail; restart on `snapshot-changed`. Changing page size is allowed.
Switch detail on a new first page using the source snapshot. Source freshness is checked on
all calls. Exact matched lookup checks again before attaching context because search
can await a separate worker; `context_ms` includes this second check.

Add the optional `authored` section to retain source properties, callbacks,
expressions and explicit unresolved syntax from selected graph owners. Unlike
the `fields` discovery summary, it does not filter properties by name. For
example, `sections=["composition","hosts","authored"]` combines navigation
and source facts in one request. Values keep their original indexed syntax,
owner/compiler context and hashed source citations. They are not evaluated,
merged through spreads or inherited into a final form shape.

Authored collection follows bounded indexed dependency paths in the selected
compiler context. It preserves the extractor's limits of 64 facts per owner and
1,024 characters per value, with explicit truncation and unsupported-syntax gaps.
Imperative assignments, helper effects and renderer implementation can still
require targeted source reads. Empty facts never prove absence of behavior.
The section reuses a bounded in-memory collection while checking freshness on
every page; source or artifact changes invalidate its continuation. Rows keep
their indexed values through pagination instead of becoming shorter previews.

The entire summary response targets at most **16 KiB of serialized UTF-8 bytes**,
including metadata and gap previews. `definition` points into `nodes`; each node
has a graph `id`, `file_id` and `citation_refs`. `roles` groups node references.
Resolve citation references through `citations`, then file IDs through `files`.
These short references are page-local: pass a node's graph `id`, not its `n1`
reference, to evidence tools. Field rows retain `owner_ref` and `source_span_ref`
when available; repeated keys on different authored fields remain distinct.
Translation facts keep the original property and both source and dictionary citations.

`has_more`, `next_offset`, section counts, traversal truncation, gap counts and
`omissions` expose bounds. The definition remains available; unusual metadata or
oversized items can be omitted with recovery instructions. `detail="graph"`
preserves expanded paths and citations, with the earlier 24,000 serialized item
character and 4,000 unresolved-preview character budgets plus metadata.
Traversal is capped at 2,000 nodes per direction. Missing profiles and static
extraction gaps stay explicit. The checklist is a guide to evidence needs, not
proof that every role has been inspected.

Context is **static candidate evidence**, even if optional reviewed records exist.
It does not recursively expand ordinary imports or renderer internals, resolve
model/type-only interfaces, execute factories, infer Angular injector precedence,
or promise exhaustive usages or a final compiled/runtime field shape. Use the
cited source and optional code tools to resolve those relevant gaps.

## Request-focused answer blocks and draft checking

These tools are opt-in experiments. A source-grounded replay did not establish a
speed or reliable completeness improvement for the packet/checker workflow.
Use the brief/source workflow above for ordinary investigation; the checker is
not a required step for complex answers. Full behavioral packets can require
substantially more pagination than the brief.

`get_form_answer` returns up to **16 KiB** with `items`, page-local
`nodes`/`files`/`citations`, source hashes, compiler context and explicit omissions.
Each item has a stable `id`, `section`, `kind`, reusable Markdown `text`,
`owner_ref` and `citation_refs`. Format v2 keeps machine-only anchors on the
server; they do not consume the model-visible response budget. TypeScript source
citations retain UTF-16 offsets.
Renderer items carry component/template references and keep location candidates
together. These are static associations, not a runtime implementation choice.

Sections are `definition`, `subparts`, `consumers`, and optional `behavior`.
Unrequested authored facts are counted as withheld. Source bodies, helper
transformations and template guards still require inspection; read only relevant
followups. Continue with `next_offset` and the packet snapshot using the same
sections and selectors. No complete-dependency or resolved-shape claim is made.

For helper bodies or authored model declarations, call `get_form_evidence` with
`selection="helpers"` or `selection="models"` and `view="source"`. These selections
follow indexed references within the bounded form/host/renderer context and return
numbered source with hashes. They do not accept explicit `node_ids` or infer a
resolved model shape. The default is 160 lines (maximum 400), bounded to 24 KiB
source/48 KiB response. Use the packet's `source_snapshot` for the first source call,
then the source response's snapshot and unchanged selectors for continuation.
An absent selected declaration is a coverage gap, not proof no helper/model exists.

For an optional exact-text diagnostic, `check_form_answer` accepts the exact packet snapshot,
selectors, sections and offset plus `draft` and `dispositions`:

```json
[
  {"item_id":"ITEM_ID","disposition":"included","draft_excerpt":"Exact unique text from the draft"},
  {"item_id":"OTHER_ID","disposition":"unverified","reason":"Relevant helper body has not been inspected"}
]
```

`omitted` is also supported with a reason. Unlisted items remain `unaccounted`.
An included item may instead provide `draft_span: {"start": 0, "end": 42}`:
Unicode codepoint offsets into the actual draft, with an exclusive end. Send
either a span or an excerpt, never both. Spans avoid repeating draft paragraphs
for several items. The checker reconstructs the same page's anchors internally.
Included excerpts must occur exactly once in the actual draft and contain the
item's exact anchors. IDs alone do not count. Changed values, incomplete
conditions and wrong path prefixes are flagged; paraphrases may need manual
review. The result is a mechanical text correspondence check, **never semantic
approval**: negated or incorrect prose can retain all the anchors. `complete`
stays false and `semantic_coverage` stays `not-assessed`. Review the actual
meaning, citations and requested scope before sending the answer.

The checker covers one returned packet page, exposes pagination/omissions, and
rechecks source freshness after checking the draft. It accepts at most 200
dispositions; draft and dispositions each have a 64 KiB UTF-8 input limit, and
the result has a 16 KiB limit. It does not retrieve new source or approve missing
facts. Simple location requests need not incur a separate check call.

## Answer brief

`get_form_evidence(target="ID", selection="related", view="brief")` returns a
bounded **16 KiB** packet. Entries group authored values by their owner and role;
renderer paths keep a scoped registration, its component and its template together.
Multiple implementation/template candidates remain explicit. `answer_ledger`
maps roles to returned entry IDs so an agent can retain relevant evidence across
questions and check that it reaches the final answer. Entry IDs are stable within
the source snapshot; table references are page-local. The ledger is a retention
aid, not a completeness score or an instruction to list every indexed fact.

Resolve `owner_ref`, renderer refs and `citation_refs` through `nodes`, `files`
and `citations`. Brief format version 1 uses the same hoisted compiler context
and evidence/citation defaults described under [compact authored facts](#compact-authored-facts).
Keep compiler context, scope and source hash with saved evidence.
`followups` distinguish unread helper bodies, renderer attributes, enclosing
conditions and other gaps. A `location-only` renderer path establishes locations,
not implementation behavior. Read relevant source before explaining that behavior.

Followups are a bounded preview repeated on continuation pages; paging entries
does not recover every omitted followup. Inspect source or use the detailed facts
view for relevant gaps rather than assuming the preview is exhaustive.

Brief requires related selection without `node_ids` or `max_lines`. Continue only
for relevant missing entries using `next_offset` and the brief snapshot; restart
at offset zero with the source snapshot when changing views. Oversized entries
and omitted followups are explicit. `complete` and `exhaustive` remain false.
Freshness is checked before and after projection. Use facts view for detailed
indexed rows, or source view for exact bodies and template bindings.

## Compact authored facts

`get_form_evidence(target="ID", selection="related", view="facts", context="CONTEXT",
snapshot="SOURCE_SNAPSHOT")` returns up to **64 fact rows and 24 KiB total** per
page. Facts use `owner_ref` into `nodes` and `citation_refs` into `citations`;
citations use `file_ref` into `files`, whose entries contain `file` and `sha256`.
Keep owner identity, compiler context and registration scope with each value.

Format version 2 hoists the common `compiler_context` and `defaults`: missing
fact evidence inherits `defaults.fact_evidence[kind]`; offset-bearing citations
inherit `defaults.citation_offset_encoding`; pointers inherit
`defaults.pointer_next_action`. Explicit row values take precedence. Equivalent
adjacent relationship rows group their targets in `target_refs`, preserving order
and duplicates. `returned_facts` counts serialized groups; `returned_fact_rows`
counts expanded rows. Offsets and the 64-row budget count raw rows, including
explicit omissions. Grouping changes serialization, not the underlying facts.

Values preserve authored syntax, including quoted strings, function expressions,
arrays and explicit type annotations. A conditional-branch row retains the exact
condition and `branch="true"|"false"`; it does not evaluate the condition or infer
its negation. Dynamic/computed/spread syntax and oversized values remain unresolved.
Indexing bounds metadata to 64 facts per node and 1,024 characters per value,
with explicit omissions; it never constructs the resolved form.

This view requires `selection="related"`, with no `node_ids` or `max_lines`.
Continue with `next_offset` and the returned fact snapshot, keeping selectors
unchanged. Fact and source continuations are separate: restart at offset zero
with the source snapshot when switching views. Role balancing and deduplicated
owner/file/citation tables keep pages bounded. Omitted rows and pointers are
reported; empty facts never establish that a form has no further behavior.

The checklist counts indexed facts; `complete` and `exhaustive` stay false.
Helper transformations and unsupported template attributes/control flow require
source inspection. Follow a relevant pointer with source view or code tools,
then retain the supported details in the final answer. A path-only pointer is
sufficient to locate a file, not to explain its implementation. No additional
model call or source review is required during indexing. Source and artifact
bytes are checked before and after fact projection.

## Authored source evidence

`get_form_evidence(target="ID", selection="related", context="CONTEXT",
snapshot="SOURCE_SNAPSHOT")` selects up to **20 related graph nodes** and returns
numbered authored source windows, hashes and compact role information. It
allocates source across selected roles so a large definition does not consume
the whole page. Selection is bounded candidate navigation, not an exhaustive
dependency inventory; relevant model types, imports or enclosing conditions may
still need targeted source inspection.

| Selection | Default / maximum lines per page | Source / whole-response byte caps |
| --- | --- | --- |
| `selected` (default) | 120 / 200 | 16 / 32 KiB |
| `related` | 400 / 400 | 24 / 48 KiB |

Automatic related selection gives only the first 40 lines of a helper longer
than 400 lines, with an explicit omitted-tail pointer for source-tool follow-up
if relevant. That tail is not part of continuation pages. Definitions, referenced
types, hosts, renderers and templates are exempt from this helper-only cap.

Omit `max_lines` to use the mode's default, or supply a positive value within its
limit. In `selected` mode, omit `node_ids` to read the definition, or supply at
most **12 unique related graph IDs** for focused evidence. Use `related` without
explicit IDs for automatic selection. Arbitrary paths and unrelated IDs are
rejected. `file` disambiguates the target; it is not an arbitrary file reader.
Byte caps measure serialized UTF-8 output.

A current source snapshot or that form's context snapshot can pin the first call
with `offset=0`. The returned **evidence** snapshot binds the target, compiler
context, selection, selected IDs and line budget. When `has_more` reports source
lines still to read, continue with `offset=next_offset`, that evidence snapshot,
and unchanged selectors and budget. Continuation serves remaining lines rather
than rereading earlier windows. Fetch only pages needed for the question. For a
different selection or `max_lines`, start at offset zero with the current
source/context snapshot. Restart after `snapshot-changed`; do not combine pages
from different snapshots.

Where a reliable node span is unavailable, the response includes an explicit
`span-unavailable` pointer and at most seven context lines, marked incomplete.
`complete` describes selected source windows only; it never establishes complete
dependencies or runtime behavior. Inspect `pointers`, `omissions` and window-level
completeness before interpreting a condition. If the needed source is outside
the selected nodes, use focused selection or targeted source tools instead of
paging unrelated text. Byte freshness is checked before and after reading source;
a detected change blocks the result and clears windows. Reading these excerpts
does not execute factories, evaluate expressions, resolve conditional composition
or prove a final form shape.

## Optional reviewed answers

- `find_forms(query="withdrawal")`: find form-related configs, factories and hosts.
  Select an exact returned ID, or supply a definition file and compiler context.
- `find_form_usages(target="withdrawalFields", file="src/forms/withdrawal.ts",
  exclude_file="src/screens/x.ts")`: get focused consumer facts. Exclusion hides
  facts about that file, retaining supporting citations through it.
- `get_form_dependencies(target="withdrawalFields", file="src/forms/withdrawal.ts")`:
  get composition and host-chain facts, including reviewed helpers, registrations,
  renderers and templates within the recorded scope.

Default `detail="record"` returns current reviewed facts when available. Dependency
answers also include usage facts explicitly classified as `host`; unrelated
consumers stay usage-only. Stable fact IDs and `record_coverage` category counts
help track requested relationships through pagination. They are evidence inventory,
not proof of application coverage or answer completeness. For broad dependency
questions, name each relevant model/helper, renderer, registration/adapter and host
relationship and cite its supporting paths; do not substitute behavior-only prose. Each page
contains only the selected section, deduplicated file/line/hash citations and
unresolved scope. `review_status` and `retrieval` distinguish reviewed records,
materialized static candidates and graph fallback. Answer from reviewed facts when
they cover the question; investigate gaps in source. Missing/stale review never
becomes a reviewed conclusion. Empty results do not prove absence.

Use `detail="graph"` for expanded per-file shortest paths and symbol evidence.
The graph follows composition and direct helpers; ordinary imports and renderer
internals are not recursively expanded. Select a host for its binding path. A
registration candidate does not establish Angular injector precedence.

Continue `has_more` results with `next_offset` and the same `snapshot`; restart on
`snapshot-changed`. Record pages target at most 12,000 serialized fact characters
plus up to 4,000 unresolved-preview characters and bounded metadata/citations,
and at most 100 facts. `unresolved_total`/`unresolved_truncated` expose preview gaps;
follow the recovery instruction before relying on an incomplete preview. Citations
use stable IDs and are complete for each
page. Graph depth defaults to 12 (maximum 24), visiting at most 2,000 nodes;
`truncated` exposes bounds, not completeness. A reviewed record's scope is its
explicit source review, independent of graph depth.

## Freshness and recovery

Every query verifies current source/config and generated record and graph bytes. Parsed graphs and
adjacency, records and search profiles are reused in memory; a previous freshness
verdict is never reused. Shared-directory checks are deduplicated within a single
inventory pass only. No timestamp cache, watcher delay or freshness TTL is used.
The persistent Node worker receives profiles only when their attested identity
changes and retains separate lexical/hybrid engines and the local model. It is
stopped with the MCP server; failed workers are restarted on the next search.
Changed, missing, damaged, incomplete or currently-written indexes return a blocked
result with no facts. Re-run the ordinary scan after inspecting changes. The same
server loads a completed replacement graph on its next query.

Missing or stale form reviews fall back to labeled static candidates. Damaged
reviewed records block record answers; starting-point queries do not load them. Rescan preserves reviews and requires
explicit re-review/re-recording; it never silently reapproves them. The MCP tools
do not load Markdown notes; use `lookup` for broader reviewed explanations and
pinned references for Formly semantics.

The server does not scan automatically, execute application factories, edit source,
or make network requests. Its stdout belongs to the SDK's MCP protocol: running it
in a terminal waits for a client and is not an interactive query shell.

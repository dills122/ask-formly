# Next extraction trial: source blocks to grounded knowledge facts

## What the current trial establishes

The reproducible compiler imports three Formly v6.3.12 source documents and
builds one SQLite database. `python -m kbcompiler.trial_audit` reports 16 heading
units and 43 smaller candidate blocks. Every candidate matches its recorded
source-line span; every substantive line in those units is covered by a
candidate or table-header context. The audit also recomputes K/E links from
source. The script creates 56 direct K/E links and zero inferred
semantic links. No final generated corpus or database row is edited by hand.

These are **block candidates, not atomic facts**. Twenty-four of 31 prose blocks
exceed 300 characters. A reviewed paragraph about hidden fields combines lazy
rendering, control removal, reset behavior, showing, and an exception. A reviewed
paragraph about disabled paths combines an alias, a behavior difference, and a
probe result. Splitting either paragraph on sentence boundaries would risk
detaching its qualification or source. Twelve blocks lack a direct K/E citation;
some are examples or cite other local documents, so this count alone is not a
count of unsupported claims. The [generated trial report](../../test-output/contextual-kb-fact-trial.json)
records the counts.

## What other systems suggest

| Source | Relevant mechanism | Consequence here |
| --- | --- | --- |
| [Anthropic Contextual Retrieval](https://www.anthropic.com/research/contextual-retrieval) | Adds short, chunk-specific context before indexing while retaining original chunk text. Its experiments found little benefit from generic document summaries. | Generate search context *for each fact*, separate from the authoritative source span. A document-wide synopsis is insufficient. |
| [Microsoft GraphRAG outputs](https://microsoft.github.io/graphrag/index/outputs/) and [configuration](https://microsoft.github.io/graphrag/config/yaml/) | Keeps source text units alongside extracted claims; claim extraction is off by default and requires prompt tuning. | Preserve the source block and quote alongside any proposed claim. Do not treat model-generated claim status as verification. |
| [LlamaIndex node parsers](https://docs.llamaindex.ai/en/stable/api_reference/node_parsers/semantic_splitter/) and [hierarchical nodes](https://docs.llamaindex.ai/en/v0.10.18/module_guides/loading/node_parsers/modules.html) | Semantic splitting groups related sentences; hierarchy links small nodes to larger context. | These can help retrieval boundaries and parent expansion, but similarity does not prove that a node is one correct Formly fact. |
| [Unstructured chunking](https://docs.unstructured.io/api-reference/partition/chunking) | Preserves section boundaries and table elements, and sometimes combines adjacent elements to fit size targets. | Keep Markdown structure and table headers; do not use a character target as the definition of a fact. |

The consequences in the third column are design inferences from the sources and
our trial; they are not claims that those libraries have been tested in this POC.

## Recommended next experiment

1. Keep the imported source and current candidate blocks as the immutable
   provenance layer. Any source correction goes into the authored source or
   transpiler, followed by a full rebuild and audit.
2. Define a constrained fact proposal format: one narrow behavior or rule, exact
   Formly version and adapter, source document and line/character span, verbatim
   supporting quote, K/E or other local provenance, and any condition or exception.
   Keep a parent-block pointer for context. A fact may use multiple adjacent
   source spans when a qualification is separate.
3. First extract where structure is explicit: table rows and authored one-fact
   list items. For mixed prose, trial a source-normalization pass and a structured
   extraction pass on the same 43 blocks. Each output remains a proposal until
   checked; a failed or ambiguous block stays intact and unresolved.
4. Generate retrieval-only metadata from approved facts: API identifiers,
   controlled topic labels, and a short chunk-specific context line. Never use a
   generated summary as the sole evidence or replace the source quote with it.
5. Rebuild the database from source and scripts. Reject missing spans, invented
   citation IDs, broken parent/version links, duplicate IDs, and changed source
   hashes. Evaluate semantic support and missing qualifiers on the small corpus
   before using a model-driven path unattended. The earlier local Ollama headmatter
   trial produced an unsupported `FieldTypeConfig` claim, so model output needs an
   explicit quality gate.

## Decision gate

Compare the normalized-source path and structured-extraction path on the same
blocks. Record (a) fact coverage, (b) unsupported or over-broad claims,
(c) lost conditions/exceptions, (d) correct version/provenance, and (e)
rebuild repeatability. If a method cannot preserve qualifications reliably, keep
the larger exact source block as the authoritative unit and mark finer extraction
unresolved. Embeddings, FTS, MCP response assembly, and semantic relation
generation remain outside this data-organization trial.

## Structured-proposal trial result

The first path is now implemented in the same deterministic compiler. It emits
nine table-row proposals from the three imported documents; the other 34 blocks
are explicitly unresolved (31 prose and three examples). Four proposals have no
direct K/E link. The compiler and audit retain exact source quotes, character
offsets, version/adapter joins, and a disposition for all 43 blocks. A controlled
`- Fact:` item format with explicit condition and exception lines works in
fixture tests, but is not present in the real corpus. The
[generated report](../../test-output/contextual-kb-proposal-trial.json) is the
reproducible result.

This fails the promotion gate: no proposal has undergone semantic/atomicity
review, and a table row is not automatically one fact. In particular, the four
callback-contract rows rely on a later table-level evidence paragraph rather
than row-level K/E links. Assigning those links to each row automatically would
claim support the source has not established at that granularity.

The next comparison should normalize a bounded selection of the mixed prose
into explicit fact items **as authored source**, then regenerate and compare it
with this structural baseline on claim coverage, qualification retention, and
authoring cost. If that cost is too high, test model-generated *proposals* under
the same source-quote and semantic review gates. Neither path should write
accepted facts without passing those gates.

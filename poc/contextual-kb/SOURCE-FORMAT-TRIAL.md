# Controlled source format: first extraction and seed trial

## Decision being tested

Treat an **authored fact record**, rather than a Markdown paragraph or a size-based
chunk, as the input to the knowledge compiler. The compiler reads the explicit fields;
it does not decide where one claim ends or infer missing qualifications.

This is a bounded format and database-seeding trial. The
[review boundary](REVIEW-SCOPE.md) defines its acceptance scope.
The two trial files in `authored/` were drafted from selected existing Formly
knowledge passages for this experiment. Only compiled Formly knowledge was
carried forward from previous implementations.

## Why this shape

One JSON file represents a topic and its Formly version/adapter. JSON provides
explicit objects and lists, no Markdown heading/list ambiguity, and a standard
parser that rejects malformed syntax. YAML would be more pleasant for some manual
edits but brings scalar parsing and indentation ambiguity; free-form Markdown
requires another semantic splitting pass. JSON is an experiment choice, not an
industry standard or a measured retrieval winner. The compiler enforces the
supported fields and rejects extras.

| Field | Purpose |
| --- | --- |
| `id`, `title`, `formly_version`, `adapter` | Stable topic identity and bounded version scope |
| `summary` | Topic routing text; never an evidence source |
| `derived_from.path` and `sha256` | Exact source-material snapshot used in this extraction trial |
| `facts[].id`, `claim` | Stable, standalone behavior or rule |
| `conditions`, `limits` | Explicit qualifications that must travel with the claim |
| `context` | Fact-specific retrieval context, separate from the authoritative claim |
| `source_quote` | Verbatim passage from the source snapshot; compiler locates its exact offsets |
| `evidence_ids` | Direct K/E links present in the quoted passage and existing catalog |
| `related` | Explicit `see_also` pointers, resolved during seeding |

The format intentionally has no free-text confidence score, arbitrary relation
taxonomy, or inferred version facade. Every fact is stored as `authored`, which
means it passed structural validation, **not** that code has proved its meaning.

The source quote and K/E evidence link are distinct. The quote proves where the
claim was extracted from; the K/E record points toward pinned Formly source or
an example. A matching quote and valid ID do not establish that the cited code
entails the claim. This follows the provenance distinction in [W3C PROV-O](https://www.w3.org/TR/prov-o/)
and the source-text/claim separation in [Microsoft GraphRAG outputs](https://microsoft.github.io/graphrag/index/outputs/).
Keeping `context` separate from the claim also leaves room for the chunk-specific
retrieval context described by [Anthropic Contextual Retrieval](https://www.anthropic.com/research/contextual-retrieval/);
that retrieval method has **not** been tested in this slice. [JSON Schema's object
rules](https://json-schema.org/understanding-json-schema/reference/object) informed
the strict required/unknown-field boundary. These are design inferences from
the cited sources, not evidence that this format is optimal.

## Real extraction trial

The trial uses four real prose passages: two from configuration/defaults and two
from expressions/hiding. It produces 13 authored facts in two topic files. One
defaults paragraph yields separate eligibility and defined-value facts; one reset
paragraph yields baseline capture and reset behavior. The hiding passage yields
separate default settings, control removal, model cleanup, array cleanup,
re-registration, default reapplication, and `resetOnHide: false` behavior. A
second hiding passage supplies the shared-key control exception. See the actual
[defaults source](authored/defaults-and-resets.json) and
[hiding source](authored/hiding-and-visibility.json).

The compiler validates required fields, IDs, version against the evidence
catalog baseline, duplicate JSON keys, UTF-8 source material, source SHA,
exact unique source quote, existence of each K/E
record, presence of each cited K/E ID in the quote, and link targets. It then
replaces one SQLite database atomically with documents, facts, evidence links,
and `see_also` links. Only evidence records cited by the authored facts are seeded.
Tests cover valid seeding, stale quotes, unknown evidence,
missing links, duplicate identities, strict fields, failed-build preservation,
repeatable logical output, and detection of tampered seeded facts. The read-only
audit compares every database row with the authored inputs and source spans.

The clean rebuild trial produced two topic records, 13 fact records, four cited
evidence records, 16 fact-evidence links, and six explicit `see_also` links.
All 13 source offsets matched their quoted passage; SQLite integrity and foreign
key checks passed; a second build produced the same audit. The saved
[trial report](../../test-output/contextual-kb-structured-source-trial.json)
records those mechanical results and explicitly reports that semantic entailment
was not verified by the compiler.

A fresh read-only review found two validator gaps: duplicate JSON keys could
silently discard facts, and non-UTF-8 source text caused an exception instead of
a lint error. Both now have failing-before-fix regression tests and were corrected.
The full isolated POC suite passes 34 tests after those fixes; the read-only
database audit still reports the counts above.

The [pinned core defaults/reset implementation](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/extensions/core/core.ts#L109-L168),
[registry defaults](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/services/formly.config.ts#L28-L39),
and [hide transition implementation](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/extensions/field-expression/field-expression.ts#L185-L222)
were read for a development spot check of the trial claims. That is separate
from deterministic compiler validation.

## What this trial proves

This trial tests whether carefully authored, controlled inputs can be seeded as
small, condition-bearing, source-anchored records with valid links and repeatable
output. Four selected passages are not the entire three-document knowledge base.
The earlier 34 unresolved candidate blocks remain historical baseline results,
not silently converted facts. The compiler proves structural and provenance
checks; semantic fidelity of the selected facts requires source review. The
possible future AI authoring workflow was background context and is outside this
trial and its reviews.

The later [expanded source trial](EXPANDED-SOURCE-TRIAL.md) tests more topics and
developer questions without changing this first trial's historical result.

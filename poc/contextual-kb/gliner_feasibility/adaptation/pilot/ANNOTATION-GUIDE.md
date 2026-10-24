# Pilot annotation guide v1

Training-only pilot: 24 questions, four in each of six strata. Read only
questions.json for question content. No model outputs or other annotator labels.
The parent ADAPTATION-EXPERIMENT-DESIGN.md is the canonical experiment design.

Output a JSON list in question order. Each item has id, question, status (clear or
needs_clarification), aspects, entities, relations, rationale. A span is
{text,start,end}, half-open Unicode codepoint offsets. Source substrings only.
Use explicit offsets even for identical strings. Do not normalize punctuation.

Each aspect has id (a1 etc), target_anchor (one span), and these list-of-span
fields: targets, request_cues, conditions, negative_constraints, identifiers,
literals, versions, ui_adapters, references, resolved_antecedents,
unresolved_references. Include all fields, with [] for absent information.
Use the first target in source order as anchor. Distinct asks about one source
target may share an anchor; do not merge to satisfy a library restriction.

Prefer the smallest complete target noun phrase (include its/that when present).
Request cues include the interrogative/action words necessary to state the ask;
they may be discontinuous lists. E.g. a shared 'how are' and 'handled' can appear
in both records. Setup actions belong in conditions, not as extra requested asks.
Requested locations retain 'Where' as part of their cue. A single comparison
record includes both targets. Coordinate outcomes requiring independent answers
are separate records. Shared conditions/scope/negative constraints repeat on each
applicable aspect; global copying is not an attachment judgment.

Condition spans include the introducing preposition/conjunction but not trailing
punctuation. Negative constraints include negator and complete governed phrase.
For 'without X or Y', one whole constraint is acceptable; do not drop 'without'
from the second alternative. A negated requested outcome still uses the negative
constraint field to preserve polarity. A literal false is not a negation label.

Identifiers are exact API/code names (whole paths/generic expressions). Also label
user-defined identifiers with their own entity type. Generic wrapper/control/type
words are not API identifiers. Literals include quotes when supplied. Repeated
mentions get separate spans. Entity map keys: api, custom_identifier, literal,
version, ui_adapter; every key has a list (possibly empty). Do not invent APIs.
Record identifiers can contain either explicit identifier subtype. Identifier-
literal relations use kind=has_value, head=identifier span, tail=literal span.

References include referring expressions that require in-question interpretation.
Use kind=refers_to, head=reference span, tail=antecedent span for uniquely resolved
references. Pronouns with an obvious referent are clear. Ambiguous references
remain in unresolved_references; never guess. Any unresolved reference affecting
interpretation implies needs_clarification. Rationale explains competing readings
or borderline aspect decisions. Missing knowledge about behavior is not ambiguity.

Keep entities global and attach relevant spans to records; conditions may overlap
identifiers/literals. Resolve exact pairings using relations rather than relying
on list position. No Formly answer labels, facts, retrieval, or correctness claims.

Raw independent annotations must be retained before adjudication. Report initial
agreement separately from guideline clarifications and adjudicated gold.

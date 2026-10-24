# Fresh flat-model question set: author notes

Authored independently on 2026-10-22 against `narrow-mentions-v1`. The author
read only the POC guidance, steering, narrow contract, and its envelope validator.
No prior training/evaluation questions, model outputs, failure analyses, candidate
implementations, sealed evaluation, or database content were inspected. No
inference was run. Custom registration names were newly chosen for these questions.

## Composition

`questions.json` contains 48 complete gold envelopes, all `status: ok`, with
empty issues. `families.json` maps every question ID to exactly one family.
There are six questions in each of eight requested families: custom types and
wrappers; validation and errors; expressions and visibility; defaults, model and
reset; repeat, nesting and layout; lifecycle and options; adapters and version
scope; conceptual and claim distinctions.

There are eight genuinely empty mention sets, one per family. The other 40
questions vary in form and ask about library mechanisms, distinctions, timing,
configuration, and evidential scope. They do not request application inspection.
Question lengths range from 71 to 216 Unicode codepoints. This is intentionally
a focused-question set, not a long conversation or compound task benchmark.

Gold occurrence counts:

| Role | Count |
| --- | ---: |
| api_reference | 52 |
| registration_name | 9 |
| model_key | 8 |
| value | 13 |
| version | 10 |
| ui_adapter | 8 |

The set includes dotted and bracketed API paths, dotted and array-form model
keys, quoted strings, booleans, numbers, null, and three opaque expressions.
Opaque expressions retain their entire supplied expression, including syntactic
quotes on the string-expression example, without nested API annotations.
Comparison and negation retain every explicit mention regardless of active scope.
The quoted behavioral proposition in question 045 is not a value mention.
Generic nouns such as field, model, wrapper, and type in ordinary prose are not
promoted to API references; explicit configuration-property occurrences are.

## Validation and interpretation

Every envelope passed the existing `pilot/contract.py` validator. Author checks
also verified 48 unique IDs, eight families of six, eight empty mention lists,
and at least six occurrences each of registration names, model keys, versions,
and UI adapters. Spans are source-ordered, non-overlapping Python Unicode
codepoint offsets into the exact stored question. Syntactic quotes and complete
paths are retained. These checks establish representation consistency, not
semantic annotation correctness; an independent annotation review must precede
freeze and model inference.

Questions are requests for information, not asserted Formly answers. A named
custom registration is not claimed to be built in. Mention annotations do not
prove API existence, compatibility, behavior, registration activation, persistence,
or source support. This set does not measure answering, retrieval, relation
prediction, application investigation, or handling genuinely ambiguous spans.
All examples were selected to support determinate occurrence labels. No supplied
examples intentionally require `needs_review`.

The family balance and role minimums are deliberate coverage choices, not an
estimate of natural developer-question frequency. The version/adapter family
contains a disproportionate share of version and adapter occurrences. Empty
questions are distributed evenly rather than sampled from production traffic.

Pre-freeze review clarification: question 030 now says “dotted string path”
to avoid an incidental configuration-property reading of its final noun.
Question 033 formats the explicit `model` API reference with backticks and
uses “dynamic settings” to avoid an incidental API reading of “expressions”.
Labels are unchanged. An intermediate authoring-markup delimiter defect
that omitted closing brackets from five spans was corrected before freeze;
all complete paths and the array-form key were revalidated against source.

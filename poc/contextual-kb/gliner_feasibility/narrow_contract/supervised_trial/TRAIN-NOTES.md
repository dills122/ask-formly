# Supplemental narrow-contract training annotations

This file documents `train-new.json`: 40 newly authored, clear Formly library
questions, T01–T40, supplementing the 22 existing clear pilot training cases.
Only `../CONTRACT.md` and `../pilot/ANNOTATE.md` were read for semantic guidance.
No development questions, development labels, model predictions, application
code, data/DB, or sealed evaluation evidence were consulted. No existing pilot
annotations were read or edited.

## Coverage

| IDs | Primary coverage | Count |
| --- | --- | ---: |
| T01–T08 | Whole API references, properties, maximal paths, hypothetical API | 8 |
| T09–T16 | Registration names versus supplied model keys and paths | 8 |
| T17–T24 | Quoted values, booleans, null, numbers, escaped strings, opaque expression | 8 |
| T25–T32 | Versions and adapters, including comparison and negation | 8 |
| T33–T40 | Business purposes, unrelated application names, and negative constraints | 8 |

Every envelope uses `narrow-mentions-v1`, `status: ok`, and `issues: []`.
There are 113 mentions: 49 API references, 11 registration names, 14 model keys,
15 values, 12 versions, and 12 UI adapters. Four questions (T33–T36) have empty
mention lists. There are no unresolved annotation ambiguities.

## Annotation decisions

Spans were selected semantically by the author. A temporary Python standard-library
script located each explicitly selected spelling in source order and generated
Python Unicode codepoint offsets. It did not infer labels with regular expressions
or consult a model. After JSON round-trip, validation checked all 40 sequential
IDs, envelope keys, schema/status/issues, legal mention kinds, mention record keys,
positive in-range spans, source ordering, non-overlap, and exact substring equality.
All checks passed.

API paths retain internal quotes and brackets as a single maximal reference.
Markdown backticks are excluded. Syntactic quotes on names, model keys, and values
are retained. In T20 the quoted value contains literal backslash-escaped double
quotes; T21 contains the literal backslash-n sequence, not a newline. In T23 the
entire explicitly identified opaque expression is one value, with no nested API
or null-value annotation.

Repeated occurrences remain separate, notably in T05, T08, T16, T24, and T31.
T12 gives the same quoted spelling distinct registration-name and model-key roles.
T19 distinguishes quoted model keys from boolean and numeric values. Negative
constraints in T28 and T37–T40 still contribute their explicitly named mentions.
HarborDesk and ConsentPortal are explicitly application names and are not labeled.
Business purposes do not imply API or registration names.

The new custom spellings include `harbor-picker`, `consent-badge`, `personCode`,
and `regionKey`. Questions request syntax or explanation; they do not supply
answers or assert library compatibility. T04 explicitly marks its proposed API
as hypothetical. API extraction does not establish API existence. Version tokens
and adapter mentions do not establish compatibility or attach versions to a
particular library through an additional relation schema.

These supplemental gold annotations are initial author output, not inference or
runtime qualification evidence. They must remain unchanged after delivery;
corrections, if later necessary, should be separately recorded with provenance.

# Independent fresh role and boundary cases

Authored 22 October 2026 for the role/boundary adaptation experiment. This file
records authorship and annotation decisions, not model results or a passed gate.

`fresh.json` contains 40 exact question envelopes, IDs `rbf-01` through `rbf-40`.
`families.json` maps each ID to one primary diagnostic family. There are five
questions in each of eight families. Every question explicitly concerns Formly
library/configuration semantics; none requests application investigation. All
40 have `status: ok` and no issues. Six intentionally have no mentions.

## Provenance and independence

The author read the supplied task, POC `AGENTS.md` and `STEERING.md`, the narrow
`CONTRACT.md`, pilot `contract.py` and `test_contract.py`, and the older top-level
schema definition. The narrow contract is authoritative. No training questions,
prior evaluation questions, experiment results, or model outputs were read.
No model inference was run. The examples are newly authored synthetic questions,
not claims that an API exists or that a described Formly behavior is correct.

The training author and this author exchanged reserved custom spellings only,
not questions or gold spans, to avoid accidental custom-name overlap. Shared
API vocabulary and deliberate role-collision spellings remain necessary for the
experiment. This is independent authorship, not a claim that every natural word
is absent from training. Downstream reviewers may inspect this set before it is
frozen; their review and any inference must be recorded separately.

## Diagnostic taxonomy

| Family | IDs | Focus |
| --- | --- | --- |
| ordinary_noun_vs_api | 01–05 | Model, field, type, wrapper and control prose versus explicit configuration-property occurrences. First three questions are empty. |
| registration_vs_value | 06–10 | Registered type/wrapper/validator names versus labels, defaults and literal content, including repeated identical strings. |
| model_key_vs_registration | 11–15 | Named registrations versus explicit model addresses, including an array-form key. |
| backtick_api | 16–20 | Complete API paths and classes with Markdown delimiters excluded; includes a hypothetical API-existence question. |
| backtick_quoted_registration_key | 21–25 | Syntactic single/double quotes retained within Markdown, and registration/key roles preserved. |
| same_word_different_roles | 26–30 | Different occurrences of identical words assigned their contextual roles; ordinary prose occurrences remain unannotated. |
| opaque_expression_boundaries | 31–35 | Complete arrow functions, expression text, an array literal and an object literal retained as single values. |
| negative_mixed_library_contexts | 36–40 | Ordinary quoted prose is not requested literal content; mixed Angular/Formly and negated adapter scopes remain explicit mentions. First three questions are empty. |

Each case belongs to only one primary family for reporting, though contrasts
naturally overlap. The six empty questions are 01, 02, 03, 36, 37 and 38.
The dataset contains 104 mentions: 42 API references, 19 registration names,
15 model keys, 16 values, six versions and six UI adapters. API coverage remains
substantial rather than making every difficult question empty.

## Boundary and role decisions

- Markdown backticks are excluded. Syntactic string quotes remain in names,
  keys and values, including double-quoted strings in questions 22 and 25.
- The complete array-form key in question 14 is one model-key occurrence:
  the question explicitly presents the array as a model address.
- In question 08 the supplied string is explicitly a registered validator name,
  not an arbitrary configuration string.
- Complete bracketed API paths are single API references, with no nested path
  fragments or strings emitted separately.
- Explicit expression/array/object values in questions 31–35 are opaque. Their
  internal apparent APIs, strings, numbers and booleans produce no extra spans.
- Quotes in questions 36–38 delimit ordinary explanatory prose. Those questions
  do not supply configuration values or request literal field content.
- A hypothetical API in question 19 remains an API reference: extraction makes
  no existence assertion. Versions from either library and adapters mentioned
  under negation are preserved without asserting active scope or attachment.

## Validation

Offsets were computed while assembling each exact question from authored text
segments, using Python string lengths (Unicode codepoints). The existing pilot
`validate` function accepted all 40 generated envelopes. After serialization,
a second read-back check validated all envelopes and confirmed unique IDs,
exact family coverage, five cases per family, six empty cases and all six roles.
This checks representation integrity, not an extractor's performance. Independent
semantic review remains part of the parent experiment's pre-freeze workflow.

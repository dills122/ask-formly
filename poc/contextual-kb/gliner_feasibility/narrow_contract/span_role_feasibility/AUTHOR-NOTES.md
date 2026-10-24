# Fresh span-role feasibility set — author notes

Status: authored and mechanically validated; ready for blind independent semantic
review, not frozen. Authored 22 October 2026.

## Isolation

The author read only the POC AGENTS.md and STEERING.md, narrow-contract
CONTRACT.md, and pilot/contract.py for task-specific source material. No previous
cases, training data, experiment results, inference harness, predictions, or
application source were read. The tool initialization instructions were also
read. No model inference was run. Only the three assigned fresh-set files were
written. Reserved custom spellings were sent to the development author without
questions or annotations.

## Contents

fresh.json is a list of 40 complete narrow-mentions-v1 gold envelopes.
families.json maps each question_id to one family slug. Each of eight families
contains five questions:

- registration-versus-value
- key-versus-value
- adapter-versus-registration
- api-versus-prose
- repeated-occurrences
- quotes-and-markdown
- opaque-expression-boundaries
- negative-no-explicit-mentions

All six roles occur. Six questions have empty successful mention lists: the fifth
API/prose case and all five negative cases. The other 34 questions contain 101
mentions. All envelopes currently have status ok; no genuinely unresolved
annotation was intentionally introduced.

## Annotation decisions

Role assignment follows each occurrence's explicit context. Identical spelling
can denote a supplied registration, model key, literal content, or adapter in
different positions. Syntactic string quotes belong to names, keys and string
values; Markdown backticks do not. Plain explanatory nouns and quoted behavioral
claims remain unannotated. A hypothetical property explicitly proposed as a
Formly API reference is annotated without asserting that the property exists.

Compound paths remain maximal API spans. Explicit opaque expressions remain
single values, including their inner apparent property paths, keys, registration
spellings, and adapter spellings. Repeated mentions retain separate offsets.
The question with a string containing backticks deliberately distinguishes
backticks inside the requested literal content from surrounding Markdown.

These are focused library questions, not requests to investigate an application.
The questions ask about behavior and do not supply behavioral answers. Adapter
and version occurrences do not assert compatibility. Families target role and
boundary distinctions but do not guarantee that every question creates a model
or decoder conflict; conflict frequency must be measured separately.

## Validation and review boundary

Offsets were generated from manually chosen annotated substrings in the original
question text, using Python Unicode codepoints and exclusive end bounds. Every
envelope passed pilot/contract.py validate against its exact question and ID.
Additional assertions checked 40 cases, six empty cases, and coverage of all six
roles. Eight groups of five were constructed explicitly.

Mechanical validation establishes source fidelity and structural validity only.
Independent blind review should assess whether every required occurrence is
included, every excluded occurrence is correctly omitted, and each role/boundary
agrees with the contract. Freeze only after that review and any corrections.

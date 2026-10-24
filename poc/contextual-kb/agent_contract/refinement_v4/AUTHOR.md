# Fresh case authorship and frozen expectations

Authored 23 October 2026, before planner generation for these twelve cases.

## Isolation and ownership

The author read only the supplied assignment, project guidance, POC AGENTS.md
and STEERING.md, refinement_v2/CONTRACT.md, and refinement_v4/LEDGER-RULES.md.
The author did not inspect the v4 contract or implementation, previous cases or
outputs, sealed evaluation material, or the knowledge database. No answers were
researched. Only fresh.json, fresh-rubric.json, and this document are deliverables.
No other agent's files were changed.

## Frozen rubric policy

The request set and semantic expectations are now frozen before generation.
The rubric's aspects describe independently sought information, not mandatory
wording or arbitrary exact output counts. Equivalent phrasing is acceptable;
all distinct aspects must remain represented without unsupported extra lookups.
Explicit comparisons retain their alternatives together. Each generated question
must independently retain its applicable scope and constraints.

Every mandatory_conditions item requires a meaningful verbatim excerpt from the
request in the actual condition ledger and the identical case-sensitive excerpt
in each question assigned to that binding. The examples are non-exhaustive
acceptable source excerpts, not a closed whitelist. Longer or overlapping excerpts
can satisfy several conditions when they remain meaningful and have the correct
attachment. Local constraints must not spread to other questions. Identical
excerpts must be combined with all applicable zero-based question indexes. Text-only
paraphrases do not satisfy the ledger requirement, even when semantically accurate.
No fixed ledger-entry count is imposed. The full predeclared ledger rules govern
exact schema and binding validity; this rubric does not weaken those requirements.

The exclusions field describes mistakes to reject in evaluation; it is not a
second list of source constraints requiring generated bindings. Active user
exclusions are also represented in mandatory_conditions. Relevant API tokens and
custom names must survive in question text without automatically creating extra
ledger conditions. Empty application-only output requires an empty ledger.

## Predeclared attachment and ambiguity decisions

- F01: the final exclusion applies to existence and contingent meaning; hiding
  is local to the meaning question. Do not assume the supplied option exists.
- F02: polling is excluded only for observation. Persistence is excluded globally.
- F03: the two natural-language exclusions apply to all three operations.
- F04: retraction removes the quoted exclusion. The comparison supersedes the
  initial single-setting scenario for both requested outcomes.
- F05: the quote supplies a scenario for verification, not an active instruction
  or established outcome. The follow-up explicitly shares that scenario.
- F06: the dependency relationship and undecided value mapping apply to configuring
  the property and observing changes in that scenario. No truth value is supplied.
- F07: the hiding transition attaches to model value; the later showing transition
  attaches to FormControl. The setting and disabling exclusion apply to both.
- F08: completed implementation and registration are prerequisites, not new asks.
- F09: comparing API concepts is an operation, not unresolved scenario alternatives;
  no ledger conditions are required and both global constraints are null.
- F10: all requested work is application investigation. Its negative instruction
  cannot create a library question or nonempty ledger.
- F11: per-question scopes differ, so both global fields are null. The last sentence
  reinforces attachment of existing scopes rather than adding another condition.
- F12: uncertain version must remain uncertain globally and in the question. The
  rubric's version string represents the two alternatives semantically; equivalent
  uncertainty-preserving strings are acceptable. The exact source-excerpt rule is
  still mandatory in the ledger and assigned question. Only the model outcome is
  sought; the negative control restriction is active and requires a binding.

These decisions were made from source requests and the predeclared ledger policy,
without inspecting generated outputs. Any later rubric revision must be separately
recorded as post-generation and must not silently replace this frozen baseline.

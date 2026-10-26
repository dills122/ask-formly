# Condition-generation candidate v1

Status: isolated runtime candidate, not installed or qualified. No hosted calls
were made during implementation. Arrays-v1 remains a failed historical
qualification; this candidate does not alter its artifacts, facts or decisions.

## Failure and change

Arrays-v1 repeat 2 candidate Q20, planner attempt
`8ec371824b9247c6a89fd54eb8a9b007`, emitted valid JSON with an incorrectly
lowercased source condition and an empty `question_indexes` array. The unchanged
validator rejects source grounding first; changing only its opening letter still
fails the nonempty-index requirement. The exact saved core/request is retained
as a self-contained test fixture, including original questions and reasons.

This candidate strengthens generation prospectively:

- CONTRACT.md contains the complete frozen qualification_v3 contract as a prefix,
  followed by a source-copy and nonempty binding completion audit. It preserves
  existing semantic scope rules and requires preserving conditions and questions.
- plan.schema.json differs only by `minItems: 1` on each binding's index array.
  The outer bindings list and questions list may still be empty.
- planner.py uses candidate-local contract/schema paths. It reuses the frozen
  command builder, strict JSON decoder and model/settings constants; its local
  transport preserves the existing API and raw request/events/stderr/receipt audit.
  It never mutates the frozen planner module's globals.

Compose `CapitalizingPlanner(CodexPlanner(directory))` as before. The promoted
narrow wording adapter and strict `build_plan` validator are unchanged. Candidate
CodexPlanner, like baseline CodexPlanner, returns raw core plus generation receipt;
validation remains the responsibility of this composition and the service. There
is one hosted attempt, no recovery call, no inferred indices, and no broader
case-folding. Invalid output fails closed before retrieval.

## Verification

Run from the repository root:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/condition_candidate_v1 -p test_planner.py
```

The MCP environment supplies jsonschema. Before the contract/schema change, the
actual schema acceptance test failed because it accepted empty indices; the
contract and schema-difference tests also failed (3 failures / 12 tests). After
the change, all 12 tests pass. Tests exercise the exact saved invalid plan,
capitalization-only failure, valid mapped bindings, lost bound conditions,
negation, local restriction placement, API spelling, malformed indices, empty
out-of-scope plans, one-shot failure and candidate paths/tool-disabled settings
with raw audit retention. The hosted subprocess boundary is replaced only in the
transport test; there is no model/DB access.

## Limits and qualification

The schema constrains structure, not semantic correctness. The unchanged strict
validator checks declared binding excerpts and assignments; it cannot discover
undeclared conditions or prove correct semantic attachment. In particular, tests
that reject a removed negation retain its ledger entry: they do not claim to catch
a model dropping both the condition and its ledger. Contract wording is a model
instruction, not a semantic proof. Fresh fixed live qualification must assess
complete requests, local/shared scope, negation, spelling, all conditions and
requested information, and successful evidence delivery. Existing failed attempts
must remain failures; successful new attempts cannot overwrite them.

No retry mechanism or major architecture is introduced. Adding one later would
require a separately reviewed design preserving all source constraints/questions,
all raw attempts and final strict validation.

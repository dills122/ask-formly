# Fresh challenge set — frozen before inference

Authored independently from the six-role narrow-mentions-v1 contract. This is a
small, targeted diagnostic challenge, not a representative estimate of general
question-layer accuracy or Formly answer correctness. No model was run by the
test author. Questions make no assertion that a supplied custom registration is
built in, or that a quoted behavioral claim is true.

## Exposure boundary

The author read the POC AGENTS.md and STEERING.md, narrow_contract/CONTRACT.md,
and the existing pilot/contract.py validator. Repository README.md and
development guidance were read for scope. No prior training/dev examples,
model results, new adaptation code/data, or sealed old evaluation content were
read. A, v2, pilot, and data/DB were not edited. The contract itself contains
public worked examples; this is contract-only independence, not independence
from the schema specification. Authoring and mechanical span validation occurred
before the challenge freeze and before any challenge inference.

## Families and annotations

challenge.json is a JSON list of 24 complete expected envelopes.
challenge-families.json maps question_id to a family; no family metadata is
inserted into model input.

- repeated_literals: eight questions; each includes three occurrences of one
  literal value, with a negative constraint attached to at least one occurrence.
  All explicit occurrences remain required mentions, including negated ones.
- same_string_roles: eight questions; each reuses one quoted string as a
  registration_name, model_key, and value, with explicit contextual role cues.
  Some registrations are wrappers or validators rather than renderer types.
- quoted_claims_vs_literals: four claim-only negatives for value extraction,
  followed by four questions containing both a quoted claim and an identical
  explicitly supplied configuration string. Claim-only questions can still have
  other valid API, version, adapter, or boolean-value mentions. These are
  negatives for the quoted claim span, not necessarily empty-output cases.

The eight custom strings are reserved for this challenge only: opal-orbit,
cedar-latch, velvet-tern, amber-pivot, cobalt-reed, silver-harbor, moss-compass,
ivory-kite. Do not use these surface strings in adaptation training or dev data.

All questions are focused library/configuration questions; none requires
application discovery. There are no deliberately ambiguous annotations.
All expected statuses are ok, and issues are empty. This does not authorize
forcing ok on ambiguous real inputs or converting model errors into abstentions.
Quotes remain part of names, keys, and string values; offsets are Python Unicode
codepoints. Mentions are source ordered and nonoverlapping. Negation and
relationships remain in the complete question, not a predicted relation graph.

## Validation and freeze

The unchanged pilot/contract.py validate function accepted all 24 envelopes.
An additional mechanical check verified unique IDs, eight cases per family,
and all six roles represented. Manual review of the authored annotations checked
claim exclusion and the role cues; the validator alone cannot establish gold
semantic correctness. challenge-freeze.json records SHA-256 digests of these
three authored files and of the contract/validator used, plus case/role counts.
Frozen files must not be rewritten in response to model predictions. Any later
annotation defect requires a separately recorded correction and both original
and corrected reporting, not a silent replacement. Both trained GLiNER models
must receive identical original question strings and extraction settings.

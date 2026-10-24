# Fresh request and rubric authorship

Authored independently on 2026-10-23 as three batches of eight realistic Formly question-layer requests, N01–N24. The author owned only this file and `data/fresh-cases.json` / `data/fresh-rubric.json`. No prior cases, generated outputs, new v6 prompt, sealed evaluation, DB contents, model weights, or web sources were inspected. No Formly behavioral answers or API support assertions were used as ground truth. Supplied speculative API names are objects of neutral support questions.

Actual file contents read:

- `/Users/dsteele/repos/ask-formly/AGENTS.md`
- `/Users/dsteele/repos/ask-formly/poc/contextual-kb/AGENTS.md`
- `/Users/dsteele/repos/ask-formly/poc/contextual-kb/STEERING.md` (required by POC guidance)
- `/Users/dsteele/repos/ask-formly/poc/contextual-kb/agent_contract/refinement_v2/CONTRACT.md`
- `/Users/dsteele/repos/ask-formly/poc/contextual-kb/agent_contract/refinement_v5/LEDGER-RULES.md`

A filename-only search located applicable guidance and the permitted conceptual contracts. No other contract contents were opened. The parent assignment and supplied project instructions also informed the isolation boundary.

## Rubric interpretation

`aspects` describes required meanings, not exact wording or a rigid number of questions. A legitimate compound question or alternate decomposition passes if independently requested outcomes remain explicit and all conditions attach correctly. Each `conditions` item names a mandatory source restriction and its semantic applicability, rather than assuming output question indexes. Meaningful equivalent source excerpts, overlapping excerpts, and combined entries are acceptable when they retain every condition and correct attachment. For a ledger-based output, the selected excerpt must actually be verbatim from the request and appear in each bound question; a paraphrase alone does not meet that evidence rule. Prerequisite pronouns must be resolved to their capability without turning support into an assumed fact.

All active scenario, dependency, prerequisite, exclusion, uncertainty, eligibility, and scope conditions are listed. A supplied custom name or topic alone does not create a ledger obligation. Exact API spellings, custom values, and pairings still belong in the questions. `scope` gives expected global constraints; N12's notes explicitly permit a source-grounded uncertain version string in place of null, while forbidding a guessed resolved version. N20 has heterogeneous comparison scope, so both global fields are null and each side stays explicit. Unspecified adapters are null; explicit core-only scope is `none`.

Same-field return transitions may use one self-contained excerpt to represent relevant prior history and return meaning; duplicate history bindings are not required. Explicit preceding prerequisites must survive. Unrelated subjects and locally scoped method restrictions must not leak across aspects. Empty cases require no invented library question or ledger entry. No-condition controls should not acquire invented conditions.

## Coverage

- Batch 1: nested support gates; dynamic configuration and observation; shared/local exclusions; corrected scope; same-field return versus unrelated field; registered custom key/type pairing; no-condition comparison; application-only empty control.
- Batch 2: nested hypothetical hook support; dependent select options with distinct value/control outcomes; local observation restrictions; unresolved version/adapter scope; explicit preceding event versus unrelated field; mixed registration prerequisites; unconstrained concept lookup; editing-only empty control.
- Batch 3: nested conditional applicability; dependency plus contingent observation; shared initial value and hidden/disabled comparisons; heterogeneous version/adapter comparison; return-state history versus background subject; registered type/default pairings; two no-condition concepts; unresolved-pronoun empty control.

Validation: parsed both JSON files, checked 24 unique sequential IDs, three batches of eight, aligned rubric IDs, and every proposed condition excerpt as an exact substring of its request. This is authoring validation, not a model evaluation or a claim that a particular implementation passes.

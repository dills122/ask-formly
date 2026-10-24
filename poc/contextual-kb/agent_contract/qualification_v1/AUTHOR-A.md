# Author A provenance

Authored K01–K24 independently for fixed qualification groups 1–3, eight requests per group. Owned only `data/author-a-cases.json`, `data/author-a-rubric.json`, and this provenance file. Requests and criteria were authored together before any candidate generation or result inspection. No candidate responses were generated, and no subagents were used.

Read these required sources:

- Repository `AGENTS.md`, `README.md`, and `docs/development.md`.
- `poc/contextual-kb/AGENTS.md` and `STEERING.md`.
- `agent_contract/refinement_v2/CONTRACT.md`.
- `agent_contract/refinement_v7/LEDGER-RULES.md`.
- `agent_contract/qualification_v1/POLICY.md` and `PROTOCOL.md`.

A filename-only `rg --files` inventory located instructions and named documents; it exposed historical directory and document names. Required README, development, steering, and contract documents incidentally contain historical result summaries, examples, earlier experiment names, known limitations, and baseline scope. Those required contextual exposures are disclosed here; no linked historical reports, old case files, old rubrics, old candidate responses, old results, full candidate contract, another author's output, sealed evaluation contents, DB, model weights, or web sources were opened. The initial combined read was truncated, so the affected required documents were subsequently read in smaller complete calls.

Cases include ordinary conceptual discovery, custom type and wrapper setup, an application-only request, straightforward scoped configuration, unknown and uncertain scope, corrected and heterogeneous scope, basic state questions, paired model/control outcomes, default-value comparisons, temporal changes, and observation events. This is synthetic policy-informed development evidence; independent authorship does not make it a random or production-representative sample.

Rubric `aspects` are semantic information needs, not exact output wording or question-count requirements. Each `conditions[].applies_to` refers to an exact string in that rubric's `aspects`. Listed excerpts are source anchors for required meanings; alternative meaningful verbatim excerpts or larger shared excerpts are acceptable when they preserve scope and meet the frozen ledger contract. They are not an exact-match answer key. Harmless grounded redundant context and neutral same-capability support caveats are governed by POLICY.md throughout, even when a case note does not repeat that permission. Additional unsupported library claims, inferred app behavior, or investigation plans remain outside the task.

Scope strings are canonical semantic expectations. Uncertainty-preserving equivalent strings remain acceptable for K11; this is not permission to normalize an uncertain version into a certain one. K10 has explicit wholly unknown scope and null globals, with source bindings still required. K13–K15 retain heterogeneous or alternative scopes in question text while using null for the relevant global. K23 explicitly permits optional prospective same-field default context without treating “Separately” as independent scope.

Validation performed locally: both files parse as JSON; IDs K01–K24 are unique, ordered and paired across source and rubric; each batch has eight cases; every listed source excerpt occurs verbatim in its request; every condition attachment refers to an authored aspect. Manually reviewed conditions against stage, event, scope, literal pairing and local/shared ownership. No Formly runtime correctness, candidate quality or qualification outcome is claimed by these checks.

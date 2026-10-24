# Fresh case authoring provenance

Authored 24 new requests (Q01–Q24), in three batches of eight, and a corresponding prospective semantic rubric. This author was separately delegated only the fresh-case files and this note. No model responses were available during authoring. The requests ask library questions and do not certify any Formly behavior.

## Interpretation of the rubric

Aspect names identify meaning to cover, not required wording or a rigid number of output questions. Accept equivalent useful decomposition, provided distinct requested operations remain searchable and explicit comparisons remain intelligible. Conditions list representative meaningful verbatim source excerpts with intended aspect attachments. Accept other meaningful contiguous source excerpts or combined spans where their whole meaning applies to every bound question. Every chosen emitted excerpt must occur exactly in the original request and each assigned question. Do not reward uninformative fragments merely because they match.

No minimum or maximum ledger size is imposed. Do not require an exact match to these representative spans. Required conditions must be present both in the appropriate question and its ledger; the presence of text alone is insufficient. Targets and operations must survive in question wording even when they do not require a condition entry. Scope values describe intended global constraints, with per-question scope retained for heterogeneous cases.

Same-referent history is permissible in Q03 and Q21 without requiring it. Explicit historical wording may preserve initial setup in Q13 and prior hiding in Q15. Extra grounded context is not by itself a failure or a reason to force a minimal ledger. It fails when it invents causality, eligibility, current setup, or scope. Q04 explicitly requests independence; Q05 explicitly supplies eligibility. Method restrictions remain local unless the source shares them. Conditional ancestry is required for Q09 and Q22, not collapsed by logical implication.

## Actual access

Read or requested through shell file reads:

- Root `AGENTS.md` and the root guidance supplied in the task context.
- Root `README.md` (initial combined read and a later lines 80–210 read).
- `docs/development.md` (initial combined read, then lines 1–180 and 181–400).
- `poc/contextual-kb/AGENTS.md`.
- `poc/contextual-kb/README.md`.
- `poc/contextual-kb/STEERING.md`.
- `poc/contextual-kb/agent_contract/refinement_v2/CONTRACT.md`.
- `poc/contextual-kb/agent_contract/refinement_v7/LEDGER-RULES.md`.
- `poc/contextual-kb/agent_contract/refinement_v9/CHANGE.md`.

Some combined command output was truncated. Follow-up reads recovered the POC guidance, steering, and the requested contract/rules/change were visible in the initial returned output. Root overview/development documentation includes historical result summaries; those incidental summaries were not used to construct these requests. No linked historical reports were opened. A filename-only `rg --files` inventory under `poc/` located guidance; it did not inspect old case content. Serena's initial instructions were read as required by the tool setup. No structural code exploration was performed, so no graph results informed the cases.

Did not read the full v9 prompt, old cases or rubrics, generated outputs, old result artifacts, sealed evaluation material, DB contents, model weights, or web sources. No subagents were spawned. Only the three assigned repository files were written; a temporary authoring script was also created under `/tmp`.

## Validation

Parsed both generated JSON files independently after writing. Checked 24 aligned unique IDs Q01–Q24, exactly eight cases in each integer batch 1–3, required record keys, nonempty unique aspect names, every condition excerpt as an exact request substring, and every attachment against the case's aspect names. Empty controls have empty aspects and conditions. Validation does not establish a model pass or any library behavior; evaluation is separate.

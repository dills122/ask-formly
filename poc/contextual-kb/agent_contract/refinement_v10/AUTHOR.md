# Fresh v10 case authorship

Authored independently by the fresh-case subagent before planner generation. This is a synthetic development set, not sealed evaluation or evidence of production generalization. The author did not inspect prior cases, rubrics, responses, grades, old results, the full v10 candidate, sealed evaluation contents, DB contents, weights, or the web. No planner response generation was run and no subordinate agents were used. Cases were newly composed from the delegated coverage requirements and the permitted guidance; they were not copied from prior experiment cases. Independence is procedural, not a claim of statistical independence from the model's general training or other synthetic authors.

Only these owned files were created: `data/fresh-cases.json`, `data/fresh-rubric.json`, and this record. Existing files were not edited. IDs U01–U24 are allocated in order to integer batches 1–3, eight per batch. U08 and U24 are empty out-of-scope controls. Other cases combine ordinary library questions with selected scope, dependency, timing, correction, literal, or exclusion challenges.

## Sources seen

- Delegated task instructions, including the required coverage topics and JSON shape.
- The user-supplied repository AGENTS.md and environment instructions.
- Repository `AGENTS.md`, `README.md`, and `docs/development.md`.
- `poc/contextual-kb/AGENTS.md` and `poc/contextual-kb/STEERING.md`.
- `poc/contextual-kb/agent_contract/refinement_v2/CONTRACT.md`.
- `poc/contextual-kb/agent_contract/refinement_v7/LEDGER-RULES.md`.
- `poc/contextual-kb/agent_contract/refinement_v10/CHANGE.md` and `PROTOCOL.md`.
- Serena's initial tool instructions (tool-use guidance only, no code or prior experiments).
- A repository filename-only inventory locating the required documents. The inventory exposed filenames, not old case or result contents.

The initial combined document read was truncated, so README, development guidance, and the POC instructions/steering were subsequently read separately. The v2 contract, v7 ledger rules, and v10 change/protocol were visible in the combined read. No linked historical reports were opened. No source-code structural exploration was needed.

## Prospective rubric semantics

The rubric names requested aspects, meaningful verbatim source conditions and their applicable aspects, forbidden interpretations, global scope, and explanatory notes. These mappings precede any response generation and are submitted for parent review and freeze. They impose neither a fixed question count nor a minimum ledger size. Semantically equivalent decomposition is acceptable when each actual interrogative clause covers its aspect with the right conditions; a compound question must not move a local condition to another clause. Larger verbatim excerpts may satisfy a condition if their full meaning applies; unrelated padding is not a substitute for the meaningful relationship. Repeated synonymous restrictions need not create duplicate ledger entries. Target/API names alone are not automatically conditions.

Scope values distinguish explicit core-only (`none`) from unknown/unspecified/heterogeneous (`null`). A null global never excuses an active explicit uncertainty statement missing from the applicable question and ledger. Plain versions normalize their Formly/v prefix only. Uncertain version strings retain their uncertainty and range. Rubric `scope` values are the prospective expected projection, not claims about actual installations.

## Uncertainty bindings declared before generation

| Case | Active uncertainty and binding |
| --- | --- |
| U01 | Unknown release and unidentified adapter bind both key and fieldGroup aspects. |
| U02 | None; known version/Material. |
| U03 | Probably >=6.2 <7, not verified, binds the null/zero default comparison; Bootstrap known. |
| U04 | No scope supplied; do not invent uncertainty text. |
| U05 | Unknown adapter only on select labels; parser scope is explicitly core-only; version shared known. |
| U06 | Undecided adapter binds configuration and observation; version correction resolves to 6.3.12. |
| U07 | Quoted unknowns do not bind; asserted review scope is known core-only. |
| U08 | Unknown version/adapter do not create library aspects or ledger bindings in empty control. |
| U09 | Unknown adapter binds focus support, contingent use, and independent hooks aspect. |
| U10 | Unknown version binds all three nested support/use aspects; Material known. |
| U11 | Adapter not chosen binds both wrapper aspects; version known. |
| U12 | No uncertainty; distinct known version/adapter pairings remain in comparison with null globals. |
| U13 | No uncertainty; known core-only. |
| U14 | Explicit lack of version/adapter information binds key comparison and unrelated description configuration. |
| U15 | No scope supplied; no invented unknown statements. |
| U16 | Unsettled Material/Bootstrap alternatives bind support and configuration; version known. |
| U17 | Unknown version binds hint and error; correction retracts unknown adapter in favor of Material. |
| U18 | Unknown version binds only Material select; core expression has known 6.3.12. |
| U19 | Unconfirmed 6.3.x/7.0.x and unknown adapter bind registered-type use and default behavior. |
| U20 | Quoted unknown adapter does not bind; asserted scope is known Bootstrap. |
| U21 | No uncertainty; known Material. |
| U22 | Unknown installed version binds read-only configuration and editable-return model outcome; adapter absent. |
| U23 | No uncertainty; known Material. |
| U24 | No uncertainty; known global scope is retained but empty control has no ledger bindings. |

The data files pass JSON parsing, count/ID/batch checks, exact source-substring checks for every condition, and aspect-reference checks. These are data integrity checks only; the parent must review semantic quality before freezing. No experiment outcome has been observed.

## Author handoff hashes

- `data/fresh-cases.json`: SHA-256 `7d07308b23a7d5d6817a1a1c2637c00e3d4c7d5e50f9ea7403aa7e8bb4a14676`
- `data/fresh-rubric.json`: SHA-256 `8805f4f4ac1d563cb7bb8ff4c82797b356638996ccae21ec587cb3b7833e439c`

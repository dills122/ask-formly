# Shared-condition regression development cases

Authored 2026-10-23 as new, self-contained development evidence before inspecting any refinement-v3 candidate prompt, implementation or model output. This is not sealed or held-out evaluation. The parent agent must independently review these annotations before freezing them.

Behavior references were only the POC `STEERING.md` and the unchanged `agent_contract/refinement_v2/CONTRACT.md`. The test-driven-development skill supplied the reproduction-first workflow. The author extracted only H07 from the v2 cases file; no other old cases, sealed evaluation, database, baseline or model outputs were inspected. No model responses were generated and no comparison was run. A RED result remains to be established by the parent harness; authored expectations alone do not prove a failure or a fix.

`cases.json` contains 13 requests: R01 is the exact known H07 request, and N01–N12 are newly authored. `rubric.json` has one matching entry per request. Coverage includes all-aspect shared conditions, conditions shared by only a subset of aspects, local-only conditions, asymmetric version/adapter scope, negation, literal/property pairings, explicit correction, condition retraction, ambiguous antecedents and an empty no-library case.

## Semantic judging

The rubric describes meaning, not required generated wording. Accept equivalent wording that preserves the complete relationships. Preserve exact supplied API spellings and literal values where relevant; this does not require an exact generated sentence. Expected aspects are separately searchable questions except where the request explicitly asks for a comparison. Each applicable shared or local condition must occur meaningfully in each relevant focused question. A condition solely in another question, the reason, global metadata or an unattached fragment does not make a question stand alone. Do not reward copying meaningless fragments, contradictions, or spreading local restrictions globally. Evaluate question text in its entirety, including whether it asserts an unestablished outcome instead of asking neutrally.

Apply the v2 output contract as well as these case-specific semantic expectations: exactly the two specified top-level fields, nonempty question/reason strings, no answers/application work, no invented aspects, deduplication, and grounded library constraints. All nonempty cases state their version and adapter, which must also remain in the relevant question text. Except N04, global scope follows the stated version and adapter (strip only the plain Formly/v prefix); N01 uses ui_adapter `none`. N04 requires both global constraints null and retains each distinct scope in its respective question. N12 requires an empty question list and null constraints because no version or adapter was supplied.

## Annotation decisions for review

- R01 intentionally carries the selected-value-still-present condition into the options-change question. The explicit “Those conditions apply to both questions” overrides any narrower default reading of the preceding sentence. Disabled, asynchronous options and no enabling also remain attached to both questions. R01 does not ask to debug the background timeout.
- N06 is a single explicit comparison. The initial undefined model value applies to both alternatives; default values 0 and false must remain paired with their respective resetOnHide settings.
- N08 retracts only disabled-only scope. Questions may say “regardless of disabled state” or otherwise clearly retain that unrestricted scope; they must not add “without enabling” from the superficially similar regression case.
- N09 deliberately has an unresolved antecedent and no library capability supplied for the custom-component sentence. Only the independent props.label lookup is justified. The rubric does not choose a referent or require a clarification workflow.
- N10 uses shared conditions across a subset: hide/reset applies to the first two questions, while version/adapter applies to all three. Already registered excludes creation and registration expansion.
- N11 asks only for registration of the custom type; the type name does not imply masking, validation, implementation or usage requests.
- N12 deliberately supplies no justified library lookup despite mentioning Formly. Empty output is expected.

These scope decisions should be independently reviewed before freeze; none requires guessing actual Formly runtime behavior. No answer-correctness, retrieval or corpus-coverage claim is made by this suite.

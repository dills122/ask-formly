# Prospective independent label review — instance 1

Reviewed all 36 fresh requests, all 45 derived questions, all 46 catalog facts, and all 36 saved foundation envelopes before retrieval/model predictions. This review used the complete catalog claims, conditions and limits, not initial relevance IDs as an exhaustive answer key. No sealed evaluation, prior predictions, models or database were consulted or changed. The source graph does not cover this POC; direct file reading was used for these non-code data/contracts. No application behavior or source API implementation was inferred.

Artifacts: `data/cases-reviewed.json` contains full-catalog relevance, required substitute groups, support class and explicit missing parts. `data/gold-proposed.json` copies every question row verbatim and adds reviewer-authored spans, rationale and prospective alternatives. `test-output/labels-author.py` records the manually selected strings and roles; Python `find` calculates offsets only. `test-output/labels-validation.json` records mechanical validation. These are proposed development labels awaiting parent adjudication and independent preflight, not frozen evaluation truth.

## Relevance policy and decisions

Relevant facts must directly support an answer or a necessary qualification, not merely mention an API or topic. All catalog facts were considered for every request. Required groups are AND across groups and OR within each group; extra corroborating relevant facts are not automatically required. Coverage of these catalog-backed groups is not proof of complete answerability for partial cases.

- R01/R13 include equivalent fallback support and eligibility; zero is already defined in R01.
- R04 includes the associated-fields condition on control unregistration as direct explanation of the shared-key exception.
- R06 expands to all direct registration/use alternatives, plus supported registration fields and the key/type distinction. General defaults/inheritance background is excluded. The key/model identity group is necessary for the supplied distinct key and custom type.
- R07 requires the ancestor-composition fact for the requested explanation; merely stating non-equivalence is relevant but does not alone explain why.
- R14 is **partial**: supplied reset model plus rebuild/control reset is established, but saving that supplied model as the durable baseline for a subsequent no-argument reset is not established by the catalog. The separate updateInitialValue fact is relevant to explaining that distinction, not proof of the missing claim.
- R16 includes direct default-retention/fallback support alongside the visibility-specific facts; the latter two are required.
- R18 requires the concrete input-derived example, which alone establishes the requested pattern. Registration-options and configuration-contribution facts corroborate without creating artificial extra coverage obligations.
- R19 includes the conditional hide target as direct support for the alternative configuration mechanism.
- R25 includes initial model preference and the fallback/defined-value behavior explaining the comparison.
- R28 includes the shared-key and resetOnHide-false qualifications, while requiring the two independently requested control/value outcomes.
- R30 includes reverse merge and direct registration configuration facts. Only reverse merge is necessary to explain the interaction; complex precedence is outside the catalog claim.
- R31 is **partial**: default `modelChange` is established, but the exact meaning/triggering boundaries are not fully defined by the catalog. Its context and formState observation caveat do not establish every triggering detail.
- R11/R12/R23/R24/R35/R36 retain empty relevance and required groups. This means **not established in this catalog**, never false in Formly. R12/R23's shared context fact and R36's retention fact are adjacent background, not support for automatic persistence/encryption/transport claims. Returned candidates on these requests measure unsupported retrieval exposure, not answer hallucination.

Counts: 28 directly supported requests, 2 partial requests, 6 requests not established in the catalog; each batch still has its two unsupported requests. Exact IDs and row-specific reasoning are in the reviewed data.

## Span decisions, ambiguities and prospective parent adjudication

The frozen six roles and Python Unicode offsets apply. Every span is an exact source substring, sorted, nonoverlapping and occurrence-specific. No API inferred from purpose, no Boolean inferred from “enabled”, no model key inferred from “amount” in prose. All four hypothetical API occurrences in R35 remain present. Quoted registration names retain quotes; the numeric key and complete array key in R34 are model_key spans. R31's modelChange is a setting value in that occurrence. R32's model is an explicitly listed FieldType accessor; other ordinary model nouns are untyped.

Six rows initially had genuine boundary uncertainty before any predictions: R02-q0/q1 (method calls), R14-q0/q1 (method plus object argument), R20-q0 (method plus placeholder argument), and R10-q0 (generic class type). The primary contract says whole API paths but does not explicitly settle every call/generic boundary. The parent supplied these prospective operational conventions before inference:

1. API spans stop at the maximal dotted/bracketed method name, excluding call parentheses and argument payload.
2. `{amount: 0}` is one opaque value. Its internal amount and 0 are not separately labeled.
3. Placeholder `field` arguments are generic field nouns, not inferred values or API references.
4. `FormlyFieldConfig` is the API name; application type argument `MyProps` and its later standalone occurrence are untyped. Explicit `props` remains an API.
5. `Observable` (RxJS), `localStorage` and `sessionStorage` (platform) are outside the Formly/Angular-only API role here. They are not being presented as hypothetical Formly API spellings in these questions.

Primary proposed gold now applies those decisions: 78 mentions across 45 rows, no remaining unresolved row under this operational convention. `alternatives` retains the original boundary candidates as audit evidence, **not alternative passing gold**. For R20 the initial method-plus-value candidate is explicitly rejected by the placeholder convention. Independent preflight must verify these choices before freeze. The earlier bare-model-expression adjudication remains unchanged; no new expression-root convention was invented here.

Additional judgment: generic “custom type”, “that type” and “registered type” are category nouns, not literal configuration-property references. `key` in the same-key scenario is a configuration property following the earlier P10 convention. Bare `input` in R18 is the explicitly supplied inheritance registration target: narrow CONTRACT covers named field-type registrations, though the shorter pilot label description emphasizes custom registrations. This precedence interpretation is reported for preflight. `mat-form-field` is the explicit Angular Material element API. Whole bracketed expression targets are single API spans with no nested values.

## Fresh foundation semantic grading

Grading uses qualification_v3/CONTRACT.md as frozen, including its allowance for different decomposition and harmless grounded context. A pass means the saved question plan preserves requested information and applicable source conditions; it says nothing about whether the requested library claim is true. Requests were not rewritten or rerun. All ledger excerpts occur verbatim in both the request and every bound question. All saved question rows match the envelopes. Versions preserve precision (global v prefix removed only as required); Material applies only where supplied; unspecified scope stays null.

| Request | Grade | Semantic assessment |
|---|---|---|
| R01 | pass | Version, default 7 and pre-existing 0 remain paired; all three conditions bind. |
| R02 | pass | Capture and reset consumption are separate questions; reset question names both APIs and stands alone. No supplied extra condition is lost. |
| R03 | pass | Hidden field and false setting remain together in question and ledger. |
| R04 | pass | Same-key shared-control scenario is preserved; neutral can/why formulation retains explanation ask. |
| R05 | pass | Material and inheritance-by-itself restriction preserved and bound. |
| R06 | pass | Registration and use separated, custom name copied twice, key preserved on use; prospective registration prerequisite is grounded. Custom registration name alone needs no redundant ledger entry. |
| R07 | pass | Full path spellings, version and disabled ancestor retained; explicit comparison remains one question. |
| R08 | pass | Modern/legacy argument comparison kept together; API targets do not require redundant ledger. |
| R09 | pass | Subscription and disposal separated with returned Observable/hook scenario bound to both. |
| R10 | pass | Generic props-versus-model-key meaning comparison intact; no version inferred from API name. |
| R11 | pass | Hypothetical spelling retained and existence neutrally questioned with service exclusion bound. |
| R12 | pass | Entire automatic persistence/browser-restart claim remains a question and bound context, not an assertion. |
| R13 | pass | v6.3.12, false default and missing keyed value preserved with exact bindings. |
| R14 | pass | Supplied object preserved in both questions; new-baseline and rebuild outcomes separated without answering either. Catalog support gap is independent of plan quality. |
| R15 | pass | Array hiding and enabled reset setting retained as supplied scenario conditions. |
| R16 | pass | Control registration and default outcomes separated; visibility transition copied and bound to both. |
| R17 | pass | Material ownership and missing-value-accessor substitution separated; adapter shared and missing accessor local. |
| R18 | pass | Requested input inheritance/default-options pattern and custom name intact; no-new-renderer restriction bound. Inheritance is the capability being asked about, not asserted existing setup. |
| R19 | pass | Constant versus conditional comparison and true value intact, with version and scenario binding. |
| R20 | pass | Explicit method comparison remains together, with both supplied field arguments preserved. |
| R21 | pass | Manual versus returned Observable cleanup comparison retained; both hook patterns are bound. |
| R22 | pass | Neutral alias/relationship question preserves v6; global version is 6 without changing precision. |
| R23 | pass | Encryption-before-writing claim remains neutral; supplied timing preserved and bound. |
| R24 | pass | Presupposed option turned into existence plus identification question; remote-validator restriction bound; no retry API invented. |
| R25 | pass | Before-build availability retained and bound; model/default choice intact. |
| R26 | pass | Qualifying model-input change retained and bound; FormlyForm tree effect remains neutral. |
| R27 | pass | Both settings have separate questions with default-registry context shared. |
| R28 | pass | Control and model effects separated; hiding event bound to both. |
| R29 | pass | Complete API and decoration context retained with exact binding. |
| R30 | pass | Registered source and explicit local values both bound; merge question unchanged. |
| R31 | pass | Default and meaning separated; modelChange correctly repeated as target setting value, not asserted default. |
| R32 | pass | Accessor-context request includes all three requested names; generic list is target information, not extra scenario conditions. |
| R33 | pass | Shared-context capability preserved without adding persistence or application inspection. |
| R34 | pass | Number 0 versus whole path array versus string alternatives preserved and bound together. |
| R35 | pass | Both hypothetical spellings preserved, existence made explicit, until-resume limit bound; extra occurrences are grounded clarification, not invented API names. |
| R36 | pass | False setting, hidden values and navigation event bound; automatic storage claim remains a question. |

Result: 36/36 prospective semantic passes, 45 derived questions. No runtime or repeated-qualification claim follows. This is one independent review, subject to the requested fresh preflight. Mechanical checks passed for all question copies, ledger excerpts, offsets, ordering, non-overlap, catalog IDs and required-group subset membership. No extractor/retrieval output informed these labels.

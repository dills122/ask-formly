# Knowledge completion backlog

Current planning authority for the first **Formly 6.3.12 core/Material knowledge set**, reconciled on 2026-10-26 against foundation15: **192 facts / 36 authored documents**. This replaces the old priority list for deciding what to do next; frozen batch ledgers and results remain evidence of their original scope. It does not authorize admission, promotion or runtime changes.

**N1–N7 and the public API/configuration follow-ups are installed as foundation15 / model-free discovery7: 192 facts across 36 documents.** The [promotion checkpoint](../poc/contextual-kb/knowledge-expansion/promotion-v13/RESULTS.md) records canonical reproduction, installed testing and review. Q1 previously qualified the176-fact intermediate set at160/160 positive requests after bounded recovery, plus16/16 controls, in three fixed-plan repeats; initial lookup supported121/160. Those historical scores are not rerun scores for the final192-fact DB. See [Q1](../poc/contextual-kb/knowledge-expansion/q1-v1/CLOSEOUT.md) and the [N2–N7 closeout](../poc/contextual-kb/knowledge-expansion/completion-v1/CLOSEOUT.md). The bounded retained-source milestone is complete; exclusions and separately scoped deferrals remain below.

A later external question-bank diagnostic exposed narrower public API/configuration gaps beyond the N2–N7 requests. The [public API/configuration experiment](../poc/contextual-kb/knowledge-expansion/public-api-v1/RESULTS.md) now has an **isolated 188-fact / 35-document candidate**, adding 12 pinned-source facts. Its fresh positive score is **20/24 (83.33%) after independent-review correction in each of three fixed-plan repeats**, below the frozen 22/24 gate; all eight preservation cases and eight controls pass. It is **not qualified for promotion**. Remaining delivered-evidence gaps concern FieldType accessor relationships, the optional model argument to updateInitialValue, wrapper lookup's suppression-option boundary and unknown named presets. The original21/24 score is retained with a separate grading erratum. This result does not revise historical Q1 or external-bank scores. Independent final review accepted the completed failed experiment with a non-blocking assessment-seal tooling follow-up; promotion remains not ready.

The subsequently installed [four-contract follow-up](../poc/contextual-kb/knowledge-expansion/api-contracts-v1/RESULTS.md) added four facts to the **192-fact / 36-document knowledge set**. Fresh targeted results are **24/24 positives**, 8/8 preservation cases and 8/8 controls in each of three fixed-plan repeats, versus 5/24 baseline positives; final independent review is **Ready**, with no actionable findings or scoring corrections. This covers accessor forwarding/fallback, optional reset-baseline arguments and clone limits, wrapper lookup signature, and absent-preset processing boundaries. It does not rewrite the earlier failed run or qualify whole-library behavior. The reviewed192-fact candidate is now installed; both runtime implementations and models remain unchanged, and evaluation stays sealed.

Both runtime implementations, models and installed DB stay frozen during preparation and comparison. Candidate builds require separate authorization; installation requires explicit promotion. Evaluation remains sealed, including during the final development qualification proposed here.

## How to read dispositions

- **Covered:** a specific installed authored claim supports the listed topic. This does not certify an entire guide, control or application recipe.
- **Remaining:** a library topic belongs in this milestone but needs source verification, duplicate checking and a disposition before admission.
- **Excluded:** provenance, duplicate explanation, application policy or retired tooling; retain it without turning it into a library behavior fact.
- **Deferred:** potentially useful work outside this exact-version milestone, with a stated reopening trigger.

An old ledger's `pending` means “not handled in that batch.” Resolve it through the installed records and later promotions below; do not add pending counts across historical checklists. An old exclusion can also be a batch-local deferral, such as select stream ownership subsequently covered by Material select.

## Installed coverage, reconciled

The installed set now contains36documents. N2–N7 references in the table point to installed detailed packages, not pending tasks. Paths below are relative to [authored/](../poc/contextual-kb/authored/). They are the authoritative installed claim records; embedded source excerpts may support more than the explicit claim, which must be credited during baseline comparisons.

| Installed documents | Covered scope | Detailed coverage and retained limits |
| --- | --- | --- |
| `props-and-registration.json`, `model-scope.json` | Props vocabulary/alias, key shapes, registration, formState, built-field links, keyed/keyless/leaf scope | Exact key parsing, shared-control semantics and attribute limits → N4 |
| `initial-values.json`, `defaults-and-resets.json` | Initial model versus defaults, changed-model rebuild, reset baseline and resetModel | Specialized clone/merge behavior → N4 |
| `custom-component-use.json`, `custom-type-use-example.json`, `custom-types-and-wrappers.json` | Selecting registered types, inheritance/defaults, wrapper insertion/responsibility | Detailed default merging and HTML/Angular templates → N4 |
| `custom-type-recipe-core.json`, `custom-type-recipe-material.json`, `material-wrappers.json` | Control/attributes bindings, public registration type, class versus alias, module configuration, Material bridge and wrapper ownership | Presentation props → N2; arbitrary composite controls deferred |
| `expression-callbacks-and-hooks.json`, `expressions-notifications.json`, `hiding-and-visibility.json` | Callback contracts, hide/disabled paths, stream expressions, checks, formState observation, expression events, managed hook subscriptions, hide/reset/shared-key behavior | Value-event surfaces → N3; outer-field versus rendered-component lifetime → N4 |
| `extensions-presets.json`, `extension-addons-material.json` | Build phases/priorities, preset setup/provider/timing, guarded addons example | Detailed merge semantics → N4; recursive preset composition deferred |
| `validation-contracts.json`, `validation-group-example.json` | Validator return contracts, built-ins, error visibility, basic message configuration, async results and group errorPath example | Full message precedence/Observable messages and routed-error cleanup → N5 |
| `array-operations.json`, `array-repeat-example.json` | Item templates/children, coordinated add/remove, falsy initial values, scoped insertion fixture and registered repeat example | Arbitrary reorder/identity and browser recipes deferred; schema-generated arrays → N7 |
| `material-select-options.json`, `material-select-all.json` | Mapping/groups, identity, stream ownership, expression-array updates, multiple/change, select-all predicates/cache | Accessible names/panelClass/readonly boundary → N2 |
| `material-datepicker.json` | Registration, adapter responsibility, nested constraints, calendar options and callback signatures | Adapter-specific parsing/timezones and universal compatibility deferred |
| `material-choice-controls.json` | Checkbox registration/labels/indeterminate, multicheckbox map/array/disabled behavior, toggle forwarding | Remaining secondary registration details → N2; affirmative-consent semantics → N5 |
| `material-input-textarea.json` | Input kind/bindings, textarea dimensions/autosize/bindings | Module aliases now covered by N1; parser semantics → N3; browser sizing/hydration deferred |
| `material-radio-native.json`, `material-common-registration.json` | Radio mapping/focus/registration; native-select values/groups/bindings/registration; aggregate imports and input aliases (N1 installed) | Browser/keyboard/readonly guarantees remain excluded; N2 presentation/slider and N3 parser semantics remain separate |
| `json-schema-conversion.json` | Conversion result, renderer registration separation, customization/map, local and remote references | Scalar mappings/format → N6; structural mappings/composition → N7 |

Additional installed authored documents: `material-presentation.json`, `value-propagation-events.json`, `core-configuration-lifetime.json`, `validation-reactive-details.json`, `json-schema-scalars.json`, `json-schema-structures.json`, `public-field-api.json`, `public-api-configuration.json`, and `public-api-contracts.json`. The [promotion checklist](../poc/contextual-kb/knowledge-expansion/promotion-v13/CHECKLIST.md) maps all nine additions to their source decisions and qualification records.

The original three-guide milestone accounted for all 18 sections with explicit exclusions; it was not whole-library completion. See its [installed ledger](../poc/contextual-kb/knowledge-expansion/source-ledger/CHECKLIST.md). Later installed dispositions are in [validation](../poc/contextual-kb/knowledge-expansion/validation-v1/CHECKLIST.md), [arrays](../poc/contextual-kb/knowledge-expansion/promotion-v6/CHECKLIST.md), [select](../poc/contextual-kb/knowledge-expansion/promotion-v7/CHECKLIST.md), [JSON Schema](../poc/contextual-kb/knowledge-expansion/promotion-v8/CHECKLIST.md), [datepicker](../poc/contextual-kb/knowledge-expansion/promotion-v9/CHECKLIST.md), [choice controls](../poc/contextual-kb/knowledge-expansion/promotion-v10/CHECKLIST.md), and [input/textarea](../poc/contextual-kb/knowledge-expansion/promotion-v11/CHECKLIST.md).

## Completed admission packages

N1's historical checkpoint installed124/27; [foundation15](../poc/contextual-kb/knowledge-expansion/promotion-v13/RESULTS.md) now includes N2–N7 and public API/configuration follow-ups at192/36. The [detailed package ledgers](../poc/contextual-kb/knowledge-expansion/completion-v1/CHECKLIST.md) retain their original candidate status as history; installation is recorded in the new promotion checkpoint. Source IDs below remain evidence references, not blanket permission to admit unrelated claims.

| ID / package | Included review targets | Evidence leads | Required distinction in tests |
| --- | --- | --- | --- |
| N1 — Radio, native-select and common registrations | Radio option mapping, per-option disabled/focus bindings; native-select ngValue/groups; umbrella membership and missing input aliases/radio/native-select registrations | `material.md`, `material-controls.md`; K13, K32, K50, K55 plus matching module sources | Mapping versus identity; native-select versus mat-select; readonly binding versus demonstrated interaction; common versus secondary imports |
| N2 — Slider and Material presentation | Slider module/legacy/MDC split; wrapper appearance/floatLabel/hints/prefix/suffix types; required-marker presentation; select accessible names/panelClass/no readonly binding; remaining secondary registration such as toggle | Same guides; K17, K33, K53, K54, K14, K52, K62; I3855 as attributed guidance only | CDK selection boundary is not a compatibility matrix; text versus template inputs; host class versus overlay; marker versus validation |
| N3 — Value propagation and events | updateOn/debounce shape and scope; parser pipeline and write-back; parser/debounce interaction; control.valueChanges versus fieldChanges/valueChanges, modelChange and props.change | `api-contracts.md` value section; K01, K11, K37, K41; `async-and-state.md` Formly-specific boundaries | Model propagation versus validation/HTTP timing; normalization versus preservation of raw text; callback versus model update |
| N4 — Core configuration and lifetime | Exact key/path and shared-control rules; rebuild/validator ownership; reverse merging, arrays and null/empty/false/zero; cloning/immutable limits; attributes versus component inputs; field versus type hook lifetime; HTML template versus Angular template; string-expression execution boundary; public setup/export caveats | `api-contracts.md`, `api-map.md`; K39–K43, K37, K46, K59, K60, K03/K04/K11; deduplicate existing setup/preset facts | Source-backed public behavior versus internal extension APIs; defaults versus merge; hide/show versus hook destruction; HTML versus compiled Angular |
| N5 — Remaining validation, messages and reactive labels | Message selection/precedence, Observable message handling and errorPath special case; named versus anonymous routed-error cleanup; group async placement; direct translation-stream pattern; required versus affirmative consent | `validation.md`, `async-and-state.md`, `patterns.md`; K08, K38, E03/E04/E13, I3601/I4022 | Invalidity versus presentation; error-name cleanup; application-defined validators versus built-ins; async contract versus networking policy |
| N6 — JSON Schema scalar/value mappings | Numeric/integer parsers and constraints, empty/null handling, strings/patterns, enum/const identity, format limitations | `json-schema.md` mapping bullets; K20/K56/K57/K61, I3698 | Conversion versus browser behavior; substring versus anchored pattern; reference identity versus structural equality; format annotation versus validator/datepicker |
| N7 — JSON Schema structures/composition | Object required/dependencies, arrays/defaults/tuple/removable/uniqueItems, allOf merge strategy, oneOf/anyOf/multischema branch handling, residual local-reference annotation/escape/cycle limits | `json-schema.md`; K22/K56/K57 and matching tests | Generated behavior versus full logical/conformance equivalence; source-supported limits versus untested assumptions |

Each package closes only when every included target is mapped to an installed fact, admitted candidate claim, justified exclusion or explicit deferral. A deferral of an included target is visible scope reduction and requires an owner decision; it cannot silently count as successful coverage. Unsupported generalizations should be excluded, while a useful, source-supported limitation can itself be admitted.

Source observations that point to old probe/evaluation artifacts are leads only. This consolidation did not open those artifacts. No sealed artifact may be used to author or tune a package; if source inspection cannot support the proposed claim, use a separately authorized fresh development probe or defer it.

## Retained-source disposition register

This register accounts for **every original retained file in `skill/ask-formly/references/`**, including supporting JSON and retired product instructions. It is a file/topic reconciliation, not a completed line-by-line claim audit of every remaining guide. N1–N7 must create their detailed source mappings before builds. “Covered” below applies only to the installed scope listed above.

| Retained files | Disposition and destination |
| --- | --- |
| `config-and-model.md`, `customization.md`, `expressions-and-lifecycle.md` | Covered within original three-guide ledger; recommendations explicitly excluded there remain excluded. Detailed semantics delegated to other guides route to N3/N4. Select ownership deferral is now covered by select facts. |
| `arrays.md` | Covered for its admitted array mechanisms/example; application adaptation advice and unexecuted upstream-test implications excluded. Reorder/browser compatibility deferred. |
| `validation.md` | Partial: ordinary contracts covered; cleanup and residual async distinctions N5. Application HTTP policies excluded. |
| `material.md`, `material-controls.md` | Partial: installed controls/select/bridge covered; N1 radio/native-select/common registrations now covered; remaining slider/presentation/secondary registration N2. Broad browser/adapter/SSR claims deferred. |
| `json-schema.md` | Partial: conversion/customization/references covered; mappings N6/N7. General JSON serialization/application integration advice excluded. Full conformance deferred. |
| `api-contracts.md`, `api-map.md` | Partial: existing public setup/scope/reset/extension/expression facts covered; detailed residual behavior N3/N4. The map is an index, not one new fact per symbol. |
| `async-and-state.md` | Partial: direct expression streams, formState and select ownership covered; Formly value timing N3 and messages/group async/translation N5. HTTP cancellation, stale-result policy and business payload choices excluded. |
| `patterns.md` | Duplicate/design-guidance overlay: P02/P03/P06/P08–P16/P19/P20 largely refer to covered mechanisms; residual mechanisms route to N3–N7. P01/P05/P07/P22/P23 are application design choices, not unconditional library rules. P04/P17/P18/P21/P24 route to boundaries below. No wholesale pattern ingestion. |
| `examples.md` | Supporting provenance, not a separate batch. Existing custom type/repeat/validation/select examples already support facts; E13 is a lead for N5. Demo application registration, CSS, HTTP policy and all example recipes are not automatically admitted. |
| `performance.md` | Existing expression/state/extension mechanisms already represented; residual lifetime/event/clone detail N3/N4. Performance recipes, timing numbers and universal field-count limits excluded; new benchmarks deferred. |
| `debugging.md` | Investigation workflow excluded from factual library DB. Keep diagnostic guidance in provenance/history; specific supported mechanisms belong to their topic package. |
| `sources.md`, `evidence.json` | Source index/catalog support, not new claims or a target fact count. Duplicate excerpts do not justify duplicate facts. Preserve paths/bytes. |
| `bug-ledger.md`, `discussions.md`, `discussions.json`, `fix-patches.json` | Historical reports and patch provenance; consult when a package needs a precise behavior boundary. Wholesale issue ingestion and new release coverage deferred. Reporter claims/workarounds are not library guarantees. |
| `coverage.md`, `version-policy.md` | Historical research scope/confidence and version policy, not proof of installed coverage. Preserve as provenance; current exact-version scope is controlled by runtime manifests and this backlog. |
| `runtime-evidence.md`, `runtime-evidence.json`, `angular21-qualification.md`, `angular21-evidence.json` | Historical execution evidence retained, excluded from automatic admission. B06/B13 remain known failures. No general Angular21/browser/adapter qualification claim. No artifact reopening needed for this consolidation. |
| `evaluation-lessons.md`, `evaluation-evidence.json` | Retained evaluation history, excluded as development inputs here; contents not opened for this consolidation. Keep sealed evaluation separately untouched. Reproduce necessary behavior through fresh development evidence if authorized. |
| `e2e-analysis.md` | Proposed consuming-application test workflow; excluded from library facts and from evidence of tests actually run. |
| `form-records.md`, `local-mcp.md`, `project-indexing.md`, `semantic-search.md`, `workspaces.md` | Retired application-inspection/indexing product instructions; excluded. No importing, wiring in, or reviving their implementation. |

### Pattern crosswalk and exclusions

The pattern document must not become a second copy of the same knowledge. Use these dispositions to review its 24 entries:

| Patterns | Disposition |
| --- | --- |
| P02 layout/scope; P03 hidden data; P06 direct streams; P08 option identity; P09 validator returns; P10 group validation; P11 messages; P12 custom controls; P13 wrapper ownership; P14 extension guard; P15 arrays; P16 reset; P19 subscriptions; P20 schema conversion | Existing mechanisms covered; qualifications in this backlog still apply. P10/P11 residual details → N5; P19 lifetime detail → N4; P20 deeper mappings → N6/N7. The accompanying application prescriptions are excluded as universal rules. |
| P04 readonly/disabled/display | Renderer boundaries → N1/N2; generic Angular payload aggregation and application submission policy excluded. |
| P17 normalization | Formly parser behavior → N3; application request pipeline recipes excluded. |
| P18 consent | Required-versus-true validation boundary → N5; application consent policy excluded. |
| P21 JSON expressions | Execution/sanitizer/template boundaries → N4; application security architecture excluded. |
| P24 patch history | Supporting provenance only; no promise of fixed behavior in other releases. |
| P01 factories; P05 cheap expressions; P07 dependent-select retention; P22 state stores; P23 tabs/steps | Contextual design guidance excluded as standalone guarantees. Review any concrete library claim against covered topics; do not create new networking, performance or application-layout batches. |

## Deferred beyond this milestone

| Deferred area | Reopen when |
| --- | --- |
| Additional Formly releases and other UI adapters | A separately scoped version/adapter expansion is authorized, using matching evidence and applicability. |
| Cross-browser accessibility, visual behavior, SSR/hydration, date adapters/locales/timezones, Angular/Material compatibility matrix | A named environment/behavior is selected for executable qualification. Source bindings alone do not settle it. |
| Arbitrary composite widgets, recursive presets, array identity/reordering, complete JSON Schema conformance | A concrete library gap justifies bounded source and runtime investigation. No claim of completeness until then. |
| Real HTTP races/errors, application schemas/components, payload/state-store policy, consuming-project investigation | These remain caller/application responsibilities; adding them would require an explicit product-scope decision. |
| Production packaging, fresh-machine provisioning, hosting and licensing | Separate project readiness work; knowledge completion does not imply distribution readiness. |

## Qualification and finish line

Use the existing admission process, not a new pipeline: reviewed pinned sources → frozen draft/cases/rubric → isolated scripted candidate build → baseline/candidate comparison → independent review → separately authorized guarded promotion. TDD applies to any necessary new mechanism; do not modify runtime behavior to rescue a knowledge-only comparison. Credit existing full-source evidence in the baseline, including the input evidence recovered in the last batch.

Completion checklist:

- [x] Reconcile the 27 installed documents and classify all retained reference files without opening sealed evaluation.
- [x] N1 — Source mappings, candidate qualification and admission review complete; historical installed124/27, now a subset of192/36. Promotion verification is recorded in its checkpoint. All N1 targets have explicit dispositions.
- [x] N2 — Slider/Material presentation qualified in candidate; installed in foundation15.
- [x] N3 — Value propagation/events qualified in candidate; installed in foundation15.
- [x] N4 — Core configuration/lifetime qualified in candidate; installed in foundation15.
- [x] N5 — Residual validation/messages/reactive labels qualified in candidate; installed in foundation15.
- [x] N6 — JSON Schema scalar/value mappings qualified in candidate; installed in foundation15.
- [x] N7 — JSON Schema structures/composition qualified in candidate; installed in foundation15.
- [x] Q1 — Fixed mixed-topic development qualification, independent review and final coverage reconciliation completed. The Q1 candidate176/33 is retained as historical evidence; its facts are included in the installed192/36 set. Source-informed fixed-plan repeats are not unseen autonomous-agent accuracy; model-backed mode was maintenance/preflight-checked only.

For Q1, freeze fresh realistic requests, grading criteria, scope/gap controls, retrieval/recovery budgets and versions before execution; no tuning during the run. Aim for at least **90% usable, supported answers per repeat**, with a predeclared acceptable lower band of **89.25%** reflecting the owner's 0.75 percentage-point tolerance. Run three repeats; report exact counts, percentages and failures for each. Small sets cannot demonstrate sub-percentage consistency—state their resolution and uncertainty instead of rounding a failure into a pass. Choose the sample size and integer threshold before running. No critical unsupported claims or failed scope controls are acceptable. A failed gate stays failed until a separately frozen follow-up; it does not reopen all completed packages automatically.

Qualify the default model-free caller flow and report the retained model-backed mode separately; never pool their scores. Retain both modes' regression/manifest checks. If an end-to-end model-backed comparison is not executed, explicitly limit its qualification claim. Distinguish independent caller generations from deterministic packet replays. Diagnose missing knowledge, retrieval loss and caller omissions separately. This milestone uses fresh development cases; the sealed evaluation remains sealed.

Every included source claim must ultimately be linked to an installed fact or a reasoned exclusion/defer decision, with no anonymous pending sections. Reconcile later promotions into this document as they occur, without editing frozen historical ledgers. This is completion of the **bounded retained-source milestone**, not certification of the entire library or a mandatory fact-count target.

# Validation plan and current evidence

Status: **two-arm development comparison complete: 8/8 passes in both arms, tied 10/10 means, no critical failures or demonstrated advantage**. Both authored forms passed strict AOT and 3/3 Chromium scenarios each; two fresh skill variants passed review. See [full protocol, artifacts and limits](evaluation/2026-10-15-pilot/README.md). The original three-arm/full-release design below remains unrun.

Update 2026-10-15: owner-authorized construction, Angular 21 zoneless/AOT/browser qualification and the adapted two-arm comparison are complete. The broader browser result remains 12/14 with two known select failures. Three supplemental JIT and three RxJS virtual-time checks add focused evidence; they do not replace that result.

## Hypothesis and comparisons

Hypothesis: a small, source-backed v6 skill improves correctness or reduces the work needed to obtain a correct, auditable Formly answer.

Compare on the same model/settings, task inputs, tool access, and dependency versions:

- A: normal coding agent, no specialist skill.
- B: normal agent with a short instruction pointing to official v6 docs and the target versions.
- C: `ask-formly` prototype with curated notes and recipes.

Each trial begins in a fresh context. Baselines retain access to the same official sources; the skill must not win merely because its competitors are denied evidence. Record prompt, model/settings, package lock, retrieved evidence, answer, tool usage, test output, review score, and elapsed time. An evaluator should judge observable behavior and source support rather than matching preferred wording.

## Cheapest pilot

Use cases 01, 03, 04, 05, 07, 09, 11, and 15 below. Prepare expected behavior and fixture assertions before running the arms. Budget: 24 task runs plus at most one targeted correction/retest cycle. Stop broad development if C neither reduces errors nor meaningfully reduces lookup effort compared with B.

Pilot gate: at least seven of eight cases pass, no critical failure, and a useful advantage over B. A marginal difference on eight cases is directional evidence, not statistical proof.

## Qualification cases

Develop using cases 01–16. Keep 17–24 as held-out prompts/fixtures unavailable during authoring; these descriptions are category requirements, not the eventual exact test inputs or answer keys. Use sanitized real tasks where available.

| ID | Scenario | Observable success |
| --- | --- | --- |
| 01 | Explain a nested group with dotted keys | Correct model paths and distinction between grouping and model nesting |
| 02 | Repeatable items and insertion/removal | Correct model/control relationships; behavior checked in fixture |
| 03 | Read legacy `templateOptions` / expression APIs | Recognizes supported deprecated syntax and actual callback arguments |
| 04 | Supplied v7 setup in a v6 task | Detects unsupported APIs and gives appropriate v6 setup |
| 05 | Author a Material form with requirements | Compiles, renders, validates, and produces the intended model |
| 06 | Required/disabled/readonly requirements | Distinguishes states; observed values match requested semantics |
| 07 | Hidden field unexpectedly loses data | Diagnoses configuration/version and meets explicit retention requirement |
| 08 | Default value versus model value and reset | Preserves intended defaults and reset behavior |
| 09 | Validator returns wrong kind of result | Corrects the specific validator contract, with positive/negative checks |
| 10 | Async validation and error messages | Handles resolution/error state appropriately; fixture settles as expected |
| 11 | Unknown custom field type | Finds registration or identifies missing evidence without inventing it |
| 12 | Custom field with strict templates | Correct control typing and successful template compilation |
| 13 | OnPush custom property does not update | Explains and fixes the demonstrated change-detection issue |
| 14 | Dependent options and stale selected value | Correct dependency/clearing behavior and subscription lifecycle |
| 15 | Older v6 patch with a relevant release-note fix | Separates plausible patch issue from reproduced cause; no forced upgrade |
| 16 | Supplied JSON Schema versus Formly configuration | Chooses correct integration; does not emit functions into claimed JSON |
| 17 | Unfamiliar deeply nested factory configuration | Follows scope/registrations and reports missing dynamic context |
| 18 | Material date or custom control integration | Matches target adapter/module/value-accessor requirements |
| 19 | Cross-field validator with changed sibling | Correct invalid/valid transitions after the dependency changes |
| 20 | Newer-major snippet from retrieval | Rejects or qualifies its applicability to v6 |
| 21 | Unsupported version and incomplete snippet | Gives bounded help and asks only for information that changes the answer |
| 22 | Offline feature question | Uses retained knowledge with appropriate source/verification limits |
| 23 | Hidden required field / repeat toggle regression | Fixture confirms intended visibility, validation, and model transitions |
| 24 | Unrelated Angular or other “Formly” product task | Does not misroute or replace the user's actual task |

## Scoring and release criteria

Score each case on correctness (0–4), version/context fidelity (0–2), evidence/calibration (0–2), and usefulness/scope (0–2). A passing case earns at least 8/10 with no critical failure. Critical failures include an unsupported API presented as v6-compatible, fabricated verification/source, destructive model behavior contrary to requirements, or an invented registration presented as existing project fact.

Full gate: at least 22/24 passing cases, at least 7/8 held-out passes, and zero critical failures. Every shipped executable recipe must compile and pass its stated behavior checks on the declared fixture versions. Do not substitute TypeScript compilation for rendering, validation, or model-transition tests.

Compare C with B: target at least a 15-percentage-point improvement in average normalized rubric score, or equal/better quality with at least 25% lower median evidence-lookup effort. “Lookup effort” is recorded retrieval/tool actions to locate relevant evidence; report elapsed time and context usage separately when available. These are product decision thresholds, not claims of statistical significance. If B is already strong, prefer the smaller artifact unless the efficiency benefit is useful in real tasks.

First full comparison budget: 72 runs (24 cases × 3 arms), followed only by targeted reruns of failures or unstable cases. Record repeated-run variability before making broad reliability claims. Later field trial: three owner-relevant tasks across explanation, generation, and debugging; retain the actual outputs and needed corrections.

## Verification performed in this research phase

- Read original candidate skill files and Formly Contract's stated product boundary.
- Retrieved npm peer metadata and resolved the v6.3.12 tag to a source commit.
- Compared selected v6 guide statements with tagged declarations and changelog.
- Behavioral tests, Angular builds, candidate installation, and skill invocation were not performed.
- Checked all eight packet documents for local link targets, source-ID resolution, and unfinished template markers: no errors. Confirmed 23 defined source IDs, 24 uniquely ordered evaluation cases, and consistent brief/index status. The pilot uses only development cases; held-out cases remain outside the pilot. Reviewed recommendation, version pins, scope, and next action for consistency. These are document checks, not evidence that the proposed skill works.

## Knowledge construction verification — 2026-10-15

Acceptance was defined in [task_plan.md](task_plan.md) before construction: cover the selected topics with exact source evidence, distinguish reading from execution, and validate the portable package. Results:

| Check | Observed result |
| --- | --- |
| Skill structure | Official `skill-creator/scripts/quick_validate.py` returned `Skill is valid!` |
| Discovery metadata | YAML parsed; display fields are strings; short description length is within 25–64 characters; prompt contains `$ask-formly` |
| Evidence manifest | 51 unique IDs across 48 files; all full-file SHA-256 hashes match the local pinned source; every excerpt range is within file bounds; URLs use the pinned commit and matching line bounds |
| Readable index | Every manifest ID and URL has a corresponding readable index entry |
| Local links | 27 Markdown files checked, including anchor targets; no missing targets or invalid heading anchors |
| Lookup smoke checks | Ordinary `rg` searches found focused notes for resetOnHide, datepickerOptions, compareWith, errorPath, FieldArrayType, templateOptions, toFieldConfig, and prePopulate |
| Scope and provenance | Source cache is Git-ignored; portable package uses relative links and public immutable evidence; third-party notice retained; no global installation, commit, or publication |

The first validator attempt failed because PyYAML was absent from both available Python environments. Installed PyYAML 6.0.2 into a temporary directory and reran the original validator successfully via `PYTHONPATH`; no project dependencies were added. The source hash/line checks and local-link checks used temporary inline Python, not a new supported tool shipped with the skill.

The eight lookup checks are navigation smoke checks, **not** the eight-case behavioral pilot. No fresh-context agent trials, Angular compilation, upstream test execution, browser rendering, runtime verification of examples, or user field trial occurred. The source-reading concern in the cascaded-select demo remains unconfirmed by execution.

Next: use a pinned fixture to promote three examples to verified recipes, then compare the prototype with the normal-agent and docs-pointer baselines. A passing source audit must not be substituted for that gate.

## Deepening and executed probes — 2026-10-15

This supersedes the current-status implications of the historical construction section above; its earlier results remain an audit trail.

| Check | Observed result |
| --- | --- |
| Source corpus | 83 records across 74 files; hashes, excerpt bounds, immutable URLs, and readable index parity checked |
| Maintainer/bug evidence | 25 issue bodies and 85 comments inspected; retained content hashes match the local cache; four linked fix diffs inspected and hashed |
| Knowledge integration | 24 pattern/anti-pattern entries, 25 bug cases, 13 official example walkthroughs; focused API, Material, async/state, performance, and testing guidance |
| Executed behavior | 17/17 custom JIT TestBed probes passed on Formly 6.3.12 and Angular/Material/CDK 18.2.14 under jsdom; see [fixture](qualification/README.md) |
| Skill structure | Official quick_validate.py returned `Skill is valid!`; entrypoint remains 58 lines |
| Provenance and navigation | Source, discussion, patch, and runtime artifact hashes verified; 507 local Markdown links checked after final handoff updates with no errors |

R11 and R14 characterize limitations: the selected debounce path bypasses a parser, and a false initial array value falls through to the item's default. Passing those probes establishes the observed behavior, not correctness for an application's requirements. The fixture retained missing-Material-theme warnings. Runtime artifacts and hashes are linked from [runtime evidence](skill/ask-formly/references/runtime-evidence.md).

No AOT/strict-template build, real-browser/theme/accessibility qualification, full upstream suite, complete official-demo execution, fresh-context agent evaluation, or consuming-project field trial was performed. These 17 development probes do not satisfy or substitute for the eight-case comparison or held-out release gate above. The locked npm ci reinstall instructions have not been clean-room executed.

Next: qualify browser/AOT behavior and selected executable recipes, then compare normal-agent, docs-pointer, and ask-formly answers. Preserve held-out cases for that evaluation.

## Angular LTS requalification — 2026-10-15

Owner requirement supersedes the Angular 18 target above. Angular's [support schedule](https://angular.dev/reference/releases) identifies Angular 21 as the newest LTS line. Selected Angular 21.2.25 / Material and CDK 21.2.14, retaining Formly 6.3.12 and using Zone.js 0.15.1. Registry metadata is retained with the fixture.

Installed the pinned dependencies with scripts disabled and no force/legacy-peer-deps flags. All 17 existing probes passed again; stderr is empty. Version labels are read from installed packages. Explicit provideZoneChangeDetection() preserves the test's Zone-based integration mode. Angular 21's default zoneless mode is not qualified. Existing JIT/jsdom, browser, AOT, theme, accessibility, and comparative-evaluation limits still apply.

Original Angular 18 artifacts and hashes remain in [historical/angular18](qualification/historical/angular18/). Current [results](qualification/results.json), [lockfile](qualification/package-lock.json), and [portable runtime manifest](skill/ask-formly/references/runtime-evidence.json) now describe Angular 21.

## Zoneless / strict AOT / real-browser execution — 2026-10-15

The [separate fixture](qualification/browser/README.md) uses the same Angular 21.2.25, Material/CDK 21.2.14, Formly 6.3.12 baseline. Results: 17/17 zoneless JIT probes pass; strict optimized AOT build passes; a negative-control number-to-FormControl binding fails TS2322 as expected and original source is restored. No Zone.js or runtime Angular compiler inputs appear in the emitted bundle's stats.

Playwright 1.64.1 / actual headless Chromium 156.0.8078.4 ran 14 cases: **12 pass, 2 fail, zero skipped, zero retries**. B06 (Formly) and B13 (bare Material) retain option-replacement/keyboard-selection failures. B14 verifies Escape/close/reopen recovery. Cases assert model, native DOM, validation rendering, async notifications, repeat values, date minimum/selection, focus, and runtime page/console errors. Screenshot inspected for basic layout. These observations are bounded; no blanket visual/accessibility certification is claimed.

Initial strict-TS errors were in the fixture and corrected with explicit AbstractControl typing and deliberately dynamic UntypedFormGroup. Required-marker/date-dialog locator ambiguities and an early click on an empty select were harness issues; evidence is retained. Installed CDK/Material source and a bare control isolate the remaining issue below the Formly field layer. No private patch was used. The global npm installation was unchanged; a temporary npm 11.6.2 runner recovered from npm 10's resolver crash. The locked clean-room ci reproduction remains unrun.

The source and fixture manifests retain hashes and exact versions. These tests extend compatibility evidence and do not substitute for the independent agent-answer comparison. Remaining browser/adapter/HTTP/SSR scope is in [coverage](skill/ask-formly/references/coverage.md).

Final artifact audit for this milestone: official skill validator returned `Skill is valid!`; 554 local Markdown links/anchors passed; all 84 pinned source hashes/ranges/index links and all qualification artifact/source hashes passed. Exact package pins match lock resolution. Confirmed the negative-control source was restored byte-for-byte and the zoneless probe contains neither a Zone.js import nor manual detectChanges calls. There are 20 focused topic/coverage references; browser failures remain visible in the retained report.

## Executed two-arm pilot — 2026-10-15

The user requested comparison against an agent without the skill. Adapted the earlier plan to eight cases × two arms, with fresh contexts, the same pinned upstream access/settings/tool budget, a frozen skill/rubric, independent partially masked review, and unchanged C04 artifacts compiled/browser-tested. Both arms scored 80/80 with eight passes and no critical failures. Self-reported median source actions were equal; their counting limitations prevent an efficiency claim. The pass threshold was met, but comparative advantage was not established.

Added explicit disabled-path migration semantics, parser view/model write-back and immediate request invalidation guidance after source/behavior checks. Two fresh skill-only variants passed root review; this is a single development correction/retest cycle, not held-out efficacy. Full details, model-ID limitation, raw artifacts and evaluation shortcomings: [pilot report](evaluation/2026-10-15-pilot/README.md). The three-arm/24-case gate, repeated-run variability and consuming-project trials remain unrun.

## Independent accuracy, blind challenge and lean-context audit — 2026-10-15

Two content auditors and a source-only challenge designer produced four accuracy findings and six new tasks. Twelve fresh answers received independent partially masked grading: both arms 5/6,57.5/60, no demonstrated advantage. Both H05 outputs imported an unavailable public TypeOption; original AOT failures remain. Four unchanged H03/H04 cases passed AOT/Chromium; both narrowly repaired H05 cases passed. Six focused probes passed. Three fresh skill-only variants passed review, with the new custom control also compiled/browser-tested unchanged.

Integrated five actionable corrections and removed repetition. Entrypoint 818→515 words; all Markdown 17,806→17,369. Optional evidence brings whole package bytes up 0.4%; no token/efficiency claim. Independent revision review found one citation issue, corrected. Fixture errors and original failures are retained separately; broad Chromium qualification remains 12/14. [Full protocol, evidence, limitations and validation](evaluation/2026-10-15-audit/README.md).

Final audit checks: official skill validator passes; 84 source hashes/bounds, frozen snapshot/designer/answer manifests and 45 execution artifacts verified; local Markdown links/anchors and JSON parse checks pass. See the retained final-validation.json in the audit packet.

## E2E-builder use-case qualification — proposed 2026-10-15

The owner clarified that fast understanding of unfamiliar existing forms should reduce Playwright generation/debugging effort. Prior knowledge-question results do not measure this. The [new workflow and benchmark](e2e-use-case.md) defines eight source-to-test scenarios, equal builder conditions, first-run meaningful success, repair/time metrics and controlled false-positive checks. It is unrun; gates must be frozen before trial. This pass adds a conditional skill reference and planning updates only. Static package/source/link checks are recorded separately; no application tests or performance benefit are claimed.

## Project inventory and connection-map qualification — 2026-10-15

Owner-authorized implementation is complete for the declared static-discovery scope. Twenty-five behavioral tests pass with zero skips, including separate 500-form discovery/graph fixtures, freshness/notes/output protections, alias/re-export and UI/config/registration relationships. Independent review found five defects; all were reproduced, fixed, and regression-tested. Additional tests cover shorthand references, alias-aware discovery kinds, and reviewing fully read large forms despite preview truncation. A retained synthetic exercise demonstrates stale-source detection and note preservation/invalidation on refresh. [Tests, boundaries, example and reproduction](qualification/project-index/README.md).

This does not establish complete extraction of arbitrary applications or workplace E2E effectiveness. The static fixture is not an Angular runtime; prior AOT/browser evidence remains unchanged, including its two retained select failures. Compiler API tested: TypeScript 5.9.3. Source inventory completeness, extraction gaps, reviewed conclusions and runtime observations remain distinct.

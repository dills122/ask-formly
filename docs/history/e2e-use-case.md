# Formly understanding inside an E2E test builder

Updated 2026-10-15. Status: user-confirmed use case; proposed workflow and evaluation, not a completed workplace integration.

## Decision and evidence

The owner describes a large workplace admin system with 100+ forms, approximately 200–500 Formly-related files, years of accumulated code and multiple implementation styles. These are user-reported estimates; this repository has no inspected workplace source or browser session. The primary goal is fast, accurate Formly interpretation that helps an eventual E2E builder generate Playwright tests with little debugging or adjustment.

The decision is now: does ask-formly reduce time and repair work needed to generate meaningful passing E2E tests across unfamiliar existing forms? General feature explanation remains useful, but previous question scores and authored-control checks do not answer this question. Prior results and original failures remain unchanged.

The initial reframing stopped at a workflow and benchmark. The owner subsequently authorized a static inventory and connection map; see [indexing implementation](project-index-plan.md) and [qualification](qualification/project-index/README.md). Do not invent company conventions. Angular 21.2.25 / Material 21.2.14 / Formly 6.3.12 remains the laboratory baseline. Workplace versions, auth, data setup, test conventions and available browser access are unknown.

## Recommended division of responsibility

| Part | Responsibility |
| --- | --- |
| ask-formly | Interpret config/model/control relationships, factories, registrations, hooks, validators, async options, custom renderers and submit transformations for the requested scenario |
| Project-owned context | Source-linked shared registrations, helper meanings, conventions, versions and known interactions; validated against current files and scenario |
| E2E builder | Navigate/authenticate, prepare data through existing fixtures, inspect actual UI, choose locators, generate/run Playwright, diagnose traces and assess the acceptance requirement |

These are responsibilities, not three new services or mandatory separate agents. The existing builder may load the skill directly. Keep generic knowledge reusable; company-specific facts stay in that company's workspace. The authorized index adds generated discovery and source-reviewed notes. Its effect on total preparation time and E2E repair effort still requires measurement.

## Per-task workflow

1. Receive route or feature, requested behavior and acceptance criteria. Resolve actual package versions and existing Playwright conventions once per project/revision where practical.
2. Find the owning screen and follow the scenario's dependency paths: composed factories, local feature registration overriding root defaults, inherited types, wrappers, custom components, relevant services and submit mapper. Support old templateOptions/expressionProperties alongside newer conventions without migrating them.
3. Produce a compact field/behavior table plus ordered actions. Record model paths separately from DOM identity; initial/conditional state; valid data; visible error triggers; option label/value mapping; dependency readiness; hidden-value retention and submitted payload. Attach source locations and uncertainty only where useful.
4. Check locator candidates, widget interaction and readiness against the running UI. Accessible labels may be generated/localized; duplicate labels need row/section scope; Material overlays can require a different scope. Treat custom composites as unknown until their implementation or behavior is inspected.
5. Generate the requested test using project fixtures. Verify the acceptance outcome, not merely a toast, a completed click or an implementation-derived payload. If requirements and implementation conflict, report the conflict rather than encoding the bug as expected behavior.
6. Run the test and record what required repair. Classify errors as source discovery, Formly semantics, custom widget/locator, timing/data, environment or incorrect expectation. Promote only a generalizable lesson to the shared skill.

A useful handoff is small: relevant fields, action ordering, readiness conditions, assertions and unresolved checks. Avoid a full report for every form or a repository-wide scan for each task. Reuse a shared helper summary only when its source and relevant dependencies remain current; permission/tenant/mode/locale can change the answer even without a code change.

## Example of the intended question

Illustrative, not a claim about the workplace application:

> Add a Playwright test for editing a supplier. Changing country should reset an incompatible region. Add a contact row, verify required email feedback, save, and verify persisted values. Start from the supplier route and existing test fixtures. Follow whatever factories, wrappers or custom controls are necessary; preserve existing form code. Identify unresolved behavior before generating speculative assertions.

The useful answer discovers the actual dependency and value contracts and produces a working test. It is not enough to explain resetOnHide or know a select API in isolation. Direct writes to Angular/Formly controls would bypass the UI behavior under test; existing API/data fixtures can still establish prerequisites where appropriate.

## Next benchmark: source to meaningful running test

Proposed, unrun. Begin with eight previously unseen scenarios sampled from real forms or faithful de-identified reproductions. Include several implementation styles and both ordinary flows and failure-prone dependencies. Selection dimensions: inline versus composed factories; old/new expression syntax; shared custom widgets; cascading remote choices; repeats/duplicate labels; conditional sections; create/edit/reset defaults; payload transformations. Don't deliberately select only rare library traps.

Both arms receive the same route/requirement, repository snapshot, project facts, browser access, fixtures, time/tool budget and model settings. Neither receives the relevant file list, precomputed Formly explanation or expected diagnosis. Keep the broader E2E builder identical; the treatment is ask-formly. A separate reviewer supplies acceptance outcomes before seeing generated tests and checks whether assertions are meaningful. A requirement absent from source must be supplied or marked unknown, not guessed.

Run a cold task and a separate reuse task that shares project helpers but changes the form. Record context preparation separately and include it in end-to-end cost. If comparing a project overlay, give both arms the same factual overlay or clearly label it as a separate combined-workflow experiment. Do not attribute overlay improvements to generic skill knowledge alone.

Metrics:

- First-run meaningful pass: test passes on its first execution, covers the requested outcome, and has no skipped/weakened assertion or bypass of the behavior.
- Time to accepted test and number of edit/run repair cycles; separate environment/setup failures.
- Correctness of field/dependency interpretation and unsupported assumptions; missed requirements and false-positive tests.
- Measured input/output tokens, files/bytes read and repeated source discovery when instrumentation exists; don't infer these from word counts or inconsistent self-reports.
- Failure detection on a controlled seeded regression for selected scenarios, reviewed against the requirement; repeated execution on stable data to expose flaky timing.

Proposed initial gate, to freeze before trial: no critical false-positive test or invented custom behavior; at least 6/8 first-run meaningful passes; all eight scenarios covered correctly within two repair cycles each. Report every outcome if the gate fails. Call the skill useful for this workflow only if correctness holds and paired results show fewer repair cycles or lower total time without a coverage tradeoff. Eight cases are a directional pilot, not statistical proof or production reliability certification. Do not pool these scores with prior knowledge quizzes.

## Sources and remaining unknowns

Formly mechanisms are grounded in the existing pinned corpus; the new portable [E2E reference](skill/ask-formly/references/e2e-analysis.md) links canonical topics. Workflow boundaries, index design and evaluation gates are engineering proposals.

Official Playwright sources accessed 2026-10-15; publication dates unspecified:

- [Best practices](https://playwright.dev/docs/best-practices): user-visible behavior, isolated tests and retrying assertions.
- [Locators](https://playwright.dev/docs/locators): user-facing locator contracts, scoping and strictness.
- [Auto-waiting](https://playwright.dev/docs/actionability): actionability checks and assertion retries; application-specific readiness still needs an observable condition.

Before executing this benchmark, need an authorized project or representative reproduction, actual resolved versions, existing fixtures/test conventions, defined acceptance scenarios and a usable test environment. No company files, framework assumptions or test results have been invented. No benchmark or integration was executed in this reframing pass.

# Construction findings

Updated: 2026-10-15. Earlier discovery is retained in [research.md](research.md) and [sources.md](sources.md). The construction evidence is in the portable [pinned index](skill/ask-formly/references/sources.md).

## First construction findings

- The 6.3.12 source snapshot supplies a useful bounded corpus: declarations, implementation, guides, selected tests, and official examples. Retained 51 evidence records and ten example walkthroughs; source-read status is explicit.
- Material's umbrella module does not register every widget. Datepicker and slider setup must be checked separately. Datepicker constraints are nested under `props.datepickerOptions`. See [Material](skill/ask-formly/references/material.md).
- Legacy expression callbacks and newer field-based callbacks differ. Boolean validation expressions also differ from Angular null/error-object validators. These are high-value sources of mistakes for the skill to catch. See [expressions](skill/ask-formly/references/expressions-and-lifecycle.md) and [validation](skill/ask-formly/references/validation.md).
- Reading tests helps interpret intent, but even test titles can be misleading: the retained expression spec must be interpreted by its actual assertions. No upstream test has been run here.
- The official cascaded-select source has a potential child-retention comparison problem. The file-accessor example omits disabled-state handling. These are adaptation cautions, not reproduced application defects. See [E02](skill/ask-formly/references/examples.md#e02) and [E10](skill/ask-formly/references/examples.md#e10).
- JSON Schema conversion does not itself register all structural renderers; the official demo supplies custom setup. Remote references are rejected in the inspected resolver. Coverage is intentionally narrower than a conformance claim.
- External designer/builder projects inspected use different Formly majors. They remain design leads, not v6 source-of-truth material. See [companions](companions.md).

## Retrieval observations

Downloaded 889 regular files from the pinned public archive into the Git-ignored `local/ask-formly/upstream/` cache. Archive SHA-256 is retained in the skill's evidence manifest; the distributable contains original notes and provenance, not the whole checkout.

An optional fast source graph (`ask-formly-upstream-v6-3-12`) contained 2,269 nodes and 5,448 edges. Coverage checks and file reads were required: docs, demo examples, and test specs were outside graph coverage. Structural source navigation used the graph; excluded material used direct reads. This supports retaining plain search and file access as fallbacks, not claiming graph completeness.

## Current recommendation

Keep the knowledge base local and portable. The Angular 21 fixture and first two-arm answer comparison are complete. The comparison tied; unseen consuming-project tasks and the retained select boundary are the next meaningful checks. Additional companion skills should follow repeated needs, particularly project-context collection or knowledge maintenance.

## Open questions

- Which exact Angular and Material versions does the consuming application use?
- Which local custom types/wrappers should be represented in a future project overlay?
- Does a focused local evidence lookup cover typical questions without external retrieval infrastructure?

## Deepening findings — 2026-10-15

- API coverage now includes key/control ownership, merge and clone semantics, parser/debounce/event ordering, template boundaries, registration, and message precedence. See [API contracts](skill/ask-formly/references/api-contracts.md).
- The [pattern catalog](skill/ask-formly/references/patterns.md) contains 24 actionable designs and anti-patterns, tied to source, issue, or runtime evidence.
- The [bug ledger](skill/ask-formly/references/bug-ledger.md) covers 25 cases and distinguishes reported version, maintainer recommendation, confirmed patch, unresolved cause, and applicability to this baseline. Inspected 85 comments and four fix diffs; issue closure alone is not fix evidence.
- Seventeen custom probes passed on the declared stack. Two expose limitations: parser bypass under the selected modelOptions debounce path, and falsy initial array data falling through to the default. See [runtime evidence](skill/ask-formly/references/runtime-evidence.md).
- Material control contracts and array/map multicheckbox behavior, sibling-dependent group validation, and automatic existing formState property observation have stronger coverage. Date adapters, browser focus/layout, network races, and AOT remain unqualified.
- The corpus now retains 83 records across 74 files and 13 official example walkthroughs. That measures inspected evidence, not the probability of answering an arbitrary question correctly. Comparative answer quality remains unknown.

## Angular LTS correction — 2026-10-15

Angular 18 is unsupported and no longer the qualification baseline. The owner requires LTS or newer; Angular 21 is the selected minimum, based on the current official support schedule. All 17 probes passed again on Angular 21.2.25 / Material/CDK 21.2.14 with Formly 6.3.12. Angular 21 defaults to zoneless, but this run explicitly uses Zone.js and does not establish zoneless compatibility. See [version policy](skill/ask-formly/references/version-policy.md) and [current runtime evidence](skill/ask-formly/references/runtime-evidence.md).

## Zoneless/AOT/browser findings — 2026-10-15

- Formly 6.3.12 already detects a no-op zone and bypasses onStable waiting for modelChange. Added pinned K64 for relevant marking/version helpers; B02 verifies actual output delivery on Angular 21.
- All 17 adapted probes pass without Zone.js/manual fixture.detectChanges. External expressions, state, and async validators also render correctly in selected Chromium cases without forced detection.
- Strict AOT passes with typed custom Material control bindings and v6 NgModule registration in a standalone host. An empty typed FormGroup was inappropriate for dynamically named fixture controls; explicit dynamic typing corrected the fixture while preserving compiler checks.
- Async select rendering is not sufficient evidence of working keyboard/model behavior. Replacing the sole active option while open leaves a failure in Formly and bare Material; close/reopen recovery is verified. Exact scope and source interpretation: [Q01](skill/ask-formly/references/angular21-qualification.md#q01-replacing-the-active-select-option-while-the-panel-is-open).
- Native en-US date min/calendar selection, selected repeat operations, reset, and validation interactions pass; other adapters, cross-browser, HTTP races, SSR and full accessibility remain unknown. Browser result is 12/14, not a clean compatibility pass.

## Agent comparison findings — 2026-10-15

- Both source-equipped arms passed all eight development cases, averaging 10/10. No critical failure or useful measured comparative advantage; ceiling scores and uninstrumented lookup counts limit inference.
- Both generated Material forms passed strict AOT and three Chromium scenarios without correction. The skill arm additionally supplied prior exact-stack compatibility evidence in C03; the normal arm appropriately limited itself to source evidence.
- Both arms identified disabled-path migration differences and raw/normalized request boundaries. Retained these explicitly in the skill; three focused zoneless checks and three RxJS virtual-time checks passed. Two fresh variants retrieved/applied the new guidance correctly.
- Independent review also called for effective modelOptions when tracing custom value conversions and kept uncompiled C03/C08 snippets distinct from executed C04 artifacts. No new helper skill/retrieval service justified. See [pilot report](evaluation/2026-10-15-pilot/README.md).

## 2026-10-15 — Additional independent/blind audit

Five grounded refinements: routed-error cleanup requires name/key alignment; JSON Schema string patterns inherit Angular anchoring; structured enum/const uses identity; typed scalar composition can be omitted; internal TypeOption is absent from the public v6 package barrel. Six targeted observations passed. Both blind arms 5/6, with the same real AOT failure. Corrected skill transferred to three fresh variants; the fresh custom Material type passed AOT/Chromium. No comparative advantage established. Detailed evidence and bloat accounting: [audit](evaluation/2026-10-15-audit/README.md).

## 2026-10-15 — Operational use case clarified

The owner needs an E2E builder to understand a mature admin application's Formly code quickly, across 100+ forms and roughly 200–500 related files. The relevant outcome is reliable generated Playwright tests with fewer adjustments. Inference: shared factory/registration discovery and scenario-specific interpretation are likely more useful next investments than broadening library trivia. This hypothesis needs the [source-to-test evaluation](e2e-use-case.md); it is not yet measured.

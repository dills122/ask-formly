# Executed behavior and limits

Current follow-up: [Angular 21 zoneless/AOT/browser qualification](angular21-qualification.md) adds 17 passing zoneless probes, a passing strict AOT build/negative control, and 12/14 passing Chromium cases with a retained select limitation. The table below describes the earlier Zone-based run.

Executed 2026-10-15 against npm Formly core/material **6.3.12**, Angular **21.2.25**, Material/CDK **21.2.14**, RxJS **7.8.1**, zone.js **0.15.1**, Node **22.23.3**, jsdom **25.0.1**. Seventeen custom probes passed again on the new LTS baseline. Angular 18.2.14 results are retained as historical evidence in the development fixture. The development fixture lives in `ideas/ask-formly/qualification/` in the source repository; it is not required to read/use this portable skill. [Results and artifact hashes](runtime-evidence.json) are retained here.

This is **JIT Angular TestBed under jsdom with explicit `provideZoneChangeDetection()`**. This run alone did not exercise a real browser, AOT compilation, theme/layout, accessibility, the upstream suite, or agent comparison. The linked follow-up adds scoped AOT/browser evidence. The current run emitted no stderr. No Material theme is loaded. Angular 21 defaults to zoneless, but these probes explicitly use Zone.js to qualify the existing v6 integration; this run alone does not qualify zoneless behavior; see the follow-up above. Do not use these results to claim production UI readiness or compatibility with every Angular/Material release.

| ID | Checked behavior | Result |
| --- | --- | --- |
| R01 | Input event on nested Material field | Nested model updated |
| R02 | Hide/show with resetOnHide false | Value retained, control removed/restored |
| R03 | Default hide-reset policy | Edit cleared; default reapplied on show |
| R04 | Disabled field in enabled group | Absent from form.value; retained in raw value/model |
| R05 | Angular and Boolean validator contracts | Both reject bad and accept valid input |
| R06 | Direct Observable expression | Disabled state follows emitted Booleans |
| R07 | updateInitialValue then edit/reset | Saved baseline restored |
| R08 | Local versus global required message | Rendered Material error uses local message |
| R09 | Simple custom Material FieldType input | Programmatic value updates render |
| R10 | Immediate uppercase parser | Model becomes ABC |
| R11 | Same parser with 5 ms modelOptions debounce | **Limitation observed:** model remains abc |
| R12 | Explicit requiredTrue on checkbox | False invalid; true valid |
| R13 | JSON Schema object conversion / remote ref | Object config produced; remote ref rejected |
| R14 | Array add(0, false) with item default true | **Limitation observed:** model gets true |
| R15 | Material multicheckbox click | Selected-value array or Boolean map as configured |
| R16 | Existing formState property mutation | Disabled updates without manual expression check |
| R17 | Group rule depending on two fields | Reevaluates when either sibling changes |

R11 and R14 pass because the checks confirm the observed limitation, not because that behavior is desirable. For normalization plus debounced search, separate request throttling from the model parser and test the chosen design. For falsy initial array values, do not promise the add argument preserves them; create a focused application fix with a regression check. The skill has not patched or published an upstream fix.

No probe establishes blanket nullability behavior, date adapter correctness, async-request race handling, or all multi-schema combinations. Use the [coverage map](coverage.md) to bound answers and add a targeted reproduction for uncovered behavior.

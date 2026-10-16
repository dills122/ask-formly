# Angular 21: zoneless, AOT, and browser qualification

Executed 2026-10-15 with Formly core/material **6.3.12**, Angular/compiler **21.2.25**, Material/CDK **21.2.14**, TypeScript **5.9.3**, CLI/build **21.2.27**, Node **22.23.3**, Playwright **1.64.1**, and Chromium **156.0.8078.4** on macOS arm64. [Machine-readable results, source references, and hashes](angular21-evidence.json).

## What passed, and what did not

| Layer | Observed result | Meaning |
| --- | --- | --- |
| Zoneless JIT/jsdom | 17/17 probes pass; Zone.js absent; no manual fixture.detectChanges | Original selected behaviors survive the change-detection-mode change |
| Production AOT | Build passes with strict TypeScript, strictTemplates, and skipLibCheck false | Host, custom Material input, repeat renderer, registrations and their templates compile |
| AOT negative control | Number bound to formControl rejected with TS2322; original source restored | The input-binding type-checking gate is active |
| Emitted browser bundle | Build stats contain no Zone.js or runtime Angular compiler inputs | Browser tests execute the linked AOT app without either runtime |
| Headless Chromium | **12 pass, 2 fail**, zero skips/retries | Broad selected behavior works; open-select option replacement has a retained failure |
| Select recovery | B14 passes after Escape/close then reopen | A public interaction recovers keyboard selection in this reproduction |

The two failing browser tests are not marked expected or hidden by retries. Do not call this an unconditional compatibility pass. The earlier Zone-based 17-probe run remains separate [runtime evidence](runtime-evidence.md).

Passing browser cases cover native input/model/modelChange, required error after blur and submit, external disabled expressions, external formState hiding/retention, Promise validation settling and error display, custom Material control updates, array add/edit/remove, reset, and native date input/minimum/calendar selection. They also check actual rendered layout and runtime errors. One inspected screenshot and those assertions are not accessibility or visual-regression certification.

## Q01: replacing the active select option while the panel is open

**Exact reproduction:** begin with a single `Initial` option, open the select, asynchronously replace the list with a single `Blue` option, press ArrowDown then Enter. With the Formly select (B06), Blue renders and the combobox remains focused, but its active-descendant ID still refers to the removed option; the trigger/model do not acquire Blue. The bare Material control (B13), without a Formly field/type/options pipe, also fails to update its FormControl value in the same interaction. The bare case shares the application but is not managed by Formly.

This is evidence of a **Material/CDK integration boundary**, not evidence that Formly alone causes the defect. Installed CDK 21.2.14 source leaves the active item unchanged when it is absent from the replacement list; Material's Enter handling selects the active item. Those paths support the observed mechanism; they are not a maintainer-confirmed upstream fix. Exact source URLs, ranges and hashes are in [the evidence manifest](angular21-evidence.json).

**Verified recovery:** close with Escape, reopen the panel, then Enter selects Blue and updates the Formly model (B14). For an application that replaces options while open, consider closing before replacement/reopening after readiness via supported Material APIs, and test its focus/UX requirements. Only the recorded close/reopen interaction was executed here; no application wrapper implementation or upstream patch was shipped. Do not mutate private key-manager fields, add arbitrary sleeps, or recommend a Formly-major upgrade as a demonstrated fix.

The initial empty-options test also clicked before any options had arrived, so the panel never opened. That was a test-readiness error, not proof that options failed to render. Wait for a defined loading/readiness condition when testing initially empty selects. This limitation has **not** been established as zoneless-specific: no Zone-based control comparison or other Material patch was run.

## V6 already has relevant zoneless paths

Do not assume every v6 form waits forever on NgZone.onStable. The pinned host detects a no-op zone and takes an immediate emission path before modelChange; otherwise it waits for zone stability. Field marking calls ChangeDetectorRef.markForCheck, and the version predicate enables the newer form-event path on Angular 21. These are inspected implementation details, not APIs to import into applications. [K11](sources.md#k11), [K64](sources.md#k64). Browser B02 confirms actual modelChange delivery on this stack.

For new application-specific async logic, follow Angular's [zoneless notification guidance](https://angular.dev/guide/zoneless), accessed 2026-10-15. Our external timer/Observable cases passed without application or test calls to tick/detectChanges. That does not prove arbitrary plain-property mutations render. Test the actual DOM after the external completion, without a later click masking a missed notification.

## Strict compilation lessons

- A standalone Angular host can import the v6 NgModules and register `FormlyModule.forRoot(...)` through `importProvidersFrom`. This does not make newer Formly provider APIs available in v6.
- The custom input uses `MaterialFieldType<FieldTypeConfig>` and binds its real FormControl. Its declaration uses `standalone: false` in the custom-types NgModule. Keep typed control contracts rather than hiding binding errors with `$any` or disabling strictTemplates.
- An empty `new FormGroup({})` infers an empty control shape; addressing a runtime-added key produced a `never` value error in our fixture. The deliberately dynamic Formly host uses `UntypedFormGroup`. For known application schemas, an explicitly typed control map can be preferable; do not globally discard typed forms.
- Type custom validator callback arguments explicitly when the v6 configuration surface does not contextually type them. The fixture's implicit-any callback correctly failed strict TypeScript compilation.
- Datepicker qualification uses `FormlyMatDatepickerModule`, `provideNativeDateAdapter`, locale `en-US`, and nested `props.datepickerOptions`. Native dates/min/calendar selection passed; other adapters, time zones, locale parsing and date ranges remain separate tests.

## Boundaries and how to extend

The development fixture is `ideas/ask-formly/qualification/browser/`; it stays outside the portable skill and includes lockfile, source, test scripts, logs and raw results. Use its recorded failed cases as regressions when changing Material/CDK, and rerun on the consuming application. Keep the strict/AOT and browser evidence distinct from JIT results.

Unqualified: Firefox/WebKit, SSR/hydration, full accessibility, exhaustive layout/performance, real HTTP cancellation/races, all date adapters, all schemas/control types, and custom application components. The full upstream suite remains unrun. Separate answer-quality evaluations are summarized in [coverage](coverage.md).

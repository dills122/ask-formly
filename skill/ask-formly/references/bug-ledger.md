# Maintainer conversations and real-bug lessons

Read on 2026-10-15. Each case distinguishes reports, maintainer advice, released fixes, and remaining uncertainty. Issue closure alone does not prove a fix. The [conversation index](discussions.md) records dates, URLs, and comment sources; [discussions.json](discussions.json) retains provenance hashes. Unless named in [runtime evidence](runtime-evidence.md), these reproductions were **not run here**.

## I3984

**Large formState and performance regression.** Report followed a v5 → v6 / Angular 17 upgrade. Maintainer first asked for a reproduction and modelChange expression mode, then identified moving shared formState observation to the host as the direction; confirmed release in **6.3.8**. The reviewed patch does that move, while the later 6.3.11 patch corrects observer initialization. Do not ship the reporter's removal of observers as baseline advice. Measure with the actual state size. [Conversation](discussions.md#i3984), [K29](sources.md#k29), [K11](sources.md#k11)

## I3791

**Slow insertion into large nested arrays.** Reported on **6.1.8**; maintainer confirmed **6.2.1** release. Current source installs async validation only when validators exist and uses optimized build/validity paths. Reporter timings are case-specific. Check exact version and separate build cost from DOM rendering before redesigning the form. [Conversation](discussions.md#i3791), [K43](sources.md#k43), [K29](sources.md#k29)

## I3799

**Repeated expression evaluation.** Reported on **6.2.1**, fixed/optimized in **6.2.2** according to maintainer and changelog. Maintainer also suggested direct Observable expressions and virtual scroll for appropriate cases. Do not promise one callback invocation per edit or treat expressions as one-shot hooks. Test pure computation and rendering costs separately. [Conversation](discussions.md#i3799), [K07](sources.md#k07), [K29](sources.md#k29)

## I4018

**formState changes not reflected until input changes.** Body prose mentions 6.3.0 while its environment lists **6.3.10**; retain that discrepancy. Maintainer confirms **6.3.11**. Reviewed fix initializes the formState observer when host subscriptions are established rather than during later model emissions. R16 verifies an existing property changing on 6.3.12/Angular 21.2.25. [Conversation](discussions.md#i4018), [K11](sources.md#k11)

## I4027

**Submit validation with Angular 19.0.1 / Formly 6.3.11.** Maintainer confirms **6.3.12**. Patch corrects an Angular version predicate that mishandled a newer major with minor zero. Do not diagnose every absent submit error as an application validator issue. The current probes do not exercise this submit-specific fix. [Conversation](discussions.md#i4027), [K29](sources.md#k29)

## I4002

**Nested hidden array items lose defaults.** Reporter later states **6.3.7**; maintainer confirms **6.3.10**, followed by reporter confirmation. Includes boolean defaults and hide/reset interactions. The earlier suggestion about oneOf is not the whole diagnosis. Reproduce adding a nested item while branch visibility changes; do not “fix” all cases by disabling reset globally. [Conversation](discussions.md#i4002), [K12](sources.md#k12), [K29](sources.md#k29)

## I3957

**Inserting at a custom index with oneOf loses defaults.** Reported on **6.3.5**, maintainer confirms **6.3.6**. Appending successfully does not establish arbitrary-index insertion correctness. Test first/middle/last insertion and retained row-specific state. This fix is separate from the falsy-initialModel limitation reproduced in R14. [Conversation](discussions.md#i3957), [K12](sources.md#k12), [K29](sources.md#k29)

## I3901

**Cleared optional JSON Schema number remains invalid.** Maintainer confirms **6.3.4**; reviewed patch moves parser execution earlier in the value stream and adds input-transition assertions. Do not replace the entire schema converter before inspecting parser/empty-value behavior. The debounce bypass observed in R11 remains a separate baseline limitation. [Conversation](discussions.md#i3901), [K41](sources.md#k41), [K56](sources.md#k56)

## I3738

**Parent disabled transition conflicts with a child's disabled rule.** Report includes a delayed true → false parent transition but no exact version in the body. Returned comments are empty; closure supplies no verified fix boundary. Source contains parent-expression and control disabled propagation. Test both schedules and the actual group hierarchy; do not assert the reporter's expected precedence as a universal contract. [Conversation](discussions.md#i3738), [K07](sources.md#k07), [K42](sources.md#k42)

## I3541

**Function returning an Observable expression.** V6 upgrade discussion; a community reply suggests a field factory accepting streams. Later closure references future signal forms, which does not add support to v6.3.12. Source recognizes direct Observable values, not flattening callback results. Use a direct stream/factory. [Conversation](discussions.md#i3541), [K07](sources.md#k07)

## I3808

**Cascaded requests and hidden fields.** Reporter sees first-change failure when hidden but not when disabled. Maintainer suggests `fieldChanges` for expression changes. No released fix is established. Inspect lazy rendering/subscriber ownership and the event being observed, not only the HTTP call. Test hidden initial state and repeated transitions. [Conversation](discussions.md#i3808), [K41](sources.md#k41)

## I3131

**Options change while selected value is no longer available.** Historical Bootstrap discussion, exact version unspecified; not a Material v6 bug reproduction. Maintainer assigns policy to the application: clear/check the value, validate membership, or intentionally retain object data. The same policy distinction is useful with the inspected v6 Material select, which does not establish universal membership validation. [Conversation](discussions.md#i3131), [K14](sources.md#k14)

## I3820

**Closure over external state stops updating as expected.** V6 migration report includes differing demo/application versions. Maintainer points to default modelChange checking and prefers an Observable dependency. This is a scheduling/migration issue, not proof that arrow functions are unsupported. Avoid globally increasing check frequency without assessing cost. [Conversation](discussions.md#i3820), [K36](sources.md#k36)

## I3601

**Observable validation-message typing.** Maintainer and reporter distinguish working runtime behavior from a narrow declaration. Type clarification released in **6.1.2**. Preserve that distinction: a typing issue is not evidence of missing runtime capability. The 6.3.12 message component handles Observable results. [Conversation](discussions.md#i3601), [K38](sources.md#k38), [K01](sources.md#k01)

## I3558

**Material 15.1 checkbox/toggle styling.** Reported with Formly **6.1**. Users provide MDC CSS workarounds; maintainer links a custom-base-class answer for a separate form-field-control error. No single released styling fix is established by this thread. Avoid extrapolating a user's claim of unsupported Material versions. Check theme, base class, and wrapper contracts separately. [Conversation](discussions.md#i3558), [I3512](#i3512)

## I3855

**Asterisk without current required validation.** This is a custom presentation requirement. Maintainer recommends a custom wrapper/type. The proposed `showAsterisk` is not an established v6 prop. Keep future-required decoration separate from current validation. [Conversation](discussions.md#i3855), [K17](sources.md#k17)

## I3721

**Standalone host rejects ModuleWithProviders in component imports.** Report: Angular **16.0.4**, Formly **6.1.7**. Community suggests environment-level `importProvidersFrom`; the pinned official FAQ points to that answer. Maintainer closes as duplicate of the broader feature request. A community helper named provideFormlyConfig is not proof of that v6 export. Check injector scope and actual module imports. [Conversation](discussions.md#i3721), [K46](sources.md#k46)

## I3622

**Custom UI library expects default validation messages.** Maintainer requests a minimal reproduction; no resolved cause or fix appears in inspected comments. Keep as a diagnostic lesson, not a confirmed library bug: inspect message registration, wrapper display, and actual error keys. Source message lookup/precedence is the reliable contract. [Conversation](discussions.md#i3622), [K38](sources.md#k38)

## I4022

**Async validator reads another field and sees stale/insufficient updates.** Report: Angular **17.1.3**, Formly **6.1.1**. Maintainer recommends group validation and using asyncValidators. Follow-up workarounds are the reporter's solution, not a universal recommended pattern. Model dependency scope and pending/sync-invalid behavior before choosing a group or explicit revalidation. [Conversation](discussions.md#i4022), [E04](examples.md#e04)

## I3550

**No initial statusChanges notification.** Initial report lists **6.0.4**, later comments narrow a history into v5; no verified release fix here. Community suggests seeding a status stream; maintainer says further investigation is needed. Read the current status after construction and treat future notifications separately. Do not recommend forcing change detection from every wrapper as a general fix. [Conversation](discussions.md#i3550), [K42](sources.md#k42)

## I3698

**JSON Schema nullable values normalize inconsistently.** Reported on **6.1.6** with detailed expected/actual types; no maintainer resolution in returned comments. Source string and numeric parsers have different empty/null rules. Do not promise null preservation across types. Test required × nullable × clear-input behavior and serialize according to the application's contract. [Conversation](discussions.md#i3698), [K56](sources.md#k56), [K61](sources.md#k61)

## I3572

**Custom control model binding and composite local fields.** Original reporter discovers the reactive formControl binding; a later commenter reports a composite-control issue. Maintainer links **6.2.1** release, and changelog describes local-field detection inside wrappers. Separate the basic integration mistake from the subsequent library fix. props.change alone is not a model-binding implementation. [Conversation](discussions.md#i3572), [K29](sources.md#k29), [K41](sources.md#k41)

## I3824

**Angular 17 textarea hydration mismatch.** Maintainer confirms **6.3.0**. The current template has no inter-tag textarea whitespace. Check the specific error and patch before disabling hydration everywhere. This does not establish universal SSR support. [Conversation](discussions.md#i3824), [K51](sources.md#k51), [K29](sources.md#k29)

## I3937

**JSON Schema number/integer within array errors.** Report says introduced in **6.3.3**; maintainer confirms **6.3.4**, with reporter confirmation. Treat as a narrow observed version regression, not an unsupported numeric-field category. Test typing, clearing, and submission in the same array shape. [Conversation](discussions.md#i3937), [K56](sources.md#k56), [K29](sources.md#k29)

## I3512

**Custom Material file input lacks MatFormFieldControl.** Maintainer points to importing FieldType from `@ngx-formly/material`, with FieldTypeConfig from core. That addresses the bridge, not the full file value accessor, disabled/reset, or upload lifecycle. The official file-accessor fragment remains incomplete for production use. [Conversation](discussions.md#i3512), [K16](sources.md#k16), [E10](examples.md#e10)

## Locally reproduced Angular 21 boundary (Q01)

Separate from the 25 upstream issue conversations: B06/B13 reproduce keyboard-selection failure after replacing a sole active option while a select is open, in both Formly 6.3.12/Material 21.2.14 and a bare Material control. B14 verifies close/reopen recovery. No maintainer-confirmed fix or zoneless-only attribution is claimed. See [the reproduction and source analysis](angular21-qualification.md#q01-replacing-the-active-select-option-while-the-panel-is-open).

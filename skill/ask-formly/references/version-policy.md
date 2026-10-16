# Version policy

Baseline: **6.3.12**, upstream commit `5f099fddea6426b46a453866adf0fede5be0bcd7`, retrieved 2026-10-15. Source evidence is indexed in [sources.md](sources.md). This is a reference snapshot, not an instruction to update applications.

## Establish the target

For application work, inspect resolved dependencies relevant to the question; check core/adapters, Angular, Material/CDK, RxJS and TypeScript for compatibility/build work. A package.json range is not the installed version. In a monorepo, use the consuming project's resolution context. Ask for missing context only when it changes the answer.

The registry metadata for [core 6.3.12](https://registry.npmjs.org/@ngx-formly/core/6.3.12) declares Angular Forms `>=13.2.0` and RxJS `^6.5.3 || ^7.0.0`; [Material 6.3.12](https://registry.npmjs.org/@ngx-formly/material/6.3.12) peers on core exactly `6.3.12` and Material `>=13.0.0`. These are package constraints, not a claim that every later framework release works. Metadata accessed 2026-10-15.

## Answer at the right specificity

- No workspace: assume the baseline, label it, and answer.
- Earlier v6: use these notes as a starting point; check patch-sensitive behavior against the installed tag/source. Do not infer the first supported version from a late-v6 implementation.
- v5 or v7+: disclose the boundary and retrieve that version's evidence. In particular, do not introduce newer `provideFormlyCore` setup into v6. The pinned v6 exports and module implementation establish its setup surface [K02](sources.md#k02), [K03](sources.md#k03).
- Supported deprecated APIs are not necessarily bugs. v6 retains `templateOptions`, `expressionProperties`, and `hideExpression`; their shapes and callback contracts matter [K01](sources.md#k01).

The presence of Angular standalone host components does not establish the availability of Formly's newer standalone APIs.

## Patch-sensitive areas

The late-v6 changelog records array/default/hiding work in 6.3.10, formState observation in 6.3.11, and Angular 19 submit-validation work in 6.3.12 [K29](sources.md#k29). A similar symptom is a lead, not proof that upgrading fixes a specific application.

Use precise labels: **documented**, **source-checked**, **upstream test read**, and **runtime-verified in named environment**. Seventeen custom probes are runtime-verified on the exact environment in [runtime evidence](runtime-evidence.md); this does not qualify every example or configuration. Prefer pinned source and tests over unversioned snippets; explain material conflicts rather than silently combining incompatible evidence.

## Angular LTS baseline — verified 2026-10-15

The selected qualification policy is **Angular 21 LTS or newer**, with **Material/CDK 21** for this fixture; it does not authorize upgrading consuming applications. Angular's [support schedule](https://angular.dev/reference/releases) lists 21 as the newest LTS line and 22 as active; 20 is also LTS until 2026-11-28, but is not our selected baseline. Angular 18 is unsupported and its earlier probe run is historical evidence only. Recheck this schedule when refreshing dependencies; an Angular major number alone does not establish continuing support.

Exact tested pins: Angular **21.2.25**, Material/CDK **21.2.14**, Formly core/material **6.3.12**, Node **22.23.3**, RxJS **7.8.1**, Zone.js **0.15.1**. Patch numbers for Angular and Material differ by release train; Material and CDK match each other. Public registry metadata was checked for [Angular](https://registry.npmjs.org/@angular/core/21.2.25) and [Material](https://registry.npmjs.org/@angular/material/21.2.14). Angular's [compatibility table](https://angular.dev/reference/versions) accepts this Node/RxJS stack; TypeScript must be >=5.9 <6.0 when adding compilation. The original Zone-based JIT fixture does not compile TypeScript; the separate [AOT fixture](angular21-qualification.md) does.

Angular 21 [defaults to zoneless](https://angular.dev/guide/zoneless). The original fixture uses `provideZoneChangeDetection()`. A separate zoneless fixture now passes 17 JIT probes and strict AOT; its Chromium suite passes 12/14 cases with two retained select failures and a verified recovery. Inspect the consuming app's mode and read [qualification boundaries](angular21-qualification.md). Do not infer broader compatibility from either fixture or mask missed notifications with manual change detection.

Keep the Formly v6 knowledge/API boundary. A supported Angular version and broad Formly peer ranges do not establish vendor support or full runtime compatibility for their combination. The executed probes and browser cases establish only their stated observations. Do not silently migrate Formly majors or upgrade an existing application to match the fixture.

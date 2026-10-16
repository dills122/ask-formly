# Sources and evidence

All sources accessed **2026-10-15**. Dates below are publication/update dates when identifiable; unknown means the page did not establish one. Search-engine crawl dates are not publication dates. Candidate source inspection establishes advertised scope, not verified runtime behavior.

| ID | Primary source | Published / updated | Evidence and limitations |
| --- | --- | --- | --- |
| S1 | ngx-formly: [homepage](https://formly.dev/) and [upstream repository](https://github.com/ngx-formly/ngx-formly) | Unknown; mutable | Identifies the Angular library and source. The site and current repository showed different newest-major matrices; neither is used as an exact v6 compatibility guarantee. |
| S2 | ngx-formly: [v6 getting started](https://v6.formly.dev/docs/guide/getting-started/) | Unknown | Versioned documentation and NgModule-based setup. Unpinned installation snippets must not be copied blindly into a v6 project. |
| S3 | ngx-formly: [v5-to-v6 migration](https://v6.formly.dev/docs/guide/migration/) | Unknown | v6 behavior changes: rendering, defaults, expressions, hiding, and strict templates. Major-level guidance; exact patch still matters. |
| S4 | ngx-formly: [v6 properties/options](https://v6.formly.dev/docs/guide/properties-options/) | Unknown | Configuration concepts and deprecated aliases; some simplified type descriptions need checking against declarations. |
| S5 | ngx-formly: [v6 expressions](https://v6.formly.dev/docs/guide/expression-properties/) | Unknown | Dynamic properties, visibility, field changes. Observed prose/code mismatch concerning disabled versus hidden. |
| S6 | ngx-formly: [v6 validation](https://v6.formly.dev/docs/guide/validation/) | Unknown | Multiple validator registration/return contracts. Contains inconsistent boolean-validator prose; examples require verification. |
| S7 | ngx-formly: [v6 custom types](https://v6.formly.dev/docs/guide/custom-formly-field/) | Unknown | Type extension and registration workflow. Not a complete Material custom-control integration reference. |
| S8 | ngx-formly: [v6 Material UI](https://v6.formly.dev/docs/ui/material/) | Unknown | Route verified; fetched HTML mostly exposed navigation/shell. Detailed Material behavior not established by this page read. |
| S9 | npm: [core registry metadata](https://registry.npmjs.org/@ngx-formly/core), [core 6.3.12 metadata](https://registry.npmjs.org/@ngx-formly/core/6.3.12) | 6.3.12 published 2024-12-08T17:48:54.726Z | Enumerated stable `6.*` versions and sorted numerically: newest was 6.3.12. Core peer ranges recorded below. Package metadata is not a runtime compatibility test. |
| S10 | npm: [Material 6.3.12 metadata](https://registry.npmjs.org/@ngx-formly/material/6.3.12) | Publication date not separately queried | Exact core peer and minimum Material peer; no claim that every later Material release works. |
| S11 | ngx-formly: [v6.3.12 field declarations](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/models/fieldconfig.ts) | Release 2024-12-08 | Tagged source read for aliases, expression signatures, async validators, and fieldArray. Type declarations are not a substitute for runtime tests. |
| S12 | ngx-formly: [pinned changelog](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/CHANGELOG.md) | Through 2024-12-08 | Patch-specific fixes, including 6.3.10–6.3.12. Release notes establish claimed changes, not exhaustive affected-version ranges. |
| S13 | ngx-formly: [v6-to-v7 migration](https://formly.dev/docs/guide/migration/) | Unknown; mutable route | Addition of standalone Formly APIs and provider alternatives. Used only to identify a boundary; not as the v6 corpus. |
| S14 | Angular: [skills README](https://github.com/angular/skills), [developer skill snapshot](https://github.com/angular/skills/blob/c02b20403133da29f404be5acb7c92aa79da9145/angular-developer/SKILL.md) | Skill file updated 2026-10-13 | General Angular skills, version-first instruction, modern defaults. Not evaluated on Formly questions. |
| S15 | Analog: [repository](https://github.com/analogjs/angular-skills), [angular-forms snapshot](https://github.com/analogjs/angular-skills/blob/18996fd1b2bf663c978065a8d5417393e72ccc6a/skills/angular-forms/SKILL.md) | Skill updated 2026-08-06 | Unmaintained status, redirect to official Angular skills, explicit Formly exclusion. Mirrors may be stale. |
| S16 | OpenEMS: [oe-ui-test snapshot](https://github.com/OpenEMS/openems/blob/c4b92f484b133f2f2f499c172a3fd010a2073885/.github/skills/oe-ui-test/SKILL.md) | File updated 2026-05-15 | Actual application-specific skill with Formly view-testing guidance and local helpers. No general v6/Material expertise claim. |
| S17 | Context7: [ngx-formly repository index](https://context7.com/ngx-formly/ngx-formly), [website index](https://context7.com/websites/formly_dev) | Unknown; relative update labels not retained as dates | Listings exist and show “Latest.” No successful v6-specific retrieval evaluation. Website listing also displayed a fetch error. |
| S18 | dills122: [Formly Contract README snapshot](https://github.com/dills122/formly-contract/blob/9b80dcfd725c56a381489d1ae1c9a60efc4ac6b6/README.md) | README updated 2026-09-03 | Agent-readable Formly 6.x contracts, declared/resolved evidence, prerelease status, unshipped production MCP. Author-reported capabilities, not tested here; not asserted to be an independent third-party project relative to the owner. |
| S19 | ng-forge: [dynamic forms](https://ng-forge.com/dynamic-forms), [Formly migration comparison](https://ng-forge.com/dynamic-forms/material/migrating-from-ngx-formly) | Unknown | Different form engine and own MCP tooling. Vendor's comparative claims were not used to establish Formly semantics. |
| S20 | formly.so: [product homepage](https://formly.so/) | Unknown | Hosted form-builder product; example of a same-name search false positive. |
| S21 | Local [skill-creator instructions](/Users/dsteele/.codex/skills/.system/skill-creator/SKILL.md) | Unknown; installed session version | Entrypoint/resources structure, progressive disclosure, validation, scope preservation. Local machine path is intentionally not portable. |
| S22 | ngx-formly: [pinned MIT license](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/LICENSE) | Copyright 2016; release snapshot 2024-12-08 | Attribution/notice requirements for reused upstream material. Other sources need their own provenance review before copying. |
| S23 | ngx-formly: [v6 JSON Schema](https://v6.formly.dev/docs/guide/json-schema/) | Unknown | Separate JSON Schema integration is available. Detailed mapping behavior deferred to corpus construction. |
| S24 | GrumpTech: [Formly Designer README](https://github.com/GrumpTech/formly-designer/blob/main/README.md), [package manifest](https://github.com/GrumpTech/formly-designer/blob/main/package.json), [repository metadata](https://api.github.com/repos/GrumpTech/formly-designer) | Publication unknown; last push observed 2026-10-09 | Accessed 2026-10-15. Visual-designer/OpenAPI ideas; current manifest is Formly 8 / Angular 21, outside this baseline. README describes dual licensing; no code reused. Mutable branch observations. |
| S25 | nthonymiller: [builder sample README](https://github.com/nthonymiller/formly-builder-sample/blob/main/README.md), [package manifest](https://github.com/nthonymiller/formly-builder-sample/blob/main/package.json), [repository metadata](https://api.github.com/repos/nthonymiller/formly-builder-sample) | Publication unknown; last push observed 2021-03-14 | Accessed 2026-10-15. Typed fluent-builder example; manifest uses Formly 5 / Angular 11, so not v6 API evidence. Mutable branch observations. |

## E2E workflow sources — accessed 2026-10-15

| ID | Primary source | Publication date | Scope |
| --- | --- | --- | --- |
| S26 | [Playwright best practices](https://playwright.dev/docs/best-practices) | Unspecified, living documentation | User-visible behavior, isolation, resilient locators and retrying assertions. |
| S27 | [Playwright locators](https://playwright.dev/docs/locators) | Unspecified, living documentation | Accessible role/label and test-ID contracts, locator scoping/strictness. |
| S28 | [Playwright auto-waiting](https://playwright.dev/docs/actionability) | Unspecified, living documentation | Actionability and assertion retries; does not identify this application's data-readiness contract. |

## Retained metadata observations

Read directly with Python `urllib.request`, using public HTTPS endpoints; no credentials were needed. Network reads initially failed inside the sandbox and succeeded with the approved network-capable execution path. No package installation or source execution occurred.

```json
{
  "accessed": "2026-10-15",
  "newestStableV6Observed": "6.3.12",
  "corePeers": {
    "@angular/forms": ">=13.2.0",
    "rxjs": "^6.5.3 || ^7.0.0"
  },
  "materialPeers": {
    "@ngx-formly/core": "6.3.12",
    "@angular/material": ">=13.0.0"
  },
  "tag": "v6.3.12",
  "tagObject": "2db86679cf7047d6b5728cdb23d56cd0b76456d3",
  "sourceCommit": "5f099fddea6426b46a453866adf0fede5be0bcd7"
}
```

Tag resolution used the public [tag ref endpoint](https://api.github.com/repos/ngx-formly/ngx-formly/git/ref/tags/v6.3.12) and [annotated tag object](https://api.github.com/repos/ngx-formly/ngx-formly/git/tags/2db86679cf7047d6b5728cdb23d56cd0b76456d3). The tag-object SHA and source-commit SHA are different and should not be confused. Candidate file dates/revisions came from GitHub's commits API filtered by file path, not from marketplace timestamps.

## Construction and deepening evidence registers

The S-series above records the original research decision. The constructed skill retains finer-grained, immutable evidence in its [83-record source index](skill/ask-formly/references/sources.md), [25-case discussion register](skill/ask-formly/references/discussions.md), and [runtime evidence](skill/ask-formly/references/runtime-evidence.md). Their JSON companions preserve source revisions, ranges, dates where available, and hashes. Discussion comment dates unavailable from the connector are explicitly null; they were not inferred. Four inspected fix diffs are recorded in [fix-patches.json](skill/ask-formly/references/fix-patches.json). All were accessed during the 2026-10-15 work.

## Angular LTS qualification sources — accessed 2026-10-15

- [Angular release/support schedule](https://angular.dev/reference/releases): current status, 21 newest LTS, 22 active, 18 unsupported. Living documentation; no page publication date supplied.
- [Angular compatibility table](https://angular.dev/reference/versions): Node/RxJS/TypeScript constraints for Angular 21. Living documentation; no page publication date supplied.
- [Angular zoneless guidance](https://angular.dev/guide/zoneless): v21 default and explicit TestBed Zone.js provider. Living documentation; no page publication date supplied.
- Exact registry versions, publication dates, engine/peer requirements, and URLs are retained in [angular-lts-metadata.json](qualification/angular-lts-metadata.json). Registry metadata is compatibility input, not a full vendor-support claim for Formly v6 on Angular 21.

## Zoneless / AOT / browser evidence — accessed 2026-10-15

Official [zoneless guidance](https://angular.dev/guide/zoneless), [AOT compiler guide](https://angular.dev/tools/cli/aot-compiler), [template type-checking guide](https://angular.dev/tools/cli/template-typecheck), and [Playwright assertions](https://playwright.dev/docs/test-assertions) informed fixture design. These are living pages without supplied publication dates.

New pinned K64 covers Formly's field marking/no-op zone/version helpers; existing K11 contains the modelChange path. Actual execution and exact installed Material/CDK source URLs, ranges and hashes are in [angular21-evidence.json](skill/ask-formly/references/angular21-evidence.json). The select finding is local runtime/source evidence, not a newly claimed maintainer acknowledgement or release fix. Bounded web searches for upstream zoneless/select-keyboard reports produced code leads but no retained exact matching fix claim.

## Project indexing implementation evidence — accessed 2026-10-15

- IX01: Microsoft TypeScript, [Using the Compiler API](https://github.com/microsoft/TypeScript/wiki/Using-the-Compiler-API), page edited 2026-08-17. Primary guidance for Program/CompilerHost, AST traversal and checker use; it explicitly describes APIs through TypeScript 6 and warns of a different 7.1 API. The implementation uses an indexed-file host with no emit and accepts majors 5/6; only 5.9.3 is locally tested. No installation instructions from the page were executed.
- IX02: Local [index qualification](qualification/project-index/README.md), synthetic fixtures/tests/exercise, 2026-10-15. This is implementation evidence, not upstream Formly API or workplace effectiveness evidence. Existing pinned v6 references remain the semantic baseline.

# Public-source unresolved-case audit — 2026-10-16

Scope: classify the unresolved groups from the four [pinned public scans](pnpm-nx-public-qualification.md),
fix source-provable relationships useful to Formly v6, and replay those exact checkouts.
No repository dependencies/plugins were installed or application factories executed.
No new Formly-major API support was added. The historical report remains unchanged.

## Classification and decision

| Unresolved group | Evidence and disposition |
| --- | --- |
| Dynamic registration names | GSA's `SdsFormlyTypes` is a string enum imported into `formly.config.ts`. Actual scanner gap: registration names used literal-only parsing while field types already resolved initializers. Fixed for source string constants/enums, including matching wrapper and validator references. Calls, numbers and unknown values remain unresolved. |
| Registration inheritance/wrappers | GSA declares `extends: SdsFormlyTypes.FORMLYGROUP` and shared wrapper arrays containing spreads. Actual navigation gap: declarations were visible but had no registration-to-registration links. Added candidate links for base types and wrappers, retaining scope/inheritance review warnings. Cycles are finite graph edges, not recursive runtime merges. |
| Factory providers | Siemens' `dynamicUiConfig` and ng-matero's dependency-taking `formlyConfigFactory` have readable source. Added direct implementation links, including inline-function locations. Factory results, branches, dependencies and runtime effects remain unknown. This improves navigation; it does not erase the legitimate output gap. |
| External imports / missing registrations | Public dependencies were deliberately not installed. Many missing types are built-in/external or supplied by factories. Keep explicit; installing or executing arbitrary repo code is not a scanner fix. GSA's missed enum registrations were the source-provable subset addressed here. |
| Dynamic field types / generic objects | Sampled GSA demo descriptors, Siemens chart/file objects and Bitwarden domain objects are broad structural candidates, not confirmed Formly fields. Removing them without a reliable provenance model risks hiding valid keyless/composed fields. Counts still need source classification; no claim of precision was added. |
| Template bindings and inherited members | Siemens uses `@let` aliases/signals; GSA includes complex/repeated bindings and inherited Formly members. These need Angular template scoping/type analysis. Keep unresolved in this focused change rather than add unsafe expression matching. |
| Nx / source coverage | Bitwarden lacks a resolved Nx export and has overlapping static declarations. Siemens docs asset symlinks remain excluded; its `IndexError_` warning is the path-policy exception, not a Python list-index crash. GSA's tools tsconfig has no inputs; ng-matero's schematic templates contain template syntax. Preserve these boundaries. |

## Formly v6 grounding

All scanner changes use the existing TypeScript compiler API and v6-compatible source shapes:

- [v6.3.12 ConfigOption/TypeOption](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/models/config.ts): string names, `extends`, `wrappers`, validators and components.
- [v6.3.12 FormlyConfig](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/services/formly.config.ts): `setType` stores declared configuration and `mergeExtendedType` resolves runtime inheritance. The scanner deliberately does not simulate that merge.
- [v6.3.12 core module](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/core.module.ts): `FORMLY_CONFIG` providers include `useFactory`; linking their implementation is valid for v6.

These pinned files were read locally. Public discovery evidence still spans newer
Formly majors and does not expand the Angular 21 / Formly 6.3.12 / Material runtime qualification.

## Replay evidence

All four scans completed with the same source inventory, compiler contexts and
coverage classifications as before. Counts are per-context records, not unique forms.

| Check | Before | After |
| --- | ---: | ---: |
| GSA dynamic registration-name warnings | 148 | 0 |
| GSA registration nodes | 236 | 384 |
| GSA missing-registration warnings | 1,607 | 744 |
| GSA inheritance-review warnings | 13 | 153 |
| GSA total unresolved records | 4,362 | 3,491 |
| GSA wrapper candidate edges | 343 | 1,197 |
| GSA base-type candidate edges | 0 | 7 |
| Siemens factory-implementation edges | 0 | 7 |
| ng-matero factory-implementation edges | 0 | 1 |

The increase in GSA inheritance warnings is expected: recovered registrations now
expose declarations that still need scope/default review. Siemens retains all 9
factory-output warnings; ng-matero retains all 3 (including schematic contexts).
Bitwarden's node/edge counts and unresolved groups are unchanged, with zero Formly
registrations. Siemens remains partial source coverage; Bitwarden remains Nx
`static-candidates`. None is relabelled fully resolved.

Source spot checks assert GSA's recovered `input` registration connects to
`FormlyFieldInputComponent` and all five declared shared wrappers, Siemens' legacy
provider points to `dynamic-ui-config.ts`, and ng-matero's app provider points to
`shared/formly-config.ts`. Factory-output warnings are asserted to remain present.
The source paths and revisions are in the prior pinned report; machine-readable
before/after counts and spot checks are retained locally.

## Regression contract and size

Six [focused tests](../tests/project-index/test_public_gaps.py) failed before the
fixes and pass afterwards. They cover enum/constant names, shared/spread wrapper
lists and base types, inheritance cycles/missing bases, imported factory pointers,
inline versus external factory sources, and dynamic names/lists that must remain
unknown. These are independent minimal v6-shaped fixtures, not copies of public
applications. The test gate also exercises the exact pnpm/Nx cross-library fixture.

Final validation: `npm run check` passed all **53 tests**, zero skips, metadata/link/syntax
validation and the extracted-bundle smoke check. Browser/AOT suites were not rerun
because these changes affect static discovery only.

Only the existing indexing-reference paragraph changed in the portable skill;
the audit and fixtures stay outside the bundle. The implementation adds no package
dependency, template parser or factory evaluator. Raw results live in ignored
`test-output/public-gap-fixes-2026-10-16/`; use `npm run check` for the permanent gate.

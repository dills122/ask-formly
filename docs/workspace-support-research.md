# Angular and Nx workspace support — decision and evidence

Decision date/access date: 2026-10-15. Owner: ask-formly maintainers. Scope authorized by the owner: research existing helpers and implement Angular single-project, Angular multi-project and Nx Angular monorepo support in the Formly scanner. Preserve the Angular 21 / Formly 6 / Material knowledge baseline.

Decision question: how should a portable, static Formly scanner discover projects and resolve their source relationships without inventing workspace semantics or executing application factories?

Research boundary: official Angular/Nx/TypeScript documentation and APIs, two established TypeScript helpers, and the existing Angular lookup implementation. Stop after comparing these options and qualifying the chosen integration against representative generated workspaces; no exhaustive ecosystem survey or workplace compatibility claim. Acceptance criteria: custom project layouts; project/config ownership; different aliases in different apps; shared imports; config inheritance/references; Nx inferred metadata and exclusions; explicit gaps; freshness; portable bundle regression gates.

## Findings and choice

| Option | Evidence and suitability | Decision |
| --- | --- | --- |
| TypeScript compiler API | Defines config inheritance, relative-path origins, include/exclude rules, package resolution and project references. Already required for our AST graph. [S3–S5] | Use `getParsedCommandLineOfConfigFile`, `resolveProjectReferencePath`, `sys.readDirectory`, `createProgram` and `resolveModuleName`. One context per config, with context-qualified nodes/edges. |
| Angular workspace API | `@angular-devkit/core.workspaces.readWorkspace` exposes projects and targets, retaining JSON formatting/comments for editing. [S2] | Use as a qualification oracle. Production only reads the documented `angular.json` data model via TypeScript's JSONC reader; we do not need Angular's writer or schema framework in the shipped skill. |
| Nx CLI / Devkit | Nx resolves inferred plugin configuration, defaults and project declarations. `nx graph --file=...` exports `GraphJson.graph`, containing nodes and dependencies. Public Devkit also exposes `createProjectGraphAsync`. [S6–S9] | Import the installed Nx's exported graph. Do not bundle one Nx version into every consuming repo or reproduce its plugin/merge/package-membership algorithms. |
| `get-tsconfig` | Small parser/path helper, handles extends and file matching without requiring TypeScript. [S10] | Useful for tools without a compiler; redundant here and adds a second config implementation to reconcile. |
| `ts-morph` | Convenient project/source wrappers around compiler facilities. [S11] | No need to migrate the existing read-only compiler graph just for workspace discovery. |
| Existing Angular lookup helper | Local `angular-usage-lookup/skill/angular-usage-lookup/scripts/discover.mjs`, inspected 2026-10-15: workspace-installed `nx show`, recursive target tsConfig discovery, official TS parsing/references, redirected Nx scratch caches. | Reuse the architectural approach; new implementation in this repo, no cross-repo dependency or copied helper file. Separate Nx execution from static Formly scanning. |
| Keep root-only scanning / manual scopes | Observed old implementation applied one root options object to all source files. | Rejected: two apps can resolve the same import differently. Directory names alone cannot establish project membership. |

Documented facts: Angular project-map names need not mirror directories; a root application may have an empty root. Nx configuration can come from plugins, `nx.json` defaults and project/package metadata. Package workspace globs and exclusions affect membership. A scan of `apps/` and `libs/` alone cannot reproduce this. [S1, S6]

Inference/engineering decision: a source-only consumer should ingest Nx's resolved metadata rather than automatically run an unknown workspace's plugins. Nx graph computation invokes plugins and can write caches; importing its JSON does neither. A plain export has no trustworthy source freshness attestation, so the scanner explicitly reports `nx-export-freshness-unverified`. Re-export after workspace/plugin/configuration changes; `check` only establishes that scanned inputs and the supplied export are unchanged. [S7–S9]

## Implemented contract

- `--root` is the actual workspace root. `angular.json`, project/package metadata and exported Nx project roots drive ownership; no `apps/`/`libs/` layout assumption.
- Target options and configuration variants supply `tsConfig` seeds, including arbitrary config filenames. Conventional configs and recursive references add contexts. Base-only configs do not create competing whole-workspace contexts.
- `--project` selects compiler contexts while preserving imported shared source. Keep the default whole-workspace inventory for this. `--scope` is a stricter file boundary and can intentionally remove required dependencies; omissions remain gaps.
- `--tsconfig` can select explicit contexts. TypeScript handles JSONC, array/relative/package extends, path origins, includes/excludes and references. Referenced configs receive separate source contexts; this does not run a solution build or claim declaration-output equivalence.
- Shared files can appear in more than one context. Nodes identify their source-owning project(s) and compiler context; edges cannot accidentally join two apps' compiler universes. `trace --context` selects one context.
- Alias/barrel imports and source-linked workspace package exports use the compiler resolver. Only indexed workspace source and small dependency metadata/config files are read. External installed implementation source, out-of-workspace symlinks, built-only library outputs and PnP loaders are not expanded as source.
- Package JSON/config reads and misses are fingerprinted, including resolved real paths. Installing a missing config or retargeting a workspace link invalidates freshness. Changed compiler dependencies do not silently approve old notes after rescan.
- Nx without an export provides **static candidates** with a required resolved-graph gap. Nx exports preserve project dependencies and resolved targets. Project dependencies describe Nx relationships; they do not prove Formly injector precedence or UI navigation.
- Excluded/unconfigured source remains inventoried in separate candidate contexts. Build file replacements, runtime conditions, template scope and registration precedence still require review.

## Executed qualification

The portable source remains dependent only on Python, Node and an existing trusted TypeScript compiler. No Nx/Angular dependency was added to the skill ZIP or root dependency lock.

`npm test`: 44 passing tests, zero skips at this milestone (25 prior indexing regressions, 16 new workspace regressions, 3 packaging regressions). New cases cover JSONC root apps, custom directory layouts, competing app aliases and build configs, shared-library ownership, references and array extends, explicit selection, Nx fallback/nonexecution and export data, config package install/change freshness, scope omissions, invalid paths, cycles and linked package exports, context-filtered traces, overlapping project roots and package-link retargeting.

`tools/qualify_workspaces.cjs`: four generated workspaces passed with Node 22.23.3, TypeScript 5.9.3, Angular DevKit **21.2.27**, and Nx **23.3.0**:

| Case | Independent oracle and observed result |
| --- | --- |
| Angular single app | Scanner project list matches Angular `readWorkspace`; root app resolves shared fields and a form host. |
| Angular multi-project | Same comparison with nonstandard app/library roots; project-specific contexts resolve the shared source. |
| Nx integrated | Actual Nx export includes a local plugin-inferred project, target defaults and custom roots; scanner follows the selected app into shared forms. |
| Nx package workspace | Actual Nx resolves npm/pnpm workspace membership, negative exclusion, package metadata, inferred project and target defaults; scanner imports the same project set. |

These are real-tool **static discovery and source-graph** checks on generated workspaces, not Angular builds, browser tests, or an audit of the owner's workplace monorepo. Angular 21.2.25 / Material 21.2.14 / Formly 6.3.12 runtime evidence remains unchanged, including the two known browser failures. Older Nx export shapes, custom executors without discoverable configs, generated external schemas and very large production graphs remain qualification opportunities.

Final `npm run check` passed all 44 tests with zero skips, current syntax/link validation, and the extracted-bundle scan/trace/note smoke check. The four real-tool cases passed again after the final fixes. Raw outputs are retained locally under ignored `test-output/workspaces-2026-10-15/`.

See [development](development.md) for repeatable commands and [the portable workspace guide](../skill/ask-formly/references/workspaces.md) for consuming-project usage. The new workspace tests stay under committed `tests/`; ignored historical archives are not required by CI.

## Sources

All accessed 2026-10-15. These are living documentation pages; publication dates were not stated. Installed-tool versions used for execution are listed above, not inferred from today's documentation.

- S1 — [Angular workspace configuration](https://angular.dev/reference/configs/workspace-config) and [file structure](https://angular.dev/reference/configs/file-structure): root/project/target layout.
- S2 — [Angular DevKit workspace API](https://github.com/angular/angular-cli/blob/main/packages/angular_devkit/core/README.md): workspace host and read/write APIs.
- S3 — [TypeScript extends](https://www.typescriptlang.org/tsconfig/extends.html): inheritance and relative path origin.
- S4 — [TypeScript project references](https://www.typescriptlang.org/docs/handbook/project-references): referenced config paths and solution structure.
- S5 — [TypeScript paths](https://www.typescriptlang.org/tsconfig/paths.html) and [compiler API](https://github.com/microsoft/TypeScript/wiki/Using-the-Compiler-API): compiler-based analysis. Public API signatures also checked in installed TypeScript 5.9.3 `typescript.d.ts`.
- S6 — [Nx project configuration](https://nx.dev/docs/reference/project-configuration) and [configuration types](https://nx.dev/docs/concepts/types-of-configuration): inference/defaults/project layering and workspace membership.
- S7 — [Nx commands](https://nx.dev/docs/reference/nx-commands) and [GraphJson](https://nx.dev/docs/reference/devkit/GraphJson): project graph export.
- S8 — [createProjectGraphAsync](https://nx.dev/docs/reference/devkit/createProjectGraphAsync) and [public Devkit imports](https://nx.dev/docs/kb/migrate-nx-imports-to-devkit): supported graph API, daemon and cache behavior.
- S9 — [Nx plugin project graph contributions](https://nx.dev/docs/kb/add-language-support): plugin code supplies nodes and dependencies.
- S10 — [get-tsconfig upstream](https://github.com/privatenumber/get-tsconfig): standalone parser and matchers.
- S11 — [ts-morph project setup](https://ts-morph.com/setup/): wrapper alternative.

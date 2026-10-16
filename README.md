# ask-formly

A source-grounded ngx-formly v6 skill with Angular Material guidance and a project-local inventory/connection map for agents building Playwright tests.

This is the canonical development repository, extracted from Research Depot on 2026-10-15. Start with [the skill](skill/ask-formly/SKILL.md) or the [project indexing guide](skill/ask-formly/references/project-indexing.md). The research documents at the repository root describe earlier milestones; their raw qualification/evaluation archives are local-only and may be absent in a fresh checkout; current setup commands are here and in [development](docs/development.md).

## Use the skill

Point your agent at `skill/ask-formly/SKILL.md`, or build the ZIP and extract its `ask-formly/` folder into your agent's supported skill directory. No Angular application dependencies are bundled or installed into the consuming project.

> Use ask-formly at /path/to/ask-formly/skill/ask-formly/SKILL.md. Index the admin app's Formly setup, custom fields/wrappers/validators, config locations and UI-to-config relationships. Infer conventions from source, ask only about unresolved scope, and save the inventory and reviewed notes under the app's .agents/ask-formly/ folder.

The index combines a static file inventory and TypeScript graph with agent-reviewed project/form notes. It follows simple screen bindings, config initializers, shared helpers and custom registrations. Dynamic construction and injector precedence remain explicit review gaps. It does not execute application factories or establish runtime behavior.

Angular single apps, multi-project workspaces and Nx monorepos have separate compiler contexts, project ownership and shared-library tracing. Nx uses its resolved graph export for inferred projects; see [workspace usage](skill/ask-formly/references/workspaces.md) and [research/qualification](docs/workspace-support-research.md). The [pnpm Nx and public-repository checks](docs/pnpm-nx-public-qualification.md) cover the exact apps/libs fixture and four public source scans. See the [public-gap fixes](docs/public-gap-fixes.md) for the subsequent source audit and regressions, followed by the [blind scanner audit](docs/blind-scanner-audit.md).

For direct use, with Python 3.9+, Node and the consuming application's trusted TypeScript compiler:

```sh
python3 skill/ask-formly/scripts/project_index.py scan --root /absolute/path/to/admin
python3 skill/ask-formly/scripts/project_index.py check --root /absolute/path/to/admin
python3 skill/ask-formly/scripts/project_index.py trace --root /absolute/path/to/admin --query SupplierComponent
```

`scan` writes `.agents/ask-formly/` in that application; `check` is read-only. See the guide for scopes, compiler selection, source-reviewed notes and limitations. Conceptual Formly questions do not require indexing.

## Develop and package

Use Node 22 (tested 22.23.3), npm and Python 3.9+ (tested 3.14.6). The single root development dependency is TypeScript 5.9.3; Angular fixtures retain their own separate lockfiles.

```sh
npm ci --ignore-scripts --no-audit --no-fund
npm run check
npm run build
```

`check` validates current docs/skill syntax, runs 71 indexing tests plus three packaging tests, and scans/traces/records a note using the extracted ZIP. Missing compiler dependencies fail the gate instead of silently skipping graph tests. `build` writes a deterministic ZIP, file manifest and SHA-256 checksum to ignored `dist/`. It packages only `skill/ask-formly/`, excluding research, tests, dependencies and local AI setup.

## Evidence and limits

- Knowledge snapshot: Formly 6.3.12; qualification baseline Angular 21.2.25 and Material/CDK 21.2.14. Do not upgrade a consuming app to match these pins.
- [Index regression tests](tests/project-index): 71 synthetic tests, including 500-form cases; no workplace source has been indexed.
- [Angular qualification summary](skill/ask-formly/references/angular21-qualification.md): earlier 17/17 zoneless probes, strict AOT success and **12/14 browser passes**, with two retained select failures. These are historical executed results, not an all-green release claim.
- [Agent audit summary](skill/ask-formly/references/evaluation-lessons.md): both comparison arms passed 5/6; no comparative superiority established.
- [Extraction record](docs/extraction.md): copied-file provenance and the checks executed after relocation. Old logs, paths and manifests are preserved as historical evidence.

## Repository map

| Path | Purpose |
| --- | --- |
| `skill/ask-formly/` | Portable skill, references and index helpers |
| `tests/project-index/` | Active index regressions used by CI |
| `qualification/`, `evaluation/` | Optional local historical archives, excluded from Git |
| Root research Markdown files | Original briefs, sources, decisions and plans |
| `tools/` | Current validation, packaging and AI Central bootstrap |
| [Development](docs/development.md) | Active commands, including runtime fixture reproduction |
| [AI Central](docs/ai-central.md) | Optional local maintainer setup |
| [Releasing](docs/releasing.md) | Local bundle and prepared draft-release workflow |
| [Handoff](docs/work/handoffs/2026-10-15-extraction.md) | Current state and next actions |

Upstream attribution remains in [third-party notices](skill/ask-formly/THIRD_PARTY_NOTICES.md). This extraction does not assign a new license to the owner's original work or publish a repository/release.

## Public corpus evidence

- [Angular/Nx and Formly corpus qualification](docs/public-corpus-qualification.md): 30 pinned public repositories and measured limits.
- [Corpus-driven indexing fixes](docs/corpus-gap-fixes-2026-10-16.md): provider discovery, binding source links, focused traces and the 11-repository replay.

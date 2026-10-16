# Index an application's Formly inventory and flows

Use when asked to index a project or when repeated form analysis needs durable project context. Keep results in **the consuming project's `.agents/ask-formly/`**, separate from this skill's upstream knowledge. Do not index a research repository's downloaded examples as an application.

## Start from code, ask only about unresolved scope

1. Locate the workspace root, Angular/Nx projects, actual dependency versions and existing index. Read project instructions. For an existing index, run `check` before relying on its notes.
2. Inspect conventional entry points: bootstrap/application config, root and feature modules, `FormlyModule.forRoot/forChild`, `FORMLY_CONFIG`, and imported configuration constants. Follow custom registration helpers and lazy modules. A root registration is a candidate setup entry point; establish whether the app actually imports it.
3. Choose app and shared-library scopes from source. If several apps are plausible, ask which the user means. Ask about backend/external schemas or nonstandard config locations only when code leaves a consequential gap. Persist answers, date and provenance in the project note. Missing optional answers permit an explicitly partial inventory.
4. Scan, inspect the generated summary and bounded queries, then read the cited sources. Automatic output is discovery evidence; the agent supplies the reviewed map.

Python 3.9+ runs discovery. Node and a trusted TypeScript compiler enable the AST graph. The default compiler is `<project>/node_modules/typescript/lib/typescript.js`; `--typescript` selects an existing trusted compiler. No install, application factory execution, build, package script or network request is part of indexing. Compiler majors 5/6 are accepted; 5.9.3 is tested. A missing compiler leaves lexical discovery available and reports the graph unavailable.

Set these variables to the actual absolute paths for this invocation:

```sh
ASK_FORMLY=/absolute/path/to/ask-formly
FORM_PROJECT=/absolute/path/to/application
python3 "$ASK_FORMLY/scripts/project_index.py" scan --root "$FORM_PROJECT"
python3 "$ASK_FORMLY/scripts/project_index.py" check --root "$FORM_PROJECT"
python3 "$ASK_FORMLY/scripts/project_index.py" find --root "$FORM_PROJECT" --query registration --limit 20
python3 "$ASK_FORMLY/scripts/project_index.py" trace --root "$FORM_PROJECT" --query SupplierComponent --direction out --depth 8 --limit 80
```

For a monorepo, repeat `--scope apps/admin --scope libs/forms` on `scan`; include relevant shared helpers and root setup files. Scope/exclude/compiler choices persist in `config.json`. `--scope .` restores whole-project discovery. Repeated `--exclude` accepts project-relative Python fnmatch patterns; edit `exclude: []` in config to clear exclusions. Git ignores apply when Git discovery succeeds; otherwise the report explicitly says they were not applied. Dependency/build/agent folders are always excluded. Symlinks, oversized/unreadable inputs and discovery limits are reported. Narrowing scope is a declared boundary, not a way to claim omitted forms were inspected.

## Build the map the E2E builder needs

Review every candidate when the user requests a full inventory; use bounded file/graph queries rather than loading all JSON. Record non-Formly matches, unclassified candidates and out-of-scope locations. Follow references from both the host and registration sides. Use `trace --direction in` for consumers and `both` for a bounded neighborhood; `truncated` means more traversal is needed.

| Reviewed note | Minimum useful contents |
| --- | --- |
| `project` | Selected app(s), actual versions/evidence, bootstrap → Formly setup path, root/feature/provider scopes, external config sources, user answers and unknowns |
| `inventory` | Candidate files classified as config/factory/schema/host/helper/registration/non-Formly/unresolved; observed directories and naming families with examples; coverage counts and exclusions |
| `registrations` | Each type, wrapper, validator, message, extension and preset: registration site/scope → implementation file/symbol; defaults, inheritance and override behavior where relevant. Preserve duplicate names. |
| `form-<name>` | Route/screen → component/template → `[fields]` binding → declaration/initialization → factory → sub-configs/shared helpers → custom registrations and implementation files. Note model paths, repeat/group structure, dynamic branches, external inputs, transformations and E2E implications. |

Use repository-relative `file:line` references and symbols, with each connection labeled **source-confirmed**, **candidate**, **user-reported**, **runtime-observed**, or **unresolved**. State static context (e.g. a particular call site) rather than pretending a graph proves runtime order. Shared helpers need one concise note and links, not copied explanations in every form. UI routes are candidates until Angular routing/component composition is followed; runtime visibility and accessible locators need browser evidence.

Write each reviewed note to a temporary Markdown file, then record it with all directly supporting source files:

```sh
python3 "$ASK_FORMLY/scripts/project_index.py" note --root "$FORM_PROJECT" \
  --id form-supplier --input /absolute/path/to/reviewed-form.md \
  --source src/supplier.component.ts --source src/supplier.fields.ts
```

The CLI records provenance; it cannot judge whether the note is true. Read the sources before attesting it. Do not include credentials, private example values or copied production data. Notes are project-local; ask-formly must not transfer them into its shared knowledge base. Honor the project's tracking policy; no automatic Git staging or ignore changes.

## Files, refresh and limits

`index.md` is the compact entry point. `index.json` contains file fingerprints, lexical signals, AST discovery kinds, import candidates, project metadata and separately labeled requested/npm-lock versions. `graph.json` contains source locations and typed edges. `notes/*.md` are reviewed context; matching JSON records fingerprints and review provenance. `config.json` stores scan settings. Generated files carry schema/ownership markers; unsupported or unmanaged output is refused where detected.

`complete-within-scope` describes source reading, not extraction completeness. Truncated signal previews and unparsed metadata remain warnings but do not prevent reviewing the fully read source. Unreadable/omitted scoped inputs make coverage partial and prevent note attestation until addressed or the scope is explicitly narrowed. JSON/remote schemas and nonstandard registration helpers may require manual classification even when their files are fingerprinted.

`check` is read-only: exit 0 means unchanged scoped inputs/artifacts and recorded note contents, exit 1 means missing/stale/incomplete, exit 2 is an error. Freshness is **not completeness, semantic verification or browser validation**. Any scoped source, settings, compiler or indexer change requires reviewing existing notes. `scan` refreshes generated files and preserves notes; it never silently re-approves them. Manually edited notes are reported as edited until deliberately reviewed and re-recorded. `find`/`trace` do not recheck freshness themselves. An interrupted writer leaves a lock to inspect before removal.

AST support includes declarations/references, relative imports, root-tsconfig aliases/re-exports, member assignments, literal root/feature/provider registrations, literal field/custom-name candidates, route/component references, lazy import targets, and simple template member bindings. Generic declarations provide leads for helpers and sub-configs. Registry-name edges deliberately **do not resolve Angular injector precedence**. Child tsconfig differences, inherited members, namespace/indirect registration helpers, complex template bindings, dynamic keys/types, remote schemas, factory-return evaluation, runtime mutation and registration inheritance need agent tracing. The tool never infers a custom type's behavior from its name. A built-in/external registration missing from the scanned source is not an application defect.

Finish by reporting the files/flows reviewed, candidate and unresolved counts, naming conventions observed, graph limitations and the next consequential gap. A full static inventory can still have unresolved runtime branches. Hand the requested form note plus current source references to [E2E analysis](e2e-analysis.md); the builder still verifies locators, requirements and behavior in the browser.

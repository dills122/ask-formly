# Angular and Nx workspace indexing

Use the **workspace root** containing `angular.json` or `nx.json`, not a nested app directory. Single Angular apps, Angular multi-project workspaces, and Nx repos use the same Formly inventory and graph. Project names/roots come from workspace metadata; do not assume `apps/` and `libs/`.

## Select an app without losing its shared forms

```sh
python3 "$ASK_FORMLY/scripts/project_index.py" scan --root "$FORM_PROJECT" --project admin
python3 "$ASK_FORMLY/scripts/project_index.py" trace --root "$FORM_PROJECT" \
  --query SupplierComponent --context products/admin/tsconfig.app.json --depth 8 --limit 80
```

`--project` is repeatable and selects named compiler contexts. The default file inventory still covers the workspace, so imports into shared libraries remain available. `--scope` instead removes files from the readable inventory; use it only for an intentional partial boundary. Reset a previous narrow scope with `--scope .`. Settings persist in `.agents/ask-formly/config.json`; remove `projects`, `tsconfigs` or `nx_graph` there to clear those choices.

Angular `angular.json` is read as JSONC. Project roots/source roots, target options and configuration variants are retained. Target `tsConfig` paths, conventional tsconfigs and recursive project references supply separate compiler contexts. For a custom executor/config location, use repeatable `--tsconfig workspace/relative/compile.json`. No config is required for a provisional source inventory, but unconfigured source has candidate status and default compiler options.

## Nx: use its resolved project graph

Nx plugins, target defaults, package workspaces and project declarations contribute to the final model. Static `project.json`/`package.json` discovery alone cannot establish that model. The scanner reports `static-candidates` until given an export.

In a trusted workspace, generate an export with its **installed Nx**; do not install or upgrade Nx just to scan:

```sh
cd "$FORM_PROJECT"
mkdir -p .agents/ask-formly
NX_DAEMON=false ./node_modules/.bin/nx graph --file=.agents/ask-formly/nx-project-graph.json
python3 "$ASK_FORMLY/scripts/project_index.py" scan --root "$FORM_PROJECT" \
  --nx-graph .agents/ask-formly/nx-project-graph.json --project admin
```

Nx graph generation executes workspace plugins and can write Nx caches; it is a separate workspace-tool command, subject to the project's execution policy. Importing the export never executes plugins or factories. If workspace execution is unavailable, use an existing export or report the partial static inventory. Both `GraphJson.graph` and a direct `ProjectGraph` object are accepted. Explicit export input can be ignored by Git and is fingerprinted (up to 16 MiB).

Regenerate the export after changing plugins, workspace membership, target defaults, package metadata or relevant configurations. Plain Nx JSON does not attest the source revision: `nx-export-freshness-unverified` remains an explicit warning. A fresh Formly index means unchanged inputs/export, not that the export matches today's Nx computation. Do not use a stale export to claim complete discovery.

## Interpret contexts correctly

Every graph node/edge carries its compiler context. Source nodes also identify their owning project; a shared library file can appear under several apps' different compiler settings. Select the relevant context before drawing E2E conclusions. Config names are identities, not a claim about which target/configuration is currently deployed.

TypeScript resolves JSONC, relative/array/package extends, path aliases, barrels, includes/excludes, project references and source-linked package exports. Cross-project imports remain in the requesting app's context; referenced projects can also have their own contexts. The scanner does not run `tsc -b`, use build output as a substitute for missing source, or simulate builder file replacements. Review reported config errors and import gaps.

Package config/metadata reads and source links within the workspace are fingerprinted, including missing probes. No dependency JavaScript is evaluated. External implementation packages, out-of-workspace symlink targets, PnP loaders, generated/ignored source and built-only libraries can remain unresolved. A package range or an Nx dependency edge is not proof of Angular/Formly runtime compatibility, registration scope or navigation.

A source outside configured programs remains an `unconfigured-source-candidate`, grouped by source owner. It must not be treated as shipped app code. A graph can contain test, library and application contexts; inspect `contexts`, `workspace.projects`, `workspace.configs` and `unresolved` selectively in `graph.json`.

Qualification: TypeScript 5.9.3 contract tests plus actual Angular DevKit 21.2.27 and Nx 23.3.0 discovery on four generated workspaces, plus a real pnpm 10.23.0 apps/libs install with root/base and per-project tsconfigs, shared Formly configs, custom types/wrappers/validators, and both path-alias and source-package-export resolution. This is static tooling evidence; the Formly v6 / Angular 21 / Material behavior baseline and browser limitations are unchanged. See [indexing](project-indexing.md) for freshness, reviewed notes and E2E handoff.


## Large repository interpretation

Select an app context before tracing; broad workspace scans may contain many test,
Storybook, library and unconfigured contexts with duplicated source nodes. Report
unique source files separately from context-specific graph nodes. A field-shaped
object is a structural candidate, not a confirmed Formly form: inspect its route,
host/binding or registration connections before using it to plan an E2E test.
Repositories without Formly can still contain such candidate objects.

Inspect current workspace metadata and dependency versions rather than assuming
an older README still describes Nx or the qualified Formly major. Public source
scans on newer Formly versions are discovery evidence only. Missing dependencies,
factory providers, asset symlinks and schematic template syntax can create
explicit gaps; distinguish those from proven app defects or runtime behavior.

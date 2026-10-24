# Index an application's Formly inventory and flows

Scans also generate bounded search profiles with cited static text and optional
configured aliases/translations. See [local form search](semantic-search.md) for
the optional lexical/hybrid CLI; search installation and model setup are separate
from the scan, and the existing MCP query tools remain unchanged.

Use when asked to index a project or when repeated form analysis needs durable project context. Keep results in **the consuming project's `.agents/ask-formly/`**, separate from this skill's upstream knowledge. Do not index a research repository's downloaded examples as an application.

## Reuse during development

An ordinary indexing request creates a static inventory and navigation starting points. Run `scan`, inspect `navigation.status`, inventory coverage and unresolved scope, then report what is available. Full source reviews and saved notes/records are optional enrichment, not a setup requirement. `review.status: pending` describes that optional coverage and does not make a ready navigation index unusable.

For repeated structural lookup use the optional [local MCP server](local-mcp.md):
`find_forms` selects an identity and `get_form_starting_points` supplies files,
symbols and relationships for Serena/codebase-memory or targeted source reads.
The CLI equivalent is `start --target SYMBOL --intent usages` (or `dependencies`).
Select `--file`/`--context` when ambiguous; follow `--offset` and `--snapshot` for
pages. `start` checks freshness; CLI depth defaults to 5 (maximum 10), and MCP
uses 12 (maximum 24). The result is static evidence, never automatic source review.
Existing reviewed facts remain available through the record queries.

For an already indexed application's behavior or reviewed explanations, use
`lookup` as the first retrieval call:

```sh
python3 "$ASK_FORMLY/scripts/project_index.py" lookup --root "$FORM_PROJECT" --query "supplier country validation"
python3 "$ASK_FORMLY/scripts/project_index.py" lookup --root "$FORM_PROJECT" --id form-supplier
```

It checks freshness and returns ranked note bodies with supporting source paths,
review provenance and relevant version evidence. The default is three notes and
12,000 total note-text characters; `--limit`, `--offset` and `--max-chars` control
these bounds. `truncated` marks shortened text; load that exact note with a larger
budget when needed. `has_more`/`next_offset` describe additional ranked matches,
not missing application coverage. Each match previews up to 12 supporting paths;
`source_count` and `metadata_path` identify further provenance. Version evidence
is also bounded to 12 entries with `version_count` indicating the total.

For implementation or diagnosis questions, optional `--with-source` adds numbered current
source excerpts from the selected notes' supporting files in that same call.
This mode defaults to two notes and 6,000 note-text characters, plus 14,000 total
source-text characters (`--source-chars` overrides the latter). `--limit` and
`--max-chars` still override note bounds. Up to four source files are selected
lexically from at most 64 supporting candidates; files above 128 KiB are skipped
for excerpts, with explicit reasons. Omission counts remain visible. These are
source excerpts, not additional reviewed conclusions: lines can be noncontiguous,
`complete_file: false` marks partial files, and `truncated` marks text lost to the
budget. Inspect missing context before assuming surrounding control flow. The
full freshness check still covers scoped source bytes, including omitted files.

Ranking is lexical, with name/title priority and a length adjustment; it is not
semantic search. Prefer a few distinctive form, field or behavior terms. A
`no-match` result does not establish absence: try an exact note ID, narrower
terms, a bounded `trace` or targeted source search. A fresh raw scan without
notes also returns `no-match`; lookup does not perform or certify source review.

Reuse returned source-confirmed facts and citations within their recorded scope.
If they answer the question, no redundant source reread is required. Read only
uncovered details or code being edited, batching independent known paths. Load
the relevant pinned skill reference for Formly semantics. Do not repeat the
initial inventory, a separate `check`, or a known form chain in the same unchanged
task. Check again after edits or when starting the next task.

`lookup` is read-only: exit 0 means `ready` or `no-match`; exit 1 means a missing
index or blocked reuse. Stale sources, edited notes, partial coverage or damaged
artifacts block note text. It checks all scoped source bytes and tool/config
fingerprints, including same-size edits with unchanged timestamps. Unchanged
lexical metadata can be reused; file contents and freshness verdicts are not
cached. It does not execute factories or require network access.

If `check` reports stale context, inspect the affected inputs, refresh discovery as needed and review notes before re-recording them. A new question outside the reviewed scope requires new investigation even when the index is fresh. Keep candidate, source-confirmed and runtime evidence distinct throughout reuse.

## Initial setup: start from code

1. Locate the workspace root, Angular/Nx projects, actual dependency versions and existing index. Read project instructions. For an existing index, run `check` before relying on its notes.
2. Locate configuration needed for scanning: workspace project selection, compiler and tsconfig. Let the scan discover conventional entry points and registration candidates. Follow custom helpers or lazy modules when a later question requires their semantics; do not investigate every registration before scanning.
3. Choose app and shared-library scopes from source. If several apps are plausible, ask which the user means. Ask about backend/external schemas or nonstandard config locations only when code leaves a consequential gap. Optionally save source-supported conclusions with date and provenance in a project note. Missing optional answers permit an explicitly partial inventory.
4. Run `scan` and inspect inventory coverage, graph availability, compiler contexts and unresolved scope. `navigation.status: ready` means static starting points are available, not that every form is understood. Report limited coverage or lexical-only discovery explicitly.
5. Use `start` or MCP `get_form_starting_points` for the requested form and pass its file/symbol hints to available code tools. Read source for gaps and conditions. Ordinary indexing is complete at this navigation stage; no full source review is required.
6. When requested, or when useful conclusions emerge during development, save source-reviewed notes and [form records](form-records.md). `review` checks optional note coverage and `records` lists form-record status. Pending review does not block starting-point lookup. Preserve existing notes without silently reapproving them after edits.

Python 3.9+ runs discovery. Node and a trusted TypeScript compiler enable the AST graph. The default compiler is `<project>/node_modules/typescript/lib/typescript.js`; `--typescript` selects an existing trusted compiler. No install, application factory execution, build, package script or network request is part of indexing. Compiler majors 5/6 are accepted; 5.9.3 is tested. A missing compiler leaves lexical discovery available and reports the graph unavailable.

Set these variables to the actual absolute paths for this invocation:

```sh
ASK_FORMLY=/absolute/path/to/ask-formly
FORM_PROJECT=/absolute/path/to/application
python3 "$ASK_FORMLY/scripts/project_index.py" scan --root "$FORM_PROJECT"
python3 "$ASK_FORMLY/scripts/project_index.py" check --root "$FORM_PROJECT"
# Optional: inspect saved-review coverage separately
python3 "$ASK_FORMLY/scripts/project_index.py" review --root "$FORM_PROJECT" --limit 20
python3 "$ASK_FORMLY/scripts/project_index.py" find --root "$FORM_PROJECT" --query registration --limit 20
python3 "$ASK_FORMLY/scripts/project_index.py" find --root "$FORM_PROJECT" --query registration --limit 20 --offset 20
python3 "$ASK_FORMLY/scripts/project_index.py" trace --root "$FORM_PROJECT" --query SupplierComponent --direction out --depth 8 --limit 80
```

For Angular/Nx monorepos, read [workspace discovery](workspaces.md). Prefer `--project admin` with the default workspace inventory to retain shared imports. `--scope` is a strict file boundary, not a project selector. Scope/exclude/compiler/project/config/export choices persist in `config.json`; `--scope .` restores the whole-workspace file inventory. Repeated `--exclude` accepts project-relative Python fnmatch patterns; edit `exclude: []` to clear exclusions. Git ignores apply when Git discovery succeeds; otherwise the report says they were not applied. Dependency/build/agent folders, including `.serena` and `.codebase-memory` caches, are excluded from ordinary inventory. Explicit Nx export input, dependency JSON needed by the compiler and source-linked packages have the bounded exceptions described in the workspace guide. Symlinks, oversized/unreadable inputs and discovery limits are reported. Narrowing scope never establishes coverage of omitted forms.

`find` searches file paths and discovery kinds, not source text; use `trace` for symbol or field names. Follow `next_offset` until `has_more` is false to review all file matches. Keep the query and index snapshot unchanged between pages. `trace` is a bounded neighborhood, not a paged inventory: continue from relevant symbols when it reports truncation. If the requested root itself is ignored by an enclosing Git repository, discovery stops with an error rather than presenting an empty inventory as complete. Use the intended workspace root or a standalone copy outside that repository.

For a focused form chain, repeat `--relation` on `trace`, for example `--relation renders --relation binds-fields --relation binds-fields-source --relation assigned-from --relation contains-field --relation references --relation type-candidate --relation wrapper-candidate --relation validator-candidate --relation implementation --relation extends-type-candidate`. The output records `relations` and `relation_filtered`; traversal and returned edges use only that selection. `truncated: false` describes the selected neighborhood, not complete application coverage. Excluded relationships can hide relevant paths: follow up with an unfiltered trace, another relation selection or source review. All relations remain enabled by default; direction, depth and node limits still apply.

Modern source discovery also recognizes imported `provideFormlyCore` and `provideFormlyConfig` calls (including aliases and namespace imports), with static config objects/arrays. A direct factory argument gets a `config-factory` implementation pointer when resolvable; its returned registrations remain unresolved. This syntax follows [pinned upstream core.config.ts](https://github.com/ngx-formly/ngx-formly/blob/1a13f84438590b5855a27458b425d9af35a319a1/src/core/src/lib/core.config.ts); it does not extend the Formly v6 runtime qualification. Exact zero-argument component-member calls (`fields()`, `this.fields()`) and member async bindings (`fields$ | async`) produce `binds-fields-source` edges with `runtime-value-unresolved` evidence and `template-value-needs-review` questions. These locate source members without proving signal identity, pipe scope, emitted values or factory results. Plain member bindings retain `binds-fields`; local-shadow guards apply to both.

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

`review` is read-only and checks freshness itself. Exit 0 / `status: recorded` means current `project`, `inventory` and `registrations` notes exist and each detected host file is a supporting source of a current `form-*` note. Exit 1 means pending, blocked or missing context; exit 2 means an error. Its `hosts` list is paged with `--limit`/`--offset`. This verifies recorded coverage, not note quality, completeness of host discovery or runtime behavior. Review unsupported factories, external schemas and other inventory gaps manually. `scan` and `check` include a compact review summary; `check` retains its source-freshness exit contract, so a fresh scan can still have pending review.

## Files, refresh and limits

`index.md` is the compact entry point. `index.json` contains file fingerprints, lexical signals, AST discovery kinds, import candidates, workspace/project/config-context metadata and separately labeled requested/npm-lock versions. `graph.json` contains source locations and typed edges. `form-records.json` contains bounded materialized static navigation; `forms/*.json` and `forms/*.meta.json` contain explicitly source-reviewed form facts and provenance. `notes/*.md` are reviewed context; matching JSON records fingerprints and review provenance. `config.json` stores scan settings. Generated files carry schema/ownership markers; unsupported or unmanaged output is refused where detected.

`complete-within-scope` describes source reading, not extraction completeness. Truncated signal previews and unparsed metadata remain warnings but do not prevent reviewing the fully read source. Unreadable/omitted scoped inputs make coverage partial and prevent note attestation until addressed or the scope is explicitly narrowed. JSON/remote schemas and nonstandard registration helpers may require manual classification even when their files are fingerprinted.

`check` is read-only: exit 0 means unchanged scoped inputs/artifacts and recorded note contents, exit 1 means missing/stale/incomplete, exit 2 is an error. Freshness is **not completeness, semantic verification or browser validation**. Any scoped source, settings, compiler or indexer change requires reviewing existing notes. `scan` refreshes generated files and preserves notes and reviewed form records; it never silently re-approves them. Manually edited notes are reported as edited until deliberately reviewed and re-recorded. `find`/`trace` do not recheck freshness themselves. An interrupted writer leaves a lock to inspect before removal.

AST support includes declarations/references, relative imports, per-config aliases/re-exports and source-linked workspace packages, member assignments, symbol-identified root/feature/provider registrations (named or namespace imports) with literal or source-resolved string constants/enums, field/custom-name candidates, route/component references, lazy import targets, and simple template member bindings. `provider-factory` points to source without evaluating its result. `extends-type-candidate` and `wrapper-candidate` follow declared base types/shared wrapper arrays; they do not merge defaults. Known object/array spreads follow override order; unknown spreads remain unresolved. Registration identities distinguish category and entry-point scope. Generic declarations provide leads for helpers and sub-configs. Registry-name edges deliberately **do not resolve Angular injector precedence**. Build file replacements, external/unresolved configs, inherited members, namespace/indirect registration helpers, complex template bindings, dynamic keys/types, remote schemas, factory-return evaluation, runtime mutation and registration inheritance need agent tracing. Possible template-local shadows suppress implicit member bindings across the whole template; explicit `this.member` still binds. This conservative guard can leave valid bindings for manual review. The tool never infers a custom type's behavior from its name. A built-in/external registration missing from the scanned source is not an application defect.

Finish indexing by reporting navigation readiness, candidate and unresolved counts, scope and graph limitations. When source review was performed, report its actual coverage separately. A full static inventory can still have unresolved runtime branches. Hand the requested form note plus current source references to [E2E analysis](e2e-analysis.md); the builder still verifies locators, requirements and behavior in the browser.

# Corpus-driven indexing fixes — 2026-10-16

Follow-up to the frozen [30-repository baseline](public-corpus-qualification.md). The baseline report and registry retain their original observations. This change prioritizes three observed obstacles to navigating real Angular/Nx and Formly projects.

## Changes

1. **Modern Formly registration discovery.** Recognize lexically imported `provideFormlyCore` and `provideFormlyConfig`, including aliases and namespace imports. Static config objects, arrays and known spreads reuse the existing registration discovery. Local functions/parameters with the same spelling do not qualify. A resolvable direct factory argument exposes a `config-factory` source pointer, while its returned registrations remain unresolved.
2. **Runtime field-binding source navigation.** Recognize `fields()`, `this.fields()` and `fields$ | async` as limited source-navigation shapes. New `binds-fields-source` edges carry `runtime-value-unresolved` evidence and a review question. Plain member bindings retain `binds-fields`. Local shadows, arguments, nested access, inherited members and complex expressions remain conservative gaps.
3. **Focused trace relationships.** Repeated `trace --relation` options restrict traversal and returned edges to explicitly selected relationships. This lets callers follow rendered hosts, field sources, assignments, field configurations and registration candidates without automatically expanding every component member. Default traces retain all relationships. Output records the filter; an untruncated result describes only that selected neighborhood.

The provider syntax is grounded in [pinned upstream Formly source](https://github.com/ngx-formly/ngx-formly/blob/1a13f84438590b5855a27458b425d9af35a319a1/src/core/src/lib/core.config.ts). The template shapes follow Angular's [signal getter syntax](https://angular.dev/guide/signals) and [AsyncPipe](https://angular.dev/api/common/AsyncPipe); the recognizer does not prove their runtime identity or scope. These are source-discovery improvements, not newer-major Formly runtime qualification. Formly v6/Material remains the semantic baseline.

## Regression evidence

Five new tests in `tests/project-index/test_modern_corpus.py` cover positive navigation and negative controls, factory non-evaluation, relation selection, inward traversal, depth truncation and rejecting relation options on non-trace commands. Red logs reproduced the absent capabilities before implementation. `npm run check` passed **84 tests, zero skips**, repository validation and installed-bundle smoke checks in the original working checkout after the changes. The isolated PR branch, which excludes unrelated in-progress workspace changes, separately passed **81 tests, zero skips**, validation and installed-bundle smoke checks.

Raw evidence is kept separately under ignored `test-output/corpus-gap-fixes-2026-10-16/`: frozen pre-change scripts, red/green logs, final check log, new scanner snapshot, replay driver/results, source assertions and in-session review. Public source pins and baseline acquisition details remain in the original registry. No public application dependencies, factories or Nx plugins are executed.

## Pinned corpus replay

All nine Formly repositories and two Angular/Nx controls produced static graphs. Every replay matched its original revision, had unique node IDs and valid edge endpoints, detected a temporary source mutation, and restored tracked source bytes. All generated artifacts and source snapshots were current. The three partial inventories remain partial; ng-matero correctly marks its existing baseline review note `needs-review` after the scanner change. No note was silently re-approved.

Bitwarden uses the previously qualified `--project web --tsconfig apps/web/tsconfig.json` scope. The other ten retain their default baseline scopes. Times are single samples on the same machine with uncontrolled caches and other local work; these are operational measurements, not evidence of a speedup or a statistically established regression.

| Repository | Baseline → new scan (s) | New binding source links | New registration candidates | Coverage |
|---|---:|---:|---:|---|
| bitwarden/clients | 34.93 → 35.33 | 0 | 0 | complete-within-scope |
| stefanoslig/angular-ngrx-nx-realworld-example-app | 2.62 → 2.83 | 0 | 0 | complete-within-scope |
| GSA/sam-design-system | 36.77 → 36.79 | 0 | 0 | complete-within-scope |
| siemens/element | 22.42 → 23.99 | 14 | 2 | partial |
| ng-matero/ng-matero | 2.58 → 2.71 | 0 | 0 | complete-within-scope |
| super-productivity/super-productivity | 42.06 → 45.89 | 10 | 3 | partial |
| iqb-berlin/studio-lite | 22.75 → 27.67 | 0 | 0 | partial |
| ngx-formly/ngx-formly | 7.78 → 8.29 | 2 | 234 | complete-within-scope |
| intershop/intershop-pwa | 48.76 → 53.06 | 59 | 0 | complete-within-scope |
| rero/rero-ils-ui | 12.60 → 12.76 | 8 | 2 | complete-within-scope |
| rero/ng-core | 6.21 → 6.38 | 3 | 0 | complete-within-scope |

Counts include repeated compiler contexts, test sources and examples; they are not counts of runtime forms. The patch adds 96 binding-source edges and 241 registration candidates across this replay. Angular/Nx controls retain zero Formly hosts/registrations. Source assertions specifically verify Super Productivity’s two main provider entries and Flowtime signal binding, Intershop’s shipping async binding, and RERO ILS public-search provider discovery.

Focused traces use an explicit compiler context, depth 8 and a 100-node limit, with the relation set recorded in raw evidence:

| Query | Unfiltered | Selected relationships | Source detail retained |
|---|---|---|---|
| IQB `ItemComponent` | 100 nodes, truncated | 87 nodes, not truncated | `id` field and `IdValidator` |
| Intershop `AccountProfilePasswordComponent` | 100 nodes, truncated | 24 nodes, not truncated | password fields and `PasswordFieldComponent` |
| Super Productivity `DialogFlowtimeSettingsComponent` | 100 nodes, truncated | 38 nodes, still depth-truncated | computed field source and `isBreakEnabled` |

The IQB substring query matches two class names; the recorded seed count makes this visible. Filtered traces remain source-review aids, not complete form inventories. Sixteen corpus assertion groups passed.

## Remaining limits

Factory return evaluation, runtime injector reachability/precedence, full Angular template scope and inherited bindings still need source or runtime review. Relation filters can omit useful paths; broad seed matches can still exhaust the node budget. Traces still load the full graph. The largest whole-workspace timeouts, memory costs and partial inventories are separate performance/coverage work; this patch makes no general scan speedup claim. Compiler contexts remain isolated.

No browser behavior changed, so runtime suites were not rerun. The historical browser result remains **12/14 with two known failures**; this static qualification does not supersede it.

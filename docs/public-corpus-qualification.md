# Public Angular, Nx and Formly corpus

Qualification date: 2026-10-16. This effort exercises the supplied Angular/Nx
repository list as structural workloads and adds public Formly applications and
libraries. The purpose is to discover useful workflows, performance boundaries
and incorrect or unresolved relationships. A completed scan is not a correctness
verdict for every node or edge.

## Outcome

- **All 21 supplied repositories were attempted**, plus **nine public Formly repositories**. Twenty-seven default scans produced static graphs; Spartacus, Angular framework and Bitwarden exceeded the 120-second whole-workspace deadline.
- All three narrower follow-ups produced graphs: Spartacus storefront tsconfig **60.58 s**, Angular `packages/forms` scope **8.14 s**, Bitwarden web selection **34.93 s**. These do not qualify the omitted scope.
- Default completed scans ranged from **0.65 to 48.76 seconds**. The highest reported peak RSS was **2.75 GiB**, for Super Productivity. Twenty default inventories were complete within scope; seven were partial.
- All 27 default graphs had unique IDs and valid edge endpoints, and all detected a controlled source-file change. Those are integrity checks, not proof of semantic accuracy.
- Median per-repository warm retrieval time was **0.077 s for find** and **0.129 s for trace**. The slowest trace median was **1.412 s**. **13/27** broad trace probes hit the 100-node bound.
- Ten source-reviewed positive relationship checks, three negative controls and five gap/boundary observations matched expectations. Fourteen strict-JSON Angular project inventories matched their declared names; one JSONC file was not compared by that independent check. No resolved Nx graph was executed or validated.
- The ng-matero note lifecycle passed: record → fresh → source change detected as stale → source restored and fresh. Artifact modification was detected, pagination returned distinct pages, and a note on partial IQB coverage was refused.

Focused context selection does not guarantee a compact trace: the 100-node IQB,
Intershop and Nx RealWorld probes were still truncated. The ng-matero focused
trace returned 76 nodes without truncation. Source-reviewed assertions establish
the specific relationships separately from these bounded retrieval outputs.

## Public Formly cohort

“Host files” means unique files containing detected Formly hosts, including tests
and demos. It is neither a count of production screens nor a runtime form count.

| Repository | Tracked TS files | Host files | Best use in this corpus |
| --- | ---: | ---: | --- |
| Super Productivity | 3,316 | 17 | Large application; settings, computed/signal fields, application-scale retrieval |
| IQB Studio Lite | 1,117 | 1 | Nx application with a focused metadata form and custom validator/wrapper registrations |
| Intershop PWA | 2,421 | 60 | Substantial commerce forms; custom type inheritance, validator factories and async configs |
| GSA sam-design-system | 1,323 | 164 | Dense Formly types, wrappers and demos; strongest broad positive source corpus here |
| Siemens Element | 1,857 | 22 | Design-system integration, factory providers and explicit partial coverage |
| ng-matero | 211 | 1 | Small application control; understandable route/host/config trace and note workflow |
| ngx-formly upstream | 720 | 77 | Library/examples corpus across adapters; not an independent consuming application |
| RERO ILS UI | 706 | 14 | Multi-application consumer with schema/editor and external-library boundaries |
| RERO ng-core | 219 | 7 | Companion form library, schema/editor helpers and newer provider patterns |

Keep these as complementary workloads. Prioritize Intershop, Super Productivity,
GSA and Siemens for breadth/scale; IQB for the Nx/Formly combination; ng-matero
for quick workflow checks. Larger Angular repositories are useful structural
controls even when they contain no Formly. RERO's application and library were
scanned independently, without linking or installing one into the other.

## Method

All repositories are shallow public checkouts with recorded commit IDs. The
scanner's three source files were frozen before measurement, independently of
other work in the development checkout. Runs use the existing trusted TypeScript
5.9.3 compiler, without installing public dependencies or executing public build
scripts, application factories or Nx plugins. Thus Nx results remain static
candidates; this experiment does not validate resolved Nx project graphs.

The initial pass scans every repository with default whole-workspace discovery.
Each scan has a 120-second external deadline and a 4 GiB Node heap ceiling.
Timeouts, unavailable graphs and partial inventories remain explicit results.
Follow-up selected-project/config scans are separate experiments, not replacement
passes. Versions are declarations at the pinned revision, not installed runtime
versions. Workspace catalog versions require separate resolution.

Measurements are sequential wall-clock CLI durations and macOS `time -l` maximum
resident set size. Peak RSS is the OS measurement for the command and its children,
not total simultaneous machine memory. The host is shared, OS caches are not
controlled, and one scan is not a statistically stable throughput benchmark.
Some sources had already been read by the retained sandbox attempt; these are
not cold-cache measurements, and `scan` recomputes the index rather than measuring
an incremental parser update.
Three subsequent CLI find/trace samples include process startup and JSON loading.
Trace size/truncation measures retrieval behavior, not the correctness of an
agent's reasoning. Source mutations for freshness checks occur only in disposable
clones and are restored byte-for-byte.

Raw logs, acquisition records, frozen scanner, measurement drivers and results
are under ignored `test-output/public-corpus-2026-10-16/`. The earlier sandbox
measurement attempt is retained separately and excluded: macOS `time -l` could
not read `kern.clockrate`, changing the wrapper's exit status. An aggregation
mistake (`edge.kind` instead of `edge.relation`) was corrected without changing
the scanner; valid scan logs were reused for subsequent retrieval probes.
The inventory oracle initially filtered by evidence label, wrongly excluding two
legacy Nx projects whose `angular.json` declarations are labelled static
candidates. Comparing the declared source file corrected that harness mistake;
the original comparison is retained alongside the corrected result.

## Evidence boundaries

This is static scanner qualification. No public application was compiled or run
in a browser. No Formly runtime version compatibility, injector precedence,
complete Angular template semantics, business-rule extraction accuracy or agent
speed improvement is established. Existing Angular 21 / Formly 6 / Material
runtime evidence remains separate, including its two known browser failures.

The public Formly cohort intentionally includes newer majors and non-Material
adapters. It tests source discovery and exposes API-shape gaps; it does not expand
the portable skill's Formly 6 semantic baseline. Framework repositories and
component libraries are structural stress cases, not representative form apps.
The corpus does not turn ask-formly into a general Angular analysis engine:
complete NgRx/data-flow understanding, permission-rule extraction and Markdown
instruction/skill ingestion are not part of its established scanner contract.

## Use-case assessment

| Use case | What this experiment can establish |
| --- | --- |
| Discover an unfamiliar Angular/Nx workspace | Declared/static project inventory, compiler contexts, source ownership and explicit missing dependencies. Nx plugins and inferred targets require a separately generated graph. |
| Find a form or field implementation | Source file search, candidate hosts/configurations, and sampled source-reviewed relationships. Generic field-shaped objects remain candidates. |
| Trace custom types, wrappers and validators | Known module/provider shapes and source-resolvable imports; runtime registration precedence and factory results remain unknown. |
| Work in a very large monorepo | Whole-workspace resource limits versus selected project/config or explicitly narrowed source scope. |
| Reuse reviewed knowledge | Record a source-backed note and detect a subsequent source change or generated-artifact modification. |
| Prepare a debugging or E2E handoff | Bounded source pointers and explicit unknowns. Browser locators, behavior, accessibility and generated-test quality still need runtime verification. |

The useful next improvements should follow observed gaps: modern Formly provider
recognition with version-specific evidence; signal/pipe template binding analysis;
large-workspace memory and context-duplication costs; and focused retrieval that
does not require loading an entire graph for every query. These are follow-up
engineering opportunities, not changes made by this qualification run.

## Reproduction

Final repository verification: `npm run check` passed **79 tests with zero skips**,
metadata/link/syntax validation and the extracted-bundle smoke test. The frozen
three-file scanner snapshot still matched the current scanner byte-for-byte at
completion. All downloaded tracked source files were restored after probes.
This effort added evidence and documentation; it did not change the scanner.

Use the revision and scan options in the accompanying registry. Clone and check
out that revision into a disposable directory, then run the portable CLI with an
explicit trusted compiler:

```sh
python3 skill/ask-formly/scripts/project_index.py scan \
  --root /absolute/path/to/disposable-checkout \
  --typescript "$PWD/node_modules/typescript/lib/typescript.js"
python3 skill/ask-formly/scripts/project_index.py check \
  --root /absolute/path/to/disposable-checkout
python3 skill/ask-formly/scripts/project_index.py find \
  --root /absolute/path/to/disposable-checkout --query form --limit 20
```

Use `trace --context` with the recorded compiler context for source-reviewed
chains. Inspect coverage, warning reasons and truncation before relying on
results. Missing external dependencies and unsupported API shapes must not be
silently treated as complete discovery.




## Measured results

Exact revisions, compiler/scanner fingerprints, declared versions, scan options, timings and unresolved groups are in [the registry](public-corpus-registry.json).

The cohort contains **30 repositories: all 21 supplied Angular/Nx repositories and nine Formly repositories**. Counts include tests/examples; graph records can repeat source in different compiler contexts. Host counts below deduplicate file paths, not runtime forms.

| Repository | Tracked TS | Scan seconds | Reported peak RSS GiB | Source coverage / outcome | Host files |
| --- | ---: | ---: | ---: | --- | ---: |
| [super-productivity/super-productivity](https://github.com/super-productivity/super-productivity/tree/6e132c00860bfcb6665cb7994f081fa9aa43ba1d) | 3316 | 42.06 | 2.75 | partial | 17 |
| [iqb-berlin/studio-lite](https://github.com/iqb-berlin/studio-lite/tree/51843a9e7d9b3007cd8a252753629bbd74f593e6) | 1117 | 22.75 | 1.10 | partial | 1 |
| [ABIRAJ-JUNIOR/Nx-angular-workspace](https://github.com/ABIRAJ-JUNIOR/Nx-angular-workspace/tree/d9a5c1131480db05293a27a3fb68065942f4b09c) | 46 | 1.28 | 0.17 | complete-within-scope | 0 |
| [Ismaestro/angular-example-app](https://github.com/Ismaestro/angular-example-app/tree/6b47dfa03ef3a6cdd48674a68d0bd655f892e8e4) | 119 | 1.65 | 0.18 | complete-within-scope | 0 |
| [NexuSolo/Nx-CI-CD](https://github.com/NexuSolo/Nx-CI-CD/tree/3b5099bcf3e343603ca8d77bdf2b4ba9db87b3f3) | 38 | 0.65 | 0.14 | complete-within-scope | 0 |
| [NguyenPham1805/ngx-admin-v20](https://github.com/NguyenPham1805/ngx-admin-v20/tree/a5ed1f1d33f8b70969cf0752c9bebb27e04a50cd) | 214 | 1.86 | 0.18 | complete-within-scope | 0 |
| [SAP/spartacus](https://github.com/SAP/spartacus/tree/9c0b2a88d0bc9de88ad8b04d3ce68509af2a6039) | 9023 | 120.00 | unavailable | timeout / no completed graph | — |
| [analogjs/analog](https://github.com/analogjs/analog/tree/0e3fb39d0dfd66c7edf4a593890766c639ac5153) | 871 | 16.24 | 0.92 | complete-within-scope | 0 |
| [angular/angular](https://github.com/angular/angular/tree/92e5aa8f154096a756757d0e295cde4299788650) | 6202 | 120.01 | unavailable | timeout / no completed graph | — |
| [angular/components](https://github.com/angular/components/tree/3f9f22ba985eb7f85e812aa66a75ec7b143fd756) | 2349 | 39.99 | 2.63 | partial | 0 |
| [angular/material.angular.io](https://github.com/angular/material.angular.io/tree/de23cd20a37e14c2ff5cbbcb6d390fc98a745a3f) | 139 | 1.85 | 0.19 | partial | 0 |
| [bitwarden/clients](https://github.com/bitwarden/clients/tree/6d198af9512e6a180eb4e1d6a226dcaced81edd3) | 6665 | 120.00 | unavailable | timeout / no completed graph | — |
| [cjanz/nx-monorepo-sample](https://github.com/cjanz/nx-monorepo-sample/tree/e8ef45a8082a50da00654ab707e92ff7c4f3b263) | 49 | 1.25 | 0.16 | complete-within-scope | 0 |
| [code-star/nx-reference](https://github.com/code-star/nx-reference/tree/dc16abaf605f439cdffab084fd4a84ec8135ea22) | 66 | 1.04 | 0.17 | complete-within-scope | 0 |
| [coreui/coreui-free-angular-admin-template](https://github.com/coreui/coreui-free-angular-admin-template/tree/ba51cff2f2f8ced9ad71cbbb1969129bdc5ba69c) | 147 | 1.56 | 0.17 | complete-within-scope | 0 |
| [ngrx/platform](https://github.com/ngrx/platform/tree/ddd9772e81e2db8a8964fa65f355086118d29dd9) | 1157 | 10.82 | 0.71 | complete-within-scope | 0 |
| [nrwl/nx-examples](https://github.com/nrwl/nx-examples/tree/a543631df74669bf7ea12f7982376fce3a1f645c) | 85 | 1.13 | 0.17 | complete-within-scope | 0 |
| [primefaces/primeng](https://github.com/primefaces/primeng/tree/fe82b291d6fedde177dc12c0af7ef1008dc1b1ff) | 3205 | 20.34 | 1.20 | partial | 0 |
| [realworld-angular/realworld-angular](https://github.com/realworld-angular/realworld-angular/tree/e73088a1a54b89554eeb70399325578b4f62b8ce) | 144 | 1.80 | 0.18 | complete-within-scope | 0 |
| [skrischer/nx-setup](https://github.com/skrischer/nx-setup/tree/d9bd1268120aa3bd2940b7eec34718d616c10bb5) | 26 | 0.66 | 0.14 | complete-within-scope | 0 |
| [stefanoslig/angular-ngrx-nx-realworld-example-app](https://github.com/stefanoslig/angular-ngrx-nx-realworld-example-app/tree/bc7158d61319b6748b94cef301dc347efcc23f00) | 110 | 2.62 | 0.22 | complete-within-scope | 0 |
| [taiga-family/taiga-ui](https://github.com/taiga-family/taiga-ui/tree/3ae41cf83dc3d9c24c62660394a4f99dab08fe8a) | 3451 | 47.23 | 1.53 | partial | 0 |
| [tomwhite007/enterprise-angular-mono-repo-patterns-example](https://github.com/tomwhite007/enterprise-angular-mono-repo-patterns-example/tree/4862afbcc2f5cb8b10b414afa3075d43764a1f40) | 90 | 1.29 | 0.17 | complete-within-scope | 0 |
| [GSA/sam-design-system](https://github.com/GSA/sam-design-system/tree/d7125deb76ddb3278e83b2639705da13367c4282) | 1323 | 36.77 | 2.62 | complete-within-scope | 164 |
| [siemens/element](https://github.com/siemens/element/tree/2360b8f4bbdb1241516603355ed415d5a22bded9) | 1857 | 22.42 | 0.97 | partial | 22 |
| [ng-matero/ng-matero](https://github.com/ng-matero/ng-matero/tree/d351bf5957d8c6dc9eca79d0c9b260c5b8d07822) | 211 | 2.58 | 0.19 | complete-within-scope | 1 |
| [ngx-formly/ngx-formly](https://github.com/ngx-formly/ngx-formly/tree/1a13f84438590b5855a27458b425d9af35a319a1) | 720 | 7.78 | 0.41 | complete-within-scope | 77 |
| [intershop/intershop-pwa](https://github.com/intershop/intershop-pwa/tree/6b18c92f92af6aab3c9c7f532f0059e8845051d0) | 2421 | 48.76 | 1.61 | complete-within-scope | 60 |
| [rero/rero-ils-ui](https://github.com/rero/rero-ils-ui/tree/ebf410cf487e120f136445d7cd9ce0577ec039c7) | 706 | 12.60 | 0.57 | complete-within-scope | 14 |
| [rero/ng-core](https://github.com/rero/ng-core/tree/4cb26c551367738de4bfee63c8f70f28bb813332) | 219 | 6.21 | 0.29 | complete-within-scope | 7 |

### Selected follow-ups

These are narrower scopes after a deadline, with the original failures retained above.

| Repository | Selection | Seconds | Reported peak RSS GiB | Coverage / result |
| --- | --- | ---: | ---: | --- |
| SAP/spartacus | `--tsconfig projects/storefrontapp/tsconfig.app.json` | 60.58 | 2.04 | partial |
| angular/angular | `--scope packages/forms` | 8.14 | 0.85 | complete-within-scope |
| bitwarden/clients | `--project web --tsconfig apps/web/tsconfig.json` | 34.93 | 1.68 | complete-within-scope |

### Source-reviewed probes

These deliberately small checks cover source-reviewed chains and explicit limitations. A true observation in a known-gap row means the limitation was reproduced, not that the feature works.

| Repository | Check | Classification | Observation matched |
| --- | --- | --- | --- |
| iqb-berlin/studio-lite | ItemComponent renders the source Formly host | positive | True |
| iqb-berlin/studio-lite | Host binds to ItemComponent.fields | positive | True |
| iqb-berlin/studio-lite | fields assignment contains id configuration | positive | True |
| iqb-berlin/studio-lite | id field links to registered id validator candidate | positive | True |
| iqb-berlin/studio-lite | id registration links to IdValidator implementation | positive | True |
| super-productivity/super-productivity | Flowtime settings host is discovered | positive | True |
| super-productivity/super-productivity | fields() signal binding has no binds-fields edge | known-gap | True |
| super-productivity/super-productivity | Signal binding carries complex-template-binding warning | boundary | True |
| intershop/intershop-pwa | Password form host binds fields | positive | True |
| intershop/intershop-pwa | Password config has custom type candidate | positive | True |
| intershop/intershop-pwa | Password type inherits no-validation base candidate | positive | True |
| intershop/intershop-pwa | Async checkout binding remains explicit | boundary | True |
| stefanoslig/angular-ngrx-nx-realworld-example-app | Application lazy import reaches home library source | positive | True |
| stefanoslig/angular-ngrx-nx-realworld-example-app | No detected Formly hosts or registrations | negative-control | True |
| nrwl/nx-examples | No detected Formly hosts or registrations | negative-control | True |
| nrwl/nx-examples | Static Nx discovery requires resolved graph | boundary | True |
| bitwarden/clients | No detected Formly hosts or registrations | negative-control | True |
| bitwarden/clients | Static Nx discovery requires resolved graph | boundary | True |

### Retrieval and freshness

| Repository | Find median seconds | Trace median seconds | Trace nodes | Truncated |
| --- | ---: | ---: | ---: | --- |
| super-productivity/super-productivity | 0.129 | 1.157 | 100 | True |
| iqb-berlin/studio-lite | 0.126 | 0.396 | 100 | True |
| ABIRAJ-JUNIOR/Nx-angular-workspace | 0.075 | 0.074 | 0 | False |
| Ismaestro/angular-example-app | 0.077 | 0.126 | 100 | True |
| NexuSolo/Nx-CI-CD | 0.075 | 0.076 | 63 | False |
| NguyenPham1805/ngx-admin-v20 | 0.075 | 0.128 | 77 | False |
| analogjs/analog | 0.076 | 0.451 | 100 | True |
| angular/components | 0.129 | 1.412 | 100 | True |
| angular/material.angular.io | 0.077 | 0.129 | 28 | False |
| cjanz/nx-monorepo-sample | 0.073 | 0.078 | 4 | False |
| code-star/nx-reference | 0.074 | 0.077 | 7 | False |
| coreui/coreui-free-angular-admin-template | 0.075 | 0.074 | 100 | True |
| ngrx/platform | 0.126 | 0.338 | 100 | True |
| nrwl/nx-examples | 0.073 | 0.074 | 0 | False |
| primefaces/primeng | 0.129 | 0.448 | 100 | True |
| realworld-angular/realworld-angular | 0.078 | 0.127 | 100 | True |
| skrischer/nx-setup | 0.075 | 0.078 | 0 | False |
| stefanoslig/angular-ngrx-nx-realworld-example-app | 0.077 | 0.075 | 100 | True |
| taiga-family/taiga-ui | 0.130 | 0.621 | 100 | True |
| tomwhite007/enterprise-angular-mono-repo-patterns-example | 0.122 | 0.075 | 0 | False |
| GSA/sam-design-system | 0.078 | 0.937 | 15 | False |
| siemens/element | 0.147 | 0.551 | 100 | True |
| ng-matero/ng-matero | 0.077 | 0.127 | 17 | False |
| ngx-formly/ngx-formly | 0.074 | 0.176 | 78 | False |
| intershop/intershop-pwa | 0.125 | 0.788 | 100 | True |
| rero/rero-ils-ui | 0.124 | 0.179 | 4 | False |
| rero/ng-core | 0.073 | 0.129 | 19 | False |
| SAP/spartacus (selected) | 0.185 | 0.970 | 100 | True |
| angular/angular (selected) | 0.073 | 0.330 | 100 | True |
| bitwarden/clients (selected) | 0.124 | 0.538 | 100 | True |

The generic retrieval benchmark searches `form` and traces a discovered host name (or `form` when no host was found). These are deliberately broad requests, often spanning contexts. Empty/truncated traces are not useful navigation passes. Separately recorded focused traces use source-reviewed class/file queries and explicit contexts.

Freshness, note lifecycle, pagination, and artifact-integrity observations are retained in `test-output/public-corpus-2026-10-16/workflow-results.json`; source-reviewed assertions are in `source-checks.json`. Bitwarden source checks use the selected web graph; other source checks use their default graphs.

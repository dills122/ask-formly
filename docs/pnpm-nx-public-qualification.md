# pnpm Nx fixture and public repository qualification

Executed 2026-10-15. Decision: use the controlled fixture as the exact Angular 21 /
Formly v6 / Material contract; use several pinned public repositories for scale,
unfamiliar source patterns and conservative handling of unresolved cases. None of
the public results establishes runtime compatibility or exhaustive trace accuracy.

## Exact pnpm Nx fixture

[Fixture sources](../tests/fixtures/pnpm-nx-formly/README.md) use pnpm 10.23.0,
Nx 23.3.0, TypeScript 5.9.3, Angular 21.2.25, Material/CDK 21.2.14 and
Formly core/material 6.3.12. A real pnpm install and actual Nx graph export passed
the shared [flow contract](../tests/project-index/pnpm_nx_contract.py) twice:
with inherited TypeScript path aliases, then with those aliases removed so
resolution must use pnpm workspace links and source package exports.

Verified chain:

`suppliers route → SupplierComponent → formly-form → fields assignment → buildSupplierFields → billing group → addressFields → accountCode`

The accountCode field connects to its custom type, wrapper and validator, each
with implementation file/project identity. The main bootstrap's `forRoot`
registration connects to all three. The source flow crosses four libraries while
remaining in `apps/admin/tsconfig.app.json`; Portal's same-name registration is
excluded. All four expected Nx dependency edges are present. The CLI trace has
18 nodes / 20 edges and is not truncated. Registration matches remain explicitly
`registration-scope-unresolved`; these tests do not prove runtime injector scope.

The final `npm run check` passed 47 tests with zero skips, metadata/link/syntax
validation and the extracted-bundle smoke check.

Three permanent regressions cover the complete chain, a broken-barrel negative
control, and freshness invalidation when the imported shared config changes.
The negative control confirms that an incomplete chain cannot pass the contract.
The only graph-level unresolved reason in the exact fixture is
`nx-export-freshness-unverified`, retained by design even after an export was just
generated. The scanner does not independently attest Nx's source revision.

## Public candidates actually scanned

Counts below come from pinned local checkouts (`git ls-files`, including test and
declaration files ending in `.ts`). Versions are declared package versions/ranges,
not installed runtime versions. No public repository dependencies, build scripts
or Nx plugins were installed/executed. The scanner used our TypeScript 5.9.3.

| Repository | Tracked TS files | Declared Angular / Formly | Why retain it |
| --- | ---: | --- | --- |
| [GSA sam-design-system](https://github.com/GSA/sam-design-system/tree/d7125deb76ddb3278e83b2639705da13367c4282) | 1,323 | 21.2.24 / 7.1.0 | Strongest large Formly corpus here: custom types, wrappers and many demos; includes Material date range implementation |
| [Siemens Element](https://github.com/siemens/element/tree/d255d4b46862ecc0bab869a33c72d0245c7ebe72) | 1,857 | 22.0.8 / 9.0.0 | Large Angular design-system workspace, factories, wrappers and legacy/modern Formly integration |
| [ng-matero](https://github.com/ng-matero/ng-matero/tree/d351bf5957d8c6dc9eca79d0c9b260c5b8d07822) | 211 | ^22.2.0 / ^8.0.0 | Smaller Material admin app; straightforward screen/config trace ground truth |
| [Bitwarden clients](https://github.com/bitwarden/clients/tree/95040c39dff64fb4f0846456599da9948116240b) | 6,642 | 21.2.17 / no root Formly dependency | Best large Nx structural control here: Nx 22.7.10, apps and shared libs; not a positive Formly benchmark |

GSA's old contributor documentation references Nx, but this revision has no
`nx.json` or root Nx dependency. Classify it as an Angular workspace. Bitwarden
has an actual [Nx configuration](https://github.com/bitwarden/clients/blob/95040c39dff64fb4f0846456599da9948116240b/nx.json).
Repository names, old docs and folder conventions alone are insufficient evidence
of present workspace tooling.

| Scan | Indexed files | Contexts | Graph nodes / edges | Source coverage |
| --- | ---: | ---: | ---: | --- |
| GSA, default workspace | 1,885 | 17 | 155,363 / 210,685 | complete-within-scope |
| Siemens, default workspace | 3,264 | 44 | 68,228 / 156,019 | partial |
| ng-matero, default workspace | 329 | 5 | 2,039 / 4,125 | complete-within-scope |
| Bitwarden, web project + explicit web tsconfig | 8,252 | 2 | 48,735 / 162,951 | complete-within-scope; Nx static candidates |

These are source-reading metrics, not confirmed forms or semantic completeness.
GSA/Siemens/ng-matero have hosts in 164/22/1 unique files respectively. Multiple
contexts duplicate nodes; structural field candidates also include unrelated
objects. Bitwarden has no detected Formly hosts, entries or registrations, although
generic field-shaped candidates exist. Its web context imports 2,983 unique
library source files. The second context is explicitly unconfigured source.

### Source-checked examples and open limits

- **GSA:** `formly.module.ts`'s `FormlyModule.forChild(FORMLY_CONFIG)` connects
  through the imported config to `daterangepickerv2` and its actual
  `FormlyFieldDateRangePickerComponent`. Both graph edges were asserted and source
  read. See [registration](https://github.com/GSA/sam-design-system/blob/d7125deb76ddb3278e83b2639705da13367c4282/libs/packages/sam-formly/src/lib/formly/formly.config.ts#L244)
  and [implementation](https://github.com/GSA/sam-design-system/blob/d7125deb76ddb3278e83b2639705da13367c4282/libs/packages/sam-formly/src/lib/formly/types/daterangepicker.ts).
  The run still has 4,362 unresolved records, including external imports, dynamic
  names, registration gaps and an empty tools tsconfig.
- **Siemens:** the [legacy provider](https://github.com/siemens/element/blob/d255d4b46862ecc0bab869a33c72d0245c7ebe72/projects/element-ng/formly-legacy/si-formly.module.ts#L30)
  uses `FORMLY_CONFIG` with `useFactory: dynamicUiConfig`. Its
  `dynamic-provider-factory` gap was asserted rather than treating factory output
  as known. The run has 6,660 unresolved records. Coverage is partial because docs
  asset symlinks are not traversed; an unreadable metadata path also reports
  `IndexError_`. This is not a complete-inventory pass.
- **ng-matero:** the [dynamic route](https://github.com/ng-matero/ng-matero/blob/d351bf5957d8c6dc9eca79d0c9b260c5b8d07822/src/app/routes/forms/forms.routes.ts#L10)
  connects to `FormsDynamic`, then two HTML hosts bound to `fields` and `fields2`.
  The route edge and both bindings were asserted against source. Its 284 unresolved
  records include external registrations and unconfigured schematic templates
  that are not parseable ordinary TypeScript. Those templates do not prove the
  application's TS source is broken.
- **Bitwarden:** selected `web` and `apps/web/tsconfig.json`; verified library
  imports and absence of Formly hosts/registrations. Its 3,348 unresolved records
  include external imports, overlapping package/project declarations and
  `nx-resolved-project-graph-required`. No Nx export was generated, so this is a
  static discovery/scale check, not validation of its resolved Nx model.

No scanner implementation change was required by the exact fixture. Public scans
exposed useful limits and noise, not enough ground truth to assert every reported
connection is correct. Registration factories, real injector scope, generated
source and built dependency implementations remain follow-up work.

## Reproduce and extend

The [development guide](development.md#exact-pnpm-nx-formly-fixture) describes the
locked fixture and real-tool harness. The regular gate includes its three offline
regressions and needs neither pnpm/Nx nor network access after root dependencies
are installed.

For public sources, clone the repository, check out the exact commit above, and
use a trusted compiler without installing the target repository's dependencies:

```sh
python3 skill/ask-formly/scripts/project_index.py scan \
  --root /absolute/path/to/public-checkout \
  --typescript "$PWD/node_modules/typescript/lib/typescript.js"
```

For Bitwarden, append `--project web --tsconfig apps/web/tsconfig.json`.
Review `index.json` coverage/warnings and `graph.json` unresolved records before
tracing. Use the context containing the relevant app; do not sum all contexts as
unique forms. A larger public suite should pin revisions and assert selected
source-reviewed chains and intentional unknowns rather than graph size alone.

This bounded search did not establish a large public repo matching **all** of
pnpm + modern Nx + Angular 21 + Formly v6 + Material. Smaller Nx/Formly leads
[formly-builder-sample](https://github.com/nthonymiller/formly-builder-sample) and
[fullstack-monorepo](https://github.com/cntower/fullstack-monorepo) were inspected
as candidates but not qualified; they do not replace the large corpus or our exact
version fixture. The selected four scans plus three source spot checks are a
useful starting corpus, not an exhaustive public-repository audit.

Sources accessed 2026-10-15; commit pins above identify all executed source.
Local raw outputs, declared versions, commit dates and gap counts are retained in
ignored `test-output/pnpm-nx-public-2026-10-15/`. No third-party source is bundled
into the skill. Browser/AOT results and Formly v6 knowledge remain unchanged.

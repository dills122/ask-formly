# Blind scanner audit — 2026-10-16

Scope: adversarial source-indexing correctness for Formly 6.3.12 with Angular 21 /
Material as the project baseline. No runtime behavior, AOT, Playwright, dependency
upgrade, factory execution or new parser dependency is claimed.

## Independence and frozen target

The first agent had no inherited conversation. It recorded its own cases and
preliminary results before reading the public-gap report, associated tests or
author explanation. Mandatory README/development guidance disclosed intent and
test counts, so this was blind to implementation rationale, not to repository
purpose. The initial scanner SHA-256 was
`c6512b2ddb38a94cbd6a7a571e38c1a072f61a26001b3db54d5ecff2aa9a922a`.

The independent oracle ran **11 cases: 3 passed, 8 failed**, covering five findings.
The author replayed that immutable oracle against preserved baseline scripts and
confirmed the failures. Most defects predated the latest six public-gap fixes;
the audit does not attribute them all to that patch.

A second fresh-context reviewer checked the corrections and adjacent patterns.
This was an informed revision review, not a second fully blind experiment. It
confirmed the original 11 cases passed and found three further bounded issues.
The final informed reviewer accepted the resulting corrections. Three independent
review instances were used; detailed reviewer reports remain local.

## Findings and disposition

| Finding | Decision and resulting behavior |
| --- | --- |
| Registration-item and field spreads kept obsolete properties | Accept. Reuse ordered static property extraction for names, components, field keys/types/wrappers/validators and inheritance. An unknown spread withholds unverifiable semantic links and emits a gap. |
| Shadowed `FormlyModule` / `FORMLY_CONFIG` names became registrations | Accept. Recognize the actual TypeScript import binding rather than matching spelling. Component decorator recognition uses the same identity check. |
| Template locals linked to unrelated class fields | Accept. Decline implicit bindings when a same-name local/reference is detected anywhere in the template. Explicit `this.member` remains supported. This deliberately over-approximates possible shadowing rather than parsing lexical scope. |
| Static validator-array spreads silently lost validators | Accept. Reuse bounded array traversal for validators and async validators; retain known entries plus explicit gaps for unknown spreads. |
| Namespace imports lost Formly entry points | Accept. Support namespace member imports while rejecting shadowed namespace bindings. |
| Spreads/duplicate keys inside validator objects kept obsolete rules | Accept. Apply the same ordered property extraction inside validators/asyncValidators. Unknown object spreads do not preserve potentially overwritten validator connections. |
| One object shared by type and wrapper categories collided | Accept. Registration IDs now include both category and entry-point scope. Tests use a `FieldWrapper` subclass, which also extends v6 `FieldType`. |
| A provider spread could replace its token but still be treated as Formly | Accept. Resolve the effective token and value/factory before extracting a provider, including static spread-only providers. Unknown overrides remain unresolved; unrelated spread objects are probed without emitting provider noise. |

The final reviewer also reproduced a missing warning for an unknown spread over
a statically inherited Formly token. A diagnostic-only adjustment now reports
that uncertainty without adding resolved edges. The same still-open final review
verified the narrow amendment with old/new hashes; no fourth review was started.

These corrections stay inside the existing static model. They do not decide which
registration wins at runtime, merge inherited defaults or evaluate functions.
Generic reference edges still describe source references, including overwritten
expressions; they are not claims that an expression is an active runtime value.

## Tests and evidence

The immutable first-review oracle passes after the first corrections. The 21
portable [regression tests](../tests/project-index/test_blind_patterns.py) retain
its original 11 cases, five adjacent boundary tests, four tests from the second
review and one final diagnostic regression (several contain subcases). New failing
expectations were executed before each implementation change. Controls are retained rather than being misreported
as new baseline failures. The ordinary gate also includes the existing exact
pnpm/Nx cross-library fixture and earlier 53 tests.

The original audit validates the v6 source forms against the pinned upstream
configuration and validator implementation. Additional grounding:

- [v6.3.12 configuration model](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/models/config.ts)
  keeps type and wrapper categories separate.
- [v6.3.12 FieldWrapper](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/templates/field.wrapper.ts)
  extends `FieldType`, grounding the shared-object category regression.
- [Angular lexical expression context](https://angular.dev/guide/templates/expression-syntax#lexical-context-for-expressions)
  documents local shadowing and explicit `this.` access (accessed 2026-10-16).
  Only that lexical rule is relied on; newer expression features on the live page
  do not expand the Angular 21 baseline.

No exact scanner checkout was indexed by codebase-memory; review used direct
source inspection and executable CLI fixtures, with no graph-coverage claim.
Source fixtures are static probes, not compiling/running application examples.

## Final validation and public replay

Final review verdict: **Ready**, with no actionable findings remaining in the
reviewed scope. The frozen scanner SHA-256 is
`2ee549a4f7467522f345db61bf1a80b1c608a216de2f71e60499ebad213c5a92`.
The independent original oracle passes **11/11** and retained audit regressions
pass **21/21**. The full repository gate passes **74 tests with zero skips**
(71 indexing and three packaging tests), metadata/link/syntax validation, and
an extracted ZIP smoke test. Browser and AOT checks were not rerun for these
static scanner corrections.

All four pinned public repositories from the [public corpus](pnpm-nx-public-qualification.md)
were replayed after the main fixes. Results below precede the final warning-only
amendment; they are not claimed as public replays of the final hash. That amendment
was separately verified against the original oracle, permanent regressions and
review probes, with unchanged nodes and edges in both affected reproductions.

| Repository | Nodes | Edges | Unresolved records | Source coverage |
| --- | ---: | ---: | ---: | --- |
| GSA/sam-design-system | 155,511 | 213,834 | 3,507 | Complete within selected scope |
| siemens/element | 68,228 | 156,030 | 6,660 | Partial; asset-link limitations retained |
| ng-matero/ng-matero | 2,039 | 4,126 | 284 | Complete within selected scope |
| bitwarden/clients | 48,757 | 162,981 | 3,349 | Complete within selected scope; static Nx candidates |

Every replay used TypeScript static analysis, unique node IDs and valid edge
endpoints. Unresolved counts include missing external registrations and dynamic
source; they are not defect counts. These public versions provide discovery
coverage, not Formly v6 or Angular 21 runtime qualification. No application
factories, Nx plugins or public-repository dependencies were executed.

## Remaining boundaries and package size

Template scope is deliberately conservative across an entire template, including
sibling scopes; this can decline valid bindings. A full Angular template parser,
arbitrary re-export helpers, dynamic factories, runtime mutation and injector
selection remain outside this change. Public source candidates still require
classification, and missing external registrations are not automatically defects.

Scanner changes invalidate old indexes through the existing tool fingerprint.
The portable skill receives only a small edit to its existing indexing-reference
paragraph. Tests, review reports and raw replay outputs remain outside the ZIP.
Local evidence is in ignored `test-output/blind-scanner-audit-2026-10-16/`.

# Validation source mapping

Nine proposed facts in two core documents; isolated candidate target79facts/17documents. No installed/canonical source changes, no model changes, and no evaluation artifacts opened. These are curated claims supported by inspected pinned sources, not automatically extracted truth or runtime qualification.

The unchanged validation guide supplies eight facts; the unchanged matching-fields example summary supplies one. All evidence IDs already exist in the installed catalog. Eight upstream files were fetched at commit5f099fddea6426b46a453866adf0fede5be0bcd7 and their full-file hashes match the retained catalog. `source-verification.json` records URLs/hashes and exact review ranges. Web-reader raw fetch returned cache misses; read-only HTTPS fetch then succeeded. Upstream tests were inspected, not run.

| Proposed fact | Pinned evidence checked | Bounded interpretation |
|---|---|---|
| validation-contracts/named-boolean-expression | K08:23–27,110–142;K26:138–157 | Named expressions use boolean validity; truthy error maps do not mean invalid. |
| validation-contracts/registered-validator-contract | K36:30–39,62–67;K26:118–135 | Public registration is FieldValidatorFn→ValidationErrors/null; no new TypeScript/AOT execution claim. |
| validation-contracts/registered-boolean-tolerance | K08:97–142 | Runtime boolean adaptation and typed contract are distinct; simple name:true payload only without options. |
| validation-contracts/builtin-prop-validators | K08:17–21,34–94 | Six named props; observed changes revalidate when a control exists; keyless group exception retained. |
| validation-contracts/length-error-key-compatibility | K08:69–84 | Exact lowercase message checks; no arbitrary casing tolerance. |
| validation-contracts/default-error-visibility | K04:34–44 | Default predicate, not a promise for custom wrappers/showError overrides. |
| validation-contracts/message-configuration | K04:55–63;K36:48–50,65–67;K38:45–77 | Configuration surfaces keyed by errors; full precedence/reactivity intentionally not added. |
| validation-contracts/async-expression-result | K08:126–143;E03a:15–54 | Promise/Observable named booleans; example is not a production HTTP policy. |
| validation-group-example/group-errorpath-registration | E04a:14–42;E04b:11–38;K08:148–161 | Group placement+registered name+errorPath. Bootstrap presentation and universal cleanup guarantees excluded. |

## Explicit exclusions/deferred work

- Historical routed-error probe results and references to evaluation-evidence.json are not used. Source cleanup implementation alone does not establish every sibling-edit transition; keep that risk as a limit, not a newly claimed tested defect/repair.
- TS2322/AOT execution in historical prose is not asserted as a newly reproduced compiler result. The public type signature itself was inspected.
- Application investigation, domain validation policy, real network error/retry/cancellation policy and universal async completion are excluded.
- Exact message precedence, first-error ordering and reactive message-trigger nuances were inspected in K38 but are not admitted in this small batch. The retained guide does not spell out all those contracts.
- Source advice to test all control transitions remains advice; no Angular application was run.

The validation source ledger has all four direct sections accounted for with pending draft admissions and explicit exclusions. The example summary is supplemental provenance for the one group fact; this does not claim complete examples.md coverage. Source hashes and quote matching are mechanical checks. Mapping interpretation and final admission require independent review plus the frozen MCP comparison.

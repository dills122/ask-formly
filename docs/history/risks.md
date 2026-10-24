# Risks and unresolved assumptions

As of 2026-10-15. These are research risks and proposed controls, not observed skill failures.

| Priority | Assumption or risk | Evidence / uncertainty | Cheapest useful check and decision consequence |
| --- | --- | --- | --- |
| 1 | A focused skill improves on a capable agent with official docs | Entirely untested | Eight-case comparison remains outstanding; the owner explicitly requested corpus deepening before that gate. If it adds little value, retain a small docs/version guide. |
| 1 | v6 knowledge remains separated from newer APIs | v7 introduces different setup APIs [S13]; adjacent Angular skills have modern defaults [S14] | Include incompatible-API traps and mixed-version retrieval in evaluation. Any undetected critical version mismatch blocks release. |
| 1 | Exact application versions are known | Material selected; Angular and Formly patch unknown | A synthetic Angular 21.2.25 / Material 21.2.14 fixture is declared; inspect a consuming workspace before application qualification. Treat reference-snapshot qualification separately from application qualification. |
| 1 | Documentation summaries are sufficiently accurate | Specific prose/type inconsistencies observed [S4–S6, S11] | Source-check and execute the highest-impact recipes. Do not ingest scraped pages as unquestioned instructions. |
| 2 | Local field registrations and factory behavior are understood | No application configuration supplied | Use a custom-type case where required context is missing. Skill must identify unknowns rather than invent registrations or runtime results. |
| 2 | Loading many references remains useful | No token/latency measurements | Measure loaded references and evidence lookup effort across baseline/prototype. Split or remove content only in response to actual retrieval failures. |
| 1 | Material guidance transfers across versions | Broad package peers are metadata, not exhaustive compatibility evidence [S10] | Qualify exact combinations; use existing project harnesses and adapters. Avoid a universal v6/Material claim. |
| 2 | A suitable existing skill was not missed | Public search incomplete; unauthenticated code search unavailable | Reassess any specific maintained candidate offered later; keep the initial custom work small and reusable. |
| 2 | Third-party retrieval is version-correct and available | Context7 v6-specific retrieval not verified [S17] | Make retrieval optional; reject evidence whose applicable version cannot be established. |
| 3 | Maintenance can stay small | Estimate only | Review references when upstream/app versions or observed failure cases change; rerun affected cases before updating the corpus. Do not silently refresh to newest Formly major. |
| 3 | Reused material remains attributable and private details stay local | Upstream MIT license inspected [S22]; no private configs used | Keep source notices and a source map; keep project-specific examples outside the shared package unless sanitized and intended for reuse. |

Sources: [source register](sources.md). The 17 development probes validate only their stated behaviors on the declared stack; no product-level assumption above is marked experimentally validated. See [runtime evidence](skill/ask-formly/references/runtime-evidence.md).

Observed qualification boundary: replacing the sole active select option while open fails keyboard/model selection in both Formly and bare Material on this exact stack. A consuming-app regression and public-API close/reopen design need qualification before relying on this flow. [Evidence](skill/ask-formly/references/angular21-qualification.md).

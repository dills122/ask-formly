# Findings: ask-formly

Research date: 2026-10-15. Source IDs resolve in [sources.md](sources.md).

## Recommendation

**Inference:** build a focused Formly skill and reuse upstream documentation, source, and examples. A fork of a broad Angular skill would still need most of the Formly-specific work and would introduce unrelated guidance. Start with curated Markdown references and small tested recipes; defer a documentation server or vector database until a measured retrieval problem justifies it.

The owner's idea has a useful shape. The important asset is the combination of version discipline, project context, diagnostic workflows, and verified examples. A senior-engineer persona can describe the expected judgment, but is not evidence of expertise. The proposed architecture follows the local skill-creator guidance on concise entrypoints and loading supporting knowledge only when relevant [S21].

## What already exists

These are original repositories or provider documentation inspected during this pass. Marketplace descriptions were used for discovery, not capability verification.

| Candidate | Verified scope | Fit and disposition |
| --- | --- | --- |
| Dedicated `ask-formly` / ngx-formly expert skill | None verified in the bounded search | This is an observation about discovery, not proof that none exists. See [coverage](search-log.md). |
| Official `angular/skills` | General Angular development and new-app skills; the developer skill starts by checking the project version [S14] | Useful companion and packaging example. It is not a demonstrated v6 Formly knowledge base. Keep its newer framework defaults subordinate to the actual application. |
| Analog `angular-forms` | Original skill now marked unmaintained; description targets Signal Forms and explicitly excludes Formly [S15] | Do not adopt as the Formly foundation. Marketplace copies can preserve older content after upstream changes. |
| OpenEMS `oe-ui-test` | Real skill with Formly view-test instructions, tied to OpenEMS/Ionic test helpers [S16] | Evidence that application-specific Formly skills exist. Too coupled to OpenEMS to serve as a portable Material/Formly expert; use as a design example rather than copying its conventions. |
| Context7 | Provider lists both ngx-formly repository and website documentation [S17] | Optional retrieval helper. The inspected listing says “Latest”; a v6-specific result set was not verified. It cannot be the sole version authority. |
| Formly Contract, `dills122/formly-contract` | README describes declared/scenario extraction for Formly 6.x, producing agent-readable contracts. It explicitly says production MCP and automatic browser-test generation are not shipped [S18] | Potential later input for analyzing large forms. It is an extraction tool, not a general expert skill. Capabilities were read, not executed. |
| ng-forge | Different Angular dynamic-forms library with its own MCP package [S19] | Adjacent design reference; changing the form engine would not meet the stated need. |
| Manual v6 documentation plus a normal coding agent | Official documentation is publicly available [S2–S8] | Credible low-cost baseline. Keep this approach if the skill cannot measurably improve quality or effort. |

Several “Formly AI” search hits refer to hosted form builders or compliance products rather than `@ngx-formly/core`. For example, formly.so describes a hosted agent-connected forms service [S20]. Name overlap is a discovery hazard.

## What the version boundary actually means

**Documented facts and direct metadata observations:**

- There is a separate official v6 site. The current site's v6-to-v7 migration guide introduces `provideFormlyCore` and standalone Formly APIs [S2, S13]. A v6 answer should not import those APIs. Angular standalone host components and Formly's own standalone exports are separate questions.
- Registry inspection found v6.3.12, published 2024-12-08, as the newest stable v6 package. Its core peers require Angular Forms `>=13.2.0` and RxJS `^6.5.3 || ^7.0.0`. Material v6.3.12 requires core exactly `6.3.12` and Angular Material `>=13.0.0` [S9, S10]. A permissive peer range does not prove every later Angular/Material combination works.
- Tagged v6.3.12 types retain `templateOptions`, `hideExpression`, and `expressionProperties` as deprecated APIs. Prefer `props` and `expressions` when authoring new configurations, while understanding old code. Legacy expression callbacks and `expressions` callbacks do not have interchangeable signatures [S4, S11].
- v6 migration behavior includes OnPush rendering, changed defaults, model-change expression checks, lazy rendering, and clearing hidden values by default [S3]. These are useful diagnostic topics, not reasons to globally change an application's settings.
- Patch history matters: v6.3.10 includes an array/default/reset-on-hide fix; v6.3.11 includes form-state change detection; v6.3.12 includes Angular 19 submit-validation work [S12]. Diagnose against the installed patch before attributing a symptom to user code.

**Inference:** use a pinned reference snapshot plus a small patch-history map. “V6 expert” should mean bounded expertise across v6, with explicit patch qualifications; it should not mean silently treating every v6 installation as v6.3.12.

## Why copying the docs is insufficient

**Observed documentation inconsistencies:** the v6 expression guide describes an example setting `props.disabled` as hiding the field [S5]. The properties table describes async validation as promise-based, while tagged types also allow Observables [S4, S11]. The validation guide distinguishes Angular validators from boolean Formly expressions, but contains inconsistent wording in a later boolean example [S6].

These observations justify source-backed fact notes and executable examples. They do not justify discarding the docs. When prose and code disagree, compare the exact release's declarations, implementation, and tests; retain the discrepancy and reproduce the relevant behavior before presenting it as established.

The Material documentation route exists, but the fetched HTML exposed mostly a shell, not useful component guidance [S8]. Plan to inspect versioned Material source and examples during corpus construction. Merely crawling pages would miss important content.

## Build/adapt/use comparison

| Approach | Initial effort (relative estimate) | Main benefit | Main limitation |
| --- | --- | --- | --- |
| Manual docs + normal agent | Lowest | No maintenance artifact | Repeated research and inconsistent version selection |
| Docs retrieval service alone | Low | Convenient source discovery | No guaranteed v6 boundary or debugging workflow |
| Adapt broad Angular skill | Medium | Existing structure | Formly knowledge still missing; broad defaults need care |
| Focused skill + curated references + fixtures | Medium | Fits requested tasks; portable and auditable | Requires ongoing curation and behavioral evaluation |
| Custom MCP/RAG expert service | Highest | Shared retrieval and possible integrations | Adds infrastructure before evidence that it is needed |

The fourth option is the recommended first investment. A skill supplies instructions and resources to the invoking agent; it does not itself create a separate model or expert service [S21]. Another agent can use the same skill with a task packet containing versions, relevant configuration/registrations, the question, and expected behavior.

## Confidence and remaining unknowns

High confidence in the v6 source boundary and the verified candidates' stated scope. Moderate confidence that a new focused skill is the best fit, because public search has coverage limits. Effectiveness, context cost, and actual maintenance effort are untested. The application's Angular version, Formly patch, custom Material types, and representative troublesome forms are still unknown. The [validation plan](validation.md) is designed to resolve these before a broad rollout.

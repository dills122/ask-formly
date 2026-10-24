# Companion mechanisms and next construction steps

Updated/accessed: 2026-10-15. These are engineering recommendations based on the current corpus, not demonstrated improvements in answer quality.

## Primary integration: E2E builder

The owner clarified a large legacy admin-system use case and subsequently authorized indexing. Prioritize the [source-to-test workflow](e2e-use-case.md): ask-formly interprets form behavior; the builder owns browser evidence and Playwright execution. The new [indexing workflow](skill/ask-formly/references/project-indexing.md) combines a local inventory/AST graph with source-reviewed project notes under `.agents/ask-formly/`. It requires no additional skill or retrieval service. Synthetic qualification establishes discovery behavior, not reduced E2E repair effort on real forms.

## Use now

| Mechanism | Purpose | Boundary |
| --- | --- | --- |
| Focused reference files | Load only the API/behavior needed for a question | Entrypoint stays small; no whole-source prompt dump |
| `evidence.json` plus readable sources | Locate exact source paths, revisions, excerpts, and evidence status | Hashes support provenance, not behavioral correctness |
| Ordinary text search | Find a topic/known symbol offline in retained notes | Fetch/read exact-version source for uncovered questions |
| Optional source graph | Navigate classes and relationships in a pinned source checkout | Coverage must be checked; docs, examples, and tests need file-search fallback |
| Existing Angular tooling | Inspect target versions and compile/run a relevant reproduction | No universal compatibility inferred from Formly peer ranges |

The portable [skill](skill/ask-formly/SKILL.md) requires no MCP server. This construction used a local source graph, but the graph's exclusions made direct source reads essential. Adding a mandatory retrieval service now would not address the largest remaining uncertainty: whether answers and generated code work in the target application.

## Development fixture: first probe built

The deeper pass created a [development fixture](qualification/README.md) with a lockfile and 17 passing JIT/jsdom probes on Angular 21.2.25 / Material/CDK 21.2.14 and Formly 6.3.12. It stays outside the distributable skill. This synthetic stack does not establish compatibility with the owner’s app. The [zoneless/AOT/browser follow-up](qualification/browser/README.md) now adds strict compilation and 14 Chromium cases, including two retained select failures and verified recovery.

Start with three executable recipes: a nested Material form with validation, conditional visibility with an explicit data-retention requirement, and a registered custom Material-compatible type. For each, define expected model and control transitions before running it. Use compilation, rendering, and behavior assertions appropriate to the requirement. Then run the eight-case comparison in [validation.md](validation.md). Source-read examples should only become copyable verified recipes after passing their checks.

Unknown target versions do not block knowledge authoring. They do prevent calling this corpus qualified for the owner's application. A synthetic stack can qualify a declared example environment, with that narrower claim.

## Add a project overlay when a real application is supplied

Keep project-specific knowledge with that project: resolved versions, selected form factories, registered type/wrapper names and meanings, validation conventions, model/submission transformations, and links to relevant tests. Record unknown dynamically supplied behavior. The shared skill should inspect this overlay when relevant, without treating a custom name such as `address` as a universal Formly feature.

The authorized index now supplies generated discovery plus short project, registry, inventory and per-form notes. Scope and freshness are explicit; refresh preserves notes and flags them for review after source changes. A separate companion skill is unnecessary while this workflow fits inside ask-formly. Do not copy secrets or private form data into the shared corpus.

## Optional later integrations

| Candidate | Useful role | Adoption trigger |
| --- | --- | --- |
| Formly Contract | Consume existing declared/resolved contracts and diagnostics as extra evidence | A real task benefits from extracted context; keep browser-observed behavior distinct [S18] |
| General Angular skill | Framework-specific implementation help | Relevant Angular task and version-compatible instructions [S14] |
| Context7 or another docs retriever | Discover additional documentation | Returned content can be tied to the required Formly version [S17] |
| A knowledge-maintenance helper | Check hashes, links, and new evidence records repeatedly | Manual maintenance becomes frequent enough to justify a supported script |
| Dedicated review/debug companion skills | Repeat a specialized workflow with its own inputs and checks | Actual use shows the entrypoint's modes are insufficient |

Do not create empty companion skills, a custom MCP server, embeddings, or a fine-tuning pipeline yet. Retain retrieval failures or context-size evidence before adopting that complexity. One focused skill with task routing is enough for the first usable knowledge artifact.

## External projects inspected

These were checked for transferable ideas, not copied into the v6 knowledge base. Repository push dates describe activity, not release dates or quality. Dependency observations describe the files read on the access date, not all historical versions.

| Project | Observed primary evidence | Decision |
| --- | --- | --- |
| GrumpTech/formly-designer | README describes a visual designer, OpenAPI support, demos and dual licensing; package manifest uses Angular ~21.2.18, Material ^21.2.14 and Formly ^8.0.0. Repository last push observed 2026-10-09. [S24] | Potential design/interaction inspiration. Current code is outside the v6 baseline; inspect a suitable historical revision and licensing before reuse. |
| nthonymiller/formly-builder-sample | README describes a typed fluent builder; manifest uses Angular ^11.0.0, Material ^11.1.1 and Formly ^5.10.14. Last push observed 2021-03-14. [S25] | Historical authoring-pattern example, not v6 API evidence. No reason to adopt its dependency stack. |

Official pinned examples remain the first source for implementation mechanics, with explicit caveats where their source is incomplete or potentially misleading. The [example catalog](skill/ask-formly/references/examples.md) records those caveats.

Source register: [sources.md](sources.md). Corpus evidence: [pinned index](skill/ask-formly/references/sources.md).

# Construction plan for ask-formly

Status: deeper knowledge pass and selected runtime probes completed, 2026-10-15. The owner authorized building the knowledge base after the initial research. The portable [draft](skill/ask-formly/SKILL.md) now exists in this idea folder; it is not installed; only the explicitly listed probe behaviors are runtime-checked. The milestones below retain the broader qualification plan. The owner confirmed Angular Material as the first UI adapter. Research and source IDs are in [research.md](research.md) and [sources.md](sources.md).

Current priority: [Formly understanding for the E2E builder](e2e-use-case.md). The earlier milestones below describe the original general-purpose skill plan; the next gate is meaningful generated-test performance on unfamiliar existing forms.

## Product contract

`ask-formly` helps a developer or coding agent understand and work on ngx-formly v6. It should answer a small feature question directly, and inspect enough surrounding code for a complex diagnosis. It should preserve the application's design unless a change is requested.

| Mode | Input | Useful result |
| --- | --- | --- |
| E2E analysis | Route/requirement, repository context, relevant UI evidence | Source-linked behavior, prerequisites, action order, locator candidates, assertions and unknowns for the test builder |
| Explain | Feature/API question, optional version | Plain explanation, version boundary, minimal example, relevant source |
| Read/review | Fields, model, registrations, relevant hooks | Model paths, nested structure, dependencies, runtime unknowns, actionable issues |
| Author | Desired behavior and application context | Typed fields plus necessary imports/registrations, model example, validation steps |
| Debug | Expected/actual behavior, config, versions | Evidence-based diagnosis, smallest correction, regression scenario, remaining uncertainty |
| Extend | Existing type/wrapper and desired behavior | Appropriate extension point and integration with the existing Material setup |

The senior-engineer persona should be behavioral: trace model/control/config relationships, distinguish symptoms from causes, ask only for material missing context, prefer small changes, and state what was actually verified. Avoid biography, inflated authority, or generic Angular tutorials.

## Package and development layout

```text
ask-formly/                       # future development repository
  skill/ask-formly/
    SKILL.md                      # scope, version gate, task routing, answer contract
    agents/openai.yaml            # optional Codex discovery/UI metadata
    references/
      version-policy.md
      config-and-model.md
      expressions-and-lifecycle.md
      validation.md
      custom-types-and-wrappers.md
      material.md
      debugging.md
      sources.md                  # exact source revisions + known discrepancies
    assets/recipes/               # only verified examples worth reusing
  evals/                          # development-only prompts, rubric, results
  fixtures/                       # development-only pinned Angular/Material app
```

The current draft uses this general structure, with separate API, arrays, customization, JSON Schema, examples, and coverage notes plus a machine-readable evidence manifest. A development qualification fixture now has 17 passing JIT/jsdom probes on pinned Angular 21.2.25 / Material 21.2.14 and Formly 6.3.12; a separate zoneless fixture now passes strict AOT and 12/14 Chromium cases; two select failures are retained. Full application recipes and agent-comparison results do not yet exist. This broader layout is not a requirement to create empty files. Add arrays, JSON Schema, extensions, or other separate references when their actual depth warrants it. Keep evaluation answers and full fixture dependencies out of the installed skill. No custom scripts are needed initially; add a version-report or reference-check helper only if repeated manual work proves its value.

Aim for roughly 150–250 lines in the entrypoint as a planning ceiling, not a target. Load the version policy and only task-relevant references. A short feature question should not load all recipes or require a repository-wide scan. This follows progressive disclosure guidance [S21].

## Version and project-context gate

1. Identify `@ngx-formly/core`, all installed Formly UI packages, Angular, Material/CDK, RxJS, and TypeScript from the consuming workspace. Prefer resolved lockfile/installed versions over a manifest's semver range; record disagreements. Do not run arbitrary project configuration just to read versions.
2. Use v6.3.12 at commit `5f099fddea6426b46a453866adf0fede5be0bcd7` as the proposed reference baseline [S9–S12]. If the application uses another v6 patch, qualify patch-specific claims and consult that release. Do not automatically upgrade it.
3. For a conceptual question without a workspace, state the v6 assumption and proceed. Request exact versions only when they change the answer. For v5 or v7+, acknowledge the boundary and obtain relevant sources instead of silently treating it as v6.
4. For code-specific questions, inspect the selected form's factory, model, `formState`, type/wrapper registration, extensions, validators, and custom components as needed. A field named `address` or `repeat` is not automatically a built-in type.
5. Identify whether the input is a TypeScript field config, serializable application schema, or JSON Schema. Functions, Observables, and injected services cannot simply be put into a JSON payload. Treat dynamic behavior unavailable from supplied code as unknown.

## Build the knowledge base

Use an explicit source hierarchy: the consuming application's behavior and exact installed release; pinned upstream declarations/implementation/tests; official v6 guides/examples; finally issues and discussions corroborated against the release. Recent unversioned snippets are discovery leads, not v6 proof.

Create small knowledge records containing: topic, applicable versions, rule or explanation, source URL and commit/path, known caveats, recipe/test reference, and evidence status (`documented`, `source-checked`, `runtime-verified`). A source-checked record must not imply a passing runtime test.

| Knowledge area | First release contents | Later expansion |
| --- | --- | --- |
| Configuration/model | Keys and paths, groups, arrays, model versus control versus formState, defaults, reset | Deep factory composition and large-form analysis |
| Dynamic behavior | `expressions`, legacy callback differences, visibility, preservation, hooks, subscriptions | Performance investigation and complex async dependencies |
| Validation | Angular validator versus Formly expression contracts, messages, async/cross-field patterns | Application-specific error handling and server validation |
| Material | Existing module setup, common controls, wrappers, select values, custom types, datepicker prerequisites | Other UI adapters; Material-version-specific edge cases |
| Extension | Types, wrappers, registration and inheritance; recognize extensions/presets | Advanced extensions and detailed JSON Schema mapping |
| Debugging | Symptom-to-evidence paths, patch history, minimal reproductions | Curated real application incidents |

The actual Material API notes must be verified from the selected release's source/examples; the website route alone was insufficient [S8]. Do not assume every Angular Material input is exposed as a Formly `props` property. For dates and custom controls, inspect the application's adapters and value-accessor wiring.

Retain short original explanations and necessary examples rather than copying whole manuals. Preserve upstream attribution and required notices when reusing source [S22]. Keep private application rules in a project-owned overlay; only promote general lessons into the shared skill.

## Core diagnostic rules to encode

- Explain nested model scope before rewriting a path or expression.
- Differentiate hidden, disabled, readonly, removed-from-DOM, and excluded-from-submission behavior; inspect the relevant model/control values.
- Recognize supported deprecated v6 syntax. A request to understand or fix it is not automatically a migration request.
- Diagnose value loss, defaults, form reset, missing registrations, validation contracts, and change detection against the correct version.
- Preserve application factories and services. Do not evaluate supplied callbacks merely to explain a configuration; execute reproductions only in an appropriate test environment.
- Prefer public APIs. If a diagnosis depends on internals, identify that dependency instead of recommending an unexplained private API workaround.
- Separate a plausible diagnosis from a reproduced cause. For generated code, distinguish “checked against source,” “compiled,” and “behavior tested.”

These are proposed quality requirements; the evaluation must show whether the skill actually follows them.

## Retrieval, invocation, and agent use

Support explicit invocation as `$ask-formly` and normal discovery through a precise description, subject to the target host's skill support. Suggested description: “Explain, author, review, and debug Angular ngx-formly v6 configurations and custom field types, with Angular Material guidance and version-specific source checks.”

An invoking agent supplies the question, target versions, relevant field config/model/registrations, and expected behavior. The same agent then follows the skill. A separate specialist agent is optional orchestration, not required for v1. No separate service or model training is proposed.

Default retrieval is local curated notes, then exact-version official sources when needed. Context7 is optional and usable only when the returned evidence's version can be established [S17]. Offline answers should use the retained notes and disclose unverified gaps. Keep links resolvable without depending on a particular MCP provider.

Formly Contract can later supply an existing contract and diagnostics as additional evidence. Keep declared, scenario-resolved, and browser-observed behavior distinct. Do not make this tool a prerequisite or claim the skill provides its extraction/MCP capabilities [S18].

## Milestones and exit gates

Effort is an unvalidated planning estimate for one engineer with agent assistance, not measured delivery time. Assumes a usable target workspace, no infrastructure build, and common Material controls.

| Milestone | Deliverable and exit gate | Estimated focused effort |
| --- | --- | --- |
| M0: baseline and scope | Inspect target versions; define eight cases and expected behavior before testing; measure normal-agent and docs-pointer baselines | 0.5–1 day |
| M1: narrow prototype | Entrypoint, version notes, config/expressions/validation/Material notes, three recipes; pass the eight-case pilot | 1–2 days |
| M2: capability coverage | Complete required references and small fixture app; execute 24-case evaluation with held-out cases | 2–3 days |
| M3: package and field trial | Validate skill format/links/attribution; use on three real tasks; install in the chosen host only when requested | 0.5–1 day |

Total initial estimate: 4–7 focused days. Major cost drivers are source curation, fixture compatibility, and reviewing answers; a large document scrape is not the main work. No paid service is necessary for the proposed design; model usage remains dependent on the execution environment.

The first three recipes should cover a Material form with nested data and validation, conditional visibility with an explicit preservation requirement, and a custom registered Material-compatible type. Add dependent selects and repeaters when their behavior is tested. Do not claim all v6 patches or all Material versions are qualified by one fixture.

## Implementation handoff

Current destination: `ideas/ask-formly/skill/ask-formly/` for the authorized knowledge draft. A dedicated repository can later hold development fixtures and evaluation, with only the packaged skill installed or linked into the chosen agent environment. Do not edit shared AI Central targets. Repository creation, installation, and publication have not been requested.

First concrete task: inspect one consuming application's package/lock files and select eight realistic evaluation prompts, including one real config and one real bug. If no application is supplied, a synthetic pinned fixture can be used, with its compatibility assumptions explicit and rollout deferred until a real task is checked.

The complete [evaluation plan](validation.md) determines whether to expand the prototype. If docs pointers perform equally well, keep the smaller solution. Add a custom retrieval system only after retained failure evidence shows that local notes and exact-version source lookup are insufficient.

## Authorized indexing extension — implemented 2026-10-15

The owner requested a project-local static inventory and connection map. The [indexing guide](skill/ask-formly/references/project-indexing.md) now combines the scanner/AST graph with reviewed project/registry/inventory/form notes under `.agents/ask-formly/`. [Implementation boundaries and test plan](project-index-plan.md), [executed qualification](qualification/project-index/README.md). No new companion service or installed skill is required. The next gate is consuming-project coverage and measured E2E outcomes, not further generic corpus expansion.

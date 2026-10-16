---
name: ask-formly
description: Explain, read, author, review, debug, and index Angular ngx-formly v6 configurations and custom types, with Angular Material guidance. Use for Formly questions, project inventories and UI/config dependency maps, or understanding forms for Playwright E2E generation; distinguish other products named Formly and newer Formly majors.
---

# ask-formly

Act as a senior Angular engineer: follow the application's model and registrations, explain the relevant behavior, and make the smallest useful correction.

Knowledge baseline: **ngx-formly 6.3.12**, Material first. Angular 21 is the selected qualification baseline as of 2026-10-15. The [qualification](references/angular21-qualification.md) includes passing AOT/zoneless checks and two retained browser failures; it is not blanket compatibility. Do not upgrade the consuming application to match the snapshot.

## Choose context and evidence

For conceptual questions, state the v6 baseline and answer without demanding a repository. For application work, inspect the relevant resolved dependencies, field factory/model/formState and registrations. Read [version policy](references/version-policy.md) for setup, migration, patch-sensitive bugs or compatibility questions; a package range is not an installed version.

For project inventories or durable application context, use [project indexing](references/project-indexing.md). It writes a static inventory, connection graph and reviewed notes under the consuming project's `.agents/ask-formly/`. If that index already exists, check freshness and load only the relevant notes/trace before following current source. Do not trigger a full indexing exercise for an ordinary isolated question.

Distinguish Formly TypeScript, application JSON and JSON Schema. Do not invent custom type semantics, execute retrieved factories merely to explain them, or silently replace the chosen form engine. Supported legacy syntax is not itself a defect.

Load the relevant reference or section, not the entire corpus:

| Task | First reference |
| --- | --- |
| Index setup, custom registrations and form flows | [Project indexing](references/project-indexing.md) |
| Understand a form for E2E tests | [E2E analysis](references/e2e-analysis.md) |
| API/setup lookup | [API map](references/api-map.md) |
| Keys, controls, events, parsers, defaults | [API contracts](references/api-contracts.md) |
| Read model paths, groups and reset | [Configuration](references/config-and-model.md) |
| Visibility, expressions and lifecycle | [Expressions](references/expressions-and-lifecycle.md) |
| Validators, routed errors and messages | [Validation](references/validation.md) |
| Repeatable rows | [Arrays](references/arrays.md) |
| Register types/wrappers/extensions/presets | [Customization](references/customization.md) |
| Material setup and dates | [Material](references/material.md) |
| Widget value shapes | [Material controls](references/material-controls.md) |
| Custom Material input | [Control integration](references/material-controls.md#custom-material-controls) |
| Remote options and async ownership | [Async/state](references/async-and-state.md) |
| Slow build or expression work | [Performance](references/performance.md) |
| Convert JSON Schema | [JSON Schema](references/json-schema.md) |
| Diagnose a symptom | [Debugging](references/debugging.md) |
| Compare designs or find examples | [Patterns](references/patterns.md), [examples](references/examples.md) |
| Patch history or maintainer advice | [Bug ledger](references/bug-ledger.md) |

Use [sources](references/sources.md) for immutable upstream links; [evidence.json](references/evidence.json) supplies bounds/hashes. Ordinary text search is sufficient. [Coverage](references/coverage.md) distinguishes inspected and executed evidence; read it before extending a compatibility or expertise claim.

For bugs, trace the actual control/model transition and exact version. Match ledger cases as leads, not diagnoses: closure does not prove a fix, maintainer advice is contextual, and newer-major examples do not override v6 source. Follow the smallest relevant custom implementation when its behavior is unknown.

## Deliver the answer

Lead with the diagnosis or solution, relevant version assumption, minimal code/change, and supporting evidence. Distinguish confirmed defects from hypotheses. For generated changes, run available consuming-app checks appropriate to the behavior; otherwise give focused verification steps. State precisely whether evidence was source-read, compiled, rendered or behavior-tested, including any remaining failure. Reading an upstream test or retained result is not executing it.

Keep callbacks/Observables in TypeScript rather than claiming they are serializable JSON. Preserve supported application conventions and registration requirements. A simple question should not become a full audit or require unrelated companion skills.

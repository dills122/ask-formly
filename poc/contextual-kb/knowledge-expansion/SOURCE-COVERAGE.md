# Remaining library-source coverage inventory

**Current status (2026-10-25):** the original inventory below was prepared at the 46-fact stage and is retained as history. The installed foundation now has 64 facts. Extensions/presets has a repaired 70-fact candidate that passed frozen qualification and independent review; the first mixed-adapter candidate failed runtime eligibility and remains recorded. The current source-by-source decisions are in [the reviewed checklist](source-ledger/CHECKLIST.md), with [repeatable commands](admission/RUNBOOK.md) and [broader-source priorities](source-ledger/NEXT-SOURCES.md).

Prepared during custom-types qualification; results are now complete. This is a source-section inventory and proposed sequence, not authorization to promote any DB or a claim that later batches passed.

## What “existing compiled source” currently contains

The preserved import manifest names **three imported guides**: configuration/model, expressions/lifecycle, and customization. The POC corpus also contains two supplemental source notes (custom-type use and initial values), an evidence index and catalog. The accepted authored input has nine documents/46 facts, drawing on both imported/supplemental material and retained original reference paths.

The retained `skill/ask-formly/references/` directory is broader than those three imported guides. It contains library material such as validation, arrays, Material controls and JSON Schema, but also retired application-inspection workflows and historical qualification reports. File presence is not proof of ingestion, authored fact coverage, or runtime qualification. Do not automatically import that whole directory.

## Finish the already imported library guides first

| Group | Existing authored support | Remaining source sections to verify and turn into a bounded batch |
| --- | --- | --- |
| Custom types / registration | Broad alias, inheritance and wrapper concepts | Isolated custom-types-v1 adds ten facts and strongly improves support, but failed the per-repeat end-to-end gate. See custom-types-v1/RESULTS.md and FINAL-REVIEW.md; not installed. |
| Configuration and model scope | Shared formState, key shapes, props, defaults/resets, initial values | Fields/model/Angular-control distinctions; keyed versus keyless groups; leaf field.model versus scalar value; runtime links on built fields. Verify K01/K05/K09 before drafting. Do not re-author existing default/reset claims just to increase count. |
| Expression values and notifications | Modern/legacy callback arguments, hide/disabled behavior, default expression check setting, checkExpressions/detectChanges and managed onInit returns | String-expression bindings; direct Observable expression behavior; formState change observation; expressionChanges event shape. Verify K01/K07/K11/K25/K29 and distinguish source-read tests from executed tests. |
| Extensions and presets | Custom types/wrappers mostly covered; no dedicated extension/preset fact group | Extension build phases and priority; bounded idempotent-addon example; preset module/reference/provider contract and substitution timing. Verify K03/K06/K23/K24/K35/K44/E06. Avoid claiming arbitrary extension reruns or recursive presets are qualified. |

Small batches should follow actual gaps, not a target fact count. Existing qualifications in source quotes may already support an answer even if the short claim does not name the detail; compare semantic evidence before deciding an addition is needed.

## Broader retained library references, later

After the imported-guide coverage is qualified, inspect validation/message contracts, arrays/repeat operations, Material control specifics, and JSON Schema separately. Each requires explicit scope/evidence review and a candidate comparison. No completeness claim follows from one successful group. Retired indexing, application inspection, supplier examples, old local-MCP workflows and evaluation artifacts are excluded from library knowledge ingestion.

## Repeatable group gate

For each group: source-to-fact gap inventory → exact pinned evidence review → isolated authored/catalog inputs → explicit-path candidate compilation preserving prior accepted rows → real-agent MCP comparison and matched-plan diagnostics → independent result audit. Preserve the installed DB and model assets throughout. Additional groups may build on a successful isolated candidate only after its outcome is reviewed; never silently replace the installed DB.

Finalization means every in-scope imported-source section is mapped to supported authored claims or an explicit exclusion/unresolved item, with provenance and representative regression coverage. It does not mean every Formly API, application scenario or future version is covered.

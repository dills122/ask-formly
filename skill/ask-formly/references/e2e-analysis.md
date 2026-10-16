# Formly analysis for an E2E builder

Proposed workflow, not yet evaluated on a consuming project. The E2E builder owns authentication, fixtures, browser inspection, test code and execution; ask-formly supplies focused behavioral interpretation.

## Trace only the requested scenario

Start from the route and acceptance requirement. Follow field factories/helpers, registrations/inheritance, relevant wrappers/custom renderers, expressions/hooks, option services and submission mapping. Stop when the scenario's controls, prerequisites and outcome are explained; expand unresolved dependencies, not every Formly file. Custom type names do not identify their behavior.

Reuse project-owned summaries of shared registrations/helpers with source paths and revision stamps. Revalidate changed dependencies and scenario context (permissions, mode, locale); don't copy private forms into the generic skill or treat cached conclusions as current facts.

If `.agents/ask-formly/` exists, follow [project indexing](project-indexing.md) to check freshness, then load the requested form/shared notes and a bounded connection trace. The static map accelerates navigation; candidate edges do not prove injector resolution, runtime state or accessible locators. Build or expand that index when requested, keeping an isolated E2E task scoped to its scenario.

## Return a compact handoff

For relevant fields only, supply:

| Item | Required distinction |
| --- | --- |
| Identity | Model path, renderer and source location; a key is not a DOM locator |
| State | Initial value, visibility/enabled/required conditions and triggering user actions |
| Data | Valid/invalid examples grounded in constraints; option label versus stored value |
| Readiness | Observable UI condition after options/validation settle; unresolved async dependency |
| Outcome | Visible validation, reset/retention, submission transformation and acceptance assertion |
| Evidence | Source-derived, browser-confirmed or unknown; next targeted check |

Include action order and locator candidates for browser verification. State blocked conclusions rather than inventing runtime labels, selectors, values or business rules. Source behavior explains implementation; acceptance requirements determine correctness.

## Formly-specific traps

- Trace keyed/group/array model scope and payload mapping; form values and submitted model can differ. [Configuration](config-and-model.md)
- Distinguish hidden, absent, disabled and readonly; conditional fields may reset values or unregister controls. [Expressions](expressions-and-lifecycle.md)
- Find the error-display trigger, not just the validator. [Validation](validation.md)
- Resolve native versus Material/custom selects, label/value mapping, overlays and date adapters. Confirm overlay scope in the browser; do not assume a popup belongs inside the field DOM. [Controls](material-controls.md)
- Scope repeated labels to an identified row; indices can change after deletion. [Arrays](arrays.md)

Prefer confirmed accessible roles/labels or existing test IDs; don't derive generated IDs from model keys. Use observable readiness assertions instead of fixed delays. Playwright's actionability checks do not establish business-data readiness. See official [locators](https://playwright.dev/docs/locators) and [auto-waiting](https://playwright.dev/docs/actionability), accessed 2026-10-15, publication dates unspecified.

Keep E2E interactions through the application's UI and established fixtures. Patching Formly models/controls directly bypasses the user behavior being tested.

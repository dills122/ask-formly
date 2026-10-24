# Knowledge-base construction

Updated: 2026-10-15. The owner authorized building the source-backed knowledge base and investigating useful companion mechanisms. Keep the first artifact in this idea folder; do not install, commit, publish, or modify shared skills.

Budget and stopping rule: one construction pass through the listed topic areas, ten selected official example walkthroughs, and two external project checks. Stop this milestone when the portable notes/catalog pass source/structure checks and coverage gaps are recorded. Full runtime qualification follows the separately budgeted evaluation plan.

## Phases

- [x] Acquire the pinned v6.3.12 source and inspect API, implementation, tests, docs, and examples.
- [x] Create a portable draft skill with focused knowledge references and source provenance.
- [x] Add a searchable evidence/example catalog and assess companion mechanisms.
- [x] Validate citations, links, source pinning, catalog lookup, and skill structure; record coverage limits.

## Acceptance

Cover model/configuration, lifecycle/expressions, validation, arrays, extension points, Material, JSON Schema, and debugging using exact upstream evidence. Each material behavior must have a precise source reference. Distinguish upstream tests read from tests run. Include official demo recipes and assess external projects without claiming untested examples are verified. No claim of a production-qualified expert until behavioral evaluation is performed.

## Decisions

Use upstream commit `5f099fddea6426b46a453866adf0fede5be0bcd7`. Keep a local source cache outside the distributable skill. Package concise original notes and a provenance catalog. Evaluate helpers against actual retrieval needs.

## Risks

Consuming Angular/Material version remains unknown. Documentation and source may disagree. Existing behavioral qualification plan remains future work; knowledge construction is now authorized independently of that rollout gate.

## Outcome

First source-backed knowledge milestone complete. See [coverage](skill/ask-formly/references/coverage.md), [companions](companions.md), and [verification](validation.md). Runtime qualification remains a separate next milestone.

## Deepening pass — 2026-10-15

Owner request: substantially deepen API, common patterns, best practices, anti-patterns, maintainer discussions, and real bugs, retaining v6 and Material as the boundary.

Decision question: which additional operational knowledge changes the skill's diagnoses and implementation choices, and how can each claim be traced to the baseline or a clearly identified version difference?

Budget/stopping rule: inspect the remaining core public contracts and Material control surfaces, search across performance, async dependencies, validation, arrays, lifecycle, custom controls, and JSON Schema; retain approximately 15–25 relevant issue/discussion cases and a practical pattern catalog. Follow concrete source conflicts to resolution. Complete when each retained lesson has version/evidence boundaries, source links, a diagnostic or construction implication, and a verification scenario; avoid padding with generic Angular advice. This is a deeper corpus milestone, not a claim of universal expertise.

- [x] Expand primary source coverage and read maintainer conversations, issue bodies/comments, and linked fixes.
- [x] Build API contract details, practical patterns/anti-patterns, and a version-aware bug ledger.
- [x] Integrate focused routing and richer Material, async, performance, and custom-control guidance.
- [x] Validate evidence, links, package structure, and representative knowledge use; update coverage and handoff.

Deepening outcome: 83 pinned evidence records across 74 files, 13 example walkthroughs, 24 practical patterns, 25 issue cases with 85 comments, four inspected fix diffs, and 17 passing custom runtime probes. The portable skill and source/link/hash checks pass. Next: real-browser/AOT qualification on a declared stack and the separate agent-quality comparison; the consuming application remains unspecified. See [verification](validation.md) and [executed behavior](skill/ask-formly/references/runtime-evidence.md).

## Angular LTS requirement — 2026-10-15

- [x] Verify current official LTS status and package versions; choose Angular 21 minimum.
- [x] Preserve Angular 18 historical artifacts, update pinned fixture to Angular 21.2.25 / Material/CDK 21.2.14, and rerun existing probes.
- [x] Record 17/17 passing results with explicit Zone.js change detection; update skill policy, provenance, and current planning records.

Stopping rule: existing meaningful probes rerun on the supported target, truthful compatibility boundaries retained, current package and evidence internally consistent. Zoneless, browser/AOT, and agent evaluation remain separate qualification work.

## Zoneless, browser, and AOT qualification — 2026-10-15

User authorized execution on Angular 21, Formly v6 and Material. Keep the Zone-based results intact. Build a separate reproducible fixture with pinned dependencies, strict Angular templates/AOT, and actual Chromium interaction. Test zoneless scheduling without manual detectChanges after actions; include native input, async expressions/options/validation, visibility, custom types, arrays, submit/reset and Material overlay/date behavior. Establish expected outcomes before execution. Preserve failures and targeted follow-up checks; do not monkeypatch Formly internals to manufacture compatibility.

- [x] Qualify representative zoneless scheduling in JIT and browser.
- [x] Compile a strict-template AOT application and run meaningful browser interactions on its emitted bundle.
- [x] Investigate observed failures; retain exact scope, evidence and fixes or unresolved limits.
- [x] Integrate lessons into ask-formly and validate package, citations and artifacts.

Stop when all three requested layers have actual results, each observed failure is classified with evidence, and lessons/remaining limits are recorded. This is scoped compatibility qualification, not exhaustive browser, schema, accessibility or performance certification.

Qualification outcome: 17/17 zoneless probes pass; strict AOT and its negative control pass; Chromium 12/14 pass with two retained select failures and a verified close/reopen recovery. Completed execution/knowledge milestone; a full compatibility pass is not claimed. See [results and reproduction](qualification/browser/README.md).

## Agent comparison and skill refinement — 2026-10-15

User authorized realistic question/debugging comparison against an agent without ask-formly. Use [the frozen two-arm protocol](evaluation/2026-10-15-pilot/protocol.md); preserve prior three-arm/release-gate plans as unrun.

- [x] Freeze eight tasks/rubric and skill snapshot; run 16 fresh-context answers with equal sources/settings.
- [x] Compile/exercise authoring outputs; independently score masked answers and identify actual gaps.
- [x] Apply focused skill changes and run fresh variants for the affected cases.
- [x] Validate artifacts, report comparative results and limits, and update current status.

Outcome: 8/8 passes and 10/10 mean in both arms; no demonstrated comparative advantage. Both authored forms passed strict AOT and three browser scenarios. Six focused behavior/stream checks and two fresh skill variants passed. Added tested nuances without new helper infrastructure. Next: unseen consuming-project trials; [report](evaluation/2026-10-15-pilot/README.md).

## Independent audits and blind challenge pass — 2026-10-15

User requested additional audits, blind testing and useful expansion without bloat. [Protocol](evaluation/2026-10-15-audit/protocol.md):

- [x] Freeze skill and measure size; independent source-accuracy and bloat audits.
- [x] Source-only designer creates six new tasks/criteria; run paired fresh agents and masked review.
- [x] Verify material findings with focused source/runtime checks, retain only justified changes and trim repetition.
- [x] Retest affected topics, validate provenance/links/size, update current status.

Outcome: both arms 5/6 and 57.5/60; five verified corrections, six focused probes, three fresh variants, preserved original H05 compile failures, and smaller Markdown context. [Audit report](evaluation/2026-10-15-audit/README.md).

## E2E use-case reframing — 2026-10-15

- [x] Record the workplace-scale use case and distinguish user-reported context from inspected facts.
- [x] Add concise scenario-driven Formly interpretation guidance for the invoking Playwright builder.
- [x] Define a paired source-to-test evaluation with meaningful outcome/repair/time metrics.
- [ ] Execute that evaluation on representative consuming-project forms; requires an authorized workspace/reproduction and usable test environment.

At that milestone no scanner was built; the subsequent authorization and implementation below supersede that boundary. [Current workflow](e2e-use-case.md).

## Project indexing — 2026-10-15

- [x] Specify static files, discovery, source freshness, questions and reviewed-note workflow.
- [x] Build/test Python inventory and TypeScript AST connections without executing application code.
- [x] Add root/feature/provider registrations, custom implementation links, UI bindings, config/helper dependencies and bounded traces.
- [x] Review correctness independently and add regression tests for scope identity, assignments, Git symlinks, spread overrides and keyless fields.
- [x] Add skill routing and a project-local indexing guide; retain a synthetic example and validation evidence.
- [ ] Exercise the index in the consuming admin system and measure source-to-E2E effectiveness.

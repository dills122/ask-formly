# ask-formly — a Formly v6 expert skill

- Status: ready
- Created: 2026-10-15
- Updated: 2026-10-15
- Owner / decision owner: repository owner
- Decision question: Should we adopt, adapt, or build a skill that reliably explains, authors, reviews, and debugs Angular ngx-formly v6 configurations?
- Research budget: one bounded deep web research pass, approximately 30 targeted search queries plus primary-source inspection; extend only to resolve a decision-changing candidate or version conflict.
- Stopping rule: cover dedicated skills, adjacent Angular skills, documentation retrieval, and official v6 documentation/source; identify a credible reuse/build recommendation, version hazards, and a testable construction plan. Search absence is not proof of nonexistence.

## Problem and intended user

The owner wants developers and coding agents to invoke `ask-formly` for feature questions, configuration reading, new configuration generation, and debugging. The proposed expertise starts at ngx-formly v6, with a senior Angular engineer's judgment. Angular Material is the first UI adapter, confirmed by the owner on 2026-10-15. The consuming application's Angular version and exact Formly patch are unknown.

The owner clarified the primary workflow: an eventual workplace E2E builder should use ask-formly to understand a large existing admin application quickly and generate correct Playwright tests with little repair. User-reported scope is 100+ forms and roughly 200–500 Formly files accumulated over years, with multiple implementation styles. These figures and conventions have not been independently inspected. See the [E2E use case and next evaluation](e2e-use-case.md).

## Scope and evidence standards

The owner subsequently authorized source-backed knowledge construction on 2026-10-15. Build the draft inside this idea folder; do not install it, change shared skill targets, commit, or publish. Prefer official versioned docs, tagged upstream source/tests and package metadata, then original skill repositories. Search listings are leads, not proof of capability. Compare an existing skill, an adapted Angular skill, a new focused skill, docs retrieval alone, and the current manual approach.

The deliverables are the research packet and a portable knowledge draft with focused references, pinned evidence, example walkthroughs, and companion-mechanism recommendations. Distinguish documented facts, observations, inference, and untested proposals.

## Current position and next action

Newly authorized and implemented: [project indexing](skill/ask-formly/references/project-indexing.md) writes a scoped inventory, static connection graph and reviewed notes to the consuming project's `.agents/ask-formly/`. It maps candidate setup/registrations, source locations, naming families, screens, config initialization, sub-configs and custom implementations. Synthetic discovery/graph tests and independent review are retained in [index qualification](qualification/project-index/README.md). Dynamic construction, injector precedence and browser behavior remain explicit review boundaries. Next: use it on the authorized admin workspace, classify the complete candidate inventory, and measure the E2E workflow; no workplace files have been inspected.

Owner requirement: Angular LTS or newer; selected minimum qualification baseline is Angular 21 LTS with Material/CDK 21. Angular 18 results are historical only. Recheck support status when refreshing the fixture.

Recommend building a small, version-aware `ask-formly` skill using upstream knowledge, with Angular Material first. No general-purpose v6 Formly expert skill was verified in the bounded search. Existing Angular skills, an application-specific Formly testing skill, Context7, and Formly Contract are useful adjacent work, with different scopes. This is a build recommendation, not a claim of validated effectiveness.

Use v6.3.12 as the proposed reference snapshot, while answering against the consuming application's actual version. The npm registry identifies v6.3.12 as the newest published stable v6 patch at access time [S9]; its upstream source commit is recorded in [sources](sources.md). Do not upgrade a consuming application merely to match the reference snapshot.

The [knowledge draft](skill/ask-formly/SKILL.md) now contains 84 pinned source records across 74 files, 24 practical patterns/anti-patterns, 25 issue cases with 85 comments inspected, four reviewed fix patches, and thirteen official example walkthroughs. Seventeen custom behavior probes passed on Angular 21.2.25 / Material 21.2.14 with Formly 6.3.12 under JIT TestBed/jsdom. Two probes characterize important limitations: debounce bypassing a parser and falsy array initial values falling through to defaults.

Follow-up: 17/17 zoneless probes and strict AOT pass; 12/14 Chromium cases pass. The two select-option replacement failures reproduce with bare Material; close/reopen recovery passes. See [qualification](qualification/browser/README.md). The two-arm [agent pilot](evaluation/2026-10-15-pilot/README.md) is now complete: both arms passed 8/8 at 10/10 average, with no demonstrated comparative advantage. Both authored forms passed AOT and browser checks; three tested migration/parser/request-lifetime lessons were added, and two fresh variants passed. The [additional audit](evaluation/2026-10-15-audit/README.md) is complete: independent accuracy/bloat reviews and six fresh blind challenges; both arms pass 5/6 (57.5/60), with a shared TypeOption import failure. Five verified corrections were integrated and three fresh variants passed; that audit reduced the entrypoint by 37% and Markdown by 2.5%. The subsequent E2E reframing adds one conditional analysis reference. Next: evaluate source-to-Playwright tasks on representative existing forms, measuring meaningful first-run passes, repair cycles and total time, including the select boundary where relevant. Inspect the consuming application's exact versions before making application-specific compatibility claims. See [coverage](skill/ask-formly/references/coverage.md) and [probe results](qualification/README.md).

- [Research and alternatives](research.md)
- [Search coverage and limitations](search-log.md)
- [Knowledge draft](skill/ask-formly/SKILL.md) and [coverage](skill/ask-formly/references/coverage.md)
- [Companion mechanisms](companions.md)
- [Construction plan](plan.md)
- [Validation design](validation.md)
- [Risks](risks.md)
- [Decision](decisions.md)
- [Sources](sources.md)

The portable draft and a pinned development probe are present; the skill has not been installed. Scoped real-browser/AOT qualification is complete with a retained limitation; both development comparisons are complete with tied results; original failures and separate repairs are retained. Broad or held-out effectiveness is not established. Construction and runtime verification are recorded in the validation document.

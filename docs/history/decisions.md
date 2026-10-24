# Decisions

## 2026-10-15 — Recommend a focused prototype

**Status:** build recommendation with an actionable plan; implementation not started. Decision owner: repository owner. The owner requested research and planning and selected Angular Material as the first adapter.

**Decision question:** adopt, adapt, or build a v6 ngx-formly expert skill?

**Recommendation:** build `ask-formly` as a concise skill with selectively loaded v6 references and tested examples. Use the official v6 material and a pinned source snapshot; retain the consuming application's actual versions as the authority for task-specific advice. Treat the “senior Angular engineer” persona as observable engineering behavior.

**Evidence:** no general-purpose expert skill was verified within the recorded public search. The original Analog forms skill is unmaintained and excludes Formly [S15]; Angular's official skills are general framework guidance [S14]. OpenEMS supplies a real but application-specific Formly testing skill [S16]. Context7 provides documentation listings without a verified v6 retrieval boundary [S17]. Formly Contract is relevant extraction tooling, not a shipped expert/MCP service [S18]. The v6 docs/types/changelog expose sufficient material to construct a bounded knowledge base, and documented inconsistencies make verification important [S3–S6, S9–S12].

**Tradeoffs:** custom curation introduces maintenance, but avoids coupling the requested expertise to a different form engine, broad Angular defaults, or a service dependency. A small prototype is reversible and can be reduced to a docs-pointer guide if it fails the baseline comparison.

**Deferred:** multiple UI adapters; newer Formly majors; a custom MCP/RAG service; fine-tuning; automatic repository-wide extraction; mandatory Formly Contract integration; exhaustive JSON Schema/extension coverage. No claim of full v6 compatibility or improved answer quality is made yet.

**Next gate:** execute the eight-case pilot described in [validation.md](validation.md) when implementation is requested. Inspect the actual application's Angular/Material/Formly versions before runtime fixture selection. The [plan](plan.md) includes package structure, milestones, and acceptance criteria.

**Would change this recommendation:** a maintained, inspectable v6 expert skill with relevant tests; baseline results showing no useful gain; inability to reproduce required behavior on the target stack; or a material retrieval limitation that warrants a different architecture.

Source register: [sources.md](sources.md). Search limits: [search-log.md](search-log.md).

## 2026-10-15 — Build the source-backed knowledge draft

**New authority:** the owner requested construction of a knowledge base from the API, docs, demos, and examples, with investigation of companion mechanisms. This supersedes the earlier research-only scope for knowledge construction. Installation, publication, and shared-skill changes remain outside this request.

**Result:** created [ask-formly](skill/ask-formly/SKILL.md), twelve focused knowledge/coverage references, a 51-record evidence manifest with immutable source links and file hashes, ten official example walkthroughs, attribution, and discovery metadata. The baseline is v6.3.12 at `5f099fddea6426b46a453866adf0fede5be0bcd7`. The full source cache remains outside the portable package.

**Evidence that refined the approach:** selected implementation/tests reveal distinctions easily lost in summary docs: callback/validator contracts, Material secondary modules, nested datepicker options, and JSON Schema registrations. Official examples also have adaptation cautions. Current external designer and historical fluent-builder projects use other Formly majors. See [findings](findings.md) and [companions](companions.md).

**Decision:** keep a single entrypoint with task-specific notes and plain-search retrieval. Use a development fixture as the next companion mechanism. Defer separate helper skills and a custom retrieval service until concrete repeated needs justify them.

**Quality boundary:** source pinning, hashes, link targets, skill structure, metadata, and eight topic lookups passed construction checks. No Angular build, browser behavior test, or comparative answer evaluation was performed. The draft is useful retained knowledge, not a qualified expert or proof of improved answers.

**Next gate:** select the application or declared synthetic dependency stack, qualify three executable recipes, and run the eight-case comparison already designed in [validation.md](validation.md). Keep exact held-out prompts/answers out of authoring. Current source coverage does not complete the broader M0–M3 qualification milestones.

## 2026-10-15 — Deepen operational expertise and characterize behavior

**New authority:** the owner requested substantially deeper API, patterns, anti-patterns, maintainer conversations, and real bugs. This authorizes the broader corpus before the previously proposed answer-comparison gate; it does not establish that gate's outcome.

**Result:** expanded to 83 pinned records across 74 files, 19 focused topic/coverage references, 13 official example walkthroughs, 24 practical patterns, and a 25-case issue ledger informed by 85 comments and four inspected fix diffs. Added a development fixture with 17 executed probes on the declared synthetic Angular/Material 18.2.14 and Formly 6.3.12 stack.

**Evidence that changed guidance:** parser/debounce interaction and falsy array initialization are now reproduced limitations. Patch history separates initial formState performance changes from a later observation correction. Closed issues and community suggestions now have explicit evidence/version boundaries. Material value shapes, custom-control contracts, JSON Schema limits, and event ownership have detailed source-backed guidance.

**Decision:** retain one small routing skill with selectively loaded evidence. Use the fixture as the first companion mechanism, keeping dependencies outside the portable skill. No additional helper skill or retrieval service is justified yet. Treat source-read, issue-reported, patch-inspected, and runtime-observed knowledge as different evidence levels.

**Limits and next gate:** this is a substantially deeper knowledge artifact, not a claim of universal expertise or measured answer-quality improvement. Browser/AOT, dates, network races, broader arrays/schema scenarios, the consuming stack, and comparative skill evaluation remain to qualify. See [coverage](skill/ask-formly/references/coverage.md) and [validation](validation.md). No installation, commit, or publication was performed.

## 2026-10-15 — Raise the Angular qualification baseline to LTS

The owner requires Angular LTS or newer. Verified Angular's official support schedule: 21 is the newest LTS major, 22 is active, and 18 is unsupported. Selected Angular 21 as the minimum qualification baseline; this supersedes the earlier synthetic Angular 18 choice, while preserving that run under qualification/historical/angular18.

Resolved and pinned Angular 21.2.25, Material/CDK 21.2.14 and Zone.js 0.15.1. Formly remains 6.3.12. All 17 existing probes passed again using explicit Zone.js change detection under JIT TestBed/jsdom; runtime stderr was empty. The probe now obtains version labels from installed package metadata. No forced dependency resolution was needed.

Updated the skill version policy, runtime evidence/hashes, current fixture/lock, brief, index, and planning references. Angular 21 defaults to zoneless, which remains unqualified by this explicitly Zone-based run. Browser/AOT and agent comparisons remain outstanding. Sources and exact scope: [version policy](skill/ask-formly/references/version-policy.md), [fixture](qualification/README.md).

## 2026-10-15 — Qualify zoneless, AOT and Chromium with an explicit select limitation

The owner authorized zoneless and real-browser/AOT execution on Angular 21 while retaining Formly v6 and Material. Built a separate pinned fixture, preserving the Zone-based results. Seventeen zoneless JIT/jsdom probes pass without Zone.js or manual fixture.detectChanges. The optimized AOT build passes strict TypeScript/templates with skipLibCheck false; an intentionally invalid FormControl input fails TS2322 and source is restored. Emitted build inputs include neither Zone.js nor the runtime Angular compiler.

Chromium 156.0.8078.4: **12/14 cases pass**, zero skips/retries. B06/B13 fail keyboard selection after replacing the sole active option while the panel is open, in both Formly and bare Material. Diagnostics retain focus and a stale active-option reference in the Formly case; installed CDK/Material source supports the mechanism. B14 verifies close/reopen recovery. This is not an unconditional compatibility pass, nor proof of a zoneless-only defect. No upstream package patch or dependency-major migration was made.

Decision: retain the two failing regressions, document a narrow verified recovery, and include the actual boundary in ask-formly. Source corpus now has 84 records across 74 files; the new Angular 21 reference routes compilation, runtime and failure evidence. Broader browsers/adapters/HTTP/SSR and agent-quality comparison remain separate work. [Fixture and raw results](qualification/browser/README.md), [skill lessons](skill/ask-formly/references/angular21-qualification.md).

## 2026-10-15 — Retain the skill after a tied development pilot

The user authorized testing realistic questions/debugging against an agent without ask-formly and folding findings back into it. Ran 16 fresh answers on eight predeclared cases, equal pinned source access and inherited model/settings, plus independent partially masked review. Both arms passed 8/8 with 10/10 means and no critical failures. Both authored forms passed unchanged strict AOT and three browser scenarios. Tool counts are self-reported and do not establish efficiency improvement.

Decision: retain the portable draft and make focused evidence-backed improvements, but do not claim superiority or justify a retrieval service/additional companion skills. The pass portion of the pilot gate passed; useful comparative advantage was not established. Added disabled-expression migration caveats, visible parser write-back/draft normalization, and immediate request invalidation/cleanup. Three supplemental zoneless and three virtual-time checks passed; two new skill variants passed source-based assessment. These are development refinements, not held-out validation.

Next evaluation should use unseen consuming-project tasks and independently measured costs/repeat trials. The prior three-arm/full-release gate remains unrun, and the broader browser suite still has its two select failures. [Protocol, results and retained artifacts](evaluation/2026-10-15-pilot/README.md). No installation, staging, commit or publication.

## 2026-10-15 — Accept narrow audit corrections; keep the skill compact

Owner authorized further independent/blind audits. Accept the routed-error cleanup correction, JSON pattern/structured-enum/scalar-composition boundaries, and the public registration-type fix. Each has pinned source and focused execution evidence; the typeless anyOf fallback is source-only. Both blind arms scored 57.5/60 with 5/6 passes, so no advantage claim is warranted. Original compile failures remain visible after separate repairs and fresh retests.

Shorten routing and remove repeated explanations; keep detailed evidence outside the portable skill. Do not add companion skills or retrieval infrastructure without a demonstrated need. The entrypoint is 37% shorter and Markdown 2.5% smaller; optional provenance adds 0.4% package bytes. Next evidence should come from unseen consuming-project tasks, not arbitrary corpus expansion. [Audit report](evaluation/2026-10-15-audit/README.md).

## 2026-10-15 — Prioritize understanding existing forms for E2E generation

New user context changes the primary success criterion: the skill should help an eventual workplace Playwright builder understand 100+ forms / approximately 200–500 Formly files across mixed historical implementations. These are owner-reported estimates, not inspected source facts. Keep the existing v6/Material knowledge; add one conditional source-to-test reference and a project-owned context recommendation. Do not require separate agents or new retrieval infrastructure.

Prior knowledge audits establish useful mechanics, not reduced E2E repair effort. The next proposed trial starts from routes and acceptance requirements, with paired builder runs and measured first-run meaningful pass rate, repair cycles, total time and false positives. Keep app requirements separate from inferred implementation behavior. [Workflow and proposed gates](e2e-use-case.md). No workplace integration or new runtime trial was executed.

## 2026-10-15 — Build a project-local inventory and connection map

The owner explicitly authorized indexing and clarified that the goal is a full inventory/flow map: Formly entry points, custom registrations and implementations, config locations/naming families, and UI/initialization/sub-config/helper connections. This supersedes the earlier recommendation to defer a scanner. Keep it within ask-formly rather than adding a separate skill or service.

Implemented a scoped Python inventory and optional TypeScript AST analyzer, plus a workflow for source-reviewed `.agents/ask-formly/` notes and targeted user questions. Source fingerprints, tool/settings identity, bounded queries and preserved-but-invalidated notes support reuse. Static registration candidates retain scope identity; no injector winner or runtime behavior is invented. Twenty-five tests pass, including 500-form fixtures; independent review defects were fixed with regressions. [Qualification and retained example](qualification/project-index/README.md).

The tool provides discovery and source navigation, not an automatically complete semantic model. The agent must classify the inventory, resolve consequential static gaps and preserve dynamic unknowns. No workplace source has been inspected and no E2E efficiency advantage is claimed. Next: use the authorized consuming workspace and measure useful coverage and source-to-test outcomes. No installation, staging, commit or publication.

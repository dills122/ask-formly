# Custom types and registration: first knowledge expansion

Status: isolated build, comparison, preservation checks and final review complete. Knowledge gain confirmed; end-to-end gate failed in repeat2. No promotion or follow-on candidate build. Earlier plan-review checkpoint below is retained as history.

## Scope

The user's 24 October 2026 request authorizes a separate coverage inventory and proposed first knowledge batch, followed by plan review before a candidate DB build. This narrowly supersedes the historical question-layer-only restriction in STEERING.md for proposal artifacts only. Active authored records, corpus/catalog, compiler, runtime, installed DB, models, and sealed evaluation remain unchanged. All new artifacts stay in this directory inside the POC. No application inspection or runtime code is imported.

## Phases

- [x] Inventory all 46 current claims and map relevant coverage to requested capabilities.
- [x] Verify proposed additions against immutable Formly 6.3.12 upstream sources.
- [x] Draft a bounded batch with claims, conditions, limitations, source quotations and existing-fact relationships.
- [x] Define development requests, candidate-build prerequisites and comparison criteria.
- [x] Run artifact consistency checks and a fresh-context independent plan/source review.
- [x] Report findings and stop before DB construction.

## Acceptance

Distinguish existing support, partial support and absent authored support; source presence alone does not mean retrievable fact coverage. Avoid duplicate claims. Preserve core/Material and source-inspection/runtime-proof distinctions. New claims require exact pinned source evidence. Candidate-build instructions must use explicit separate input/output paths and preserve the complete accepted 46-fact baseline. Existing sealed evaluation is excluded.

## Authorized build/comparison continuation

User subsequently authorized isolated candidate construction and MCP comparison, followed by independent review, and conditional iteration on further knowledge groups. Installed DB promotion is still excluded.

- [x] Implement isolated runner with safety tests; review before building.
- [x] Build candidate; preserve all accepted SQL rows/provenance and hashes.
- [x] Implement real-agent MCP comparison, exact delivery audit and matched-plan replay.
- [x] Review qualification harness and fix failure accounting gaps.
- [x] Complete initial 16-case development comparison on both DBs and independent semantic assessment.
- [x] Apply development gate, freeze reviewed experiment, run 30-case qualification three times per arm.
- [x] Run matched-plan replay, retain failures in denominators, diagnose gains/regressions/latency.
- [x] Obtain final independent result review. Failed qualification prevents the conditional next build; source inventory/proposal prepared only.

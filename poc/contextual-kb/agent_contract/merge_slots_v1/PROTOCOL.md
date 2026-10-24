# Eight-slot combination experiment

The user explicitly authorizes an isolated result-combination experiment. This extends the earlier question-only boundary for this new harness alone. No existing merger, retrieval engine, candidate, model, knowledge or DB is edited. Evaluation stays sealed (hash only). No training, GLiNER inference, evidence answerer, corpus changes or serving integration.

## Fixed policy and comparison

Three paired arms share identical fresh foundation and supplemental query rankings:

1. Foundation: existing merge_obligations over original hybrid top-eight lists, cap eight.
2. Current fusion: unchanged per-question RRF of original and contextual supplemental hybrid top-eight, cap eight; unchanged merge_obligations, cap eight.
3. Protected-six candidate: keep the first six IDs of the foundation packet, in order. Fill at most two remaining slots from the current-fusion packet in its order, skipping duplicates. If still short, fill from the remaining foundation IDs. If no distinct supplemental query was executed, return the foundation unchanged. Fewer than six originals means protect all available originals and fill free slots. Never return more than eight unique IDs or an ID outside executed query results.

Six is fixed before generation/results: reserve a clear majority while leaving two opportunities for new evidence. No parameter sweep, query-specific exception, gold-aware selection or later change to six. This cannot guarantee preserving every useful original fact: original positions seven/eight may be displaced. Measure that honestly. A zero-displacement eight-slot policy would simply retain the entire baseline packet and could not add a ninth fact.

Original/supplemental hybrid results are queried once per request and shared across arms to isolate combination. Foundation-only logical query count excludes supplements; both augmented arms have the same query cost. Report actual shared acquisition time separately from pure combination time, not a fabricated per-arm end-to-end speed comparison. Reuse unchanged contextual query contract and foundation qualification_v3 contract. No query text edits to obtain a pass.

## Fresh inputs and integrity

36 new requests in three disjoint batches of12, each with10 catalog-related and2 unsupported requests. Freeze source text and protocol before native generation. Topic overlap is unavoidable with46facts; fresh wording/conditions are not held-out library topics. Each batch gets a fresh native context: save first foundation literal, then first contextual supplement JSON using only savedplan and frozen contract. No catalog/gold/results supplied to generators, no repairs/retries. Use frozen qualification_v2 first-save transport. Native generation is not a pinned hosted API experiment or repeated delivery qualification.

Before retrieval, independently review all outputs for meaning/conditions/negation/scope, and prospectively label source requests from full46factcatalog. Retain semantic failures; never remove failed cases or repair text. Keep partial and unsupported coverage explicit. Freeze labels, code, actual dependency metadata, DB, embedding artifacts and readiness decision before query acquisition. Existing context candidate's whole-record fallback handles invalid supplements, with errors counted. Invalid foundation produces an explicit empty result for all arms, counted. Structural/semantic input quality and merger performance must be reported separately; input failures prevent full-pipeline qualification, but do not erase the conditional merger comparison.

All work inside this new directory. Prior46protectionmanifests verified before/after; sealed semantics never read. SQLite mode=ro/query_only; ordinary transient fact vectors only. Exclusive first-run results, all traces retained, manifests verified before scoring. No live reruns for reviewer; pure recomputation from saved lists is permitted.

## Success criteria before results

Primary safety gate against FOUNDATION: zero paired losses of complete required groups@8, zero lost relevant baseline facts@8 across every request (stronger than equal aggregate recall), no increase in unsupported candidate exposure. This is observed safety, not a mathematical guarantee for future requests. Protected-six prefix invariant must hold in every request.

Utility: at least one gained relevant fact and pooled mean recall@8 improvement of at least0.5percentagepoints, no batch recall regression, precision@8 not lower. This is a new bounded merger criterion, not a retroactive change to the previous contextual query experiment's+2point gate. Safety remains strict. Compare also to current fusion: enumerate every rescued/lost relevant fact and paired-group change; don't let rescue versus fusion conceal loss versus foundation.

Consistency diagnostic: target90% macro all-relevant recall@8, engineering floor89.25% in every batch and pooled. This is not annotation precision or final-answer accuracy. Promotion is not automatic: report safety, utility, consistency and input semantic validity independently. No choosing a passing metric after results.

Report macro precision/recall, binary nDCG, MRR/any-hit, required-group coverage and complete cases at4/8 per batch and pooled. Gold required groups are AND across groups and OR within substitutes. Unsupported emptygold recall is null; count candidate exposure separately. Partialcases score only catalog-backed aspects. Track fact-level paired losses even when a required substitute survives. Report all missing groups, query counts/bytes, combination/acquisition/setup time, errors and semantic judgments. Small related synthetic batches do not establish population accuracy to±0.75points; include descriptive request-bootstrap intervals and count sensitivity.

TDD for policy and safety accounting. Independent prospective/preflight review1, completedreview2; maximum3instances, third reserved for material fixes. Existing tests/old diagnostics may inform design before freeze, but no oldcase replay is counted as fresh evidence. No postrun tuning. A negative experiment is retained and reported.

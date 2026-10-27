# External question bank diagnostic results

All260 original external questions were tested against the isolated176-fact candidate, with an explicit Formly6.3.12/Material context. The installed124-fact DB remains unchanged. Frozen criteria and case classifications preceded every tool call; no tuning or knowledge changes during this run. Independent review: **Ready for the bounded diagnostic**, no actionable findings; see REVIEW.md.

## Outcomes in each of three repeats

| Outcome | Initial | After bounded recovery |
| --- | ---: | ---: |
| Fully supported |36/260 (13.85%)|79/260 (30.38%)|
| Partial support |125|113|
| Unsupported by delivered evidence |47|15|
| Needs application/version/question context |52|53|

No question was removed. Needs_context can increase when additional evidence clarifies the missing dependency; it is not a positive answer. Safe handling was assessed separately:260/260 answers explicitly bounded their gaps, with no critical unsupported claims identified. Safe handling is an assessor judgment and does **not** count as full support or establish autonomous-harness reliability.

## Frozen request scopes

| Scope | Requests | Initial full | Completed full | Partial | Unsupported | Needs context |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
|application|9|0|0|0|0|9|
|clarification|8|0|0|0|0|8|
|library|102|30|66|33|3|0|
|mixed|130|6|13|80|11|26|
|version|11|0|0|0|1|10|

Library-focused full support is **66/102 (64.71%)**, versus30/102 initially. This does not meet90%; the frozen plan treats this broader, unverified-answer bank as a diagnostic, with no pass threshold. Application questions alone do not explain the gap. Recovery substantially improves support but leaves36 library-focused requests incomplete (33partial,3unsupported).

## What this means

Q1 qualified a source-informed bounded set; it did not establish whole-library accuracy. This external set exposes both missing delivered contract details and full-question retrieval misses. Example: FQ043 asks why toggling a conditional section erases values, yet did not receive the needed hide-retention evidence. Failure to deliver an answer after bounded search does not prove the DB lacks it. Before adding facts, separate caller-plan wording/retrieval misses from genuinely absent knowledge.

Concrete library-focused gaps include field.get versus formControl.get (FQ017); global/local hide-reset precedence (FQ042); state-preserving row reordering and row-count UI enforcement (FQ074/FQ078); complete hook inventory/order (FQ081); FieldArrayTypeConfig typing (FQ094); wrapper nesting (FQ103); className versus fieldGroupClassName DOM targets (FQ105); duplicate registration resolution (FQ118); and per-field preset overrides (FQ119). These are evidence gaps in this run, not a new authorized ingestion backlog.

Mixed questions often require Angular/control contracts, HTTP race handling, CVA behavior, accessibility/browser evidence or application policy. Repository questions have no repository fixture. Version questions do not become answered by substituting our available release. Those boundaries remain explicit, with all cases still visible.

## Execution and limits

1,770 actual stdio MCP calls:780 initial lookups and990 recovery calls,590calls perrepeat. Every corresponding tool argument/result packet matched exactly, excluding timings. Zero tool/operational errors; original scope, observed-ID provenance, budgets and receipts passed audit. First lookup returned259ok/1no_evidence perrepeat; ok means evidence candidates, not semantic completeness. At most2pages of16 discovery candidates and2fetches of16 observedIDs perquestion; many requests required fewer. Discovery candidates were fetched before citation.

22 focused tests passed, including new metric tests first run red. Full local maintenance passed, protected-file hashes and both database pins matched. Both runtime implementations/manifests/models, installed DB, candidate and sealed evaluation stayed unchanged. No promotion, commit or publishing.

The bank has no validated gold answers and is not measured traffic. Requirements were authored from questions before retrieval; the same assessors later judged their groups, with an independent review challenging results. Exact original requests were supplied as one-question caller plans, holding planning constant as in Q1. This is **not** a fresh autonomous decomposition or model-backed comparison. Three repeated identical packets do not provide three independent semantic samples. Do not use these numbers as universal production accuracy.

See COVERAGE.md for every original question, outcome and missing requirement; per-case explicit answers/citations remain in test-output/assessment. RESULTS.json is the audited machine-readable report. Next useful work is a bounded diagnosis of the36 library-focused misses with actual caller-derived plans, separating retrieval/planning from knowledge coverage before editing the DB.

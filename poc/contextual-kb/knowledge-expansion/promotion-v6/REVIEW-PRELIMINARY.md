# Promotion preliminary review

Review instance: 1 of 3. Independent deployment/promotion review; candidate qualification is closed and distinct.

Before reading REVIEW-AUTHOR.md, inspected tests, promotion preparation/rollback, smoke invocation, service composition, qualified planner source and qualification pins, source-check integration and runtime-test integration. Base verified as 39957158b18c040aae87a58a6fa9fcd58ec0a814. Existing candidate histories remain in scope only as immutable inputs.

No actionable defect identified in the initial source pass. Outstanding verification: independently compare dry-run generated changes and hashes; confirm all five DB tables reproduce, existing rows remain, exact qualified planner pins are installed, and only the six intended installed targets change. Test default-service assertion is deliberately expected to fail until promotion applies. Smoke semantics, citation support, Q20 premises, current documentation and final preservation checks remain pending and cannot be inferred from fixture tests.

Operational limit: replacement is per-file atomic with exception/interrupt rollback, not a multi-file crash transaction; stop competing service processes during promotion and preserve the recovery snapshot. The CLI accurately states this limit.

Graph Tier 2 lookup returned no promotion-v6 symbols; exact coverage reports new promotion/planner sources untracked, changed tests/checks stale and tools excluded. All relevant implementation was read directly; no completeness claim rests on the graph.

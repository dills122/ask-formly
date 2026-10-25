# Isolated build and comparison execution

User authorization: build and compare this isolated candidate through MCP; independent review; conditional further group iteration. No installed-DB promotion or publication.

## Fixed setup

- Accepted planner/normalizer/GLiNER/retrieval/selection/service/server modules unchanged.
- Same hosted model/effort as accepted setup: gpt-6-astra, medium.
- Development: 16 requests, baseline and candidate, one pass first. Qualification: 30 fresh requests, each arm three repeats, seeds 1701/1702/1701 matched between arms. Development uses groups of four; qualification uses fixed groups of five, alternating arm order.
- Real calling agent invokes the real stdio MCP, forwards each request verbatim exactly once, receives facts/citations and writes an explanation. Caller has no gold rubric, file/shell/web access or application knowledge. It reports failed calls without retry.
- Matched-plan replay uses normalized cores saved by actual MCP requests, then applies the same core to the other DB. This isolates retrieval/selection differences; independently planned real-agent calls remain a separate measurement.
- Candidate-only manifest pins DB and inputs. Original foundation preflight and preservation checks still apply. No production config or source manifest repinning.

## Gates

1. Independent safety/qualification review before build or inference.
2. Build, verify original SQL rows/provenance plus expected counts, and run development.
3. Inspect developmental failures before qualification; fix only harness defects, never discard failures. If a core support/safety failure makes qualification pointless, report it rather than labeling a development run a qualification pass. Do not relax 90% gate.
4. Freeze hashes of candidate DB, question files, caller/schema/harness before fresh qualification. No knowledge/prompt/rubric tuning during qualification.
5. Independently assess usable answers and semantic evidence coverage; exact fact ID hit rates are diagnostic only. Classify planner, knowledge, retrieval, selection, delivery and caller failures separately.
6. Independent final review; preserve accepted assets. A successful candidate permits the next knowledge-group inventory/candidate cycle, not an installed DB replacement.

## Progress

See progress.md, review reports, and test-output receipts. No result is assumed from the prepared batch.

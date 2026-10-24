# MCP usability checkpoint results

The stable local entry point works with the accepted frozen components. No planner, wording, extraction, retrieval or selection implementation was changed. The new launcher, manifest, doctor and setup/configuration documents are in this directory only.

## Delivered

- `launcher.py serve`: stable stdio entry point using the accepted composition, default seed 1701 with seed 1702 alternate.
- `launcher.py doctor`: read-only prerequisite report. Checks 75 recorded source/data/model/cache hashes, key installed package versions in the two existing environments, executable worker Python and Codex PATH availability. Startup uses the same checks. It does not certify auth/network/quota/native-load health.
- `foundation.json`: named component/version/hash record.
- `README.md`, `codex.example.toml`, `generic.example.json`: launch/setup, current-checkout prerequisites, request/data flow, timeouts, support limits and recovery. No global/client configuration changed.

## Executed checks

Seven new launcher tests pass after recorded RED/GREEN. Eleven existing MCP tests and nine wording tests also pass (27 total). Existing MCP test output retains its unclosed SQLite ResourceWarning; it is not hidden or attributed to this wrapper.

Actual SDK stdio verification ran twice in separate processes: initialize, discover exactly lookup_formly, empty request returns MCP error, successful ping afterward, graceful close and fresh restart. A controlled empty PATH produces clear missing-Codex startup error, exit 2, no stdout contamination. Doctor passes in the qualified environment. Parsed TOML and JSON configs agree on command/args/env; doctor also passes under the example config PATH.

Two real-agent sessions use the stable launcher and actual hosted planner/selector, one for each frozen GLiNER seed. Each session asks a supported hiding question twice, a missing validator knowledge question, and a public weather question. All 8 MCP calls succeeded. Eight fresh planner generations and six actual hosted selector generations completed; weather produces an empty plan and bypasses selection. No fallback, retries or generated-result discard.

| Request | Seed 1701 | Seed 1702 |
| --- | --- | --- |
| Hiding: value and FormControl, first request | supported | supported |
| Same complete request repeated | supported | supported |
| Synchronous validator plus custom message | not_supported | not_supported |
| Weather | out_of_scope | out_of_scope |

Answers retain the distinction between value retention and active control-tree membership. Validator answers explicitly acknowledge missing evidence; weather answers do not invent a library lookup. No whole-library or new 90% accuracy claim follows from these exposed diagnostic cases.

First supported calls took 25.60/31.00 seconds; repeats 13.86/15.46 seconds; validator 11.55/11.48 seconds; out-of-scope 4.58/4.63 seconds. The audit verifies one reused extractor worker per session and different workers across the two fresh sessions. These small-sample timings are not latency guarantees.

The audit reconstructs normalization, compares raw planner output to recorded original plans, replays original full-question retrieval, checks exact stored fact/citation identity and packet delivery, and matches hosted selector payload/decision evidence (consuming repeated identical payloads as a multiset). It confirms eight-slot/replacement bounds, model parameter integrity, DB integrity and explicit empty-scope handling. No changes to existing artifacts were required.

## Approval and scope record

The first attempted agent-test launch was blocked before execution by automatic approval review for a newly introduced application-specific ownership query. That case was replaced before any generation with the public question “What is the weather today?” to test the same out-of-library boundary without application data. The revised safe run was approved. Original/revised harness freezes and the adjustment receipt are retained; this was not outcome-driven resampling.

Independent review: REVIEW.md and REVIEW-DECISION.json. Prior preservation chains and all three preceding candidate/evidence final manifests match. Models, DB/data and sealed evaluation unchanged. Evaluation was hash-checked only. No installation, training, default client registration, commits or publication.

This checkpoint qualifies local use of the existing POC checkout. Fresh-machine distribution, remote service hosting, large concurrent load, automated provider outage recovery and knowledge expansion are not established. Real-provider outage behavior was not deliberately induced; missing CLI and invalid-input recovery were tested. The inherited planner/selector timeout/fallback behavior is documented, not newly stress-qualified here.

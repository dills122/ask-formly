# Bounded MCP integration results

The new local stdio tool accepts a raw Formly request and runs the unchanged foundation contract, frozen advisory GLiNER extraction and unchanged full-question retrieval. This report records the fixed qualification; independent acceptance is recorded in REVIEW.md and CLOSEOUT.md when complete.

## Actual execution

The installed Codex CLI called the new MCP through its native MCP client. Three independent calling-agent processes each handled the same ten fresh development cases once, forwarded requests verbatim, read returned tool packets and produced evidence-limited final answers. Server sessions used frozen adapter1701,1702,1701 respectively. No call was repaired, retried or replaced. Raw client events, server audits, planner generations and first final answers remain in test-output/qualification. The development cases were frozen before these runs; sealed evaluation was not used.

- 30/30 scheduled tool calls completed, each with one matching server audit and one final answer.
- 30/30 structured packets exactly match the responses recorded in the real calling-agent logs.
- 30/30 original full-query lists, rankings/merged IDs and whole fact records match foundation-only replay of each actual generated plan using the original retrieval environment.
- Both frozen GLiNER adapters ran natively:50derived questions total (17,16,17 by round). All native parameter checks succeeded; no extraction or verification errors. All nonempty plans reported available annotations, and the three app-only requests reported not_needed.
- All returned citations map to selected fact IDs; every cited answer fact ID exists in that response.
- 50 protected manifest chains remain unchanged, including the accepted advisory integration and its closeout. Models, DB, existing candidates and foundation remain unchanged. Sealed files were hashed only.

## Semantic assessment

Author manually inspected all30plans/answers against the predeclared rubric and their actual returned facts/provenance. No material lost request, API substitution, polarity reversal, scope invention or mandatory condition/ledger failure was observed. All10case triplets preserve meaning and required context; only1triplet is exactly equal as full plan JSON. The frozen contract permits harmless wording, reasons and prerequisite decomposition differences.

Each repetition has the same outcome:

| Outcome | Per10requests | Across30 |
|---|---:|---:|
| Fully supported answer |4|12|
| Explicit partial answer |2|6|
| Explicit missing/version-inapplicable support |3|9|
| Appropriate application-scope decline |1|3|

All30 meet the frozen **usable-response** rubric: a faithfully planned, delivered response that answers only supported claims and identifies missing support. Each run meets the >=9/10 usability target. This is not30complete answers or100%general answer accuracy. In particular, wrapper selection and dynamic required configuration have partial retrieved support; validator setup has missing retrieved support;6.3.12facts do not establish a7guarantee. A missing retrieved fact is not proof that the whole locked KB lacks it. No further tuning was performed to change these outcomes.

The panel has10synthetic cases and correlated repetitions; it cannot resolve the requested0.50–0.75percentage-point tolerance, establish broad Formly coverage, or compare the adapters' accuracy causally. Server parity alone is not the semantic grade. See test-output/results/semantic-grades.json and stability.json for individual assessments, and the independent review for reconciliation.

## Timing

| Round / adapter | First server call | Warm server median | Full10-case calling-agent batch |
|---|---:|---:|---:|
|1 /1701|20.95s|6.98s|132.39s|
|2 /1702|20.13s|6.69s|119.01s|
|3 /1701|20.80s|6.75s|125.96s|

The first call includes retrieval setup and GLiNER loading. Warm server times still include fresh planner generation and model integrity verification; planner median was5.74–6.19s. Full batch timing includes agent/tool orchestration and final answers. No unmeasured general latency promise follows.

## Verification and provenance

11new unit/transport tests pass, and the unchanged35-test advisory suite passes independently. Service tests cover validation before IO, preserved raw request/core, repeated use, sticky integrity failure, closure, concurrent-call serialization and cancellation drain. A real SDK subprocess test covers tools/list, structured tools/call, repeated calls, invalid inputs and stdout isolation. Citation metadata is separately tested against selected records.

Initial failures are retained: missing service RED; citation helper RED; transport bare-dict output absent/invalid for structuredContent. The typed SDK output annotation fixed the latter before the qualification freeze. The initial restricted connectivity probe and dependency download failure were environment failures, not dropped scored cases. The exact-contract planner smoke and actual SDK/native smoke are separate pre-qualification diagnostics. Source code and cases did not change during qualification.

This is a local POC serving milestone, not global client registration, production hosting or a new answer-generation subsystem. Codex authentication/network is required for the planner; its alias and effort are pinned but the provider revision, temperature and seed are not. Stored provenance is returned, not revalidated against external source bytes. Earlier artifacts and failures remain immutable.

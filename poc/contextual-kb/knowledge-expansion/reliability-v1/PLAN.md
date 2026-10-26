# Isolated delivery reliability candidate

User authorization: fix MCP availability and capitalization validation in an isolated candidate, retest and independently review. Existing runtime, prior candidates, models, installed and expanded DBs, compiler inputs and sealed evaluation remain unchanged. This is a new authorized implementation/review flow; maximum three fresh review instances, starting at zero. No publication.

## Diagnosis and bounded changes

1. Saved Q20 fails because a ledger entry lowercases source-initial `An`. The strict validator correctly rejects a non-exact source span. Add an adapter that restores exact source spelling for a unique leading ordinary article (`A`, `An`, `The`), with identical remainder and explicit boundaries. Restore only existing copies in the linked questions; never insert a missing condition. Repairs are limited to single-line prose: reject any question with backticks, tilde fences, angle brackets or line breaks, and reject matches inside straight/curly quoted regions. Already-valid plans remain unchanged. API names, literals, negation and all other text remain exact. Re-run the accepted wording adapter and strict validator. Preserve original plan and rewrite provenance.
2. The previous calling-agent config left Formly optional. Official documentation states optional servers have a default 1000ms initial-catalog grace period, independently of startup_timeout_sec. Reproduce delayed initialization with a disposable real MCP fixture. Mark Formly required, wait for the initial catalog with mcp_optional_startup_grace_ms=0, and clarify actual namespaced invocation in the candidate caller; retain finite startup/tool timeouts. If startup fails, abort rather than generate answers without the knowledge tool. No retry or failure replacement. Record server startup milestones/stderr so subsequent failures can be distinguished.

Documentation: https://learn.chatgpt.com/docs/extend/mcp#other-configuration-options (fetched 2026-10-25). Installed CLI0.164.0-alpha.11.1. The historical missing-tool event has insufficient logs to prove its exact cause; a controlled reproducer establishes a mechanism, not retrospective certainty.

## Tests and gates

- TDD: real saved capitalization failure, valid-plan identity/idempotence, API/literal case mismatches, ambiguity, token/quotation boundaries, missing or wrongly bound conditions, negation, malformed structures, no input mutation, existing wording rule retained.
- Real delayed MCP fixture with optional and required settings: same delay beyond optional grace but within startup timeout. Required connection must expose and call the tool; deliberately failed required startup must abort without any generated answer. Retain every attempt.
- Real SDK integration replays saved failed plan through new adapter/backend, with unchanged expanded DB and both frozen extractor seeds. Assert raw request preserved, strict normalized plan valid, source facts/provenance returned, immutable assets intact.
- Freeze before live regression: original30 now-exposed questions, three repeats with seeds1701/1702/1701, batches of five; candidate only, same model/effort/rubric. These are regression evidence, not fresh qualification. Gate >=27/30 and >=18/20 custom-type in every repeat; all gap/regression controls and Q20 pass, zero critical failures. No retries or tuning during run.
- Six fresh realistic requests, three repeats, same fixed setup; >=17/18 useful, no repeat below5/6, zero critical failures. Freeze them with the harness before inference; they are not the existing sealed evaluation.
- Separate-context grading and fresh independent review. Report startup, planning, retrieval and caller failures separately. Do not infer general deterministic reliability from a bounded run.
- Before/after: old qualification freeze hashes and candidate DB manifest, accepted source pins, foundation doctor incl model weights. No installed launch path or config changes.

## Status

Development and controlled startup probes complete; review1 found a quoted-literal boundary defect, now corrected with red/green regressions. Review2 found a double-backtick edge case; repair is now conservatively limited to plain prose. Final review3 must assess the guard before frozen inference and audit results afterward. See DIAGNOSIS.md for failed hypotheses and limits. No acceptance or promotion assumed.

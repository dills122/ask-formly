# Fixed discovery caller checkpoint

## Outcome

The model-free discovery workflow met the bounded target: all10covered answers
were supported in each of3passes, and both controls were safe in each pass.
The old foundation9 reference supplied sufficient evidence for all10covered
requests too. This is matched evidence sufficiency on a small familiar corpus,
not proof of whole-library answer parity, superiority or production readiness.

Keep the isolated candidate for a broader real-use pilot. No model training or
retrieval tuning is justified by a failure in this run. Existing foundation,
models, installed DB and sealed evaluation remain unchanged.

## Execution and independence

The12requests were fixed before execution: ten6.3.12core/Material topics and two
controls (exact6.4.0coverage, private signing-service API). No expected fact-ID
list was prepared or consulted during caller selection. Full raw MCP responses,
inputs, plans, discovery pages, fetches and answers are retained in test-output.

Pass1 used focused split questions. Pass2 used combined questions with the whole
request retained. Both were performed by the implementation conversation and share
context/corpus familiarity. These were manual plan variants, not independent random
samples or an exact-plan determinism experiment. Pass3 was a fresh-context reviewer's
runtime verification before seeing either earlier answers or reference results.
It retained the attributed original request alongside focused questions; this
preserved conditions but may carry less selective shared context into retrieval.

This is a disclosed refinement of PLAN.md's same-conversation three-pass setup:
the final pass was moved into independent runtime review to reduce carryover.
No candidate, data, model or server instruction was tuned between passes.
Transport input arrays contained all12lookups rather than the intended four-case
batches. Follow-ups were grouped separately. This is another method deviation;
it does not constitute independent per-batch context isolation.
There was no automated oracle-driven follow-up selection. Both root answer files
were frozen before reference outputs were inspected; the third caller finished
before reference outputs were opened. Source/answer provenance is preserved.

The reviewer independently graded the20root-context covered answers and their
four controls, and self-checked its own10covered answers/two controls. Thus the
third pass is independently generated, but not independently graded by a second
reviewer. The existing parity review budget ends at instance3of3 here.

## Results

| Pass | Covered answers fully supported | Safe controls | Lookups | Discovery pages | Fetches | Errors |
|---|---:|---:|---:|---:|---:|---:|
|1: focused questions, root context|10/10|2/2|12|4|3|0|
|2: combined questions, same context|10/10|2/2|12|6|5|0|
|3: fresh-context caller|10/10|2/2|12|5|5|0|

All64calls are retained. No plan repairs, scope downgrades or budget exhaustion.
Every answer citation resolves to a full fact delivered in that pass; discovery
summaries alone were not counted as citation evidence. Semantics were reviewed:
model versus control, local/shared conditions, return typing versus runtime,
array falsy insertion versus final build result, exact scope, subscription ownership,
and length versus membership equality. No critical invented API/lost-condition
error was found. Target>=90% per covered pass was met; this does not estimate
accuracy to within0.5–0.75% or establish behavior on unfamiliar library coverage.

The reference completed12calls with no operational failures. Its ten covered
packets were semantically sufficient; do not require identical fact IDs. In D03,
keyed-group evidence supported the nested model answer without the dedicated leaf
fact. In D09, the wrapper insertion citation's source quotation also supported the
control/value-accessor distinction without the dedicated wrapper-limit fact.
The old MCP returns evidence, so no old answering-agent accuracy is claimed.
The signing-service control returned unrelated lexical candidates on both paths;
the caller must disclose missing support rather than infer a built-in API.

No no-discovery caller ablation was run on this set. The results qualify the
combined workflow; they do not isolate the marginal accuracy gain of the new tool.

## Cost and transport limits

Serialized MCP result bytes (including duplicated text/structured content, excluding
wire framing) were839010,776658,961330 across the three passes. Calls per request
averaged1.58,1.92,1.83, counting controls. All discovery stopped after one page per
request that used it; no exhaustive automatic scan was used. Unselected full
facts/discovered candidates remain visible in metrics.json and raw output. They
were not used as answer support merely because they were returned.

Summed tool execution seconds were0.236,0.281,0.264; reference tool execution totaled
321.369seconds (covered-request median30.468seconds). These are NOT comparable
end-to-end latency measurements: new-arm planning/reading/selection/synthesis and
SDK server startup are excluded. Do not advertise a speedup from these numbers.
Reference stderr showed no rate-limit/retry markers; internal behavior beyond the
available logs is not asserted.

The experimental ask_formly_discovery connection was added alongside the unchanged
ask_formly_candidate in project .codex/config.toml. Project-scoped MCP configuration
and tool allowlists follow the [official configuration guidance](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).
Its new tool did not appear in this chat catalog during this turn. Tests therefore
used the real MCP SDK stdio protocol with the exact frozen discovery server under
the offline guard. The calling conversation/reviewer made the decisions; no separate
agent CLI and no new-arm server inference was used. This does not qualify app-native
discovery registration. Do not promote this result as a completed desktop connection
test. The additive entry is ready for the next client reload/connection check.

## Verification and preserved boundaries

- Six new transport/accounting tests passed after failing before implementation.
- Startup/initialization-failure handling is not covered by those six helper unit
  tests. All observed sessions completed; retained receipts/raw outputs establish
  this run, not general fault-tolerant benchmark orchestration.
- All813frozen files verified unchanged, including original93-fact DB/models,
  candidates, original qualification inputs and additive config snapshot.
- Existing project maintenance command passed; final result in project-check.txt.
- All cited facts have full delivery;64calls and their failures(0) counted.
- Independent review instance3of3; see REVIEW.md for final verdict and scope.
- No staging, commits, publication, installed-DB rebuild or sealed-evaluation access.

## Next practical step

Verify lookup/discovery/fetch through the newly configured app-native connection
when its tool catalog is refreshed, then use this candidate in a bounded real-task
pilot. Keep explicit evidence gaps and scoped citation review. Use later distinct,
fresh-context requests for broader qualification rather than repeatedly tuning this
already successful small panel. No promotion into the installed foundation is made
by this checkpoint.

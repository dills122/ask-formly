# Response readability, batching and listed-fact reuse

**2026-10-28 — source candidate; unchanged 192-fact DB.** This follow-up addresses
confusing response meanings and oversized fetch recovery identified in the
[call-cost audit](recovery-call-cost-audit.md). Recipe storage remains deferred.

## What changed

Responses now identify what they contain without requiring the caller to infer
it from several other fields:

| `record_kind` | Meaning and next action |
| --- | --- |
| `complete_evidence` | Lookup/fetch facts have complete claims, conditions, limits and provenance. Assess relevance and reuse them; another fetch is not required merely for completeness. |
| `claims_without_provenance` | Discovery supplies claims and limits for selection, but selected IDs need a full provenance fetch before citation. |
| `topic_inventory` | Help lists IDs and titles, not evidence. Fetch chosen IDs directly without rediscovering them. |
| `workflow_and_topic_inventory` | General help contains instructions and topic names. |
| `batch_instructions` | No evidence was delivered. Follow the reported retry batches or unbatchable-record boundary. |

Existing fields and the legacy lookup next-action type remain available. The
next-action text now says that returned lookup facts are complete. `candidate_only`
means relevance needs assessment; it does not mean a fact was truncated.
`truncated` concerns omitted candidates, not clipped returned records. Discovery
instructions are shorter and explicitly distinguish its claims from full evidence.

Caller/help guidance now explains this reading order and asks for batching of
independent already-selected IDs. Read a fact immediately when its conditions
will determine the next search; do not postpone every fetch merely to maximize
batch size. Avoid optional answer elaboration that creates unrelated evidence
obligations. The existing evidence-owner handoff and scope protections remain.

## Oversize recovery

Previously, a compact fetch over the response budget raised a generic instruction
to request fewer IDs. It now validates the entire request first and returns a
bounded `batch_required` packet with `facts: []` and `retry_batches`. Each batch
contains exact `get_formly_facts` arguments and measured packet/result sizes.
The caller can execute those arguments without rediscovery or guessed splits.

No partial facts are silently delivered. Unknown or ineligible IDs still reject
the whole request. First-occurrence order is preserved and duplicates are
normalized. If a record cannot fit alone, `response_too_large` identifies it in
`unbatchable_fact_ids`; do not retry it unchanged. Other feasible batches can be
reported separately. Instructions themselves remain bounded.

The limits remain 28,000 UTF-8 packet bytes and 30,000 serialized MCP-result bytes.
A maximum of 16 input IDs is not a promise that all 16 fit. Retry scope is resolved
explicitly, and sizing uses that retry context so default/major-version metadata
changes do not invalidate the advertised sizes. The explicitly requested full
format retains its separate 48,000-byte limit and reports compact/fewer-ID recovery
when oversized. No new preflight tool or mandatory extra call was added.

## What this does not solve by itself

The previous eight lookup packets were near the size ceiling. Complete provenance
was a large contributor, alongside facts and question diagnostics. We did not
remove conditions, source quotations or provenance to obtain smaller numbers, and
we did not add a second large prose summary of the same records. Small new labels
can still affect how many complete facts fit in a near-ceiling lookup packet;
ranking is unchanged, but budget-driven selection must be checked.

A JSON result can be large or rendered into a client-managed file even while it
fits the MCP budget. Earlier ask-formly-only tests could not establish whether
callers needed Python. The fresh comparison explicitly permits local parsing of
actually returned JSON, without directing callers to use it, and records such
actions separately. Neither no parser use nor successful bounded transport proves
all clients will display every response inline. This change makes the contract
clearer; it does not eliminate every large payload or qualify all client behavior.

## Verification

Source-only checks pass 348 tests. New response regressions cover whole-request
validation, measured retry batches, duplicate/order handling, unbatchable records,
normal/full behavior and exact retry sizes for default/major scope. Focused
independent review found no actionable defect and approved fresh-caller evaluation.

A real SDK diagnostic replays the historical eleven-ID oversized fetch. Baseline15
returns its original rejection. Candidate16 returns a 1,421-byte instruction
packet (1,656-byte serialized result) and two retries. They deliver all eleven
facts once: ten facts at 26,442 packet / 28,096 result bytes, then one at
2,946 / 3,281. Measured retry sizes match actual serialization. This deterministic
probe is separate from autonomous caller behavior.

The candidate identity is `formly-model-free-discovery-16+00b3331851e8`; baseline
is `formly-model-free-discovery-15+c385659c07a7`. Both use the same 192-fact DB.
Six independently generated questions run once per arm with identical budgets
and generic prompts. They cover simple configuration, broader composition,
unknown custom-component contracts and missing dependency versions. Requests,
rubric, stage pins and prompts are frozen before generation. No expected IDs,
answers or forced parsing steps are supplied, and no quality retries are allowed.

Full local maintenance still cannot run because the worktree compiler environment
is missing. Source tests and SDK probes do not qualify model-backed behavior or
Angular/browser application execution. Raw results, exact before snapshots,
independent review and preservation receipts live in ignored
`test-output/response-batching-v1/`. Canonical knowledge, installed DB, isolated
195-fact candidate and historical results remain protected; nothing is released
or installed by this work.

## Fresh caller observations

All twelve sessions completed within budget with no launch failures. The single
failed tool call was baseline R03's oversized fetch at the end of its budget.
No quality retry was performed. Eighty-four raw caller files and frozen inputs
are retained with hashes.

| Metric | Baseline15 | Candidate16 |
| --- | ---: | ---: |
| Non-help calls | 31 | 29 |
| Help calls | 7 | 9 |
| Total calls | 38 | 38 |
| Discovery calls | 17 | 15 |
| Repeated candidate occurrences across discoveries | 27 | 4 |
| Already-delivered full facts fetched again | 0 | 0 |
| Reserialized response-envelope bytes | 512,643 | 500,145 |

Total calls are unchanged, so this is not a demonstrated overall call reduction.
Bytes decrease about 2.4%, but not uniformly: R01, R03 and R05 increase. R05 takes
two more non-help calls; R01–R04 each take one fewer and R06 is unchanged. The
additional candidate help calls occur in the two broader questions. Fewer overlap
occurrences alone do not establish less unnecessary work or a causal benefit.

No caller invoked a local parser or other action tool. Successful MCP response
texts parsed as complete JSON in the collection harness; truncation markers were
omission metadata or help text, not evidence of clipped transport. No file-spill
action was observed. The actual client/model rendering context was not separately
observed, so neither universal readability nor the absence of a need for parsing
is established. Grader-side extraction of large logs is not caller parsing.

None of the six-question comparison callers received `batch_required`. The SDK
diagnostic verifies the exact two-batch recovery separately. Two additional
frozen operational callers deliberately exercise that branch with
a supplied eleven-ID fetch task and no split hints or expected answers. Their
results are recorded separately below; they are not part of the six-question
comparison. The client where large JSON caused friction still needs its own
rendering inspection.

## Independent answer review

Independent grading found six supported or appropriately bounded candidate
answers. Baseline had five, plus R03 with partial evidence after its final
oversized fetch failed. Both arms addressed the literal questions in prose, but
baseline R03 lacked full provenance for Observable options and conditional
hide/required/reset behavior; its Observable statement cited a different mapping
contract. Its useful repeater and application-handler proposals still receive
credit. Candidate R03's ordinary successful eleven-ID fetch supplied the missing
support; it did not exercise batch recovery.

No inventory was mistaken for delivered fact provenance, and no candidate_only
or omitted-candidate marker was treated as a whole-library completeness claim.
Some unnecessary recovery remains, including R02's extra registration search.
R05's additional supported attribute-boundary explanation costs more calls and
bytes. No blanket usability or efficiency win follows from this small sample.
Arm labels were visible to the separate grader; this is independent review,
not anonymized grading. Previous experiments and failures remain unchanged.

## Focused autonomous batch handling

Two additional fresh operational callers received the same eleven-ID retrieval
task. The initial single compact request was prescribed to reach the size branch;
the prompt did not name retry_batches, suggest a split or supply expected claims.
These are intentional contract exercises, not blind natural-question samples or
an efficiency comparison with baseline.

Each caller made the original request, correctly interpreted its empty-facts
batch instruction, and executed the two returned argument sets exactly. All
eleven full records arrived once. Each used three non-help calls, no help,
rediscovery, local parser or other action calls, and no tool errors. The fourteen
raw files, separate protocol, scope/identity checks and retrieval proof are
frozen independently. Separate grading verified all 22 per-ID claims/citations
across the two answers against delivered records. One caller executed the two
batches in reverse order, which is valid for these independent facts. The main
twelve-session results are unchanged.

This establishes observed autonomous handling of this specific batching response
by two fresh callers. It does not establish how often normal tasks hit the branch,
behavior across other clients, or general cost savings. Broader payload readability
and residual unnecessary searches remain work to measure, not claims resolved by
these two successful exercises.

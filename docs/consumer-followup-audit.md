# Help limits, partial answers and retrieval cost

**2026-10-28.** Help parameter bounds are now advertised and validated in the MCP
schema. The five partial answers from the [generated-question experiment](consumer-generated-results.md)
were audited against all 192 current facts, original delivery steps and exact
pinned source. The main findings are missing Material error detail, application
recipe boundaries, and expensive repeated discovery within the same candidate
pool. No facts or installed DB were changed; the original scores remain intact.

## Implemented: help parameter contract

Both model-free server entry points share constrained help types; discovery
inherits the repair server's help tool. The generated schema states integer
`offset >= 0`, integer `limit` from 1 through 32 (default 16), and optional exact
topic prefix length 1–300. Descriptions explain `next_offset` paging and using a
returned topic rather than inventing one. Invalid inputs reject before service
access, and direct helper guards remain. Values are not silently clamped.

Source candidate identity is `formly-model-free-discovery-13+3144bbbfbe81`.
Existing frozen archives and consumer installations remain unchanged. This is
not a release or a new knowledge installation, and the twenty blind callers
were not rerun on this metadata fix.

Verification: 341 source tests passed, including generated schema checks for
original, repair and discovery servers. Actual launcher stdio rejected 40/50/100
limits and a negative offset, then accepted limits 1 and 32 on the same
connection. The six calls checked identity, response budgets and runtime pins.
Two test-staging failures remain recorded: a historical entry point used a legacy
DB pin, and a manually staged runtime initially omitted the unchanged version
catalog. The final test used the actual launcher and complete staged dependencies.

## What the five partial answers need

| Cases | Diagnosis | Appropriate next work |
| --- | --- | --- |
| F06, F09: error beneath a Material input | Existing visibility, validation and wrapper-shell facts were delivered. No fact states the wrapper's error template or its error-state bridge. Adjacent unfetched facts do not close that gap. | Propose bounded Material error facts from already pinned K17/K16, through a separately authorized knowledge change. |
| S07: wrapper versus own error markup | Label/shell/control contracts were delivered; the same error-ownership detail is absent. | Same Material fact proposal, with explicit limits for arbitrary custom widgets and their Material/control integration. |
| S05: blur validation, immediate correction and pending submission | Blur strategy, debounce limits and submitted error visibility already arrived in lookup. Immediate local correction versus remotely confirmed availability is an application policy; a pending-submit workflow is not established by those facts. | Improve recipe/docs synthesis and qualify Angular/event ordering. Clarify what “fixed” means before promising immediate remote-validation success. |
| S09: reset state and dependent options | Reset baseline/rebuild/control-reset facts were already delivered, including a later full fetch. Conditional submitted-state reset is more precise in pinned source than in the fact. Country/state restore coordination is an application recipe. | Propose a bounded reset-sequence clarification; separately verify Angular dirty/touched/display state and distinguish restore from user-change clearing logic. |

The shared Material gap is supported by source, not merely inferred from failed
searches. [K17's pinned wrapper](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/form-field/src/form-field.wrapper.ts#L81-L83)
contains the error container and Formly message child.
[K16's pinned integration](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/form-field/src/field.type.ts#L38)
connects Material error state to Formly visibility policy. These details are
absent from the current authored claims. This supports a future fact proposal;
it does not certify browser behavior or arbitrary custom components.

For reset, [K05's pinned sequence](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/extensions/core/core.ts#L109-L120)
contains a conditional submitted-state reset, rebuild and delegation to Angular
form reset. Preserve that condition rather than promising unconditional clearing
of all errors. Restoring invalid data must not be described as making it valid.
Four diagnostic source downloads matched the existing catalog's exact file hashes.
They were isolated copies; no source/provenance inputs were replaced.

Three targeted SDK fetches confirmed the stored claims through the unchanged
installed consumer runtime. These are informed diagnostic reads, not blind caller
improvements or rescored historical answers. No exact existing fact was found
that would alone resolve the missing Material markup or full timing/reset recipes.

## Why callers used so many calls

Across twenty journeys there were 154 calls: 29 help, 20 lookup, 76 discovery and
29 fetch. Median total calls per journey was eight, range three to ten. Reserialized
CLI response envelopes totaled 2,051,469 bytes; this is neither wire traffic nor
a token/cost measurement.

**All 76 discovery calls used offset zero.** Callers changed focus or question
selector and restarted the first page; they did not walk to later pages. This
was repeated reordering of the original omitted-candidate pool. Some reranking
found useful support; repeated wording cannot create a missing authored claim.

Discovery returned 757 candidate occurrences, of which 216 overlapped earlier
listings in the same journey. Three pages introduced no new IDs. There were no
exact repeats of the same discovery arguments. These counts identify overlap,
not a proof that every overlapping call was unnecessary.

Of 176 per-case fact occurrences identified by final citations or independent
grading support, 73 were first fully delivered in lookup and 103 through fetch.
That is a hindsight support proxy, not a minimal sufficient set or proof that
all recovery was required. The fetches returned 140 fact occurrences; nine had
already appeared in lookup and were byte-identical fact objects. Those nine were
requested in full format across mixed batches, so explicit provenance expansion
is a plausible reason, and the entire fetch calls cannot be labeled wasted.

Three oversized help requests and two unknown-topic requests consumed calls.
The bounds fix addresses the former. Using returned topic names addresses the
latter. Most cost came from discovery and evidence acquisition, not argument
repair: no plan-refinement response occurred in this cohort.

## Next improvements to evaluate

1. Keep a per-question evidence ledger: required decision, support already in
   lookup, remaining distinction, and IDs already seen/fetched. Target recovery
   at that remaining distinction rather than broad topic restatements.
2. Evaluate a bounded stopping rule when refocusing returns the same concepts
   without resolving the missing claim. Disclose the limit; repeated results do
   not establish absence. Test the rule on preserved cases before adopting it.
3. Prefer exact returned topic names and fetch only chosen candidates. Use full
   provenance when it helps inspection, with awareness of already delivered facts.
4. Prioritize the shared Material fact proposal and a carefully bounded reset
   clarification. More ranking alone cannot supply those absent claims. Keep
   application examples and timing policies separate from universal library facts.

These are concrete follow-ups, not additional behavior changes made in this pass.
Retain original candidate12 traces as the baseline for later comparisons.

## Evidence and preservation

Detailed per-call chronology and metrics are in ignored
`test-output/consumer-followup/call-cost/`. The five-case fact/delivery matrix,
source hashes and raw SDK diagnostics are in `partials/`; fix tests and real
stdio receipts are in `help/`. Original raw traces, rubrics and grades remain
under `test-output/consumer-generated-v1/`.

The full local maintenance command remains blocked by the worktree's missing
compiler environment. Source checks and targeted installed/staged transport
results are reported separately; no model-backed qualification is implied.

Final preservation checks matched all 87 protected source/data paths, all 281
frozen raw experiment files, and every pin in the existing consumer runtime.

# Why total calls rose after the dependency handoff change

**2026-10-28 — investigation only.** Ruflo coordinated three trace audits of the
four paired questions in the [dependency/recovery follow-up](dependency-recovery-followup.md).
Facts, installed DB, isolated knowledge candidate, caller guidance and ranking
remain unchanged during this investigation. Recipe storage remains deferred.

## The exact accounting

| Tool | Baseline14 | Guidance15 | Difference |
| --- | ---: | ---: | ---: |
| Lookup | 4 | 4 | 0 |
| Discovery | 13 | 11 | -2 |
| Fact fetch, including failed attempts | 9 | 12 | +3 |
| Non-help total | 26 | 27 | +1 |
| Help | 6 | 6 | 0 |

The extra non-help call is accounted for by D04: both callers discover three
times, but the guidance15 caller fetches in three batches rather than two.
D01 and D02 each trade one fewer discovery for one more fetch, so their totals
stay unchanged. D03 has four fetch attempts in both arms; baseline includes one
failed oversized request while candidate's four succeed. No repeated complete-fact
fetch was recorded. More fragmented retrieval, not more discovery, explains the
aggregate increase.

This describes observed calls, not a causal proof that guidance15 caused the
behavior. Plans, retrieved packets and generated answers differ, and each arm has
only one generation per question. Source and DB were otherwise held fixed.

## What counts as unnecessary

A discovery can be deleted from a known trace only when its eventual supporting
IDs were already available from earlier lookup previews, topic listings or other
discoveries. A later fact fetch may still be necessary: those listings do not
contain full claims and provenance. Overlap and lack of a citation do not by
themselves establish waste.

Batching is a separate opportunity. Combine already-selected IDs when the full
response fits transport limits, but do not assume that the allowed 16 IDs will
fit the byte budget. Do not postpone a fetch needed to decide the next search.
Retrospective packet tests can establish feasibility; they cannot prove a blind
caller would choose the same path or produce an equivalent answer.

## Remaining opportunities

| Case | Trace finding | What can be reduced |
| --- | --- | --- |
| D01 | One fewer discovery is offset by a second fetch. Baseline discovery5 adds no unique eventual full support; its relevant ID was already listed. | Remove that baseline rediscovery. Candidate fetches5/7 can fit together, but require delaying the first fetch until the independent model-propagation search completes. |
| D02 | One fewer discovery is offset by a third fetch. Candidate fetches7/8 are adjacent; all three selected IDs were already listed by discovery6. | Combine those adjacent fetches without changing the evidence or adding a new search. This is the clearest batching opportunity. |
| D03 | Baseline attempts an oversized batch, then splits it. Candidate avoids the error but makes four successful fetches. Each arm also searches exact Material markup without acquiring a new eventual support record from that call. | Remove baseline discovery8 and candidate discovery7 from the known sequences; avoid the rejected batch and consider measured smaller merges. Do not claim arbitrary widget integration is established. |
| D04 | Candidate fetches each independent branch separately. Baseline separately rediscovers a textarea-dimension ID already in the lookup preview. | Remove baseline discovery4; combine candidate fetches4/6 after discovery5. Candidate's three discoveries each supply distinct required mechanisms and should not simply be deleted. |

Some additional details were optional: explaining DOM ID/name versus an unchanged
field key, required-marker presentation beyond required validation, or adding a
rows setting the user did not request. These can create extra evidence obligations.
They are not automatically errors, and omitting one record from an existing batch
does not necessarily save a call. Prefer the requested outcome before optional
elaboration; retain any condition necessary for a correct answer.

A later page duplicating an earlier result does not prove the earlier search was
unnecessary when made. More aggressive alternative-order paths are recorded only
as retrospective hypotheses, not safe automatic deletion rules.

## Actual packet checks

Eight combined requests succeeded against the unchanged staged guidance15/192-fact
runtime; the original D03 eleven-ID request reproduced its oversized rejection.
All probes were read-only. Successful results retain full selected records and
provenance rather than trimming claims to fit.

| Proposed merge (original step numbers) | IDs | Packet bytes | Serialized MCP-result bytes |
| --- | ---: | ---: | ---: |
| D01 candidate5+7 | 6 | 12,891 | 13,766 |
| D02 candidate7+8 | 3 | 9,017 | 9,636 |
| D02 candidate5+7+8 | 6 | 16,357 | 17,396 |
| D03 baseline6+7 | 9 | 24,250 | 25,697 |
| D03 candidate3+5 | 8 | 17,831 | 18,979 |
| D03 candidate8+10 | 7 | 22,015 | 23,286 |
| D04 candidate4+6 | 5 | 14,076 | 14,931 |
| D04 candidate4+6+8 (additional probe) | 6 | 15,709 | 16,656 |

The applicable limits are 28,000 packet bytes and 30,000 serialized tool-result
bytes. These sizes establish feasibility for these exact records and runtime;
record count alone is not a safe batching rule. Delayed merges also need a scheduling
check: would an earlier full record change the next search or selection? An
adjacent merge with all IDs already selected has less uncertainty than delaying
several branches. No new blind callers ran, and these checks do not establish
answer quality or call savings after a policy change.

## Follow-up priority

Prioritize packet-aware batching and an explicit check of already-listed IDs
before more discovery. Preserve legitimate recovery when a page adds a missing
condition. Avoid a fixed low call cap, overlap cutoff or blanket dependency-topic
suppression: each can remove useful evidence.

Also avoid introducing optional implementation technologies into the plan merely
to rule them out. D02 explored Angular directive composition and setup alternatives
that its selected reuse design did not require. Some of those searches happened
to return useful ownership facts, so the remedy is a more direct mechanism query,
not blanket suppression of Angular-looking terms.

For batching, investigate a reliable size advisory or structured oversize
recovery hint rather than raising the response budget or inventing a universal
safe ID count. Current instructions allow batching but do not tell a caller the
exact size of its selected record union. Such a change needs separate design and
validation; none was implemented here.

A future change should test these behaviors separately, preserve answer
quality and scope, and measure total calls including errors rather than discovery
count alone. No new product change or blind caller rerun is made in this audit.

## Evidence and limits

The complete paired transcripts and grades remain frozen in
`test-output/dependency-recovery-v1/evaluation/`. New call accounting, per-case
reports and read-only packet checks are retained in ignored
`test-output/recovery-cost-audit-v1/`. No old caller was rerun or rescored.
The required maintenance command remains blocked by the absent worktree compiler
environment. Documentation/provenance validation and preservation checks do not
qualify application runtime or model-backed behavior.

All 103 protected paths, previous frozen inputs and raw paired outputs remained
unchanged. Documentation/provenance validation passed; no source behavior changed.

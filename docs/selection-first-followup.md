# Selection of already-discovered evidence

This follows the [recovery efficiency audit](recovery-efficiency-followup.md).
The isolated candidate now asks callers to map each unanswered decision to the
claims, conditions and limits already listed, batch-fetch suitable IDs for
citations, then continue discovery for decisions without suitable evidence.
An example can support the behavior it demonstrates without establishing a
complete API contract. The guidance permits continued searches and does not
require fetching irrelevant records.

Candidate `answer-response-v1+be2719ed135a` replaces existing discovery guidance;
it adds no response fields, changes no ranking, and preserves candidate content,
order, scope and paging. The replacement is shorter than the original message
and refreshes advertised byte counts. Empty, exhausted and invalid requests
retain their behavior. There is no server-side seen-record state.

Twenty-seven candidate tests and 348 existing source checks pass. Real SDK
replay of twelve historical requests confirms the five valid discovery packets
are identical except guidance and measured byte fields. Each focused packet is
21 bytes smaller. Missing-plan SDK errors remain unchanged. Initialization
guidance grows by 308 bytes (3,520 to 3,828); this is separate from tool-result
byte totals. In-session diff checks supplement these tests; this does not
restart the previously completed independent engineering-review flow.

The frozen comparison uses baseline `answer-response-v1+8eda6620a38c` and four
new questions, each answered once per arm by a fresh caller. Two are ordinary
requests and two require source auditing. A fifth paired question repeats the
historical callback-evidence miss and is reported separately as a targeted
regression. Questions, requirements, prompts and runtimes are frozen before
execution. Masked grading checks required decisions, limited example support,
source quotations and legitimate gaps before unmasking. No quality reruns are
permitted. Schemas and guidance may reveal the arm; masking is not guaranteed
blinding.

## Fresh results

All eight new-question sessions completed without SDK errors, refinement
responses, parser commands or budget excesses. Masked grading accepted both
arms on all four questions, retaining the permitted evidence gaps. These are
bounded supported answers, not complete coverage of every requested contract.

| Fresh-question metric | Frozen baseline | Updated candidate |
| --- | ---: | ---: |
| Total calls | 31 | 30 |
| Discovery calls | 12 | 9 |
| Help calls | 5 | 3 |
| Complete-fact fetch calls | 6 | 10 |
| Provenance calls | 4 | 4 |
| Response text bytes | 370,970 | 320,944 |
| Serialized CLI result bytes | 399,391 | 346,523 |
| Newly delivered complete facts | 59 | 64 |

Result bytes fell 13.2%. Discovery accounted for 47,612 fewer result bytes and
help for 23,171 fewer; additional fact fetching and provenance offset part of
those savings. Discovery entries fell 153→116, with repeated entries 28→19.
Transitions to another discovery after selecting from the preceding page rose
3→4; transitions without selection fell 5→1. These are mechanical observations,
not proof that every selection was relevant. No positive-offset paging occurred
in these source audits: the observed improvement concerns further discovery and
refocusing, not demonstrated elimination of unnecessary pagination.

The grader found modest selection delays in baseline S01/S03 and candidate
S04. The latter searched further for an unresolved Material display predicate
before selecting a previously listed partial example, then used that example
and its actual excerpts. Continued discovery can still be legitimate when a
listed example does not settle the remaining decision. Candidate S04 obtained
direct source excerpts that baseline did not; both accurately bounded their
available evidence. No general efficiency rate follows from one caller per arm
per question.

## Historical callback regression and remaining work

The separate T01 pair used 10→9 calls and 130,919→90,346 result bytes. Baseline
again omitted a displayed named-expression example using `control.value`.
Candidate never received that complete claim: help listed its ID/title only.
The candidate accurately reported callback inputs unresolved, but this is not
proof that the original example-selection miss is fixed. Neither caller
established the full callback signature or automatic sibling revalidation.
Masked grades distinguish baseline's omitted available partial support from
candidate's acceptable bounded partial audit; neither fully answers that input
question.

Candidate T01 also made a near-equivalent refocus returning eight already
displayed records before selecting three of them. That is a concrete remaining
selection delay. Its final provenance batch included one redundant authored
summary under a different fact ID alongside useful new provenance; discarding
the whole call would lose evidence. There were no retries for known absent
excerpts under the same fact ID.

The next priority is handling a discovery step that adds no relevant evidence:
select suitable current records, retain limited support, and state the precise
remaining gap. Provenance reuse should recognize identical already-returned
authored text without suppressing distinct evidence for other facts. Further
changes need their own frozen comparison; this trial was not tuned or rerun
after grading. Keep this candidate isolated. It improves observed selection
and payload cost on the new questions but does not close every recovery gap.

Grades were frozen before unmasking X as baseline and Y as candidate. All 144
protected paths, seven candidate files, both 31-file stages, 17 frozen inputs,
70 raw files and ten masked manifests passed final preservation verification.

Raw sessions, measurements and preservation manifests live under ignored
`test-output/selection-first-v1/`. Facts and the installed DB remain unchanged;
the candidate is not promoted, and recipe storage remains deferred. Full local
maintenance remains blocked by the missing worktree compiler environment.
Source checks and Codex caller sessions do not qualify that environment or
reproduce the reported Kiro IDE behavior.

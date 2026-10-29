# Consumer testing and blind audit direction

**2026-10-28 — next testing direction.** Add a consumer journey through a frozen
package and an actual MCP client. Measure setup, transport, evidence recovery and
final-answer support separately. Keep supplied-plan regressions for diagnosing
retrieval changes; they do not replace independent consumer trials.

The first [frozen discovery11 consumer run](frozen-consumer-results.md) is now
complete: fresh dependency installation, actual Codex CLI setup, persistent
transport and five independent own-plan callers. Its bounded results and rubric
caveats are recorded separately from the earlier staged-artifact pilot below.
The [discovery12 follow-up](consumer-v2-results.md) adds explicit build identity,
a required/optional rubric and repeated independent caller sessions.

## What the current checks establish

Current source regressions test deterministic plans, bounded responses and known
support requirements. Fresh caller checks test planning and evidence use, but
their `call.py` helper starts a source adapter for each call. It bypasses the
packaged launcher and does not exercise persistent client sessions.

The release history includes a fresh environment installation on the tested
macOS configuration. The installer self-test checks initialization, the tool
catalog and one lookup; it does not establish recovery quality, correct client
rendering or complete answers. Those remain distinct from installation success.
Earlier caller history also records cross-case fact-ID reuse, so independent
questions and multi-turn workflows need separate tests.

## First consumer journey

1. Freeze one allowlisted archive with its checksum, runtime identity, dependency
   set and unchanged DB digest. Fixes produce a new candidate, rather than
   changing the artifact under test. Publication is not required.
2. Give a fresh setup operator only the archive, checksum and shipped setup
   instructions. Use an unused installation prefix and a named MCP client.
   Record errors, configuration decisions and maintainer interventions. Do not
   prewrite the client's configuration for an unassisted setup test.
3. Give each fresh caller an ordinary user task and the installed tools. Let it
   construct its own plan and decide whether to use help or recovery. It may
   read shipped instructions and returned evidence, but not expected IDs,
   repository source, the corpus, grading rubric or other callers' answers.
4. Capture the final answer alongside complete tool arguments, errors, responses,
   citations, byte counts and timings. Independently assess support, critical
   conditions, unresolved requests and proposed-versus-established behavior.
5. Exercise a persistent session through a valid call, a rejected call, a
   corrected call and recovery. Restart and reconnect, then check that subsequent
   calls still work in the intended scope. Keep this sequence separate from
   independent answer-quality trials.

Start with a small public development bank: ordinary lookup, a compound design,
an unfamiliar custom API, unsupported scope and a repairable plan error. Include
paths with spaces and a changed working directory. Report completion without
maintainer rescue, repair/recovery counts, time to first useful answer, unsupported
claims and remaining needs. Do not blend these into one accuracy percentage.

## Stronger blind testing

Create a new consumer bank separately from the existing sealed evaluation, which
remains unopened. A curator outside the implementation work should create
realistic synthetic tasks or use consented issue reports. Include novice wording,
misleading premises, negation, compound requests and custom compositions whose
correct answer includes an explicitly bounded proposal.

Freeze intent, essential/conditional support and unacceptable claims before
execution. Have a separate evidence reviewer check the rubric against the pinned
scope. Run baseline/candidate trials in independent fresh contexts with fixed
model settings and randomized candidate labels/order. Give graders answers and
evidence without revealing which build produced them. Repeat actual caller runs
to measure variability; repeating a deterministic plan measures stability only.

Once a detailed failure is shown to an implementer for fixing, retire that case
into regression and replace it for future holdout measurement. Public cases,
visible paraphrases and guided focuses remain development evidence. Procedural
instructions to a caller are not a technical isolation boundary; stronger trials
should restrict its filesystem and tool access to the consumer surfaces.

## Agent-generated requests

An [agent-generated consumer experiment](consumer-generated-results.md) uses two
stages: question writers receive only the domain or a broad idea, then fresh
answer callers receive the frozen questions and installed tools. Freeze literal
user requirements before answers, rather than designing expected answers around
returned evidence. Retain every generated request, including duplicates,
ambiguities and unsupported requests. Keep request resolution separate from
truthful abstention and supported application proposals separate from guarantees.

Make exact questions, observable call sequences, arguments, complete responses
and final answers inspectable. Report topic concentration and generated-question
validity alongside answer findings. More generated instances do not automatically
mean broader coverage or independent models. Use exposed cases for regression;
new blind cohorts should generate fresh questions before retrieval changes.
The [follow-up diagnosis](consumer-followup-audit.md) separates five partials
into missing fact detail, already delivered mechanisms and application recipes,
and explains the 154-call cost without treating every recovery call as waste.

## Other audits in priority order

| Audit | Main failure to expose |
| --- | --- |
| Persistent packaged session | Rejection poisons later calls, connection hangs, scope/state carryover or a stale process after upgrade |
| Setup and configuration | Wrong command/arguments, path quoting, incorrect mode, missing tool permissions or instructions |
| Project/worktree state isolation | Saved scope bleeding between contexts or surprising inheritance after restart |
| Client contract and provenance | A client requires structuredContent, unresolved compact references, oversize results or incorrect paging |
| Recovery and answer boundaries | High-overlap distractors, missing conditional warnings, or invented behavior for custom APIs |
| Disposable fault tests | Missing/tampered package files, unavailable dependencies, unwritable state, interrupted installation; previous installation remains intact |
| Upgrade and rollback | Wrong build connected, accidental state loss or shared state; use side-by-side installations and explicit restart |
| Cross-client and platform checks | GUI rendering/tool-policy differences or unavailable wheels on a named OS/architecture/Python combination |
| Meaning-preserving retrieval variants | Harmless rewording, aliases or question order lose critical support; distinguish actual semantic changes |
| Bounded soak and concurrency | Latency growth, leaked resources, cancellation failures or settings races |

First run the persistent artifact journey and one fresh setup/client pilot.
Expand platforms and resilience checks after those results are clear. Broader
auditing does not resume deferred knowledge slices or authorize fact/DB changes.

## Pilot executed during this investigation

A retained discovery8 candidate archive passed a narrow staged-artifact pilot:
31 payload files verified and nine real MCP calls across a persistent session and
a restarted process. The probes covered help, missing-plan repair, lookup,
compact provenance references, discovery/full fetch, unsupported scope, schema
rejection followed by a successful call, and restart.

The pilot used existing dependencies and scratch state, with no dependency
installation or modification of an existing install. It qualifies neither a
clean install nor the later discovery11 source, and it is not a GUI-client or
blind answer-quality trial. The retained archive is not asserted to have the
published RC checksum. Its SHA-256 is
`ea0325ba91593bcdaadbd8409f2f5d95eea63af30ea763007574f89a4cd8b3f6`.
The script, receipt and complete calls are in ignored
`test-output/conditional-recovery/downstream-pilot.py` and
`downstream-pilot-run1/`.

The handshake reports MCP package version `1.26.0`, while the manifest identifies
the retrieval runtime as discovery8. The handshake alone therefore cannot verify
which retrieval build a client is using. This historical ambiguity is addressed by the subsequent
[discovery12 identity change](consumer-v2-results.md), without modifying the pilot artifact.

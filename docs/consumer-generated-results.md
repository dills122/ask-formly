# Agent-generated consumer journeys

**2026-10-28 — exploratory discovery12 test.** Twenty question writers generated
requests before accessing ask-formly. Twenty separate fresh callers then attempted
the exact requests through the frozen installed package. This tests generated
consumer demand and observable answer flows, rather than another repetition of
maintainer-written questions.

## Design

Ten writers chose their own topic within Formly 6.3.12 core/Material. Ten received
only a broad idea: dynamic visibility, nested models, repeated sections,
asynchronous choices, validation timing, JSON Schema conversion, custom field
integration, initial values, reset workflows, or registration and reuse. Writers
received no corpus, source, previous cases, fact IDs, tool schemas or MCP
initialization. All twenty produced valid question JSON with no tool use observed.
There were no exact duplicate questions; all outputs were retained.

Question generation and answering used different fresh client sessions. The
question bank was frozen before an independent curator extracted 75 literal
required decisions, separate optional detail and ambiguity notes. That checklist
was frozen before answer dispatch. Callers received only their exact question,
installed tools and general test constraints. They wrote their own plans with a
limit of eight non-help and two help calls. No answer, question or criterion was
revised in response to an outcome.

The assessment separates supported completion, partial resolution, bounded
abstention and unsupported claims. A clearly labeled application proposal may
combine supported library mechanisms without requiring an existing whole-recipe
fact. An honest evidence gap is distinct from fulfilling the requested work.
Unknown missing support cannot automatically be attributed to a missing fact or
a ranking defect. Neither returned evidence nor a proposed recipe establishes
executed application behavior.

## Artifact and isolation

The unchanged discovery12 package is
`formly-model-free-discovery-12+b642f644b08c`, archive SHA-256
`8e1e1501469ea066d6731da7e9a8c9564746bd030ba6e0a28a206f9e062fd03c`.
This experiment reuses the prior isolated consumer installation; it is not
another fresh-install test. The question bank SHA-256 is
`182aeb3038bed8b952e04f1054a95cb96a26f7b5b121f1502d90e6ac1e636009`.

The actual Codex CLI uses ignored user configuration, ephemeral contexts and
outside-repository scratch directories. Generators have no MCP configuration;
answer callers have only ask-formly explicitly configured. Built-in tools may
exist, so procedural restrictions and raw trace inspection do not amount to a
technical filesystem isolation guarantee. No model override is supplied; resolved
model and reasoning settings remain unknown unless emitted by the client.

## Findings

Independent agent assessment found **15 supported-complete and five partial**
answers. Across 75 frozen required decisions, 67 were resolved, six partially
resolved and two unresolved. No substantive unsupported claim was established.
This is a supported-proposal assessment, not an executed application test.

| Arm | Supported complete | Partial |
| --- | ---: | ---: |
| Free topic | 8 | 2 |
| Broad idea | 7 | 3 |

All 40 generation/answer sessions completed. Answer callers made 154 MCP calls:
29 help, 20 lookup, 76 discovery and 29 fetch. There were no plan-refinement
responses. Every caller stayed within eight non-help and two help calls, with
no prohibited tool use observed. Three help calls failed on page sizes above 32;
two help-topic requests returned unknown topics. Failures remain in the traces.
Maximum UTF-8 JSON reserialization of a CLI result envelope was 29,891 bytes;
this differs from transport-wire size. Discovery returned 757 candidates and
fetch returned 140 facts, both counts including repeats.


The free-choice arm has eight supported-complete answers and two partial answers:
F06 and F09 explicitly leave beneath/under-input Material error rendering
unestablished. Across its 40 literal decisions, 38 are resolved and two partially
resolved. No substantive unsupported claim was established by the independent
agent reviewer. The proposals were not executed in an application.

F08 receives a help error after requesting `limit: 40`; the tool states the valid
range is 1–32. The caller still completes a supported answer within budget. This
argument error remains visible separately from request resolution.

The seeded arm has three partials: S05 leaves immediate correction while typing,
pending-submit integration and part of untouched-field error presentation
unresolved; S07 leaves wrapper-versus-own error markup partly unanswered; S09
leaves exact dirty/touched/error cleanup and dependent country/state reset wiring
incomplete. Its other seven responses resolve their literal requests as supported,
unexecuted proposals. Its 35 decisions are 29 resolved, four partial and two
unresolved.

The rendering gaps are concrete consumer needs to investigate next. Their
traces do not distinguish absent knowledge, missed retrieval, or selection within
the budget. Preserve the original attempts before conducting diagnostic replays;
do not classify the behavior as unsupported by Formly from these gaps.

## Follow-up candidates

1. **Advertise help bounds.** F08, S06 and S09 request limits 40, 100 and 50.
   The tool rejects them with the enforced 1–32 range. The captured tool schema
   for this same frozen build declares an integer/default 16 without minimum or
   maximum (`consumer-v2/transport/run1/receipt.json`). That is a concrete schema
   discoverability gap to fix in a subsequent candidate.
2. **Trace Material error evidence.** Replay F06/F09/S07 diagnostically to
   distinguish available-but-missed support from missing fact detail or a genuine
   qualification boundary. Preserve these original partials.
3. **Separate timing/reset contracts from application policy.** S05/S09 need
   targeted evidence review for validation/display/reset state and asynchronous
   option coordination. Avoid turning application design choices into universal
   library guarantees.
4. **Investigate discovery cost.** The 76 discovery calls provide real selection
   traces. Measure whether repeated paging supplied useful new support before
   changing ranking or increasing budgets. Unknown help topics also warrant a
   discoverability check.

## What this experiment can show

The free-choice arm clusters heavily around conditional visibility and validation;
unique wording is not equivalent to broad coverage. Broad ideas produce more
varied questions, including asynchronous race handling and initialization policy.
This contrast is descriptive, not a controlled statistical estimate. The questions
are agent-generated hypothetical needs, not sampled real user reports, and the
model is not independently identified. The exposed cases are development evidence,
not a sealed holdout or whole-library benchmark.

The primary artifact is the ignored `test-output/consumer-generated-v1/journeys/`
index and individual dossiers. Each retains the exact question, generation arm,
ordered observable tool calls and arguments, full response JSON, final answer and
links to raw traces. Session times and response sizes are recorded where available;
per-tool latency is unavailable when the CLI emits no timestamps. No hidden
reasoning is inferred from the sequence.

Protocol, generation and caller freezes, curator checklists, raw streams and
independent assessments remain in `test-output/consumer-generated-v1/`. Facts,
corpus/compiler inputs, installed DB and sealed evaluation remain locked. This
experiment does not authorize fixes, knowledge admission or publication.

## Preservation and maintenance checks

Archive, installed payload and runtime checks matched before and after the run.
All 87 protected source/data hashes, including the existing installed DB, matched.
No runtime implementation or fact changes were made during the experiment.
Raw generation/caller evidence is hash-frozen separately from derived dossiers
and independent assessments. Source/document validation passed; the full
maintenance command remains unavailable because this worktree lacks its compiler
environment. That limitation is separate from these completed client sessions.

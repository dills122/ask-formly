# Issue 21: caller usability follow-up

For the subsequent read-only investigation, see
[Initialization and key-collision audit](#initialization-and-key-collision-audit-2026-10-28).

This implements the maintenance findings from [Live Project Audit #21](https://github.com/dills122/ask-formly/issues/21).
The RC demo repair runtime identity was `formly-model-free-discovery-8`; knowledge
remains the same 192 facts / 36 documents for Formly 6.3.12 core/Material.

## Delivered changes

- Exact condition-copy requirements and actionable validation errors, required
  question reasons, explicit request/scope semantics, and schema-enforced 1–16
  fact-ID fetch limits.
- `help_formly` with a valid example, workflow, limits, and scoped paginated topic
  and fact-ID inventory.
- Field-weighted lexical ranking, lowercase API recognition, conservative prose
  inflections, and removal of scope-only prefixes from topical scoring. Matching
  diagnostics distinguish recognized identifiers from semantic relevance.
- Fair candidate selection beyond four ranks, under fact-count and byte ceilings.
  A question stops when its next ranked record cannot fit; smaller low-ranked
  records do not fill the remaining space ahead of it.
- Existing scoped `see_also` links, bounded neighbor expansion, global omission
  previews, explicit recovery actions, and discovery over the complete omitted
  list rather than only the preview.
- Shared complete provenance in `compact-v1`, plus an explicit full-fetch format.
- [Design-question guides](knowledge-recipes.md) for hiding, collisions, steppers
  and initialization, separating admitted mechanisms from application proposals.
- Default model-free regression and offline transport suites in source CI.

## Response contract and client migration

The active repair/discovery server returns **one complete JSON text packet** rather
than duplicating it in both text and `structuredContent`. SDK consumers should use
`result.structuredContent` when present, otherwise JSON-decode the first text
content item. Check `isError` and the packet status before using evidence. This
preserves the complete data for ordinary text-based MCP clients.

In `compact-v1`, `citations[id].authored_source_ref` resolves in `sources`, and
each `evidence_refs` entry resolves in `evidence`. Facts retain their conditions,
limits, applicability and eligible related links. Fetch selected IDs with
`get_formly_facts(response_format="full")` when inline provenance is needed.
The full format has a separate 48,000-byte limit and may require fewer IDs.

Successful compact lookup/fetch packets have a 28,000-byte UTF-8 JSON ceiling;
the active serialized MCP result has a 30,000-byte ceiling. Client rendering
policies may impose other limits. Discovery uses its separately documented
24,000-byte candidate page limit. Help and validation errors are separate control
messages, not evidence packets.

`questions[].omitted_indexes` refer to the bounded global `omitted_candidates`
preview. Counts disclose the full omitted population, and discovery pages that
full population. A globally delivered fact is not also an omitted fact. Large
request echoes are explicitly replaced by a fingerprint; plans are summarized.
The caller must retain its original request and plan for recovery.

Restart the server after installing updated code and manifest together. Old
running processes retain their old contract. This source change does not publish
a new archive, change client configuration, or qualify a release on another host.

## What the development replay establishes

Four fixed issue-informed plans were replayed against an isolated DB compiled
from the unchanged canonical inputs. Its SHA-256 is identical to the active
launcher DB pin, `f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09`.
The installed DB was not rebuilt or replaced. G1 reproduces the issue's original
37,856-byte baseline response exactly; the other appendix plans were summarized,
so their missing reasons/prefixes were restored and are not claimed as exact
historical transcripts.

| Case | Baseline packet bytes | Updated packet bytes | Issue expected IDs in first packet | Additional known-ID fetches |
| --- | ---: | ---: | ---: | ---: |
| Hide/value/registration | 37,856 | 26,258 | 5/5 | 0 |
| Stepper/model scope | 59,660 | 27,116 | 5/8 | 1 |
| Initialization | 52,061 | 27,801 | 5/12 | 2 |
| Dynamic key collisions | 49,752 | 26,731 | 3/9 | 2 |

The fetch rubric supplies the expected IDs and uses at most four per fetch;
all expected records and their provenance are recoverable within those calls.
This measures known-ID recovery, not an autonomous caller's discovery cost.
The first packet supplies all key hide/value/registration evidence. The other
cases still need additional registration/key-path, default/preset/state, or
shared-validator/key-identity support before a complete answer.

JSON Schema `uniqueItems` and Material `compareWith` positive controls retain
their target fact first. Unsupported v7 returns no facts. An unknown API can still
produce lexical candidates with a no-recognized-identifier warning; it must not be
answered as supported, nor treated as proof of corpus-wide absence.

These are development observations, not a broad relevance or precision score.
The issue's proposed 80% first-pass ID target remains unmet for G2–G4. There was
no blanket topic penalty, unconditional whole-topic inclusion, semantic model,
or change to facts to force the target to pass.

## Remaining boundaries

The existing `see_also` graph is exposed; new semantic edge kinds are not admitted.
Complete Material stepper recipes, generic Angular payload rules, a general
`resetFieldOnHide` configuration guide and duplicate-field outcome matrices need
separately scoped evidence. Guidance documents do not turn those into guarantees.
`candidate_only` is an assessment status, not a per-fact runtime execution flag.
Historical browser failures B06/B13 remain visible and unchanged.

Full local qualification still requires the provisioned compiler, MCP and model
environments. Source-only and model-free transport checks do not qualify the
model-backed path or execute Angular/Material fixtures. New client/platform
qualification and additional library versions remain separate work.

## Verification recorded for this change

The expanded source command passes preservation checks, authored lint and its
274 fixture tests, including 42 model-free contract/ranking/response tests,
29 repair/help/stdio tests and 6 discovery tests. The updated pinned runtime passes its
21-file doctor and a real offline-guarded stdio smoke in an isolated runtime
using the byte-identical verification DB. The smoke covers help, lookup, compact
provenance resolution, discovery and explicit full fetch.

One fresh caller using only server instructions/tool descriptions/help answered
the hide question on its first lookup, with no schema error, repair or follow-up.
Its help example was closely matched to the question, so this is narrow onboarding
evidence. A transport replay of the identical call after removing duplicate
serialization returned the identical evidence in **29,314 SDK-result bytes**,
down from 55,486. That replay is not a second independent caller generation.

Independent review instance 1 found no actionable implementation defect and
recorded the first-pass/recovery limitations. The transport correction received
a separate fresh-context review (instance 2: Ready, no actionable findings). A
31-file local alpha archive also passed manifest verification and its real stdio
self-test using existing dependencies; this was not a fresh dependency installation.
Full local maintenance still stops on missing
worktree environments; these results are not full model-backed qualification.

## Initialization and key-collision audit (2026-10-28)

**Disposition:** refine retrieval, recovery and evaluation before expanding the
fact set. All 21 expected fact IDs in the existing initialization/collision rubric
are present and eligible in the unchanged 192-fact baseline. That does not make
every requested behavior covered or every expected ID necessary for an answer.
Linked examples remain deferred and were not used to supply missing support.

### Method and limits

Read the current claims, contexts, conditions, limits, source quotations and links
for the target facts; checked other existing claims for overlapping support.
Replayed the existing public G3/G4 plans through the unchanged repair/service
implementation, inspected direct and neighbor-expanded ranking, traversed all
omitted candidates in pages of eight, and traced rejected packet additions.
Ten diagnostic queries and four subsequent mechanism probes tested focused
wording, natural language and identifier forms. The latter are exploratory
diagnostics, not a frozen acceptance set or evidence of a fix.

The replay reproduced initialization's nine delivered facts / 29,704 serialized
SDK bytes and collisions' seven / 28,505 bytes. These contain respectively 5/12
and 3/9 of the historical expected IDs. The known database SHA remained
`f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09`.
Raw requests, rankings, packets, discovery pages and trace scripts are retained
locally under `test-output/fact-retrieval-audit/`.

This is stored-evidence and retrieval diagnosis, not a new upstream source audit,
Angular execution, autonomous-caller trial or whole-library relevance score.
Graph coverage was checked for the retrieval implementation and direct source
inspection was used to verify the paths involved. No source facts, ranking code,
compiler, database, runtime manifests or sealed evaluation were changed.

### Initialization: existing facts lost at different stages

The following IDs are abbreviated by topic where unambiguous. Rank is the best
position in any of G3's three question candidate lists; discovery position is in
the deduplicated omitted stream, not an overall relevance judgment.

| Missing expected fact | Best rank | Discovery position | Diagnosis |
| --- | ---: | ---: | --- |
| `core-configuration-lifetime/rebuild-clears-validators` | 5 | 1 | Useful warning already present; packet selection/budget, then recovery |
| `initial-values/default-value-is-fallback` | 4 | 3 | Clear existing fact; packet selection/budget |
| `extensions-presets/preset-setup-reference` | 6 | 8 | Existing setup support; budget/competition, then recovery |
| `public-api-configuration/preset-partial-overrides` | 10 | 20 | Existing detailed support; ranking and recovery depth |
| `initial-values/model-preferred-for-computed-initial` | 10 | 21 | Existing decision guidance; broad-query ranking and recovery depth |
| `initial-values/changed-model-input-rebuilds` | 11 | 24 | Ranking plus under-specified factual condition |
| `expressions-notifications/formstate-observation` | 49 | 85 | Identifier/intent matching and recovery depth |

The first packet already contains lifecycle and extension-phase facts. Its third
question names `options.build`, `resetModel`, `updateInitialValue`, `formState`,
model and defaults together. Rebuild/reset operations therefore compete with
initial-value guidance. The selector fills a global bounded response by
interleaving per-question ranks; nine records consume almost the entire budget.
Appending `default-value-is-fallback` would produce 31,506 SDK bytes; appending
`rebuild-clears-validators` would produce 33,635. Those omissions are real budget
decisions, not an absent fact or an arbitrary four-result cap.

Running each original question separately recovered several omitted records;
focused questions did better still. The model-versus-default question ranked
`default-value-is-fallback` first. The preset-override question ranked
`preset-partial-overrides` first and setup second. These observations support
intent separation and deliberate follow-up calls, not larger unbounded packets.

**Concrete identifier mismatch:** with the otherwise identical query
`How does options.formState trigger expression updates?`, the observation fact
ranked 22nd; using bare `formState` ranked it first. Retrieval preserves dotted
identifiers, while this fact uses bare `formState`. A narrowly defined, tested
alias policy is worth investigating. Blindly stripping all qualifiers would risk
conflating unrelated APIs.

**Coverage correction:** `public-api-configuration/defaults-order-before-wrapper-fallback`
already specifies the order of type, directly extended type, optionsTypes and
component-instance defaults, including wrapper fallback. It ranked fifth in G3's
configuration question and first in a focused ordering query. Together with
preset timing/override and reverse-merge facts, this provides substantial support
that the old expected-ID rubric and broad "ordering is missing" description omit.
It does not establish arbitrary recursive inheritance, Angular provider order or
every configuration combination. Do not duplicate it as a new fact.

### Key collisions: terminology, links and budget

| Missing expected fact | Best rank | Discovery position | Diagnosis |
| --- | ---: | ---: | --- |
| `public-field-api/key-id-name-roles` | 4 | 2 | Core distinction already clear; packet selection/budget |
| `array-operations/add-coordination` | 3 | 3 | Budget; applicable only when the request actually needs a repeater |
| `core-configuration-lifetime/key-paths` | 8 | 8 | Existing support; ranking/budget/recovery |
| `hiding-and-visibility/shared-key-control` | 14 | 29 | Shared-control context is hard to reach; conditional need |
| `array-operations/remove-coordination` | 28 | 57 | Ranking/recovery; conditional repeater need |
| `core-configuration-lifetime/shared-validator-ownership` | 30 | 65 | Existing precise support, weak matching and missing relationship |

The natural query `Two dynamic sections both have a name field. How can I avoid
their values colliding?` put a Material appearance fact first. The keyed-group
fact ranked tenth and was not delivered. Diagnostics recognized `name` and
reported `identifier_match`, while `section` and the collision term were unmatched.
A recognized DOM/config name is not enough to establish that the main intent was
matched. An explicit same-key/model-path query ranked keyed-group scope first.

In the original broad plan, the useful key/id/name fact ranks fourth in the
namespacing question, but appending it to the combined result would require
31,339 SDK bytes. The plan's third question expands "dynamic" into rebuilding,
hiding and repeating; operation and repeater facts consume room before that
fundamental distinction arrives. Do not treat every plan-introduced API as an
equally important requirement from the user.

`shared-control-lookup` and `shared-validator-ownership` both have no outgoing
stored links. The latter explicitly describes composing validators from visible
participating fields, but ranks poorly in broad collision questions. A focused
shared-control validator question ranks it first. A reviewed relationship between
these facts could improve recovery without inventing another claim. Existing
neighbor expansion is bounded, uses only the first two seeds, and takes at most
one eligible link per seed; simply adding many links would not guarantee delivery.

### What needs factual work

| Area | Current disposition | Proposed next investigation |
| --- | --- | --- |
| Initial model versus defaultValue | Existing usable facts, including equivalent defined-value/fallback records in another topic | Improve retrieval and account for equivalent evidence; review duplication before adding facts |
| Preset configuration and default ordering | Substantial existing support; several distinctions can be composed | Improve task-to-fact mapping and links; preserve merge/precedence qualifications |
| Later changed model input | Claim says "qualifying" change and condition says "passes the component change condition"; stored source quotation is similarly indirect | Verify the exact pinned change predicate and author a precise bounded clarification if supported; do not invent a reference-change rule |
| Shared-key hiding | Conservative existing claim says "does not necessarily"; lacks a useful positive condition in its limits | Review pinned source to make the exception condition explicit and link it to shared-control behavior |
| Avoiding collisions using distinct model paths | Keyed scope, key-path and key/id/name facts already support the recommendation | Ranking, vocabulary and recovery work first |
| Competing fields at the same full path | Existing lookup, validator and hide facts cover parts; they do not specify a complete type/props/default/disabled outcome matrix | A separately scoped source/fixture investigation is needed before promising which configuration wins |

Duplicate **type registration** has its own detailed fact; it is not evidence for
duplicate **field model paths**. Ancestor disabled-expression behavior likewise
does not answer competing same-control disabled-state ownership. These are genuine
boundaries in the inspected fact set, not permission to fill gaps by inference.

### Recovery and evaluation need separate corrections

G3 exposes 166 omitted candidates (21 pages of eight); G4 exposes 179 (23 pages).
The existing replay policy reads only two pages and then fetches at most four
facts selected by word overlap with the original request. For each case, three
missing expected facts occur within the first 16 candidates, but the heuristic
recovers only one: rebuild/validators for G3 and key/id/name for G4. Other expected
facts occur beyond the two-page window. This distinguishes **caller selection
loss** from **discovery depth**, and neither is proof the server cannot return them.

The collision request's everyday language and initialization request's vague,
misspelled wording are particularly poor inputs to that recovery heuristic.
The 6/12 and 4/9 recovered scores describe this fixed policy, not an autonomous
agent's ceiling. Prior oracle-ID fetch counts are not a fair comparison.

Broad OR retrieval can admit most of the corpus. Scope words are removed during
reranking but remain in candidate generation; removing only the scope prefix in
diagnostic searches reduced some candidate counts (for example G3 configuration
120 to 88) without solving all relevance problems. This is a candidate-generation
cleanup hypothesis, not justification for dropping legitimate lower-ranked facts.

The old expected-ID lists also mix essential and conditional support. Array add
and remove are not automatically required for independent dynamic sections;
formState observation is not essential to every initialization answer. Equivalent
default-value facts and existing configuration-order facts can support an answer
without satisfying the old exact-ID list. Preserve those historical scores, but
freeze a new relevance rubric with **essential, conditional, equivalent support,
and unsupported** dispositions before assessing improvements.

### Recommended order of work

1. Freeze a small public regression set spanning natural language, API-qualified
   paraphrases, initialization facets and collision facets. Define essential
   answer distinctions and acceptable supporting alternatives before tuning.
2. Investigate scoped identifier aliases, intent matching and candidate-generation
   noise. Keep negative/scope controls and prevent blanket family demotion.
3. Improve answer-facet coverage under the existing 28 KB packet / 30 KB SDK limits:
   prioritize essential distinctions, keep full conditions/provenance, and use
   targeted follow-up queries when the combined request cannot fit.
4. Test recovery by unmet question/facet rather than only original-request word
   overlap. Make page limits and incomplete support visible. Compare fixed-policy
   results with fresh callers without providing expected IDs.
5. Review a small explicit set of factual clarifications and links. Separately
   investigate unresolved same-path outcomes; do not broadly rewrite or expand
   the corpus to compensate for retrieval errors.

No fix or new acceptance threshold is approved by this audit. These findings
support the current priority of improving existing facts and retrieval; example
storage and promotion remain deferred.

## Retrieval refinement implementation (2026-10-28)

The subsequent authorized implementation freezes an answer-focused development
rubric and improves identifier matching, selection and recovery. Its source
runtime manifest is `formly-model-free-discovery-9`. The published RC remains
unchanged; this is not an installation, promotion or release. The authored facts,
corpus, compiler, schema and baseline DB are unchanged.

### Frozen rubric

The [refinement package](../poc/contextual-kb/retrieval_refinement_v1/README.md)
contains 13 gate cases plus the two historical broad G3/G4 diagnostic cases.
There are 23 essential support facets, with explicitly accepted equivalent facts,
separate conditional support, and forbidden unsupported claims. A fact-ID score
does not certify the generated answer; manual fresh-caller review is required.

Revision 2 was frozen before runtime edits or evaluation. Pre-run semantic review
removed an invalid alternative for the DOM-name/model-key distinction; the first
draft was retained as superseded evidence. No rubric change followed observed
results. Input SHA-256 values are recorded in `freeze.json`:

- Cases: `54c1027a24ea95fcdd1f5ecaade50b41dd8d32bab3f6be321e2f9543c18efdd8`
- Rubric: `38d8e9aea087bb5a92d2c94a962ed26800121d1d86ff3bfc1643f64a41dadbe8`
- Policy: `3e9a451a89a83984ef6759437e8a65fb6f3fdea1e12ee00078e608623d7a41b0`

The rubric-blind executor uses at most four follow-up calls: it selects an unmet
original-plan question using observed text coverage, discovers candidates and
fetches selected returned IDs. It does not receive expected IDs. The baseline
uses global discovery; the candidate exposes the optional question selector.
This API-aware difference is intentional and recorded, not identical call traces.

### Implemented behavior

- Exact approved spelling aliases normalize `options.formState` and
  `field.options.formState` to `formState`, and qualified `hooks.onInit` forms to
  `onInit` for retrieval. Unknown qualifiers and distinct APIs such as
  `props.disabled` versus `templateOptions.disabled` remain distinct. Original
  requests and returned facts are not rewritten.
- Scope-only prefixes no longer seed FTS candidates. Collision wording with
  explicit model/value intent receives disclosed lexical key/path/group hints.
  These are matching aids, not claims that a DOM name is a model key.
- Selection shrinks the optional omitted-ID preview before rejecting the next
  ranked complete fact. It retains provenance, conditions and limits, still
  respects both response budgets, and does not backfill smaller low-ranked tails.
  Complete omissions remain discoverable, even when the preview becomes empty.
- `discover_formly_candidates(question_index=...)` pages omissions for one
  original-plan question, excluding globally delivered facts. It echoes the
  question reference and retains the original scope/condition gate. Omission
  metadata, help and caller instructions explain this recovery path.

The service remains stateless: it validates the supplied request and plan but
cannot prove that another otherwise valid plan is identical to a prior call.
Callers must repeat the original request, plan and resolved scope. Exhausting a
call budget does not establish full support or absence of library behavior.

### Verification and remaining limits

All frozen automated gates passed across 90 actual stdio case executions
(15 cases × three deterministic repeats × baseline/candidate):

| Essential support per repeat | Baseline | Candidate |
| --- | ---: | ---: |
| First lookup | 21/23 | 23/23 |
| After bounded recovery | 22/23 | 23/23 |

The qualified formState query and natural-language collision query gained their
missing essential support. Every gate case retained at least its baseline
first-pass facet count. Hide/registration, JSON Schema uniqueItems, Material
compareWith and unsupported-version controls passed. Maximum candidate SDK
result was 29,897 bytes; limits remain 28,000 packet bytes / 30,000 SDK bytes.

The historical broad questions are not silently relabeled as fixed:

| Historical diagnostic | Baseline first / recovered | Candidate first / recovered |
| --- | ---: | ---: |
| G3 initialization | 5/12 → 6/12 | 6/12 → 6/12 |
| G4 collisions | 3/9 → 4/9 | 4/9 → 4/9 |

These selected-ID diagnostics remain distinct from the new essential-facet rubric.
The new frozen recovery policy did not improve their final recovered count;
broader query decomposition, recovery selection and the fact clarifications from
the audit remain follow-up work. No whole-library answer-quality score is claimed.

Source checks passed 319 tests. The updated 21-file model-free manifest passed
doctor and a real offline-guarded launcher smoke in an isolated runtime with the
unchanged verified database. The first scratch smoke lacked the copied
`offline_guard.py`; adding that unchanged helper fixed the scratch setup and the
smoke passed. All 86 captured fact/corpus/compiler/schema/DB path hashes matched.
Full local maintenance still requires the missing provisioned worktree environments.

A fresh rubric-blind caller inspected four questions through the actual MCP
transport. Qualified formState and collision isolation were supported on the
first lookup. Initialization guidance retained the pre-build condition and
subscription-cleanup distinction. For competing configurations on the same full
key path, the caller exhausted four discovery pages and explicitly declined to
claim a universal winner. One missing-`--arguments` CLI setup error was corrected
and recorded; there were no MCP validation errors. These four answers are narrow
evidence, not general autonomous-recovery qualification.

Independent review instance 1 found no actionable defects and rated the bounded
source refinement Ready. The reviewer independently reproduced all 319 source
tests, regraded the 90 saved executions, checked protected hashes and runtime
pins, and verified that fresh-answer citations and provenance matched delivered
evidence. The freeze hashes were verified; pre-implementation freeze chronology
is recorded process evidence rather than independently provable Git history.
No additional review instance was required. Replay and caller evidence remain in
`test-output/retrieval-refinement-v1/`; publication and installed-runtime promotion
have not been performed.

## Focused recovery follow-up (2026-10-28)

The next Ruflo-coordinated pass adds optional `focus` to
`discover_formly_candidates`. It names an unmet distinction in 1–500 nonblank
characters and reranks only the original scoped omissions. Original request,
plan, conditions, scope and candidate membership remain unchanged. The default
order and first lookup are unchanged. Keep the same focus and question selector
while paging; restart at offset zero when either changes. Matching diagnostics
are lexical navigation signals, not support or absence certificates.

The source manifest is now `formly-model-free-discovery-10`; the published RC
remains discovery8. No installed runtime or knowledge was promoted. All 86
protected fact/corpus/compiler/schema/DB hashes remain unchanged.

### Separating caller selection from server recovery

The original frozen rubric remains byte-identical and passed all 90 stdio
executions, retaining 23/23 initial essential facets. A separately frozen
[supplemental comparison](../poc/contextual-kb/recovery_refinement_v2/README.md)
uses the original broad initialization/collision plans and four essential facets
for each. Preset, formState, hiding and repeater branches remain separately
reported conditional evidence. Its fixed public intent policy is guided replay,
not autonomous planning or held-out generalization.

Twenty-four factorial executions compare both source versions with both caller
policies. Each uses one lookup plus four follow-ups, with unchanged transport
ceilings. Results per repeat:

| Source / policy | Initialization essential / historical | Collision essential / historical |
| --- | ---: | ---: |
| Baseline / original | 2/4; 6/12 | 2/4; 4/9 |
| Baseline / guided | 4/4; 10/12 | 3/4; 5/9 |
| Candidate / original | 2/4; 6/12 | 2/4; 4/9 |
| Candidate / guided | 4/4; 9/12 | 4/4; 7/9 |

Better caller selection alone recovered the initialization essentials. The focus
API additionally recovered collision validator ownership. It is not uniformly
better for every branch: the guided baseline recovered preset partial overrides,
while the focused candidate missed that conditional detail. No policy or rubric
was tuned after these outcomes. The candidate still omitted rebuild-validator
clearing, changed-model-input rebuilds, key-path detail and repeater removal from
the historical lists. These deeper/conditional misses remain open; eight delivered
essentials do not establish exhaustive support for the broad plans.

Maximum SDK response was 29,775 bytes in the factorial and 29,897 in the original
frozen comparison. All automated gates passed. Source checks passed 329 tests;
the 21-file isolated runtime doctor and offline-guarded launcher smoke passed
against the unchanged verification DB. Full local maintenance still stops on the
missing worktree compiler environment and is not claimed as qualified.

A fresh caller received only two user questions and live tool schemas/help. It
answered initialization after one lookup plus discovery/fetch, and collisions
after one lookup plus four follow-ups. It recovered shared validators and
explicitly declined a universal same-path type/props/default/disabled winner.
The answers preserved pre-build/default conditions, hook cleanup, scope and
formState limits. This is two-answer evidence, not whole-library accuracy.
Raw calls, answers and reports remain in `test-output/recovery-round2/`.

The [reconciled issue backlog](knowledge-completion-backlog.md#issue-21-follow-up-order)
identifies G2 stepper/model-scope retrieval and weak-match follow-ups as the next
retrieval audit. Changed-model and shared-key-hide clarifications, missing outcome
matrices, typed relationships and durable examples remain separately scoped work.

That subsequent [library-support audit](library-support-audit.md) is complete.
It found existing support for all eight focused facets, plus a conditional G2
historical coverage drop from 5/8 to 4/8 after the earlier source refinement.
Guided recovery reaches 6/8; the passing essential rubric does not erase that loss.

Independent review instance 1 verified the source checks, regraded all 114
executions, checked protected/runtime hashes and matched every fresh-answer
citation and provenance object to delivered evidence. Its minor backlog wording
correction was accepted; no runtime correction was needed. Final verdict: Ready
for this bounded source change, with no actionable findings remaining.

## Conditional control lifetime and evidence selection follow-up

The discovery11 source change adds bounded, search-only registration and
unregistration vocabulary for explicit control-lifetime questions. These are
contrasting consequences, not synonyms. It preserves original request/fact
polarity and public API names. Ambiguous type/component/provider/wrapper
registration wording is excluded unless an explicit hide/show/unregister action
establishes lifetime context. Diagnostics disclose the expansion; packet budgets
and the selection algorithm are unchanged. No facts or installed DB changed.

Production help and caller guidance now prioritize the exact missing claim and
its conditions over titles, shared words or vocabulary novelty. When a proposed
design hides fields, control registration and value retention need separate
support. If discovery repeats already-supported concepts, narrow focus to the
remaining distinction while preserving the original request, plan and conditions.

The [conditional comparison](../poc/contextual-kb/conditional_recovery_v3/README.md)
retains its failed first revision: broad recovery plus either lexical selector
missed key-parser evidence, leaving 14/15 facets. A second public development
revision narrowed only that recovery focus; cases, fifteen facets, gates,
selectors and budgets stayed unchanged. This is an outcome-informed development
iteration, not held-out validation or a semantic-selection breakthrough.

All 120 final revision-2 executions passed. The initial G2 control warning is
restored, bringing historical first-pass delivery from 4/8 back to 5/8; recovery
reaches 6/8. Claim-first scoring helps select the warning on the baseline page,
but both selectors need the narrower focus to select the key parser. Named
component registration and registration options remain outside this bounded
recovery result. Prior frozen v1/v2 comparisons passed 90 and 24 executions.
Maximum SDK response in the new comparison was 29,990 bytes.

Source checks passed 337 tests, including six new evaluation-harness tests. The
isolated source11 runtime passed its 21-file integrity check and offline launcher
smoke with the unchanged verification DB. Full local maintenance still lacks the
worktree compiler environment; no model-backed or installed-runtime promotion is
claimed. The published RC remains discovery8.

Two fresh targeted callers' answers needed one lookup each and preserved the
hide/value/shared-control and key-syntax qualifications. A separate recovery-only
caller inherited a real G2 lookup and used three discoveries plus one eight-fact
fetch. It supported a proposed composition while explicitly leaving Material
stepControl wiring, lazy-content behavior and runtime transitions unverified.
That latter trial tests recovery from a supplied state, not independent planning.

The [consumer-testing direction](consumer-testing.md) separates scripted
regressions, blind answer trials and actual installation/client journeys. A
retained discovery8 archive passed nine persistent/restarted-session probes using
existing dependencies. That is not clean-install qualification of discovery11.
Next testing work should use one frozen archive, a fresh setup operator and a
named client, followed by independently graded callers who author their own plans.
Raw evidence remains in `test-output/conditional-recovery/`.

Independent review instance 1 returned Ready with no actionable findings. It
regraded the final 120 executions, checked 2,184 delivered fact occurrences for
resolvable provenance, verified protected hashes and reviewed the three caller
answers. The verdict covers this bounded source/guidance change, not publication
or installed-runtime promotion.

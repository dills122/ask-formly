# Question planner A/B evaluation — design v1

Status: preimplementation review target, 21 October 2026. Contract:
[QUESTION-PLAN-CONTRACT.md](QUESTION-PLAN-CONTRACT.md). Steering:
[STEERING.md](STEERING.md). This document specifies tests; it reports no tests
executed and no measured planner quality.

## Scope and sequence

1. Independently review this contract and protocol before implementation.
2. Prepare and freeze 12 development cases and their meaning-based rubrics.
3. An independent case author prepares 30 held-out cases and rubrics without
   seeing candidate code/outputs. Keep them unavailable to the implementing
   agent until both candidates/configurations are frozen. Commitments are
   file SHA-256 hashes, not Git commits. No staging or committing is requested.
4. Implement contract tests first and record expected failures, then minimal
   contract code; build A and B against development cases with TDD. Stub tests
   prove failure handling only; real-library smoke tests establish integration.
5. Independently review implementations and isolation before held-out timing.
6. Freeze code, dependencies, models, prompts, hardware/configuration, grading
   rubric and cases. Run the held-out comparison once under this protocol.
7. Grade without arm labels; freeze grades before joining timings and method
   labels. Review results independently. Do not tune after opening held-out
   outputs. Any revision needs a new held-out set and separate evidence.

All new implementation/test code stays in the POC. No imports or copied code
from other project implementations. Do not run the compiler, full data tests,
or any command that rebuilds the locked seed. Future checks use a narrowly
selected new question-planning suite. Before and after checks, hash authored,
corpus, data/compiler modules and the existing DB; a mismatch invalidates the
run and is reported, never repaired automatically. New evidence belongs in a
fresh `test-output/` directory. Existing experiment artifacts stay unchanged.

## Case design and gold rubric

The 30 held-out cases comprise six cases in each primary group:

1. Multiple outcomes/actions with shared or differently scoped conditions.
2. Negation, exceptions, hypothetical premises, and comparisons.
3. Exact identifiers, dotted paths, generic syntax, literals, and code/prose mixtures.
4. Pronouns, paraphrases, elliptical wording, and genuinely ambiguous references.
5. Single asks, explicit version/adapter scope, and unfamiliar/out-of-domain requests.

Cross-label cases to cover overlapping risks. Include at least four genuinely
ambiguous cases and at least six unambiguous single-aspect cases across groups.
Balance normal questions and adversarial wording; do not merely paraphrase old
cases. Gold annotations contain atomic requested information, relevant condition
attachments, negation/polarity, exact strings and their roles, comparisons,
scope mentions, acceptable alternatives, and forbidden invented implications.
They also mark independently searchable outcomes and permissible combinations.
Whole-question echo fails cases requiring separate focused searches; single
asks and genuinely inseparable comparisons are not forced into arbitrary splits.
They contain no required fact IDs and require no Formly answer to grade.

For ambiguous cases, specify the ambiguity and what can still be requested.
An explicit interpretation ambiguity is a correct result when warranted;
unnecessary ambiguity on a clear question is a failure. Out-of-domain requests
must still be represented faithfully: the planner cannot infer DB coverage.

Old 13-case catalog and 11-case obligation sets remain exposed diagnostics,
reported separately and excluded from selection. Prior fact-ID scores are not
comparable to this plan rubric. No earlier question-layer arm is modified.

## Structural and failure tests (TDD)

Test observable contract behavior rather than library internals:

- Exact original text preserved, including Unicode and punctuation; correct
  codepoint offsets, bounds, and literal source-span correspondence.
- Empty/oversized input, unknown fields/status, duplicate IDs, dangling
  aspect references, uncovered aspects, empty queries, and capacity overflow
  rejected without silent coercion or truncation.
- Status invariants for successful, ambiguous, and failed plans.
- Arm B tagged SEARCH/AMBIGUITY decoding, mixed/ambiguity-only results, missing
  prefixes, empty payloads, and capacity checks. Real-library smoke tests must
  demonstrate this transport without a second semantic pass.
- Model malformed output, wrong tool names, parser/backend errors, and deadline
  expiration remain explicit failures. No cross-arm or old-planner fallback.
- Single-attempt configuration, no hidden retries, full failure retention.
- Question injection attempting to answer, select fact IDs, or invoke tools
  cannot cause tool execution or access to locked data. Treat text as input.
- No DB/corpus reads during planning, no writes to locked paths, no imports
  from outside project implementations. Package imports remain permitted.
- Real spaCy parser and real LlamaIndex standalone generator each exercised
  on development examples. No mocked result counts as semantic qualification.

Automatic validators establish structure and exact-string properties only.
They cannot prove complete aspect recognition or correct condition attachment.

## Semantic scoring

Two independent graders assess anonymized outputs against the frozen rubric,
record disagreements, and adjudicate with written reasons before labels/timing
are revealed. If two graders are unavailable, report that limitation and do
not describe the result as independently double-graded. Automated exact-match
checks supplement rather than replace this assessment.

Primary metric: complete-plan success count out of 30. A case passes only when
all required information is represented, no material extra ask is invented,
conditions/negation/relationships/scope are correct, necessary exact strings
are intact in the focused queries, and each request is usable independently.
Correctly represented genuine ambiguity can pass; a failed plan cannot.

Secondary metrics, separately reported:

- Atomic aspect recall and invented-aspect count.
- Required condition/relationship attachment accuracy (correct / annotated).
- Exact identifier/literal preservation (correct role and text / annotated).
- Usable search requests / all requests; duplicates and unnecessary requests.
- Ambiguity precision/recall; failures by code; full case failure ledger.

Use N/A for a case with no applicable annotations, not a fabricated 100%.
“Usable” means a bounded natural-language query fits the existing string-query
interface, identifies the requested target and relevant scope, preserves
necessary context, and contains no answer or invented API. It does not mean
that retrieval found a fact. Human usability grading is reported as such.

Critical semantic errors are polarity reversals, material condition inversions,
silent version/adapter substitution, and corruption/replacement of a necessary
identifier or literal. Missing information also fails completeness even if it
does not meet this critical-error definition. Duplicating original context
does not erase a focused-query error.

## Timing and repeatability

Record one cold startup per arm separately, distinguishing model loading from
question processing. After one development-question warmup, run five paired
passes of the 30 held-out questions. Alternate A/B ordering by case/pass, with
a frozen seeded question order. No concurrent tests or workloads. Both arms
run on the same host; B uses an explicit local model with frozen identity and
generation settings, not a cloud default. Record model serving configuration.

Pre-run hardware provenance records CPU/device model, memory and core counts,
with unavailable fields explicit. Its manifest is included in the reviewed
freeze. The runner verifies that hardware snapshot before opening held-out
cases and records Ollama version plus actual `/api/ps` model/device-memory state
before preparation, after preparation and after samples. Server settings not
exposed by the local API are marked unavailable, not inferred from the calling
shell's environment. These unknowns limit timing reproducibility.

Measure monotonic wall time from accepted input through final validation,
including serialization and failures. Record native call duration separately
where available. Report all 150 warm samples per arm, median, nearest-rank
p95, maximum, timeout rate, output size, and request counts. Cold startup is
not mixed into warm percentiles. Do not drop failed runs or rerun them until
they pass. A host failure invalidates the paired run with its evidence retained.

If the supervisor kills a worker for timeout or malformed output, retain that
failed sample unchanged. Before that arm's next scheduled sample, start a new
worker and run the same development-only warmup once. Never retry the failed
question/pass. Record recovery startup, warmup output and total recovery time
separately; mark the next sample as after recovery. Include its planning time
in the primary distribution and report recovery-affected counts and total
recovery overhead separately. Recovery can affect caches, so disclose this
timing limitation. If worker startup or the one recovery warmup fails, invalidate
the run as an execution-environment failure, retaining all partial evidence.

The first output per case is the primary semantic sample, selected in advance.
Compare normalized plans (excluding trace timings and incidental IDs) across
all five passes. Apply the full semantic rubric to every distinct normalized
output; reuse a grade only for an identical normalized plan. Normalization
preserves query text, conditions, status, ambiguity descriptions, request
grouping and relationships; it removes only timings and consistently remaps
incidental IDs. Report complete-plan stability as cases for which all five
outputs pass completeness, and separately report exact output agreement.
Repeated samples are not 150 independent questions.

## Decision gates

Proposed quality floor: at least 27/30 complete first-pass plans, no critical
semantic errors in any observed pass, and no isolation/contract failures.
This is an experiment gate, not a statistical guarantee. Report raw paired
case outcomes and uncertainty; do not claim population superiority from a
small sample. Within eligible arms, a gap of fewer than three complete cases
is inconclusive on quality. Then compare measured latency and maintenance
burden without declaring an accuracy winner.

The product planner latency budget remains unapproved. The contract's 10-second
deadline only bounds the experiment. Report the quality/latency tradeoff and
request that budget decision before any promotion. Neither arm is promoted
automatically. If both miss the quality floor, recommend neither; if only one
passes, identify it as the quality candidate pending latency approval.

Maintenance review records custom semantic-rule count and purpose, custom code
size, package/model footprint, configuration complexity, and failure behavior.
The reviewer verifies A actually uses dependency structure and B the library
generator, with no undisclosed semantic repair in the common adapter.

## Current stage completion

This stage ends with reviewed documents and an explicit finding disposition.
No dependencies, executable schema, tests, planner code, case fixtures, or
benchmarks are created before that review. Implementation and execution are
the next stage; no results are claimed by this plan.

# Linked examples v1 candidate

Examples are one of the [four planned knowledge slices](knowledge-direction.md).
Their compositions remain distinct from library guarantees and project standards.

**Status — deferred, 2026-10-28.** Preserve the working candidate and the storage
investigation below, but prioritize refining the current facts and retrieval
process before extending this feature. Linked examples remain important future
work. No further storage implementation, schema migration, promotion or release
is scheduled by this document. See the [current priorities](knowledge-completion-backlog.md#current-priority-fact-and-retrieval-refinement).

The candidate lives in `poc/contextual-kb/linked_examples_v1/`. It is an opt-in
development runtime, not part of the installed service or RC package. Its example
catalog is separate from the frozen 192-fact database. It reads facts without
compiling, seeding, migrating or replacing the installed database.

Examples have stable IDs and many-to-many fact links. Each link explains what
the fact supports. Conditions, limits, prerequisites and provenance travel with
the example. Application choices are illustrations, not additional library
guarantees. A linked fact does not certify every line of an example.

The initial set covers hide/show with model retention and control registration,
independent dynamic sections using keyed groups, and initialization using model
values, defaults and a lifecycle hook. A Material stepper is outside this batch.

## Retrieval contract

Ordinary fact retrieval supplies only small example references when space allows.
The separate `get_formly_examples` tool lists summaries by fact IDs or retrieves
selected examples by example IDs. Scope, pagination, response budgets and complete
file delivery are part of the contract. Code is never silently truncated to fit
the ordinary fact response. Refer to the candidate caller guide and tool schema
for exact arguments.

Example verification is separate from fact assessment. Source review, an executed
fixture and whole-application qualification are different claims. Execution
records identify tested code, dependencies, assertions and command; a passing
retrieval test cannot qualify Angular behavior.

## Regression evidence

Public development cases cover the issue's hide, stepper, initialization and
collision questions, the three example tasks, and an unsupported-version control.
Expected fact IDs belong to the grader, not the caller. Recovery selects IDs
actually exposed by lookup, help or discovery. Report first-response coverage,
coverage after recovery, recovery calls, example delivery and serialized MCP bytes
separately. An out-of-rubric fact is not automatically irrelevant.

Deterministic plan replays measure retrieval and transport regressions. Fresh
caller generations measure whether an agent can independently discover and use
the tools. Neither is a broad accuracy score. Keep unsuccessful cases in results;
adding examples does not itself repair the remaining first-pass ranking misses.
Raw transcripts and generated fixtures belong under ignored `test-output/`.

## Current candidate results

The source suite passed 296 tests, including 22 candidate/catalog/transport and
regression-harness tests. The exact example factories passed TypeScript checking
and 17 browser assertions after a clean pinned dependency install. The tested
environment was Formly core/Material 6.3.12, Angular/Material 18.2.14, Node 22.23.3
and Chrome 156 on macOS arm64. Assertion names, source hashes, fixture hashes and
the result digest are recorded in the example manifests. This does not extend
library, browser or platform coverage beyond those assertions.

The full-corpus development replay ran eight cases three times against both
baseline and candidate (48 case executions). All repeats were stable, there were
no tool errors, and the candidate preserved exactly the baseline's first-pass
and recovered fact IDs. Maximum serialized SDK results were 29,704 bytes for the
baseline and 29,804 for the candidate. All three example-focused cases fetched
their intended example. These are deterministic replays, not 48 independent
calling agents.

Remaining selected-evidence gaps are visible:

| Case | First response | After bounded scripted recovery |
| --- | ---: | ---: |
| Hide/value/registration | 5/5 | 5/5 |
| Stepper/model scope | 5/8 | 5/8 |
| Initialization | 5/12 | 6/12 |
| Dynamic key collisions | 3/9 | 4/9 |

The recovery policy used only returned candidate IDs, not the grader's expected
IDs. These results cannot be compared directly to earlier oracle-ID fetch counts.
Examples improve access to demonstrations; this batch does not resolve the
underlying ranking gaps. The required full local maintenance command still stops
on missing provisioned worktree environments; source and candidate checks do not
replace full model-backed qualification.

A fresh caller, given only user requests and live tool instructions, completed
the three example tasks in 4, 2 and 3 workflow calls. It discovered IDs through
the MCP, fetched all three complete examples, and recovered omitted hook facts
for initialization. Its answers distinguished retained model values from control
registration, nested model paths from DOM IDs, and supplied values/defaults from
hook lifetime. This was one fresh caller handling three requests, not three
independent generations or a broad answer-quality qualification.

The first fresh-caller startup exposed a mismatch between nested execution
metadata and the catalog schema. The schema was corrected and regression-tested;
the caller retried successfully. That failed initialization remains recorded in
the development history. Successful calls still emitted the previously observed
dependency lifespan forward-reference warning.

Independent review instance 1 found no actionable defects and marked the isolated
candidate Ready. It independently ran the 22 candidate tests, verified browser
artifact/code/fixture hashes, inspected replay parity, and checked all three
fresh-caller answers against their actual transcripts. The largest fresh-caller
result was 29,812 serialized SDK bytes. The reviewer verified recorded browser
evidence rather than rerunning the browser fixture. This verdict does not approve
promotion or publication.

## Promotion boundary

Source CI tests the isolated implementation without activating it. The active
launcher, runtime manifest, release allowlist, authored facts, corpus, compiler,
database and model assets remain unchanged. No sealed evaluation is opened.

Before promotion, review example support and execution evidence, response budgets,
fresh-caller answers, preserved baseline hashes and remaining failures. Decide
separately whether new factual claims need normal admission. Installing the
candidate or publishing a release requires a separate promotion decision.

## Storage investigation and proposed direction

This section records the 2026-10-28 investigation, not an approved implementation
plan. The current candidate loads manifests and code files into an in-memory
catalog at startup. It does not query a compiled example database.

The preferred long-term direction is **files for authoring, one compiled SQLite
snapshot for serving facts and examples**. Keep manifests and TypeScript/HTML
sources in Git for review and executable testing. A future compiler would validate
them and embed complete code, metadata, fact links and portable verification
records in a new candidate database. The MCP would read the promoted snapshot.

| Storage option | Strength | Cost or limitation |
| --- | --- | --- |
| Files loaded at startup (current candidate) | Simple editing, review and debugging; no fact DB change | Must distribute and validate all matching files; catalog currently loads code into memory |
| Separate examples database | Can package or update examples independently | Requires an explicit binding to the fact snapshot and compiler/startup checks for cross-database links |
| Combined knowledge database (preferred proposal) | Facts, links and code form one release snapshot; fact references can use foreign keys | Requires deliberate compiler/schema/runtime compatibility work; an example update produces a new knowledge artifact |

A separate database remains an option if independently distributed example packs
become a real requirement. Current measurements do not justify a separate service,
vector index, or external object store for these small code examples.

### Disposable feasibility experiment

The investigation read the existing baseline and wrote disposable prototypes under
ignored `test-output/example-storage-study/`. It did not modify the installed DB,
authored inputs, compiler or runtime. Results are summarized here so the decision
does not depend on retaining local scratch files.

| Measurement | Observed value |
| --- | ---: |
| Examples / fact links | 3 / 12 |
| Example code | 2,798 bytes |
| JSON manifests | 15,153 bytes |
| Existing database | 794,624 bytes |
| Combined prototype | 847,872 bytes (52 KiB increase) |
| Gzip size increase, combined versus baseline | 7,011 bytes |
| Separate examples prototype | 57,344 bytes; 6,604 bytes gzip, in addition to the baseline |
| Shared execution records after deduplication | 1 |

Both prototypes returned byte-identical code. The combined prototype rejected an
unknown fact link with a foreign-key constraint, passed integrity/reference checks,
and retained every original table's rows, including the fact-search tables. Query
plans used indexes for scoped fact-to-example lookup. The baseline file hash stayed
unchanged. The separate prototype pinned the baseline hash and checked fact IDs
during construction; it did not have a cross-database foreign-key constraint.

These are storage feasibility checks for three examples, not benchmarks or runtime
qualification. Gzip measurements concern these DB files, not a published release
archive. The prototype retained schema version 2 solely for the disposable study;
it is **not** a valid release candidate. It stores only one revision/scope per ID
and does not implement the proposed revision model below.

### Proposed data model

Separate stable identity, applicability and execution evidence instead of putting
everything into one JSON blob or attaching code directly to each fact.

| Entity | Responsibility |
| --- | --- |
| Example revisions | Stable example ID, immutable revision digest, title, summary, prerequisites, conditions and limits |
| Example files | Revision, safe relative path, language, complete UTF-8 content and content hash |
| Example–fact links | Revision, fact ID and an explanation of the exact behavior that fact supports |
| Example applicability | Explicit supported Formly version and adapter for the revision; do not infer compatibility from a fact's broader applicability |
| Verification runs | Exact dependency environment, fixture/input hashes, assertions, outcomes and result digest |
| Example–verification links | Which revision and specific assertions a run verified; one run can cover multiple examples |

Code and relevant authored semantics should identify the revision. Verification
runs should refer to that revision rather than changing its identity merely
because a test was rerun. Editing code or behavior-relevant metadata must invalidate
the old execution association until the new revision is verified. A shared run's
17 assertions must not imply that all 17 independently apply to every example.

Retain portable execution summaries and provenance in the compiled artifact.
Large logs, screenshots and traces can remain external development evidence with
recorded digests; machine-local result paths must not be required to serve examples.
Digests establish identity and consistency, not proof that an arbitrary claimed
execution occurred. Admission still requires reviewing the underlying evidence.

### Retrieval and release behavior to preserve

- Fact lookup returns small references; explicit example retrieval returns code.
  Storage choice does not remove response budgets or permit silent truncation.
- List metadata without loading all code; fetch selected complete files on demand.
  Index fact links and scope. Do not add code to the existing fact FTS index.
- Deduplicate an example linked to several retrieved facts. Keep deterministic
  ordering and scoped pagination; do not silently select a different version.
- Build a new immutable candidate snapshot, verify it, and promote only after a
  separate decision. Preserve the previous release for rollback rather than
  mutating an installed database in place.

The existing compiler already constructs a disposable SQLite DB, validates foreign
keys and integrity, and publishes a new output. The current model-free reader
explicitly requires schema version 2. A combined store therefore needs an explicit
schema transition, reader compatibility checks, and updated release integrity
pins. Do not treat adding tables to the current file as a safe deployment strategy.

### Questions to settle when this work resumes

1. Define revision identity and handling of several versions/adapters for one
   example ID, including deterministic selection and ambiguity errors.
2. Decide whether verification summaries belong in reviewed source manifests or
   separate portable evidence records, and how those records are admitted.
3. Specify a new storage schema and compatibility policy for both retained runtime
   modes without requiring a rewrite of unchanged authored fact sources.
4. Design compilation checks for links, scope, paths, hashes, execution bindings,
   licensing/provenance and complete-file response limits.
5. Compare database-backed and file-backed candidate outputs, preserve all fact
   rows and ranking results, and qualify packaging/rollback before promotion.

These questions are deferred. The next implementation focus is current fact
quality and retrieval; a future isolated compiler prototype requires an explicit
decision to resume this feature.

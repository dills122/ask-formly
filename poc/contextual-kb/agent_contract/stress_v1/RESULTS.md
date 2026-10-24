# Five-run Formly contract stress test

2026-10-22. The frozen v1 contract was behaviorally consistent on this panel,
but its exact outputs were **not deterministic**.

## Work completed

30 diagnostic requests, five groups of six, each repeated in five fresh-context
Codex agent runs: 150 responses. Same contract, same questions, same order in each
run. All responses saved before grading, with no correction or selected rerun.
No application investigation, Formly answers, training or retrieval executed.

| Group | Examples | Met rubric and structure |
| --- | --- | --- |
| Custom-field workflows | New vs already registered types, wrappers, repeat rows, validators |30/30|
| API and condition preservation | resetOnHide, null/undefined/0, key representations, Unicode literals |30/30|
| Version and adapter scope | Mixed versions, historical version vs current, Angular vs Formly, core only |30/30|
| Library/application boundaries | Opaque widget failures, grounded dropdown goals, mixed requests |30/30|
| Messy/adversarial wording | Corrections, repeated requests, override attempts, malicious-looking label data |30/30|

Each repeat independently scored 30/30. There were150/150 structurally valid
outputs, no missing cases, no observed prohibited application investigation, and
no observed rubric violations. All30 cases retained the same rubric-grade
signature across repeats. That measures stability against the specified criteria,
not a mathematical proof that all outputs are semantically identical.

## Repeatability measurements

| Measure across all five repeats | Cases |
| --- | --- |
| Identical full JSON (canonical object-key order) |4/30|
| Identical question text and list order, ignoring reasons |11/30|
| Same number of questions |26/30|
| Identical global constraint fields |29/30|
| Same scored behavior on every required/forbidden criterion |30/30|

All four fully identical cases were appropriate empty outputs: B01, B03, B05,
M06. Thus none of the26 nonempty cases had identical entire objects across every
run. Full-JSON equality occurred in43 of300 within-case run pairs, including40
pairs from those empty cases. This is descriptive repeat agreement, not150
independent trials or a population reliability estimate.

Reasons frequently changed wording without changing justification. Four cases
changed question grouping (counts listed in run order1–5):

- W01 custom type implementation/registration/use:2,1,1,1,1.
- W03 wrapper definition/registration/application:2,1,1,1,1.
- E01 model value and FormControl under resetOnHide: false:2,2,1,2,2.
- E04 set and observe expressions['props.required']:2,1,1,1,1.

The frozen contract allowed focused combined questions; graders found the required
aspects and relevant conditions retained in both combined and split variants.

S05, explicit core-only registration, produced ui_adapter "none (Formly core)"
in four runs and "none (core only)" in one. All questions preserved the exclusion
of UI adapters; none incorrectly selected Material. This is a real normalization
gap in v1, though it did not violate the frozen semantic rubric.

## Provenance and verification

- CONTRACT.frozen.md, cases.json and rubric.json were hash-frozen before generation
  in freeze.json. Generation agents read only contract and cases. All five use the
  inherited Codex model configuration; no API model revision, temperature, sampling
  seed or per-request generation latency was pinned/measured.
- Each run processed all30 cases in one fresh context. Cases were grouped, but
  each group was NOT given an isolated context within that run. Fixed order means
  this does not test order sensitivity or single-request performance.
- test-output/repeat-1.json through repeat-5.json are actual saved generated
  outputs. raw-freeze.json binds their hashes before grading. No outputs changed.
- Two fresh grader agents, neither of which generated the runs, reviewed disjoint
  panels of90 and60 responses. Within each case, candidates were shuffled with
  fixed seed4917 and anonymous labels; graders did not see the repeat mapping or
  the other grader's scores. Each response received one rubric assessment, not
  two independent grades. Per-criterion booleans and case-specific evidence remain
  in grades-a.json and grades-b.json; grading-map.json and joined-grades.json make
  the join auditable. The parent also inspected all question outputs and agreed
  with the stated semantic conclusions.
- Structural validation and semantic grading remain separate. finalize.py requires
  both for an overall pass and rejects incomplete grades or changed frozen files.
  final-summary.json holds per-run/group scores and all repeatability measurements.
- 9 analyzer unit tests and 17 existing contract tests passed. Red/green logs are
  retained. Metrics review found two defects in the initial quality summarizer:
  duplicate case/rubric IDs could corrupt counting; structural validity was not
  required for overall pass. Both were fixed and regression-tested. A follow-up
  made the duplicate-case regression target its intended guard. The reviewer
  verified closure. These defects did not alter this panel's valid, unique inputs.
- A question-text-only descriptive metric was added after observing variation in
  the first three runs, to distinguish reason phrasing from query wording. The
  frozen contract, cases, rubric and all generated responses remained unchanged.

Commands, from the repository root:

    python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/stress_v1 -p 'test_*.py' -v
    python3 -B -m unittest discover -s poc/contextual-kb/agent_contract -p 'test_*.py' -v
    python3 -B poc/contextual-kb/agent_contract/stress_v1/analyze.py

analyze.py recomputes descriptive structure/repeatability to stdout. finalize.py
joins grades and writes evidence exclusively; it refuses to overwrite the completed
report. The generators were real fresh-context agents, not a deterministic mock.
This folder does not expose a standalone provider client to rerun those agents.

## Interpretation and next improvement

This is stronger evidence than the original one-batch trial for the library-only
boundary and retention of supplied conditions. It remains a curated, agent-authored
panel with related scenarios and agent judgments. Several cases extend earlier
patterns; these are exposed diagnostics, not held-out production traffic. Five
runs cannot establish deterministic behavior or a reliable general error rate.
No claim is made about answer correctness, retrieval coverage, production latency,
other model versions, or long-context/conversation behavior.

Before relying on output shape downstream, specify whether to split related
lookups and choose one representation for explicit no-adapter scope. Natural
wording can remain flexible if the consumer does not require byte equality. Those
would be a versioned contract change followed by a new comparison, not retroactive
normalization of this run. V1 is unchanged in this task.

All writes stayed in agent_contract/stress_v1. Existing A, pilot, original
contract/evidence and data/DB were left unchanged. Prior sealed evaluation was not
used; integrity.json records byte-hash checks without loading its content into
agent context. No dependency, MCP, retrieval, or knowledge-data code was changed.

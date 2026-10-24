# V1 versus refined V2: hard-case comparison

2026-10-22. Recommend V2 for the next agent-layer experiments: it met the same
semantic criteria as V1 and consistently produced the intended grouping on the
six targeted regression cases. This does not establish deterministic generation.

## Scope and actual execution

24 independently authored hard requests plus6 previously exposed regression
cases. Both contracts ran in3fresh contexts with identical forward ordering, then
one additional fresh context with reversed ordering. Eight runs,240responses,
30distinct requests. The candidate was frozen before the hard cases were available.
No post-result prompt tuning or response repair occurred.

New cases cover corrections/conflicting notes, asymmetric version/adapter scopes,
partially ambiguous application descriptions, exact literal pairings and quoted
instructions, unsupported premises and hypothetical APIs, and dense multi-part
requests. Hard-case author read only V1 and did not see V2 or any outputs.

| Metric | V1 baseline | V2 refinement |
| --- | --- | --- |
| Common rubric + structure, three forward repeats |90/90|90/90|
| Common rubric + structure, reversed-order probe |30/30|30/30|
| Valid output structure, all runs |120/120|120/120|
| Identical full JSON across three forward runs |1/30 cases|1/30 cases|
| Identical question text/order across three forward runs |6/30|8/30|
| Same question count across three forward runs |28/30|29/30|
| Same global constraint fields across three forward runs |29/30|30/30|
| V2-specific count/adapter checks, six regressions × four runs |7/24|24/24|

The common rubric passes were agent judgments, not automatic conclusions from
valid JSON. All six new hard-case groups passed16/16per version across four runs;
the regression group passed24/24per version. No required semantic aspect was judged
missing and no prohibited application work, invented requirement, or unsupported
factual answer was observed by the graders in this panel. The single exactly
stable full output in each arm was the appropriate empty response for H11.

The7/24 V1 score against V2 representation checks is **not** a V1 correctness
failure: V1 permitted combined questions and free-form core-only scope strings.
It quantifies the new representation preference, separate from common correctness.

## What improved

On the targeted examples V2 consistently separated:

- Custom type implementation, registration, and usage into3questions.
- Wrapper definition, registration, and application into3questions.
- Model-value retention and FormControl behavior into2questions.
- Expression configuration and observation into2questions.

Explicit no-adapter requests consistently used ui_adapter: "none". Unknown values
remained null. V2 also normalized plain version prefixes in global constraints
while preserving scope in questions. The JSON schema did not change.

The parent inspected all24 V2 regression outputs, confirming their question
identities and carried conditions, not merely their counts. The count/adapter
checker alone would not establish correct grouping. This inspection is recorded
separately in test-output/representation-review.json.

## Tradeoffs and remaining variability

V1 produced37,37,37questions in the forward runs. V2 produced60,60,61: about63%more
lookups, since it separates operations and repeats necessary context. This may
help downstream interpretation, but may cost more retrieval work. No downstream
benefit or latency improvement was measured.

V2's remaining forward count variation was H13: two field configurations with
exact string keys '0'/'false' and numeric/boolean defaults sometimes shared one
question and sometimes became two. Both pairings and types survived in all runs.

The reversed V2 run produced58questions and changed grouping relative to forward
run1 in H13,H18,H19,H20. Conditional API existence/scope questions and wrapper or
validation comparisons sometimes combined. All required conditions/alternatives
were graded as retained. V1's reversed run produced40questions and changed counts
in H02,H07,H21. One reversal probe cannot separate sampling variation from order
effects or establish order independence. V2 is more prescriptive, not a guarantee
of atomic or identical grouping everywhere.

No new machine-generated topic IDs or fuzzy matching were introduced. Correctness
here concerns preservation of the library information needs; a future extractor
still needs its own tests for that mapping. GLiNER2 was not run or changed.

## Evidence and review

- candidate-freeze.json freezes V1,V2 and protocol before hard-case exposure.
  panel-freeze.json freezes the complete inputs/rubric and regression expectations
  before execution. No candidate content changed after freezing.
- inputs/alpha is V1, inputs/beta is V2. Generation agents received only their
  assigned instruction and ordered request file, not rubrics, arm comparison,
  other responses or conversation history. Each run shares context across30cases;
  individual requests were not isolated in separate provider calls.
- All eight raw files in test-output are exclusive-write artifacts. raw-freeze.json
  binds them before grading. No generation retry or output repair was used.
- Three fresh grader agents each reviewed80anonymized candidates. Candidates were
  shuffled within each case using seed1207; graders saw the request and common
  rubric, but not arm labels/contracts, run identities, or each other's grades.
  Each response received one grade, not three independent grades. Exact API/literal
  spelling mattered; semantically equivalent natural wording was allowed.
- grades-1/2/3.json preserve per-criterion judgments and case-specific evidence.
  grading-map.json provides the auditable join after grading. final-summary.json
  retains every result, per-group scores, repeatability and representation checks.
- Parent inspected representative hard cases, all V2 regression groupings, and
  remaining grouping differences. No grade overrides were needed.
-10 refinement tests and17 baseline contract tests pass. Red/green logs retained.
  A focused reviewer inspected metrics, tests, panel preparation, and finalizer;
  no actionable defects were found. Review explicitly limits representation checks
  to count/adapter conformance and requires reverse results to remain separate.
- The inherited Codex model configuration was used throughout; exact provider
  model revision, sampling temperature and seed were not controlled. No inference
  latency or production load measurement was attempted.

This is a diagnostic comparison with agent-authored cases and agent judgments,
not an expert-human or held-out production evaluation. Repeats are correlated;
240responses are not240independent user requests. High scores do not establish
universal reliability, library answerability, retrieval quality, or answer accuracy.

## Decision and boundaries

V2 meets the predeclared next-experiment preference: no common-score regression
in any group, no observed forbidden semantic errors, and all targeted representation
checks pass. Use this folder's CONTRACT.md or prompt.py to try the refined version.
The parent contract/CLI remains V1 so the baseline and earlier evidence stay intact.

All new files are confined to agent_contract/refinement_v2. No locked knowledge,
data/DB, retrieval, baseline A, pilot, old training artifacts, or old sealed cases
were changed or used for scoring. integrity.json records byte-hash verification;
old evaluation contents were not supplied to author, generators or graders.

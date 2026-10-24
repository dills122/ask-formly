# Agent contract refinement comparison

Keep v1 and all earlier evidence unchanged. Compare BASELINE.md (exact v1) with
CONTRACT.md (v2 candidate). Candidate drafted/frozen before seeing independently
authored hard cases. No GLiNER, retrieval, application inspection or DB work.

Panel:24 independently authored hard requests plus6 exposed regression cases.
Both arms get identical requests, same order for3fresh-context repetitions; a
fourth fresh run reverses that order. Thus240 responses,30 distinct scenarios.
Three same-order repeats measure repeatability. Reversal is an additional order
probe, not proof of order independence. No output repair or selected reruns.

Freeze inputs and rubric before generation. Generation agents see only one
contract and the request array for their assigned run. No arm names, rubric, other
runs or conversation history. Same inherited Codex configuration; exact provider
model revision, temperature and seed not controlled. Each batch shares context;
this is not isolated production per-request execution or a serving latency test.

Common semantic criteria compare both versions: coverage, correct scope/condition
attachments, no invented app work or requirements. Combined focused questions are
allowed for v1 and not automatically semantic failures for v2; measure v2 grouping
as a separate candidate-specific conformance property on6regression cases. Canonical
"none" and splitting are new requirements, not retroactive v1 errors.

Grade saved candidates anonymously, shuffled per case, with frozen per-criterion
rubrics. One fresh grader per candidate, none of them generation agents. Parent
reviews failures/disagreements against input/output before any conclusion. Preserve
raw grades and any adjudication separately. Overall success requires structure AND
rubric success; never drop failures from denominators. Exact equality and graded
meaning are separate metrics. Five identical failures would still be failures.

Prefer candidate only if common semantic pass rate does not regress overall or
within a group, all serious scope/invention errors are resolved, and candidate
representation rules pass the regression cases. If not, retain v1 and report what
failed. Do not tune candidate on this scored panel then call its rerun held-out.
This is a diagnostic comparison, not a deployment guarantee or a final-answer test.

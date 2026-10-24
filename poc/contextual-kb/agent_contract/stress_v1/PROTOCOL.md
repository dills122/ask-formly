# Frozen repeatability stress test

30 new exposed diagnostics in five groups of six. Execute all groups in the same
fixed order in five fresh-context runs (150 responses). Each run receives exactly
the frozen contract and cases, never the rubric or other runs. Cases share context
within a run. This tests repeated grouped batches, not isolated per-request calls
or permutation/order sensitivity. No prompt tuning or selected reruns.

Every raw response is saved once before grading. Preserve errors. Complete-case
accounting includes missing/invalid results as failures. Do not repair outputs.
Model is the inherited Codex agent model; no explicit temperature, seed or model
version pinning is available here. Five runs cannot establish determinism.

Report separately:
- Structural validity and full case accounting.
- Exact JSON agreement (object keys canonicalized; array order and all strings kept).
- Question-count and constraint agreement.
- Rubric correctness: each required obligation and forbidden assumption, graded
  semantically from saved output; compatible combined questions are allowed.
- Stability of graded behavior: identical obligation/error signatures is not proof
  of complete semantic equivalence. Consistently wrong answers remain failures.
- Per-group/per-repeat scores and cases with any failure; no best-run selection.

Grade against frozen rubric, hidden during generation. Grading is by agents with
case-specific evidence, not expert-human ground truth. Review disagreements and
failures; retain original grades. No external facts, app investigation, retrieval,
training, old sealed cases, or DB writes. All work in this subdirectory.

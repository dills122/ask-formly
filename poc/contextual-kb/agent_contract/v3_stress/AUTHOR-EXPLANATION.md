# Author explanation

## Intent and plan
Test frozen v3 on24 fresh realistic development requests, three batches of8, three fresh-context repeats each. User authorized independent testing and review, not modifying candidate or sealed evaluation. No new v2 arm; no comparative improvement claim. See protocol frozen before generation.

## Flow and files
Independent case author read only POC steering and v2 contract; authored24 cases and rubric. Parent reviewed all cases before freeze. Each generation agent received only one full-contract packet in a fresh context, wrote first output to its own file, and received no validation feedback or retry. Nine separate generation agents total. File I/O was transport only. Exact provider revision/random seed/temperature not controlled; this is a native agent instruction-packet test, not a deployed API benchmark.

assess.py validates every scheduled slot via unchanged v3 candidate and tests malformed optional hints cannot change plan/query projection. Missing and invalid outputs count as failures. Grades supplied independently; core semantic and binding validity remain separate. Its 'usable' aggregate is the STRICT combined candidate gate (structural AND semantic AND binding); a binding-only error may leave text practically useful, which must be distinguished in reporting. Exact equality canonicalizes object keys only.

audit.py performs byte-hash checks across30 existing manifests,38,202 entries (may overlap). It reads no sealed case contents semantically. protected-before.json records successful preflight. input-freeze covers13 files. round freezes and raw-freeze protect generator outputs. No candidate/source/DB edits. Existing unrelated dirty main worktree untouched.

## Verification
TDD:8 harness tests initially failed due absent module; implementation then passed all8. Tests cover missing and invalid outputs, duplicate/unknown slots, incomplete grades, wording variation, independent semantic and binding failures, and no semantic claim before review. Original candidate tests remain frozen. Actual generation results in raw files; structure.json mechanically checks all72. All72 responses passed structural validation;2/24 cases have identical canonical JSON across all3 runs. Semantic findings deliberately left to independent reviewer; do not infer them from validator success.

## Risks and tradeoffs
Small, synthetic development panel exercises known failure categories; not representative user traffic or sealed qualification. Three repeats of24 requests are correlated. One shared context within each8-request batch. Case author and reviewer use agents from the same system family; independence means fresh context and distinct role, not different model vendor. Model may produce stable omissions, awkward literal copying, or plausible-but-wrong condition attachment. No answer accuracy, retrieval usefulness measurement, performance SLA or model stochasticity guarantee. No tuning/resampling after results. New evidence isolated for audit rather than wired into runtime.

## Challenge points
Audit every question and binding, including conditions omitted from the ledger (validator cannot detect those). Check that rubric ambiguities do not manufacture failures or excuse clear ones. Distinguish exact output equality, semantic equivalence, valid structure, usable text, and complete bindings. Preserve all failures and assess readiness of evidence separately from readiness of candidate.

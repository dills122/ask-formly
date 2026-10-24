# Preliminary independent review

Review instance: 1 of 3. Recorded before reading AUTHOR-EXPLANATION.md.

Boundary: dirty main, refinement_v5 only; older imports inspected read-only. Direct source verification used because graph coverage reports the three v5 Python files not tracked. No sealed contents inspected.

Initial inspection: all 48 question texts retain requested outcomes, scope, and source eligibility excerpts. G01 uses meaningful source ellipsis `if it does` resolved in its question. G03 and N06 return transitions suffice without duplicated earlier hide history under v5. N05 preserves its explicit mandatory after prerequisite. N07 generalizes names in run 1 but keeps independent scenarios; no unrelated field leakage observed.

Concern to resolve against frozen policy: N02 runs 1 and 2 bind `Please keep the support check independent of the usage question.` The rubric calls this an attachment clarification rather than an additional Formly scenario. Determine whether this harmless restatement is a permitted interpretation restriction or an excluded response-format instruction; do not add a new forbidden rule after generation. N07 run 3 and N08 run 1 similarly restate existing attachment distinctions, without altering outcomes.

Engineering: thin prompt selector reuses frozen v3 transport. Seven candidate tests pass; preserve.py passes 32 prior manifests. Structural omission acceptance is explicitly tested and does not prove semantic coverage. Remaining verification: reconstruct all raw records, input/raw manifests, all v5 plans/hints and final source-by-source grading. No new semantic detector or retry mechanism found.

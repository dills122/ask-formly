# Independent review instance1 of3

Verdict: Not ready for full training. Three bounded P2 findings:
1. Preparation accepted hashed bytes without independent review/structural qualification
   before optimization. Require a review receipt bound to fresh hash.
2. Accepted-envelope metrics discarded correct raw occurrences in overlapping outputs;
   add separate raw per-role metrics and gates.
3. Unresolved reasons collapsed boundary/multi-role/no-role/unsupported causes; separate
   diagnostics and retain nonfinite-vs-alignment failure distinction.

Reviewer independently ran19tests, reproduced raw-metric discrepancy, observed completed
smoke log selected=null/diagnostic_only=true, verified repository scope. No model updates,
real fresh/historical contents or sealed data read. Graph untracked/direct sources used.

Author: Accept all3. Added bound independent receipt + pretraining structural/native
qualification; raw metrics/gates; explicit reasons/counts and runtime nonfinite failure.
Additional invalid-to-valid-butwrong regression guard and synthetic/CLI flow tests added.
Material fixes require fresh review2. No architecture pivot or protected-file changes.

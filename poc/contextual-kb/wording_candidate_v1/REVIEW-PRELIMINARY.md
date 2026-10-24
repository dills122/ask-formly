# Preliminary independent review
Review instance: 1 of 3

Recorded before reading AUTHOR-EXPLANATION.md. Scope is the new wording_candidate_v1 directory on dirty main at c3091328f49d53de6b41a49c4fe5aa8f1c45e516; unrelated working-tree changes excluded. Read PLAN.md, tests, candidate.py, serve.py, replay.py, original validator, service and planner. Coverage reports all inspected POC source paths not_tracked; conclusions use direct source fallback.

No correctness defect found in the bounded rewrite. Fullmatch preserves both ordered, case-sensitive paths and the track relation; existing ledger, source grounding and final original validation are required. Other conditions remain untouched. Strict-valid inputs pass unchanged as specified. CodexPlanner returns decoded raw plans, so it does not reject the target case before the adapter can run. Service validates before backend initialization.

Nine tests passed with python -B unittest discovery. Pending: independently repeat all 84 exposed packets, adversarial checks, hash-only preservation verification, and author-claim reconciliation. The strict validator remains unable to find undeclared lost conditions; no broader semantic or answer-accuracy conclusion is supported. Replay summary hardcodes distinct_repaired_outputs=1; verify against actual repeated payloads before relying on that count. Native evidence is optional for the bounded syntax verdict but must not be inferred from mock service tests.

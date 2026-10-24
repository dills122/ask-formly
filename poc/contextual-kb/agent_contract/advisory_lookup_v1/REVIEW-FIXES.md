# Accepted independent-review fixes

Review1 was Not ready with two findings. Both are accepted; original reviewed cli.py/verify_live.py are preserved in test-output/pre-review-fix-source.

P1: CLI's final model verification could throw after an extraction worker failure, hiding the successful full-question retrieval packet. Three new RED regressions reproduce this composition failure and missing cleanup helper. CLI now retains successful retrieval, marks advisory status degraded and reports parameters_unchanged:null with an explicit extractor_verification diagnostic when verification cannot complete. It does not falsely assert unchanged parameters. Actual DB search errors still propagate, and DB hash checks remain mandatory. This behavior also applies when final verification itself fails after otherwise successful extraction; the failure remains visible.

P2: verification harness worker cleanup was not guaranteed after output or verification exceptions. model_session now owns the worker lifecycle in a finally block. Body-failure regression confirms closure. This does not alter successful extraction/query behavior.

23tests pass. The real DB/CLI path was additionally exercised with an intentionally failing local subprocess: search IDs match the prior actual native CLI output and verification is explicitly unknown. This is fault injection, not a GLiNER quality result. A separate new actual default CLI run verifies the successful path after the fix; no model/threshold changes or old-output rewrites occur.

Original failed-environment run and successful native full-panel run remain intact. Audit original run-freeze against failed-environment-source for cli/verify_live/README; audit run-ready-freeze against pre-review-fix-source for cli/verify_live. Other bound inputs are unchanged. The final implementation has its own final-code freeze. No full-panel resampling is used to hide either failure.

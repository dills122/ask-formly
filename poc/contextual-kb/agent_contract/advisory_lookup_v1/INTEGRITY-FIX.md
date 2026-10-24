# Review2 integrity correction

Accept review2's remaining finding. Ordinary verification unavailability and observed frozen-parameter mismatch are distinct outcomes.

runtime.IntegrityError now represents positively observed checkpoint or parameter drift. Native worker startup and command errors carry an explicit error_type; ProcessExtractor reconstructs IntegrityError and closes failed workers. Local before/after mismatch raises the same type. AdvisoryLookup propagates integrity failures from loading or extraction (guarding the older integration's broad exception capture), and CLI propagates them from final verification. Other advisory availability failures continue to return the full retrieved packet with degraded status and explicit unknown verification. Real retrieval/DB failures remain hard errors.

Seven targeted RED regressions preceded the correction, with another real-pipe CLI integrity composition check added afterwards. All31tests pass. Tests distinguish worker unavailable from changed weights and verify cleanup. Existing models, thresholds, native schema, questions and retrieval algorithm are unchanged.

Pre-correction cli/lookup/runtime/transport/worker sources are archived in test-output/pre-integrity-fix-source. final-code-freeze.json binds the previous review2 target; ready-code-freeze.json binds the corrected review3 target. Prior run-ready/native results remain successful historical evidence and are not overwritten or resampled. A fresh actual CLI smoke after this correction checks final package/transport imports and successful native model execution; it is not an accuracy sample selection.

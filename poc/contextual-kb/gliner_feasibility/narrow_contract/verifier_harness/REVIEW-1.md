# Review instance 1 of 3

P2: Original run.py published completion before final integrity checks. An isolated
reviewer reproduction showed a failed final audit left completion.json and no failure
receipt or after-check evidence. Accepted and addressed by guarded_run: all checks
attempted, phase-specific failures retained, completion only after success. New tests
cover failed setup and final audit. Reviewer independently ran11then13 passing tests.

Training recipe, LoRA-only optimization, question averaging, schedules, full-state
checkpoint comparison and RNG restoration were consistent. Calibration never enters
gradients/checkpoints. Tiny model exercised124updates; GLiNER smoke onlyone per seed.
Both smoke checkpoints had exact564state entries/logits,37,873protected checks unchanged.
No other actionable findings. Reviewer used direct sources because graph untracked.

Verdict: Not ready for final acceptance in instance1 pending prescribed fresh review
of material orchestration fix. Full experiment remains not ready: evaluation/calibration/
resolution/timing orchestration is deferred. No reviewer edits, training or sealed reads.

Author response: Accept. Correction and13tests complete; corrected CLI preflight-002
then completed with0updates and37,873unchanged protected checks. Fresh review2 requested.

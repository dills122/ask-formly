# Verifier training harness implementation

Training harness implemented inside this POC. No full GLiNER training, calibration
selection, fresh evaluation or operational adoption was performed.

## Evidence

- TDD retained three red/green stages: missing module→9pass; missing training loop→11pass;
  missing failure-guard function→13pass. Initial red runs fail at import; do not claim
  the individual assertions executed in those red runs.
- Tests use actual Torch computation for question-vs-occurrence weighting, fixed124-step
  loop/992exposures, seeded complete-cycle schedules, invalid labels, nonfinite loss,
  LoRA-only optimizer membership, buffer mismatch and RNG/mode restoration.
- Actual GLiNER smoke: one8-question AdamW update per seed1701/1702. Each changed198
  trainable state entries;zero frozen parameters/buffers changed. First-save reload
  matched all564state entries and exact logits on eight fixed training-only questions.
- Native preflight checks all1,215training/calibration supplied spans, keeps26empty
  coverage-only questions out of optimization and records216eligible schedules.
- Corrected CLI preflight-002 completed withzeroencoderforwards/optimizersteps.
  Its frozen inputs passed verification and37,873protected checks passed unchanged.
  Both baselines,A,v2,previous experiments and data/DB remain unchanged.

## Independent review and correction

First review confirmed a finalization reporting defect: completion could precede a
failing preservation audit. Accepted. guarded_run now attempts all final checks, records
setup/work/audit failures, and only writes completion after success. Two new regression
tests and corrected CLI preflight pass. Original smoke logs/receipts remain intact;
its input freeze hashes refer to the earlier source before this orchestration correction.
Current source is separately frozen for review. REVIEW-1.md records the original finding.

## Scope and next prerequisite

Default mode only performs preflight. Explicit smoke mode is capped atoneupdateperseed.
The later full mode fixes124updates×8exposures,AdamW1e-4/wd.01,clip1 and first/final
save verification. Full-length GLiNER run and update124checkpoint are unexecuted;
tiny-model scheduling tests and shared checkpoint helper do not replace that evidence.

This delivery implements the TRAINING component requested this turn. The reviewed
protocol also requires executable development threshold selection, conflict-only
resolution, historical/fresh regression accounting and timing before the complete
experiment starts. Those remain unimplemented here; the current harness must not be
presented as full-experiment readiness. No accuracy/improvement claim from smoke losses.

Fresh review2 verdict: Ready for scoped training harness only; no actionable findings.
Reviewer independently ran13passing tests and verified source freeze. Full trial remains
not ready until the deferred protocol orchestration is implemented/reviewed.

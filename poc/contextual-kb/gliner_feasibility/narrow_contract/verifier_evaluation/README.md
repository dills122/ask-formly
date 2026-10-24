# Verifier decision and evaluation wiring

Implements the remaining frozen verifier_training_plan protocol inside this POC.
No full training, fresh evaluation, promotion, or production serving is performed by
unit tests or the smoke stage. All writes are new files under test-output; sealed
fresh inputs are independently authored under sealed/ in this same directory.

Modules: decisions.py resolves only same-offset conflicts and accounts per-occurrence
losses, probe rejection, prior repairs and paired thresholds; pipeline.py separates
operational from oracle-span passes, validates fresh coverage and runs repeated timings;
runtime.py loads frozen models, calibration and (only when requested) historical
records; stages.py guards evaluation access; cli.py binds execution stages with hashes.

Run with gliner_feasibility/env/.venv/bin/python -B cli.py STAGE --name NEWNAME.
Stages:
- smoke: existing one-update disposable adapters,30development questions only. No
  optimizer or historical/fresh loader. Decision artifacts are marked smoke and cannot
  authorize evaluation. This proves wiring, never efficacy or calibrated readiness.
- prepare --fresh PATH: requires PATH with suffix .review.json containing verdict=ready,
  independent=true, reviewer identity and fresh_sha256. Validates coverage/duplicates,
  split leakage and native token transport (no encoder forward) in an isolated process;
  binds review/fresh hashes and current source/data before optimization. Training and
  calibration processes do not receive fresh rows.
- train --from-run PREPARATION: explicit later full-training launcher; records the
  preparation binding before invoking the frozen training harness. Not run this turn.
- calibrate --from-run TRAIN_LAUNCH: requires completed124-step/992-exposure full runs,
  verifies full checkpoint states and chooses one shared pair from nine fixed pairs.
- evaluate --from-run CALIBRATION: requires a frozen selected pair and bound models/code,
  then opens416historical cases/622probes and40sealed fresh cases, checks frozen baseline
  replay, preserves prior correct repairs, scores all gates and runs five timing passes.
  No selected pair stops before reading evaluation. Diagnostic-only pair cannot qualify.

Dataset envelope for independent fresh author: list of40rows, each with id,text,group,
gold [[start,end,role]], probes [{start,end,expected_role (null for negative),family}].
Groups cross_role/boundary/unfamiliar/ordinary each10; >=8gold occurrences perrole;
>=4empty-gold questions; allgold probes; negative families clipped_path/broken_quote/
merged_mentions/nested_fragment each12 plus4unsupported. Exact offsets are Unicode
half-open. Author/reviewer must certify semantic labels before sealing; automated
coverage validation is not semantic review. No real fresh content is created/read by
this implementation turn. The real trial still needs that independently reviewed seal.

No-conflict/overflow/partial-overlap inputs skip inappropriate verifier calls. Safe
abstention retains raw output and does not count as repair. Accepted-output metrics
exclude invalid overlapping envelopes; raw per-role metrics are separately reported
and gated, alongside exact-mention loss checks. Unsupported negative spans stay in rejection denominator.
No knowledge lookup or application investigation occurs. Private pinned native schema
transport remains a dependency. Timing includes routing overhead, reports eligible-only
p95 as well as all-question p95, and uses the stricter for the1second experimental gate.

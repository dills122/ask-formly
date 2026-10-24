# Full training and development calibration results review

Review instance: 1 of 3. Independent-review reviewer mode; new results review, not an additional implementation review. Scope is the 50-artifact `test-output/full-run-review-freeze.json` and its referenced training/calibration evidence. Repository HEAD is `c3091328f49d53de6b41a49c4fe5aa8f1c45e516`, branch main; the working tree contains extensive unrelated modifications/untracked files, including this POC. The explicit hash manifest, rather than HEAD, identifies the reviewed experiment.

## Findings

No actionable artifact-integrity or results-interpretation defects found. The experiment fails its predeclared calibration acceptance criterion: every shared threshold pair has supported-gold failures. The sealed-evaluation gate must remain closed.

## Preliminary independent conclusions

Recorded to the initiating agent before reading FULL-TRAINING-AUTHOR-EXPLANATION.md or the summary analyses: both seeds completed 124 steps and 992 exposures across 216 eligible questions; the 50 artifact hashes matched; all nine pairs were ineligible and selected was null. The frozen protocol explicitly requires STOP in that situation. First/final receipts reported identical restored state/predictions. The initial conclusion was a valid negative calibration result, not readiness for sealed evaluation.

## Plan Review

The run config matches the fixed two seeds, CPU float32, four threads, 124 updates, batch eight, lr 1e-4, weight decay .01, clip 1, LoRA r8/alpha16/dropout0 on encoder/extractive_head, and final scheduled checkpoint policy. Actual steps exactly match both stored schedules. Each complete 216-row cycle contains every eligible row; each seed exposes 128 rows five times and 88 rows four times. All 26 explicit coverage-only rows are excluded and retained with their no-BCE reason in training-row-policy.json.

Both seeds' update-1 and update-124 receipts contain 564 state hashes and successful state/logit equality flags. Between these checkpoints, exactly 198 entries change and every changed entry is LoRA; result.json reports zero changed frozen state. All four adapter weights files match frozen hashes. This verifies retained receipts and weights integrity, not a fresh model reload.

The calibration cache exactly matches all 30 frozen development texts, gold offsets/roles and probe membership: 71 gold and 30 negatives per seed. An independent standard-library calculation of all nine fixed pairs reproduces every gold-failure and malformed-rejection count. Gold failures range 12–26 for 1701 and 9–19 for 1702. Therefore no ranking/tie-break can produce an eligible choice. selected=null and diagnostic_only=true correctly implement the protocol's stop condition.

Independently counting raw exact-offset groups with different roles confirms zero for both seeds. Thus zero repairs/losses is passthrough evidence only. Supplied-span success is not operational extraction success, and absence of an eligible threshold is not zero correct extraction.

## Author-Claim Reconciliation

| Claim | Independent evidence | Status |
| --- | --- | --- |
| Fixed budget and exact schedules | config.json, steps.jsonl, schedules.json and source row membership | Confirmed |
| Four first/final reloads match | receipt flags and 564 state hashes per receipt; frozen weights hashes | Confirmed as retained runtime evidence; no inference rerun |
| Loss decreases | Independently recomputed first/last eight step means: .766601→.083554 and .763017→.059935 | Confirmed; optimization evidence only |
| No paired calibrated candidate | Independent nine-pair probe arithmetic from calibration-outputs.json | Confirmed |
| Diagnostic (.5,.5) gold pass 59/71 and 62/71, negatives rejected 30/30 and 29/30 | Independent cache replay | Confirmed; pair is not selected |
| No operational opportunities | Independent grouping of raw cached extractor outputs | Confirmed |
| Protected artifacts preserved | Matching before/after audits, 37,925 checks and no changes; frozen input/source/trained manifests match current bytes | Confirmed within audit/manifest evidence |
| No sealed/historical evaluation execution | Reviewed train/calibrate completions and development-only cache | Consistent; receipts are not a universal filesystem-access audit |

## Verification Performed

Read applicable AGENTS, STEERING, README/development guidance, PROTOCOL and LABEL-CONTRACT before results/author claims. Used read-only Python standard-library checks, without importing model or harness code: all 50 review targets, 125 input-freeze targets, 20 source-freeze targets and 33 trained-file targets hash-match current bytes. Protected before/after audit files match at harness and outer stage levels. Recomputed step counts, schedule equality, full-cycle membership, coverage-only exclusion, checkpoint hash deltas, loss summaries, calibration input membership, raw conflict counts, and all nine threshold gold/rejection counts. No model predictions/training, historical evaluation contents, or sealed contents were opened. No source or frozen artifacts were changed.

## Open Questions And Residual Risks

This is a bounded results review, not an independent rerun of training or a repeat implementation audit. Deterministic algorithms/RNG restoration and optimizer semantics are evidenced by the frozen prior-qualified implementation and runtime receipts rather than a newly executed model. The protected audits report 37,925 checks; this review did not independently rehash their entire historical corpus. No generalization, latency, or downstream answer-quality conclusion follows from the development results. Development lacks operational conflicts and cannot establish resolver benefit.

## Verdict

Ready — to accept and archive this completed negative training/calibration result. Not ready to open sealed evaluation or promote a candidate. No threshold qualifies, and PROTOCOL.md explicitly requires stopping without a calibrated candidate.

## Recommended Next Actions

Preserve the current evidence and sealed set, retain all locked baselines/A/v2/DB, and report the failed calibration gate. Do not expand the grid, select thresholds per seed, retrain, or evaluate sealed cases within this experiment. Any new experiment requires a separately authorized plan; this review proposes no tuning.

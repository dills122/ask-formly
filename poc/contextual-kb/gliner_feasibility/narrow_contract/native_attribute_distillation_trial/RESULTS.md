# Controlled native span-attribute distillation trial

The fixed preservation penalty reduced training-anchor drift, but did **not** produce a reliable improvement over matched continuation. Both arms fail the preregistered improvement and qualification gates, and treatment fails paired superiority. No candidate is promoted.

## What was controlled

For each seed, control and treatment started from the same frozen native-attribute epoch-6 adapter. They received the same 242 supervised questions, malformed labels, shuffled schedule, 124 updates, 992 supervised-row exposures and 248 anchor-row exposures. Both performed the same dropout-free anchor forward/backward computations. The sole objective difference was lambda 0 versus fixed lambda 100 on teacher KL (temperature 1). There was no weight search, checkpoint selection or post-evaluation tuning. These findings apply to this fixed strength and budget, not all possible distillation configurations.

Teachers supplied training-only distributions for 937 targets each: 488 valid occurrences and 449 malformed spans across the original 194 questions. Seed 1701 retained 915 targets and excluded 22; seed 1702 retained 926 and excluded 11. All 488 valid targets were retained in each seed. Exclusions included real teacher errors (18/8) and low-confidence correct predictions (4/3); 26 rows had no targets. Excluded targets remained supervised by gold. No evaluation example entered training or the cache.

The 28-input training freeze preceded fresh exposure; the full run froze 1072 inputs. Before optimization, all 376 historical operational outputs and 470 historical probes reproduced exactly for both frozen extractors and starting candidates. Evaluation used 416 questions and 622 supplied-span probes per candidate. Supplied gold or malformed offsets were never inputs to operational resolution.

## Fresh results

|Seed / arm|Correct valid roles|Semantic negatives rejected|All negatives rejected|Valid spans rejected|Whole-question exact|
|---|---:|---:|---:|---:|---:|
|1701 control|99/100|41/48|41/52|1|28/40|
|1701 treatment|99/100|37/48|37/52|1|28/40|
|1702 control|99/100|40/48|40/52|1|30/40|
|1702 treatment|99/100|35/48|35/52|1|30/40|

The four additional negative probes have unsupported token boundaries. They remain in the total denominator and are never counted as learned rejection. Fresh whole-question exactness was unchanged from the frozen extractor and starting candidate. High supplied-span accuracy does not establish successful extraction, retrieval or final answers.

Treatment versus control gained 3 and lost 7 correct fresh probe decisions for 1701; it gained 0 and lost 5 for 1702. Thus the fresh results fail the lossless paired improvement requirement.

## Retention and operational consequences

Counts below are previously correct probe decisions lost relative to the **starting candidate**, including role correctness rather than acceptance alone.

|Seed / arm|Fresh losses|Original attribute probes|Contrast probes|Retention probes|Historical total|
|---|---:|---:|---:|---:|---:|
|1701 control|3|1|4|2|7|
|1701 treatment|0|1|1|0|2|
|1702 control|1|2|2|0|4|
|1702 treatment|1|5|3|1|9|

Treatment partly preserved seed 1701's earlier decisions while sacrificing new rejection gains. That benefit did not replicate in seed 1702: historical losses increased from 4 to 9. Against matched control, historical treatment gains/losses were 5/10 for 1701 and 1/16 for 1702. Complete per-occurrence transitions, including confidence, are in the paired ledger; net totals are not used to hide regressions.

Seed 1701 retained the same two correct operational conflict resolutions in both arms, with no wrong resolution. Seed 1702 produced no correct operational repair in either arm. Its control made one wrong resolution (`srf-026`, a malformed merged span) and safely abstained on the quoted `Material` registration ambiguity. Treatment made both wrong resolutions, including assigning the quoted registration to `value` and losing a correct registration occurrence. Abstention retains unresolved raw output and is not counted as a successful repair. Fresh operational output did not improve.

The prior retention experiment is only a historical diagnostic, not the matched control. Across its 470 historical probes, current control gains/losses were 12/5 and 12/2 for seeds 1701/1702; current treatment gains/losses were 10/8 and 3/8. The historical comparison file retains legacy `contrast_*` field names, but its source is explicitly the prior **retention treatment**.

## Execution and evidence

All four runs completed 124 updates, changed 202 LoRA parameter tensors and changed zero frozen tensors. All eight first/final save-reload checks passed exact parameter and prediction parity. Teacher caches remained byte-identical; teachers were not loaded into training optimizers. The final scheduled-anchor KL was 0.009096 versus 0.000621 for 1701, and 0.025843 versus 0.002215 for 1702 (control versus treatment). This confirms a training preservation effect, not generalization. Calibration was gradient-only on predeclared training batches and did not choose lambda.

Training times were 1271.94/625.84 seconds for 1701 and 622.17/590.77 for 1702. The first control encountered a machine slowdown: a read-only process sample showed active native backward computation, and subsequent persisted optimizer steps confirmed progress. Runtime differences therefore are not a model-speed comparison.

All 37,592 prior protected-file checks passed unchanged, including A, v2, extractor baselines, historical adapters/evidence and locked data/DB chains. 15 tests passed before exposure. The same independent reviewer completed the raw-output and report reconciliation: ready as a completed negative experiment; neither arm qualifies for adoption.

Evidence: [protocol](PROTOCOL.md), [decision gates](test-output/decision.json), [paired superiority](test-output/superiority.json), [probe metrics](test-output/probe-scores.json), [operational scores](test-output/scores.json), [operational ledger](test-output/ledger.json), [paired occurrence ledger](test-output/paired-ledger.json), [paired summary](test-output/paired-summary.json), [historical comparison](test-output/historical-probe-comparison.json), [cache source audit](test-output/source-audit.json), [protected audit](test-output/protected-after.json), [independent review](REVIEW.md).

The controlled result does not justify adopting this preservation objective. It can restrain training-anchor drift, but here it also restrains useful corrections and preserves unsafe role decisions. A next design would need a different, explicitly tested way to distinguish trustworthy boundary preservation from teacher errors; simply continuing this fixed recipe is unsupported by these results.

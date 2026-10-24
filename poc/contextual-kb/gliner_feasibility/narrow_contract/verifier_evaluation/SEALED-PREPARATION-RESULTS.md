# Reviewed sealed evaluation preparation

## Outcome

Timing review 4 of 4: Ready for the scoped fix, with 32 passing tests and additional invalid-score checks. See REVIEW-4.md. User explicitly authorized the extra review.

Fresh evaluation was authored by a separate context and reviewed by independent contexts. Review 1 found three incomplete inventories and one negative-family mismatch. The author accepted the findings, preserved v1 provenance and prepared v2. Review 2 returned Ready for annotation/data preparation, with no outstanding findings. See SEALED-REVIEW-2.md. Question contents, detailed rationale and annotations remain under sealed/; the implementation/coordination context received only metadata, counts and ID-based findings.

## Qualified final dataset

- 40 questions, four disjoint primary groups of 10.
- 154 gold mentions across all six roles; four no-mention questions.
- 206 supplied probes: all gold plus 48 supported semantic negatives and four deliberate unsupported negatives.
- Zero normalized train/calibration duplicates. Independent review accepted two near-template comparisons after manual assessment; thematic overlap limits broad generalization claims.
- Dataset SHA256: d38c1ecca57b0e84099c133fb604124bb607a4093516d01b85bbb4c3c52c8ec6.
- Independent receipt SHA256: 4fbba2da26c90ff09bc43c919010d066f01c6a3e95c4c2cd24dad73d05a2bdf8.

## Execution evidence

Existing frozen CLI prepare stage completed successfully as sealed-preparation-v2. It verified the independent receipt, coverage, split leakage and exact native span transport; no encoder forward, predictions or optimizer. Training and calibration processes were not run. The preparation reference was reloaded and its frozen bindings verified successfully.

Both before/after protected audits passed 37,925 checks. All 48 previously frozen implementation artifacts also match. Both original extractor baselines, A, agent v2, data/DB and earlier experiments remain unchanged. No production code changes in this turn.

Receipts: test-output/sealed-preparation-v2/{preparation,completion,protected-before,protected-after,freeze}.json and test-output/sealed-preparation-summary.json. Prior RESULTS.md and review reports remain historical provenance; this document records the newer readiness state.

## Next execution

The remaining preparation prerequisite is complete. Next is the already specified fixed two-seed full training (124 updates and 992 exposures each), followed by development-only calibration. Use preparation reference sealed-preparation-v2; do not read or use fresh questions for training or threshold choice. A qualifying frozen shared threshold is required before historical/fresh evaluation. If none qualifies, stop without exposing fresh evaluation to model predictions. Actual model efficacy, historical replay and latency remain untested.

From repository root, the future explicit training command is:

    poc/contextual-kb/gliner_feasibility/env/.venv/bin/python -B poc/contextual-kb/gliner_feasibility/narrow_contract/verifier_evaluation/cli.py train --name full-verifier-v1 --from-run sealed-preparation-v2

This command has NOT been run. No adoption or improved-extraction claim is made from annotation/compatibility qualification.

# Full two-seed training and development-only calibration

## Decision

Both full training runs completed successfully. Development-only calibration found no qualifying shared threshold among the nine frozen pairs. No calibrated candidate exists. The sealed evaluation remains unopened for inspection or scoring; only byte-hash integrity checks were used. The actual evaluation stage was never invoked. A direct gate check rejected the decision before calling even a sentinel loader.

## Training evidence

Each seed (1701,1702) completed124 updates,992 exposures and all216 optimizer-eligible training questions, with the exact preregistered schedule. The26 coverage-only rows did not enter optimization. Each run changed198 trainable state entries and zero frozen entries. Update1 and124 checkpoint reloads matched all564 state entries and training-panel predictions for both seeds.

First8 versus last8 update mean training BCE: .7666 to .0836 (1701), .7630 to .0599 (1702). Loss reduction confirms optimization, not generalization or answer accuracy.

## Development-only outcomes

30 questions per seed;71 supplied valid mentions and30 malformed probes. At the predeclared (.50,.50) pair, shown diagnostically and NOT selected:

| Check | 1701 | 1702 |
| --- | ---: | ---: |
| Complete boundary plus exactly correct role on valid probes | 59/71 | 62/71 |
| Malformed probes rejected by boundary score | 30/30 | 29/30 |
| Eligible operational conflict groups | 0 | 0 |
| Operational repairs / wrong repairs / lost correct mentions | 0 / 0 / 0 | 0 / 0 / 0 |
| Runtime errors / unsupported gold | 0 / 0 | 0 / 0 |

Every grid pair fails the valid-mention gate; ranges are12–26 failures for1701 and9–19 for1702. This does not mean zero correct mentions. Higher thresholds within the frozen grid do not resolve the failures. No threshold expansion, per-seed selection, retraining or fresh evaluation was performed.

At(.50,.50),1701 failures comprise8 no passing role,2 wrong single role,1 multiple-role,1 boundary failure;1702 comprises4 no-role,3 wrong-role and2 multiple-role. Recurrent issues include explicit configuration properties, supplied registration names, literals and UI-adapter role distinctions. Malformed rejection is stronger than valid-role reliability on this development set.

Operational limitation: the30 calibration questions yielded zero eligible same-offset role-conflict groups in either frozen baseline output. Thus passthrough preservation is observed, but actual repair benefit is not established. Supplied probes are a separate oracle-span test and were never injected as operational candidates.

## Preservation and artifacts

Both baselines,A,v2,data/DB and previous experiments unchanged. Training and calibration each passed37,925 protected checks before/after. All85 prior preparation artifacts also verified unchanged. Sealed fresh contents were not parsed by these stages. No source code changes.

Training: ../verifier_harness/test-output/verifier-full-verifier-v1/
Launch: test-output/full-verifier-v1/
Calibration/full nine-pair ledgers: test-output/full-calibration-v1/
Derived receipts: test-output/full-training-summary.json, full-calibration-analysis.json, full-run-preservation-summary.json.
Independent review is recorded separately in FULL-TRAINING-REVIEW-1.md.

## Next decision

Do not open sealed evaluation or promote these adapters. A further experiment would need to address valid-role failures and establish development coverage of actual eligible operational conflicts before further training. This result does not authorize changing the frozen contract, decoder, thresholds, annotations, baselines or data/DB. The trained artifacts and complete negative result remain available for later diagnosis.

## Independent result review

Review1 of3 returned Ready to accept the completed negative result; not ready for sealed evaluation or promotion. It independently verified schedule membership, development cache membership, all nine threshold calculations, absence of eligible conflicts, and frozen artifacts/weights. It found no actionable integrity or interpretation defects. No model inference or sealed-content inspection was performed by the reviewer. See FULL-TRAINING-REVIEW-1.md for verification limits.

# Independent review

Review instance: 4 of 4. Reviewed 21 October 2026.

## Findings

No blocking defect found in the bounded record-identity and compatibility revision.

**P2 — Original first-save loss comparison was omitted (accepted residual verification gap).** `training_smoke.py:117–126` saves the trained adapter and compares decoded predictions after fresh-base reload, but does not capture original pre-save losses as required by PLAN step 4. Identical decoded predictions do not establish equality of the training objective. The supplemental saved-adapter reserialization now checks exact losses, parameters, batches and outputs; it cannot recover the uncaptured original values. Keep this distinction in reports and include first-save loss capture in any future approved training harness. This is non-blocking for the narrower compatibility result, not satisfaction of every original acceptance item.

Initial dense-oracle coverage concern was addressed within this review: `compatibility.oracle_records` now transports gold assignments through native packed-to-ragged conversion and decoding and compares all 24 field sets. It still supplies perfect candidates, assignments and selected instances; it does not establish public inference accuracy or learned instance selection.

## Plan Review

The selected anchorless representation is implemented without changing canonical pilot annotations or inventing per-question anchor rules. `target_anchor` remains a field. The existing 32 learned instance queries permit two records sharing the same target occurrence. Explicit empty relation tasks preserve zero-edge supervision. The natural-mode collision control remains failing as intended.

The recorded smoke performs exactly 24 optimizer steps on the same exposed pilot, with four task-gradient checks on P02. It uses the installed trainer's LoRA setup followed by a direct AdamW loop, not the full trainer scheduling/checkpoint-selection workflow. Its parameter inventory and source checks support encoder-only adapter training. The original first-save loss criterion is the exception above.

Scope matches the bounded revision. No full training, annotation expansion, evaluation, retrieval, A execution, or knowledge changes were performed by this reviewer. Existing repository dirty/untracked state was inspected and preserved; main HEAD was c3091328f49d53de6b41a49c4fe5aa8f1c45e516.

## Author-Claim Reconciliation

The preliminary findings were sent before reading AUTHOR-EXPLANATION.md and FINDINGS.md. The author acknowledged dense coverage limits; those were not hidden claims. Later verification extensions were inspected as changes within this fourth review.

| Claim | Evidence | Result |
| --- | --- | --- |
| Unchanged gold and exact occurrence/attachment transport | revision tests and strict native target tests | Confirmed on 24 pilot cases |
| Same-target identity is representable | Ragged and supplemented dense oracle, natural-mode control | Confirmed as capacity, not learned quality |
| Four task paths reach adapters | Retained task gradient records and smoke implementation | Supported on fixed P02 only |
| 24 bounded joint updates, 144 adapter tensors changed, zero frozen parameters changed | Original smoke code, inventory, steps and report | Supported by recorded execution; optimization not rerun |
| Reload output parity | Original before/after JSON | Independently equal on 24 outputs |
| Supplemental loss/weight/output parity | v3 before/after artifacts and implementation | Independently equal: 24 cases, 478 parameter entries |
| Protected integrity | Protected-before manifest | Independently rehashed 137 paths, no mismatch |
| Generalization or full-training readiness | No such evidence | Not established and not claimed |

The initial supplement failed exact loss equality while parameters/outputs matched. The retained diagnostic attributes differing prepared batches to Python RNG not reset by torch-only seeding. The revised check resets both RNGs. The second attempt's evidence serialization failure and third successful attempt remain recorded; tolerances were not weakened. These were non-optimizing checks.

## Verification Performed

From identity_revision, independently ran:

`PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 ../../env/.venv/bin/python -m unittest test_revision test_compatibility`

Initial frozen revision: 10 tests passed in 4.206 seconds. After dense-oracle extension: 10 tests passed in 4.413 seconds. Loader/deprecation warnings remain; no tests skipped. Shell initialization emitted an unrelated parse message on the initial invocation, but the Python test process completed successfully.

Independently checked original review freeze: all 27 entries matched before supplementation. Checked final review freeze: all 17 entries matched. Rehashed 137 protected paths twice, including after supplementation; no mismatch. Inspected four isolated task checks plus 24 finite-loss optimizer records. Original pre/post decoded JSON is equal on 24 cases.

Inspected the retained final supplemental run rather than rerunning its exclusive-output test: 11 tests passed in 30.482 seconds, zero optimizer steps. Independently compared v3 before/after JSON for losses including batch fingerprints, all 478 parameter hashes, and 24 outputs: exact equality. No full training or optimization rerun was performed. Protected bytes were hashed only; no sealed/evaluation/knowledge contents were inspected.

## Open Questions And Residual Risks

The pilot is training-exposed and cannot support held-out claims. Oracle field scores establish representation, not semantic decomposition. Nonzero adapter gradients do not establish that frozen task heads can learn the desired task sufficiently. Full Trainer.train, development selection, two-seed stability, semantic scoring and evaluation isolation remain future work. Audit hooks are defense in depth, not a general sandbox. Original first-save loss equality remains unobserved.

## Verdict

**Ready with non-blocking follow-ups**, specifically for accepting the bounded identity-revision and mechanical compatibility evidence. The source-target collision blocker is removed. This verdict does not establish semantic learning quality, complete retrieval plans, or readiness/authorization for full training.

## Recommended Next Actions

Carry the anchorless mode and explicit negative relation supervision into a separately approved experimental protocol. Before full training, prepare the approved grouped data, custodian-sealed evaluation, complete training/selection workflow, deterministic RNG handling, and original first-save loss/parameter/output capture. Any task-head training change needs separate compatibility evidence. No heavy architectural pivot is indicated by this review.

The additional authorized fourth review is now exhausted. No further review instance or full-training run follows automatically; further scope requires human action.

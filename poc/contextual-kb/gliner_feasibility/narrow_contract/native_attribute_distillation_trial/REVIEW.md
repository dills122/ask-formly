# Independent review

Review instance: 1 of 3

Scope: only `native_attribute_distillation_trial/`; reviewer owns this report. Branch `main`, HEAD `c3091328f49d53de6b41a49c4fe5aa8f1c45e516`. Extensive unrelated dirty/untracked workspace content is excluded. No implementation changes made.

## Blind semantic preliminary pass

Read the fresh questions, gold, family assignments and probe candidates before training data, prior results, implementation or author explanation. Checked against the canonical narrow mention contract and root/POC instructions.

Reviewed all 40 questions, 100 gold mentions, 48 semantic negatives (12 each clipped API, merged API/literal, quote/nested and prose), and 4 transport-only negatives. Independently verified every gold/probe substring against its offsets with Python. Opaque expressions, invented API spellings, repeated occurrences, Unicode names, occurrence-specific roles and all four empty cases agree with the contract.

Initial concern about DF21 escaping was resolved without edits: an independent parsed-codepoint check confirms exactly one actual backslash (92) followed by apostrophe (39). The apparent doubling came from tool/JSON representation. No semantic corrections are required; no actionable findings remain in the blind fresh-data review.

## Implementation preliminary pass

Read protocol, tests, schedules/objective, cache creation/validation, training loop, save/reload, assessment/comparison and protected-chain code before author explanation. No blocking implementation findings. Cache query IDs fail closed dynamically before backward; upfront validation would be a non-blocking refinement only.

Independently ran all 15 unit tests using the pinned GLiNER virtualenv; all passed. Verified the first 194 supervised rows and malformed targets equal their original source artifacts. Parsed both teacher caches: 937 represented targets, 915/926 retained for seeds 1701/1702, no unsupported targets. Code freezes/evals teachers under no_grad, hashes full state, detaches probabilities, and masks wrong/low-confidence teachers. Native supervised labels stay unmasked. Two arms share starts, schedules, optimizer and RNG use; anchor eval-mode forwards preserve dropout state. Zero-anchor denominator follows protocol. Save/reload checks restore RNG and demand exact predictions/parameters.

Inspected actual preflight code and receipt: zero optimizer updates; control anchor gradient zero; treatment/raw norm scaling 100x (7.57737/0.0757731 and 2.19049/0.0219057), unchanged RNG and parameters. Deterministic perturbation avoids identical-start zero-KL illusion. Scale diagnostic ratios range 0.00664–0.17607; this establishes gradient presence, not expected success. Final actual unperturbed-training KL evidence remains required.

Gate implementation preserves original and starting-candidate correctness, separates semantic no_entity rejection from abstention, and requires both seeds without fresh gains offsetting old losses. Prior retention is labeled historical rather than matched control. Pending author reconciliation, freeze and final artifacts; no final efficacy verdict.

## Plan Review

The bounded plan isolates λ0/100 with two fixed seeds, 124 updates, 992 supervised and 248 anchor-row exposures per arm. It has explicit old/fresh gates and preserves all four results without selection. No heavy pivot required. This is an experiment, not a claim of extractor qualification.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status | Consequence |
| --- | --- | --- | --- |
| Same starts/supervision/order/budget, sole λ difference | policy.py, run.py training loop | Confirmed by code; execution pending | Audit final receipts and losses |
| 937 targets and real masked teacher errors | Both parsed caches and audits | Confirmed: retained 915/926 | Mask covers real mistakes |
| Training is original194 plus authorized48 | Independent exact JSON equality with original and contrast artifacts | Confirmed, including all negatives | No added evaluation training rows |
| Actual 0/1/100 gradients and stable RNG | preflight.py and gradient-preflight.json | Confirmed receipt/code; reviewer did not rerun model smoke | Final actual-training evidence still required |
| Fixed coefficient, no outcome tuning | Protocol precedes fresh exposure; separate fresh authorship | Consistent with available provenance | No coefficient changes after freeze |
| Both-seed qualification and strict no-loss superiority | assess.py, compare.py, gate/effect tests | Confirmed | Failures must remain visible |

## Verification Performed

Independent command: `poc/contextual-kb/gliner_feasibility/env/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/gliner_feasibility/narrow_contract/native_attribute_distillation_trial -p 'test_*.py' -v`: 15 passed. Independent Python checks verified fresh source slices/codepoints, cache counts, original194 identity, suffix48 identity and complete contrast training/negative equality.

## Open Questions And Residual Risks

Final four-arm inference, exact historical replay, save/reload, teacher/cache preservation, leakage overlap audit, paired correctness ledgers and protected-chain verification remain execution evidence to review. Finite synthetic diagnostic sets cannot establish generalization. Low initial KL is expected for identical starts; perturbation smoke must not be described as actual optimization efficacy.

## Verdict

**Pretraining readiness: Ready**, conditional on writing and successfully verifying the complete training freeze before first fresh exposure or optimization, as prescribed by protocol. No actionable blocking findings. This is permission to execute the already-authorized bounded experiment, not a final correctness/efficacy verdict. Same review instance will audit all final arms.

## Recommended Next Actions

Freeze code, protocol, schedules, inputs, cache identities/bytes and provenance; execute all fixed arms without tuning; retain failures and complete final evidence for this same reviewer.

## Partial execution audit (same instance)

Independently recomputed SHA-256 for all 28 training-freeze entries and all 1,072 run-freeze entries: zero changes. Both teacher cache files still match their cache-creation audit digests. Independently compared all old stored inference records against historical originals: each seed reproduces 376 original and starting-candidate operational outputs and 470 old supplied-span records exactly.

Seed 1701 control: all 124 completed loss records independently match the predeclared supervised IDs, anchor IDs, retained-anchor counts and λ0 objective. Receipt records 992 supervised / 248 anchor-row exposures, no frozen tensors changed, 202 trainable tensors changed, unchanged cache. Starting parameter map equals original native epoch-6 receipt. Both step31 and step124 reload receipts require exact predictions and parameters and passed. Raw KL begins at approximately numerical zero (-8.3e-9), later reaches 0.04654: expected divergence under supervised updates, not a zero-KL-only run.

Remaining arms and endpoint scoring are still pending. No final efficacy verdict is issued from this partial audit. Reported CPU slowdown does not justify any schedule or optimization change.

### Seed 1701 paired audit

Independently verified treatment's 124 schedule/objective/mask records, identical initial parameters to control, both reload receipts, 992/248 exposure totals, 202 changed trainable tensors and zero frozen/cache changes. Both freeze manifests remain unchanged. Actual treatment raw KL reaches 0.01803; it contributes to the λ100 objective after the identical start.

Against control, treatment gains/loses correct supplied-span outcomes: fresh 3/7, old 0/4, contrast 3/3, retention 2/3. Starting-correct outcome losses for control are 3/1/4/2 and treatment 0/1/1/0 across those same sets. Fresh valid roles are 99/100 for both; negative rejection is 41/52 control versus 37/52 treatment (48 semantic negatives plus four transport failures; semantic denominator is reported separately). Every operational resolved output is identical between the two arms across all eleven splits. Thus seed1701 provides no operational treatment gain and already violates strict no-loss treatment superiority. These are partial paired findings; all four endpoints remain required for final audit.

## Final Findings

No actionable implementation or reporting defects remain. The experiment failed its declared adoption criteria; this is an observed result, not an implementation finding to tune away.

- Both arms fail improvement and full qualification. Independent raw-resolution audit confirms seed1701 has two correct/zero wrong resolutions in each arm; seed1702 control has zero correct/one wrong, and treatment zero correct/two wrong.
- Seed1702 treatment introduces an unsafe resolution relative to matched control: `va-f03-q04` explicitly names a registered type `'Material'`. Control abstains at value confidence 0.4477803; treatment selects wrong `value` at 0.5051600, removes the correct registration occurrence and produces a clean wrong envelope. Both seed1702 arms also wrongly resolve merged span `srf-026`.
- Treatment superiority is false. Independently counted control-to-treatment probe gains/losses are seed1701 fresh3/7, old0/4, contrast3/3, retention2/3; seed1702 fresh0/5, old0/6, contrast1/4, retention0/6. Fresh correctness cannot offset these losses.

## Final Plan Review

All four fixed endpoints completed without selection or protocol changes. Each has 416 operational cases and 622 supplied-span probes, preserving all old and fresh sets. Both seeds and every failure remain in the report. No new training example came from evaluation: exact question intersections are empty across all eleven sets. Evaluation offsets stay separate from operational resolver input. The plan is complete; no candidate should be promoted.

## Final Author-Claim Reconciliation

RESULTS.md accurately reports the independently checked fresh counts, historical starting-correct losses, operational consequences and gate failures. Historical-retention comparison totals and final scheduled-anchor KL figures match their artifacts. The legacy `contrast_*` names in the historical comparison are explicitly disclosed as referring to prior retention treatment. Runtime slowdown is disclosed and timing is not used as a speed comparison. Lower training-anchor KL is bounded to training preservation, not claimed as generalization.

## Final Verification Performed

Independently inspected every final loss record: all four runs have 124 updates, exact predeclared supervised/anchor IDs and retained-anchor counts, λ0/100 objective arithmetic, 992 supervised and 248 anchor-row exposures. Both arms start identically per seed. All four receipts record 202 changed LoRA tensors, zero changed frozen tensors, and caches whose current byte hashes equal creation hashes. All eight step31/124 exact reload receipts pass. Actual mean training KL decreases control-to-treatment from 0.00609674 to 0.00216537 (1701), and 0.0122473 to 0.00231841 (1702); the unperturbed training logs establish nonzero preservation activity after the identical start.

Independently recomputed all 28 training-freeze and 1,072 run-freeze hashes: zero changed. Independently recomputed all **37,592 unique protected-file SHA-256 checks** across the entire previous protection chain, including the 44-file compatibility freeze: zero changed. This verifies the locked artifacts rather than merely trusting the generated protected-after receipt.

Independently recomputed probe correctness transitions from raw predictions with the strict scored/confidence>0.5 condition, checked every operational endpoint against its gold identity and resolution, and reconciled report tables and gates. Both seeds reproduce historical 376 operational and 470 probe records exactly before training. Unit tests passed independently before exposure (15); no source edits occurred afterward. No expensive model training/inference was rerun by this reviewer; execution validation uses immutable inputs, code, raw outputs, gradients and receipts.

## Final Residual Risks

The 40 fresh questions are synthetic bounded diagnostics, not representative production traffic. Identical exact question checks cannot rule out conceptual resemblance between synthetic train/eval families. Only one fixed λ/budget was tested. This trial supplies negative evidence for adopting this recipe, not proof that every distillation method fails. No retrieval or answer-quality claim follows from this mention-layer experiment.

## Final Verdict

**Ready** — the controlled experiment and its negative report are review-complete. **Neither candidate arm is qualified or recommended for adoption; treatment superiority fails.** Review instance remains **1 of 3** throughout pretraining and final audit. No further reviewer or tuning loop is required. Final report-only freeze may now be written after all authors are quiescent.

## Final Recommended Next Actions

Preserve all four endpoint artifacts and this report unchanged; create the final artifact freeze, verify it, and close the bounded trial with its failed gates visible. A different experiment requires a new explicit scope rather than continued tuning of these results.

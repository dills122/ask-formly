# Native span-attribute contrast experiment — completed, not ready for adoption

This fixed continuation improved merged API/literal rejection substantially, but did not produce a safe improvement across both models. Both preregistered improvement gates and full qualification failed. Neither candidate is promoted. Training and evaluation completed without selecting an epoch, tuning after fresh exposure, or changing either frozen extractor, A, v2, or the data/DB.

## What ran

The reviewed protocol added 48 explicitly annotated questions and 85 malformed candidates to the unchanged 194-question/449-negative replay: 242 training questions and 534 negative spans total. Both existing native-attribute candidate adapters continued for exactly four epochs/124 optimizer updates each. Each consumed 968 training examples. Epoch-one and epoch-four save/reload predictions and parameter hashes matched exactly. Only LoRA parameters changed; frozen parameters did not.

Native GLiNER qualified span-query supervision and its existing attribute scorer were reused. This is boundary/query supervision followed by native attribute softmax inference, not a new classification head. The operational replay supplied only the original extractors' exact occurrences, used the frozen conservative resolver, and retained unresolved raw output on abstention or partial overlaps. Supplied gold/malformed-span audits were separate from operational resolution.

Before training, both models reproduced all 296 previous operational raw and candidate outputs and all 156 old probe predictions exactly. Evaluation added 40 independently authored fresh questions, giving 336 operational questions per model. Fresh probes contained 106 valid spans, 40 semantic negatives and four intentionally unsupported mid-identifier offsets. The 156 old probes contain 106 valid spans, 46 semantic negatives and four unsupported offsets. Unsupported transport never counts as learned rejection.

## Supplied-span results

“Before” means the previous native-attribute candidate; “after” means this fixed continuation. Correct valid spans require both the exact supplied occurrence and the correct role. These scores do not establish extraction completeness or final-answer accuracy.

| Probe set / seed | Correct valid roles, before → after | Negative rejection, before → after | Semantic rejection after | Valid spans rejected after |
| --- | --- | --- | --- | --- |
| Fresh / 1701 | 104 → 105 / 106 | 29 → 32 / 44 | 32 / 40 (80%) | 1 |
| Fresh / 1702 | 105 → 105 / 106 | 30 → 31 / 44 | 31 / 40 (77.5%) | 1 |
| Old / 1701 | 105 → 105 / 106 | 26 → 32 / 50 | 32 / 46 (69.6%) | 1 |
| Old / 1702 | 105 → 105 / 106 | 31 → 31 / 50 | 31 / 46 (67.4%) | 0 |

On the 40 fresh semantic negatives alone, rejection improved from 29/40 to 32/40 for 1701 and 30/40 to 31/40 for 1702. The table's 44-negative denominator additionally includes four unsupported transport probes.

Both models now reject all ten fresh clipped-API probes, but both already did so before continuation. Fresh merged API/literal rejection improved from 3/10 to 10/10 for 1701 and 4/10 to 9/10 for 1702. That gain did not generalize reliably to old clipped-path cases: rejection decreased from 3/10 to 2/10 and 5/10 to 2/10 respectively.

The aggregate numbers conceal regressions. The complete paired [probe ledger](test-output/probe-ledger.json) records every transition:

| Set / seed | Newly correct | Previously correct lost |
| --- | --- | --- |
| Fresh / 1701 | 8 | 4 |
| Fresh / 1702 | 5 | 4 |
| Old / 1701 | 8 | 2 |
| Old / 1702 | 5 | 5 |

Both models lost the same four fresh negative successes: an inner object fragment became a value, and three prose phrases changed from explicit rejection to low-confidence abstention. Abstention is reported separately and is not credited as learned `no_entity` rejection. Old 1701 regressions include the clipped `formState['view.mode']` and broken quote `'it is ready`. Old 1702 loses three clipped-path rejections and two merged-span rejections. Every old prior-correct loss fails the preservation gate.

Both models still reject the valid full API `field.model.shipping.city` on the fresh audit. The old valid quoted registration `'lagoon-input'` remains wrong: 1701 rejects it; 1702 now calls it an API reference. Consequently, 1702's old valid acceptance reaches 106/106 without improving its correct-role score of 105/106. Acceptance alone would give a misleading success claim.

## Operational resolution

Fresh complete-question exactness is unchanged across original extractor, previous candidate and current candidate: 37/40 for 1701 and 36/40 for 1702. The fresh 1702 partial overlap remains invalid/unresolved. Fresh supplied-span improvements therefore did not improve operational extraction in this resolver.

1701 preserves its two previous correct repairs (`roles-04` placeholder value and `va-f03-q04` quoted Material registration), with zero wrong resolutions, zero lost correct raw mentions, and zero nonconflicting changes. Its old cross-role partial overlap remains unresolved. Its overall gate nevertheless fails because two old correct probe rejections were lost.

1702 has zero correct operational repairs and one wrong resolution. It still resolves the malformed merged `props.label: 'entry[2]'` in `srf-026` to `value` (confidence 0.5233), producing a structurally valid but wrong envelope. The span-set accepted F1 remains 93.14%, below the original extractor's 94.06%.

For quoted Material in `va-f03-q04`, 1702 now abstains at confidence 0.4681 instead of choosing the previous wrong value role. This restores the original raw registration mention and unresolved conflict. It is safer than the previous destructive resolution, but is not a correct repair. The vocab set becomes invalid again; accepted F1 changes from the previous candidate's 94.94% to the original 94.87%. This is explicitly disclosed in [prior metric changes](test-output/prior-metric-changes.json), rather than treating the prior valid-but-wrong envelope as a successful baseline. No original correct raw mentions or nonconflicting mentions are lost in the new operational outputs.

The [operational ledger](test-output/ledger.json) contains all six conflict-bearing cases across both models, raw/gold/prior/current mentions, errors, and native decisions. The [decision receipt](test-output/decision.json) records the separate failed paired-improvement and full-qualification gates. Rejection remains below the required 90%, false rejection remains, and the required zero-harm/each-seed-correct-repair conditions are not satisfied.

## Evidence and conclusion

Nine TDD tests passed before the run. Both native training-target compatibility checks covered all 242 questions/534 negatives. The reviewed training freeze has 15 inputs; the full run freeze has 666 inputs and verified at completion. The [protected audit](test-output/protected-after.json) checked 37,199 protected entries with zero changes, including the previous experiment's 139-file final freeze and the existing A/v2/data/DB protection chains.

Training receipts and epoch-one/four parity evidence are under [1701](test-output/1701/training-receipt.json) and [1702](test-output/1702/training-receipt.json). Full scores are in [scores](test-output/scores.json), [probe scores](test-output/probe-scores.json), and [paired probe transitions](test-output/probe-transitions.json). The independent reviewer approved the protocol, annotations and implementation before training and completed the final independent audit in [REVIEW.md](REVIEW.md): completed, auditable experiment; not ready for adoption. The report was reconciled with that review.

Results show improved merged-span rejection under this contrastive continuation. There was no matched continuation-only control, so the effect of the added examples alone was not isolated. It also demonstrates incomplete generalization and interference with previously learned boundaries, plus persistent operational role confusion. More of the same augmentation cannot yet be assumed to make this reliable. Keep the frozen extractors operational and these two continuation adapters experimental; any next training experiment needs a new preregistered design and fresh evaluation, not tuning on these exposed results.

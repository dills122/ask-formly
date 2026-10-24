# Matched native-attribute retention experiment — completed, not ready for adoption

The retention treatment did not beat continued replay under the preregistered superiority rule. Both control and treatment failed their independent preservation/improvement and full-qualification gates. All four fixed candidates completed; none is promoted. The control matters: additional original-data training alone changed rejection performance, so improvements over a starting checkpoint cannot automatically be credited to added contrast examples.

## What was controlled

Each seed's control and treatment began from exactly the same native-attribute epoch-six checkpoint, before the previous contrast experiment. Each ran 124 optimizer updates / 992 examples, with fresh optimizer/RNG initialization. Control replayed only original 194 training questions. Treatment shared seven of eight replay slots per update and replaced the eighth with existing contrast training material at 0.25 weight. No evaluation question or probe became training data.

This is a bundled sparse, reduced-weight replacement intervention. Control's total raw example weight was 992; treatment's was 868+31=899, giving mean update loss coefficients 1 versus0.90625. It does not isolate weighting, replacement, or scaling individually. The previous contrast experiment remains a historical diagnostic, not a matched control.

All four candidates changed 202 LoRA tensors and zero frozen tensors. First-save(update 31) and final-save(update 124) prediction and parameter parity passed for every candidate. Before optimization, both original extractors and starting candidates reproduced all 336 historical operational outputs and 306 old probe predictions exactly. Each final candidate was evaluated on 376 questions and 470 separate supplied-span probes.

## Fresh results

All four candidates correctly classified all 112 supplied valid spans, with zero valid-span rejection. Both starting candidates already scored 112/112, so this is retention, not a new gain. Supplied-span correctness does not establish that the extractor finds those spans itself.

| Seed | Starting semantic negatives rejected | Control | Treatment | Control → treatment correctness gains/losses |
| --- | --- | --- | --- | --- |
| 1701 | 33/48 | 34/48 (70.8%) | 35/48 (72.9%) | 2 gained, 1 lost |
| 1702 | 37/48 | 38/48 (79.2%) | 38/48 (79.2%) | 0 gained, 0 lost |

Four additional mid-identifier offsets per fresh set are unsupported transport, never credited as learned rejection. Including them, rejection is34/52 versus35/52 for 1701 and 38/52 versus38/52 for 1702. The required 90% rejection threshold is unmet even on the semantic-only denominator.

Whole-question operational exactness remained 34/40 for 1701 and 35/40 for 1702 across original extraction, starting candidate, control and treatment. The fresh 1701 partial overlap remains unresolved. Thus112/112 supplied-role accuracy does not mean all 40 questions were extracted correctly, and no final-answer accuracy claim follows from these scores.

## Historical retention

“Native-old” is the 156-probe earlier native-attribute audit (106 valid, 46 semantic negatives, 4 unsupported). “Contrast-old” is the 150-probe previous contrast audit (106 valid, 40 semantic negatives, 4 unsupported). Correct valid roles require the correct role, not mere acceptance. Prior-correct losses below are relative to this experiment's starting checkpoint, and include rejection→abstention as a loss of learned rejection.

| Seed / arm | Native-old correct valid roles | Native-old semantic rejection | Native-old prior-correct losses | Contrast-old correct valid roles | Contrast-old semantic rejection | Contrast-old prior-correct losses |
| --- | --- | --- | --- | --- | --- | --- |
| 1701 control | 105/106 | 30/46 | 1 | 103/106 | 28/40 | 6 |
| 1701 treatment | 106/106 | 28/46 | 4 | 105/106 | 30/40 | 4 |
| 1702 control | 105/106 | 33/46 | 2 | 104/106 | 30/40 | 5 |
| 1702 treatment | 105/106 | 30/46 | 3 | 105/106 | 28/40 | 4 |

For total-negative rejection, the corresponding denominators are 50 and 44; the numerators are unchanged. Valid-span rejection counts equal 106 minus correct valid-role counts in these final historical endpoints. Every arm loses previously correct old probes and therefore fails preservation, even where its aggregate score improves.

Compared directly with control, 1701 treatment gains 8 and loses 5 old correct probe outcomes; 1702 treatment gains 2 and loses 6. The 1701 fresh gain is also accompanied by a fresh loss, and 1702 has no fresh gain. These observations fail the separate treatment-superiority gate. Complete endpoint confidences and every gain/loss are retained in the [paired ledger](test-output/paired-ledger.json) and [summary](test-output/paired-summary.json).

One useful localized result is 1701 treatment finally assigning the old quoted `'lagoon-input'` occurrence its correct registration role. It does not compensate for lost boundaries elsewhere. Historical comparisons with the previous contrast continuation are preserved separately in [historical probe comparison](test-output/historical-probe-comparison.json) and the historical score columns; no historical candidate is selected.

## Operational safety

Both 1701 arms preserve the same two correct existing repairs(Material registration and placeholder value), with zero wrong resolutions. They produce no new operational repair beyond the starting candidate. Old and fresh partial overlaps remain unchanged.

Both 1702 arms still make two wrong operational resolutions and zero correct repairs. Both remove the original correct quoted Material registration by selecting `value`(control confidence 0.8774,treatment 0.8481). For the malformed merged `props.label: 'entry[2]'`, control selects API reference (0.9761), while treatment selects value (0.9366); both are wrong. Both turn these original invalid conflicts into structurally valid but incorrect envelopes. The span-set accepted F1 remains 93.14%, below the original extractor's 94.06%.

The previous contrast candidate had safely abstained on Material; neither current arm reproduces that historical safety gain. They start from an earlier candidate and do not qualify for adoption. The [operational ledger](test-output/ledger.json) preserves original, starting and final cases; [scores](test-output/scores.json) include the prior contrast endpoint separately. Partial overlaps and no_entity/low-confidence abstention are never counted as repaired extraction.

## Decision and evidence

Both per-arm paired improvement gates, both full-qualification gates, and treatment superiority are false: [decision](test-output/decision.json), [superiority](test-output/superiority.json). Preservation losses alone prevent adoption; remaining rejection, boundary, invalid-output and wrong-resolution failures reinforce that result. A reliable advantage from this particular retention intervention was not established. Continued replay itself also causes interference, so attributing all previous regressions solely to contrast examples would be unsupported.

Twelve tests passed, including actual torch gradient scaling and preservation/superiority semantics. Native compatibility covered both starting adapters and all 242 authorized training rows / 534 negative spans. The 19-input training freeze preceded fresh exposure; the 810-input run freeze verified at completion. The [protected audit](test-output/protected-after.json) checked 37,337 entries with zero changes, including the previous 138-file contrast freeze and A/v2/data/DB protection chains. Training receipts and parity artifacts are under each seed's control/treatment directory. The independent reviewer approved the protocol before training and completed final independent evidence reconciliation in [REVIEW.md](REVIEW.md): a completed, credible negative experiment; not ready for adoption.

Keep the original extractors and existing agent layer unchanged. These results do not support another unbounded pass of the same training strategy. Any next experiment should address why the native role/rejection scores confidently accept malformed spans and trade off previously correct boundaries, with a new explicit hypothesis and fresh test—not tuning against this now-exposed packet.

# Native GLiNER span-attribute training results

**Native span-role training works, but this paired candidate is not safe to adopt.** Both models learned substantially better role selection on supplied correct spans. Model 1702 nevertheless lost a correct role in an operational conflict and legitimized a malformed span. The predeclared both-model improvement gate fails; full qualification fails for both. Neither frozen extractor is replaced, and no seed is selected after seeing results.

## What was actually trained

Two isolated copies of the frozen role_boundary_adaptation epoch 6 adapters were continued for 6 fixed epochs each: 194 existing training questions, 449 generated malformed span targets per pass, 150 optimizer updates per model. GLiNER native qualified span queries supervise seven roles, including no_entity, alongside ordinary entity replay. No spaCy component, new classification head, document-level classifier, third-party source patch, or new knowledge data was used.

`InputExample` has no first-class attribute field. The POC lowers labels into the exact qualified native entity queries used by `entity_attributes`; the native boundary losses train those span scores, and native inference applies softmax. A pinned private native force-scoring routine is used to score supplied exact frozen-extractor spans. This is not a claim that public GLiNER exposes supplied-span classification or a documented dedicated attribute-training API. [Compatibility proof](COMPATIBILITY.md) includes qualified-query-only gradient evidence, occurrence sensitivity, all-role public/helper score parity, and actual save/reload checks.

Both original extractors were run with flat decoding on 296 questions each: 40 independent fresh requests plus 256 exposed diagnostics. All 256 prior raw outputs reproduced exactly for both models before training. Both candidate scorers were run before/after on the same frozen spans and on a separate 156-probe fresh supplied-span audit. Gold/probe offsets never enter operational conflict resolution. The latter only removes a losing role on identical offsets; partial overlaps, no_entity, low confidence and unrepresentable boundaries retain the original raw output.

## Supplied-span role and rejection audit

These are predictions at supplied exact spans, not end-to-end extraction or answer accuracy.

| Metric | Model 1701 | Model 1702 |
| --- | ---: | ---: |
| Valid roles correct before → after |43/106 →105/106|56/106 →105/106|
| Valid role accuracy after |99.06%|99.06%|
| Valid spans incorrectly rejected |1/106|1/106|
| Negative probes learned-rejected before → after |0/50 →26/50|0/50 →31/50|
| Overall negative rejection recall |52.00%|62.00%|
| Representable semantic-negative rejection recall |26/46 =56.52%|31/46 =67.39%|
| Rejection precision |26/27 =96.30%|31/32 =96.88%|
| Unsupported mid-identifier probes |4/4|4/4|

Each 50-negative denominator comprises 40 malformed candidates, 6 ordinary-prose candidates, and 4 intentionally unrepresentable mid-identifier boundaries. Unsupported cases remain unsupported; they are never counted as learned no_entity. Each model wrongly rejects the valid quoted registration name in native-fresh-29. Full qualification required at least 90% negative rejection recall and zero valid rejections, so neither passes.

| Semantic negative family | Model 1701 rejected | Model 1702 rejected |
| --- | ---: | ---: |
| Merged API/value fragment |2/10|3/10|
| Clipped API path |3/10|5/10|
| Nested fragment |9/10|9/10|
| Broken quote boundary |6/10|8/10|
| Ordinary prose |6/6|6/6|

The remaining weakness is concentrated in merged API/value candidates and clipped paths. A broad 99.06% valid-role score must not hide these failures or the valid-name false rejection.

## Operational changes and preservation

The fresh 40 requests contain no baseline cross-role conflicts. Their original extraction results remain exactly unchanged: 38/40 and 39/40 wholly correct, accepted F1 98.59% and98.58%. This verifies preservation under the narrow resolver; it is not evidence of fresh conflict-resolution success. There are only 3 operational conflict groups for 1701 and 2 for 1702 across all 296 questions.

- **1701:** Correctly resolves roles-04's placeholder `'amber-pivot'` as value and va-f03-q04's quoted `'Material'` as registration_name. Both outputs change from invalid to wholly exact. No correct mentions are lost and no nonconflicting spans change. The partial overlap in cross-role-fresh-07-02 remains unresolved. This seed passes the narrow improvement gate.
- **1702:** Assigns value to the malformed combined span `props.label: 'entry[2]'` in srf-026, turning an invalid output into a structurally valid but wrong output. The span diagnostic's accepted F1 falls 94.06%→93.14%. It also assigns value to the actual quoted registration `'Material'` in va-f03-q04, removing the correct registration label. Both resolutions are wrong; the preservation gate fails.

The untrained attribute scorer was also unsafe: it already made an incorrect resolution on srf-026 for 1702. Training changes that choice from API to value without fixing the boundary problem. The trained candidate is judged against the original frozen extractor, not against this unsafe untrained intermediate.

Zero invalid outputs for 1702 after resolution does not mean success: the invalid-to-valid-but-wrong gate catches both errors. No threshold, schema, dataset or checkpoint was changed after fresh baseline exposure. No model was chosen because its result looked better.

## Verification and decision

Six unit tests pass. Both candidates perform 1164 training-example passes and 150 optimizer updates, with no frozen base parameters changed. Epoch 1 andepoch 6 saves reload with identical parameter hashes and native attribute predictions. All 522 run-input hashes remain unchanged. The protected audit passes 37,060 checks across accumulated manifests with zero changes, including A, v2, both baselines and the locked knowledge/data/DB layers. Counts are manifest checks, not a claim of 37,060 unique files.

**Do not adopt this paired candidate.** Retain the frozen extractors and the new adapters as experiment evidence. The native attribute training path is verified, and role learning is real; malformed-span rejection and cross-seed operational reliability remain inadequate. Any follow-up should target those specific failures with separately authored evaluation, not pick 1701 or tune on this exposed fresh set.

Independent review completed: the same fresh-context reviewer checked pretraining readiness, independently recomputed final results and preservation gates, and reconciled this report with raw evidence. The verdict is **Not ready for adoption; a completed credible negative experiment**. See [REVIEW.md](REVIEW.md).

## Evidence

- [Fixed protocol](PROTOCOL.md), [native compatibility](COMPATIBILITY.md), [independent review](REVIEW.md).
- [Decision and separate qualification gates](test-output/decision.json), [complete scores](test-output/scores.json), [operational changed/conflict ledger](test-output/ledger.json).
- [Supplied-span metrics](test-output/probe-scores.json), [all 312 paired probes](test-output/probe-ledger.json), [remaining probe failures](test-output/probe-failures.json).
- [Run-input freeze](test-output/run-freeze.json), [protected audit](test-output/protected-after.json).
- Training/reload receipts and raw before/after outputs are in `test-output/1701/` and `test-output/1702/`.

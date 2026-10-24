"""Materialize the complete paired supplied-span ledger and compact report."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent;OUT=HERE/'test-output'
def read(n):return json.loads((OUT/n).read_text())
ledger=[]
for n in (1701,1702):
 before=read(f'{n}/probes-before.json');after=read(f'{n}/probes-after.json')
 for b,a in zip(before,after):
  assert (b['question_id'],b['start'],b['end'])==(a['question_id'],a['start'],a['end'])
  pred=a['prediction'];chosen=None if pred['status']!='scored' or pred['confidence']<=.5 else pred['label']
  ledger.append(dict(seed=n,**{k:v for k,v in a.items() if k!='prediction'},before=b['prediction'],after=pred,selected=chosen,correct=chosen==a['expected_role']))
for name,data in [('probe-ledger.json',ledger),('probe-failures.json',[r for r in ledger if not r['correct']])]:
 with (OUT/name).open('x') as f:json.dump(data,f,indent=2)
text='''# Native GLiNER span-attribute training results

**Native span-role training works, but this paired candidate is not safe to adopt.** Both models learned substantially better role selection on supplied correct spans. Model1702 nevertheless lost a correct role in an operational conflict and legitimized a malformed span. The predeclared both-model improvement gate fails; full qualification fails for both. Neither frozen extractor is replaced, and no seed is selected after seeing results.

## What was actually trained

Two isolated copies of the frozen role_boundary_adaptation epoch6 adapters were continued for6 fixed epochs each:194 existing training questions,449 generated malformed span targets per pass,150 optimizer updates per model. GLiNER native qualified span queries supervise seven roles, including no_entity, alongside ordinary entity replay. No spaCy component, new classification head, document-level classifier, third-party source patch, or new knowledge data was used.

`InputExample` has no first-class attribute field. The POC lowers labels into the exact qualified native entity queries used by `entity_attributes`; the native boundary losses train those span scores, and native inference applies softmax. A pinned private native force-scoring routine is used to score supplied exact frozen-extractor spans. This is not a claim that public GLiNER exposes supplied-span classification or a documented dedicated attribute-training API. [Compatibility proof](COMPATIBILITY.md) includes qualified-query-only gradient evidence, occurrence sensitivity, all-role public/helper score parity, and actual save/reload checks.

Both original extractors were run with flat decoding on296 questions each:40 independent fresh requests plus256 exposed diagnostics. All256 prior raw outputs reproduced exactly for both models before training. Both candidate scorers were run before/after on the same frozen spans and on a separate156-probe fresh supplied-span audit. Gold/probe offsets never enter operational conflict resolution. The latter only removes a losing role on identical offsets; partial overlaps, no_entity, low confidence and unrepresentable boundaries retain the original raw output.

## Supplied-span role and rejection audit

These are predictions at supplied exact spans, not end-to-end extraction or answer accuracy.

| Metric | Model1701 | Model1702 |
| --- | ---: | ---: |
| Valid roles correct before → after |43/106 →105/106|56/106 →105/106|
| Valid role accuracy after |99.06%|99.06%|
| Valid spans incorrectly rejected |1/106|1/106|
| Negative probes learned-rejected before → after |0/50 →26/50|0/50 →31/50|
| Overall negative rejection recall |52.00%|62.00%|
| Representable semantic-negative rejection recall |26/46 =56.52%|31/46 =67.39%|
| Rejection precision |26/27 =96.30%|31/32 =96.88%|
| Unsupported mid-identifier probes |4/4|4/4|

Each50-negative denominator comprises40 malformed candidates,6 ordinary-prose candidates, and4 intentionally unrepresentable mid-identifier boundaries. Unsupported cases remain unsupported; they are never counted as learned no_entity. Each model wrongly rejects the valid quoted registration name in native-fresh-29. Full qualification required at least90% negative rejection recall and zero valid rejections, so neither passes.

| Semantic negative family | Model1701 rejected | Model1702 rejected |
| --- | ---: | ---: |
| Merged API/value fragment |2/10|3/10|
| Clipped API path |3/10|5/10|
| Nested fragment |9/10|9/10|
| Broken quote boundary |6/10|8/10|
| Ordinary prose |6/6|6/6|

The remaining weakness is concentrated in merged API/value candidates and clipped paths. A broad99.06% valid-role score must not hide these failures or the valid-name false rejection.

## Operational changes and preservation

The fresh40 requests contain no baseline cross-role conflicts. Their original extraction results remain exactly unchanged:38/40 and39/40 wholly correct, accepted F198.59% and98.58%. This verifies preservation under the narrow resolver; it is not evidence of fresh conflict-resolution success. There are only3 operational conflict groups for1701 and2 for1702 across all296 questions.

- **1701:** Correctly resolves roles-04's placeholder `'amber-pivot'` as value and va-f03-q04's quoted `'Material'` as registration_name. Both outputs change from invalid to wholly exact. No correct mentions are lost and no nonconflicting spans change. The partial overlap in cross-role-fresh-07-02 remains unresolved. This seed passes the narrow improvement gate.
- **1702:** Assigns value to the malformed combined span `props.label: 'entry[2]'` in srf-026, turning an invalid output into a structurally valid but wrong output. The span diagnostic's accepted F1 falls94.06%→93.14%. It also assigns value to the actual quoted registration `'Material'` in va-f03-q04, removing the correct registration label. Both resolutions are wrong; the preservation gate fails.

The untrained attribute scorer was also unsafe: it already made an incorrect resolution on srf-026 for1702. Training changes that choice from API to value without fixing the boundary problem. The trained candidate is judged against the original frozen extractor, not against this unsafe untrained intermediate.

Zero invalid outputs for1702 after resolution does not mean success: the invalid-to-valid-but-wrong gate catches both errors. No threshold, schema, dataset or checkpoint was changed after fresh baseline exposure. No model was chosen because its result looked better.

## Verification and decision

Six unit tests pass. Both candidates perform1164 training-example passes and150 optimizer updates, with no frozen base parameters changed. Epoch1 andepoch6 saves reload with identical parameter hashes and native attribute predictions. All522 run-input hashes remain unchanged. The protected audit passes37,060 checks across accumulated manifests with zero changes, including A, v2, both baselines and the locked knowledge/data/DB layers. Counts are manifest checks, not a claim of37,060 unique files.

**Do not adopt this paired candidate.** Retain the frozen extractors and the new adapters as experiment evidence. The native attribute training path is verified, and role learning is real; malformed-span rejection and cross-seed operational reliability remain inadequate. Any follow-up should target those specific failures with separately authored evaluation, not pick1701 or tune on this exposed fresh set.

Independent review: the same fresh-context reviewer checked pretraining readiness and is reconciling final artifacts in [REVIEW.md](REVIEW.md). Final review conclusions are recorded there; review does not override the failed gates.

## Evidence

- [Fixed protocol](PROTOCOL.md), [native compatibility](COMPATIBILITY.md), [independent review](REVIEW.md).
- [Decision and separate qualification gates](test-output/decision.json), [complete scores](test-output/scores.json), [operational changed/conflict ledger](test-output/ledger.json).
- [Supplied-span metrics](test-output/probe-scores.json), [all312 paired probes](test-output/probe-ledger.json), [remaining probe failures](test-output/probe-failures.json).
- [Run-input freeze](test-output/run-freeze.json), [protected audit](test-output/protected-after.json).
- Training/reload receipts and raw before/after outputs are in `test-output/1701/` and `test-output/1702/`.
'''
with (HERE/'RESULTS.md').open('x') as f:f.write(text)

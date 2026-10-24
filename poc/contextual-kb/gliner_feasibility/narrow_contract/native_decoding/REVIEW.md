# Independent review

Review instance: 1 of 3. Reviewer scope: native_decoding working-tree experiment on main at c3091328f49d53de6b41a49c4fe5aa8f1c45e516. The POC is untracked; unrelated repository changes are excluded. Only this review file is reviewer-owned.

## Preliminary review, before results and author explanation

Read POC AGENTS/STEERING, experiment protocol and tests before implementation. The neutral task assignment disclosed the intended experiment but no outcome or author rationale. Inspected run.py, comparison.py, test_comparison.py, reused train/data and pilot scorer, and installed GLiNER overlap/runtime/boundary sources. No inference performed; old sealed evaluation and DB were not inspected.

No blocking implementation finding identified. The native argument reaches inference metadata and boundary entity decoding; the resolver is invoked separately for each entity query/label. Flat means maximum-total-confidence disjoint spans within a role, not global cross-role exclusivity. Nested permits containment but rejects crossing spans. The protocol correctly makes this distinction.

Exact occurrence identity includes role, start, end and raw text. Correct losses are compared against raw baseline mentions, independently of accepted-envelope gains. The gate requires both seeds, zero losses, strictly fewer total invalid envelopes per seed, zero newly invalid cases and no accepted-F1 regression on either split. Five focused comparison tests pass.

The baseline check compares complete output objects, including confidence, after verifying question IDs/order, and rejects any inference errors. Checkpoint parameter hashes are checked against saved receipts and after inference. Existing final-freeze protects prior artifacts; the run manifest carries the pinned base and library-source hashes and adds the new implementation and adapters. End-of-run manifest verification is required before accepting results. Final scores, full delta enumeration, qualification conclusion and manifest integrity remain pending independent verification.

## Findings

No actionable implementation findings remain. This verdict covers the bounded comparison, not deployment or model qualification.

## Plan Review

The implementation follows the frozen comparison protocol: both latest epoch-8 adapters, two exposed 24-question splits, both native policies at threshold 0.5, alternating call order, unchanged exact-span scorer and whole-envelope rejection. All 192 result rows exist. All 96 nested outputs match prior outputs exactly, including confidence. The 137-entry run manifest and 70-entry prior final manifest independently validate without mismatches. Both weight-check receipts report checkpoint identity and unchanged parameters; code checks these against actual named-parameter hashes before and after inference. No model inference was repeated by the reviewer.

## Author-Claim Reconciliation

Author observations were received only after the preliminary review was recorded.

| Author claim | Independent evidence | Status |
| --- | --- | --- |
| Useful-without-loss gate passes | Recomputed all four summaries and decision from raw saved outputs and unchanged gold | Confirmed |
| No lost correct mentions or flat invalid envelopes | Recomputed all 96 case deltas and scores; exact equality with changes.json/scores.json | Confirmed |
| 13 false mentions removed | 1701 challenge 7, olddev 1; 1702 challenge 5, olddev 0; no new correct or false mentions | Confirmed |
| Challenge exact 17/24 and 19/24; olddev 24/24 for both | Full scorer recomputation | Confirmed |
| Nested replay exactly matches prior | Compared IDs and complete outputs on all four paired datasets | Confirmed |
| Parameters unchanged | Both saved checks true; source checks actual before/after hashes against training receipt | Confirmed by execution receipts; reviewer did not rerun inference |
| Native flat is per-label, not a global guarantee | runtime.py policy normalization/metadata forwarding and boundary/engine.py `_decode_content_entities` resolve candidates inside the per-name loop | Confirmed |

## Verification Performed

Ran `python3 -B -m unittest discover -s poc/contextual-kb/gliner_feasibility/narrow_contract/native_decoding -p 'test_*.py' -v`: 5 tests passed. A separate read-only Python check recomputed every score, family metric, per-case delta, overlap count, transition and gate input from raw output files; asserted exact equality with scores.json, changes.json and decision.json; verified prior nested outputs and both hash manifests. No sealed evaluation or DB access, source changes, dependency changes, training or inference occurred during review.

Flat challenge results (raw equals accepted because invalid count is zero):

| Seed | TP / FP / FN | Precision | Recall | F1 | Exact |
| --- | --- | --- | --- | --- | --- |
| 1701 | 116 / 4 / 3 | 96.67% | 97.48% | 97.07% | 17/24 |
| 1702 | 115 / 2 / 4 | 98.29% | 96.64% | 97.46% | 19/24 |

Both olddev results have 62 TP, zero FP/FN, and 24/24 exact. Invalid envelopes fall from 5 to 0 for seed 1701 and from 3 to 0 for seed 1702 across the two splits. There are no new invalid envelopes. Both within-role and cross-role overlap counts are zero after flat decoding on these outputs; source semantics do not guarantee the latter on other inputs.

Remaining challenge failures, with half-open offsets:

- Both seeds miss api_reference `hide` at 15:19 in repeat-03 and `key` at 118:121 in roles-03, plus value `'moss-compass'` at 123:137 in roles-07.
- Seed 1701 retains false value claims: claims-03 at 41:78 (`'a default always replaces the model'`), claims-05 at 167:207 (`'hidden fields always keep their values'`), claims-07 at 89:126 (`'a default always replaces the model'`), and claims-08 at 144:176 (`'wrappers choose the model path'`).
- Seed 1702 additionally misses value `'amber-pivot'` at 41:54 in roles-04 and wrongly labels `text` at 70:74 as a value; it retains the false value claim in claims-07 at 89:126.

Every nonempty role and overall P/R reaches 90%, but the quoted-value boundary diagnostic still misses 1/34 for seed 1701 and 2/34 for seed 1702. Compound API boundaries are 24/24 for both. The strict qualification requirement of no critical boundary misses is therefore not met.

## Open Questions And Residual Risks

This is exposed synthetic diagnostic evidence, not fresh held-out evaluation, real traffic qualification or answer accuracy. Semantic claim/value confusion and missed correct identifiers/quoted values remain. Native flat resolves overlaps within a role; future cross-role conflicts still require the unchanged contract rejection. Timing measures include first-call effects and should be described as this run's measurements rather than a qualified latency benchmark.

## Verdict

Ready: the bounded native-decoding experiment and its useful-without-loss conclusion are supported. Neither model is qualified under the separate strict boundary criterion.

## Recommended Next Actions

Report the benefit and remaining failures together, preserving all per-case deltas. Do not equate zero observed cross-role conflicts with global exclusivity or promote the exposed diagnostic pass to general qualification.

## Final results-document reconciliation (same review instance)

Read RESULTS.md after the completed independent review. Its quantitative and qualification claims agree with the verified artifacts. Explicit additional aggregation confirms accepted true positives 312→355 across 96 model/question cases while raw true positives remain 355; challenge exact counts 14→17 and 17→19; olddev exact counts 23→24 and 24→24. Reported timing totals round correctly from the saved per-call measurements. The report preserves the per-label limitation, the one/two quoted-value misses and failure of full qualification. Carrying flat into another experiment is presented as a proposed experimental next step, not an integration, production or adoption claim.

The separate protected-after receipt reports 36,576 hash checks with no changes. The reviewer inspected that receipt but did not independently traverse those protected trees; only the 137-entry run and 70-entry prior manifests were independently rehashed in this review. No discrepancy found; verdict remains Ready for the bounded experiment.

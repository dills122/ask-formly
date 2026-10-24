# Independent native-attribute review

Review instance: 1 of 3. Status: preliminary; full training and adoption are not approved by this document.

## Scope and independence

Explicit review boundary: new `native_attribute_training/` experiment. Repository is on `main`, HEAD `c3091328f49d53de6b41a49c4fe5aa8f1c45e516`, with substantial pre-existing dirty/untracked state. No whole-working-tree readiness claim is made. Reviewer owns this file only. Old sealed evaluation material and implementation-author rationale remain unread at this checkpoint. Applicable repository guidance, contextual-KB STEERING.md, and narrow CONTRACT.md were read.

## Preliminary findings ledger

Before implementation inspection, independently reviewed all 40 fresh questions and 106 gold mentions against the six-role contract, including maximal paths, opaque values, quoted names/keys/values, repeated occurrences, negation, and six empty questions. No semantic gold disagreement found. A separate Python JSON/slice check verified every gold raw value and all 152 initial candidate texts against exact question codepoint bounds.

The initial malformed set has 10 merged, 10 clipped API, 10 quote-error, 10 nested-fragment, and six ordinary-prose candidates. Requested additional mid-identifier clipping probes without replacing current candidates: inability to represent arbitrary supplied boundaries must be visible as unsupported transport, not scored as rejection or removed from evaluation.

Pre-full-training checks still required: native attribute targets reach attribute loss; positive/negative roles compete with explicit no_entity; exact supplied-span transport distinguishes unsupported boundaries; native attribute parameters receive gradients; saved/reloaded adapter predictions agree. The attribute-enabled inference API alone is insufficient evidence of trainability.

## Verdict

Unable to verify at this preliminary checkpoint: implementation and readiness evidence pending. Fresh semantic gold audit passes, subject to retaining additional unsupported-boundary probes and freezing final hashes/counts.

## Pre-full-training checkpoint

Verdict: **Ready for the bounded baseline replay and training experiment**, contingent on the implemented baseline hash/raw-output checks passing before optimization. This is not adoption or full qualification.

- Supplementary four mid-identifier probes independently checked; final fresh set has 40 questions, 106 gold occurrences, 40 core malformed candidates, six ordinary-prose negatives, and four unsupported-boundary probes (156 total supplied candidates). No semantic gold revisions were needed.
- Inspected `transport.py`, `native.py`, both smoke paths, `gradient_smoke.py`, `resolution.py`, imported occurrence policy, `run.py`, `assess.py`, and tests before an author explanation. PROTOCOL.md was read as the acceptance/configuration contract and includes author mechanism claims; those were verified against code and installed upstream source rather than treated as evidence by themselves.
- Installed `Schema.entity_attributes` lowers qualified labels to entity queries; boundary engine `_attach_entity_attributes` uses `score_explicit_spans` and softmax. There is no separate native attribute cross-entropy training head. The implementation teaches qualified attribute queries through native boundary supervision; the protocol accurately states this distinction.
- Both seeds' 194-row transport receipts retain exact positive/negative coordinates. The seven-query-only target-permutation check excludes ordinary extraction queries and demonstrates loss/gradient sensitivity when registration/no_entity targets are swapped. Ordered smoke observes nonzero gradients, 202 changed parameters, changed attribute scores, and exact saved/reloaded weights and scores. Extended parity covers 57 retained public mentions across all six roles for each seed and repeated equal text at distinct coordinates.
- Requested training/inference qualified-label ordering alignment; author corrected transport to sorted native schema order and retained a superseding ordered smoke. Requested missing value-role parity; complete receipt now covers it. These were readiness corrections within this review instance before full training.
- Resolver only removes losing roles from identical-span cross-role conflicts; nonconflicting spans, partial overlaps, low-confidence, unsupported coordinates, and no_entity predictions retain raw output. Supplied gold/probe coordinates never enter production resolution.
- `run.py` starts from original frozen adapters, enforces original weight hashes and prior diagnostic prediction parity, trains only the existing 194 rows plus derived negatives, and checks save/reload at epochs 1 and 6. It freezes code and source inputs and keeps role scorer training separate from frozen candidate extraction.

Verification run independently: `python3 -B -m unittest discover -s poc/contextual-kb/gliner_feasibility/narrow_contract/native_attribute_training -p 'test_*.py'`: six tests passed. Independently checked fresh/probe exact slices and inspected upstream schema/scorer source. Model smoke receipts were inspected, not rerun by the reviewer; their scripts were reviewed.

Remaining reporting action: make diagnostic improvement and full qualification separate machine-readable verdicts. Full qualification additionally requires zero wrong resolutions, at least 90% malformed rejection recall, and zero valid spans rejected for both seeds. Results and every changed occurrence remain pending independent audit.

## Frozen baseline audit

Independently recomputed all 522 `run-freeze.json` hashes: no mismatch. Inspected all 296 before-role operational records per seed and confirmed score coordinates equal exactly each frozen extractor's emitted coordinates. The supplied-span audit remains separate.

Before training, supplied valid-role accuracy is 43/106 (seed 1701) and 56/106 (1702), versus positive-role acceptance of 47/106 and 75/106. Seed 1701 explicitly misrejects two valid supplied spans; neither seed rejects any of the 50 negative candidates. Each reports the four mid-identifier probes as unsupported. Thus API compatibility alone demonstrably does not establish useful role attribution or rejection.

The untrained role resolver changes one diagnostic question per seed. Seed 1701 selects registration_name for the exact quoted Material occurrence in `va-f03-q04`; seed 1702 selects api_reference for merged `props.label: 'entry[2]'` in `srf-026`. The latter is a malformed maximal-occurrence boundary; removing its conflicting value role is not semantic correction. Final reporting must preserve this before-arm harm even if training avoids it. Original frozen extractors remain the safety-gate comparator.

## Final findings

**P1 — Candidate 1702 violates the preservation gate.** In `test-output/1702/vocab-after.json`, case `va-f03-q04`, the resolver chooses value (confidence 0.978265) for the explicit registered name `'Material'` at 58:68 and removes the correct registration_name. In `span-after.json`, `srf-026`, it chooses value (0.747755) for the merged span `props.label: 'entry[2]'` at 53:76, which should instead be two separate mentions. Both outputs become structurally valid but semantically wrong. These are observed candidate failures, not an implementation/reporting defect: the frozen gate correctly rejects them. Smallest safe action: retain original extractors and do not activate either trained candidate; do not select seed 1701 retrospectively.

**P2 — Learned rejection remains inadequate and falsely rejects a valid name.** Both candidates reject the valid registration `'lagoon-input'` in `native-fresh-29` at 48:62 (confidences 0.835277 and 0.537406). Learned rejection reaches only 26/50 and 31/50 negatives; even excluding the four explicitly unsupported coordinates, it reaches only 26/46 and 31/46. The predeclared rejection and valid-retention requirements fail. Smallest safe action: preserve these failures and qualification=false; any new training/evaluation requires a separately bounded follow-up, not tuning this exposed set.

No additional actionable code or reporting defect remains within the completed experiment. The failed candidate is documented candidly.

## Plan review

The planned experiment was completed within the permitted boundary: native attribute-training mechanism verified before full training; original 194 training questions plus derived malformed candidates only; fresh gold independently audited before inference; both seeds trained with fixed settings; original extractors retained as candidate providers and gate comparator; operational and supplied-span tests kept separate; no threshold or seed selection after seeing results. No heavy architectural pivot or additional review instance occurred.

Both full runs have exactly 1164 finite loss records, each authorized training identity once per epoch across six epochs, and 150 updates. Initial parameter hashes equal the corresponding original checkpoint. Each changes 202 trainable parameters with zero frozen parameter changes. Epoch 1 and 6 score snapshots are exactly equal before/after reload for both models; receipts also report exact parameter equality.

## Author-claim reconciliation

| Final author claim | Evidence inspected | Status and consequence |
| --- | --- | --- |
| Native qualified attribute training receives signal | Installed lowering/scorer source; qualified-only target permutation; ordered update/save smoke | Confirmed. Boundary supervision trains attribute query scores; no dedicated attribute cross-entropy API is claimed. |
| Both candidates reach 105/106 valid supplied roles | Independently recounted both 156-record after-probe files | Confirmed; each remaining error is a learned rejection of a valid name. This is not operational accuracy. |
| Rejection precision is 26/27 and 31/32, with recall 26/50 and 31/50 | Independent role/threshold/unsupported recount | Confirmed. Representable-negative recall is separately 56.52% and 67.39%. |
| Operational preservation fails for 1702 | Independent comparison of all 592 baseline/after records, source gold, and four changed outputs | Confirmed: one correct mention lost, two invalid-to-valid-wrong outputs, zero nonconflicting changes. 1701 has two correct resolutions and no lost correct mentions. |
| Fresh extraction is unchanged | All fresh raw/after records and scores | Confirmed: 38/40 and 39/40 exact. Fresh inputs have no operational conflict, so this is preservation evidence only. |
| Paired improvement and full qualification fail | Recomputed operational cases and supplied metrics; `decision.json` | Confirmed. No promotion or best-seed selection is justified. |
| Protected material is unchanged | Reviewed protected hash-check implementation and 16-manifest receipt; independently recomputed all 522 run hashes | Receipt confirms 37,060 checks with no change. The 37,060 protected checks were not independently rerun; they are not 37,060 unique files. |

`RESULTS.md` and `COMPATIBILITY.md` were read after implementation and outcome inspection. Their claims match the evidence and preserve the private-API, unsupported-span, before-arm harm, and low operational-conflict-count limitations.

## Verification performed

- Independent exact-slice/semantic audit of all 40 fresh cases and 156 final probes before implementation outcomes.
- Independent six-test unittest run; installed upstream lowering and explicit-span scoring source inspection.
- Independently checked 522 frozen input/source hashes before and after training: zero mismatch.
- Checked every before-role operational input against original frozen candidate coordinates, all 296 per seed.
- Recomputed split scoring and inspected every changed output against source gold, including both harmful 1702 changes. Independently checked all 592 final outputs for lost correct mentions, nonconflicting deletions, and invalid-to-valid-wrong outcomes.
- Independently recounted supplied probes before/after, including unsupported statuses, family rejection counts and the exact false rejection.
- Checked both complete training loss logs/identity coverage, original parameter hashes, training receipts, and epoch 1/6 reload output equality.

The model training and native smoke executions were performed by the worker; their code and retained evidence were reviewed. No old sealed evaluation content was inspected. No root indexing/package or Angular behavior change is claimed, so broad repository/Angular checks were not run for this isolated experiment.

## Open questions and residual risks

Native supplied scoring depends on a pinned private API and cannot represent the four mid-identifier boundaries. Training's native binary span objective and inference's softmax normalization are different mechanisms. The five diagnostic conflict groups are too few for broad resolution claims; fresh40 contributes supplied-role/rejection evidence but no fresh operational conflicts. High supplied valid-role accuracy does not establish safe malformed rejection or complete extraction.

## Final verdict

**Not ready for adoption.** The experiment is complete and its negative conclusion is supported. Native role-query training is real, but the paired improvement gate fails and neither candidate meets full qualification. This final verdict supersedes the earlier readiness-to-run checkpoint; it does not invalidate the compatibility proof.

## Recommended next actions

Retain both frozen extractors, all raw results, and both new adapters as evidence. Report paired failure without selecting the better seed. Any further attempt needs an explicitly bounded follow-up with independently authored evaluation targeting malformed-span rejection and cross-seed preservation. Do not implement a new architecture or start another review instance as part of this completed review.

Review instance: 1 of 3, completed in the same reviewer context through readiness and final outcomes.

# Independent pilot review

Review instance: 3 of 3. Scope: `adaptation/pilot/`, excluding caches, at repository HEAD `c3091328f49d53de6b41a49c4fe5aa8f1c45e516`. The repository has extensive pre-existing dirty/untracked files; this is a directory-bounded review, not approval of that worktree. Reviewer did not inherit the implementation discussion. Bootstrap, instructions, design, tests, implementation, labels and evidence were inspected before AUTHOR-EXPLANATION.md and FINDINGS.md. No training, prediction, implementation edits or sealed/knowledge/DB content inspection occurred. Protected files were read only as bytes for hashes.

## Preliminary findings

Recorded to the initiating agent before reading the author explanation: 17 tests reproduced 16 passes and one same-anchor failure. Installed natural-mode instance formation creates one instance per anchor candidate; P04 requires two records at the same occurrence. Corrected record-field preprocessing passes, but does not establish training compatibility. Agreement and hash recomputation were still pending at this preliminary checkpoint.

## Findings

**P1 — Proposed natural-mode identity blocks full training.** `test_native_contract.py:60–65` demonstrates that two requests about the same exact target produce one record even with perfect supplied assignment scores. The distinct-anchor control passes. Installed `gliner2/models/boundary/records.py:715–725` sets instance count from anchor candidate count and seeds each instance from one anchor. P04 legitimately retains two requested operations on `the wrapper`; exporter `contract.py:56–57` preserves both gold records and declares that target as the natural anchor. This is a representational limitation, not a failure to train enough. Smallest credible correction is an explicitly approved record-identity design revision followed by compatibility checks on the unchanged difficult pilot cases. Do not merge gold requests or claim an alternative mode is qualified without testing it.

No additional actionable defect blocks accepting the bounded pilot report. The known limitation is correctly surfaced as a failed acceptance requirement rather than hidden as a skip or passing test.

## Plan review

The 24-question annotation stage and initial transport/representation checks are supported. Initial agreement missed the specified gate; retained clarification and re-annotation evidence follows the planned remedy. The shared P20 annotation mistake shows why agreement alone cannot establish semantic correctness; its separately frozen correction is appropriate.

The compatibility stage remains incomplete by design: no joint-loss/backward, per-task gradient, resource-training budget, adapter/head inventory or save/reload parity validation was executed. Stopping when the representation fails is faithful to the explicit design checkpoint. Full dataset creation, training and evaluation are not approved by this review. The original later implementation/evaluation review gate cannot silently reuse or reset this exhausted review budget.

## Author-claim reconciliation

| Claim | Evidence | Assessment |
| --- | --- | --- |
| Raw agreement improves from .801603 to .981053; counts/status agree throughout | Recomputed both reports from retained raw annotation files; exact equality to saved reports | Confirmed numerically; independent annotation process is reported provenance, not independently reconstructable from labels alone |
| All 24 native examples round-trip and corrected record fields preprocess exactly | Re-executed native and local-model preprocessing tests | Confirmed for tested transport paths; not entity/relation target-graph or loss coverage |
| Same-anchor incompatibility is structural | Real RecordHead oracle test, positive control and installed source | Confirmed |
| Encoder LoRA does not automatically train all task heads | Installed trainer.py:858–882 freezes all parameters before selected adapter injection | Confirmed source behavior; actual proposed adaptation configuration remains untested |
| Protected files remain unchanged | Recomputed all 90 protected hashes | Confirmed against supplied manifest, not proof that no historical read occurred |
| Pilot is not training or model-quality success | Scope and executed checks contain no optimization/prediction path | Report is appropriately limited |

## Verification performed

From pilot directory, with `PILOT_WRITE_EVIDENCE` unset:

`PYTHONDONTWRITEBYTECODE=1 ../../env/.venv/bin/python -m unittest test_contract test_analysis test_native_contract test_preprocessing`

Result: 17 tests, 16 pass, one failure in `test_same_exact_target_must_support_two_different_requests`, exit code 1. All 24 record-preprocessing subcases pass. Loader/deprecation warnings remain visible. No evidence rewrite requested.

Recomputed six code-freeze-v2 hashes, nine annotation-freeze-v2 hashes and 90 protected-before hashes: zero mismatches. Recomputed both agreement objects: exact matches. Inspected retained initial red logs, native acceptance evidence, current gold and correction history. Checked installed natural record formation and LoRA setup source.

## Open questions and residual risks

Agent agreement is not human-reviewed gold or general annotation reliability. Source-order attachment matching is suitable for this aligned pilot, not an arbitrary output scorer. Substring validation cannot reject every semantically wrong occurrence. Passing request-record preprocessing does not verify entity/relation graphs or negative relation supervision. The Python audit hook is defense in depth, not OS isolation. No model accuracy, latency, learning, downstream retrieval or answer-quality conclusion follows.

## Verdict

**Not ready for full training.** Accept the bounded pilot findings and the decision to stop. No further correction is required to make that negative result honest or reproducible; the blocking issue is the proposed representation itself.

## Decision gate and next actions

Human approval is required for a targeted revision of native aspect identity and a renewed compatibility-only phase. Candidate designs may explore an aspect-specific anchor or latent/anchorless records, while preserving same-anchor, shared-action, repeated-occurrence, nested-span and exact-pairing gold requirements. These are candidates, not verified remedies. Negative relation supervision and eventual joint-loss/head/save-reload checks must remain explicit acceptance requirements.

Proceeding directly to bulk annotation/training risks spending effort on an incapable output contract. Ending here preserves a valid negative feasibility result but leaves adaptation unresolved. Exact approval needed: authorize the record-identity design revision and bounded compatibility work, and specify a revised review allowance before any further implementation/evaluation gate. Review instance 3 of 3 is exhausted; no new reviewer or workstream has been created.

# Independent review

Review instance: 1 of 3

Scope: new `cross_role_resolution/` only; branch main at c3091328f49d53de6b41a49c4fe5aa8f1c45e516 with broad pre-existing dirty state excluded. No sealed evaluation was read. Reviewer owns this report only.

## Preliminary ledger — before implementation or author rationale

Read POC AGENTS/STEERING, narrow CONTRACT and TEST-PLAN. Reviewed all 40 fresh questions and gold mentions before implementation or author notes. Independent mechanical offset audit: 40 questions, 100 mentions, six empty questions, no raw/offset mismatch. Roles: api_reference 32, value 27, registration_name 16, model_key 11, ui_adapter 9, version 5. No annotation correction identified. Version conclusions have a particularly small denominator. Fresh questions do not include quoted instruction text, so a deterministic instruction-as-data test remains necessary. Opaque expressions deliberately contain nested apparent APIs and role names; partial-overlap failures must remain visible.

The bootstrap disclosed the intended native classification versus confidence control before this pass; this is not a fully blind design assessment. Gold and implementation remained unseen until the respective passes. No author rationale has yet been read.

Review conditions: conflict elimination alone is insufficient; correct-role preservation must be measured. Check full label vectors, reversed order sensitivity, unique confidence winner, same-occurrence identity, partial overlaps, malformed/nonfinite predictions, raw-invalid retention, no-mention denominators, per-model/per-role gains/losses, and unchanged A/v2/data/DB boundaries.

## Verdict

Unable to verify — implementation and executed comparison are pending.

## Precomparison review checkpoint

Inspected PROTOCOL.md, resolve.py, test_resolve.py, run.py, existing pilot scorer/validator and narrowly imported supervised loader helpers. Then read AUTHOR-NOTES.md, which is the independent gold author's provenance statement, not implementation rationale. The observed gold matches its 40/eight-family/six-empty claims; historical non-exposure is author testimony rather than mechanically provable.

Initial bounded findings sent to worker: marker-tag collision ambiguity; classifier/extractor exception preservation; malformed raw handling; checking nonconflicting records inside conflicting questions; true fresh-family attribution; classifier-inclusive latency; explicit qualification output; and failure-sensitive gate tests. First four fixes inspected. No heavy architectural pivot required.

Executed `python3 -B -m unittest discover -s poc/contextual-kb/gliner_feasibility/narrow_contract/cross_role_resolution -p 'test_*.py'`: 12 tests passed at this checkpoint. Inspected retained RED logs showing missing resolver/consensus functions and GREEN evidence. Inspected smoke log for seeds 1701/1702: both native classifier paths returned registration_name with confidence about .985/.990 on the disposable synthetic smoke input. This proves API compatibility only, not fresh accuracy. Review remains pending final harness changes and executed comparison.

Precomparison follow-up: verified raw-confidence validation, marker-collision abstention, arbitrary classifier-exception retention, baseline exception records, same-question nonconflicting-span preservation check, explicit separate latency/qualification outputs, and gate tests. Caught and corrected fresh-family list/dictionary mismatch and persistence-after-parity ordering before inference. Final independently executed discovery suite: 14 tests passed. Native fresh-family map test reads the real 40-ID/eight-family fixture. Readiness cleared for bounded frozen two-seed comparison; this is not approval to adopt the candidate. Opaque-expression qualification remains explicit manual review, and copied extraction seconds must not be presented as full contextual latency.

# Final review

Review instance: 1 of 3

## Findings

No remaining actionable implementation defect was identified in the bounded experiment after the precomparison corrections. The requested behavioral fix is not achieved: `test-output/decision.json` rejects both seeds because neither resolves a conflict correctly. Every contextual output equals its baseline. This is a valid negative experiment, not readiness evidence.

The confidence control cannot substitute: seed 1702 `va-f03-q04` removes the correct registration_name occurrence `'Material'` at [58,68) and keeps the wrong value role. Invalid-output count improves while semantic correctness regresses. The retained control ledger and score recomputation establish this directly.

## Plan Review

The scope remained an isolated question-layer experiment with fixed adapters, flat extraction, threshold .5, unchanged labels, independent 40-case gold and 176 exposed diagnostic cases per model. Same-boundary conflicts alone enter classification. Full-vector/native single-label agreement and reversed role order protect against the tested selection mistakes; abstention preserves all unresolved outputs in scoring. Partial/nested overlap remains unsupported explicitly. The candidate correctly fails its predefined preservation-plus-repair gate; no inference-time tuning was applied after exposure.

Precomparison hardening corrections stayed within the intended architecture. They did not require another design or review instance. A future occurrence-supervision or span-attribute design is a proposal outside this completed review, not an approved implementation or proven remedy.

## Author-Claim Reconciliation

| Claim | Inspected evidence | Status and consequence |
| --- | --- | --- |
| Fresh gold has 40 questions, eight families, six empty cases | fresh.json, families.json, independent source-offset audit | Confirmed; 100 exact-source mentions across all six roles. |
| Candidate changes zero outputs and loses zero prior correct spans | All 432 baseline/contextual records, independent scorer recomputation | Confirmed; preservation is achieved through abstention, not repair. |
| Fresh exact is 37/40 and 40/40, with one/zero invalid envelopes | Independently recomputed scores for both models | Confirmed; limited synthetic extraction evidence. |
| Confidence arbitration is unsafe | Seed 1702 vocabulary control and gold | Confirmed; correct Material registration lost. |
| Three eligible conflicts trigger 12 native calls; partial overlap abstains | Per-model audit/call records | Confirmed by review of conflict records and retained calls. |
| Frozen inputs stay unchanged | Recomputed all run-freeze file hashes | Confirmed; no mismatch. Broader protected A/v2/data/DB audit belongs to parent. |
| Existing training lacks marked-occurrence classification supervision | Narrowly inspected existing train.prepare; author's installed-library source diagnosis in RESULTS | Entity-only transport is consistent with inspected code. Detailed library-loss causality was not independently re-audited and is not needed for the rejection verdict. |
| New supervision or span attributes may help | Proposal only | Unverified; no success inference authorized. |

## Verification Performed

- Independently executed discovery unittest suite after fixes: 14/14 passed.
- Inspected retained initial, consensus, hardening and family RED/GREEN evidence. One weak passing confidence RED attempt is retained honestly; a stronger failure-specific RED preceded its GREEN.
- Independently recomputed raw/accepted per-role metrics, exact/invalid counts, boundary diagnostics and empty/nonempty categories for all 36 model/split/arm combinations with the frozen scorer; all match saved scores.
- Compared all 432 baseline/contextual records directly; identical.
- Recomputed every run-freeze SHA-256; zero mismatches.
- Inspected both compatibility smoke outputs and final integrity receipts.
- Manually checked fresh opaque-expression family: seed 1701 exact 4/5, seed 1702 exact 5/5. `cross-role-fresh-07-02` retains an invalid model_key fragment inside the full object value for seed 1701. This check supplements the intentionally unmodified qualification JSON's pending-manual marker; it does not establish comprehensive opaque qualification across all historical sets.

## Open Questions And Residual Risks

Classification on marked occurrences was never supervised by the entity-only trial, and semantic target selection is not guaranteed by document classification. Scores are uncalibrated. Reversal agreement tests two label orders, not all permutations. Most fresh questions produced no conflict, so fresh exact accuracy mainly measures the unchanged extractor. Five version mentions and six empty cases are small denominators. Marker and instruction-data unit tests prove representation behavior, not model immunity to arbitrary question instructions.

Timing in RESULTS correctly excludes model loading and Python validation/resolution overhead; `latency.json` totals are sums of model call durations, not end-to-end latency. Qualification remains failed on the diagnostic suite. Full protected-artifact audit is separately performed by the parent; this review checked its own writes were confined to REVIEW.md and compared the runner's frozen inputs.

## Verdict

**Not ready** for adoption as the requested cross-role fix. The bounded experiment and its negative result are reviewable and supported by reproduced evidence. Prior learned gains are preserved, but neither model receives a correct contextual conflict repair. No further independent review instance or architectural pivot was started.

## Recommended Next Actions

Retain this result and the unchanged checkpoints. Report explicitly that the fix remains unresolved. If continued development is authorized, freeze a new bounded occurrence-aligned supervision/attribute design with its own acceptance tests and independent data before training; do not quietly lower this experiment's threshold or use confidence arbitration as a fallback.

Final reconciliation addendum: inspected the parent's `test-output/protected-after.json`: 36,802 manifest entries checked and no changes reported across protected A/v2/earlier experiments/data evidence. Independently inspected installed native boundary candidate loss, classification activation/loss paths and pinned config: candidate hard-negative machinery exists, configured counts are 20/16, and native softmax/sigmoid behavior agrees with RESULTS. This supports its bounded architecture description; it still does not prove a unique causal defect or future remedy. RESULTS accurately rejects the candidate, distinguishes extraction from answer quality, states unchanged outputs and all failed gates, and limits latency claims. Final verdict remains Not ready for adoption; review instance 1/3 is closed.

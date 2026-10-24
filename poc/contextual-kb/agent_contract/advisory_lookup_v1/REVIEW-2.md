# Independent integration review

Review instance: 2 of 3. Verdict: **Not ready**.

## Findings

### P2 — Keep confirmed integrity failures distinct from unavailable verification
`cli.py:43–48` catches every exception from `verify_unchanged`, converts it to `parameters_unchanged:null`, and returns normally. This includes `transport.py:59` reporting that the observed before/after parameter maps differ. A real JSON subprocess reproduction returned eight candidates, status degraded, and unknown integrity despite `before={'w':'before'}` and `after={'w':'after'}`. See `test-output/review2-integrity-reproduction.json` and its retained reproduction script. Cleanup succeeds, but the frozen-model boundary has lost its hard failure and machine-readable known-false distinction. Original review R1 explicitly required retaining hard errors for observed integrity mismatch.

The worker also serializes verification exceptions as generic error text, so merely rethrowing local ValueError is insufficient: distinguish integrity errors across worker startup/verify transport and CLI, while retaining fail-open behavior for ordinary worker unavailability. Add regressions for both remote and locally detected mismatch. No actual frozen model corruption was observed; this is a reproducible exception-classification defect, not a claim that retained artifacts changed.

Original P1's unavailable-worker output loss is corrected, and original P2's harness cleanup defect is corrected. The remaining issue is a bounded correction, not an architectural pivot.

## Plan Review

The implementation preserves the intended architecture: caller-produced foundation plan, advisory extraction, and unchanged full-question retrieval. The lookup passes only search_requests to retrieve with enhanced=False, keeping hints out of query expansion and ranking. Tests cover invalid input before work, empty plans, advisory load/inference/malformed-output failures, retrieval failure propagation, and copied facts. The harness context manager registers its worker before evidence persistence and closes it in finally across body, persistence, and verification failures.

The two-environment subprocess approach fits the existing immutable environments; failed-environment evidence and successful native evidence remain separately retained. No model/config/selection changes or reruns are needed for the integrity correction. Task-plan checkboxes remain pending and should reflect final acceptance only after the last review. Scope was verified as new advisory_lookup_v1 on dirty main HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516; unrelated working-tree changes were excluded.

## Author-Claim Reconciliation

| Claim | Evidence inspected | Status and consequence |
| --- | --- | --- |
| Unavailable final verification preserves retrieved candidates | CLI source, composition tests, real-DB injected-worker artifact | Confirmed |
| Failed verification is explicitly unknown | Source and real subprocess mismatch reproduction | Correct only for unavailable verification; confirmed mismatch is known false, finding above |
| Harness closes workers on exceptional exits | model_session source and body-failure regression | Confirmed |
| Both frozen models preserve full-question retrieval | All 144 retained packets, 70 extractions per seed | Confirmed |
| Final default CLI works after fix | cli-final-native.json and final-cli-freeze | Confirmed: two hints, eight candidates, integrity true |
| Model/DB/prior evidence preserved | Nine freeze audits, 48 prior chains, per-parameter maps and DB hash | Confirmed |
| Functional parity proves accuracy or production qualification | Author explicitly disclaims this | Correctly bounded; no such qualification established |

Preliminary findings were saved before REVIEW-FIXES.md and AUTHOR-EXPLANATION.md. Bootstrap claims of successful tests/evidence were already visible, but no author rationale was read before the source pass. RESULTS.md was absent when checked.

## Verification Performed

- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/advisory_lookup_v1 -p 'test_*.py'`: 23 tests passed; output retained in test-output/review2-tests.txt.
- `python3 -B poc/contextual-kb/agent_contract/advisory_lookup_v1/test-output/review2-integrity-reproduce.py`: real JSON worker plus mocked index reproduces normal CLI return after confirmed hash mismatch; subprocess closed. No native model or real retrieval run.
- `python3 -B poc/contextual-kb/agent_contract/advisory_lookup_v1/test-output/review2-audit.py`: offline raw-evidence audit passes. Initial audit attempt encountered relative manifest paths; corrected reviewer script resolves them against their owning directories. This was an audit-tool error, not an implementation failure.
- 48 prior chains match protected-before counts and all bound bytes; sealed files were hashed only. Nine integration freezes validate, using the documented archived source copies for original run and run-ready.
- Independently checked exact input question plans, projected query text/order/count, query logs, final IDs and complete fact records for 48 foundation packets and 48 per seed. Each seed has 70 retained extractions. Hint anchoring/advisory flags validate: seed1701 has 73 hints/38 API hints; seed1702 has 71 hints/39 API hints. This does not assess semantic correctness.
- All 564 before/after parameter hashes per seed equal original training receipts. Current DB hash equals native setup. Final native and injected-failure CLI candidates/facts match; only native success claims unchanged model parameters.
- Graph coverage checks report inspected POC sources not tracked in October16 generation; direct source fallback used, no reindex or graph-completeness claims.

The initiating agent subsequently reported adding a separate intentionally RED test_integrity_boundary.py and integrity-red.txt after this review's 23-test execution. These are remediation inputs outside the final-code manifest reviewed here; I have not executed or approved them. They do not change the recorded 23-test result or resolve this finding.

## Open Questions And Residual Risks

No native inference or retrieval was rerun. Evidence validates functional parity and immutability for retained cases, not annotation accuracy, answer quality, reliable abstention, universal compatibility, or production readiness. Foundation generation revision remains unpinned. Ordinary model unavailability must remain degradable while immutable-model integrity breaches remain hard failures.

## Verdict

**Not ready for final functional-integration acceptance** until the confirmed-integrity boundary is corrected. Happy-path and ordinary degraded retrieval integration are verified; harness lifecycle correction is sound. Annotation accuracy and production qualification remain separate and unestablished.

## Recommended Next Actions

Preserve this reviewed source and evidence, implement the bounded typed-integrity correction with failure-sensitive tests, and use review instance 3 of 3 for that final change. Do not rerun or replace the full native panel. No further review instances beyond the configured maximum and no architectural expansion are authorized by this review.

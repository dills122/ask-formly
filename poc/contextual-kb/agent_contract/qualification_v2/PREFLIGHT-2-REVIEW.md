# Independent preflight review

Review instance: 2 of 3

## Findings

No actionable blocking or non-blocking defects found in the reviewed implementation. Ready for freezing and generation, subject to completing the already-required freeze before any response. This is not a verdict on semantic qualification, promotion or production readiness.

The explicit review boundary is qualification_v2 on dirty main at c3091328f49d53de6b41a49c4fe5aa8f1c45e516. Broader repository changes were excluded. PREFLIGHT-2-PRELIMINARY.md was saved before AUTHOR-EXPLANATION.md was read. The initiating assignment disclosed the earlier execution/accounting finding, but did not supply the author's detailed explanation. Graph coverage returned not_tracked for all seven reviewed Python files, so implementation conclusions use direct complete source inspection. No implementation or input files were edited; only this review, its preliminary record and preflight2-* logs were written.

## Plan Review

The fixed plan is coherent: source/rubric preparation precedes freeze; 48 fresh sources in six groups and five prior diagnostics yield 159 unique scheduled slots, each source repeated three times. Seven packets contain the exact new contract, matching source requests and scheduled order. Parent case-review records prospective corrections and preserves optional shared-context allowances. Condition excerpts and aspect references resolve for every rubric item. The new contract is byte-for-byte qualification1 CONTRACT plus LEDGER-ADDITION, retaining POLICY. Timing/stage, supplied methods and explicit no-substitution limits are ordinary conditions with local reach; the addition expressly forbids inventing conditions for bare targets or absent context.

Execution now has an appropriate division of responsibilities: runner only parses/serializes data; execute reserves a new attempt directory and captures first-save hashes, logs and completion; load_attempt verifies identity and byte integrity before account checks the entire envelope. Wrong count/order/IDs, malformed or missing records and duplicate JSON keys fail all scheduled slots without salvage. Semantically invalid objects survive valid envelopes for after-save scoring. The attempt directory remains reserved after parse failure, preventing the ordinary same-attempt retry path. All 159 slots must use execute followed by load_attempt, as specified by PROTOCOL and the initiating commitment, rather than bypassing receipt checks through a scorer.

The final independent full-results review is instance 3 of 3. It must examine all 159 semantic rows and 53 stability units, the preserved first artifacts, integrity evidence and fixed-gate aggregation. No tuning or replacement generation after an unfavorable result is allowed. Freezing, generation and that final review are outstanding planned work, not preflight failures.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status | Review consequence |
| --- | --- | --- | --- |
| Fixed transport removes producer execution/import fragility | runner.deliver, six runner tests, absolute-path subprocess probes | Confirmed | literal_eval rejects executable expressions; no generated imports run |
| Original response and failed attempts remain intact | exclusive file and attempt creation, first-save/completion records, tests and duplicate CLI probe | Confirmed within the specified local procedure | no automatic retries or overwrites; external freezes still required |
| Whole packet and integrity failures cannot be salvaged | execution.account/load_attempt, six execution tests and targeted corruption probes | Confirmed | every scheduled output becomes None on checked envelope/integrity failure |
| Semantic defects are not repaired or filtered before save | runner tests and candidate regression tests | Confirmed | structural transport evidence is separate from semantic grading |
| Contract only adds a missing-condition audit | exact concatenation comparison; full CONTRACT/POLICY/addition review | Confirmed | existing interpretation rules preserved |
| Fresh schedule and source/rubric preparation complete | schedule, all 48 source requests, seven packet comparisons, case-review and all rubric span/reference checks | Confirmed for preflight scope | no output-derived rubric changes observed |
| Earlier evidence remains untouched | preserve.snapshot comparison before and after tests | Confirmed | protected manifests match; sealed material only hashed |
| New prompt improves semantic reliability | no outputs exist | Unverified by design | must be established by fixed qualification, not inferred from passing unit tests |

## Verification Performed

- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/qualification_v2 -p 'test_*.py' -v`: 20 passed; log test-output/preflight2-v2-tests.txt.
- Equivalent discovery in qualification_v1: 8 passed; log test-output/preflight2-v1-tests.txt.
- `python3 -B poc/contextual-kb/agent_contract/v3_stress/test_assess.py`: 8 passed; log test-output/preflight2-scorer-tests.txt.
- Actual absolute execution.py CLI invoked in an unrelated temporary directory: success, exact parsed literal/raw object equivalence, original literal bytes unchanged, semantic defect preserved, duplicate invocation rejected with all attempt artifacts unchanged.
- Temporary corruption probes: unsuccessful returncode, changed source-before/source-after/output hash, packet-byte change, runner receipt hash mismatch, and missing completion/output each invalidate the complete packet. No protected file was mutated.
- Schedule/input probes: 53 source identities, 159 unique source/run slots, three repeats each, packet ordering and exact request/contract agreement; every rubric excerpt exists in its source and every condition aspect reference resolves.
- preserve.snapshot matches protected-before.json before and after checks; reviewed scope hashes also remain unchanged. Logs: preflight2-protected-check.json, preflight2-scope.json, preflight2-probes.txt.

An initial reviewer probe failed because its expected contract concatenation inserted one extra blank line. A diff showed only that separator; the corrected exact concatenation passed. This was a reviewer-check error, not an implementation defect, and is retained in the probe log.

## Open Questions And Residual Risks

Receipts and hashes protect the ordinary local workflow against changes; they do not prove an adversarially immutable history or unseen generation chronology. A caller could deliberately choose a different attempt directory or edit both receipt and data. The frozen schedule, no-rerun instructions and independent final artifact audit remain necessary. Missing source/packet before launch may leave only the reserved directory, which must remain a failed scheduled attempt; it is not permission to recreate or retry it. Frozen packet validity and identity are prerequisites to interpreting load_attempt's scheduled IDs.

Literal parsing/JSON encoding has ordinary Python representation semantics; semantic completeness and correct condition attachment still require independent reading. The 20 tests demonstrate transport/structural regressions, not the new ledger prompt's success. Native model settings are uncontrolled and repeats correlated; this synthetic experiment remains separate from sealed evaluation and cannot establish universal reliability.

## Verdict

**Ready for freezing and generation.** No concrete preflight blocker remains. The earlier whole-packet and first-save gap is addressed by executable checks and demonstrated failure-sensitive tests/probes.

## Recommended Next Actions

Complete the pre-generation source/code/input freeze, then perform exactly the scheduled 21 first-response packet submissions. Preserve their original literals, raw JSON, receipts and failures; use execute/load_attempt for every slot. Apply the already-fixed rubric and gates without tuning, then use the reserved third review for completed results. No additional review instance or workstream was created.

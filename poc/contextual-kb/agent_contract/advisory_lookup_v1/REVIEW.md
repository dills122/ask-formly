# Independent integration review

Review instance: 1 of 3. Verdict: **Not ready**.

## Findings

### P1 — Preserve the degraded lookup packet when the worker fails
`cli.py:40–41` unconditionally invokes `verify_unchanged()` on every successfully created extractor. `transport.py:_exchange` closes the worker after an inference error, timeout, malformed response or broken pipe. The lookup catches that failure and retrieves normally, but the subsequent verification raises `RuntimeError: GLiNER worker unavailable`, so the CLI never emits the result. This violates the contract's caller-visible fail-open behavior. The existing tests separately verify lookup degradation and transport closure, missing their composition.

Reproduced with the real JSON transport, an injected failing worker, and a fake retrieval index: the full query ran once with depth 8, all workers closed, but no packet returned. See `test-output/review-reproduce-cli-failure.py` and `review-real-transport-failure.json`. No model inference or real retrieval was rerun.

Smallest correction: represent unavailable post-failure verification explicitly in the degraded result and keep returning its candidate packet; retain hard errors for an observed integrity mismatch and real retrieval failure. Add tests through `cli.run`, covering worker failure, cleanup and unchanged candidates.

### P2 — Close verification workers on exceptional exits
`verify_live.py:43–62` closes loaded workers only after every lookup, evidence write and integrity verification succeeds. Exceptions in retrieval, serialization, persistence or verification bypass cleanup; calling the harness in a long-lived process can leave its model subprocess and descriptors alive. Wrap each worker lifecycle in `try/finally`, with closure registered before evidence writes, and test exceptional paths without rerunning frozen inference evidence.

## Plan Review

The implementation follows the chosen architecture: caller-supplied foundation reasoning, optional advisory GLiNER annotations, and unchanged full-question hybrid retrieval. The existing bridge is invoked with `enhanced=False` and only `search_requests`; hints cannot enter its query expansion branch. Foundation validation precedes model loading/retrieval, and returned fact records are copied. Reusing frozen POC components avoids changes to the locked DB, retrieval or model artifacts.

The separate environment correction is justified by retained failure provenance: the first run lacked torch and never established native success. Its source copies and outputs remain hash-verifiable. Both existing environments are reused without package/model changes. Persistent subprocess transport creates lifecycle obligations that are not fully covered yet.

The four-item plan remains unchecked; final completion should reflect the accepted review and final preservation. This is an integration acceptance exercise, not an annotation-accuracy gate or production qualification. No architectural pivot is required to address the findings.

## Author-Claim Reconciliation

| Claim | Evidence | Status and consequence |
| --- | --- | --- |
| Hints do not alter queries or candidates | lookup/integrate/bridge source; offline reconstruction of all 144 packets | Confirmed |
| Advisory failures degrade visibly while search continues | Lookup tests; actual pipe plus cli.run failure reproduction | True internally, contradicted at CLI output boundary; P1 |
| Worker cleanup covers failures | transport tests/source, CLI finally, harness lifecycle | CLI/transport cleanup works; harness lacks exception cleanup; P2 |
| Both frozen adapters execute natively | 70 raw extraction records per seed; parameters-before/after | Confirmed for retained run |
| Parameters and DB unchanged | 564 parameter hashes per seed equal training receipt and before/after; DB setup hash | Confirmed |
| Usable default CLI | cli-native.json and cli-first-freeze | Confirmed happy path: 2 hints, 1 query, 8 facts, integrity checks true |
| Prior evidence and frozen boundaries preserved | Qualified preserve.snapshot; seven freeze audits including archived original sources | Confirmed, 48 protection chains unchanged |
| No new accuracy or answer-quality claim | CONTRACT/README/author explanation | Appropriately bounded; semantic role errors remain possible |

## Verification Performed

- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/advisory_lookup_v1 -p 'test_*.py'`: 20 tests passed.
- Real subprocess transport plus mocked index reproduction through `cli.run`: full retrieval occurred, worker closed, but result was lost with `GLiNER worker unavailable`.
- Read-only evidence reconstruction: 36 saved plus 12 fresh inputs, 48 packets per arm, 70 derived-question extractions per seed. Exact source question order/text/count, search projections, query logs, final IDs and complete fact records match foundation-only for both seeds.
- Seed 1701: 73 hints including 38 API hints, no diagnostics. Seed 1702: 71 hints including 39 API hints, two explicit overlapping-hint warnings. Every retained hint has correct literal anchoring and `usable_as_filter=false`. These counts do not establish semantic-role accuracy.
- Parameter maps: all 564 entries per seed equal their original training receipt and before/after maps. Current DB bytes equal the saved setup hash.
- All 48 prior protection chains verify and match protected-before.json; sealed evidence handled by bytes only.
- Design, generation, original run, corrected run-ready, original live, corrected live-native and CLI freezes verify. The original run's three changed source files were checked against the preserved failed-environment-source copies.
- Recorded review audit artifacts: review-preservation.json, review-native-evidence.json, review-cli-evidence.json and the two failure reproduction outputs.

## Open Questions And Residual Risks

No RESULTS.md existed during this pass; live raw outputs and the author explanation were inspected directly. Preliminary findings were saved before author testimony. Scope was verified as the new directory on dirty main at c3091328f49d53de6b41a49c4fe5aa8f1c45e516; unrelated work is excluded. The October 16 graph reports scoped source files as not tracked; exact source fallback supports this review, not graph completeness.

Foundation generation revision remains unpinned, semantic role mistakes and original retrieval limits remain, and no final-answer, universal compatibility or 90% accuracy qualification follows from parity. The current successful native run does not remove the failure-path defect.

## Verdict

**Not ready** until P1 is corrected and the harness cleanup gap is addressed. Happy-path integration evidence is strong and preserved; remediation is small and within the agreed scope.

## Recommended Next Actions

Add failing CLI composition and harness-cleanup regressions, implement bounded fixes, preserve this reviewed source/evidence, and request independent review instance 2 of 3. Do not overwrite or rerun the completed native evidence merely to repair local failure handling.

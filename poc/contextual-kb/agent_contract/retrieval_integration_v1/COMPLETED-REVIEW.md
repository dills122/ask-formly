# Independent completed review

Review instance: 3 of 3. Verdict: **Ready** as a completed negative experiment and report. Neither model nor the API-only bridge is qualified for promotion.

## Findings

No actionable correctness or evidence-integrity finding remains in this bounded report. The two preflight reporting follow-ups are satisfied at the retained-evidence level: report-metrics.json contains any-hit, top4/top8 per batch, count sensitivity and timing components; current output manifests verify. Scripts do not enforce downstream output manifests themselves, so future reuse still requires the documented orchestration check. This review verifies current byte integrity, not historical execution order from filesystem hashes alone.

The main negative result is real: baseline mean supported recall@8 is 92.2222%; each model and gold API arm is 91.6667%. Precision falls from 22.5% to 22.0833%. Both models fail the frozen benefit gate, independently of the unchanged 30/30 required-group coverage. R06 alone loses top8 relevant-fact recall, from 5/6 to 4/6; no case gains it. The saved Formly key probe displaces the named custom-type example with default eligibility. At top4, annotation arms have only 27/30 complete required groups versus baseline 30/30. Perfect any-hit does not contradict these losses.

Accepted annotation counts independently reconstruct to seed1701 66 TP/12 FP/12 FN and seed1702 67/10/11. Pooled precision is 84.6154% and 87.0130%. Seed1701 batch precisions are 81.4815%, 85.7143%, 86.9565%; seed1702 82.1429%, 92.3077%, 86.9565%. Thus neither clears the requirement to pass every batch and pooled; seed1702 batch2 does pass individually. Seed1701 batch1 recall is also below 80%. No missing extraction record or runtime extraction error is present. Foundation deliberately emits no annotations, so its false consistency flag is inapplicable.

## Plan Review

Implementation matches the frozen plan: original full questions remain queries; optional source-ordered unique API texts create supplemental queries; saved fusion uses the unchanged RRF and obligation interleave, with eight-result cap. No other role becomes a filter. All 144 traces reconstruct exactly from their saved query rankings. Queries rise from 45 baseline to 82 each model and 84 oracle. The negative utility result despite gold API annotations supports declining further extractor training merely to improve this bridge. A proposed context-preserving query experiment is a reasonable next hypothesis, not an observed improvement or an authorization to run it.

All 36 first foundation envelopes were inspected against requests and retained conditions; their identity with records.json is exact. All 45 gold rows and all 36 relevance cases were inspected, against the 46-fact catalog including conditions/limits. Required-group substitutes are defensible under the stated catalog policy. R14 and R31 retain unresolved scope; six unsupported cases are exposure tests, not library impossibility or answer correctness tests. No new semantic reinterpretation of sealed evidence occurred.

The experimental design is bounded and prospective. Small, related synthetic questions and a narrow catalog prevent population accuracy or general speed claims. Gold-probe failure is evidence about this particular API-only transformation, not a theorem that richer annotations cannot help. The report preserves those limits.

## Author-Claim Reconciliation

| Claim | Evidence inspected | Status and consequence |
| --- | --- | --- |
| Neither model improves retrieval | Independent reconstruction of all 144 rankings and top4/top8 metrics | Confirmed; do not promote bridge |
| Both models fail annotation consistency | All 45 rows per model, raw/accepted exact sets, per-role and per-batch counts | Confirmed; seed1702 batch2 is an individual pass only |
| Reported shared boundary and role errors | Complete per-question miss/extra ledger | Confirmed; prospective conventions remain visible |
| Gold API diagnostic also fails | Saved gold-derived probes and ranking reconstruction | Confirmed within current bridge/corpus only |
| Extra extraction/query cost is material here | All request timing samples, load receipts, setup record | Confirmed; no whole-service or general speed claim |
| Core plans and model parameters unchanged | Core equality for all 36 records per arm; before/after parameter maps equal training receipts | Confirmed at saved-evidence level; no model rerun |
| Output and prior evidence preserved | 5 design, 329 run, 9 extraction, 3 retrieval, 54 result hashes; preserve.snapshot | Confirmed current integrity; all 44 prior manifests match initial snapshot |
| Preflight reporting follow-ups completed | report_metrics.py and independent aggregate recomputation | Confirmed; supplement is descriptive and does not rescore predictions |

## Verification Performed

Read protocol and tests before implementation, raw evidence before RESULTS.md; wrote COMPLETED-PRELIMINARY.md before opening RESULTS.md and AUTHOR-EXPLANATION.md. Bootstrap/parent had already disclosed scope and the R06 diagnostic, so that part was not blind. Reviewer did not inherit implementation reasoning history.

Repository HEAD is c3091328f49d53de6b41a49c4fe5aa8f1c45e516 with broad existing dirty state excluded. Read-only scope is the new experiment plus specifically reused code and hash-only preservation. Codebase-memory reported not_tracked freshness for all eleven relied-on code paths; direct source reads supplied the evidence, without reindexing or graph completeness claims.

- `python3 -B .../test-output/completed-independent/verify.py`: passed independent raw-set TP/FP/FN, role counts, exact sets, Wilson intervals, sensitivity, gold offsets, foundation identity, all retrieval per-row metrics and per-batch aggregates, query counts and manifest preservation checks. Full independently reconstructed ledger saved as recomputed.json.
- `python3 -B .../test-output/completed-independent/check_traces.py`: passed independent source-order probe, RRF and obligation-merge reconstruction for all 144 traces; timing totals/p50/p95/max, setup/load and saved parameter receipts verified.
- Same wrapper ran 13 bridge/scoring unit tests: all passed. SQLite denial uses only a disposable completed- fixture in the new review output directory. Log: test-output/completed-independent/tests.txt.
- Additional arithmetic check of typed/untyped/role F1 against retained counts passed.

No inference, live retrieval, training, dependency install, Git mutation, gold/code edit, or sealed semantic read occurred. Writes are only named completed review artifacts and test-output/completed-independent/.

## Open Questions And Residual Risks

Present integrity checks cannot prove absence of all unrecorded activity, nor establish historical pre-consumption verification solely from final hashes. Saved raw output/manifests and parameter receipts are internally consistent; no contradictory evidence was found. The report's first-run and no-retry statements rely on retained attempt records and orchestration provenance.

The foundation outputs are first submissions on these development cases, not repeated foundation qualification. No answerer was run, and no successful final-answer accuracy or real-application compatibility claim follows. The six unsupported requests always receive eight candidates; that is an explicit missing abstention capability, not a hidden success. The 89.25% engineering floor is not a statistical guarantee; one changed prediction moves batch precision several percentage points.

## Verdict

**Ready** for retaining and communicating the completed negative experiment. **Not qualified for promotion:** both frozen model annotation gates and both model retrieval-benefit gates fail; the gold API diagnostic fails too. No blocking issue or heavy architecture pivot is required to report these results honestly.

## Recommended Next Actions

Keep foundation-only as the tested working path, preserve both experimental models and all failures, and treat a context-preserving query comparison as a separate prospective experiment. Do not tune on these results and relabel them fresh qualification. Review budget is exhausted at 3 of 3; no further review instance or worker was created.

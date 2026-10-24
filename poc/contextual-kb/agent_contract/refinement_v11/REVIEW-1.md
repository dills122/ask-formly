# Independent review of v11

Review instance: 1 of 3. Verdict: **Not ready** for the predeclared fresh acceptance gate. Experiment delivery and preservation checks pass. This is a bounded question-derivation experiment, not a production readiness assessment.

## Findings

1. **P2 — V04 run 1 violates the frozen attachment rubric.** `test-output/b1-r1-raw.json:145`, observation question 0, adds the field's separately requested `options.formState.locked` configuration. Its dependency binding includes indices 0 and 1. The reviewed V04 rubric expressly forbids back-propagation into observation; runs 2/3 keep it local to configuration. Primary text, semantic and binding grades fail. Smallest future correction: keep that dependency on configuration when the source clearly makes observation independent; preserve this first output and score.

   **Material interpretation uncertainty:** this is a definite frozen-rubric mismatch, but not an unambiguous misunderstanding of the source. “Separately” can separate requested operations while “same field” retains shared field context. The contract also says a defining dependency belongs in related observation questions and allows grounded identifying context. This output describes a *requested configuration*, without inventing an only-if gate or claiming successful implementation. A reasonable broader reading would allow it. The frozen rubric takes the narrower independent-observation reading. Do not present this as an unqualified regression in understanding or silently change the primary score.

2. **P2 — V24 run 3 introduces an additional configuration qualifier under strict source attachment.** `test-output/b3-r3-raw.json:351`, configuration question 2, ends with “if that dependency is supported.” The source's explicit narrower “Only if” clause governs observation, while configuration is under the earlier dynamic-placeholder gate. Primary text/semantic fail for the added eligibility; binding passes because the ledger correctly assigns the narrower source gate only to observation index 3. Smallest future correction: retain the source's distinct gate attachments without adding a new configuration condition; do not repair this output.

   **Material interpretation uncertainty:** the added phrase can reasonably be read as a harmless applicability/prerequisite caveat to configuring the requested dependency, especially since dependency support is itself explicitly requested. The frozen rubric gives the narrower gate only to observation, and the inherited contract cautions against inventing eligibility from library reasoning. The primary uses that stricter reading; the sensitivity below makes the alternative visible.

No additional material defects found in the small selector/serializer code. C12 run 3 repeats its support interrogative inside attachment; redundant wording does not change requested meaning. V14's global “version 6 or version 7” preserves unresolved alternatives. V17 run 1 uses a meaningful return-event excerpt and keeps “after” in question text. Neither is failed for exact wording, arbitrary question counts, or redundant ledger inventory. U22 passes using the prospectively changed criterion, not a retrospective regrade.

## Plan Review

The implementation matches the bounded plan: a new v11 prompt selector reuses unchanged same-POC structural transport, adds eight lines of scope/history guidance plus heading, and introduces a six-line standard-library serializer. No new runtime dependency or downstream behavior is involved. The source imports remain inside this POC. Tests cover selection, unchanged request/output, parser strictness, source-copy enforcement, optional hints, and serialization escaping/error behavior. They intentionally cannot prove semantic completeness or attachment correctness.

The acceptance requirement is 24/24 fresh cases passing all three runs and 6/6 diagnostics passing all three. The primary fresh gate fails; the diagnostic gate passes. Independent review and reporting/final freeze were still pending in task_plan.md at review start, appropriately owned by the parent. No further reviewer, repair, resampling or implementation was initiated.

Scope: dirty `main`, HEAD `c3091328f49d53de6b41a49c4fe5aa8f1c45e516`. Numerous inherited tracked/untracked changes exist; review boundary is refinement_v11 and its referenced unchanged POC dependencies, not the whole worktree diff. No staging, commits or publication. The preliminary report was saved before AUTHOR-EXPLANATION.md was opened; no parent semantic grades were read. After preliminary assessment, the parent raised source ambiguity for the two observed concerns; this report evaluates that challenge explicitly while retaining independent primary grades.

## Results

Text means question/reason meaning; semantic adds normalized globals. Binding is complete, meaningful source-to-question attachment, independently of structural validity. Joint requires structure, semantic and binding. All global scope projections pass 90/90.

| Cohort | Run | Text | Semantic | Binding | Structure | Joint |
| --- | --- | --- | --- | --- | --- | --- |
| Fresh | 1 | 23/24 | 23/24 | 23/24 | 24/24 | 23/24 |
| Fresh | 2 | 24/24 | 24/24 | 24/24 | 24/24 | 24/24 |
| Fresh | 3 | 23/24 | 23/24 | 24/24 | 24/24 | 23/24 |
| Fresh total | all | 70/72 | 70/72 | 71/72 | 72/72 | 70/72 |
| Diagnostics | each of 1/2/3 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| Diagnostics total | all | 18/18 | 18/18 | 18/18 | 18/18 | 18/18 |

Fresh all-three: text/semantic/joint 22/24; binding 23/24; structure 24/24. Diagnostic all-three: 6/6 on every dimension. Combined joint 88/90, all-three 28/30. No scheduled slot excluded or salvaged.

Primary semantic stability including globals is 22/24 fresh and 6/6 diagnostics; ledger-obligation stability 23/24 fresh and 6/6 diagnostics. Exact normalized output equality across three runs is 2/24 fresh (V08/V16), 0/6 diagnostics. Different reasons, excerpt boundaries and question decomposition can be semantically equivalent despite unequal JSON.

Sensitivity, separate from frozen primary scores:

- Allow only V04's grounded identifying context: fresh joint 71/72 and all-three 23/24; binding 72/72. V24 remains.
- Allow only V24's support caveat: fresh joint 71/72 and all-three 23/24; binding stays 71/72. V04 remains.
- Allow both: fresh joint 72/72 and all-three 24/24; diagnostics unchanged. These are interpretive alternatives, not revised primary evidence, repaired outputs or a causal improvement claim.

## Author-Claim Reconciliation

| Author claim | Evidence | Status and consequence |
| --- | --- | --- |
| Unknown-null/setup-history clarification is isolated | Contract diff against v10; selector imports | Confirmed; only new v11 rule block and version heading in contract |
| Standard encoding retains wrong-but-encodable content | delivery.py, six tests, 12 AST literal reconstructions | Confirmed for retained outputs; semantics remain fallible |
| 90 scheduled outputs, 12 packets, all structural | Raw IDs, packet inputs, records equality, strict parser and validate | Confirmed, 90/90 |
| 14 v11, 8 v10 and 8 scorer tests pass | Independently executed suites | Confirmed; no semantic guarantee |
| TDD red then green | Retained red missing-module log and green log | Consistent; historical chronology is retained testimony, not independently reconstructed |
| Only U22 diagnostic rubric changes | Diagnostic rubric comparison with v10 fresh/diagnostic entries | Confirmed; other five unchanged |
| Fresh input review altered V09 event requirement | author-submitted versus reviewed rubric | Confirmed; only V09 differs |
| 39 manifests, 38,688 overlapping entries protected | Executed byte-only preservation snapshot | Confirmed; protected-before and after-generation equal current snapshot |
| No feedback/retry; first constructed objects | Producer AST shows one literal rows assignment then direct serializer write, frozen bytes match | Consistent with artifacts; hashes cannot prove absence of unseen attempts or generator exposure |
| Native settings uncontrolled; no production or causal claim | Protocol, delivery boundary, author explanation | Appropriate limits; neither unit tests nor valid JSON establish deployed-model reliability |

## Verification Performed

Read all 30 requests, full reviewed rubrics, all 90 raw outputs and code/contract/plan directly. Exact declared source excerpts and assigned question copies validated on every output; semantic review additionally assessed omissions, scope, literals, gates, stages, controls and cross-question attachment. Wrote 90 semantic judgments and 30 stability judgments.

Executed from repository root:

```sh
python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v11 -p 'test_*.py'
python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v10 -p 'test_*.py'
python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/v3_stress -p 'test_assess.py'
```

Results: 14, 8, 8 tests passed. Additionally ran a read-only Python -B verification using `ast.parse`/`ast.literal_eval` for each producer's literal `rows`, never executing producer modules. All 12 raw UTF-8 byte strings exactly equal `delivery.serialize_batch(rows).encode()`. All four packets exactly match contract, delivery instructions and batch requests; 12 raw/producer pairs reconstruct every scheduled ID/run and equal records.json. Static nonliteral statements in each producer are imports/path setup and one direct serialize/write only, with no semantic validation/filtering or repair.

Current 90 outputs preserve question_plan/search_requests under absent, empty, malformed, valid and overlapping advisory hints; original objects remain unchanged. Old malformed v10 b4-r2 JSON remains rejected. No invalid packet required primary salvage.

Verified local manifests: candidate 12, input 21, raw 24, round1 6, round2 6, diagnostic raw 6 entries. Executed the inspected byte-only preservation chain: 39 inherited manifests, 38,688 overlapping entries, identical to protected-before and protected-after-generation. Sealed data was hashed as opaque bytes only. Final v11 reporting/freeze remains parent work.

Graph coverage reports reviewed code paths `not_tracked`; conclusions rely on full direct source reads, not graph completeness. No root npm/Angular suite was needed for this isolated question-layer experiment; no indexing, packaging or Angular behavior changed within scope.

## Open Questions And Residual Risks

V04/V24 interpretation uncertainty materially changes the strict gate; preserve both primary and sensitivity rather than claiming unambiguous failure or success. Tests establish transport properties, not autonomous semantic repair. Growing prompt length and its cost are unmeasured. Native model revision, temperature and seed are uncontrolled; targeted synthetic development remains correlated. Valid batch delivery is enforced by Python serialization, not proof of text-only model or deployed API JSON reliability. No retrieval, answer fidelity, production, latency, cost or universal Formly compatibility conclusion follows.

## Verdict

**Not ready** under the frozen fresh gate (22/24 all-three); diagnostic gate passes 6/6. The completed experiment is reviewable and its preserved mechanical evidence is sound. Readiness is sensitive to the two disclosed source-attachment interpretations, so this verdict must not be summarized as two unambiguous user-intent misunderstandings.

## Recommended Next Actions

Parent should aggregate the primary grades, report sensitivities alongside them, reconcile findings without rewriting originals, then complete preservation/final freeze. Retain the failed gate and interpretation uncertainty. Any future policy clarification or candidate belongs in a new prospective trial; this review performs no fixes or replacement runs.

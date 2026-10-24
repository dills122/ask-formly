# Independent preflight review

Review instance: 1 of 3. Verdict: **Ready** for the fixed diagnostic acquisition/selection experiment. This does not qualify the candidate for promotion.

## Findings

No demonstrated implementation blocker remains in the frozen harness.

**P2 — Retained foundation scope loss in R26.** In `data/records.json`, R26 `output.formly_questions[1]` asks about inherited defaults but omits that the named derived type reuses an **input** renderer. The source identifies those defaults through that requested renderer setup. The first question retains input, while neither ledger binding records it. Qualification_v3 requires standalone preservation of the applicable supplied configuration/dependency and its exact source binding; the same referent is not an independent general scenario. A future generated plan should preserve the input-derived scope in the follow-up and ledger. Do not alter this saved output: `data/semantic-review.json` records the failure, and the existing semantics gate correctly blocks promotion. This evidence defect does not prevent an honestly scored diagnostic run.

## Plan Review

Four arms adequately separate fixed-depth candidate acquisition from relevance selection within the bounded catalog. Depth20 retains original top8 candidates rather than assuming a prefix. Original question strings are used unchanged. No query expansion, link augmentation, serving changes, model training, or knowledge edits are introduced. Strict per-case fact and group preservation is checked in addition to pooled gain and per-batch floors.

Prospective labels were saved before implementation review and any retrieval. They contain 18 direct, 12 partial, and 6 unsupported requests. The 12 partial cases retain explicit missing aspects; required groups measure supported aspects only. Group completion must not be described as full request coverage. The small synthetic sample and known topic reuse cannot establish population accuracy, deployed latency, or answer correctness.

Remaining planned steps are appropriate: create the transitive run freeze, acquire once, freeze acquired lists, invoke six independent selector contexts, preserve first outputs plus byte/timing provenance, freeze outputs, score once, and conduct the completed-evidence review. These are execution obligations, not completed preflight evidence.

## Author-Claim Reconciliation

| Author claim | Evidence | Status and consequence |
| --- | --- | --- |
| Existing top8 foundation retained; depth20 need not prefix it | candidate.acquire; original PilotIndex.hybrid and merge_obligations; non-prefix test | Confirmed; fair baseline acquisition and candidate availability |
| Selector sees opaque handles without retrieval ranks or gold | candidate.present and schema test | Confirmed for supplied payload; native context isolation must still be checked during execution |
| Invalid output yields empty packet without repair | candidate.account and validate_selection; malformed-envelope/row tests | Confirmed |
| Fixed scoring and preservation gates | assessment.assess; bridge.relevance; loss and semantic-failure tests | Confirmed; R26 forces semantics gate false |
| Read-only database and exclusive first evidence writes | pipeline.acquire_all; bridge.readonly; safety tests | Confirmed in code; live execution not performed |
| Catalog matches source DB | Independent read-only SQL comparison | Confirmed, all 46 records including qualifications |
| 36 structurally valid outputs and 59 questions | Independent build_plan validation of all saved outputs | Confirmed, separate from semantic failure |
| 17 tests pass | Independent unittest run | Confirmed |
| Tests preceded implementation | Author testimony; no historical execution reconstruction performed | Unverified historical sequencing; current tests directly inspected and passed |
| Prior evidence remains byte-identical | preserve.snapshot and implementation manifest verification | Confirmed at preflight; no sealed semantic access |

## Verification Performed

- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/relevance_selection_v1 -p 'test_*.py'`: 17 passed; saved in `test-output/preflight-tests.txt`.
- Independent label ID/order/catalog/group/support invariants and declared exact condition spans: passed; `test-output/preflight-label-checks.json` includes original hashes.
- All 36 foundation objects passed unchanged build_plan structural validation; 59 questions. Catalog exactly matches the 46 read-only DB records: `test-output/preflight-source-checks.json`.
- Frozen implementation bytes verified against `test-output/implementation-freeze.json`.
- Extended prior-evidence byte preservation passed: `test-output/preflight-preservation.json`. Sealed artifacts were hashed only.
- No retrieval, selection, model inference, staging, or source repair performed.

The graph reports every relied-on implementation/data path checked as not_tracked in its October16 generation. Conclusions use direct source reads, not graph completeness. The bootstrap HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516 matches; unrelated dirty-tree changes remain excluded. Author explanation was read only after saving the blind preliminary review.

## Open Questions And Residual Risks

The unit tests do not execute a real native selector or embedding acquisition. Actual runtime failures, first-output provenance, selector input/output sizes, and wall times must remain visible in the completed review. Full run freeze and selection freeze are still required; current implementation freeze alone is not sufficient authorization for scoring changed inputs. Native relevance rationales are not entailment proofs. Partial catalog support remains partial even with perfect retrieval. The review does not certify universal Formly compatibility or absent capabilities beyond this catalog.

## Verdict

**Ready** to run the fixed diagnostic harness. **Not qualified for promotion:** R26 is a retained semantic foundation failure under the prospective zero-failure gate. There is no basis to waive or repair it based on later retrieval outcomes.

## Recommended Next Actions

Freeze all transitive execution inputs and this review's labels/semantics; execute the planned fixed experiment once. Preserve all failures and partial-support distinctions. Request the completed-evidence review within the remaining review budget; do not tune or change the protocol based on results.

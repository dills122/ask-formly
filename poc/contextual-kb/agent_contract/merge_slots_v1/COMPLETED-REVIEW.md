# Completed independent review

Review instance: 2 of 3. Verdict: **Ready** as a completed negative experiment. **Protected-six is rejected and remains unqualified.** This verdict does not authorize publication or promotion.

## Findings

No blocking implementation or reporting defect remains within this experiment's bounded scope. The candidate fails its predeclared requirements; these are measured experimental findings, not reasons to repair the frozen experiment:

- **Strict safety fails:** at eight, M01 loses `props-and-registration/type-name-registration`; M13 loses `custom-types-and-wrappers/component-needs-registration`. Both gain `custom-component-use/registered-component-selected-by-type`. Surviving substitutes preserve required-group coverage but do not cancel the fact losses. Evidence: `test-output/retrieval/queries.jsonl`, records M01/M13; independently reconstructed packets and `test-output/scores.json` paired fields.
- **Utility fails:** protected pooled recall equals foundation, 92.0714286%, with zero gain in each batch. Current fusion reaches 92.5476190%, a 0.4761905-point improvement below the fixed 0.5-point utility threshold, and loses M01's baseline fact. Protected versus current rescues no relevant fact at eight and loses M13's registration prerequisite. No complete-group gain/loss occurs at eight between these policies.
- **Consistency fails:** batch 2 is 85.7142857% for foundation/protected and 87.1428571% for current fusion. Every arm fails the every-batch 89.25% floor even though each pooled mean exceeds 90%.
- **Input semantics fail independently:** M36 foundation question index 1 asks about automatic database migration without carrying the original server-side SQL-schema referent; its ledger is empty. The source request, first saved output, and qualification_v3 CONTRACT's standalone-question and referential-follow-up rules substantiate the retained failure. Its supplement preserves its actual foundation input and inherits the source omission. Keep the separate 35/36 foundation and 36/36 supplement verdicts; do not relabel or repair.

The six-prefix invariant passes all 36 requests. All arms retain the same 28/30 complete-group count at eight; missing groups are M14 reverse-merged-defaults and M19 wrapper-decorates-not-control. Every unsupported request produces eight candidates, totaling 48 per arm; this is exposure, not an answer hallucination measurement.

## Plan Review

The protocol defines a fixed, gold-blind six-slot policy, shared fresh acquisition, three arms, prospective labels and distinct safety/utility/consistency/input gates. Code and artifacts implement that scope. The policy does not consult gold; metrics do so only after acquisition and its manifest. `acquisition.acquire` calls the unchanged contextual retrieval once, reconstructs all arms and checks current-fusion parity. `run.main` uses exclusive result creation, freezes acquisition before scoring, verifies code/input manifests and checks the DB hash.

Tests meaningfully cover prefix retention, fallback/no-supplement identity, short and empty inputs, uniqueness, sourced IDs, query acquisition once, missing arms/batch identity, unsupported recall, fact loss hidden by substitutes, missing groups, and current-fusion group rescue accounting. The two preflight reporting additions are present before run freeze. The checklist in task_plan.md remains unmarked; the artifacts establish completion, so this is a documentation-status follow-up rather than missing experiment work.

The four experiment modules are small and their reused transitive paths are understandable. No serving integration, new dependency, gold-aware ranking or parameter sweep was introduced. Existing sys.path-based module resolution is fragile in an ad hoc reviewer process, but direct frozen entrypoints and the verified run were unaffected. Reviewer verification imports preservation by its qualified module name to avoid selecting the preceding experiment's preserve.py after metrics alters sys.path.

## Author-Claim Reconciliation

| Claim | Evidence | Status / consequence |
|---|---|---|
| Six fixed before results, unchanged shared policies | Protocol, design/run hashes, policy and frozen RRF/interleave source | Confirmed within artifact history; no tuning detected |
| 36 plans, 46 questions and supplements; 91 calls | First-save outputs compared with all records, all acquisition query texts/counts | Confirmed; one identical supplemental is skipped |
| Gold-blind combination and conditional metrics | policy/acquisition/run/metrics and transitive code | Confirmed |
| 22 tests and complete metrics | Reviewer unittest run and independent recomputation | Confirmed; author's earlier 20/21 counts are explicitly historical preflight stages |
| Two fact losses, no protected utility or consistency | All saved rankings, independently reconstructed metrics and paired changes | Confirmed |
| Existing DB/model/artifact integrity | Run freeze, SQLite helper/PilotIndex source, all 46 protection manifests | Confirmed current byte integrity; no model/retrieval rerun used |
| Fresh native contexts and no retries | Three first-save/completion records, unchanged saved literal/output mappings, retained task provenance | Artifacts are consistent; hashes alone cannot independently prove historical context isolation or absence of discarded attempts |
| Shared timing, not three independent end-to-end arms | Timers in acquisition and contextual retrieve, saved trace sums | Confirmed; acquisition includes existing fusion overhead |

RESULTS.md matches the reconstructed values and states the decision and limitations appropriately. Its future relevance-selector idea is only an untested hypothesis, not an authorized new workstream or demonstrated solution.

## Verification Performed

Neutral-first sequence: protocol/tests/code/raw records/catalog and preliminary ledger first; RESULTS.md and AUTHOR-EXPLANATION.md afterwards. No author reasoning was inherited in this review context. Repository boundary is dirty main `c3091328f49d53de6b41a49c4fe5aa8f1c45e516`; unrelated changes were excluded. Codebase graph coverage checks report these POC files as not tracked at the October 16 generation, so conclusions use direct source inspection, not graph completeness.

Executed:

```
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s poc/contextual-kb/agent_contract/merge_slots_v1 -p 'test_*.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 poc/contextual-kb/agent_contract/merge_slots_v1/test-output/completed-verify.py
```

Results: **22 tests pass; 36 traces, 108 packets and 216 metric sets match**. The reviewer script independently implements interleave, RRF, protected filling, precision/recall/nDCG/MRR/group accounting, paired fact/group differences, macro summaries and deterministic bootstrap intervals. A second comparison calls the frozen assessment and checks the entire score object, including gates. All design 8, generation 7, run 128, retrieval 5 and results 53 hash entries match. All **46 prior protection manifests** verify and match the pre-run snapshot. Sealed contents are read only as bytes for hashes, never interpreted semantically.

All 36 prospective labels were checked against the complete 46-fact catalog and source requests, and all 46 foundation/supplemental question pairs were reviewed. No blocking label contradiction was found. Corroborating gold is deliberately broader than minimum required groups; M25 key shapes is broad corroboration with a prospective rationale. Conditional catalog limits remain necessary for M17 showing/default behavior and M28 rebuild behavior; successful retrieval does not establish an unconditional answer. Unsupported requests correctly retain empty gold rather than receiving unrelated shared-context facts.

First-save foundation outputs and supplements match every current record. Shared timing totals independently sum to 0.602135876 seconds acquisition and 0.000438538 seconds combination; setup is 0.786969959 seconds. Counts are 46 original and 45 additional calls. The saved query text is ASCII, so the reported 5,510/11,513 character totals also equal UTF-8 bytes in this run. Protected packets differ from foundation on 21 requests despite equal aggregate metrics.

Artifacts: `COMPLETED-PRELIMINARY.md`, `test-output/completed-tests.txt`, `test-output/completed-verify.py`, `test-output/completed-verification.json`, and `test-output/completed-verification.txt`. An initial reviewer-only audit failed by selecting the previous experiment's preservation module; the qualified import corrected the reviewer script. No experiment code, labels, outputs or hashes were changed.

## Open Questions And Residual Risks

The separately frozen, explicitly post-run `DIAGNOSTIC-ADDENDUM.md` and `test-output/pool-diagnostic.json` were reviewed after the preliminary ledger. Independently recomputing all 36 unions of saved query lists confirms pooled candidate availability of 95.7142857% and batch means of 100%, 87.1428571%, 100%; both diagnostic hashes verify. M13 lacks registration-adds-configuration and type-name-registration throughout its pool. M14 and M19 lack their required reverse-merged-defaults and wrapper-decorates-not-control groups. Thus, even an oracle selecting from these fixed lists cannot clear the batch-2 floor. This upper-bound diagnostic can exceed eight items and is not a qualified fourth arm. It correctly distinguishes acquisition gaps from policy displacement without altering labels, gates or retrieval. Verification is retained in `test-output/completed-pool-verification.json`.

Fresh wording over a 46-fact catalog is not held-out-topic validation. Ten supported requests per batch and correlated topics do not support population accuracy to ±0.75 points. Bootstrap intervals are descriptive. No final-answer quality, abstention, application runtime compatibility or production latency was measured. Dependency metadata hashes document the observed environment, not exhaustive attestation of every installed binary byte. Historical isolation/no-retry claims additionally rely on task history beyond static artifact checks.

## Verdict

**Ready** to retain and report this negative experiment. **Not qualified** for protected-six promotion, independently on safety, utility, batch consistency and input semantics. Keep foundation-only as the working baseline without describing it as consistently qualified: it also misses the batch floor.

## Recommended Next Actions

Close this experiment and preserve its frozen evidence. Do not tune the reserved count, relabel cases, repair outputs or start a third review merely to seek a passing outcome. No material fix is required; the reserved third review remains unused. Any future selector hypothesis needs separate authorization, design and fresh evaluation data. The author can mark the local plan complete after accepting this review.

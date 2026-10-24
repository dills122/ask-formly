# Independent review

Review instance: 1 of 3. Verdict: **Not ready** for candidate acceptance; **evidence ready** for reporting this negative fresh-gate result. Diagnostic gate passes. No new review instance or remediation was started.

## Findings

1. **P2 — Mandatory condition ledger is incomplete.** In `test-output/b1-r1-raw.json`, N01 question 2 retains true-setting meaning but its `setting it to true` binding points only at question 1. N02 in all three `b1-r*-raw.json` files retains later property changes in question 2 but binds dependency/support/no-polling only, omitting the frozen later-change scenario. N11 in `b2-r2-raw.json` and `b2-r3-raw.json` retains invalidity in question 1 but has no invalid-transition binding (run 1 does). These are source-to-ledger omissions, not missing text or arbitrary question-count failures. Smallest credible correction is reliable per-aspect scenario/setting coverage, assessed on new data rather than repairs to these outputs.
2. **P2 — A local observation limit narrows the support question.** N18 question 1 in `test-output/b3-r1-raw.json` and `b3-r3-raw.json` asks whether observation is possible *without polling* and attaches that limit to indices 1 and 2. Source/frozen rubric assigns it to usage; run 2 leaves support unrestricted. This changes the question being asked and its ledger. Preserve the unrestricted support check separately from the limited conditional usage lookup. Do not tune this frozen panel.
3. **P2 — Frozen-rubric prerequisite/scenario omissions require explicit qualification.** N09 all three `b2-r*-raw.json` outputs omit the rubric's current-model-from-callback scenario from the ledger. N14 run 1 binds original unregistered-type state only to registration, although its frozen rubric also assigns it to subsequent usage. The text correctly reads current model from callback and uses the type after registration. N09 borders the general contract exclusion for mere requested targets; N14 borders sufficient prospective setup versus retention of historical setup. These are genuine criterion interpretation concerns, recorded as binding failures under the predeclared rubric, without posthoc waiver. They do not establish bad library question text. Even excluding all four disputed slots, the full fresh gate still fails (64/72, 20/24 all repeats).

No actionable transport correctness, security, performance or architecture defect found in the bounded candidate selector. This is a small same-POC delegation to frozen v3 transport; validation intentionally cannot detect missing undeclared semantics. Excerpt-heavy sentences are awkward but intelligible; no subjective style failure assigned. Reasons were checked and do not introduce application investigations or unsupported facts.

## Plan review

The bounded prompt-only plan is implemented: frozen inputs, 24 new cases in three batches, five separate old diagnostics, three repeats, unchanged schema/transport, independent complete grading, no new scoring mechanism. The audit adds support checks, scenario inheritance and scope checking, but cannot guarantee them. No deployment or runtime integration is within this plan. Final aggregation/publication of the evidence within this directory remains the parent's closeout task. A negative acceptance result is a valid experiment completion; changing or retrying outputs is not.

The recorded independent pass preceded AUTHOR-EXPLANATION.md. Fresh-context review is not vendor independence. Current dirty main HEAD is c3091328f49d53de6b41a49c4fe5aa8f1c45e516; the POC is untracked amid unrelated dirty changes. Scope was the explicit refinement_v6 working-tree boundary, not a claim to review the whole repository diff. No sealed cases/data/weights were interpreted. Only the four authorized reviewer artifacts were written.

## Author-claim reconciliation

| Claim | Evidence | Status / consequence |
| --- | --- | --- |
| Full v5 retained plus audit before Output | Exact text reconstruction confirms audit insertion, title bump, expected spacing; 13,491 to 17,485 UTF-8 bytes | Confirmed; no hidden schema change |
| Same v3 validator/advisory transport | candidate.py import list and full v3 candidate source; independent hint checks | Confirmed; structural pass is not semantic proof |
| 6 v6, 7 v5, 8 aggregation tests | Independent unittest runs below | Confirmed |
| 87 first responses, 12 contexts, no feedback/retries | Frozen packet/raw files reconstruct 87 unique slots across 12 batches | Artifacts confirmed; first-attempt/unseen-history claims cannot be established from files |
| 34-manifest preservation chain | preserve.snapshot() equals protected-before.json and verifies every manifest | Confirmed byte preservation, no semantic sealed inspection |
| Independent fresh author, pre-generation corrections/freezes | AUTHOR/data-review, frozen source/rubric and retained original rubric | Recorded process consistent; unseen context/timing cannot be proven by file contents |
| Fallible prompt, no production/latency/retrieval/answer claims | Protocol and observed failures | Confirmed; evidence remains synthetic and bounded |

## Verification performed

Executed independently:

- `python3 -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v6 -p 'test_candidate.py' -v`: 6/6 passed.
- `python3 -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v5 -p 'test_candidate.py' -v`: 7/7 passed.
- `python3 -m unittest discover -s poc/contextual-kb/agent_contract/v3_stress -p 'test_assess.py' -v`: 8/8 passed.
- Imported v6 preserve and asserted its 34 verified manifests equal protected-before. Candidate freeze 9, input freeze 18, diagnostic raw freeze 3, full raw freeze 12, round1 3 and round2 3 entries all match current SHA-256 bytes.
- Verified every batch packet is exactly full frozen contract plus assigned id/request pairs; four packet definitions reused for three repeats produce nine 8-case fresh and three 5-case diagnostic batches. Reconstructed all 87 unique `(id,run)` outputs from raw files; no missing/duplicate/foreign slots.
- Validated all 87 outputs, then checked no hints, malformed hints, valid spans and conflicting spans leave question_plan/search_requests unchanged and do not mutate outputs. Empty outputs cannot have a valid question span; invalid supplied spans are ignored.
- Read scoring helper `v3_stress/assess.py`: scheduled denominator is retained, missing outputs fail, duplicate/foreign grades reject, full use requires structure AND semantic AND binding. Used its unchanged summarize function for independent totals.
- Graph coverage checked for relied-on candidate/test/preservation/scoring paths: all not_tracked in October 16 graph; direct complete source reads support limited conclusions. No graph completeness claim.

Two reviewer scratch assertions initially failed due to assumptions in the check: packet requests intentionally omit scheduling-only batch metadata, and prompt reconstruction initially omitted title bump/used an extra newline. Corrected the comparison expectations, inspected the exact difference, reran successfully. These were verification-script mistakes, not evidence defects. No frozen file was changed.

## Results

`semantic_pass` includes question meaning and global scope; `text_pass` evaluates useful question text alone; `binding_pass` evaluates complete correctly attached ledger. In this panel text and semantic totals coincide because no metadata-only defect remains. Stable omissions still fail completeness.

| Measure | Fresh | Diagnostics |
| --- | ---: | ---: |
| Structural validity | 72/72 | 15/15 |
| Useful text / semantic with global scope | 70/72 | 15/15 |
| Complete bindings / full usable | 60/72 | 15/15 |
| Full usable run 1 / 2 / 3 | 19/24; 21/24; 20/24 | 5/5; 5/5; 5/5 |
| Cases passing full checks in every repeat | 18/24 | 5/5 |
| Question-meaning stability | 23/24 | 5/5 |
| Ledger meaning/attachment stability | 20/24 | 5/5 |
| Exact canonical JSON equality | 3/24 | 0/5 |

Full failing fresh slots: N01r1; N02r1/r2/r3; N09r1/r2/r3; N11r2/r3; N14r1; N18r1/r3. Meaning instability: N18. Ledger instability: N01, N11, N14, N18. Optional redundant grounded context, excerpt punctuation, reasons, or harmless repeated support wording do not create extra failures. Detailed decisions for every output and all 29 stability judgments are in test-output/semantic-review.json and test-output/stability-review.json.

## Open questions and residual risks

N09/N14 criterion boundaries are visible rather than waived; resolving them should inform future protocol design, not rewrite this frozen panel. No controlled contemporary v5 arm exists. Correlated native repetitions, uncontrolled model revision/temperature/seed, synthetic inputs and file-only provenance limit inference. No production accuracy, final-answer correctness, retrieval success or latency is established. The root indexing/package/browser gates were not needed for this isolated prompt experiment; no browser qualification claims changed.

## Verdict

**Evidence ready. Candidate Not ready.** Fresh full gate requires 24/24 cases in all repeats and fails at 18/24 under the frozen criteria. Diagnostic full gate requires 5/5 and passes. Evidence supports retaining this experiment and its failures, not asserting general reliability or causal improvement from historical percentages.

## Recommended next actions

Parent should publish the separate denominators and uncertainty notes, reconcile findings with Accept/Dispute with evidence/Defer, verify the final evidence freeze and close the experiment. Do not repair responses, weaken the rubric, tune on this panel or initiate another reviewer to replace the negative verdict. Any new development work needs a separate authorized scope and fresh evaluation. Review count remains 1 of 3; no heavy architecture pivot is required by this bounded review.

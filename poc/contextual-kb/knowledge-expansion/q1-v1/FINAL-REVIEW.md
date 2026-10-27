# Q1 independent final review

Review instance: 2 of 3.

## Findings

No actionable findings remain in this bounded Q1 experiment. The previous missing-freeze guard finding is corrected. This verdict concerns the experiment and its reporting, not production promotion or universal Formly compatibility.

The review began from FINAL-BOOTSTRAP.md in fresh reviewer context. FINAL-PRELIMINARY.md was written before FINAL-AUTHOR.md was read. No implementation conversation or author rationale was supplied to this reviewer before that preliminary record. HEAD is 250f83da2d93aababf27f169078807ff66f183ee on codex/n1-radio-native-promotion. The scope is the new untracked q1-v1 directory and its named frozen dependencies; unrelated dirty/untracked work was excluded. RESULTS.md was added during the review as an unfrozen author summary and inspected after the preliminary pass. Frozen inputs and observations remained unchanged.

## Plan Review

The implementation and retained observations satisfy the declared design:

- There are exactly160 target requests and16 separate controls, with40 targets and4 controls in each of CORE, STATE, MAT and SCHEMA. Compound counts are36,30,24,39 respectively, exceeding the minimum20 per group. All176 lookup requests retain their original full question and explicit scope. These are broad source-informed development cases, not unseen/randomly sampled requests.
- gate.py preserves the144/160 target and143/160 tolerated floor. 142 fails; control failures and critical unsupported claims fail independently. All cases and judgments must have exact unique coverage. Controls never enter the160 denominator.
- Actual observations contain176 lookups plus39 fetches per repeat,215 calls,645 total. Each recovery is one fetch of at most2 IDs already present among delivered/omitted IDs, below the frozen2-fetch/16-ID budget. No discovery calls occurred. The receipt loader checks planned versus actual arguments, complete zero-error receipts and offline-guard markers; audit.py rejects recovery after unsupported scope and changed scopes.
- Initial121/160 remains a failure, with39 failed IDs and their missing-support reasons retained. Completed160/160 meets the target in each repeat; all16 controls pass and no critical unsupported claim or tool failure was identified. Group initial/completed counts are CORE31/40→40/40, STATE27/40→40/40, MAT31/40→40/40 and SCHEMA32/40→40/40.
- Exact comparison removes only elapsed seconds. It compares complete corresponding rows, including arguments and result packets. The three equal repeats justify reuse of these particular judgments; they do not create528 independent semantic samples. Changed packets would abort this evaluator rather than silently reuse judgments.
- Both runtime implementations, models, installed124-fact DB, existing176-fact candidate and prior knowledge inputs remain preserved. No candidate promotion or model-backed inference arm is part of this experiment.

The experiment is appropriately self-contained. Copying a small reviewed transport/audit and reusing the frozen receipt loader with process-local HERE injection is acceptable bounded experiment debt. The local audit module resolves correctly. No production runtime rewrite or additional architecture is needed.

### Semantic evidence challenge

I read all176 completed answers against their frozen required points, inspected the compound/control requests, and examined the delivered cited claims, conditions and limits across the groups. I specifically checked all39 recoveries against their recorded initial gap and combined actual delivered evidence. The observed fetches supply the missing mechanisms rather than merely increasing a fact count. No positive case was accepted solely because it safely abstained from its requested supported mechanism.

Several apparent headline gaps are resolved by actual delivered authored quotations, not by opening linked upstream URLs: CORE19 includes undefined/non-hidden default eligibility and defined-value retention in the default quote; STATE03 includes the modern hide callback shape; STATE09 includes managed onInit Observable return/disposal in the manual-subscription quote. The completed answer can legitimately use those delivered portions. All cited facts in both assessment stages have authored_source.quote content in their corresponding packets; a source URL alone was not treated as delivery.

The difficult boundaries remain in the answers: shared-control lookup versus independent model slots; reverse-default arrays versus model defaults; parser bypass under positive change-mode debounce; keyless versus keyed model events; typed/null-error-map versus named Boolean validation; first-error/routed-message suppression; Material readonly versus disabling and payload exclusion; date adapter and registration separation; native/radio binding and focus limits; schema format/type/required distinctions; tuple renderer responsibility; composition dispatch versus logical conformance; and reference escaping/cycle limitations. All16 controls decline the requested unsupported release/adapter, application diagnosis, browser/accessibility or universal-conformance certification.

Most SCHEMA answers restate the required-point text verbatim. That is consistent with the declared explicit-caller-judgment/evidence-usability experiment, but it reinforces why the100% result must not be presented as blind or autonomous answer accuracy. The semantic review checks support against delivered records; it is not a new audit of every upstream Formly source file or execution of Angular examples.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status and consequence |
| --- | --- | --- |
|160 targets,16 controls,129 compound targets; fixed integer gates|PLAN.md, cases.json, PREPARATION.json, lookup-calls.json, gate.py and tests|Confirmed; no denominator exclusion or control pooling.|
|Three unchanged tool flows through real guarded stdio|harness.py, server.py, actual qualification rows/receipts/stderr, inherited read_run loader|Confirmed by retained transport artifacts and code; reviewer did not rerun live MCP calls.|
|39 missing initial answers recover through observed IDs, without discovery|Initial/completed assessments and all recovery packets; audit.py provenance checks|Confirmed; maximum2 fetched IDs per affected request.|
|Recovered answers satisfy all required parts|Frozen rubrics, completed answers, delivered cited claims/conditions/limits and selected authored quotations|Supported by independent semantic inspection; no concrete omission found. This remains bounded manual assessment.|
|22 tests pass; prior missing-freeze/import fixes are effective|Current source, test_freeze.py, combined unittest run, actual imported module paths|Confirmed current behavior. Historical red-test chronology is retained testimony/log history, not independently re-executed.|
|Preflight continuity retained without case/criterion changes|Compared preflight-freeze.json to freeze.json|Confirmed: evaluate.py is the only changed pre-existing entry; additions are review records and test_freeze.py.|
|326 protected paths and both databases unchanged|Recomputed Q1 baseline-state hashes; inherited preservation/DB checks|Confirmed zero mismatches. Q1 baseline-state equals the inherited manifest.|
|Full maintenance before/after passed|maintenance-after.log and reported before-run history|After-run log confirms local foundation success; reviewer did not rerun the full maintenance suite. Before-run success remains retained author/log evidence, not a new reviewer execution.|
|Fresh questions; no sealed evaluation opened during preparation|Declared process, scoped files and frozen artifacts|Process claim not independently provable from hashes; reviewer did not open old/sealed questions to test it. No held-out claim is made.|
|No universal accuracy, statistical gain from repeats, or model-backed inference qualification|FINAL-AUTHOR.md, RESULTS.json semantics, RESULTS.md interpretation|Confirmed appropriately limited reporting.|

## Verification Performed

Executed from /Users/dsteele/repos/ask-formly:

1. `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/q1-v1 -p 'test_*.py'` —22 tests passed, including both missing-manifest cases, guarded entrypoint import, integer thresholds, provenance/scope restrictions and repeat comparison.
2. `poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/q1-v1/evaluate.py` —exit0; reproduced all RESULTS.json counts, zero failed controls/critical flags,645 calls and exact_repeat_equality:true. This checks mandatory execution/assessment hashes and inherited protected inputs/DB hashes before aggregation.
3. Read-only Python inspections — verified counts, original-request equality,176+39 per-repeat tool distribution, maximum2 fetched IDs, nonempty delivered authored quotes for every cited fact in both stages, local audit import resolution, preflight/run manifest continuity, and all326 Q1 baseline-state file hashes with zero mismatches.
4. Inspected maintenance-after.log — local foundation checks passed, with no hosted inference or sealed evaluation. This is historical verification evidence, not a newly executed maintenance command.

Graph-first discovery returned no Q1 symbols; exact-path coverage for all nine local Python files and the inherited report/candidate helpers reported not_tracked. The review therefore used direct source fallback and makes no graph-completeness claim. One ad-hoc packet-printing inspection initially stopped on an unsupported-scope control lacking facts; it was corrected to use an empty fact list for those packets and completed. This was a reviewer inspection-script issue, not an experiment/tool failure.

Only FINAL-PRELIMINARY.md and FINAL-REVIEW.md were written. No implementation fixes, additional reviewers, new workstreams, runtime inference, builds, staging, commits, publishing or promotion occurred. Global sealed content was not inspected; protected files were hashed without displaying their contents.

## Open Questions And Residual Risks

A frozen manifest records content identity; by itself it cannot independently prove when a file was first frozen or that a human/agent never consulted older questions. Execution chronology and question freshness remain process assertions with retained review history. Current case/criterion continuity and immutable observation checks are sound.

The source-informed fixed set, self-assessment by most group authors and closely related scenarios limit generalization. Independent inspection found no actionable semantic contradiction, but this is not a statistical estimate, external expert adjudication, browser/AOT qualification, or new upstream-source audit. Missing initial support remains39/160 and should stay visible whenever the completed result is quoted. Adaptive choice of an observed omitted ID is still caller work, not evidence of autonomous planning performance.

The current evaluator deliberately fails on changed repeat packets; it does not implement a general per-repeat assessment workflow. No changed packets occurred, so this does not affect this result. A future materially different run must preserve its own evidence and judgments under a separately frozen experiment.

## Verdict

**Ready** for acceptance of this bounded Q1 qualification result. The recorded completed flow meets the predeclared target with supported answers, passing controls, valid provenance and exact fixed-plan replay. This does not authorize promotion or establish whole-library, held-out, arbitrary-application or model-backed inference accuracy.

## Recommended Next Actions

Accept the Q1 result with its initial/completed distinction and limitations intact. Retain the preflight failure/fix history and this independent review. Any promotion remains a separately authorized action; no further review instance or remediation workstream is required by this pass.

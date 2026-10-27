# Independent prebuild review

Review instance: 1 of 3. Verdict: **Ready with non-blocking follow-ups** for the isolated candidate build and frozen comparison; not admission, promotion or qualification approval.

## Findings

**P2 — Normalize the disposition ledger fact IDs.** `n3/source-decisions.json:16` and `n4/source-decisions.json:16` begin a set of 40 references written as `document.fact`; the canonical authored/compiler IDs are `document/fact`. Exact joins against the combined installed/draft fact set fail for those references. All 40 resolve after first-dot normalization, so the intended coverage is identifiable and this does not undermine the build inputs or source truth. Correct those ledger references and validate their resolution before issuing the final source-to-fact checklist. The initiating author has accepted this follow-up; no reviewer fix was made.

No blocking source-truth, isolation or experimental-integrity defect identified in this prebuild target.

## Plan Review

The six package mappings account for the included backlog topics through candidate claims, existing facts and reasoned exclusions. The 52 additions are split 8/7/13/7/8/9 across N2–N7. Unsupported browser, cross-release, adapter, application-policy and full-conformance generalizations remain explicitly bounded. The plan preserves installed124DB and uses one cumulative 176-fact candidate, exposing cross-topic retrieval competition while retaining separate package gates. This is proportionate and consistent with the established N1 mechanism.

The 105 fixed cases contain 85 targets and 20 controls. Under the author's target-usability criterion, minimum passing target counts are N2 9/9, N3 9/10, N4 17/18, N5 13/14, N6 15/16 and N7 17/18, with every control separately passing. Record these integer gates before execution and do not pool controls into a target score. Zero critical unsupported claims and zero baseline-supported regressions remain independent requirements. Q1 and retained model-backed end-to-end qualification are outside this comparison.

`audit.py` checks explicit flags, citation IDs, observed recovery IDs, budgets, scope/plan continuity and repeat packet equality; it deliberately does not judge semantic support or implement all package gates. Final assessment must inspect actual answers and delivered claims/conditions/limits/quotes/excerpts. Neither whole-file citation URLs nor the frozen expected fact IDs grant the caller unseen evidence. Repeat equality allows judgment reuse only for identical packets; it does not create independent caller generations.

## Author-Claim Reconciliation

| Claim | Evidence | Status / consequence |
| --- | --- | --- |
| N1 transport/server reused; builder only changes size | Direct diffs of candidate.py, harness.py, server.py against material-radio-native-v1 | Confirmed; unchanged isolation mechanism, expected counts 176/33 |
| Installed assets preserved | candidate.preserved(), baseline-state.json, Git diff | Confirmed: 326 protected-file hashes and installed DB hash match; no tracked changes |
| Drafts lint and focused tests pass | Independent commands below | Confirmed: 52 new facts, zero lint errors, 20 tests pass |
| Pinned source-backed claims and bounded exclusions | All six ledgers/drafts/cases; cached upstream hashes; direct implementation inspection | Confirmed within bounded review; ledger identifier defect above |
| Three repeat comparison and actual answer judgments | Plan and harness/audit contract | Planned only; no candidate or comparison executed in this review |
| Initial RED and prior maintenance run | Author explanation | Historical author testimony; not independently replayed or counted as fresh reviewer validation |

### N6 external pattern documentation

`draft-authored/json-schema-scalars.json:128` attributes anchoring to Angular documentation and carries a limit distinguishing documentation from browser execution. Pinned Formly source establishes string propagation into `Validators.pattern` and the map return path; it does not itself implement Angular's matching engine. I independently checked the linked current [Angular Validators documentation](https://angular.dev/api/forms/Validators#pattern), which describes anchoring and stateful g/y flags, and the [JSON Schema string documentation](https://json-schema.org/understanding-json-schema/reference/string#regexp), which describes substring matching.

N6-09 and N6-10 test that documented distinction and reject stateless-global-pattern or automatic-substring-preservation claims. Their bounded requirements are justified. The live documentation is supplemental contract context, not a pinned Angular release, compatibility matrix or executed Material/browser result. Preserve that attribution in caller answers. The existing exact Formly applicability should not be presented as pinning Angular dependency behavior across every version.

## Verification Performed

- Read neutral bootstrap first; wrote PREBUILD-PRELIMINARY.md before opening PREBUILD-AUTHOR.md. No implementation conversation was inherited.
- Verified branch `codex/n1-radio-native-promotion`, HEAD `250f83da2d93aababf27f169078807ff66f183ee`, isolated untracked target and clean tracked diff.
- All 74 entries of prebuild-freeze.json match. All 44 package source-verification entries match cached bytes (including duplicate source copies); all 326 baseline file pins and installed DB digest match.
- `poc/contextual-kb/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/completion-v1 -p 'test_*.py' -v`: 20 passed.
- `poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/completion-v1/test-output/lint_drafts.py`: 52 additions, no errors; temporary lint inputs only, no DB build.
- Inspected all 52 draft claims and 105 case rubrics. Direct source checks included the full converter and relevant Material wrapper/select/slider/toggle, core key/merge/clone, field parser/debounce, host emission, attributes/hooks/template, validator composition and message/routed-cleanup implementations.
- Graph search returned no completion-v1 symbols. Exact coverage checks report not_tracked for code and cached source paths; conclusions use direct source inspection rather than graph completeness.

## Open Questions And Residual Risks

Retrieval availability, actual answer quality, recovery usefulness and repeat equality remain unmeasured until the isolated run. Source-level evidence is not browser or upstream-test execution. No global evaluation or qualification archive was opened, and no installed asset was rebuilt. Full maintenance was not rerun by this reviewer because the review changes no production files; its prior pass is author-reported.

## Verdict

**Ready with non-blocking follow-ups.** The drafts and experiment are sufficiently grounded to proceed to the authorized isolated build after recording the ledger-ID correction and final build/run freezes. This verdict does not claim successful knowledge admission or whole-library completeness.

## Recommended Next Actions

1. Correct the 40 ledger identifiers and check all disposition references resolve; preserve this report as the frozen-target result.
2. Freeze build inputs, then build only the new candidate and freeze actual database wiring before calls.
3. Run the fixed comparison, persist initial/completed answers and judgments, enforce the integer gates and all controls, and return results for the final independent review within the existing three-instance budget.

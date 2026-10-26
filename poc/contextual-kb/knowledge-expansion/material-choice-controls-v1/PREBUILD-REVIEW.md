# Independent prebuild review

Review instance: 1 of 3. Preliminary ledger was saved before REVIEW-AUTHOR.md was read. Scope is the untracked material-choice-controls-v1 batch on codex/material-choice-controls at eb53f184faccffc1de1ec349c0df1a29bd65091a. Unrelated untracked work was excluded.

## Findings

1. **P1 — Discovery recovery cannot pass the auditor.** `results.py:36-45` records lookup facts and omitted IDs, but ignores every `discover_formly_candidates` response. A fact observed only through discovery is therefore rejected by the subsequent get_formly_facts check with `Fetched unseen ID`. This directly conflicts with the recovery procedure in PLAN.md. Reproduced using temporary saved packets: lookup with no facts, discovery delivering an ID, then fetch of that ID. Track discovered IDs per case and scope before permitting fetch, and add a read_run regression test that accepts this sequence while rejecting a genuinely unseen ID.

2. **P2 — Identical initial plans are not mechanically enforced.** `results.py:28-30` compares each run to that arm's own saved plan; `main` only compares repeats within each arm. Neither compares lookup arguments with frozen lookup-calls.json nor compares baseline and candidate initial lookup arguments. A changed request was accepted in a synthetic run. This can confound the intended data-only comparison even with stable repeats. Validate initial calls against the frozen canonical lookup list and assert cross-arm equality; keep separately documented optional recovery calls arm-specific. Test an altered request, scope, and plan.

3. **P2 — Initial and completed evidence support are conflated.** `results.py:40-45` appends fetched facts into the original packet, and `results.py:55-65` reports only one final usability score. PLAN.md expressly requires separate initial versus completed support. Retain an immutable initial packet view and record both initial support and completed support judgments or a separately audited ledger. The present implementation cannot produce that planned distinction by itself.

## Plan Review

The seven claims are appropriately bounded to Formly 6.3.12 Material and correspond to K48/K49/K52/K62 implementation evidence. Predicate details, false map writes, strict object identity, and toggle forwarding limits match inspected upstream files. Separate toggle registration and affirmative-consent recipes are correctly deferred. Source decisions identify the relevant table subset and leave unrelated work pending.

Build isolation is credible on direct inspection: fixed child output paths, exclusive directory creation, read-only accepted DB comparison, eight-table superset checks, foreign keys, source quote/hash validation, counts, and preservation checks. No installed output is selected. No candidate build was performed in this review. Freeze and candidate manifest do not exist yet, as expected at this stage; generated database hash must be filled before transport execution.

The qualification plan is meaningful as a fixed, caller-controlled data contribution experiment, with explicit scope controls and non-independent answer reuse. Findings concern its audit implementation, not a need to replace the experiment architecture. They should be resolved before freezing/running comparison. Mapping and isolated-build design have no identified blocking defect.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status | Consequence |
| --- | --- | --- | --- |
| Seven bounded choice-control facts | draft-authored and K48/K49/K52/K62 | Confirmed | Source mapping acceptable |
| Upstream bytes match catalog | Five local SHA-256 calculations and catalog records | Confirmed | Exact pinned source evidence |
| 13 tests pass | Reviewer unittest command | Confirmed | Narrow helper coverage only; read_run untested |
| Renderer alone does not establish toggle registration | K52 and authored limits | Confirmed | Appropriate deferral |
| Candidate not yet built | Scope inventory and supplied state | Confirmed | No runtime qualification claimed |
| Tests first failed for absent modules | Author account | Unverified | Not relied on for readiness |
| Both runtimes/models remain unchanged | No tracked diff; batch-only changes inspected | Supported within review scope | No production modifications observed |

## Verification Performed

- `git status --short`, branch and HEAD verification: expected base and untracked batch; unrelated untracked artifacts excluded.
- `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/material-choice-controls-v1 -p 'test_*.py'`: all 13 tests passed.
- Independently hashed K13/K48/K49/K52/K62 local upstream files and compared hashes with receipts and canonical catalog: all matched.
- Direct full-file review of candidate.py, harness.py, server.py, results.py and their tests, plus plan, cases, lookup calls, authored mapping and source decisions.
- Synthetic temporary read_run checks reproduced discovery rejection and acceptance of a changed initial request. No candidate or installed DB was built or modified.
- Graph exact-path coverage for seven Python files reported not_tracked; direct file reads supplied review evidence. No graph completeness claim is made.
- Author subsequently reports disposable compiler lint and full project maintenance passing; these checks were not independently rerun here and are not represented as reviewer execution.

## Open Questions And Residual Risks

No browser/runtime compatibility conclusion follows from this source review. Final comparison, semantic answer review, candidate row/eligibility verification, freeze validation and installed-state preservation verification remain future gates. Table quotations summarize more detailed upstream implementation; full pinned sources are essential to the expanded claims. No sealed evaluation or qualification archives were opened.

## Verdict

**Not ready** for freezing and running the qualification harness as currently implemented. Source mapping and isolated candidate-build design are acceptable; the findings do not require a heavy pivot or wider scope.

## Recommended Next Actions

Accept or dispute each finding with evidence, correct the bounded auditor issues and add meaningful read_run tests, then freeze inputs and proceed with isolated build/comparison. Preserve the separate final outcome review within the three-instance limit. Do not promote the installed database based on this prebuild review.

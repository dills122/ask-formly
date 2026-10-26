# Final independent review

Review instance: 3 of 3

## Findings

No actionable blocking finding remains in the corrected experiment. The original run remains unqualified: candidate J10 broadened Material fetch scope in each repeat (three protocol failures). Its raw observations and failed mechanical audit remain intact.

All 30 distinct arm/case answers were reviewed against the original requests/checks and the full delivered facts, conditions, limits and citations. After independently verifying fresh evidence and retained-answer equality, these judgments were expanded to all 90 corrected observations in `test-output/corrected/independent-grades.json`.

| Measure | Baseline | Candidate |
| --- | --- | --- |
| Usable answers per repeat | 5/15, 5/15, 5/15 | 15/15, 15/15, 15/15 |
| Usable repeated observations | 15/45 | 45/45 |
| Initial semantic support per repeat | 5/15 | 14/15 |
| Controls per repeat | 5/5 | 5/5 |
| Critical claims | 0 | 0 |
| Baseline-supported regressions | — | 0 |

Baseline J01–J10 are honest gaps or partial answers, not successes. Candidate J01–J10 answer the requested conversion, cloning, registration, customization and reference questions with the delivered evidence and appropriate limits. C04 is a correct application-boundary refusal with no tool call; C05 is a correct unsupported-version refusal. Those controls count as usable boundary handling, not successful fact delivery.

Initial support is semantic, not canonical-ID coverage. C02 already receives a citation quotation explicitly explaining `resetOnHide: false` and the control-tree distinction. Candidate J10 initially receives the remote-reference quotation saying local references are handled without arbitrary-resolution guarantees, plus renderer-registration evidence; this suffices for the requested rejection of universal support. Its subsequent local-reference fetch supports the answer’s additional chains/missing-definition detail. Candidate J09 initially lacks sufficient entry-point/result-shape evidence and obtains it through discovery/fetch. Initial support therefore does not mean that every extra detail in the eventual answer was already present.

## Plan Review

The implementation follows the bounded data comparison: the unchanged model-free factories serve either frozen DB through real MCP SDK stdio, under the offline guard. The scope helper repairs the caller’s fetch arguments without editing serving code or data. The corrected run re-executes the complete call matrix, preserves the original failure, and refuses an existing output directory. Original cases/plans and budgets remain unchanged. The gate requires both mechanical and semantic success; the independently supplied grades satisfy the frozen assessment gate.

A blind first pass was not fully possible: the task handoff included the author’s approach and correction rationale. The plan, correction, tests and current implementation were read before prior review notes; no author grades were supplied. Graph coverage reports the experiment as untracked, so conclusions use direct source reads rather than graph completeness claims.

## Author-Claim Reconciliation

| Claim | Evidence inspected | Status |
| --- | --- | --- |
| Corrected transport is complete and scope-preserving | Raw calls, input sequences, receipts, stderr guards and rerun audit | Confirmed: 165 calls, zero delivery errors, zero scope failures |
| Original failure remains visible | Original raw runs and independently rerun audit | Confirmed: 165 calls, three scope failures, passed:false |
| Evidence and retained answers are repeat-stable | All corrected repeats compared with original r1 and semantic review packet | Confirmed: identical full facts/citations and answers apart from author metadata |
| Existing data/runtime assets are preserved | 846 preservation pins and both experiment freezes | Confirmed |
| Candidate adds six facts without replacing baseline rows | Read-only comparisons of all eight knowledge tables | Confirmed: 93 to 99 facts, 21 to 22 documents, every baseline row retained |
| Maintenance passed | Retained maintenance-after.txt and root report | Confirmed by log; not independently rerun in this review |

## Verification Performed

- Independently ran `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/json-schema-model-free-v1 -p 'test_*.py'`: all 11 tests passed.
- Imported and called `audit.run` read-only for both original and corrected run roots; both exactly reproduce their retained mechanical-audit.json. No audit outputs were overwritten.
- Verified all 846 preservation hashes, 13 original freeze hashes and 14 correction-freeze hashes.
- Independently checked every corrected stage input against output arguments/order and every per-case lookup/discovery/fetch budget, including fetch size at most 16.
- Verified all corrected repeats’ delivered full facts/citations against original r1, retained answers excluding author metadata, and all 30 semantic-review records against actual raw deliveries.
- Verified 31 distinct delivered authored-source quote spans against exact offsets and source hashes. The mechanical audit separately matches delivered records/citations to the selected read-only database.
- Compared all rows in documents, facts, evidence, fact_evidence, fact_links, applicability, applicability_evidence and evidence_releases; candidate is a baseline superset in every table and contains the six intended JSON Schema facts.
- Applied `assessment.gate` to the independent 90-row judgments: passed:true, complete:true, zero criticals, errors and regressions.

The corrected call total comprises 84 lookups, 66 discovery calls and 15 fetches. Six C04 no-call decisions complete the 90 answer slots. No hosted calls, new MCP experiment run, sealed material, production mutation, commit or publication occurred during this review.

## Open Questions And Residual Risks

This qualifies a bounded visible development comparison. Thirty authored answers are reused across repeats after evidence equality; the 90 slots are not independent answer generations. The same root context and visible source-derived criteria informed answer authoring, limiting independence and generalization. Fixed plans and fixed discovery choices do not benchmark independent planning. This SDK stdio test does not establish a native candidate connection, whole-library accuracy, arbitrary Material rendering, other Formly versions, application behavior or an end-to-end speedup. Historical JSON Schema and browser failures are not overturned.

## Verdict

**Ready** for the bounded model-free qualification conclusion and recommendation. The corrected run passes both gates. This does not authorize or accomplish candidate installation, promotion, publication or broader runtime qualification.

## Recommended Next Actions

Report the corrected result together with the retained failed run and the limitations above. Keep the installed DB and both runtimes unchanged. Review instance 3 exhausts this flow’s review budget; no further reviewer or heavy pivot is initiated here. Any later promotion or materially different experiment needs explicit user authorization and its own agreed scope.

# Independent qualification3 preflight review

Review instance: 1 of 3. Skills: independent-review and code-review-and-quality. Preliminary recorded before AUTHOR-EXPLANATION.md was read. Scope: qualification_v3 candidate/protocol only, on dirty main HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516. Unrelated working-tree changes excluded. No fixes, generation, additional reviewers, or sealed semantic reads performed.

## Findings

No actionable implementation or protocol findings. This is a preflight readiness decision, not semantic qualification.

The exact qualification2 CONTRACT prefix is preserved byte-for-byte; the suffix is exactly LINKED-FOLLOWUP-RULE.md (including its leading newline). POLICY is byte-identical to qualification2. The new rule requires defining restrictions on a specifically referenced observer/operation in standalone question text and bindings, while explicitly preserving independent/general API scope and optional same-field context. Earlier category-based rules still prohibit inventing success or eligibility gates from sentence order or shared subjects. The internal audit requests referent resolution, not a reasoning transcript or new output fields.

The small selector reads the new contract and preserves request data. Its structural validator and plan projection remain imports from refinement_v3. No new dependencies or runtime/retrieval integration are introduced. No local execution.py or runner.py copy exists. The plan calls the frozen qualification_v2 execution.py directly, with its frozen load_attempt for post-save accounting. Transport preserves semantic defects and rejects malformed delivery envelopes as whole packets; it does not repair meaning.

## Plan Review

The protocol prospectively fixes 48 fresh cases in six groups, three runs each, plus six diagnostic cases three times: 144 fresh + 18 diagnostic = 162 slots and 54 triplets. The fresh joint threshold, all-three threshold, per-group threshold, meaning-stability threshold, zero observed material failures, and all-diagnostics requirement remain explicit. Missing/unjudgeable outputs retain denominators and cannot pass stability. Binding-only errors are distinguished from material intent failures without disappearing from joint scoring.

The order is sound: independent input authorship, parent source/rubric review, input/candidate/criteria freeze, first submissions, fixed transport, full slot/triplet review and gate aggregation. Failure stops this candidate without tuning or replacing results. Full-results review remains required and consumes another instance within the maximum of three.

Fresh inputs are concurrently being authored/reviewed by the parent. This preflight does not certify their semantic fairness or completeness; all 48 pairs and diagnostic mappings must be reviewed and frozen before any generation. Particular boundary checks: a follow-up about *that observer* inherits its defining method restriction; a general callback signature question does not inherit a local restriction merely because it follows it; optional requested same-field setup remains optional and prospective; genuine source gates propagate only through their actual scope. These are applications of the existing text, not new grading criteria.

## Author-Claim Reconciliation

| Author claim | Evidence | Status and consequence |
| --- | --- | --- |
| Prompt-only linked-follow-up audit, unchanged POLICY and prior audit | Exact prefix/suffix and POLICY byte checks; selector source | Confirmed; limited candidate scope |
| Frozen qualification2 transport reused directly, no semantic repair | PROTOCOL, DELIVERY, execution.py, runner.py and tests | Confirmed for planned procedure; actual future invocations need receipts |
| Eight selector, twenty transport, eight scorer tests pass | Independent python3 -B unittest executions | Confirmed; no semantic-fix claim justified |
| 42 prior manifests / 39,086 overlapping entries preserved | preserve.snapshot result and protected-before comparison | Confirmed at preflight; qualification2 final manifest covers 217 files |
| Previous N21 omitted linked restriction in two runs | Author explanation only in this pass | Not independently regraded; historical diagnostic rationale is not preflight proof |
| 162 slots, first-save protocol, no retries, full independent review | PROTOCOL and task_plan | Confirmed plan; execution remains pending |
| No causal, production, retrieval, latency or final-answer claim | Protocol limits and explanation | Confirmed |

## Verification Performed

Commands from repository root, all exit 0:

- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/qualification_v3 -p 'test_*.py' -v`: 8 passed.
- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/qualification_v2 -p 'test_*.py' -v`: 20 passed.
- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/v3_stress -p 'test_assess.py' -v`: 8 passed.
- `python3 -B poc/contextual-kb/agent_contract/qualification_v3/preserve.py`: 42 manifests, 39,086 overlapping protected entries, exactly equal to protected-before.json. No sealed payload interpretation.

Evidence: test-output/preflight-candidate.txt, preflight-transport.txt, preflight-scorer.txt, preflight-protected-after.json and preflight-checks.json. The latter pins inspected candidate/protocol hashes and comparison outcomes. Tests include absolute runner CLI from an unrelated CWD, exclusive output creation, malformed literals, rejection of generated executable expressions, no semantic filtering, first-save integrity and whole-packet failures.

Graph coverage was checked for relied-on candidate, preservation and frozen transport/test files. POC paths are not_tracked in the 2026-10-16 graph generation; direct source inspection supplies the evidence, not stale graph absence claims. README and development instructions were consulted; no indexing, packaging or Angular behavior changed, so root/Angular gates were not run.

## Open Questions And Residual Risks

Model compliance with the new referential audit remains unproven. Existing selector tests cannot establish semantic improvement or detect overpropagation. Source/rubric boundaries and actual 162 outputs require independent human/agent judgment under frozen allowances. Native revision/temperature/seed are uncontrolled; synthetic cases and correlated repeats limit generalization. Hashes establish saved-byte integrity, not unseen generation history. The existing contract heading says qualification1; this inherited label has no selection effect and is not a blocker.

## Verdict

Ready — for completing input review and freeze, then generation under the fixed protocol. No blocking preflight findings. This does not authorize generation before the pending source/rubric review and freezes, nor claim that qualification passed.

## Recommended Next Actions

Parent completes review of all new source/rubric pairs and diagnostic provenance, freezes candidate/inputs/criteria and transport hashes, then runs the 21 first-response batches with the frozen qualification2 transport. Preserve every failure and perform full-results review of all 162 slots and 54 triplets before aggregation or foundation-eligibility claims.

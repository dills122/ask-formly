# Independent full qualification review

Review instance: 2 of 3. Verdict: **Not ready** for advancement as an experimental working foundation. The prospectively fixed qualification gate and the separate strict perfect gate both fail. No tuning, repair, regeneration, semantic salvage, baseline promotion or runtime integration was performed.

## Findings

### P1 — Two producer import failures invalidate 16 scheduled delivery slots

`test-output/b5-r1-producer.py:3` resolves `parents[3] / 'refinement_v11'` under contextual-kb rather than agent_contract. `b5-r2-producer.py:3` similarly adds contextual-kb before importing `refinement_v11.delivery`. The retained raw files contain matching ModuleNotFoundError tracebacks (`b5-r1-raw.json:1`, `b5-r2-raw.json:1`), not JSON batches. Both imports occur before the literal assignment/serialization. Nineteen other producer literal batches serialize byte-identically to retained raw JSON; these two do not.

K33–K40 in runs 1 and 2 therefore fail primary delivery as whole packets. The correct disposition is the protocol's fixed 16 failures and eight unstable triplets, not recovered semantics from undelivered literal drafts. These slots are unassessable for intent: `material_intent_failure:false` means no observed intent failure, not evidence of preserved meaning. This alone blocks the required 144/144 fresh structural gate. The smallest credible future prevention is a separately qualified fixed delivery runner/path rather than generator-authored imports; applying it to recover this frozen trial would violate the no-retry rule. Stop this qualification with its actual result.

### P2 — Five valid responses omit required ledger conditions while preserving question meaning

- `test-output/b3-r2-raw.json:54`, K19 run 2: the question preserves the initialization comparison, but its three ledger excerpts cover only default 8 and model values 0/undefined. None retains initialization. Runs 1 and 3 bind it.
- `test-output/b3-r1-raw.json:170`, `b3-r2-raw.json:176`, `b3-r3-raw.json:176`, K23 all runs: the question asks about change **through a model update**, but the ledger records default false and disabled state only. The supplied update method is not bound in any repeat.
- `test-output/b6-r1-raw.json:122`, K46 run 1: the exact API is neutrally verified, with uncertainty preserved, but the explicit “not silently replaced with hideExpression” restriction is absent from the ledger. Runs 2 and 3 include it. No replacement occurs in the question, so this is not an observed material intent failure.

These omissions fail binding and joint usability. An ideal response would pair each missing meaningful source excerpt with its owning question and ledger entry, but the frozen outputs must not be edited. K23 is consistently incomplete, so ledger stability does not establish correctness. Group 3 has 20/24 joint, below its 22/24 minimum even independently of group 5's delivery failures.

## Plan Review

The fixed qualification plan is coherent: preflight settled interpretation and operational stability before the recorded input freeze; 48 fresh requests span six groups, and two old diagnostics remain separate. Every source/rubric pair was reviewed here against the complete contract and POLICY. The K19 initialization requirement is source-grounded. Optional context is not treated as mandatory merely because another run includes it. No hidden exact-question-count, exact-wording or minimal-ledger requirement was imposed.

All 134 valid delivered responses were read with their source/rubric, including reasons, globals and ledger attachments, in bounded batches. All 150 scheduled slots and all 50 triplets receive explicit judgments. K06, K43 and K44 are justified empty controls. Shared prospective context in K05/K23/K32/K37/K45 and V04 is judged under POLICY. V04 run 1's “from options.formState.locked” is a meaningful directional dependency excerpt attached to the disabled-configuration question, not an isolated keyword. V24 run 1 redundantly restates broad support while preserving all requested support/configuration/observation information and genuine ancestors; this does not change the information sought.

The candidate module selects the new contract and reuses the unchanged validator/plan projection. The serializer is standard JSON encoding with no semantic filtering. AST inspection of every producer shows literal rows followed by serialization/write, with no validation-driven rewrite or feedback path. The selector and serializer tests cover their declared boundaries, but do not exercise each generated import script. That verification gap explains why passing unit tests coexist with the observed operational failure. No new dependency, application runtime import, database mutation or retrieval integration is present in the reviewed path. The bounded batch sizes and linear structural checks present no material performance concern; prompt cost remains unmeasured.

Failure is a valid completed experimental outcome. Finish aggregation and preservation documentation, then stop under PROTOCOL; do not reinterpret the thresholds or spend a new review instance replacing this unfavorable result. No heavy architectural pivot is needed to report this result.

## Author-Claim Reconciliation

The preliminary review was written before opening AUTHOR-EXPLANATION.md. This reviewer received only the neutral task/bootstrap before the first pass, not the implementation conversation or author rationale.

| Author claim | Independent evidence | Status and consequence |
| --- | --- | --- |
| New v11-derived contract plus prospective policy; transport unchanged | CONTRACT/POLICY, candidate.py, v3 validator, v11 serializer, candidate freeze | Confirmed; apply the stated allowances rather than old narrower interpretations. |
| Seven packets carry full contract/delivery/request only | Exact equality and exact key checks against all seven batch files | Confirmed; no rubric in retained generator packets. |
| 21 attempts, two import failures, 19 matching deliveries | All 21 producer ASTs and raw files, serializer reconstruction | Confirmed for retained artifacts; unseen attempts/history are not provable. |
| 128/144 fresh and 6/6 diagnostic structural | Independent packet parsing, all per-object validation and exact records reconstruction | Confirmed; whole-packet failure disposition retained. |
| 8 selector, 14 v11 and 8 scorer tests pass | Independent python3 -B unittest runs | Confirmed; tests do not establish semantic completeness or producer import reliability. |
| Forty inherited manifests/38,764 entries preserved | Independently hash every listed byte payload and compare before/after-generation summaries | Confirmed, overlapping entries; no sealed semantic access. |
| No generation before freeze, no retries or feedback | Prospective documents/freezes and static producer behavior | Consistent with saved evidence, but chronology and unseen execution cannot be independently proven by hashes. |
| Experimental eligibility only; no downstream/production claims | PROTOCOL and author limits | Confirmed as intended boundary; eligibility was not achieved. |

## Verification Performed

Working-tree scope is qualification_v1 on dirty `main`, HEAD `c3091328f49d53de6b41a49c4fe5aa8f1c45e516`. The unrelated broad repository diff is excluded. Graph coverage reports the reviewed POC files as `not_tracked`; conclusions use direct source/AST reads rather than graph completeness claims.

Executed successfully:

- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/qualification_v1 -p 'test_*.py' -v`: 8 tests.
- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v11 -p 'test_*.py' -v`: 14 tests.
- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/v3_stress -p 'test_assess.py' -v`: 8 tests.
- `python3 -B poc/contextual-kb/agent_contract/qualification_v1/test-output/reviewer-audit.py`: seven exact input packets, 21 AST literal batches without executing producers, strict raw parsing, serializer byte identity, 150 reconstructed scheduled records exactly matching records.json, current-output malformed/empty/null hint core invariance, six qualification freeze manifests and all 40 inherited manifests verified. Results retained in reviewer-audit.json.
- `python3 -B poc/contextual-kb/agent_contract/qualification_v1/test-output/reviewer-write-grades.py`: materializes the independently assessed 150 semantic rows and 50 triplet rows; it is not an automated semantic grader.

The audit's first execution stopped because an inherited manifest uses relative paths. The reviewer script was corrected to resolve those relative to the manifest's experiment root and rerun successfully. No candidate/evidence artifact was changed. A tool hook also rejected the initial preliminary-report shell call before execution; the successful preliminary write preceded author reading.

| Fixed metric | Observed | Requirement | Result |
| --- | ---: | ---: | --- |
| Observed material intent failures | 0 among 134 assessable; 16 unassessable | 0 | No observed failure; missing evidence not counted as success |
| Fresh structural | 128/144 | 144/144 | Fail |
| Fresh text / semantic including globals | 128/144 each | Report separately | 16 unavailable |
| Fresh binding and joint | 123/144 | Joint ≥137/144 | Fail |
| Fresh all-three joint | 37/48 | ≥44/48 | Fail |
| Group joint, groups 1–6 | 24,24,20,24,8,23 of 24 | Each ≥22/24 | Groups 3 and 5 fail |
| Fresh question-meaning stable | 40/48 | ≥44/48 | Fail |
| Fresh ledger stable | 38/48 | Report separately | K19/K46 differ; eight missing triplets |
| Diagnostic joint | 6/6 | 6/6 | Pass |
| Diagnostic meaning / ledger stable | 2/2 each | Report separately | Pass |
| Fresh exact JSON equality | 3/48 | Report separately | Empty controls only |
| Diagnostic exact JSON equality | 0/2 | Report separately | Wording/segmentation varies |

Fresh per-run joint is 38/48, 38/48, 47/48. Whole-panel joint is 129/150. There is no inference of meaning failure from unavailable outputs. Strict perfect-pass status is false; experimental acceptance is false independently on several gates. Optional context variation in K23/K32 does not make mandatory meaning unstable. Mandatory ledger omissions account for the distinction between question-meaning and ledger stability.

## Open Questions And Residual Risks

Native model revision, temperature and seed were uncontrolled; repeats are correlated and cases synthetic and policy-informed. This is not a causal baseline comparison or a sealed held-out evaluation. Hash checks establish preserved saved bytes, not temporal order, isolation or absence of unseen attempts. The two transport failures prevent judging the full scheduled panel's intent fidelity. No production reliability, universal compatibility, deployed structured-output guarantee, retrieval/final-answer accuracy or latency/cost conclusion follows.

## Verdict

**Not ready.** This frozen candidate run did not meet the declared experimental foundation gate. Zero observed material intent failures among delivered responses is useful bounded evidence, but does not override the delivery requirement, group requirement, joint threshold or stability requirement. The five ledger defects also remain visible. This result does not justify baseline replacement or runtime integration.

## Recommended Next Actions

Retain this review, its preliminary findings, raw failures, first literals, judgments and fixed-denominator aggregation. Complete the parent-owned report/final preservation work, then end this qualification without tuning or resampling. Any future delivery-runner work must be a separately authorized prospective experiment, leaving these artifacts and failed outcome intact. Review instance 3 is not automatically warranted and no further review was created.

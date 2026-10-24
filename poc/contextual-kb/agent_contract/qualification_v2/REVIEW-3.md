# Independent completed qualification review

Review instance: 3 of 3. Final authorized instance. Scope: qualification_v2 on dirty main HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516; unrelated repository modifications excluded. The preliminary report and semantic/stability judgments were saved before reading AUTHOR-EXPLANATION.md. No judgment changed after that reading.

## Findings

**P1 — N21 loses the non-polling observer scope in two first responses, failing the fixed material-intent gate.** In `test-output/b3-r1/output.json:145` and `test-output/b3-r2/output.json:145`, the second question asks what information is available to an unspecified observer at the invalid transition. The source asks about “the observer” of the immediately requested observation “without polling”. The frozen N21 rubric and case-review explicitly assign that restriction to both aspects. Each derived question must stand alone: retaining the restriction only in question 0 cannot constrain the independent information lookup in question 1. The binding at line 162 likewise covers only index 0. This broadens the method scope of the requested information and is a text, semantic, binding and observed material-intent failure, not just missing ledger bookkeeping. Run 3 at line 145 explicitly preserves non-polling observation and binds both indices. N21 is therefore unstable in both meaning and mandatory ledger coverage.

The smallest conceptual correction would preserve the non-polling observer in the second standalone question and bind its source excerpt there. **Do not apply that correction to these frozen outputs or tune/retry this experiment.** The required action for this authorized flow is to report the failed gate and stop. No other actionable defect was found in the reviewed transport implementation or the remaining semantic slots under the frozen POLICY.

## Plan Review

The bounded plan was executed through generation and independent grading: 48 fresh sources across six groups, five exposed diagnostics, three first responses each, 21 packets and 159 scheduled slots. Source/rubric review and the recorded three prospective corrections predate the preserved input freeze. Original author submissions remain provenance. Receipt-based whole-packet handling addresses the earlier preflight gap; missing or malformed packets would fail every scheduled slot. None occurred in this run. All slots were assessable.

The experiment correctly separates structural copying, semantic fidelity, mandatory ledger coverage and triplet stability. The thresholds do not demand perfection except where explicitly stated. Nevertheless, the zero-observed-material-intent-errors criterion is independently mandatory. Passing the other thresholds cannot override it.

| Fixed criterion | Observed | Result |
| --- | --- | --- |
| Zero observed material intent errors | 2 (N21 runs 1/2) | Fail |
| Fresh structure 144/144 | 144/144 | Pass |
| Fresh joint at least 137/144 | 142/144 | Pass |
| All-three fresh joint at least 44/48 | 47/48 | Pass |
| Each fresh group at least 22/24 | 24, 24, 22, 24, 24, 24 | Pass |
| Fresh meaning stability at least 44/48 | 47/48 | Pass |
| Diagnostic joint 15/15 | 15/15 | Pass |

Fresh text, semantic and binding scores are each 142/144. Fresh mandatory-ledger stability is 47/48; diagnostics have 5/5 meaning-stable and ledger-stable triplets. Overall joint is 157/159. Strict perfect fails separately. Full-object exact equality is only 2/48 fresh and 0/5 diagnostic, which is not a semantic failure criterion.

The next planned parent actions are aggregation, reporting, preservation verification and final freeze, not another generation or review. No heavy architectural pivot is needed to report this result. Future improvement work requires separate authorization.

## Author-Claim Reconciliation

| Author claim | Inspected evidence | Status and consequence |
| --- | --- | --- |
| Fixed runner parses data without generated execution and preserves first object encoding | runner.py, AST reconstruction of all 21 literals, runner tests | Confirmed for recorded artifacts; byte-for-byte standard JSON equality |
| First-save/completion checks and whole-packet accounting close preflight gap | execution.execute/load_attempt/account, execution tests, all 21 receipts and reconstructed records | Confirmed; no packet salvage or retry directories found |
| Contract is qualification1 plus ledger addition; structural transport unchanged | Exact byte concatenation; candidate.py and refinement_v3/candidate.py, base contract.py | Confirmed; no automatic semantic repair |
| 159 first outputs structurally valid and semantics pending review | Independent validation of all current outputs and full manual assessment | Structure confirmed; semantics now fail in N21 runs 1/2 |
| All protected manifests unchanged | Independent preserve.snapshot and local freeze hashes | Confirmed: 41 manifests, 38,869 overlapping protected entries |
| Tests establish transport, not semantic success | 20/8/8 executed tests and current output judgments | Confirmed distinction; passing tests do not discharge failed intent criterion |
| No feedback/repair/retry and first native submissions | Preserved literals, schedule, receipts, attempt inventory and freezes | Consistent with retained evidence; saved hashes cannot prove unseen chronology |

## Verification Performed

Read every one of the 53 source/rubric pairs and every one of the 159 saved outputs, including reasons, globals and bindings, in bounded batches. Compared all three outputs per source for information need, scope, literals, conditions and ledger meaning. Judgments are in `test-output/semantic-review.json` (159 unique source/run rows) and `test-output/stability-review.json` (53 rows). Independent gate calculation is in `test-output/reviewer-gate.json`.

Applied POLICY to avoid arbitrary exact-wording or question-count failures. Examples: redundant support clauses in N06/N35/V24 do not lose an ask; optional prospective same-field context in N28/N37/N38/K23/V04 is allowed; N34's shorter form-state ledger excerpt retains its dependency relation; N42 split literal excerpts retain both pairings. Unknown/heterogeneous/core-only globals were checked separately. N21 differs because the source and frozen rubric require the observer's method scope, not optional field context.

Independently parsed each first literal with ast.literal_eval, without executing generated content, and compared `json.dumps(..., ensure_ascii=False, allow_nan=False, indent=2) + newline` bytes against raw output. All 21 match. All attempts include first-save, completion, stdout, stderr and output. Reconstructed all records using the tested load_attempt and compared exactly to records.json. There are exactly 21 literal files and 21 attempt directories, matching all 159 scheduled slots. No production attempt was re-executed.

Verified candidate/input/round1/round2/round3/raw freezes: respectively 17/37/42/42/42/126 entries, zero mismatches. Verified inherited protected manifests by byte hashes only, including sealed evaluation; no sealed semantic contents were inspected. Verified exact contract concatenation. Ran validate/build_plan on all 159 current outputs with absent, empty and malformed optional hints; core question plans and search requests remain unchanged. Existing tests additionally cover valid and overlapping hints.

Executed:

- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/qualification_v2 -p 'test_*.py' -v`: 20 pass.
- Equivalent discovery in qualification_v1: 8 pass.
- `python3 -B poc/contextual-kb/agent_contract/v3_stress/test_assess.py`: 8 pass.
- `python3 -B poc/contextual-kb/agent_contract/qualification_v2/test-output/reviewer-audit.py`: all integrity assertions pass.

Test logs and reproducible integrity audit are `test-output/reviewer-*`. Direct source reads were used for the POC's not-tracked graph scope. No code fixes, frozen artifact rewrites, evaluation opening, additional agents or review instances occurred. A read-count tooling hook interrupted one artifact-write command before execution; repeating the permitted write succeeded without changing any qualification evidence.

## Open Questions And Residual Risks

Transport uses small standard-library components with clear parsing, reservation, accounting and integrity responsibilities. Tests cover real CLI calls, parse/encode failure, malicious expression rejection, duplicate destinations/attempts, envelope failures and corruption. This is a bounded local evidence procedure, not a hostile-input resource sandbox or tamper-proof audit service. A deliberate external actor can edit data and receipts together; saved hashes establish bytes, not unseen generation chronology.

Native model revision, temperature and seed are uncontrolled; repeats may be correlated. Authors were policy-informed and synthetic; the 48 fresh cases are development qualification, not sealed held-out evaluation. Diagnostics are exposed cases. Different fresh questions and no causal baseline prevent a causal improvement claim. No retrieval, latency, production reliability, universal compatibility or final library-answer accuracy conclusion follows. The known unrelated browser failures remain outside this review and unchanged.

## Verdict

**Not ready for experimental foundation eligibility.** The fixed qualification gate and strict-perfect gate both fail because N21 runs 1 and 2 lose mandatory method scope. The delivery implementation is verified within this local procedure, and the other numerical thresholds pass. This does not qualify promotion, runtime integration or production use.

## Recommended Next Actions

Parent should accept or dispute this finding with source evidence, aggregate the saved judgments, report the failed fixed gate and preserve/freeze the final evidence. Do not repair outputs, revise criteria, tune, salvage, regenerate or begin another review. This is instance 3 of 3; the authorized review loop is exhausted.

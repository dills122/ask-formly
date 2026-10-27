# Q1 preflight independent review

Review instance: 1 of 3

## Findings

**P2 — Enforce the actual preflight freeze before execution and evaluation.** `evaluate.py:17–22` checks only `freeze.json` and `assessment-freeze.json`, and silently skips missing files. The only current Q1 freeze is `preflight-freeze.json`. The imported `candidate.preserved()` and `checked_database()` protect completion-v1 inputs/runtime assets but do not validate Q1 cases, rubric, gate, local transport or planned calls. Thus a change to Q1 criteria or calls after this preflight could still be evaluated against three mutually identical modified runs without detecting departure from the predeclared experiment. Current hashes all match; this is an enforcement gap, not evidence of tampering. Smallest correction: require a run freeze derived from this reviewed preflight snapshot before calls, and require the final run/assessment manifests in the evaluator; test that missing manifests or changed pinned files fail. Checking the existing preflight manifest directly is also valid. Preserve continuity from the reviewed hashes to the final run freeze. Correct this before the first lookup so the run starts with an enforceable frozen contract.

The initiating author subsequently clarified that preflight-freeze.json is a review snapshot and a final freeze.json will be copied/expanded before calls; assessment-freeze.json follows assessment. That lifecycle is reasonable, but optional verification still permits missing final manifests. The author accepted a bounded mandatory-final-manifest guard with targeted tests. No architecture change is needed.

No further concrete preflight blockers identified within this bounded review.

## Plan Review

The design is appropriate for a broad source-informed evidence-usability experiment on the isolated 176-fact candidate. Cases contain exactly 160 targets plus 16 controls, balanced at 40+4 across CORE, STATE, MAT and SCHEMA. Compound flags total 129: 36/30/24/39 respectively, meeting the declared minimum in each group. The scenarios span core configuration, model/control ownership, arrays, expressions/events, validation, Material controls and schema conversion. They are not a random sample or unseen benchmark; PLAN states this correctly.

The integer criteria are correct: 144/160 = 90%; the accepted floor 143/160 = 89.375%; 142 fails. All controls must pass and critical unsupported claims fail the gate. The loader rejects incomplete/error receipts; audit rejects tool failures, altered plans/scopes, excess recovery budgets and unseen fetched IDs. Recovery requires an eligible initial result, so unsupported scope stops. Repeat reuse requires exact packet/argument equality apart from timing. A changed repeat aborts this evaluator rather than receiving a misleading reused score; a per-repeat assessment path is not implemented here.

Initial and completed assessments remain separate. Full original questions and explicit scopes match all 176 planned lookup calls. These plans measure fixed full-question retrieval and bounded recovery; they do not test autonomous caller decomposition. Candidate-only scoring and model-backed preservation limits are explicit. No production changes or DB promotion are proposed.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status / consequence |
| --- | --- | --- |
| 160 mixed targets, 16 controls, 129 compound | cases.json, per-group counts and rubric inspection | Confirmed; breadth is bounded to the authored topic set. |
| Fresh questions, no old/sealed questions used | Author statement; old questions deliberately not inspected | Unverified process claim; no claim of unseen accuracy is made. |
| Exact-plan repeats and bounded adaptive recovery | lookup-calls.json, audit.py, reused completion-v1/report.py | Confirmed design; no calls have run. |
| 20 focused tests pass, integer gates fixed | test_gate.py and unittest execution | Confirmed 20 passing tests; historical RED phase not independently verified. |
| Q1 freeze adds local/dependency hashes | preflight-freeze.json and recomputed hashes | Hashes currently match, but evaluate.verify does not enforce this manifest; finding above. |
| Candidate facts can support these rubrics | Sampled candidate-inputs/authored facts | Supported for the sample; retrieval delivery remains untested. |

Specific achievability checks included CORE key/control/merge/clone/lifetime requirements against `core-configuration-lifetime.json`; STATE parser/debounce/event requirements against `value-propagation-events.json`; MAT radio/native requirements against `material-radio-native.json`; and SCHEMA required/dependencies/defaults/tuples/composition/reference requirements against `json-schema-structures.json`. The rubrics retain the conditional limits in those facts. This was not a new audit of all pinned library source or exhaustive fact-to-rubric matrix.

## Verification Performed

- HEAD is `250f83d`; Q1 is untracked, with pre-existing dirty/untracked work outside the review scope.
- Recomputed every entry in `preflight-freeze.json`: zero mismatches.
- Confirmed target/control/compound counts and all 176 unique initial call IDs, original questions and declared scopes against cases.
- `poc/contextual-kb/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/q1-v1 -p 'test_*.py'`: 20 tests passed.
- Confirmed no qualification outputs currently exist under Q1 test-output.
- Recorded PREFLIGHT-PRELIMINARY.md before reading PREFLIGHT-AUTHOR.md.

No MCP calls, builds, inference, prior questions, sealed archives or fixes performed. Only the two authorized review reports were written.

## Open Questions And Residual Risks

Semantic usability remains a caller judgment, requiring every requested part to be supported by delivered evidence; tests cannot establish the future 143/160 outcome. Source-informed cases and closely related scenarios do not establish a whole-library success rate. Three equal repeats measure stability, not independent semantic uncertainty. The freeze check above should be fixed before any run; final review must inspect actual answers, failures, citations and receipts.

## Verdict

**Not ready** for execution until the P2 freeze-enforcement gap is corrected. The prepared breadth, controls, sampled rubric achievability and integer gates otherwise support proceeding with the stated limited experiment.

## Recommended Next Actions

Require the final run and assessment manifests in the evaluation path, add targeted missing/mismatch tests, and produce the final run freeze from the reviewed preflight inputs plus the guard correction before any lookup. Preserve cases and rubrics unless a separately documented pre-execution issue requires amendment. Return the correction to the initiating task for review disposition; no additional review instance is started here.

# Preflight review
Review instance: 1 of 3. Verdict: not_ready (reviewed pre-adjudication state).

## Findings

**P2 — Resolve gold semantics before prediction.** `data/gold-initial.json` / `data/annotate.py`, cases below. All offsets are Python codepoints, end exclusive. The empty alternatives arrays currently present contested roles/boundaries as settled truth, affecting the fixed precision gate.

| Case | Proposed adjudication | Confidence / rationale |
|---|---|---|
| P10-r1-q0 | Add api_reference `key` [58,61). | Recommended correction: the question explicitly asks about the Formly field key in relation to its model path. Unlike generic type nouns, this names the configuration property. If adjudicator regards this as generic prose, preserve that ambiguity explicitly. |
| I05-q0 | `model.needsReview` [58,75): api_reference versus value. | Ambiguous: supplied model-data dependency expression, not explicitly called a library API. Prefer value under opaque-expression wording, but complete-path wording admits another reading. |
| I05-q1 | Same disputed role for `model.needsReview` [111,128). | Must receive the same adjudication as q0. |
| P28-r1-q0 | `options.formState.busy` [150,172): reconcile with I05. | API-root path is a defensible API reference, but also a supplied dependency expression. Do not settle I05 inconsistently without explaining known API root versus model-data root. |
| P36-r1-q0 | `options.formState.region` [65,89): same reconciliation. | Same issue as P28. |
| P14-r1-q0 | Prefer version `6.2` [13,16) and `7` [18,19), replacing `>=6.2` [11,16) and `<7` [17,19). | Token-only boundary wording supports numeric tokens; comparator-prefixed range units are also plausible from current prose. Record the prospective boundary decision before predictions. Comparisons remain authoritative in full question. |
| P04-r1-q0 | Retain both registration names [72,87), [121,136); clarify narrative exclusion. | Frozen label text excludes quoted narrative *as value*, not the explicit registration mention inside it. Protocol's shorter “Quoted narrative excluded” is broader. Clarify that no value span is emitted for the enclosing narrative; retaining the embedded explicit name is defensible. |

The role reconciliation can either adopt a justified prospective rule (known Formly API-root paths are APIs; supplied bare model-data expressions are values), or retain explicit api_reference/value alternatives for all disputed paths. The latter requires pre-inference alternative scoring support. This review does not assert that frozen wording uniquely mandates value for I05. No gold was changed.

**P2 — Missing extraction attempts are counted as empty successful predictions.** `assessment.py:49-56` initializes raw predictions for every question before checking extraction coverage. A model-arm row with a missing extraction entry on a gold-empty question gets `missing=false`, can get `exact=true`, and adds no extraction error. An otherwise accurate run can pass the advisory gate despite omitted work; duplicate or unexpected extraction question indexes are also not rejected. Require exactly one extraction entry per question for model arms, none for foundation, with valid unique index and matching question text, plus consistent error/raw accounting. Missing attempts must block the value gate and remain visible in denominators. Add an end-to-end assessment regression rather than only testing `metrics` with a missing dictionary key. Parent accepted this finding; pending remediation was not reviewed here.

## Plan review

The bounded three-arm design matches the stated integration objective: immutable foundation and adapters, original questions as authoritative search input, no retrieval or answer-quality claims. Inference is sequential and offline, with separate import/load/extract/projection timing. Safety and both per-model value gates are distinct. Repeated saved outputs are explicitly correlated. All 174 core records validate; extraction panel contains 44 rows including two no-question controls. Empty question controls never invoke the extractor. Gold-empty *real questions* remain meaningful false-positive controls.

Readiness still requires gold adjudication, corrected scoring coverage, and a completed run-freeze including final inputs, gold, scorer/tests and existing dependencies. `assessment.main` currently rejects alternatives, but that rejection occurs after extraction if only the scorer is invoked later; if alternatives remain, implement support and validate before run. No architecture pivot or expanded scope is needed.

## Gold row coverage

Every initial row was manually read against exact question text, narrow_contract/CONTRACT.md and pilot/labels.json. All source spans match text, are source ordered and nonoverlapping. The following rows have no additional semantic objection beyond the table above:

P02, P06, P08, P12, P16, P18, P20, P22, P24, P26, P30, P32, P34, P38, P40, P42, P44, P46, P48 (each run1 q0); I01-q0/q1; I02-q0/q1; I03-q0/q1; I04-q0/q1; I06-q0/q1; I07-q0; I08-q0; I09-q0/q1; I10-q0; I11-q0/q1; I12-empty.

P02/I01 generic type nouns and P06 generic type noun are properly omitted. P12 ordinary label noun is not explicit props.label. P26 whole comparison expression is one value without nested fragments. P44 hypothetical API spelling is included without the surrounding prose quotes. I04 assigns the identical quoted text different occurrence roles. I08 avoids a nested name inside the complete validation.messages path. I09 retains both repeated hypothetical API occurrences. I07 includes both named adapters without selecting the negated one as active scope. P48 and I12 preserve no-question abstention.

## Fresh foundation semantic assessment

All 12 first outputs were reviewed independently; no material semantic failure found. These are single-run assessments, not repeatability qualification.

| Request | Assessment of questions, constraints, ledger |
|---|---|
| I01 | Registration and use both retained; version/Material and formatting exclusion bind both; taxId key binds use; prospective registration stage is clear. |
| I02 | Support and information questions retain disabled transition and nonpolling observer restrictions in text and ledger. |
| I03 | Comparison retains resetOnHide=false; independent default-value question retains undefined scenario; v6 scope applies to both. Minor grammar does not change meaning. |
| I04 | Registration versus use preserved; wrapper name versus field key stays distinct; key condition binds use. |
| I05 | Support check and conditional configuration preserved; controlling dependency and manual-subscription exclusion bind both; explicit If supported binds follow-up. |
| I06 | API exposure question separate from type registration; no-model-change restriction remains local to registration. |
| I07 | Bootstrap selected globally while Material exclusion survives in question/ledger; requested literal and retained key remain paired. |
| I08 | Explicit comparison retained, whole configuration path unchanged; redundant grounded comparison ledger is harmless. |
| I09 | Existence asked directly; arguments lookup remains conditional and no-existence-assumption restriction is preserved locally. |
| I10 | defaultValue:0 and null-model state retained; explicit application-loader exclusion remains present and bound. |
| I11 | Enabled-only value-change observation and no-polling restriction retained on same observer and stop operation; destruction timing binds stop. |
| I12 | Application ownership/location request correctly abstains, with empty questions and ledger and null constraints. |

## Author-claim reconciliation

The preliminary file was saved before opening AUTHOR-EXPLANATION.md. Later additions (assessment.py, test_assessment.py, preserve.py) were declared by parent and reviewed before inference.

| Claim | Evidence | Status |
|---|---|---|
| Foundation projection is unchanged and hints advisory | integration.integrate; qualification_v3 import; refinement_v3 build_plan/optional_hints; tests | Confirmed for inspected implementation and synthetic checks. |
| Native spans are not repaired and semantic mistakes stay observable | map_hints and wrong-role test | Confirmed. |
| 174 inputs and 44 annotations | records/gold checked directly | Confirmed. |
| 13 then 18 tests pass | Reviewer executions | Confirmed. |
| Scorer reports typed/untyped metrics, per-role/new-panel scores, filtering losses and timing | assessment.py | Confirmed with extraction-coverage defect above. Null empty precision/recall is correct; missing nonempty gold produces FN. |
| Local immutable adapters, inference-only setup, before/after hashes | run.py source | Implementation confirmed; actual model load/runtime behavior deliberately unexecuted. |
| Protected prior artifacts unchanged | preserve.py wrapper and parent hash audit | Wrapper inspected; recursive protected audit result remains parent evidence, not independently executed here. |

## Verification performed

- HEAD verified c3091328f49d53de6b41a49c4fe5aa8f1c45e516; dirty root state excluded.
- `python3 -B -m unittest discover -s /Users/dsteele/repos/ask-formly/poc/contextual-kb/agent_contract/gliner_integration_v1 -p test_integration.py -v`: 13 pass.
- Same command with `-p 'test_*.py'`: 18 pass.
- Read-only Python check validated all 174 foundation objects, all 44 gold rows' exact slices, and design-freeze hashes.
- Graph coverage for 10 relevant Python files is not_tracked (October16 generation); direct source inspection used, no reindex.
- No model inference, candidate mutation, DB access, sealed evaluation semantic read, staging, or commits.

## Open questions and residual risks

Real native extractor envelope compatibility and model loading are not established by mock tests; runtime failures must be retained in execution evidence. The fixed value thresholds are engineering gates, not production guarantees. Scorer schema robustness beyond expected native outputs is limited. Single-run timing cannot establish latency SLA. No independent statement about all protected bytes is made beyond verified design-freeze hashes and cited parent audit.

## Verdict

not_ready for inference in the reviewed state. This is a bounded preflight correction/adjudication gate, not rejection of the integration design. Parent should record accept/dispute/defer for each finding, preserve this initial review, complete the finite corrections and gold adjudication before input freeze, and retain completed-results review within the total three-instance budget. Do not infer a new ready verdict merely from the passing unit tests.

## Post-review author update (not reverified)

Before this review returned, parent reported prospective gold adjudication saved separately in ANNOTATION-ADJUDICATION.md and gold.json (initial gold preserved): P10 key added, P14 numeric-only versions, P04 names retained, I05 value using the explicit known-configuration-root versus model-data convention with ambiguity acknowledged. Parent also reported extraction sequence/text/evidence/time validation and 21 passing tests after a failing regression. These are remediation claims, not checks executed by this reviewer; the verdict describes the original reviewed state. Because scorer behavior changed materially, independent fix verification is warranted as instance 2, leaving instance 3 for completed-results review.

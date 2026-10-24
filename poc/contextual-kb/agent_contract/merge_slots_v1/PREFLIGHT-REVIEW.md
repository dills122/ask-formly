# Preflight independent review

Review instance: 1 of 3. Verdict: **Ready for the isolated experiment.** This is experimental-integrity readiness, not promotion. Full-pipeline qualification is already blocked by retained M36 input semantics.

## Findings

No unresolved implementation blockers. Two reporting omissions found during this pass were corrected before acquisition: per-request/arm missing required groups at 4/8, and protected-versus-current paired group changes at 4/8. Tests were added and passed. No generated question, model, prior candidate, DB, or retrieval result was repaired.

**Retained semantic failure — M36, foundation question_index 1.** The source asks about turning configuration into a *server-side SQL schema* and migrating the database. The standalone migration follow-up loses that server-side SQL referent and has no binding preserving it. Its supplemental query faithfully rewrites the saved foundation question, so supplement_pass remains true relative to its actual input; the inherited loss remains visible and blocks full-pipeline qualification. Foundation: 35/36 pass. Supplements: 36/36 pass against saved plans. Reviewed all 46 individual question/supplement pairs. Different decomposition by itself was not rejected under the frozen interpretation policy.

## Plan review

The three paired arms use shared acquired query rankings. Fixed six-prefix protection, current-fusion ordered fill, original fallback, unique eight-slot budget and no outside candidates match the prospective protocol. All selected supporting facts remain recall gold; required groups encode minimum requested aspects with OR substitutes. The labels cover 36 requests against all 46 facts: 30 direct, 6 unsupported, no partial requests identified. Conditional support such as M28 remains conditional; direct does not assert a universal rebuild guarantee.

Fact-level safety catches a lost baseline relevant fact even if aggregate recall or required-group completeness survives. Utility requires a gained fact, at least 0.5-point pooled recall gain, no batch recall regression and no precision loss. The 89.25% consistency floor and 90% diagnostic are checked in every batch and pooled. Empty unsupported gold does not inflate recall. All arms/cases and errors are retained; missing/duplicate coverage fails scoring.

Shared acquisition and combination elapsed times are retained separately. Acquisition includes the frozen contextual candidate's existing fusion overhead; it is not pure engine time. Per-arm summaries report logical query counts/characters, with no independent end-to-end speed claim. Both augmented arms share logical query cost.

Exclusive output creation prevents overwriting first retrieval artifacts. Design/generation/run manifests are checked before and after acquisition; packet traces are frozen before scoring. SQLite uses the existing read-only/query-only helper. Policy/acquisition receive no labels. Final runtime freeze is the initiating author's next required step and is enforced by the runner; this review does not claim that not-yet-created freeze has already passed.

## Author-claim reconciliation

| Claim | Evidence | Status |
|---|---|---|
| Fixed gold-blind six-prefix policy | policy.py, protocol, randomized independent checks | Confirmed |
| Original/supplement rankings acquired once | acquisition.py, frozen contextual candidate, mocked acquisition tests | Confirmed |
| Frozen current fusion unchanged | existing RRF/interleave source, acquisition parity assertion | Confirmed |
| Strict losses and batch floors | metrics.py, tests and independent batch-floor probe | Confirmed |
| Semantic failures separate from merger performance | semantic-review.json, scorer qualification predicate | Confirmed |
| 20 tests pass | Final reviewer run now 22 tests after reporting fixes | Superseded by stronger current evidence |
| Prior artifacts immutable | Byte-only preservation snapshot equals protected-before; 46 manifests | Confirmed at preflight |
| Fresh native contexts/no repairs | Retained first-save literals, generation hashes, author account | Artifact integrity confirmed; context provenance not independently attested |

## Verification performed

- `python3 -m unittest discover -s poc/contextual-kb/agent_contract/merge_slots_v1 -p 'test_*.py' -v`: 22 pass; retained in test-output/preflight-tests-final.txt.
- Independent test-output/preflight-independent.py: 2,500 randomized policy cases; bounded unique sourced candidates; exact first-six prefix and fusion-ordered fill; whole-record invalid-supplement fallback; 36 request/gold/semantic identities; 46 facts and questions; all design/generation hashes. Also verifies a pooled score over 90% cannot hide a failed batch floor, runtime errors block qualification, and no elapsed per-arm timing fields remain.
- Preservation snapshot: all 46 prior manifests unchanged, hash-only; retained in test-output/preflight-preservation.json. No sealed semantic access.
- Design freeze: 8 entries match. Generation freeze: 7 entries match. No retrieval directory existed at review completion.
- Base HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516 on existing dirty workspace. Scope is this new experiment directory; unrelated dirty files excluded.

## Open questions and residual risks

The six-prefix rule can displace useful facts in slots seven/eight. Strict paired safety will expose that outcome. Thirty supported synthetic requests over one 46-fact catalog cannot establish population accuracy or held-out-topic generalization. Label judgments are prospective and include corroborating facts, not only minimal answer facts; retrieval outcomes must not motivate label edits. M36 stays in the trial and must be reported.

Graph coverage checked for relied-on POC code: all reported not_tracked under the October 16 generation. Direct source inspection used; no reindex. The unchanged structural validator and engine are frozen dependencies, not newly qualified library implementations.

## Verdict and next actions

Ready for experimental integrity once the required run freeze is created. Run once, preserve all results and failures, verify prior preservation afterward, and use completed review instance 2 without live reruns. Do not tune six, labels, question text, or criteria after outcomes. Exact reviewed code, input, label and manifest SHA-256 values are recorded in PREFLIGHT-DECISION.json.

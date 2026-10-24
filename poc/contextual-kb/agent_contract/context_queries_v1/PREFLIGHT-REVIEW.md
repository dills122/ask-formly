# Independent preflight review

Review instance: 1 of 3.

## Findings

No blocking experimental-integrity defect found. Ready to execute the bounded paired experiment after the planned runtime/input freeze. This is not candidate qualification or promotion.

Two candidate semantic failures remain in the first outputs and must be scored:

- C11, foundation Q0: the question preserves “in IndexedDB”, but condition_bindings contains only “between visits” and “without application persistence code”. The frozen qualification_v3 contract's Mandatory ledger completion audit requires the supplied method/channel to bind; prose alone is insufficient. IndexedDB specifies the persistence channel, not merely a bare target API. This is a ledger omission, not an assertion that Formly supports persistence.
- C09, supplemental Q1: the original asks “who handles teardown when the field is destroyed?” under the separate “if onInit returns an Observable” condition. The supplement reads “Identify who handles teardown in Formly if onInit returns an Observable when the field is destroyed.” The adjacent final temporal clause now admits attachment to returning the Observable, weakening the original unambiguous teardown timing. The supplement contract requires preserved relationships/event ordering, including unbound conditions; exact copies alone do not discharge this. This is an ambiguity introduced by rewriting, not evidence about Formly lifecycle behavior.

No first-output changes were made. All other 34 case reviews pass both semantic assessments; C09 foundation and C11 supplement pass their respective local contracts. Semantic review covers all 36 plans and all 49 supplements. cases.json contains 26 direct, 4 partial and 6 unsupported requests, with 72 relevant fact memberships. Partial cases C05, C25, C27 and C34 disclose missing implementation/lifecycle/expression/path semantics. Unsupported capabilities have empty gold rather than borrowing merely related formState or expression facts.

## Plan Review

The frozen protocol and implementation agree on two paired arms over the same plans, unchanged original full-question hybrid top8, at most one supplemental query per derived question, unchanged imported RRF then merge_obligations top8, and duplicate-query suppression. Invalid supplemental structure falls back for the whole record and stays an explicit error. Foundation errors yield retained empty results. Semantic failures are retained without changing retrieval selection.

All cases/arms and batch identities are validated. The utility gate requires the declared recall gain, precision nondecrease, no batch recall regression, no paired complete-group loss at8, no increased unsupported exposure, and no semantic/runtime failures. Top4 losses remain visible. Fixed-k precision and AND-of-OR group scoring come from the reused bridge. Summary precision is macro precision over supported cases; unsupported exposure is separately reported. The final report must state this denominator.

Read-only SQLite uses URI mode=ro and PRAGMA query_only. PilotIndex computes transient ordinary fact vectors with existing local artifacts and local_files_only=True. No engine, ranker or database changes were introduced. Exclusive first-run output and hash checks retain incomplete attempts rather than replacing them. No retrieval or model inference ran during review.

## Author-Claim Reconciliation

| Claim | Evidence | Status |
| --- | --- | --- |
| 36 requests, 49 questions, unchanged generation | Requests, records, generation/design manifests | Confirmed current bytes and counts |
| First native output only, fresh isolated generation without catalog | Saved literal/attempt artifacts and author testimony | Current artifacts retained; historical context isolation not independently replayed |
| Original query retained, same RRF/merge and budget | candidate.retrieve, imported question_pilot helpers, unit tests | Confirmed |
| Failed cases cannot disappear; paired/batch/semantic gates | assessment.validate_coverage/assess, run.main, tests | Confirmed |
| 17 unit tests pass | Independent unittest execution | Confirmed |
| 45 prior protection manifests unchanged | preserve.snapshot compared with protected-before | Confirmed, hash-only |
| Runtime cache/dependencies and final inputs frozen before execution | Planned parent step, run.verify | Pending by design; completed review must verify actual freeze and execution |

## Verification Performed

- Read tests before implementation and recorded PREFLIGHT-PRELIMINARY.md before AUTHOR-EXPLANATION.md.
- Ran PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_candidate test_assessment: 17 passed. A shell startup parse warning appeared; unittest exited successfully.
- Verified seven design and seven generation manifest entries: no mismatches.
- Recomputed all 45 prior protected-manifest results: identical to protected-before.json. Sealed artifacts were hashed only.
- Validated 36 unique label rows against all 46 catalog IDs, nonempty required groups within relevant sets, 49 questions, and 36 semantic reviews.
- Saved machine-readable checks to test-output/preflight-checks.json.

Graph coverage dated October 16 reports these POC paths not_tracked; all relied-on code was inspected directly. No graph completeness claim or reindex.

## Open Questions And Residual Risks

Runtime execution, actual embedding-cache identity, final transitive dependency freeze, 72 trace records and postrun preservation remain for the parent and completed review. Unit tests use a fake index and do not prove live retrieval. Small synthetic cases and subjective relevance boundaries do not support population-level precision claims. Per-case partial gaps remain outside supported-recall denominators. C09's introduced attachment ambiguity is conservatively counted as a semantic failure; retaining its text and rationale makes this judgment auditable.

## Verdict

Ready for the experiment, with semantic failures C09 and C11 retained. Utility qualification cannot pass these first outputs. Freeze labels, semantic review, code and actual runtime dependencies before running once; completed review is instance 2 of 3. No further reviewer was spawned.

## Recommended Next Actions

Complete the planned freeze and execute once. Report all paired results and explicit semantic failures, unsupported exposure and partial gaps. Do not repair outputs or select passing cases. Verify traces, calculations, final freeze and preservation in completed review.

Prospective label challenge resolved before predictions: C08 now requires the modern callback/model fact only; legacy callback facts remain relevant but no migration comparison was requested. C15 requires model-value removal only: array child-field clearing remains relevant but does not by itself establish deletion of child model values. C18 requires the input-inheritance example only, which already covers renderer reuse with defaults. No relevance IDs were removed. This avoids splitting corroboration into artificial independent obligations.

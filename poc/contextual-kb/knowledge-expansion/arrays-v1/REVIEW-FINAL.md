# Arrays independent outcome review

Review instance: 2 of 3, continuing the same source/prebuild review. Scope: untracked arrays-v1 additions against HEAD `39957158b18c040aae87a58a6fa9fcd58ec0a814`. Installed foundation6 remains 79 facts / 17 documents. No promotion, staging or commit was performed.

## Findings

**P2 — The fixed integration qualification fails a required control, delivery and regression gate.** Repeat 2 candidate Q20 did not produce a successful lookup. The saved audit `test-output/qualification-1/r2-b3-candidate/mcp/audit/cf4efc4f37c846b3a0688f04a4e6bd60.json` records `ValueError: condition not grounded in source`. The actual tool item is failed with null structured content. The caller honestly declines the requested typing answer, although its explanation of a JSON parsing error is not the true underlying cause. Baseline Q20 in the same repeat succeeds. This single event therefore fails three frozen requirements: complete delivery, all controls passing, and no baseline-supported regression. Meeting the numeric 14/15 threshold does not override them.

The failure occurs in the unchanged planner/validation path before retrieval. Saved planner attempt `8ec371824b9247c6a89fd54eb8a9b007` is valid JSON but binds lowercase `an internal Formly source file exports TypeOption` where the original request starts uppercase `An`, and supplies `question_indexes: []`. The preserved validator rejects the exact-substring mismatch at `agent_contract/refinement_v3/candidate.py:19`; empty indexes independently violate line 22. A reviewer diagnostic using only the saved plan reproduces the first error, and a capitalization-only change to a deep copy still raises `invalid question indices`. No accepted replacement plan was synthesized. The questions retain the internal-export concept in paraphrase; this is not evidence that arrays facts are incorrect or absent.

The smallest current correction is to retain the failed qualification and keep the candidate isolated. Any runtime remediation requires separately scoped work and a new fixed qualification, preserving this failed run. Do not change arrays facts, retry this case into a pass, or characterize a capitalization-only adjustment as sufficient.

No remaining defects were found in the reviewed source mappings, isolated build or preservation checks. The pre-freeze mapping/documentation findings are closed in REVIEW-1.md. The runtime failure is exposed by this comparison, not introduced by a runtime edit in this batch.

## Plan Review

Source verification, bounded authoring, independent prebuild review, isolated build, row preservation, eligibility, freezing, reproduction, fixed comparison, grading and independent outcome audit were completed. The success gate did not pass. Promotion remains excluded.

All 90 live answers were independently read against the frozen requests, source claims, conditions, limits and returned citations. Results agree with the automated assessment:

| Repeat | Baseline usable | Candidate usable | Candidate controls |
| --- | --- | --- | --- |
| 1 | 5/15 | 15/15 | 5/5 |
| 2 | 5/15 | 14/15 | 4/5 |
| 3 | 5/15 | 15/15 | 5/5 |

Candidate targeted-array answers passed 30/30; baseline targeted answers passed 0/30 because they correctly disclosed missing array-specific support. Baseline controls passed 15/15. Candidate total is 44/45 versus baseline 15/45. There are zero critical invented Formly behaviors and one failed candidate delivery/control. No missing denominator was removed. Per-batch reviewer judgments are retained in `test-output/audit-progress.md`.

A08 is an explicit accepted interpretation: the exact upstream assertion is `field.model` equal to `['default', null]`. All three candidate answers present `{foo: ['default', null]}`. This was accepted as the root-model representation for the user-specified keyed fixture because contents/order and the inspection-only limitation are correct, and none identifies that object as `field.model`. The source assertion and caller representation must not be conflated. No rubric or case was rewritten.

The 45 directional replay slots yielded 44 successful packets: 15, 14, 15. Repeat 2 Q20 has no successful source plan and remains explicitly missing. Every actual replay retains exactly its saved source plan. The candidate targets in repeats 1 and 3 contain all indicated supporting IDs for their 15 requests; the baseline target in repeat 2 contains them for four of fourteen completed controls/requests. Those are ID diagnostics, not additional final answers or an accuracy score. In particular, a valid baseline Q20 plan retrieves the public-registration-type fact from the candidate, supporting localization to the failed live planner contract without waiving the failed gate.

## Author-Claim Reconciliation

| Claim | Evidence inspected | Status and consequence |
| --- | --- | --- |
| Six upstream sources verified | Reviewer independently hashed full retained files against catalog and read implementation/example/test spans | Confirmed; no upstream suite execution inferred |
| Six additions produce 85 facts / 19 documents | Drafts, isolated DB, manifest and independent temporary rebuild | Confirmed |
| All accepted rows preserved | Full-row set comparison across documents, facts, evidence, fact_evidence and fact_links | Confirmed |
| Candidate eligible and reproducible | Eligibility rerun, exact five-table independent rebuild comparison | Confirmed; not answer-quality proof |
| Candidate 44/45 and targeted 30/30 | All 90 answers, delivery validation, returned citations and frozen grader output | Confirmed, including recorded A08 interpretation |
| Integration qualification failed | Frozen evaluator rerun in memory and retained decision | Confirmed: Q20 delivery/control/regression failure |
| 44 actual replays, one missing source | Every replay result and corresponding saved source plan | Confirmed; denominator remains 45 |
| Installed assets and frozen inputs unchanged | All 167 protected pins, 28 freeze entries, DB hash, source hashes and successful packet integrity fields | Confirmed at closeout |
| Maintenance passed | Parent's retained local-maintenance log ends with successful checks | Confirmed from log, not rerun by reviewer |

The author explanation was read after the independent implementation/source pass. Later author summaries were checked against raw artifacts; reviewer judgments do not rely on process exit zero or required-ID presence alone.

## Verification Performed

- Reviewer ran all 16 arrays unit tests and combined 19-document compiler lint: passed.
- Independently verified the six upstream full-file hashes, source claims and exact fixture boundaries before build.
- Independently reproduced the candidate into a temporary database and compared every row in all five knowledge tables. Candidate counts: 19 documents, 85 facts, 51 evidence records, 130 fact-evidence rows and 81 fact links.
- Candidate SHA256 remains `bbb55e168cc81e60927a1bf146af767cd8ab6c9999875239ea28a879487531ff`; installed DB remains `226c377ecb4a8a220c5c6db541156c3dcad71045d73b21a5d205fbf164b7715b`.
- Reran non-hosted assessment preparation for all 18 caller batches, checking exact sequential calls, returned packet versus audit, answer IDs and citations. There are 90 delivered answer records, 89 successful live packets and the one retained Q20 failure.
- Independently checked every one of the 44 replay packets for success, correct source/target arm, exact saved plan and expected case identity. Verified all fact claim/context/condition/limit payloads across all 133 successful live/replay packets match reviewed authored records.
- All 133 successful packets report unchanged DB and model parameters. Global closeout hashes verify all 167 protected files and all 28 frozen artifacts remain unchanged. The failed request has no successful packet and is not counted as an integrity report.
- Frozen evaluator returns `qualified:false` with precisely the three Q20 consequences described above; automated grades match the independent answer audit.
- Read the retained maintenance log: 128 source tests, 114 runtime tests and 86 doctor checks passed. Reviewer did not repeat the parent's full maintenance command.
- Read the diagnostic closeout script and checked its results independently. Ten successful live packets report degraded advisory extraction, and one live selection was repaired; these are retained diagnostics, not hidden failures or proof of broad reliability.
- Graph coverage for new/ignored artifacts is unavailable; source and generated evidence were read directly. No claim depends on complete graph coverage.

No hosted reviewer run, upstream Angular test, installed write, sealed-evaluation access or source/model retuning occurred. The only reviewer plan variation was an in-memory failure diagnostic; saved production artifacts remain unchanged.

## Open Questions And Residual Risks

The existing planner can generate invalid condition bindings despite valid JSON. This run establishes one observed failure, not its frequency or a complete runtime fix. The exact source additions are promising, but the declared end-to-end qualification failed. Concurrent repeats preclude comparative latency claims. Visible targeted cases do not establish unseen whole-library accuracy, earlier/later version compatibility, a verified Material repeater or application runtime behavior. The fixture-specific test question measures knowledge of inspected source assertions.

## Verdict

**Not ready — fixed integration qualification failed.** Source mappings, isolated compilation, preservation and candidate reproduction passed. The candidate remains isolated; it must not be labeled qualified or promoted on this evidence.

## Recommended Next Actions

Retain this candidate and all failed-run artifacts. Close the current arrays qualification honestly. A separately authorized runtime investigation may address condition-binding generation/validation and then define a new frozen qualification; no further reviewer instance or workstream is started here. This remains review instance 2 of 3, with no reset of the review count.

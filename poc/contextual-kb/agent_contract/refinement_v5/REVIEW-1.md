# Independent review of v5

Review instance: 1 of 3. Verdict: **Ready** for the bounded development-panel evidence claim. No production qualification implied.

## Findings

No actionable findings in the reviewed implementation or the 48 frozen responses under the predeclared v5 policy. All 48 question/reason/scope outputs pass semantic review and all 48 ledgers pass binding review. All 16 cases retain equivalent question meaning across three runs, assessed separately from equivalent ledger meaning/attachment. Exact JSON equality is not the criterion.

Results separated by provenance:

| Panel | Semantic | Binding | All three usable | Question stability | Ledger stability |
| --- | --- | --- | --- | --- | --- |
| Fresh N01–N12 | 36/36 | 36/36 | 12/12 | 12/12 | 12/12 |
| Exposed diagnostic G01–G04 | 12/12 | 12/12 | 4/4 | 4/4 | 4/4 |
| Combined | 48/48 | 48/48 | 16/16 | 16/16 | 16/16 |

Every source request, question, reason, global scope and binding was read; row-specific rationale is in test-output/semantic-review.json (48 rows). Separately assessed question and ledger equivalence is in test-output/stability-review.json (16 rows). Structural validation alone was not used to discover source omissions.

Boundary judgments were made against the frozen policy, not a stronger post-generation rubric:

- G01 all runs: source `if it does` is a meaningful elliptical eligibility excerpt; the standalone question resolves it to props.persistHiddenValue existence. Eligibility binds only the meaning lookup, independently of the shared no-substitution exclusion. G02 and N01–N03 likewise preserve source gates in both dependent questions and ledgers without self-gating the support checks.
- G03 and N06 all runs: return-transition excerpts preserve showing again and the later FormControl outcome. Duplicating earlier hiding is optional under v5; no v4 local-only history scoring was applied. N05 preserves its explicitly mandatory earlier-hide prerequisite, setting and return-only exclusion.
- N07 run1 generalizes field subject labels but retains the independently specified library scenarios and correct local attachments. Those names are not requested configuration values. Runs2/3 retain the names. Run3's nonsequence explanation mentions the other subject only to deny coupling; it imports no other-field event, API setting or prerequisite.
- N02 runs1/2 redundantly bind the source request to keep the support check independent. The rubric correctly says this is an attachment clarification rather than a new Formly scenario. It is a source-grounded restriction on interpretation, and attaches to the ungated support question without changing its meaning. The frozen rules do not require a minimal ledger or forbid restating an applicability clarification. It is not a JSON/response-format requirement. Run3 preserves the same independence through the actual gate attachment. Therefore these are equivalent, not two posthoc binding failures. The preliminary concern is resolved on that basis.
- N08 run1's extra observing-only sentence duplicates the local no-polling attachment; it never restricts configuration. N10's separate versus combined scope excerpts likewise differ only in segmentation. All active constraints remain covered.

## Plan Review

The six-step task_plan.md matches the implementation boundary: a new candidate prompt, unchanged v3 schema/transport, fresh authoring plus exposed diagnostics, six generation batches, independent review, and final preservation/reporting. This review completes the review evidence; final report/freeze remains the initiating task's documented closeout step. No requirement to add a semantic detector or integrated production path was inferred.

The eligibility/history policy is coherent and distinguishes mandatory gates and explicit prerequisites from optional same-field history. Fresh coverage exercises unless polarity, retraction, shared setting, unrelated fields, local observation restriction, completed setup, split scope, empty and no-condition controls. Diagnostic coverage specifically checks earlier failure cases under the explicitly changed policy. These cases do not establish general accuracy or causal improvement over v4, and no new comparison arm was claimed.

Engineering review: candidate.py is a small prompt selector delegating to the frozen v3 validator/projection. The dependency direction stays inside the existing POC. Tests cover invalid input, verbatim user transport, exact declared gates, strict JSON, old plans and hint isolation. The retained omission test establishes the validator's limit instead of hiding it. No new runtime data source, application execution, detector, repair workflow or dependency was introduced. Existing quadratic hint-overlap processing is inherited and bounded by these small plans; it is not a new regression or a production performance claim.

## Author-Claim Reconciliation

The preliminary report was written before AUTHOR-EXPLANATION.md was read. This reviewer received the bootstrap and bounded assignment, without the implementation conversation.

| Claim | Evidence | Status and consequence |
| --- | --- | --- |
| v5 prompt selection with frozen v3 transport | candidate.py, refinement_v3/candidate.py, contract.py, test_candidate.py | Confirmed by direct source and tests; no schema or detector change. |
| Derivation/output unchanged; ledger inserted | Compared CONTRACT.md sections with v4 and LEDGER-RULES.md | Confirmed byte-for-byte for those sections. |
| Seven tests and prior v4 regression pass | Both unittest commands rerun | Confirmed 7/7 each. |
| Initial missing-module failure retained | test-output/red.txt | Confirmed recorded failure; file alone cannot prove historical execution order. |
| 15 frozen inputs and six raw batches / 48 slots | input-freeze, raw-freeze, cases, batches, records | Current hashes and complete reconstruction confirmed. Unseen generation attempts and delivery context are not provable from files alone. |
| Prior artifacts preserved | preserve.py and inherited audit/verify, protected-before | Confirmed 32 manifests, 38,295 entries with overlap possible, including v4 final-freeze47. |
| No semantic guarantee or production qualification | Protocol and executed omission test | Confirmed; the positive result is a finite development-panel observation. |

Authoring isolation and first-response history are described consistently with the packets, but not independently established solely by hashes. Native role context separation is not vendor independence. These limits remain explicit and do not become hidden claims of controlled provider reproducibility.

## Verification Performed

Repository: /Users/dsteele/repos/ask-formly, branch main, HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516, dirty working tree with unrelated changes. Review scope is refinement_v5 plus direct read-only imported implementation needed to verify it. No staging, commit, fixes or edits to code/data/raw output occurred.

- In refinement_v5: `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_candidate` — 7 tests pass.
- In refinement_v5: `python3 -B preserve.py` — all 32 protected manifests pass; current snapshot equals protected-before.json. Sealed/data/weight artifacts were only byte-hashed by preservation code, never semantically inspected.
- In refinement_v4: same unittest command — 7 tests pass.
- Independent Python verification: SHA-256 checks pass for input-freeze (15 files), raw-freeze (6 files) and wave1-freeze (3 files). Reconstructed records from all six raw files equal records.json exactly; each batch contains its eight expected IDs, all 48 id/run slots unique and present.
- All 48 v5 outputs pass candidate.validate and build_plan; missing, malformed, valid and overlapping optional hints preserve question_plan and search_requests, and inputs remain unchanged.
- Independently verified unchanged derivation/output prompt sections and insertion of the exact v5 ledger text.
- Graph coverage for the seven relied-on Python files reported not_tracked. Complete direct source reads were used for those files; no graph-completeness claim.

No test or semantic failure was observed. The initial login shell printed a startup `parse error near end` diagnostic before successfully executing both requested checks; explicit non-login subsequent verification succeeded. A tool hook transiently blocked one consecutive-read command; it was retried successfully, with no missing review evidence. These are environmental/tool observations, not suppressed candidate failures.

## Open Questions And Residual Risks

The panel is synthetic, small, and correlated within eight-request batches. Repeats have no pinned provider revision, seed or temperature. Hashes prove preservation, not chronology or absence of unseen attempts. The structural validator accepts undeclared omissions by design; production consumers must not mistake this passing panel for a mechanical semantic guarantee. Generalization, retrieval, answers, latency and sealed qualification remain outside scope. Existing repository browser failures were neither exercised nor reclassified by this bounded POC review.

## Verdict

**Ready.** Evidence/code readiness passes. Separately, the complete frozen candidate gate also passes: all 16 requests are semantically and binding compliant in all three runs, with question meaning and ledger equivalence each stable for 16/16. This approves the bounded v5 development evidence, not production deployment or broad accuracy claims.

## Recommended Next Actions

Complete the planned final preservation audit/report/freeze while preserving these reviewed raw responses and grades. Report fresh and diagnostic results separately with the above limitations. No material fix or replacement review is required, and this reviewer starts no further instance.

# Independent review of frozen v3 stress evidence

Review instance: 1 of 3. Scope: the working-tree evidence/harness in `poc/contextual-kb/agent_contract/v3_stress`; frozen v3 is an evaluated dependency, not a proposed implementation change. Preliminary observations were recorded in `REVIEW-1-preliminary.md` before reading the author explanation. No inherited implementation conversation or author rationale was supplied in the review task. Only review artifacts were written.

## Findings

**P2 — The candidate does not consistently produce complete condition audits.** The clearest example is `test-output/b2-r3-raw.json:139` (S12 run3): the only binding is `if it does`. Both search questions preserve the no-substitution exclusion semantically, but neither has its explicit exclusion represented in the ledger. Runs1/2 do bind it. The frozen contract's shared-condition audit explicitly requires relevant exclusions in both text and binding list. This is a binding-only failure, not lost search meaning or an erroneous Formly answer. Smallest future correction would retain a meaningful source exclusion excerpt and assign it to both questions; do not repair the frozen response or candidate during this test.

**P2 — Two repeated audit omissions under the contract's broad condition interpretation.** S16 all three runs (`test-output/b2-r1-raw.json:115`, corresponding S16 binding arrays in runs2/3) bind the reset alternatives and unresolved conflict but omit the hiding circumstance. S17 all three (`test-output/b3-r1-raw.json:9`, corresponding first records in runs2/3) bind only version/adapter, omitting dependence on `model.needsPermit`. The questions themselves preserve these meanings. My primary binding grades count these six omissions, because hiding supplies the circumstance for the model-value outcome, and the model source limits the required-state configuration. This follows the contract's audit of every applicable condition, not an assertion that the frozen rubric explicitly enumerated these ledger entries.

**Interpretation sensitivity:** S16's rubric emphasizes the uncorrected conflict and S17 lists only version/adapter under shared conditions; it describes the dependency as the requested aspect. It is therefore defensible to classify these as requested operations rather than separately audited conditions. The primary strict interpretation yields 65/72 binding passes and 21/24 all-three-pass cases. Exempting both borderline categories yields 71/72 and 23/24. The clear S12 omission remains and the candidate still fails the all24/all3 decision gate. This sensitivity must accompany the primary aggregate; do not present 65 as an interpretation-free oracle. S04's `routeBadge` is the requested target name rather than a conditional assignment, so its absence as a separate binding in run2 was not penalized.

No blocking harness or evidence-integrity defect found in the frozen inputs and nine raw files. Honest negative candidate evidence remains useful evidence.

## Plan Review

The protocol specifies 24 requests in three batches and three retained repeats per batch. All nine raw files contain the expected eight unique IDs. Packets contain exactly the frozen contract and assigned request texts. Independent reconstruction from those files equals `records.json` and `structure.json`; none of the 72 scheduled slots is dropped. Tests exercise missing/invalid slots, duplicate and unknown slots, incomplete reviews, independent binding/semantic failure, wording variation, and withholding a semantic aggregate before grading. `assess.summarize` combines structure, semantic and binding flags explicitly (line37).

The plan's checkbox file remains entirely unchecked although progress documents completion of generation and review underway. This is a documentation follow-up for the final report, not a failed experiment. This review provides the independent grading deliverable; the parent still owns final result reporting and plan reconciliation.

Rubric ambiguities were resolved against requests, not exact output counts. S12's separate existence and contingent-meaning questions are legitimate. S06's predicate on both questions describes the same hiding scenario. S19 permits the default on the control question as relevant context. S22's repeated sentence explicitly calls observation the second part and repeats no polling; local attachment of no polling to observation is reasonable despite the rubric grouping it as shared. No semantic penalty is assigned to those alternatives. Reasons contain lookup justifications, not application investigation or library answers.

## Author-Claim Reconciliation

| Claim | Evidence | Status and consequence |
| --- | --- | --- |
| 72 responses, all structurally valid, two canonical-equal cases | Nine raw files, frozen validator, independent reconstruction of structure | Confirmed; exact equality is only S08 and S24 and does not establish general determinism. |
| All scheduled slots counted; semantics independent | `assess.py`, eight tests, independent grade ingestion | Confirmed. Missing outputs fail; binding-only failures block the strict gate. |
| Thirteen frozen inputs and nine frozen raw files unchanged | SHA-256 verification of input/raw manifests and both round freezes | Confirmed. Packet contract and request equality checked directly. |
| Protected prior artifacts unchanged | Read-only `audit.py` verification of all 30 inherited manifests | Confirmed against those manifests. Byte reads only for sealed/data/weights artifacts; no semantic inspection. |
| Initial failing test before implementation | `test-output/red.txt` contains missing-module failure; current eight tests pass | Retained evidence supports the stated TDD progression; original execution timing cannot be independently reconstructed from text logs. |
| Fresh contexts, no retries, author saw only v2 scope | Packet isolation, AUTHOR.md and progress record | Consistent with artifacts, but agent provenance and absence of unseen attempts are author attestations, not independently provable from saved JSON. |
| Native-agent test, no controlled provider revision/temperature/seed or production API | Protocol and packets | Confirmed experimental limitation; no deployment, latency or final-answer qualification inferred. |

## Verification Performed

- Read every original request and all72 output objects, including questions, reasons, constraints and binding attachment. Authored `test-output/semantic-review.json` with72 distinct id/run grades and `stability-review.json` with24 case judgments.
- `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_assess`: 8 passed. The first shell invocation printed an unrelated shell startup parse warning and two wrong-working-directory documentation reads; those documents were subsequently read from correct paths. Test execution itself succeeded.
- `python3 -B audit.py`: all30 manifest checks passed. No sealed evaluation contents, database records or weights inspected semantically.
- Input freeze13, raw freeze9, round1 freeze3 and round2 freeze3 SHA-256 entries all match. All three packet contracts equal frozen CONTRACT.md; each packet's eight requests exactly equal its assigned cases.
- Rebuilt records from raw batch arrays and compared against saved records; recomputed structural summary equals saved `structure.json` exactly:72 structural passes,2 exact-equal cases.
- Aggregated independent grades: semantic text72/72; primary binding/strict usable65/72; all-three usable21/24. Batch strict totals24/24,20/24,21/24. Failures: S12r3; S16r1–3; S17r1–3. Sensitivity described above.
- Semantic equivalence24/24 means equivalent search-question meaning and coverage, not identical binding ledgers. S12's ledger varies while text meaning remains equivalent. S16/S17 repeat the same graded omission; stable errors do not satisfy usability. Exact canonical JSON equality remains2/24.
- Codebase-memory coverage checked for the five Python evidence files; all were `not_tracked`. Full direct source reads supplied verification instead of graph completeness claims. No reindexing or source edits performed.

## Open Questions And Residual Risks

The sample is24 synthetic development requests targeting familiar failure categories, with correlated repeats and shared context within batches. Case author, generator and reviewer use the same agent family; fresh roles are not cross-vendor independence. No production deployment, seeded stochastic controls, retrieval utility measurement, final-answer correctness, latency test, or new v2 comparison exists. Three samples per request cannot establish universal stability. The precise boundary between a requested operation and an auditable condition should be clarified for future experiments before new grades, without changing frozen evidence. The existing all-pass candidate gate already fails on an unambiguous exclusion omission.

## Verdict

**Ready with non-blocking follow-ups** for the bounded stress-test evidence and harness, once the parent reports the grades and interpretation sensitivity and reconciles the plan checklist. **Candidate gate: Not ready** for an unqualified all-request/all-repeat compliance claim. All72 question texts are semantically useful under this review, but the condition-audit contract is not consistently satisfied. This verdict does not authorize candidate tuning, sealed evaluation use or publication.

## Recommended Next Actions

Publish the bounded development result with separate text, binding, exact-equality and semantic-equivalence measures and the65-to71 sensitivity range. Keep every response and the frozen candidate unchanged. Record S12 as the unambiguous candidate failure and S16/S17 as stricter audit findings with explicit interpretive limits. No replacement reviewer or new workstream is requested.

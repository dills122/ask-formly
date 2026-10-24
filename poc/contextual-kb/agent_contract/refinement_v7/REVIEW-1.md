# Independent review

Review instance: 1 of 3. Verdict: **Not ready for candidate adoption; evidence ready to report a failed fresh gate.**

## Findings

**P1 — Independent property read acquires an unsupported eligibility gate.** In `test-output/b3-r3-raw.json`, F23 (entry starting line 89), question index 2 says `if it can work without subscribing to application services` before the property read. Its `if it can` binding includes indexes `[1, 2]`. The source requests that read independently after the expression changes and shares only the method restriction. This changes when the lookup is allowed. Runs 1 and 2 retain the independently requested read. Smallest credible future correction: preserve independent follow-ups when resolving shared restrictions, and verify both question eligibility and ledger assignment. Do not repair these frozen outputs or call a replacement run a first response.

**P2 — Observation event omitted from the ledger.** F23 in all three raw files (`b3-r1-raw.json:213`, `b3-r2-raw.json:90`, `b3-r3-raw.json:89`) has only the method restriction, conditional gate and post-change clause as ledger entries. No entry binds `expression-change observation` or an equivalent event excerpt to support/use indexes 0 and 1. `LEDGER-RULES.md` requires observed events in the ledger, and the frozen F23 rubric explicitly assigns this event to both aspects. The words remain in question text, so this is a ledger failure in all three, independently of the run-3 text failure. Future work must audit source events against every applicable emitted binding, including when the event is embedded in a capability name. Structural validation cannot find undeclared omissions.

No other actionable defect found in the reviewed scope. Awkward capitalization from verbatim copying is readable and not a semantic failure. No arbitrary exact-question-count, exact-excerpt or minimal-ledger requirements were used. Larger meaningful excerpts, grounded uncertain-version strings, and harmless redundant context were accepted. F22 unknown-adapter context and N14 run-2 wrapper context do not resurrect retracted scope or change the requested stage.

## Plan Review

Reviewed the new refinement_v7 directory on dirty `main`, HEAD `c3091328f49d53de6b41a49c4fe5aa8f1c45e516`; unrelated worktree modifications excluded. Read bootstrap, canonical protocol/policy/contract, plan, data review, all 30 source requests and rubrics, all 90 outputs (questions, reasons, metadata and bindings), candidate/tests and inherited transport/preservation/aggregation source. Preliminary concerns were recorded in REVIEW-1-preliminary.md before AUTHOR-EXPLANATION.md was opened. Reviewer did not inherit the implementation conversation. Coverage checks report all relied-on POC code paths `not_tracked`; conclusions rely on direct source reads, not graph completeness.

The plan is bounded and coherent: clarify prospective semantics, freeze a distinct prompt, create a policy-informed fresh panel, retain three repeats, review separately from structural scoring, and preserve historical evidence. Scope/derivation and output sections exactly equal v5; the ledger section exactly embeds LEDGER-RULES.md. candidate.py only selects v7 instructions and imports the unchanged same-POC v3 transport. No dependencies, schema expansion, integration, database change, retrieval or answer work. Security boundaries preserve request-as-data and advisory hints; no new external execution or data flow. Performance evidence is limited to prompt bytes and small local transport checks, not runtime generation cost. The final parent aggregation/report/freeze remains outside reviewer ownership.

The declared fresh all-three gate fails. This is an observed candidate limitation, not a reason to rewrite acceptance criteria. No heavy architectural pivot is established by these bounded failures, and no repair or new review instance has been initiated.

## Author-Claim Reconciliation

| Author claim | Inspected evidence | Status and consequence |
| --- | --- | --- |
| v5 scope/derivation/output retained, ledger replaced | Direct section equality and embedded policy checks | Confirmed |
| Prompt 13,979 bytes versus v6 17,485 | Byte-length check | Confirmed; no latency implication |
| Same schema and v3 transport; no completeness detector | candidate.py, v3 candidate, base contract, omission test | Confirmed; semantic review remains necessary |
| Six selector/transport tests plus six prior and eight aggregation tests pass | Independent executions | Confirmed |
| Red-before-green development | Retained tdd-red/green logs inspected | Logs support missing-module then six passes; files cannot prove execution chronology independently |
| Four packets, three repeats, 90 outputs | Exact packet contract/request equality; reconstruction of 12 raw files into records | Confirmed retained contents and slot coverage |
| First submissions, fresh contexts, no unseen retries/tuning | Protocol and retained files | No contradictory evidence; unseen execution history cannot be independently established from files |
| Fresh author informed by policy, original rubric retained and F06 amended | Data review and original/final rubric diff | Confirmed artifact difference only F06; panel remains targeted synthetic development |
| Six unchanged diagnostic requests with prospective N09/N14 rules | Compared with v6 source requests; inspected new rubrics | Confirmed; no comparable historical improvement claim |
| 35 inherited manifests preserved; payloads byte-only | Independent snapshot equality and SHA-256 checks | Confirmed current bytes; sealed semantic content not read |

## Verification Performed

All Python commands used `-B`, so verification did not write bytecode into frozen directories.

- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v7 -p test_candidate.py -v`: 6/6 pass.
- Equivalent command for refinement_v6: 6/6 pass.
- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/v3_stress -p test_assess.py -v`: 8/8 pass. Initial discovery at the parent directory found zero tests and was corrected; that attempt is not counted as a pass.
- Independent inline Python imported v7 preservation snapshot: 35 manifest results, covering 38,447 entries, equal both protected-before and protected-after-generation. Payloads were read only as bytes for hashes.
- Verified candidate-freeze (9), input-freeze (18), raw-freeze (12), diagnostic-raw-freeze (3), round1-freeze (3) and round2-freeze (3) entries.
- Checked all four packets contain the exact complete frozen contract and assigned source requests. Reconstructed nine fresh raw files of eight outputs and three diagnostic raw files of six: exactly 90 unique `(id, run)` slots matching records.json. The initial inline script assumed a `cases` packet key; after inspecting the actual `requests` key, the corrected assertion passed.
- Validated all 90 outputs and exercised 360 hint variants (missing, malformed, valid and overlapping/conflicting) without core-plan/search-request changes or input mutation. Valid spans apply to 84 nonempty outputs; the six empty outputs correctly ignore impossible spans.
- Direct scoring inspected every source/output pair. Scope metadata passes 72/72 fresh and 18/18 diagnostic. Reasons are grounded lookup justifications; no application investigations or library answers added.

| Panel / repeat | Text | Semantic including scope | Complete bindings | Joint |
| --- | ---: | ---: | ---: | ---: |
| Fresh run 1 | 24/24 | 24/24 | 23/24 | 23/24 |
| Fresh run 2 | 24/24 | 24/24 | 23/24 | 23/24 |
| Fresh run 3 | 23/24 | 23/24 | 23/24 | 23/24 |
| Fresh total | 71/72 | 71/72 | 69/72 | 69/72 |
| Diagnostics run 1 | 6/6 | 6/6 | 6/6 | 6/6 |
| Diagnostics run 2 | 6/6 | 6/6 | 6/6 | 6/6 |
| Diagnostics run 3 | 6/6 | 6/6 | 6/6 | 6/6 |
| Diagnostics total | 18/18 | 18/18 | 18/18 | 18/18 |

Fresh all-three joint gate: **23/24, failed**. Diagnostic all-three joint gate: **6/6, passed**. Structural checks: 90/90. Fresh question-meaning stability 23/24; ledger-meaning stability 23/24. Diagnostic question and ledger stability both 6/6. Exact JSON equality: fresh 2/24 (F16, F24), diagnostic 0/6; exact equality is separate and not required. Stable failures are still failures. Machine-readable artifacts contain 90 semantic judgments and 30 stability judgments.

## Open Questions And Residual Risks

The policy is prospective. N09's callback-model target and N14's registration/use stage are explicitly judged differently from older contracts; old evidence must remain frozen, and better diagnostic scores do not establish model improvement. No comparator was run. The fresh author knew the policy, so these are correlated synthetic development requests, not an independent production distribution. Native model revision, temperature and seed are uncontrolled; file contents cannot prove no unseen attempts occurred. Semantic grading is fallible. No production accuracy, latency, retrieval utility, final-answer quality, training or Angular compatibility claim follows.

## Verdict

**Not ready** for candidate adoption: the predeclared fresh all-three gate fails on F23. **Evidence ready** for honest reporting and parent final aggregation/freezing: inputs, outputs, preservation and structural transport are verifiable and the failures are retained. Diagnostic success does not override the fresh failure.

## Recommended Next Actions

Parent should aggregate these supplied judgments, report fresh and diagnostic results separately, preserve the failed gate and prospective-rule caveat, then freeze the evidence. No frozen-output repairs, resampling, replacement reviewer or new independent instance is justified merely to obtain a favorable verdict. Any later material change needs separately authorized scope and the remaining bounded review budget.

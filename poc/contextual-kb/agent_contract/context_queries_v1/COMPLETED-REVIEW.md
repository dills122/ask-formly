# Completed independent review

Review instance: 2 of 3.

## Findings

No actionable implementation or experimental-integrity defect found in the reviewed scope. The experiment is ready to retain as negative evidence. The contextual-query candidate is **not qualified** and must not replace the foundation baseline.

The failures below are retained observations, not requests to edit frozen outputs or gold:

- C06 loses a required key/model-versus-type/renderer fact after supplemental fusion and interleaving (`test-output/retrieval/results.jsonl`, C06/context; `data/cases.json`, C06). Recall falls from 5/6 to 4/6 and complete-required-group coverage falls from true to false. This violates the zero paired loss gate despite equal pooled complete totals. Keep this failure; any different merging strategy needs a separately authorized experiment.
- C09 supplemental Q1 weakens teardown timing by placing “when the field is destroyed” adjacent to the Observable return condition (`data/records.json`, C09). This introduces a plausible alternative attachment. Exact-copy validation in `candidate.supplemental_queries` cannot prove relationships, so the conservative prospective semantic failure is justified.
- C11's foundation condition ledger omits the supplied IndexedDB channel despite retaining it in prose (`data/records.json`, C11). `qualification_v3/CONTRACT.md:332` explicitly requires supplied methods/channels in the ledger. Preserve this foundation failure without attributing it to the supplemental stage or to incorrect Formly knowledge.

## Plan Review

The implementation follows the frozen bounded comparison: 36 requests, three batches of 12, 49 derived questions, 49 first supplemental texts, original full questions always queried, four identical supplements skipped, existing RRF with constant 60 and unchanged obligation interleaving, fixed final budget eight. All 72 arm records are present. Supplemental validation failures retain an explicit error and use originals; foundation delivery failures would yield empty results rather than fabricated replacements. The tests cover these accounting boundaries.

Prospective labels contain 26 direct, four partial and six unsupported cases. The 30 nonempty-gold cases are the denominator for macro recall and precision; partial cases score only supported aspects. All six unsupported cases retain empty gold and receive eight candidates in each arm. This is exposure, not false-answer or abstention accuracy.

C08's required modern callback/model fact is defensible without requiring a legacy migration comparison. C15's required model-removal fact distinguishes model values from child field objects; it remains limited by the fact's conditions. C18's inheritance example supplies the requested renderer reuse with defaults. Their related corroborating facts remain in all-relevant recall. The four partial gaps (C05, C25, C27, C34) remain open; complete groups cannot prove full answers to these requests.

The implementation does not modify the engine or DB. `run.main` uses the existing read-only SQLite helper, existing index construction, exclusive attempt/output creation, rotating arm order and retained hashes. Tests use a fake index; the saved actual traces provide the experiment evidence. No model or retrieval rerun was performed in this review. No gold, candidate or existing model edits were made.

## Author-Claim Reconciliation

Preliminary findings were saved in COMPLETED-PRELIMINARY.md before opening RESULTS.md, AUTHOR-EXPLANATION.md or FINAL-REPORT.md. The bootstrap already disclosed semantic findings and preflight history, so semantic discovery was not blind.

| Author claim | Evidence inspected | Status and consequence |
| --- | --- | --- |
| Pooled recall 89.39% → 89.94%; precision 25.42% unchanged | Independent metric implementation over all saved IDs and prospective labels | Confirmed; exact gain is 0.5556 percentage points, below two required |
| Batch recall 92.50/91.67/84.00 → 90.83/91.67/87.33 | Independent per-batch aggregate calculation | Confirmed; batch 1 regresses and batch 3 fails 89.25% in both arms |
| Equal 26/30 complete totals hide gain/loss | Reconstructed C30 and C06 traces and AND-of-OR groups | Confirmed; C30 gains, C06 loses; no paired complete loss at4 |
| C30 rewrite helped, C06 evidence displaced | Saved original/supplemental rankings, RRF and merge reconstruction | Confirmed for these complete query texts; word ordering alone was not isolated causally |
| 49 → 94 queries; 5,504 → 10,564 characters | Query text/provenance matched against every source plan and supplement | Confirmed; 45 added calls, approximately 92% more retrieval calls |
| Semantic passes 35/36 per stage and 34/36 combined | All plans, supplements, ledgers, contracts and prospective semantic judgments | Confirmed; case counts, not per-question model accuracy |
| 17 tests pass, 123 runtime freeze entries, prior 45 manifests preserved | Independent tests, hash verification and preservation-chain snapshot | Confirmed current integrity |
| Native fresh contexts and no prior exposure/retries | Literal transport, first-save records and author account | Artifacts support first retained outputs; historical isolation/absence of unrecorded attempts cannot be established by hashes alone |
| Timing 0.329s versus 0.620s plus 0.908s setup | Retained row timings, scores and setup record | Consistent; native generation cost is unmeasured and these are not service timings |

FINAL-REPORT.md and RESULTS.md accurately distinguish arithmetic, semantic readiness, supported denominators, incomplete catalog coverage and the failed candidate gate. AUTHOR-EXPLANATION.md is explicitly a preflight document; its then-pending execution steps are resolved by the completed evidence rather than silently treated as current status.

## Verification Performed

- Directly inspected protocol, supplemental contract, tests, implementation, original/supplemental outputs, 46-fact catalog, all 36 labels and semantic judgments. Repository boundary is dirty `main` at c309132; unrelated changes excluded.
- Ran `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_candidate test_assessment` in the experiment directory: **17 passed**. Captured `test-output/completed-tests.txt`. A shell initialization parse warning appeared separately; the unittest command exited successfully and its log records all passes.
- Ran `PYTHONDONTWRITEBYTECODE=1 python3 test-output/completed-recompute.py`: independent RRF/interleave implementation matches **72/72 traces**; independent relevance/group/DCG/MRR implementation matches **144/144 metric sets**. Independent supported/batch aggregates agree with scores.json. The existing pure assessor additionally reproduces the complete saved score object, including descriptive bootstrap intervals and timing fields.
- Matched every actual query's question index, kind and text to its unchanged foundation/supplement source. Compared all first literal foundation outputs with transported JSON and records, and supplemental first outputs with records.
- Verified current hashes for **7 design, 7 generation, 123 run, 4 retrieval, 43 results and 2 report** freeze entries. No mismatches.
- Recomputed the complete **45-manifest** prior preservation chain and matched before/pre-run/after-run snapshots. Sealed artifacts were hashed only. No sealed semantic inspection occurred.
- Machine-readable checks: `test-output/completed-checks.json`; verification implementation: `test-output/completed-recompute.py`.

October 16 codebase graph coverage reports relied-on POC code files `not_tracked`; direct source reads supplied verification. No reindex or completeness claim was made.

## Open Questions And Residual Risks

These are small, related synthetic development requests; descriptive bootstrap intervals and one-case sensitivity do not establish population performance within ±0.75 percentage points. Gold boundaries and C09 attachment ambiguity involve semantic judgment, with retained rationales. Fresh-context generation is native rather than a pinned hosted API experiment. Hashes verify current bytes and manifest consistency, not historical ordering by themselves. The candidate has no answerer, abstention evaluation or production service qualification.

C30 changes more than a controlled single variable. Its observed benefit supports a diagnostic hypothesis about operation-first wording, not an isolated causal conclusion. Likewise, C06 identifies evidence displacement under this combination of queries/ranks/budget; it does not prove a particular replacement policy will fix it.

## Verdict

**Ready** — to retain and report this completed bounded experiment as negative evidence. **Candidate decision: do not promote; retain foundation-only.** Neither arm establishes the requested consistent retrieval floor, and the contextual candidate fails the utility gate independently of its semantic failures.

## Recommended Next Actions

Freeze this review and preserve the evidence. Keep these 36 requests as diagnostics, not fresh tuning/qualification data. No material fix warrants review instance 3. Any later integration change addressing evidence displacement needs its own explicit scope and fresh predeclared evaluation; no such work was started here.

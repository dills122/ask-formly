# Independent final review

Review instance: 3 of 3. Final instance of the arrays follow-up flow; count is not reset.

## Findings

**P2 — Q20 source premise remains absent from the condition ledger in every fresh repeat.** All three raw Q20 plans paraphrase the supplied internal-export premise in question zero, but bind only `6.3.12` to questions 0 and 1. The source statement `An internal Formly source file exports TypeOption` is a supplied circumstance of the public-export verification, not merely the API name. The full contract requires supplied scenario states and applicable setup (condition_candidate_v1/CONTRACT.md:82 and :89), says prose alone does not complete the ledger (:275), and requires exact-source nonempty bindings (:355) without deleting applicable conditions (:365). Prose preservation does not satisfy that ledger obligation.

Evidence: line 3 of each raw generation artifact:

- `test-output/qualification-1/r1-b3-candidate/mcp/planner/3c163bf24671406b800f0f7a74250799/events.jsonl`
- `test-output/qualification-1/r2-b3-candidate/mcp/planner/55c94b72358a4e66b4a462d665b2601a/events.jsonl`
- `test-output/qualification-1/r3-b3-candidate/mcp/planner/7ef4597f652b4c079fe9371647409cfa/events.jsonl`

Delivered normalized plans equal these raw plans, with `rewrites: []`. This is not inferred-index or casing repair. The lookup answers are correct, but these attempts do not demonstrate successful exact-source, nonempty binding of the original problematic premise. The schema cannot reject an omitted binding. Do not claim the original semantic condition problem is resolved. The smallest bounded correction is prospective contract clarification distinguishing a supplied factual premise for verification from a mere requested lookup target: preserve its user-supplied, unverified status, copy its meaningful source span, and bind it to each governed question. That would need newly authorized verification; saved outputs, rubric and frozen candidate must remain unchanged. No architecture pivot is indicated by this evidence. No further implementation/review loop is authorized by this report.

**Observed noncritical answer miss:** repeat 2 A01 omits that function-valued fieldArray is called with the array field before its returned configuration is cloned. The supporting fact was delivered with full coverage. The assessor correctly marks this caller omission unusable; the independent audit agrees. This is retained in the 44/45 score and is not an additional delivery failure.

## Plan Review
The planned one-shot candidate, fixed answer denominator, three repeats, unchanged 85-fact DB, fresh six-by-three planner probes and independent result audit were executed. No hidden retry, question tuning or promotion was observed. Numeric answer gates pass: 15/15, 14/15, 15/15; all 15 controls usable; zero critical answers or delivery failures. All 18 fresh planner probes independently pass both structural and semantic review. Those targeted probes do not override the Q20 ledger omission found in the actual regression plans.

## Author-Claim Reconciliation
| Claim | Evidence | Status / consequence |
| --- | --- | --- |
| Contract/schema-only candidate, unchanged validation and capitalization | Source comparisons and 26 offline tests | Confirmed |
| One-shot generation, no inferred bindings or broad case normalization | Raw generation and normalized Q20/probe outputs | Confirmed |
| Original malformed saved core remains rejected | Exact negative fixture tests | Confirmed |
| Fresh 45 answers satisfy fixed candidate thresholds | All answers, delivered facts, assessment rows and independent evaluator call | Confirmed: 44/45, including retained A01 omission |
| All fresh condition probes pass | REVIEW-PLANNER.json, all 18 raw/normalized plans | Confirmed within six targeted scenarios |
| Original Q20 condition-binding problem is resolved | All three Q20 ledgers omit the internal-export premise | Not established; semantic contract omission remains |
| Installed and historical artifacts unchanged | 229 preservation pins, 27 freeze hashes, exact candidate DB hash | Confirmed at final audit |

## Verification Performed

- Independently ran 12 planner tests and 14 harness tests: all passed (commands in REVIEW-PRE-RUN.md).
- Read all 45 answers against the frozen cases and cited fact contents. Verified answer citations were delivered in each corresponding MCP response. Results in REVIEW-ANSWERS.json.
- Independently replayed exact sequential MCP-call validation for all nine batches (45 calls); all tool errors absent and all assessment delivery errors empty.
- Read all 18 fresh planner outputs semantically against the complete contract and fixed checks; verified one raw attempt per probe, request/receipt/raw-core linkage, and no wording rewrites. Results in REVIEW-PLANNER.json.
- Inspected raw and delivered normalized Q20 plans from all three repeats.
- Independently evaluated the final summary: qualified=true with 15/14/15 usable, no numeric-gate reasons. All 45 existing grader outcomes match this review; no grades were overwritten.
- Rechecked all 229 preservation entries, all 27 qualification-freeze entries, and candidate DB SHA-256 `bbb55e168cc81e60927a1bf146af767cd8ab6c9999875239ea28a879487531ff`.
- Repository-wide maintenance pass was reported by the initiating task; this reviewer did not independently rerun that broader command. No hosted inference, sealed evaluation reads, source edits, commits or publication were performed by this reviewer.

The graph did not index the new paths; full source fallback was used as documented in the pre-run report. The review assignment already contained design details, so a fully blind first pass was unavailable; author documents were read after source inspection and preliminary findings.

## Open Questions And Residual Risks
The exact schema prevents empty emitted index lists, but neither it nor unchanged validation detects omission of an applicable binding. The prompt change is therefore not a general semantic guarantee. The prior historical score was also 44/45, with a different failure; it is not a controlled causal comparison and does not establish improvement or regression. Hosted sampling is unseeded. Neither this targeted run nor its source evidence qualifies a Material application or the whole Formly library.

## Verdict
**Not ready** to accept the candidate as a completed fix for the stated condition-binding defect. The frozen quantitative qualification and fresh-probe gates pass; the actual Q20 semantic ledger finding remains unresolved. This verdict does not invalidate correct answers or change their frozen grades.

## Recommended Next Actions
Preserve all current artifacts and report both passing quantitative gates and the unresolved Q20 finding. Ask the human to choose whether to accept this explicitly limited experimental result or authorize a bounded follow-up. Review instance 3 of 3 is exhausted; no new reviewer, retry, tuning or architecture pivot starts under the current loop. No promotion.

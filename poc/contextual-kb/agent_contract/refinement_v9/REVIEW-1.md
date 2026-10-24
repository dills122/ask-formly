# Independent review of v9

Review instance: 1 of 3. Verdict: **Not ready** under the declared candidate gate. The retained evidence is ready for reporting a negative result.

## Findings

**P2 — Required unknown-adapter scope disappears from the third Q19 ledger.** In `test-output/b3-r3-raw.json:4`, the question correctly says “with an unknown UI adapter”, but the ledger contains only the uncertain version and two comparison targets. `data/fresh-rubric.json:631` requires the supplied unresolved adapter scope in the question and ledger. Global `ui_adapter: null` cannot distinguish this explicit uncertainty from unspecified scope. This is an omission, not a non-source excerpt: structural validation correctly accepts it. The smallest behavioral correction would preserve a meaningful verbatim unknown-adapter source span in both question and ledger during generation. Do not repair this saved response; retain the failed denominator slot. The perfect fresh gate fails.

No additional actionable code defect found in this bounded prompt/transport change. No performance, security or downstream behavior claim follows from this review.

## Plan Review

Scope is the new refinement_v9 directory on dirty `main`, HEAD `c3091328f49d53de6b41a49c4fe5aa8f1c45e516`; unrelated dirty/untracked repository changes are excluded. Root and POC instructions, STEERING, protocol, change, contract, tests, plan and all 81 source/output pairs were inspected. The preliminary assessment was saved before opening AUTHOR-EXPLANATION.md. Reviewer received a neutral bootstrap without implementation conversation.

The candidate is a small selector reusing frozen same-POC v3 validation/plan construction. Its contract adds original-source copying and prospective context rules to v8; no new runtime dependency or deterministic semantic checker was introduced. The tests appropriately establish transport properties rather than prompting completeness. The plan preserves prior evidence, separates diagnostic/fresh panels, and does not authorize resampling after a miss. Final aggregation and reporting remain the parent task's responsibility.

## Independent Semantic Results

Every scheduled slot is retained. Text means questions/reasons preserve the request; semantic includes global scope; binding means complete, correctly attached source conditions. All 81 outputs pass structural validation and exact source-to-assigned-question checks for their declared bindings.

| Panel | Repeat | Text | Semantic | Binding / joint |
| --- | --- | --- | --- | --- |
| Fresh | 1 | 24/24 | 24/24 | 24/24 |
| Fresh | 2 | 24/24 | 24/24 | 24/24 |
| Fresh | 3 | 24/24 | 24/24 | 23/24 |
| Fresh | All slots | 72/72 | 72/72 | 71/72 |
| Diagnostics | Each repeat | 3/3 | 3/3 | 3/3 |
| Diagnostics | All slots | 9/9 | 9/9 | 9/9 |

Fresh all-three joint success is 23/24; diagnostics all-three is 3/3. Fresh gate fails, diagnostic gate passes, combined candidate gate fails. Combined joint score is 80/81, not a substitute for separate panel gates.

Question meaning is stable on 24/24 fresh and 3/3 diagnostic cases. Ledger meaning is stable on 22/24 fresh and 3/3 diagnostics: Q19 loses required scope; Q06 varies the existing-value background assignment. Exact JSON equality is only 2/27 and is not the semantic standard.

Interpretive decisions were made in the preliminary pass: Q06 run1's supplied existing-value background does not assert that this setting requires an existing value; it is permitted, although its broader ledger attachment is recorded as variation. Q13's general use and specific two-field wrapping retain both requested usage formulations and are accepted as meaningful decomposition, not rejected by question count. The explicit After registration clause binds the two-field outcome in every run; general use also prospectively follows registration. Q04's redundant independence wording and Q24's optional spelling-uncertainty entries are harmless. Repeated support clauses resolve gates rather than introducing unsupported capabilities. Q22 run3 identifies the registration-free reuse capability being configured and retains both gates. No same-referent context was penalized merely for existing; explicit independent scenarios remain separate.

## Author-Claim Reconciliation

| Claim | Evidence | Status / consequence |
| --- | --- | --- |
| v8 plus v9 change, same schema/transport | Contract diff, selector, v3 source, tests | Confirmed; prompt grows from 16,098 to 19,532 bytes. |
| Literal invalidity still rejects; hints cannot rewrite core | 7 v9 tests, 6 v8 tests; all81 replay with malformed hints | Confirmed. Semantic omissions remain outside validator. |
| 81 outputs in four batches repeated three times | Four exact packets, twelve raw files, records reconstruction | Confirmed for retained artifacts; no absent/duplicate slots. |
| Diagnostic requests unchanged; only C14 criterion revised | Request/rubric equality against v8 | Confirmed; C12/F23 rubric identical, C14 only forbidden/notes differ. No historical regrade or causal gain claim warranted. |
| Q19 rubric clarification before generation | Author-submitted/final diff only Q19; input-freeze and data-review | Content and retained account confirmed; hashes alone cannot independently prove execution chronology. |
| Independent fresh authorship, first outputs only, no hidden retries | AUTHOR.md disclosure and frozen packets/raw | Consistent retained provenance; unseen access/attempt history cannot be proven from files. |
| 37 protected manifests, 38,565 overlapping entries | Independent preserve.snapshot equality | Confirmed with byte-only reads of protected payloads. |
| Seven tests preceded implementation | Saved TDD account/logs and current seven passing tests | Current behavior confirmed; chronology remains retained testimony, not independently replayed history. |

## Verification Performed

Executed with Python `-B`:

- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v9 -p 'test_candidate.py' -v`: 7 passed.
- Same discovery under `refinement_v8`: 6 passed.
- Discovery under `v3_stress` with `test_assess.py`: 8 passed.
- Independent Python assertions: candidate (9 entries), input (18), raw (12), diagnostic raw (3), round1 (3), round2 (3) freeze hashes all match.
- `preserve.snapshot()` equals protected-before across 37 manifests and 38,565 overlapping hash entries; no sealed semantic reads.
- All four packets contain byte-exact full contract strings and exact assigned ID/request pairs. Nine fresh raw files contain eight outputs each; three diagnostic files contain three each. These reconstruct records.json exactly with 81 unique expected slots.
- All81 validate and preserve unchanged output/core plans when optional hints are absent, empty or malformed. Existing tests also exercise conflicting/overlapping hints and rejection of an invalid source span.
- Compared every diagnostic request and rubric to its retained v8 counterpart, and compared original/final fresh rubrics.

One audit-script attempt used packet key `cases` rather than actual `requests` and raised KeyError before packet assertions; the corrected non-mutating check passed. This was a reviewer script error, not a candidate failure. No repository artifacts were altered by that check.

Graph coverage reported relied-on POC code as not_tracked; direct full-source reads were used. The graph does not certify this scope. No npm/Angular qualification was necessary for isolated POC prompt evidence; no portable indexing/packaging/Angular behavior changed in the reviewed scope.

## Open Questions And Residual Risks

Native model revision, temperature and seed are uncontrolled; repeats are correlated and the targeted synthetic cases are policy-informed. Saved hashes demonstrate preserved bytes, not unseen attempt history or proof of pre-generation timing. The diagnostic C14 policy changed prospectively; its result cannot establish a pure behavioral improvement over old scores. Source validity does not prove omitted-condition coverage. Prompt length increased without measured latency or cost. No production, retrieval, final-answer, universal compatibility or browser claim is supported.

## Verdict

**Not ready** for the declared all-fresh/all-diagnostic repeated-pass gate. Evidence is sufficient to report the bounded result: 71/72 fresh joint successes, 9/9 diagnostics, one preserved unknown-scope binding omission. The experiment can be closed honestly with this negative candidate decision.

## Recommended Next Actions

Parent should aggregate the supplied 81 semantic rows and 27 stability rows, retain this failure and denominator, reconcile any disputed interpretation with concrete source evidence, and complete final evidence/preservation reporting. Do not repair outputs, rerun missed slots or initiate another review simply to replace the verdict. A material future candidate would need separately authorized work and preserved evidence.

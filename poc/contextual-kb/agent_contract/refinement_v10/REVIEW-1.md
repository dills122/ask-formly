# Independent review

Review instance: 1 of 3. Verdict: **Not ready** against the frozen full-pass candidate gate. Evidence is sufficient for a bounded negative result. No fix or new generation performed.

## Findings

1. **P2 — U22 repeats exceed the frozen local attachment rubric.** In `test-output/b3-r1-raw.json:86`, the return-to-editability model-value lookup includes “a read-only presentation without disabling its Angular control”; line 92 binds this combined condition to both questions. Runs 2 and 3 repeat that attachment. The frozen rubric assigns the no-disable method restriction only to configuration. Thus all three fail primary text/semantic/binding grading. This is not an unknown-scope omission: version uncertainty is preserved. The smallest prospective correction is an explicit distinction between retained historical setup and a restriction governing the new operation, checked before submission. **Ambiguity:** the source asks about the same field; v9 permits relevant history. These responses do not say “only if” or “because”. A grounded-history reading is defensible, so this is a frozen-rubric failure rather than an unambiguous new behavioral regression. Accepting that interpretation changes fresh joint 68/72 to 71/72; do not silently amend the frozen grades.

2. **P2 — U10r3 disagrees with frozen global normalization.** `test-output/b2-r3-raw.json:26` emits version `"unknown"`; the rubric requires null. All requested questions, unknown-version excerpts, events and nested gates remain correct. Grade text and binding true, semantic including normalized global scope false. The contract also says uncertain versions remain grounded uncertain strings, which leaves a real ambiguity for a wholly unknown version. Clarify this distinction prospectively; no current output repair. Accepting `"unknown"` as equivalent affects one slot, and accepting both this and the U22 history reading yields 72/72 fresh slots. It does not recover the full candidate gate because transport still fails.

3. **P2 — One retained diagnostic packet is not valid JSON.** `test-output/b4-r2-raw.json:46` contains literal backslash-n outside a string at character 1939. F23r2 cannot become a validated plan. Its visible questions/ledger satisfy the diagnostic rubric, but its output remains null and its structural/usable grade fails. Neighboring exact original slices parse independently; that does not make the enclosing packet valid. Smallest next action for this experiment is honest retained failure and both accounting views, already supported by the observation note. Any future transport mitigation requires a separately authorized, prospective experiment, not alteration of saved evidence.

No additional actionable selector-code defect found. The selector is small, preserves request data, and reuses the established validation/hint projection without new dependencies or semantic repair. The parser is deliberately unable to prove completeness or correct attachments; tests honestly preserve that boundary. No new library behavior, security, runtime or performance claim is warranted by this change.

## Plan review

Scope is the new `refinement_v10` directory on dirty `main`, HEAD `c3091328f49d53de6b41a49c4fe5aa8f1c45e516`. Numerous unrelated tracked/untracked changes exist and were excluded. The only contract changes against v9 are the candidate heading and the explicit-unknown-scope section. This is a bounded prompt experiment, not an indexing/packaging change, so the targeted tests rather than root npm/Angular qualification are proportionate.

The plan's candidate/input freezes, 24 fresh cases repeated three times, four unchanged diagnostics repeated three times, retention and preservation requirements are materially implemented. Independent review and final aggregation/freeze were still unchecked when read; the parent owns those final steps. The malformed-packet slice method is transparently post-observation, not preregistered. The plan does not warrant promotion merely because the target Q19 omission disappears. No heavy architectural pivot is required to report the negative result; no additional review is requested to replace it.

## Author-claim reconciliation

The preliminary report was written before AUTHOR-EXPLANATION.md was read. The reviewer received a neutral bootstrap and the known transport issue, not the implementation rationale or parent semantic grades. Parent subsequently requested explicit ambiguity treatment; the primary independent grades remain unchanged.

| Claim | Evidence and disposition |
| --- | --- |
| New scope clarification; inherited transport unchanged | Confirmed by contract diff and candidate import/selector source. |
| Eight v10, seven v9 and eight scorer tests pass | Independently rerun: confirmed, 23/23. |
| Structural checks cannot detect old omission | Confirmed by candidate tests and validator implementation; not semantic success evidence. |
| 84 first responses / 12 files | 84 distinct scheduled slots and 12 retained files independently reconstructed. “First” and absence of unseen attempts cannot be established by hashes. |
| Four exact request packets | Confirmed full contract equality and original request equality for every packet. |
| Fresh rubric unchanged; diagnostics inherited | Fresh rubric equals author-submitted bytes. Four diagnostic rubric objects equal v9's corresponding diagnostic/fresh entries. |
| 38 protected manifests unchanged | Independently recomputed snapshot equals protected-before. |
| 83 structurally valid; 11 whole packets valid | Independently confirmed; does not imply 83 semantically usable. |
| Independent input author and pre-generation freeze | Saved author/data-review testimony and freezes support the process account, but do not independently prove delivery timing, unseen reads or attempts. |

## Verification performed

Executed with Python `-B`, without resampling or repairing evidence:

- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v10 -p test_candidate.py`: 8 passed.
- Same command targeting `refinement_v9`: 7 passed.
- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/v3_stress -p test_assess.py`: 8 passed.
- Imported v10 `preserve.snapshot()` and compared with `protected-before.json`: 38 manifests unchanged; protected payloads were read only as bytes by the preservation verifier, never semantically inspected.
- Independently SHA-256 checked every entry in candidate/input/raw/diagnostic-raw/round1/round2 freezes: respectively 9/18/12/3/3/3 entries matched.
- Independently compared all four packet contracts and their request arrays against original source cases.
- Parsed all raw packets strictly. For the malformed packet, independently scanned brace boundaries outside strings, checked the four recorded ranges against original bytes decoded as text, checked exact raw slice equality, and parsed each original slice without replacement. Ranges: C12 [4,922), C14 [926,1901), F23 [1905,3331), Q19 [3335,4057). Only F23 failed, at slice character 34. All other reconstructed objects and the retained null failure matched records.json: 84 unique slots.
- Independently invoked candidate validation on all reconstructed values: 83 valid, only F23r2 failed. Every declared excerpt in valid rows therefore occurs literally in source and assigned questions. Manual review separately checked omissions, meaning and attachments.
- Read all 28 source/rubric pairs, all 83 parsed output objects and F23r2's original visible text, including reasons, globals and ledger. Wrote 84 semantic rows and 28 stability rows.
- Graph coverage for inspected selector/transport/test/preservation paths reported `not_tracked`; direct source fallback was used. Graph absence is not evidence of missing implementation.

### Primary frozen-rubric results

| Panel | Text | Semantic including globals | Binding | Structure | Joint usable |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fresh | 69/72 | 68/72 | 69/72 | 72/72 | 68/72 |
| Diagnostics | 12/12 | 12/12 | 12/12 | 11/12 | 11/12 |
| Combined | 81/84 | 80/84 | 81/84 | 83/84 | 79/84 |

Diagnostic semantic counts explicitly include manual visible-text grading of malformed F23r2; they are not counts of usable structured responses. Fresh joint per repeat is 23/24, 23/24, 22/24; diagnostics 4/4, 3/4, 4/4. All-three joint is fresh 22/24, diagnostics 3/4, combined 25/28. Both full panel gates fail.

**Conservative whole-packet accounting:** 11/12 packets accepted; structural slot usability 80/84. Counting all four slots in malformed b4r2 unusable gives diagnostic joint 8/12 (4/4, 0/4, 4/4), diagnostic all-three 0/4, combined joint 76/84 and combined all-three 22/28. Fresh scores unchanged. This is supplementary post-observation sensitivity, not a replacement denominator.

**Meaning stability:** all 28 question sets and all 28 ledgers preserve equivalent requested meaning across repeats, including U22's stable disputed attachment. For F23 this is visible-text equivalence only. U10's normalized global projection differs null/null/unknown; requiring normalization-inclusive equivalence lowers that stability count to 27/28. Requiring three usable structured outputs additionally excludes F23. Exact JSON, excerpt segmentation, repeated support clauses and harmless redundancy are not semantic stability criteria. Stable failure is still failure.

Q19 explicitly preserves unknown-adapter scope in question and ledger in all three runs. All other active explicit-unknown scope statements are covered in the observed fresh panel. This targeted result does not establish a causal improvement or general reliability.

## Open questions and residual risks

U22's method-versus-history attachment and U10's unknown-version normalization are the material interpretation ambiguities. Under a permissive sensitivity accepting both, fresh reaches 72/72, but combined usable is at most 83/84 per-request or 80/84 whole-packet; the full gate remains negative. Do not retroactively rewrite rubrics, previous grades or raw evidence.

Cases are policy-informed, correlated targeted synthetic requests. Native model revision, temperature and seed are uncontrolled. No contemporaneous baseline identifies causality. Saved hashes establish integrity, not unseen attempt history or independent wall-clock ordering. There is no production-distribution, sealed-evaluation, retrieval, final-answer, latency or cost claim. The growing contract may impose unmeasured costs.

## Verdict

**Not ready** for the declared full-pass candidate gate. Evidence is ready for final aggregation of a negative, ambiguity-qualified experiment. Even the most permissive semantic sensitivity retains the diagnostic transport failure.

## Recommended next actions

Complete the parent-owned report, preservation recheck and final freeze using these grades and both transport views. Retain the targeted Q19 success, the two interpretation sensitivities and all failures. No candidate fixes, rubric rewrites, replacement samples, publication or additional review cycle are authorized by this review.

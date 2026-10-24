# Independent review of frozen v5 stress evidence

Review instance: 1 of 3. Boundary: `/Users/dsteele/repos/ask-formly/poc/contextual-kb/agent_contract/v5_stress`, dirty `main` working tree. Existing unrelated changes excluded. Review used separate context and recorded `REVIEW-1-preliminary.md` before opening `AUTHOR-EXPLANATION.md`. No candidate, request, rubric, baseline, raw response, data/DB or downstream edits. No subagents, retries, staging or commits.

## Findings

The evidence is reviewable and the full acceptance gate fails. These are failures of the frozen candidate responses, not instructions to repair retained outputs.

1. **P2 — T03 runs 2–3 omit single-field support verification.** `test-output/b1-r2-raw.json:112` and `b1-r3-raw.json:4` ask only how to invoke the API if it works on a single field. Neither asks whether single-field support exists. Run 1 includes that lookup. A compound support/invocation question would be acceptable, but there is no support-check clause here. The smallest future behavioral correction would explicitly ask support without gating that check on itself. Semantic failure; bindings on the present questions remain correct.
2. **P2 — T11 all repeats lose the shared corrected dependency on the message question.** `test-output/b2-r1-raw.json:34`, `b2-r2-raw.json:36`, `b2-r3-raw.json:37`, T11 question index 1, ask a generic required-error message and bind `props.required from model.needsReceipt` only to index 0. The independently searchable message question loses the supplied dynamic scenario. Future generation must retain and bind that relationship to the message question. Semantic and binding failure in all three runs.
3. **P2 — T17 all repeats omit the outer eligibility audit for the named message.** In all `b3-r*-raw.json` T17 records, `If so` is bound only to indexes 1 and 2, never final index 3. The final lookup retains the message-connection gate but lacks the outer source contingency in both question and ledger. The frozen contract explicitly requires inherited gates. Future generation must retain the outer support excerpt on the dependent lookup. Binding compliance fails in all three runs. Useful text remains conditionally meaningful: support for asyncValidators errors using validation.messages entails availability of that setting. This implication is accepted for useful semantics, but cannot satisfy the explicit source-excerpt ledger contract. This refines, rather than waives, the preliminary concern.
4. **P2 — T18 run 3 drops supplied uncertain scope from global metadata.** `test-output/b3-r3-raw.json:78` sets `formly_version` to null although the request supplies `6.3.x or 6.4.x`; runs 1–2 preserve it. The question and ledger themselves retain the uncertainty. Semantic scope compliance fails; question-text correctness and ledger compliance pass. Future generation must preserve supplied uncertainty globally, rather than treating it as unspecified.
5. **P2 — T21 run 2 omits the custom-rule exclusion from its ledger.** `test-output/b3-r2-raw.json`, T21 `condition_bindings`, has only registered-status and no-mutation entries. Both question texts retain the exclusion, so useful semantics pass. The missing binding breaks the complete-ledger requirement. Future generation must bind the exclusion to both questions. The extra no-mutation condition on usage is explicitly permitted by the frozen interpretation and is not penalized.

No P0/P1 issue or actionable evidence-harness defect found. No failure is assigned for grounded extra name/context bindings, split/combined excerpts, harmless wording, or optional same-field history.

## Plan Review

The bounded plan satisfies the requested experiment: 24 newly authored realistic requests, three batches of eight, three repeats each, frozen inputs and unchanged candidate transport. Broader type/wrapper/validator/hook/expression/group/array topics coexist with empty and no-condition controls. All 72 responses were inspected against source and all rubric aspects, mandatory conditions, forbidden attachments and scope. The rubric allows natural alternatives and does not impose an exact question count. T03's missing support check is an aspect omission, not a three-versus-four question penalty.

T11's shared dynamic context and T17's explicit inherited outer gate were declared before generation. Their stable errors cannot be converted into success by relaxed posthoc criteria. T14 shared-object context, T19 optional hiding history and T21 redundant no-mutation context were accepted as declared. Plan ordering, isolated role boundaries, preserved failures and full denominators are appropriate. Final report/public summary and final evidence freeze remain parent-owned closeout work; the reviewer did not alter them.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status | Consequence |
| --- | --- | --- | --- |
| 24 requests, 9 batches, 72 slots | cases, all raw batches, reconstructed records | Confirmed | No missing/dropped slots |
| 12 frozen inputs and prompt-only/request-only packets | input-freeze hashes; exact packet comparison | Confirmed | Same frozen contract and assigned requests |
| No candidate/baseline/data changes | 33 inherited manifests, 38,342 hash entries; before/after snapshots | Confirmed for protected bytes | No semantic sealed inspection needed |
| Seven v5 and eight aggregation tests pass | Independent unittest executions | Confirmed | Structural transport/counting supported |
| Structural validation cannot prove missing constraints | validator source and failing semantic cases passing structure | Confirmed | Independent grades required |
| First submissions, fresh contexts, no unseen attempts | authorship/process records and saved artifacts | Not independently provable from files alone | Retain provenance limitation |
| Native role separation is not vendor independence or production accuracy | protocol and actual bounded design | Confirmed as limitation | No broader accuracy or latency claim |

## Verification Performed

Commands executed from repository root, with bytecode writes disabled:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v5 -p test_candidate.py -v`: 7/7 pass.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s poc/contextual-kb/agent_contract/v3_stress -p test_assess.py -v`: 8/8 pass.
- `PYTHONDONTWRITEBYTECODE=1 python3 poc/contextual-kb/agent_contract/v5_stress/preserve.py`: all 33 manifests and 38,342 entries pass. Entries can overlap. Payloads read as bytes only; no sealed cases/DB/weights interpreted.
- Inline read-only Python audit: input-freeze 12/12, raw-freeze 9/9, round1 and round2 3/3 each; three packet dictionaries equal exactly `{contract: frozen v5 prompt, requests: assigned source requests}`; nine raw batches each have the expected eight IDs; exactly 72 unique slots; all record objects reconstruct exactly from raw batches.
- Recomputed preservation snapshot equals both saved before/after-generation snapshots.
- Missing, malformed, valid and conflicting optional hints leave `question_plan` and `search_requests` unchanged on all 72 outputs. Valid and conflicting-span probes exercise all 66 nonempty outputs; the six empty outputs cannot have valid spans and were checked with empty/invalid hints. Conflicting hints are discarded; valid hints remain advisory. Output inputs stay unmodified.
- Reused `assess.summarize` with all 72 independently assigned grades; complete boolean grade schema and full denominators accepted.

Graph coverage was checked for all ten relied-on Python files (v5 candidate/tests/preserve, v4 preserve, v3 candidate, v3_stress assess/tests/audit, v5_stress preserve and base contract). All were `not_tracked`; conclusions use complete direct source reads, not graph completeness. The small unchanged harness separates schema validation, advisory hints and aggregation; no new dependencies, external data flow, performance mechanism or security-sensitive implementation was introduced. Root `npm run check` and Angular fixtures were not applicable: no indexing, packaging or runtime behavior changed.

## Scores

`semantic_pass` assesses useful requested meaning plus required global scope metadata. To avoid hiding the distinction, text-only success is also reported separately: T18 run 3 has correct question text but invalid global scope. `binding_pass` assesses complete active conditions on the represented questions; it does not silently stand in for requested-aspect coverage (T03).

| Repeat | Structural | Useful text only | Semantic incl. scope | Complete bindings | Both gates |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 24/24 | 23/24 | 23/24 | 22/24 | 22/24 |
| 2 | 24/24 | 22/24 | 22/24 | 21/24 | 20/24 |
| 3 | 24/24 | 22/24 | 21/24 | 22/24 | 20/24 |
| Total | 72/72 | 67/72 | 66/72 | 65/72 | 62/72 |

All-three useful-text success: 22/24 requests. All-three semantic-with-scope success: 21/24. All-three complete-binding success: 21/24. All-three combined success: **19/24**, not the required 24/24. Failing combined cases: **T03, T11, T17, T18, T21**. Ten failed response slots remain in the denominator.

Question-meaning stability: **23/24** (T03 differs). Ledger-meaning/attachment stability: **22/24** (T03 and T21 differ). Exact canonical whole-JSON equality: **2/24**, a separate measurement. T18's global metadata difference is a scope defect, not a question-text or ledger-meaning difference. Stable errors in T11/T17 are still errors. Redundant nominal bindings and equivalent excerpt segmentation do not count as material ledger instability.

## Open Questions And Residual Risks

Native model revision, temperature and seed are uncontrolled; within-batch contexts and repeats are correlated. This synthetic panel cannot estimate production success, establish retrieval usefulness or answer accuracy, or claim latency improvements. Files cannot prove unseen generation attempts or actual delivery beyond retained process evidence. The standalone support-check obligation in T03 is explicit in the frozen rubric/contract; an alternative looser interpretation would alter that subscore but cannot rescue the full gate because the other failures remain. T17 useful semantics accepts logical support implication while enforcing explicit ledger requirements, and this interpretation is recorded per response rather than hidden.

## Verdict

**Ready — as an evidence package reporting a failed experiment gate.** The frozen v5 candidate does **not** meet the all-24-by-three semantic-and-binding gate. Evidence readiness does not authorize deployment or claim production qualification. No heavy pivot is necessary to finish this reporting task.

## Recommended Next Actions

Retain the negative result and all raw outputs, incorporate these scores in parent-owned reporting, and freeze the resulting evidence. Do not tune against this panel or start a replacement review because the gate failed. This is review instance 1 of at most 3; a further review is reserved for a material harness fix, not unfavorable results. No fix or further workstream was launched.

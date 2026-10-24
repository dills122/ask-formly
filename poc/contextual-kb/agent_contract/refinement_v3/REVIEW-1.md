# Independent review — preliminary ledger

Review instance: 1 of 3. Fresh reviewer context; no implementation conversation inherited. Candidate/control labels are visible, so this is not blinded grading. AUTHOR-EXPLANATION.md has not been read at this point.

Scope is the untracked working-tree folder poc/contextual-kb/agent_contract/refinement_v3, with named read-only dependencies. Large unrelated dirty state is excluded. No sealed content inspected. Source fallback used; no graph completeness claim.

Preliminary review after tests, candidate.py, contracts, cases, rubric, and all 26 raw outputs:

- Common semantics provisionally pass all 13 outputs in each arm, including R01/H07. No candidate regression apparent. Each arm separates requested aspects, preserves correction/retraction, keeps local scopes local, and returns an empty N12.
- Candidate binding coverage and assignment provisionally pass all 12 nonempty cases; N12 correctly has no bindings. R01 and N08 use awkward pronoun-preserving excerpts but explicitly resolve the antecedent within the relevant question. N06 preserves both literal pairings within one comparison. N11 copies the no-inference instruction into the registration query, which is wordier but does not invent an aspect or change the requested registration.
- Exact-substring validation cannot prove completeness or attachment. This limit is explicit in contract/protocol; semantic review remains necessary. Empty or wrongly assigned ledgers can pass the mechanical check and must never be reported as complete merely because validation passes.
- Optional hints are copied and excluded from text-only search_requests. Overlapping candidates are all dropped. Structurally valid wrong-role hints remain unverified advisory data, as intended. Need independent unit tests, hash checks, and replay inspection before final verdict.
- One shared-context batch per arm has no repeatability or production qualification power, and the passing fresh control means this trial alone cannot show a comparative improvement over v2.

# Final independent assessment

Review instance: 1 of 3. Applied independent-review in reviewer mode and code-review-and-quality across correctness, readability, architecture, security, and performance. Working-tree base: main at c3091328f49d53de6b41a49c4fe5aa8f1c45e516. The review target is the new folder, not the repository's unrelated changes. The preliminary ledger above was persisted before reading AUTHOR-EXPLANATION.md.

## Findings

No actionable correctness defect found within this bounded candidate scope. All 26 saved outputs were independently read against the original requests and frozen rubric; this was not blind grading. Candidate audit coverage was assessed separately from common semantics and separately from substring validation.

| Arm | Structural outputs | Common semantic outputs | Fresh cases | Focused questions |
| --- | --- | --- | --- | --- |
| Unchanged v2 control | 13/13 | 13/13 | 12/12 | 23 |
| v3 candidate | 13/13 | 13/13 | 12/12 | 23 |

All 45 candidate bindings have correct assignment; all 12 nonempty cases have complete applicable condition coverage. N12 correctly returns an empty question list and binding ledger. No shared condition dropped, local condition leaked, explicit correction reverted, retracted condition restored, or requested aspect lost in these outputs. R01/H07 passes in both arms. Candidate R01 q0 and N08 q0 retain awkward exact pronouns but resolve them within their own question; these are meaningful conditional attachments, not substring-only passes. N06's initial-state sentence clearly applies to both comparison alternatives. N11's extra restriction wording preserves an explicit user exclusion without adding a new task.

Per-output criteria and rationale are retained in test-output/semantic-review.json. A passing current v2 control means this batch establishes no comparative semantic improvement over v2. The cached historical H07 omission is a real regression target, and its declared binding is rejected by the new validator; that is distinct from the current paired result.

## Plan Review

The implementation matches the authorized design: original derivation rules plus a shared-condition audit, exact source-anchored bindings, structural checks of declared targets, and an optional advisory hint envelope. Core validation happens before hints; malformed hints produce warnings rather than invalidate a valid plan. No retrieval, model loading, serving integration, or hard filtering is introduced. The base validator remains a same-POC dependency. No new dependency or external I/O surface is added.

The tests are proportionate to this small pure-Python component and include a frozen historical H07 omission. The absence of a semantic completeness algorithm is deliberate and documented; the review supplies semantic judgment for this panel only. The planned stop after one development comparison is appropriate. The parent should mark the plan and record results after incorporating this review; no new output generation or same-panel tuning is warranted.

Readability is compressed in candidate.py and test_candidate.py, but the small module's validation, transport, and projection responsibilities remain straightforward. The overlap scan is quadratic in hint count, which is acceptable for the measured bounded experiment; there is no deployment or unbounded-input performance qualification. JSON-compatible malformed values, wrong valid roles, exact duplicate spans, partial overlaps, and Unicode span offsets were independently probed. Structurally accepted role names remain suggestions, never verified semantic roles.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status | Consequence |
| --- | --- | --- | --- |
| v2 rules preserved with added audit/schema | Both contracts and candidate.py | Confirmed | No hidden derivation-rule removal found. |
| Declared source binding checked but completeness not inferred | validate, tests, all candidate bindings | Confirmed | Passing structure alone is not a semantic gate. |
| Hint transport cannot change core query or plan | build_plan, optional_hints, independent 120-row replay and 14 extra variants | Confirmed for tested JSON-compatible inputs | Advisory-only transport gate passes. |
| 13 tests and 26 structural outputs pass | Independent unittest discovery and reviewer-check.py | Confirmed | Mechanical checks agree with saved evidence. |
| 120 actual saved annotation rows preserve transport | Both usability60 extraction files, saved ledger, independent reconstruction | Confirmed | All 120 match; 294 input hints, 292 retained. This is transport evidence, not role-accuracy evidence. |
| Inputs/raw outputs and prior entailment artifacts unchanged | SHA-256 against input-freeze, raw-freeze, entailment final-freeze | Confirmed: 11 + 2 + 64 entries | No differences in independently checked subset. |
| All inherited protected entries unchanged | protected-before.json | Recorded author evidence; full inherited traversal not independently rerun | No blanket independent attestation of all 37,925 entries. Parent preservation check remains separate. |
| Isolation, no retries, case author exposure, and freeze-before-generation chronology | Protocol, packets, AUTHOR.md, raw outputs, manifests | Consistent supplied provenance; generation process not independently reconstructable from local outputs alone | Do not claim fully blinded or reproducible inference. |

## Verification Performed

- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v3 -p 'test_*.py'`: 13 tests pass.
- `python3 -B poc/contextual-kb/agent_contract/refinement_v3/test-output/reviewer-check.py`: both arms 13/13 structural pass; exact case ordering checked; 11 frozen inputs, 2 raw outputs, and 64 prior entailment artifacts match SHA-256; 120 transport rows independently reconstructed and matched; 14 additional hint variants preserve core plans and text-only requests. Unicode span acceptance also checked.
- Manual semantic review: all 26 outputs, all 46 focused questions, and all 45 candidate bindings checked against every case's expected aspects, shared/local conditions, prohibitions, and scope metadata. Results persisted in semantic-review.json.
- Source fallback used due reported graph transport closure; no graph coverage claim. No sealed contents, database, retrieval, baseline behavior, or production code changed. No responses regenerated, fixes applied, agents delegated, staging, or commits.

The replay program and its machine-readable result are retained as test-output/reviewer-check.py and test-output/reviewer-check.json. Unit tests were run directly and reported above; the historical RED log was not recreated by mutating candidate code. Root npm checks and Angular runtime fixtures were not run because indexing, packaging, and Angular behavior are outside this change.

## Open Questions And Residual Risks

One shared-context batch per arm, visible arm schemas, uncontrolled provider settings, and exposed development cases limit inference. This cannot establish repeatability, population accuracy, runtime Formly behavior, retrieval quality, final-answer correctness, or production readiness. Optional role accuracy was not evaluated. The exact-copy constraint can produce wordier standalone questions, as observed in N08/N11, without a measured retrieval impact. Empty or wrong-target binding ledgers can still pass structural validation; downstream use must preserve the distinction between declared-binding validation and semantic completeness.

## Verdict

**Ready** for the bounded candidate experiment and evidence handoff. Every predeclared local gate passes: H07 repaired, no fresh common-semantic regression, 13/13 candidate structural validation, complete/correct condition bindings on all 12 nonempty cases, and optional-hint transport invariance. This is not a production qualification or proof that v3 outperforms v2.

## Recommended Next Actions

Record the paired tie and the candidate-specific audit result, complete the parent preservation/reporting step, and keep these artifacts frozen. No heavy pivot, remediation, extra generation, or further review instance is required by this assessment. Any broader efficacy claim needs separately authorized fresh evidence beyond this exposed panel.

# Material datepicker candidate results

Candidate only: 104 facts /23 documents, five additions over installed99/22. Exact Formly6.3.12 Material scope. Candidate SHA256 `3f0f3036ad4fb0bb581234f3d1cbaebeb0a54be03a85ea6c9634ab26002c6e38`. Installed DB remains `8487ca97dde24daff0a9dc655111e0066b7f3ce0dccf7c65d81f6f6087fa3c6c`.

| Outcome | Installed99 | Candidate104 |
| --- | --- | --- |
| Usable answers each of3 repeats | 5/15,5/15,5/15 | 15/15,15/15,15/15 |
| Initial packet sufficient (including honest scope controls) | 5/15 | 14/15 |
| Existing feature/scope controls | 5/5 | 5/5 |
| MCP calls per repeat | 34 | 16 |
| Baseline-supported regressions | — | 0 |

All150 real MCP SDK stdio calls completed without operational/tool errors. Ninety lookup observations plus57 baseline discovery calls and3 candidate fetches. D09 initial candidate packet omitted the registration fact but exposed its ID in omitted_ids; get_formly_facts recovered it with the same scope. Baseline discovery inspected up to2pages of16 candidates per datepicker request (one request exhausted after page1); none supplied the missing datepicker contract. Bounds were retained, not silently expanded.

The calling agent in the implementation conversation supplied15 fixed full-question plans, assessed actual packets and wrote30 distinct arm/case answers in answers-baseline.json and answers-candidate.json. Every repeat's full structured outputs and tool arguments matched its arm's first repeat exactly, including follow-ups; those judgments were reused only after equality verification. These are NOT90 independent generations, a fresh planner benchmark, sealed evaluation or whole-library accuracy. Baseline no-evidence answers were safe but incomplete on D01-D10. D10 requires a supported adapter-boundary explanation, not just a bare refusal.

## Source and build gates
K13/K18/K19 bytes downloaded from pinned upstream commit match the existing catalog hashes. Five draft facts carry exact reference quotations, Material adapter and exact6.3.12 applicability. Schema2 lint passed. Build preserved all accepted rows across documents/facts/evidence/fact_evidence/fact_links/applicability/applicability_evidence/evidence_releases; foreign keys, source offsets, runtime eligibility and104/23counts passed. No compiler/catalog/reference or canonical authored edits.

## Review and tests
Prebuild review1 requested two P2 safeguards (require freeze before outputs; protect all transport sidecars). Both accepted and fixed in this batch with red/green tests. Review2 passed the corrected mappings, plan and nine tests. Four additional tests cover answer accounting, unseen citations and changed-repeat rejection; all13pass. Local `python3 tools/project.py check` passed. Final independent semantic/preservation review: **Ready**, no actionable findings; see [review](FINAL-REVIEW.md).

New result-audit code was written after the frozen run to enforce the already frozen criteria; it does not generate answers or change the cases, plans, claims or runtime. Its TDD failure and final-review artifact hashes are retained. Historical failed test invocations remain under test-output; no failing qualification observation was deleted or rerun.

## Limits and decision boundary
This qualifies library evidence delivery, not a rendered Angular datepicker or specific DateAdapter implementation. No universal parsing, model value type, locale/timezone/serialization behavior, month/year model-commit rule or new version coverage is claimed. Candidate meets the numeric admission gates and passed final independent review. Installation/promotion remains a separate user decision; both runtime implementations/manifests, models and installedDB are unchanged and evaluation stayed sealed.

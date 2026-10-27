# Public API/configuration result

The isolated **188-fact / 35-document** candidate adds 12 verified Formly 6.3.12 facts to the unchanged 176-fact baseline. The build preserves all eight canonical baseline tables and exact-version retrieval eligibility. The installed 124-fact DB, both runtime implementations/manifests and models remain unchanged. Evaluation remains sealed.

| Cohort | Baseline: 176 facts | Candidate: 188 facts |
| --- | --- | --- |
| Fresh API targets | 3/12 | 10/12 |
| Fresh configuration targets | 1/12 | 10/12 |
| All fresh positives | 4/24 (16.67%) | 20/24 (83.33%) |
| Preservation cases | 7/8 | 8/8 |
| Boundary controls | 8/8 | 8/8 |

These are the independently corrected scores. The original caller score was 5/24 versus 21/24; review found that both API-12 answers incorrectly described `updateInitialValue` as taking no argument. It accepts an optional model argument. [SCORE-ERRATA.json](SCORE-ERRATA.json) records the separate Partial correction. Original answers, packets and [results](test-output/results.json) remain untouched; [reviewed-results.json](test-output/reviewed-results.json) is the current scorecard.

Three identical-plan repeats produced identical packets. **432 actual stdio MCP calls completed with zero tool errors.** Both arms used the unchanged model-free runtime under its offline guard. No candidate case lost support that the baseline had, and review found no critical unsupported claims. The API-12 assertion is a noncritical factual error and is not credited as full support.

The four remaining delivered-evidence gaps are:

- API-09: the relationships between FieldType accessors and the underlying field configuration.
- API-12: the optional model argument to `updateInitialValue`.
- CONFIG-08: whether wrapper lookup exposes a suppression option.
- CONFIG-12: what happens when a named preset is absent.

**The frozen qualification gate failed in all three repeats:** 20/24 is below the required 22/24. The combined 36/40 count includes controls and preservation cases and must not be presented as meeting the positive-target 90% goal. No promotion was authorized or performed. Any follow-up must retain this run and use a separately frozen experiment.

The [source checklist](CHECKLIST.md), [API decisions](api/source-decisions.json) and [configuration decisions](configuration/source-decisions.json) enumerate additions, existing coverage and exclusions. Verification uses upstream commit `5f099fddea6426b46a453866adf0fede5be0bcd7`. Candidate DB SHA256: `6705f2733dd7c978338d400cf93ce0b2e74c42d7a117b532ea0802d7e92e40da`.

All 35 batch unit tests and the project maintenance check passed. Model-backed inference was not run. This is a bounded development diagnostic with fixed caller plans, not sealed evaluation, independently generated answers or whole-library accuracy. The prebuild review passed after correcting numeric-key lookup limits and aligning grading rules. The [final independent review](REVIEW-FINAL.md) closed as **Ready with non-blocking follow-ups for the completed experiment**, and **Not ready for promotion**. It confirmed the four gaps are missing knowledge contracts in the inspected candidate, rather than demonstrated ranking-only losses. One tooling follow-up remains: enforce the assessment seal automatically during report recomputation; all 282 sealed files were verified manually for this run.

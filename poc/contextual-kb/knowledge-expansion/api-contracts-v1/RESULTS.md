# Four API contracts: comparison result

The isolated candidate adds four source-verified facts, taking the unchanged188-fact baseline to **192 facts / 36 documents**. No evidence IDs, version coverage, runtime implementation, model or installed DB was changed.

| Cohort | Baseline188 | Candidate192 |
| --- | --- | --- |
| Fresh API targets |0/12|12/12|
| Fresh configuration targets |5/12|12/12|
| All fresh positives |5/24 (20.83%)|24/24 (100%)|
| Preservation cases |8/8|8/8|
| Boundary controls |8/8|8/8|

Initial lookup supported4/24 baseline positives and22/24 candidate positives; bounded recovery yielded the totals above. Three identical-plan repeats produced identical packets and scores. **399 actual model-free stdio MCP calls**, zero tool errors, offline guard active; no baseline-supported losses or critical unsupported claims. Fixed plans and repeated identical packets do not establish independently generated answer consistency or whole-library accuracy.

The frozen gate (at least22/24 positives, all preservation/control cases, no loss or critical claims) passes in all three repeats, confirmed by final independent review. Original failed public-api-v1 scores and API-12 erratum remain unchanged; this is a fresh test cohort.

The [source checklist](CHECKLIST.md) and [source decisions](source-decisions.json) cover FieldType getter forwarding/fallback, updateInitialValue optional/nullish arguments and clone limits, getWrapper signature/failure, and absent-preset substitution versus lookup/rendering. Eight upstream files were verified at exact Formly6.3.12 commit5f099fddea6426b46a453866adf0fede5be0bcd7. All eight canonical baseline table row sets are preserved. Candidate SHA256: `f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09`.

TDD verified the188 baseline change and mandatory assessment-seal validation; all40 unit tests pass. `python3 tools/project.py check` passed. Both runtime modes remain unchanged; model-backed inference was not run. Installed DB remains124 facts /27 documents; evaluation stays sealed. No promotion, commit or push was performed.

Prebuild independent review: Ready. Final independent review: **[Ready](REVIEW-FINAL.md)**, with no actionable findings or scoring corrections. The reviewer independently verified the semantic judgments, all40 tests, source/provenance preservation and full local maintenance checks. The final report recomputation validates all assessment and call hashes automatically before scoring.

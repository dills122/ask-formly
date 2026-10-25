# Model-scope candidate results

Status: complete. Independent review2: **Ready for the isolated candidate**. See [final review](REVIEW-FINAL.md). **The installed foundation remains at 56 facts.** This isolated candidate has 60 facts across 12 documents.

## What changed

Four reviewed facts from the already-imported configuration/model guide explain:

- Runtime links on built fields, versus raw field configuration and model/control state.
- Ordinary keyless groups sharing their parent model and control scope.
- Keyed groups exposing a nested model scope.
- Leaf `field.model` exposing its enclosing model, rather than its scalar value or necessarily the root.

K01/K05/K09 source excerpts match the pinned upstream archive. Existing shared-formState and callback facts were not duplicated. No compiler, schema, model, retrieval or selector changes were made. All previous knowledge rows are retained. The candidate references an additional evidence record already present in the catalog.

## Build and review

Six isolation/harness tests and combined authored lint passed. The prebuild reviewer identified one ambiguous test: M06 assumed a keyed address group without stating its key. The request was corrected before freezing, building or inference. The reviewer then cleared the source, cases and harness, and verified the built 60-fact/12-document DB, source offsets, foreign keys, original-row preservation and manifests.

## Frozen live qualification

Fifteen fixed requests ran three times against each DB: 90 real MCP calls. Each repeat includes ten model-scope requests, three knowledge regressions and two gap controls. Both arms use the promoted planner/capitalization/caller settings, frozen GLiNER seeds 1701/1702/1701, existing retrieval/selector and identical grading rubric. Arm order alternates. There were no retries or tuning.

| Repeat | Baseline | Candidate | Controls | Critical failures |
| --- | --- | --- | --- | --- |
| 1 | 6/15 | 15/15 | 5/5 in both arms | 0 |
| 2 | 6/15 | 15/15 | 5/5 in both arms | 0 |
| 3 | 6/15 | 15/15 | 5/5 in both arms | 0 |

Candidate: **45/45 usable answers**, including 30/30 targeted requests and 15/15 controls. Baseline: **18/45**, including 3/30 targeted requests and 15/15 controls. All 90 deliveries succeeded. Every predeclared per-repeat gate passed; missing results were never removed from denominators.

The independent reviewer audited all 90 final answers, raw events, delivered packets and grading inputs, and corroborated these scores. Each batch had one grading attempt. Honest limitations on a supported library question remained incomplete answers under the rubric.

The baseline already had some alternative support: M01's packet included runtime-link information in an existing source quotation, but its caller omitted that explanation. M07 successfully used that same alternative evidence. The result therefore includes a caller-use improvement as well as newly explicit scope knowledge; it is not solely a count of previously absent information.

## Equal-plan evidence

All **45 paired replays** succeeded. Baseline plans from repeats 1/3 were replayed against the candidate; candidate plans from repeat 2 were replayed against baseline. Normalized plans matched exactly. The existing hosted selector remained active.

Across each repeat, the candidate packet contained every listed required fact for all 13 support-bearing requests, compared with 3/13 for baseline. The two gap controls have no required fact IDs. These are exact-ID diagnostics, **not semantic coverage or final-answer scores**: alternative source quotations can support an answer without matching listed IDs. Both source and target packets remain available for audit.

## Preservation and limits

Final verification passed: 156 protected files, 21 input-freeze entries, 18 qualification-freeze entries and 81 foundation doctor pins. Installed DB hash remains `3a2024cf5fc22c7fdd6e70020d3f7c5c82e0a56a4000bb90928043cd5b418a09`; candidate hash is `2a370ac3b0e1b72104f7321d6904ac979924c6ec707d622b09d728565bc82ded`. Original rows and source offsets remain valid. All 135 recorded model-parameter checks and DB checks passed across live and paired calls.

Five live calls discarded overlapping advisory hints under the unchanged degradation policy. Full-question retrieval remained intact; these were not extractor availability failures. No model changes or sealed-evaluation access occurred.

This is a targeted model-scope qualification for the pinned Formly version, not whole-library or unseen accuracy. Some controls are exposed regressions. Hosted generation can vary. Live tests, paired replay and grading overlapped, so latency is descriptive only. The candidate is not installed.

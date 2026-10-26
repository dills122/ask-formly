# Isolated custom-type expansion results

Status: build, live qualification, scoring, equal-plan replay and final preservation checks complete. Final independent verdict: **Not ready for adoption under the frozen gate**; see [review](FINAL-REVIEW.md). No additional source, isolation or grading defect was found. The predeclared end-to-end gate did not pass.

## What was built

An isolated 56-fact/11-document candidate adds ten reviewed custom-type and registration facts to the installed 46-fact/9-document DB. Every original document, fact, evidence, evidence-link and related-link SQL row remains identical. Existing compiler/runtime code, planner, wording adapter, advisory GLiNER models, full-question retrieval and selector are unchanged. No installed-DB promotion or launch-path change occurred.

Candidate DB: `candidate-build/knowledge.sqlite`, SHA256 `3a2024cf5fc22c7fdd6e70020d3f7c5c82e0a56a4000bb90928043cd5b418a09`.

Installed DB preserved: SHA256 `3cdef0fc65e7afd747d3283adfdc47346ecfd64abd7d555d469fb982a2f84ea3`.

## Fixed qualification

Thirty fresh visible requests:20 custom-type, five unsupported-scope controls, five original-knowledge regressions. Both DB arms use real calling agents and real stdio MCP, repeated three times with matched GLiNER seeds1701/1702/1701. Questions and all behavior-bearing experiment inputs frozen before running. No tuning or replacement of failed calls. Existing sealed evaluation was not accessed.

| Repeat | Installed baseline useful /30 | Candidate useful /30 | Candidate custom-type /20 | Gap controls /5, each arm | Regressions /5, each arm |
| --- | --- | --- | --- | --- | --- |
| 1 | 11 | 30 | 20 | 5 | 5 |
| 2 | 11 | 24 | 14 | 5 | 5 |
| 3 | 11 | 30 | 20 | 5 | 5 |

All three repeats have zero critical unsupported-claim judgments. Candidate total84/90 (93.3%); baseline33/90 (36.7%). These pooled values do not override the per-repeat gate. Separate-context automated graders had arm identity withheld and no tools; deterministic delivery checks override their semantic decisions. The independent reviewer manually audited all90 candidate answers, including failures, and independently recomputed all180 expected delivery rows. This is bounded source-grounded answer usability, not population accuracy or Angular runtime qualification. Paired paraphrases and same-model-family grading limit generalization.

## Failures retained

- Repeat2 Q11–Q15: calling agent made no MCP calls and reported the tool unavailable. No server audit/runtime log exists. CLI stderr contains rollout state-DB warnings, which do not establish the cause. Five failed requests remain in the denominator.
- Repeat2 Q20: the planner produced a lowercase `an internal Formly source file exports TypeOption` ledger entry, while the original request begins uppercase `An`. The unchanged strict source-substring validator rejected it with `condition not grounded in source`. No retrieval ran. This is a wording/validation failure, not an unavailable knowledge claim.
- Repeat3 baseline Q20 also failed before retrieval with the same grounding error. It remains a baseline failure and a missing source plan in replay3.
- Development had four extra-argument caller-protocol failures despite adequate answers; see DEVELOPMENT-RESULTS.md. They were retained, and the test caller's argument instruction was clarified before qualification froze. No runtime fix was made.

The predeclared target is at least27/30 useful and18/20 custom-type in **every** repeat. Repeat2 fails that gate. A strong pooled score or knowledge-only success cannot change this decision after the fact.

Custom-type requested-aspect coverage in pool / original foundation packet / final packet (automated semantic judgments): baseline17.08/17.08/17.08% in repeats1 and2, and16.67/15.42/16.67% in repeat3; candidate100/100/100%,70/70/70%,100/100/100%. Missing delivery is zero coverage. These are rubric-based support fractions, not independent population-accuracy estimates. No repeatable control/regression loss was observed.

## Equal-plan comparison

Repeat1 replay:30/30 successful MCP calls with exactly identical normalized plans. Candidate indicative IDs cover every required set except Q17's wrapper-owner ID; the returned new Material fact directly covers the requested import/bindings/wrapper and retains the ownership limit. Exact-ID differences are diagnostics, not semantic failures. Independent review confirmed this equivalent support.

Repeat2 replay:24/24 available source plans successfully replayed with exact equality; six missing original source plans Q11–Q15/Q20 remain missing. The only candidate indicative-ID miss is again Q17 with equivalent Material support. Repeat3 replay:29/29 available plans successfully replayed with exact equality; baseline Q20 is missing. Candidate Q17 again uses equivalent Material support. Total83 successful equal-plan comparisons out of90 expected; seven original source plans are missing, with no replay tool failures. Missing original source plans remain in the90 expected replay cases rather than being generated or removed.

## Timing and preservation

Repeat1 warm MCP median: baseline12.36s, candidate12.10s; p95 baseline18.30s, candidate17.82s. Cold-call median:23.85s versus24.09s. First live repeat completed before grading/replay overlap. Later timing is descriptive under concurrent hosted work, not a controlled SLA. Calling-agent answer-composition time is separate from these MCP timings.

Successful-call warm median/p95 seconds by repeat (baseline → candidate): repeat1 12.36/18.30 →12.10/17.82; repeat2 12.58/21.30 →12.46/27.01; repeat3 11.63/17.28 →12.19/20.35. No repeat exceeds the provisional20% warm-median increase flag. Later tail differences are not controlled performance estimates. `test-output/qualification-1/runtime-summary.json` separates175 delivered tool calls, two tool failures and five missing calls:173 successful MCP packets total, including84 candidate packets. No successful call reported degraded advisory extraction; all saved DB and parameter preservation checks were true.

Independent audit verified31 harness tests, all16 frozen input hashes, accepted preservation hashes, original SQL-row superset, source offsets and the fourteen added evidence excerpts against the pinned upstream archive. Accepted project checks also passed. The final preservation sweep also passed:16 frozen file hashes,75 foundation pins (including weights/adapters), unchanged installed DB and original SQL rows/offsets. Final independent review confirmed the result and failed-gate decision.

## Follow-on scope

The knowledge expansion shows a large useful gain; operational qualification is not yet a pass. A twelve-claim proposal for the remaining imported-guide gaps is prepared separately at ../imported-guides-v1/PROPOSAL.md, with pinned evidence. No second candidate was built. Do not promote this DB or infer that missing-tool access and strict planner failures have been fixed. Existing setup, models and installed DB remain the rollback foundation.

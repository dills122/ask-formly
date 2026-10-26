# JSON Schema batch results

**Not qualified for promotion.** The six new facts improved the targeted answers,
but the fixed run failed delivery and assessment completeness requirements.
Installed foundation9 remains 93 facts/21 documents; isolated candidate is 99/22.

| Repeat | Candidate usable (independent audit) | Baseline usable |
| --- | --- | --- |
| 1 | 15/15 | 5/15 |
| 2 | 15/15 | 5/15 |
| 3 | 11/15 | 1/15 |

All 90 raw answers were inspected independently. The final repeat's C01/C02/C03/C05
hit 180-second planner timeouts in both arms (eight failures). C04 passed both arms.
No critical fabricated answer was found. These failures remain in the denominator.
The evidence does not isolate why hosted calls slowed; concurrency and service
conditions are possible factors, not established root causes.

The automated assessor also timed out after 300 seconds on r3-b2-candidate. Its
fixed summary therefore records candidate 15,15,5 and baseline 5,5,0; missing grades
are not silently replaced by the independent scores above. qualification-decision.json
fails explicitly. No retry, tuning or discarded failed case was performed.

Raw inventory: 18 caller jobs,90 answers,82 successful packets and8 failed calls.
Successful whole facts, applicability and citations match the corresponding DB.
The first matched-plan replay completed15/15 without MCP errors; remaining30 were
stopped after the failed primary gate. Replays are incomplete diagnostics, not
additional answer scores or evidence that the overall run qualified.

Nine harness tests and local project maintenance passed. The six claims were checked
against pinned upstream service/test/demo bytes. Upstream Angular tests were read,
not executed. The paragraph checklist maps explicit claims only, not all assertions
in a mapped paragraph. All new applicability is exactly6.3.12; the registration demo
uses Bootstrap and does not establish a complete Material renderer recipe.

Candidate DB SHA256: `8487ca97dde24daff0a9dc655111e0066b7f3ce0dccf7c65d81f6f6087fa3c6c`.
Installed DB SHA256: `a0f102f1bad83dfec7c91148925187644e3092a3ca08cdaa88f586a7e1a0c106`.
All769 frozen baseline source/runtime/model pins remain unchanged. Evaluation sealed.
No promotion, commit or push performed. See REVIEW-FINAL.md for independent verdict.

Next: investigate hosted-call timeout/availability separately, then freeze a fresh
qualification run with retained failure history. Do not revise the knowledge facts
merely to address a delivery outage, and do not promote from two successful repeats.

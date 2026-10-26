# JSON Schema final independent review

Review instance: 2 of 3. Repository HEAD 8e8d02e82c01e3f0e6e0b74a31b8c7346ca22830, branch codex/versioned-knowledge. Reviewed the untracked json-schema-v1 batch. Preliminary findings were written before reading REVIEW-FINAL-AUTHOR.md. No implementation fixes, hosted calls, retries, sealed evaluation reads, staging or publication were performed by this reviewer.

## Findings

**P1 — The completed qualification fails mandatory delivery and control gates.** In `test-output/qualification-1/r3-b3-candidate/answers.json`, C01, C02, C03 and C05 report planner timeouts. Their corresponding MCP audit files record `TimeoutExpired` after 180 seconds, and completed MCP events have failed status. The baseline has the same four failures. Candidate repeat 3 is independently usable at only 11/15, below the frozen 14/15 requirement, and four required controls fail. `qualification-cases.json:criteria` requires zero delivery failures. These are retained failures, not grounds to remove observations or change the denominator. The smallest credible next step is to preserve this failed run, investigate hosted-call availability separately, and obtain authorization for a fresh frozen qualification; do not promote this candidate from this evidence.

**P2 — Assessment and matched-plan evidence are incomplete.** Only 15 of 18 jobs have completed assessor reports. The sixteenth assessment attempt, r3-b2-candidate, timed out; neither final control job was graded. The fixed automated summary correctly retains these missing assessments as failures. Only paired-r1 completed its 15 observations; paired-r2 has no completed result and paired-r3 did not start. The closeout records intentional interruption after the primary gate failed. This is an explicit plan shortfall, not evidence of a successful 45-observation replay. No additional diagnostic calls are needed to establish the present failed verdict; any future qualification must define and complete its evidence obligations separately.

No actionable defect was found in the six authored claims, candidate row preservation, or successful answers. The timeouts do not establish a knowledge defect or isolate a provider, concurrency or runtime root cause.

## Plan Review

The isolated knowledge scope is implemented: six facts in one core document produce 99 facts / 22 documents, retaining the installed 93 / 21 baseline. All eight versioned tables preserve every baseline row; foreign keys and source offsets pass. New applicability remains exactly 6.3.12. Pinned converter source supports cloning, one-field return shape, widget merge before templateOptions alignment and map, map's return contract, local reference chains, missing-definition errors and remote URI rejection. The inspected renderer registration demo uses Bootstrap; the facts and answers do not claim a complete Material recipe.

All 18 retained-guide paragraph hashes match. The checklist accounts for each paragraph while admitting only six explicit claims; it does not establish all assertions in mapped paragraphs or whole JSON Schema coverage.

The fixed 18-job schedule ran once with 90 answers, 15 cases per arm per repeat, seeds 1701/1702/1701. Cases, criteria and frozen behavioral harness bytes remain unchanged. Both arms use the same accepted components with checked DB selection. The post-freeze raw audit helper is analysis-only; its later error-record handling preserves failures without altering the tested inputs. Primary inference completed, but qualification failed and replay was intentionally curtailed. No promotion is within this review's authorized scope.

## Independent Answer Audit

I read all 90 raw answers, their cited facts' claims, conditions and limits, and checked support against the actual delivered packets rather than only assessor grades or citation IDs. The following ledger applies to each case separately across its three repeats. P = usable under the frozen delivery rule; F = incomplete or failed delivery.

| Case | Candidate repeats 1/2/3 | Baseline repeats 1/2/3 | Independent basis |
| --- | --- | --- | --- |
| J01 | P/P/P | F/F/F | Candidate names API/import and one-field versus array shape; baseline lacks converter evidence. |
| J02 | P/P/P | F/F/F | Clone and conversion-versus-serialization boundary supported; baseline explicitly lacks both. |
| J03 | P/P/P | F/F/F | Separate registration and bounded Material coverage; baseline supplies only general registration evidence. |
| J04 | P/P/P | F/F/F | Four structural registrations and Bootstrap limitation present; baseline cannot identify demo setup. |
| J05 | P/P/P | F/F/F | Widget merge, alias assignment, then map; baseline general alias fact does not establish ordering. |
| J06 | P/P/P | F/F/F | Callback return becomes mapped field; baseline honestly lacks contract. |
| J07 | P/P/P | F/F/F | Root-local traversal, chains and missing-definition throw, with pointer/cycle limits; baseline gaps. |
| J08 | P/P/P | F/F/F | Remote URI rejected without fetching; baseline gaps. |
| J09 | P/P/P | F/F/F | All three requested contracts supported; baseline gaps. |
| J10 | P/P/P | F/F/F | Reference and renderer limits retained; baseline cannot cover requested converter specifics. |
| C01 | P/P/F | P/P/F | Defined false/zero retained; final repeat has no successful packet. |
| C02 | P/P/F | P/P/F | resetOnHide:false with control-tree limit; final repeat has no successful packet. |
| C03 | P/P/F | P/P/F | Strict object identity and conditional comparator/scalar advice; final repeat has no successful packet. |
| C04 | P/P/P | P/P/P | Explicit private-file knowledge gap; no fabricated path. |
| C05 | P/P/F | P/P/F | No v7/migration guarantee; final repeat timeout fails delivery despite cautious prose. |

Independent totals: candidate **15/15, 15/15, 11/15**; baseline **5/15, 5/15, 1/15**. No critical fabrication was found. The automated totals remain separately **15,15,5** and **5,5,0**, because missing grades are not replaced with this review. No baseline-supported regression was observed in the paired results; shared failures still violate the other gates.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status | Consequence |
| --- | --- | --- | --- |
| Six pinned, bounded facts; no expanded release coverage | Draft facts, cached upstream source, source map, DB applicability | Confirmed | Authoring scope supported |
| Candidate preserves baseline and frozen inputs | Eight-table comparison, 769 baseline pins, DB/input/freeze digests | Confirmed | No installed/model drift detected |
| Fixed real-caller schedule and identical components | Harness, all 18 command/receipt/prompt files and 90 MCP event sequences | Confirmed | Complete primary denominator established |
| Nine tests and maintenance passed | Independently executed unittest discovery and project check | Confirmed | Offline maintenance passes |
| Grader assesses delivered support | Grader contract, assessment preparation and raw packet checks | Confirmed as design; incomplete execution | Missing reports remain failures |
| Qualification and replays were running | Final packet was written before completion; final results/closeout reviewed | Historical statement | Superseded by failed run and incomplete replay |
| Earlier RED/GREEN sequence and upstream fetch history | Current tests and cached pinned bytes | Historical sequence unverified | No verdict depends on that testimony |

## Verification Performed

- MCP environment: `python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/json-schema-v1 -p 'test_*.py'`: nine tests pass.
- `python3 tools/project.py check`: exit 0; source checks, 95 doctor pins and active regressions pass. This command did not perform hosted inference or access sealed evaluation.
- Independent read-only raw audit: exactly 18 jobs, 90 answers; saved answers equal final caller event JSON; prompts, order, model gpt-6-astra, medium effort, arms and seeds match. There are 82 successful packets and eight failed MCP completions. All successful delivered packets equal their saved audits; their whole fact and citation objects equal DB-derived values, including applicability. Citation membership and runtime preservation checks pass. Synthetic one-dimensional embeddings were used only to construct metadata, never ranking or quality evidence.
- Independently reproduced summary and evaluator from retained assessment outputs: exact equality with saved reports; decision is false. Verified all 90 review-packet projection records against original cases, raw answers and audits, including error rows. Raw audit has 90 observations and eight errors.
- Inspected all 15 completed paired-r1 results: normalized plans equal source plans, no MCP errors, expected supporting facts are delivered. Round 2 has zero completed results; round 3 is absent. No claim of 45 completed replays is accepted.
- Rechecked candidate/installed DB digests, input/freeze hashes, five cached source hashes, 18 paragraph hashes, 769 baseline file pins and eight-table preservation. All pass.

Graph metadata had no indexed batch symbols and exact-path coverage reported untracked files. Direct source reads supplied verification; no completeness claim relies on the graph.

## Open Questions And Residual Risks

The timeout root cause is unresolved. Completed targeted answers are encouraging but do not establish reliable service delivery, unseen accuracy, broader JSON Schema compatibility, Material rendering integration or another Formly release. Upstream Angular tests were read, not executed. Incomplete assessor/replay evidence remains incomplete even though the primary failure is decisive.

## Verdict

**Not ready.** The isolated candidate's authoring and preservation are sound within the reviewed scope, but the planned qualification failed. Do not label the candidate qualified or promote it. RESULTS.md and run-closeout.json accurately retain this distinction and the failed observations.

## Recommended Next Actions

Preserve the frozen candidate and complete failed-run history. Investigate timeout/availability evidence separately before proposing a fresh qualification. Do not tune facts, relax gates, retry this run, substitute independent scores for missing automated grades, or promote from the two successful repeats. One review instance remains under the maximum of three; this reviewer starts no further instance.

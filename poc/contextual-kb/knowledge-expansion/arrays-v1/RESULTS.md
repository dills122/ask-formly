# Arrays candidate results

**The six-fact knowledge addition performed well, but the fixed integration qualification did not pass.** The candidate scored 44/45 usable answers (97.8%); one existing typing control failed planner validation before retrieval. No promotion occurred. [Final independent review](REVIEW-FINAL.md): **Not ready for fixed integration qualification**. Source, build and preservation checks passed.

The isolated candidate contains 85 facts across 19 documents, versus the unchanged installed 79-fact baseline. It adds array templates/children, coordinated add/remove, falsy initialModel, narrowly described upstream test assertions, and the official repeater example. All six upstream files match pinned Formly 6.3.12 hashes. No upstream Angular suite was executed.

Candidate SHA256: `bbb55e168cc81e60927a1bf146af767cd8ab6c9999875239ea28a879487531ff`. All five knowledge tables preserve accepted rows and reproduce independently. Retrieval eligibility includes all six additions.

## Frozen live comparison

| Repeat | Seed | Baseline usable | Candidate usable | Candidate controls |
| --- | --- | --- | --- | --- |
| 1 | 1701 | 5/15 | 15/15 | 5/5 |
| 2 | 1702 | 5/15 | 14/15 | 4/5 |
| 3 | 1701 | 5/15 | 15/15 | 5/5 |

All 30 candidate targeted-array answers passed, versus 0/30 baseline answers that honestly reported evidence gaps. All 15 baseline controls passed. Independent review audited every one of the 90 answers and agreed with automated grades. No critical invented behavior was found.

The numeric candidate score met the frozen minimum of 14/15 per repeat. The same predeclared gate also required every control, complete delivery and no baseline-supported regression. Q20 in repeat 2 failed those gates; the frozen evaluator returned `qualified:false`. This is one underlying failure, not three separate incidents. There was no retry, tuning, case rewrite or threshold relaxation.

## Q20 failure and diagnosis

The user request begins “An internal Formly source file exports TypeOption” and asks whether that establishes a public import and for a public typing alternative. The saved planner response is valid JSON, but its condition ledger lowercases source-initial “An” to “an” and has empty `question_indexes` for that condition. The runtime rejected it with `condition not grounded in source` before retrieval. The caller's description of a JSON parsing problem was not the actual root cause.

A read-only diagnostic reproduced the original rejection; changing capitalization only in a deep-copied plan still produced `invalid question indices`. Thus a capitalization-only fix would be insufficient. The plan's questions paraphrase the internal-export concept, but its required condition binding is invalid. No runtime or saved-plan correction was applied.

Both other live candidate Q20 answers passed. Replay of the valid repeat 1 baseline Q20 plan against the candidate also retrieved `custom-type-recipe-core/public-registration-type`. These results locate the observed failure in the planner/validation path, not in the six new facts. They do not waive the failed integration gate.

## Recorded interpretation

A08's exact source assertion is `field.model === ['default', null]` after the stated fixture setup, add(0) and change detection. All three candidate answers showed `{foo: ['default', null]}` as a root-model representation. Review accepted this because the array contents/order and source-inspection-only limit were correct and none called the wrapper object `field.model`. This acceptance is recorded rather than silently changing the question or rubric.

## Verification and limits

- Independent source/prebuild review passed; bounded mapping corrections preceded input freeze.
- 16 batch tests passed, with meaningful count-guard red/green evidence retained.
- Local maintenance passed 128 source tests, 114 runtime tests and 86 doctor checks.
- Source/build and qualification freezes cover 28 artifacts; candidate reproduction matches all five tables.
- 44 saved-plan replays completed successfully, with exact normalized plans preserved. The failed repeat 2 Q20 source plan remains one missing slot in the fixed denominator of 45.
- Candidate replay retained all required diagnostic IDs in both 15-case baseline-origin rounds; baseline replay retained them in 4/14 completed candidate-origin cases. These are ID-coverage diagnostics, not final-answer scores.
- All 167 protected files and all 28 frozen artifacts remain unchanged. All 133 successful live/replay packets report unchanged DB and model parameters.
- Live advisory status: 73 available, six not needed, ten degraded. Selection: 82 unchanged, six not needed, one repaired. These counts cover the 89 successful packets; the failed Q20 call stopped before retrieval. Full-question retrieval preserved usable targeted answers despite advisory degradation.

Three repeat streams ran concurrently, so timings cannot establish comparative latency. Visible targeted qualification is not whole-library or sealed evaluation. The detailed default/insertion case measures knowledge of specific source assertions, not application execution. Bootstrap presentation is not a verified Material recipe. Installed knowledge, models, runtime, compiler, original source and sealed evaluation remain unchanged. The candidate remains isolated and uncommitted.

The next bounded work should address the invalid planner condition binding in a separate runtime candidate and run a new fixed qualification. Do not alter the verified arrays facts to hide this delivery failure.

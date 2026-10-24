# Independent focused-v2 review

Reviewed `run.py`, `score.py`, and `test_score.py` against `PROTOCOL.md` after completing blind reference annotations. Reference labels were not changed after prediction inspection. Review scope was the POC experiment; no database or sealed evaluation access.

## Findings and resolution

- **Resolved:** Missing prediction rows previously aborted scoring. The scorer now iterates expected input IDs and passes absent rows to `prediction`, producing empty predictions and a reported failure. Gold entities therefore remain false negatives.
- **Resolved:** Malformed output/request containers previously failed before the exception handler. Container checks now run inside `prediction`; regression cases cover null/list outputs, null entities, and null request records.
- **Resolved:** Required diagnostics were missing. Scores now include interpretation-label counts, per-parent/arm extraction seconds, input counts, and explicit agent abstention for H11's empty focused arm.

The runner preserves the fixed final epoch-8 adapter, model/schema separation, threshold, exact supplied questions, sequential model execution, and raw outputs. Its existing loader supplies CPU float32, four threads, and seed 1701. Shared unique typed-text atoms are deduplicated per parent, separately from exact-offset entity metrics.

## Verification

Independently reran all eight scorer tests: passed. Inspected the saved RED/GREEN logs; RED is the expected missing-helper import failure before implementation. Checked all four raw output files against regenerated diagnostics: 90 rows per cell, 360 total, zero reported failures. Summed parent timing agrees with arm timing. H11 is explicitly marked as agent abstention in every cell.

Raw top-level `request` arrays contain **2 records for base/full** and **1 record for adapted/full**, agreeing with the score report; entity-only cells contain none. Both full-schema cells report 76 `needs_clarification` and 14 `clear` labels. These are output counts, not accuracy. No full-frame gold exists, and neither counts nor entity scores establish request correctness, polarity, attachment, completeness, or answer quality.

No remaining blocking finding in the reviewed experimental path. Failure-handling changes do not affect metrics for these complete, valid saved predictions. Reference labels remain agent-authored and preserve recorded ambiguity; this review does not promote them to expert-human ground truth.

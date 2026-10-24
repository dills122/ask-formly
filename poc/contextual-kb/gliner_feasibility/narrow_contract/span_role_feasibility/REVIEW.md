# Independent review — span-role feasibility

Review instance: 1 of 3. Reviewer read fresh gold before harness or author notes. This is a pre-comparison readiness checkpoint; results review remains pending in this same instance.

## Findings

No outstanding blocker for running the frozen feasibility comparison. During preflight, malformed native attribute objects could raise instead of abstaining; the worker corrected parsing and retained RED/GREEN evidence. Missing tail records could truncate paired audits through zip; the worker added an explicit equal-length guard. These corrections occurred before fresh inference.

## Plan Review

The protocol separates zero-shot GLiNER attributes from a trained spaCy classifier and explicitly disclaims intrinsic-library superiority. Both frozen seed1701/1702 extractors must pass the replacement gate. Exact-span competing candidates alone may be filtered; partial overlaps, missing/negative/noncandidate roles and uncertain scores abstain. The public native call can alter extracted spans, so its output is diagnostic and baseline candidates remain authoritative. Gold offsets augment only typing diagnostics, not resolver candidates. Full qualification is separate from relative improvement.

Fresh gold was reviewed independently first: 40 unique cases, 101 exact zero-based half-open mentions, six empty cases, eight families of five, internally consistent role/opaque-expression annotations. No semantic correction was requested. The author notes were read afterward and agree with inspected artifacts. No old sealed evaluation data was read.

## Author-Claim Reconciliation

| Claim | Evidence | Status |
| --- | --- | --- |
| TRAIN-only spaCy, 194 questions | spacy_arm.py and training receipt | Confirmed implementation/receipt; prior training provenance inherited |
| 488 positives, 2755 negatives, no alignment loss | training receipt/alignment file | Confirmed |
| Save/reload parity | exact equality of spacy-save-before/after JSON | Confirmed for eight training cases |
| Negative class is final column | installed spaCy 3.8.16 spancat.py, labels/negative-label/predict source | Confirmed version-specific source contract; runtime calls public predict |
| Frozen extractor identity | both smoke parameter maps equal original final_hashes, before equals after | Confirmed |
| Native public attribute output | both three-question training-only smoke outputs | Confirmed target_role label/confidence shape; top-only limitation retained |
| Candidate-only mutation/no gold in resolver | policy.py and assess.py | Confirmed by code and focused tests |
| Prior216 baseline reproduction and paired gates | run.py and assess.py | Implemented, actual execution pending |

## Verification Performed

Independently ran `python3 -B -m unittest discover -s poc/contextual-kb/gliner_feasibility/narrow_contract/span_role_feasibility -p test_policy.py`: 7 passed. Independently ran planner_env/.venv/bin/python with PYTHONDONTWRITEBYTECODE=1 and -B on test_spacy_arm.py: 2 passed. Checked all fresh mention slices, spaCy save parity, and both original/smoke parameter maps. Reviewed the existing pilot strict envelope/scorer to verify downstream boundaries are reused without semantic repair.

## Open Questions And Residual Risks

Native returns only a top role/confidence; full ties or alternatives cannot be audited from that output. The >0.5 rule is conservative, not calibrated. spaCy learns from simplistic single-token negatives and no pretrained vectors. Save parity covers training examples only. Small fresh families and previously exposed diagnostics establish bounded feasibility, not broad qualification. Results must retain every failure, drift, alignment gap, and lost correct mention; aggregate typing/qualification reporting and actual ledgers still require review.

## Verdict

Ready for the frozen comparison only. No conclusion about either arm passing its replacement or qualification gate is made before results.

## Recommended Next Actions

Freeze implementation, protocol, fresh gold, model artifacts and protected inputs; execute both extractors and both arms once; report separate fresh/diagnostic results and native span drift; return actual scores/ledgers and completed narrative for final review in this same instance. Do not tune after fresh inference.


# Final results review — same instance 1 of 3

## Findings

No outstanding implementation/reporting blocker for this completed feasibility experiment. Neither candidate is ready to replace the baseline: both fail the predeclared paired gate on seed1702. This negative result is retained, not repaired or tuned away. The earlier preflight verdict authorized measurement only.

The decisive observed failure is fresh srf-026: the frozen extractor proposes oversized, identically bounded API/value alternatives. Native retains the API role and spaCy retains the value role, but both boundaries are wrong. Removing one alternative converts an invalid envelope to a valid wrong envelope. Fresh accepted F1 falls from 0.940594 to 0.931373 for both arms, even though zero correct raw mentions are lost. The gate correctly rejects both arms. Native also has no correct conflict resolution for seed1702.

## Plan Review

Both seeds completed all 256 cases, with fresh40 separate from prior216 diagnostics. No seed selection occurred. Both candidates pass the seed1701 relative gate; neither passes the paired gate. The Material registration conflict improves under native1701 and spaCy both seeds. The placeholder challenge conflict remains unresolved for seed1701. Full qualification independently fails: fresh API/adapter/version role metrics fall below 90% in applicable seeds, and each arm/seed misses one of 19 compound API spans and three of 34 quoted spans. No production adoption or broader compatibility claim is supported.

## Author-Claim Reconciliation

| Final claim | Independent evidence | Status |
| --- | --- | --- |
| All 432 prior baseline outputs reproduce | Compared each original and current output for both seeds | Confirmed |
| All scores/gates reflect stored outputs | Recomputed all 42 complete score objects with frozen pilot scorer | Confirmed exact equality |
| Zero raw-correct loss and nonconflicting changes | 1024 ledger rows plus direct original/resolved entity-object comparisons | Confirmed |
| Native errors zero; alignment failures zero | 512 audit rows | Confirmed |
| Model/input preservation | Both parameter maps equal original receipts; rehashed all 367 run-freeze entries | Confirmed |
| Protected 36,899 checks unchanged | Reviewed corrected resolver and retained receipt; full protected scan not independently repeated | Receipt-supported; original false-failure preserved |
| Native span drift 3/4 cases | Independently compared baseline/native spans per seed | Confirmed: dropped 2/3, added 2/2 |
| Fresh typing spaCy 97/101 versus native 44/101 and 53/101 | Independently counted typing.json | Confirmed; native coverage only 96/101 and 95/101 |
| Prior typing spaCy 526/565 versus native 227/565 and 278/565 | Independently counted typing.json | Confirmed; exposed diagnostics, not fresh evaluation |

## Verification Performed

In addition to preflight checks, independently recomputed every score object without rerunning inference, compared all prior baseline outputs, verified all model hashes and frozen inputs, counted drift/errors/alignment/typing/lost mentions, and checked preservation of every nonconflicting entity object. Read RESULTS.md after inspecting actual outputs and ledgers. Requested clarification that native full re-extraction and spaCy supplied-span typing are different timing workloads; the worker corrected that report text.

## Open Questions And Residual Risks

Training inequality prevents an intrinsic library ranking. Native top-only outputs do not expose full distributions, and schema extension changes extraction. spaCy's perfect training fit and high gold-span typing accuracy do not establish rejection of malformed candidate spans. Gold offsets appear only in typing diagnostics and cannot be treated as deployable candidate coverage. The same spaCy gold-span predictions across pairings are not independent replications. Proposed richer negative training is future work, not a validated remedy.

## Verdict

Ready as a completed, accurately reported feasibility experiment. Not ready for adoption: preserve both frozen extractors and current production behavior. No additional review instance or implementation pivot was started.

## Recommended Next Actions

Retain the first outputs and negative decision. Any future boundary-rejection or attribute-training experiment requires its own approved scope and fresh evaluation; do not tune these candidates on the current fresh cases.

Supplemental fresh opaque-boundary inspection: srf-031 through srf-035 preserve each complete expression value and maximal API path exactly under both baselines and both resolved arms (5/5 per seed/arm). This bounded fresh-family check does not establish exhaustive opaque-boundary qualification across all diagnostic formats; the separate numeric/quoted/compound failures already reject full qualification.

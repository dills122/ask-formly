# Independent review

Review instance: 1 of 3. Scope: this new directory only. Read-only inspection
except this review report; no training, inference or sealed-evaluation reads.
Working-tree scope is untracked POC work on main at
`c3091328f49d53de6b41a49c4fe5aa8f1c45e516`; numerous unrelated dirty paths are excluded.

## Preliminary blind inspection

Read root and POC instructions, STEERING.md, narrow CONTRACT.md, then the new
protocol and all forty fresh questions and annotations before new training
questions, author rationale or predictions. Prior protocol/runner/review were
read as frozen context. No actionable semantic defect found in fresh gold.
Checked occurrence-specific roles, ordinary type/key/wrapper nouns, explicit
configuration properties, quoted registration/key/literal distinctions, repeated
surface forms, maximal compound paths, complete opaque expressions, Markdown
exclusion, version tokens and negated adapter mentions. Array-form model keys
are represented as one complete supplied key value, consistent with the contract.
Mechanical source-slice, ordering and non-overlap checks pass.

Fresh SHA256: `98f39e5d2d897ac8088e1331a70e0aa6c61098f8c54f3c1f235641373052e217`.
Six questions are empty; eight families contain five each. Role counts are API42,
value16, registration19, adapter6, model-key15 and version6.

## Findings

Subsequently read all194 training questions and annotations. No actionable gold
defect found. Combined training equals frozen prior146 plus new48 exactly;
all194 questions are unique and all source slices/order/non-overlap pass.
Fresh/training registration and model-key sets are disjoint even after removing
quote delimiters. Shared APIs/concepts are expected; this does not establish
unseen-API generalization. Training194 SHA256:
`e443b176bc43f0d8d2ab4fb1eb7b3c579eb70ef60341392a98de6c8386021290`.

## Plan Review

Protocol and runner agree on both vocabulary epoch6 continuations, six fixed
epochs, 25 updates per epoch/150 total, AdamW reset at 1e-4/.01, clipping1,
serial chunks8 with final2 divisor, deterministic CPU float32/four threads,
same six labels and flat .5 decoding. Inference receives question strings only.
No regex repair, deduplication or suppression is introduced. Only LoRA parameters
train; frozen hashes and exact initial checkpoint hashes are verified. Epoch1/6
save/reload checks use fixed training last8 and restore RNG states. Native
transport preflight receipts cover all194 rows for both seeds. These receipts
were inspected, not independently rerun with the model.

The gate uses accepted fresh API recall, requires both seeds and >=2-point F1
gain, and compares diagnostics against both vocabulary and earlier challenge-flat
scores where available. Every diagnostic must have zero invalid outputs; this
prevents treating inherited vocabulary invalids as acceptable. The frozen prior
scoring input is verified by the vocabulary final-freeze before inference.
No checkpoint selection or evaluation during optimization is present.

## Author-Claim Reconciliation

No separate author rationale was available before the blind pass. Worker claims
of194 examples, exact replay, four passing tests, initial checkpoint/target parity
and dual-comparator diagnostic gate agree with inspected files. Authoring
independence remains process testimony, not a property provable from file bytes.
Read AUTHOR-NOTES.md only after the blind gold/harness review. Its104 mention
count, family distribution, six empties and boundary decisions match the gold
and independent inspection. Its no-output/no-training-read authorship account
is consistent with the delegated process; no file-based verification can prove
that negative statement.

## Verification Performed

`python3 -B -m unittest discover -s poc/contextual-kb/gliner_feasibility/narrow_contract/role_boundary_adaptation -p test_policy.py`
passes four tests. Read-only Python checks verified all gold source spans,
replay identity, reserved-role separation and runner syntax. Inspected retained
RED test evidence and native preflight code/receipt. No model inference or
optimization was performed by this reviewer.

## Open Questions And Residual Risks

Freeze must be written before baseline and verified before optimization; the
runner enforces data/run freezes and prior frozen evidence. Baseline must reproduce
all136 diagnostic outputs exactly including confidence. Final reporting still
requires all regression cases, separate raw/accepted metrics, critical compound,
quoted and opaque boundaries, qualification verdict and protected-path receipts.
Synthetic paired tests do not establish production robustness or answer accuracy.

## Verdict

Pretraining data/harness: **Ready**. Completed experiment evidence and report:
**Ready** after reporting corrections. Both adapted models are **not ready for
qualification or promotion**: the predeclared paired improvement gate fails.

## Recommended Next Actions

Retain and freeze this completed bounded result, including regressions and failed
gates. Do not tune against these observations or select a seed. Any subsequent
decoder/conflict investigation requires a separately bounded experiment.

## Baseline execution audit

Independently hashed all165 run-freeze entries: zero mismatches. Compared each
complete saved diagnostic output and ID against vocabulary final outputs:
all136 cases per seed match exactly, including confidences and excluding timing.
Rescored both fresh raw-output files with the existing reviewed pilot scorer;
the complete resulting objects equal baseline-scores.json.

Fresh seed1701:31/40 exact, one invalid, raw TP92/FP15/FN12 and accepted
TP91/FP12/FN13, accepted F1 87.92%. Seed1702:33/40 exact, zero invalid,
raw/accepted TP96/FP11/FN8, F1 91.00%. Both preserve all six empty cases with
zero false positives. All13 compound API mentions and all five complete opaque
values (arrow, plain expression, array and object forms) are correct in raw and
accepted output. All values, versions and adapters have100% accepted P/R.

Primary failures are quoted names/keys in Markdown: seed1701 misses all ten
name/key boundaries in rbf-21–25; seed1702 misses six in21/24/25. Both also
absorb the colon into model key 'model' in30. Thus raw quoted-boundary misses
are11/7 of40. Seed1701 emits lens.focus as both key and value in23, making the
envelope invalid and discarding its otherwise-correct key API too.

Both overpromote ordinary registered-type prose to API type in12/14/25 and
omit the explicit configuration key API in13; seed1702 additionally promotes
array-form to API in14. This is context-sensitive role/boundary failure, despite
strong API recall, not missing every spelling. Baseline qualification fails:
registration accepted recall73.68%/84.21%, model-key recall60%/73.33%, quoted
boundary misses and the first seed's invalid output. No annotations, settings
or gates were changed after observing these outputs.

## Seed1701 execution audit

Verified1164 loss rows: each of six epochs visits all194 distinct training IDs
once with24 full eight-example chunks and one two-example chunk,150 updates.
Compared before/final parameter hashes: all334 frozen parameters unchanged;
202 trainable parameters changed. Epoch1/6 saved before/after outputs agree
exactly on all eight panel questions; adapter-file hashes match saved bytes.
Parameter identity is supported by receipts; no independent model rerun occurred.

Independently scored all six final output splits. Fresh35/40 exact, zero invalid,
raw/accepted F1 97.14%; vocab34/40, one invalid, accepted95.54%; target45/48,
zero invalid,98.51%; challenge18/24, one invalid,94.42%; olddev24/24,zero invalid,
100%; train192/194,zero invalid,99.80%. No previously exact evaluation case
becomes nonexact relative to the vocabulary baseline.

Fresh fixes all ten Markdown name/key boundary misses and the duplicate-role
invalid. Remaining failures are ordinary type promoted in12/14/25, omitted
API key in13, and colon included in the model-key span in30. All13 compound
APIs and all five opaque values remain exact, and all six empty cases remain
empty. Fresh accepted P/R exceed90% for every role, but the remaining quoted
key boundary violation still blocks qualification. The zero-diagnostic-invalid
gate cannot pass with the current vocab/challenge invalids; retain the full
two-seed result before drawing the final paired decision.

Span-level regression ledger: challenge roles-07 adds model_key 'moss-compass'
on an already-nonexact case; no other lost correct raw mention or added false
positive relative to the vocabulary baseline was found. Persistent invalids are
vocab va-f03-q04 ('Material' registration plus value) and challenge roles-04
(placeholder 'amber-pivot' registration plus value). The strict validator rejects
these cross-role overlaps rather than silently repairing them.

## Final paired execution audit

Seed1702 passes the same integrity checks:1164 loss rows,194 unique IDs per
epoch,150 updates,334 frozen parameters unchanged and202 trainables changed.
Epoch1/6 eight-output comparisons and adapter hashes pass. All165 run-freeze
entries remain unchanged after both runs. Independently rescored all six final
splits for both seeds; entire score objects match final-scores.json.

Seed1702 fresh36/40 exact,zero invalid,F1 98.10%; vocab34/40,one invalid,94.87%;
target46/48,zero invalid,99.00%; challenge19/24,zero invalid,96.64%; olddev24/24,
zero invalid,100%; training194/194,zero invalid,100%. Fresh gains are9.22/7.10
F1 points and4/3 exact cases. Both preserve all five fresh opaque values and13
compound APIs in raw and accepted output. Seed1702 fixes all40 quoted spans;
seed1701 retains the one colon-inclusive key boundary.

Seed1702 newly loses exactness on fresh rbf-40 by inventing version core, and
vocab va-f05-q05 by extending version v6 into closing Markdown asterisks.
Already-nonexact regressions lose API type in va-f04-q03 and the literal value
'cedar-latch' in challenge roles-02. These and seed1701 roles-07 are all raw
lost-correct/added-false-positive regressions against the vocabulary baseline.

Independently applied both diagnostic comparators: seed1701 fails vocab invalid,
challenge invalid and challenge F1 loss2.65 points against earlier challenge-flat;
seed1702 fails vocab invalid. Thus improved=false is correct for the paired gate.
Qualification fails independently: seed1701 retains a critical quoted-key miss;
seed1702 fresh version precision is6/7=85.71%; both retain vocab overlap invalids.
Perfect second-seed training fit does not establish qualification or generalization.

Reporting finding (accepted by author): initial postprocess.py recognized opaque
values only by arrow/field prefix, omitting fresh plain !model, array and object
expressions. Requested explicit reviewed-gold inventory to include all such
values in the descriptive boundary ledger. This changes reporting only, not
runtime, data, thresholds or gates. Final ledger/report reconciliation pending.

## Reporting correction and ledger audit

The author accepted the opaque-reporting finding and replaced the incomplete
heuristic with an explicit reviewed-gold inventory. Independently checked all352
case-ledger rows: source questions, exact/improved/regressed flags, before/after
errors, and every raw/accepted gained/lost correct span, added/removed false
positive and remaining miss/false positive match gold and scored predictions.
All432 boundary rows match gold and actual raw/accepted membership. Per seed,
the inventory covers81 compound APIs,125 quoted names/keys/values and10 opaque
values. All10 opaque values per seed are exact in both representations, including
the quoted !model.enabled expression and the new plain expression/array/object.
The reporting finding is resolved without changing the frozen experiment.

Inspected protected-after.json:36,708 manifest entries checked with zero changes.
Reviewed the audit script; this is receipt verification without opening protected
data or old sealed evaluation content. Final report reconciliation remains pending.

## Final report reconciliation

Read RESULTS.md after the independent output and ledger audits. Its metric
tables, whole-case repairs/regressions, raw/accepted distinctions, fresh API and
role results, failure against both baseline generations, training-fit limitation,
synthetic paired-evaluation caveat and no-promotion decision match the evidence.
Verified the reported descriptive latency means from saved timing totals.
Independently reconstructed all qualification failures: 14 for seed1701 and11
for seed1702, matching qualification.json and both false verdicts.

The initial report attributed the roles-04 duplicate to the model-key occurrence;
inspection showed it is the placeholder value at41:54 also tagged registration,
with the distinct model-key occurrence at118:131 correct. The author accepted
and corrected this, and added the roles-07 span regression explicitly. An
editorial follow-up restored exact case IDs after an automated spacing pass.

No actionable implementation or evidence findings remain after those reporting
corrections. The failed model gate and qualification are substantive outcomes,
not review defects to remove. Review instance1 of3 closes without initiating
another review instance, decoder change or training round.

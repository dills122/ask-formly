# Independent review

Review instance: 1 of 3. Scope: vocabulary_adaptation only; no inference or
training performed by reviewer. Gold and prior evidence were not edited.

## Findings

Pre-inference gold checkpoint: no actionable annotation findings. Independently
read all 40 fresh questions and mentions before reading new training questions,
author notes, or any prediction outputs. Every occurrence role is coherent with
the narrow contract. Checked ordinary versus configuration key/type/focus/wrappers,
Angular versus UI adapters, supplied wrapper names, maximal API paths, opaque
expressions, repeated occurrences, quotes and excluded Markdown backticks.
Mechanical source-slice/order checks passed. There are eight families of five
and six empty cases. These are synthetic documentation/meta questions; they do
not substantiate production-language robustness.

Fresh SHA256: `53e6e04ece7035a282ca02a8930cbd42f5f1c0f2e4d707be66846c083a49e341`.

Subsequently inspected all 48 new training rows and their explicit author markup.
No annotation defects found. Six negative rows retain ordinary nouns, Angular,
and quoted behavioral claims without manufactured mentions. Source-slice/order
checks passed. Fresh and new-training registration-name and model-key sets have
empty intersections. Shared library APIs are expected by this contextual-transfer
experiment, and do not establish unseen-API generalization.

New-training SHA256: `5c159544d6356291af831a24288f367142423fdaf5605f0ecb0ad00cfe37ae95`.

## Plan Review

Protocol preserves six roles, flat decoding at 0.5 on both seeds, a fixed six
epochs/114 updates, paired fresh testing and exposed diagnostic reporting.
Source grounding was checked against installed @ngx-formly/core 6.3.12 package
metadata and fieldconfig.d.ts declarations for expanded properties, lifecycle
hooks and options methods. Hypothetical API examples explicitly question existence.
This does not validate behavioral claims or Angular compatibility.

## Author-Claim Reconciliation

The fresh audit preceded training/output inspection. No separate author rationale
has yet been read. Protocol counts and new-gold semantic claims are confirmed.
Combined146 identity and harness isolation were subsequently confirmed. Author
notes corroborate counts and reservations but authorship independence is testimony,
not something file contents alone prove.

## Verification Performed

`python3 -B -m unittest discover -s poc/contextual-kb/gliner_feasibility/narrow_contract/vocabulary_adaptation -p test_policy.py`
passed three tests. Read-only Python checks verified both datasets' exact offsets,
non-overlap and reserved-name/key separation. No model inference, training, DB
access, or sealed-evaluation reads occurred.

## Open Questions And Residual Risks

Runner and combined dataset were subsequently inspected before optimization.
Combined146 equals the original98 plus new48 exactly; read all prior98 rows and
found no new annotation defect. All146 source spans pass and reserved fresh names,
keys and hypothetical API are absent from training in their reserved roles.
Inspected reused load_model/prepare/weights and scorer. CPU float32/four threads,
six fixed epochs, 19 updates per epoch, final two-example mean, native target
transport checks, LoRA-only trainables, frozen parameter hashes, RNG restoration,
flat save/reload parity and final-only scoring match the plan. Inference receives
only question strings. Original artifacts are checked, and writes are exclusive.
The runner parses. Subsequently inspected the pre-freeze undefined-precision
handling: rate(None) becomes zero for adapter precision gate deltas, avoiding a
TypeError when no adapters are predicted. This changes no model behavior. All
four policy tests passed on reviewer rerun. Runtime claims await receipts.

Reporting follow-ups: inherited scoring does not summarize opaque-expression
boundaries or emit an explicit regression ledger/qualification verdict. Final
analysis must derive these from saved predictions and gold without tuning. The
save/reload panel is current train[-8:] at both epochs; protocol "originalpanel"
should be read/documented as that fixed before/after panel, not old evaluation.

## Verdict

Gold checkpoint: Ready. Pre-optimization harness: Ready with non-blocking
reporting follow-ups. Completed experiment evidence and final report: Ready.
Both adapted models:
Not ready for qualification or promotion; the predeclared improvement gate fails.

## Recommended Next Actions

Freeze reviewed gold and runner, execute the single predeclared round, then assess
both seeds against unchanged gates and complete the reporting follow-ups above.

## Baseline execution audit

Independently verified all 155 entries in run-freeze.json against current bytes;
none changed. Compared complete saved output objects (including confidence) and
IDs against prior flat evidence for all three diagnostic splits, both seeds:
48 target, 24 challenge and 24 olddev outputs per seed match exactly.

Recomputed fresh typed exact-span counts directly from gold and saved case
mentions: seed1701 TP59/FP7/FN21, exact25/40, F1 80.82%; seed1702
TP61/FP8/FN19, exact27/40, F1 81.88%. No invalids; all six empty questions
remain exact and have no false positives. Raw and accepted metrics coincide.

Fresh gold contains API41, registration9, model-key8, value5, version9 and
adapter8 occurrences. API recall is 27/41 (65.85%) and 29/41 (70.73%). Both
seeds miss six of eight plain API occurrences, including validators,
asyncValidators, wrappers, parsers, expressions and expressionProperties.
All eight API-path/class-family mentions and all21 model-key/literal/expression
family mentions are exact. Thus API difficulty depends on context/formatting;
these results do not show a uniform inability to recognize each spelling.

The version/adapter scope family's false negatives are API omissions, not
scope-label errors: version and adapter precision/recall are 100% in both seeds.
Specifically the scope
family loses five API mentions for seed1701 and four for seed1702. Both seeds
mislabel the supplied registration 'Material' as value while recognizing its
separate adapter occurrence correctly. Markdown examples account for six/seven
false positives: spans include formatting backticks and some also swap name/key
roles to value. Ordinary untagged nouns are not falsely promoted to APIs.

Baseline qualification fails on recall/role precision and quoted boundaries;
there is no basis for readiness. No gold, run input, training configuration or
threshold was adjusted in response to these observations.

## Seed1701 execution audit

Verified 876 loss rows: each of six epochs visits all146 unique training IDs
once, with18 eight-example updates and one two-example update,114 total.
Compared before/final parameter hashes: all frozen parameters unchanged;
202 of230 trainable parameters changed. Epoch1 and6 receipts report parameter
identity, and direct comparisons confirm all eight saved before/after prediction
objects identical. Every recorded adapter-file hash matches the saved bytes.
This is receipt/file verification, not an independent rerun of model inference.

Independently scored saved outputs using the reviewed scorer: fresh29/40 exact,
two invalid, accepted F1 86.84%; target43/48, one invalid,96.48%; challenge17/24,
one invalid,94.02%; olddev24/24,zero invalid,100%; train144/146,zero invalid,
99.76%. Fresh API recall rose to90.24%, adapters retain100% precision and empty
false positives remain zero. Formerly exact fresh va-f04-q02, target
fresh-flat-004/fresh-flat-030 and challenge roles-04 regress.

The paired improvement gate cannot pass: this seed's challenge accepted F1
drops3.05 percentage points, beyond the allowed two, and target/challenge invalid
counts increase. Await second-seed results for complete reporting, without
altering parameters, gold, gates or selecting the better seed.

First-seed failure classification: native flat decoding still permits cross-role
duplicates. Fresh va-f03-q04 emits 'Material' as both registration and value;
va-f05-q02 duplicates backtick-inclusive names/keys across roles. Target
fresh-flat-030 absorbs the property key into the model-key value and overlaps the
separate API occurrence. Challenge roles-04 adds a registration role on a model
key and a spurious value for ordinary "text". Fresh ordinary key/wrappers and
target wrapper/defaults are overpromoted to APIs. Remaining fresh API omissions
are type, parsers, asyncValidators and validators. Markdown boundaries persist.

Smallest evidence-supported future experiment: add bounded contrastive role and
boundary supervision, including ordinary/API minimal pairs, behavioral quotes
versus literal values, and equivalent quoted names/keys with and without Markdown.
Hold broader vocabulary and inference settings fixed; reserve a new independent
test before training. This is a recommendation only, not authorization to tune,
rerun, relax the validator or select a model from this round.

## Final paired execution audit

Seed1702 passes the same receipt checks:876 loss rows,146 unique examples per
epoch,114 updates,202 of230 trainables changed, frozen parameter hashes unchanged.
Epoch1/6 actual eight-output before/after comparisons and adapter-file hashes
pass; parameter identity is supported by saved receipts. All155 run-freeze entries
still match after both runs. protected-after.json records36,627 checked entries
with no changes; reviewer inspected that receipt without opening protected data.

Independently recomputed all five final splits for both seeds from saved outputs
using the reviewed scorer; raw/accepted counts, cases, exact and invalid totals
match final-scores.json. Seed1702 fresh31/40 exact,one invalid,F1 87.50%; target
45/48,zero invalid,98.51%; challenge18/24,one invalid,94.47%; olddev24/24,zero
invalid,100%; train143/146,zero invalid,99.64%.

Both fresh exact counts gain four, accepted F1 gains6.02/5.62 percentage points,
and raw API recall gains24.39/21.95 points. However challenge accepted F1 falls
3.05/2.99 points, with one new invalid per seed. Seed1701 additionally introduces
a target invalid. The reported improved=false decision is correct, with no
permission to select a seed or relax a threshold.

Qualification fails independently of the improvement gate: fresh accepted overall
recall82.50%/87.50%, registration recall55.56% both, model-key recall62.50%/75%,
and invalid outputs violate requirements. Do not conflate raw API recall
90.24%/92.68% with accepted API recall85.37%/92.68%; invalid envelopes drop correct
mentions too. Both raw adapter recalls are100%, but accepted adapter recall is
87.50%. All compound spans match in raw output, while fresh quoted mentions have
six/five exact-boundary misses and challenge has one/two. Each seed preserves all
four evaluation opaque arrow expressions (fresh one,target two,olddev one) in
both raw and accepted output, plus both training expressions. No opaque failure
was observed on this bounded sample.

Seed1702 newly loses exactness on fresh va-f04-q02/va-f04-q03, target
fresh-flat-004 and challenge roles-02/claims-08. Together with the first-seed
ledger above, these cover all formerly-exact cases that regress. Additional
span-level regressions in already-failing cases must remain visible in the
author's complete per-case ledger. No post-freeze tuning or gold edits occurred.

## Final report reconciliation

Read RESULTS.md after the independent gold, implementation and output audits.
Its metric tables, raw/accepted distinctions, fitting limitations, synthetic
paired-evaluation caveat, failure characterization and no-promotion decision
agree with inspected evidence. Independently verified all272 unique ledger rows,
including before/after exact flags, repairs/regressions, errors, every gained/lost
correct mention, added/removed false positive, remaining miss and source question.
Reported fresh latency averages match saved timings and are appropriately
described as uncontrolled measurements. The author accepted the findings and
did not tune or promote either model. Reporting follow-ups are resolved.

No actionable findings remain against the experiment's evidence or report.
The failed improvement and qualification results remain substantive model limits,
not review defects to erase. Freeze final artifacts and retain this bounded
negative result; do not initiate another review instance or training round.

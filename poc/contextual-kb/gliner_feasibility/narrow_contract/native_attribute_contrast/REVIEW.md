# Independent review — native attribute contrast

Review instance: 1 of 3

## Preliminary review boundary

Reviewer read the independent-review skill, repository README/development guidance,
POC AGENTS/STEERING, narrow CONTRACT and TEST-PLAN before author rationale or prior
native_attribute_training report. Scope is the new native_attribute_contrast
experiment only. Git is main at c3091328f49d53de6b41a49c4fe5aa8f1c45e516 with a
large pre-existing dirty/untracked tree; this review uses an explicit artifact
boundary, not the whole Git diff. No source fixes, training, tuning or dispatch
are owned by this reviewer. This report is the only authorized reviewer write.

## Preliminary concerns to verify

- Canonical roles are exclusive per occurrence. Full paths and opaque expressions
  require maximal exact spans; quote delimiters are semantic for names/keys/values.
- Source-exact serialization alone cannot reject semantically clipped or merged
  candidates. Rejection must be attributable to the new GLiNER training mechanism,
  with no heuristic repair, lexical postprocessing or changed frozen extractors.
- Fresh gold/probes must be independently reviewed and frozen before output access,
  excluded from training and all threshold/checkpoint tuning, with role confusion
  and clipped/merged spans retained in failure denominators.
- Both models need the identical frozen fresh questions, scoring and gates;
  abstentions, missing output and failed runs cannot become successes.
- Check training/inference loss and save/reload parity, deterministic fixed choices,
  and protected hashes for A, v2, data/DB, both extractors and all prior experiment
  artifacts (including the 139-file final manifest).

## Current checkpoint

Awaiting fresh-case artifacts and neutral implementation bootstrap. No pretraining
or adoption readiness verdict yet. Author explanation has not been read.

## Blind fresh annotation checkpoint

Reviewed all 40 questions, their full gold sets, 40 semantic negatives and transport
probes before model outputs, training implementation or author rationale. Initial
review found one omitted explicit `props` API, two accidentally unbalanced arrays,
one callback negative with a midword boundary, and four envelope-invalid probes
misclassified as token transport probes. Fresh author corrected these before freeze.
Final gold has 106 mentions. The semantic negatives are invalid in full question
context; complete opaque values remain valid, and repeated lexemes retain their
occurrence roles. No actionable semantic annotation finding remains.

Read-only check used the installed gliner2 `WhitespaceTokenSplitter` implementation
via `runpy.run_path`, without loading a model. All 40 semantic negatives and 106
valid probes are exact source slices with token-aligned boundaries. All four
transport probes are exact in-bounds source slices with unaligned boundaries.
This proves word-boundary representability, not extraction or classification.
Fresh author was authorized to freeze these artifacts; fresh content was not sent
to the training worker. Awaiting hashes and pretraining implementation review.

## Training annotation checkpoint

Read tests before annotation transport; reviewed all 48 new tagged questions and
85 explicit contextual negatives, then the 194 replay questions and 449 replay
negatives. No actionable training annotation defect found. Negative spans stay
occurrence-specific, and complete opaque expressions are not negative targets.
`python3 -B -m unittest discover -s poc/contextual-kb/gliner_feasibility/narrow_contract/native_attribute_contrast -p test_data.py`
passes four tests. Independent JSON comparison proves replay prefix equality to
prior training/gold and negatives. All 242 rows' gold/negative spans are exact
source slices and native-word-aligned; none of 534 negatives equals gold offsets.
No model loaded or output accessed for these checks.

Fresh frozen hashes independently verified after schema-only conversion:
- fresh.json: `9c0baf7b4568522e74909c3044010c51e38fccb68b34ede87e99af31e1ebb2c2`
- families.json: `bfda7bb23081387ef706c4e021ee6458e032448aa630985a8f52ac4ebe729685`
- probe_candidates.json: `7803ace490d3a2f2d19dc8433f6b77532dd27b53d89e8b811c54f1293e52694f`

These are annotation checkpoints only. Protocol, training harness and evaluation
gates remain to be reviewed before training readiness.

## Blind implementation checkpoint

Inspected `prepare_data.py`, `run.py`, `compatibility.py`, `gate.py`, `test_gate.py`,
`PROTOCOL.md` and `assess.py` before reading AUTHOR-NOTES. Nine unit tests pass.
Training continuation uses matching prior seed adapters; only LoRA parameters
can change. Four epochs give 124 optimizer steps; epoch 1/4 parity uses training
rows, never fresh probes. Frozen baseline exact spans alone enter the operational
resolver; gold/probe offsets remain a separate audit. Prior baseline and candidate
raw output/probe equality is checked before optimization.

Assessment checks original accepted P/R/F1 and invalid counts, correct mentions
from both comparison arms, prior exact outcomes, nonconflicting spans and incorrect
resolutions. A return to an unresolved original invalid envelope is not counted as
a repair. Every previously correct old probe must remain correct. Qualification
and operational improvement are distinct. No blocker found in inspected logic.
Residual robustness limitation: several internally produced arrays are joined with
`zip` without local length assertions; final review must independently verify
complete IDs/counts before trusting those joins.

## Pretraining author-claim reconciliation

After recording the blind implementation checkpoint, read the separate
IMPLEMENTATION-EXPLANATION.md. Replay counts/equality, 48 contextual additions,
85 new negatives, native helper reuse, unchanged conservative resolver, fixed
four-epoch budget, original-versus-prior gate distinction and nine passing tests
are confirmed by inspected artifacts. Native compatibility receipts report exact
242-row/534-negative transport for both seed checkpoints. TDD ordering is author
reported; retained red/green evidence is not independently reconstructed here.
Epoch 1/4 save/reload parity is implemented but remains a required executed result,
not a completed claim before training.

## Pretraining verdict

**Ready for the bounded frozen experiment.** This is not adoption readiness.
Freeze protocol, implementation, annotated training inputs and fresh artifacts
before baseline output access; run both fixed candidates and retain every failure.
No pretraining blocker remains. This same review instance will audit final raw
outputs, gates, loss/update receipts, save parity and protected hashes.

## Baseline execution audit

Independent JSON-only audit confirms each seed has all 336 unique operational
IDs and matching prior-candidate IDs. All 296 historical original raw outputs
match prior frozen baseline outputs exactly; all 296 prior-candidate supplied
scores/resolved outputs match the prior experiment exactly. Both old 156-probe
arrays match prior saved predictions exactly. Each new fresh probe array contains
all 150 candidates. No baseline drift found. Training is now running under the
15-input training freeze and 666-input combined run freeze.

## Seed 1701 executed audit

Independent raw JSON recomputation confirms 336 complete operational cases, two
correct resolutions and zero wrong resolutions. Both repairs are retained from
the prior candidate; no correct raw mention or prior wholly exact output is lost.
Fresh supplied-span correct roles improve 104→105/106; learned negative rejection
improves 29→32/44 (four unsupported included). Old supplied-span correct roles stay
105/106; rejection improves 26→32/50. One valid span remains wrongly rejected in
each set. Two previously correct old negatives become wrong semantic roles:
`native-fresh-07` clipped `formState['view.mode']` becomes api_reference and
`native-fresh-15` broken quote `'it is ready` becomes value. Thus the predeclared
old-probe preservation gate fails regardless of aggregate improvement. Four fresh
prior-correct negatives also regress (one nested fragment becomes value and three
prose probes abstain); these must be disclosed even though the preservation gate
specifically protects old diagnostic probes.

Training log independently contains 968 finite losses, each authorized training ID
once per epoch, 31 steps/epoch and 124 total. Receipt lists 202 changed LoRA tensors
and zero changed frozen tensors. Epoch 1/4 actual native before/after JSON arrays
match exactly on eight training examples; parameter-parity receipts both pass.

# Final independent audit

Review instance: 1 of 3. Same reviewer as the blind/pretraining checkpoints.

## Findings

**Adoption blocker — seed 1702 still legitimizes a malformed span.** Raw
`test-output/1702/span-after.json`, case `srf-026`, assigns value to the merged
`props.label: 'entry[2]'` span at confidence 0.5233. Its envelope becomes valid but
wrong; accepted span-set F1 is 93.14% against the original extractor's 94.06%.
There are zero correct operational repairs and one wrong resolution for this seed.
Do not promote the adapter or relax its preregistered gate.

**Adoption blocker — both seeds lose protected old probe successes.** The paired
old-probe raw predictions show two losses for 1701 and five for 1702. For 1702,
three clipped paths become API references and two merged spans abstain. All seven
losses violate the explicit old-probe preservation requirement. New fresh probes
also lose four prior successes per seed, despite aggregate gains. Keep these
losses visible; further tuning on these exposed questions is not authorized.

No actionable implementation defect remains in the reviewed bounded experiment.
These are measured candidate failures, not grounds to rewrite the frozen protocol
or start another review. Report wording initially overattributed improvement to
the added examples alone; the author corrected it to describe the fixed
continuation and disclose the absence of a continuation-only control.

## Plan Review

The authorized intervention was completed: 194/449 replay remains exact; 48/85
contextual additions produce 242 questions/534 negatives; both seed candidates
ran four fixed epochs and 124 updates. Fresh gold and probes were independently
reviewed/frozen before outputs, with training/protocol frozen before fresh access.
No fresh inputs enter training or operational span construction. Both frozen
extractors, prior adapters, A/v2 and protected data/DB remain unchanged.

Conservative same-span-only resolution and the strict original-baseline gate are
preserved. Prior incorrect but structurally valid output is not treated as a
correctness asset: 1702 now abstains on `va-f03-q04`, restoring the original invalid
conflict and its correct registration mention. This is a safe abstention, not a
repair; the report discloses the associated accepted-metric decline. No correct
raw mentions or prior exact operational outcomes are lost. Seed 1701 retains its
two original repairs; seed 1702 still supplies none. Both improvement gates and
both full qualification gates fail, as the plan requires.

## Author-Claim Reconciliation

| Claim | Independently inspected evidence | Status |
| --- | --- | --- |
| Both historical baselines and candidates reproduce | All 296 prior cases and 156 probes per seed, exact JSON comparisons | Confirmed |
| Fresh role/rejection results and regressions are retained | Both 150-probe fresh and 156-probe old arrays; 612 transition entries | Confirmed |
| Four epochs/124 updates, LoRA-only changes | Both 968-line finite loss logs; authorized IDs each epoch; before/final hashes for 564 parameters | Confirmed |
| First/final saves preserve predictions and parameters | Actual epoch 1/4 before/after native JSON plus parity receipts for both seeds | Confirmed within eight-example training panels |
| Frozen assets remain unchanged | Independent 37,199 protected checks and 15/666 freeze input hashes | Confirmed |
| Added examples alone caused gains | No continuation-only control | Not established; report corrected |
| Candidate is ready for adoption | Wrong resolution, old probe regressions, rejection/qualification failures | Contradicted; report explicitly declines adoption |

## Verification Performed

- Nine unit tests independently executed successfully before training.
- Independent source-slice/token-boundary checks covered all 242 training rows,
  all 534 negatives, 106 fresh gold spans, 40 semantic negatives and four
  intentionally unsupported transport probes.
- All 336 operational IDs per seed are present, unique and consistently ordered.
  Re-running the reviewed scorer read-only reproduced all 54 seed/split/arm
  score objects exactly. Separate set comparisons confirmed preservation and
  independently classified the two correct/zero wrong and zero correct/one wrong
  operational resolutions.
- Independent probe arithmetic confirms fresh valid roles 105/106 for each seed;
  negative rejection 32/44 and 31/44 (semantic-only 32/40 and 31/40). Old valid
  roles are 105/106 each; rejection is 32/50 and 31/50 (semantic-only 32/46 and
  31/46). Four unsupported spans per set remain failures in overall denominators.
  One valid fresh span is rejected by each seed. On old probes, 1702 accepts all
  valid spans but mislabels `'lagoon-input'` as API, so acceptance is not accuracy.
- Each training log contains 968 finite losses: all 242 authorized IDs once per
  epoch, 31 optimizer steps per epoch. Independent before/final hash-map
  comparisons find 202 changed tensors, exclusively LoRA, for each seed.
- Both epoch 1/4 saved native prediction arrays equal their reload arrays exactly;
  all parameter-parity receipts pass. No extra model training or evaluation was
  performed by this reviewer.
- A separate read-only SHA-256 traversal verified 37,199 accumulated protected
  manifest entries plus all 15 training-freeze and 666 run-freeze entries with
  zero changes. It hashed 37,328 distinct paths across those combined checks.
  This includes the prior experiment's 139-file final freeze.

## Open Questions And Residual Risks

The native supplied-span scorer uses pinned private APIs. Save parity covers the
retained training panel, not every possible query. Independent synthetic fresh
questions are bounded evidence, not a production distribution. Merged-span gains
do not isolate the contribution of added data from continued optimization.
Fresh end-to-end extraction remains unchanged at 37/40 and 36/40 exact questions;
supplied-span improvements do not establish extraction completeness or final
answer quality. No unreported train/inference change or protected mutation was
found.

## Verdict

**Not ready** for adoption. This is a completed, credible negative experiment.
The implementation and evidence satisfy the bounded experimental plan; the
trained candidates fail its adoption criteria. Both remain experimental.

## Recommended Next Actions

Retain both original frozen extractors and preserve all new artifacts and failures.
Close this authorized run without choosing a favorable seed, changing thresholds,
or tuning on exposed fresh cases. Any materially different follow-up requires a
separately authorized design and new evaluation. No additional review instance
is initiated because adoption failed. Reviewer is quiescent after this report.

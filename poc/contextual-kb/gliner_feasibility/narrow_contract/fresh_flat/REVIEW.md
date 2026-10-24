# Independent review

Review instance: 1 of 3. Reviewer owns only this report.

## Preliminary findings before author explanation and inference

The review started from POC AGENTS/STEERING, narrow CONTRACT, fresh-flat PROTOCOL,
then tests, checks.py and run.py. All 48 questions and every mention were inspected
without reading previous questions, training examples, predictions, scores, or
AUTHOR-NOTES/RESULTS. The working-tree boundary is fresh_flat, on main at
c3091328f49d53de6b41a49c4fe5aa8f1c45e516. The surrounding tree is extensively dirty
and poc is untracked; those unrelated changes are outside this review.

Initial observations while authoring was still active:

- P2: Initial snapshot truncated closing brackets in 014, 016, 018, 030 and 036.
  A subsequent read confirmed these corrected before inference. The reviewer did
  not edit gold.
- P2: 033 presents bare model as an API while its prose also uses expressions
  without a tag. Ordinary model nouns are excluded by the contract. Requested
  explicit formatting of intended API and unambiguous prose for expressions.
- P2: 030's final dotted string key could be read as a second configuration-property
  occurrence. Requested dotted string path to avoid ambiguity in a clear-case set.

All other reviewed roles and boundaries agree with the narrow contract, including
complete opaque expressions in 016/018/036; quoted behavioral claim exclusion in
045; registration/type noun distinctions; scope mentions under negation and
comparison; and eight empty envelopes. Questions are plausible focused library
questions, with deliberate source-authority questions in the final family.
They are synthetic and not a representative traffic sample.

The plan keeps checkpoints fixed, validates input identity and exact old-question
overlap, preserves both prediction files before scoring, and explicitly passes
only question text and common labels to extract(). No new training is present.
The input-check tests pass (5 tests). Current gold validates exact source offsets,
nonoverlap, identity, status and family coverage. Full final scoring review awaits
frozen inputs and outputs. No qualification verdict is issued at this stage.

## Verification performed

- python3 -B -m unittest discover -s poc/contextual-kb/gliner_feasibility/narrow_contract/fresh_flat -p 'test_*.py': 5 passed.
- validate_inputs(current questions, current families, []): passed. This verifies
  local integrity only; the parent runner owns old-question overlap checking so
  this reviewer remains blind to old examples during gold audit.

## Pre-inference gold verdict

Ready for freezing and inference: no remaining gold blocker. Final 030 uses
"dotted string path" and 033 uses formatted `model` plus "dynamic settings".
The corrected bracket spans were an unfinished authoring snapshot, not model
failures and not changes made in response to model outputs. All 48 questions
were manually audited; final validation passes. There are eight families of six,
eight empty envelopes, and role coverage meets the protocol minima.

Audited questions SHA256:
14389bcb379869ddd93c7ecb83dd4c712536543450457ab0c121a2368755f66b

Audited families SHA256:
400637ed796f745bdfe52920a8ec5566d935479c2ab966708743e0cb6dc6cc35

This is permission to run the fixed diagnostic experiment, not a conclusion that
its models qualify. Author explanation and results have not yet been read.

## Independent final recomputation before author rationale


### Checkpoint 1701

Every nonexact case (role, start, end, raw):
- fresh-flat-002: missing [('registration_name', 40, 55, "'postal-lookup'")]; extra []
- fresh-flat-003: missing [('registration_name', 73, 88, "'billing-frame'")]; extra [('ui_adapter', 73, 88, "'billing-frame'")]
- fresh-flat-005: missing [('api_reference', 29, 37, 'wrappers')]; extra []
- fresh-flat-010: missing [('api_reference', 4, 23, 'validation.messages')]; extra []
- fresh-flat-012: missing [('api_reference', 32, 42, 'validators'), ('api_reference', 47, 62, 'asyncValidators')]; extra []
- fresh-flat-017: missing [('api_reference', 26, 37, 'expressions'), ('api_reference', 42, 62, 'expressionProperties')]; extra []
- fresh-flat-027: missing [('api_reference', 71, 85, 'FieldArrayType')]; extra []
- fresh-flat-029: missing [('api_reference', 90, 99, 'FormGroup')]; extra []
- fresh-flat-032: missing [('api_reference', 32, 44, 'hooks.onInit')]; extra []
- fresh-flat-033: missing [('api_reference', 40, 45, 'model')]; extra [('api_reference', 39, 46, '`model`')]

Recomputed TP/FP/FN by role and family:
```
{
  "all": [
    88,
    2,
    12
  ],
  "custom_types_wrappers": [
    10,
    1,
    3
  ],
  "api_reference": [
    42,
    1,
    10
  ],
  "registration_name": [
    7,
    0,
    2
  ],
  "ui_adapter": [
    8,
    1,
    0
  ],
  "validation_errors": [
    9,
    0,
    3
  ],
  "value": [
    13,
    0,
    0
  ],
  "version": [
    10,
    0,
    0
  ],
  "expressions_visibility": [
    9,
    0,
    2
  ],
  "defaults_model_reset": [
    19,
    0,
    0
  ],
  "model_key": [
    8,
    0,
    0
  ],
  "repeat_nesting_layout": [
    11,
    0,
    2
  ],
  "lifecycle_options": [
    8,
    1,
    2
  ],
  "adapters_version_scope": [
    15,
    0,
    0
  ],
  "conceptual_claim_distinctions": [
    7,
    0,
    0
  ]
}
```
Exact envelopes 38/48; zero invalid/runtime outputs; empty false positives 0/8.
Opaque-expression cases 016/018/036 all exact, with no inner API fragments.

### Checkpoint 1702

Every nonexact case (role, start, end, raw):
- fresh-flat-001: missing []; extra [('ui_adapter', 81, 88, 'Angular')]
- fresh-flat-003: missing [('registration_name', 73, 88, "'billing-frame'")]; extra [('ui_adapter', 73, 88, "'billing-frame'")]
- fresh-flat-005: missing [('api_reference', 29, 37, 'wrappers')]; extra []
- fresh-flat-010: missing [('api_reference', 4, 23, 'validation.messages')]; extra []
- fresh-flat-012: missing [('api_reference', 32, 42, 'validators'), ('api_reference', 47, 62, 'asyncValidators')]; extra []
- fresh-flat-013: missing []; extra [('ui_adapter', 76, 83, 'Angular')]
- fresh-flat-017: missing [('api_reference', 26, 37, 'expressions'), ('api_reference', 42, 62, 'expressionProperties')]; extra []
- fresh-flat-033: missing [('api_reference', 40, 45, 'model')]; extra [('api_reference', 39, 46, '`model`')]
- fresh-flat-046: missing []; extra [('api_reference', 35, 39, 'type')]

Recomputed TP/FP/FN by role and family:
```
{
  "all": [
    92,
    5,
    8
  ],
  "custom_types_wrappers": [
    11,
    2,
    2
  ],
  "ui_adapter": [
    8,
    3,
    0
  ],
  "api_reference": [
    45,
    2,
    7
  ],
  "registration_name": [
    8,
    0,
    1
  ],
  "validation_errors": [
    9,
    0,
    3
  ],
  "value": [
    13,
    0,
    0
  ],
  "version": [
    10,
    0,
    0
  ],
  "expressions_visibility": [
    9,
    1,
    2
  ],
  "defaults_model_reset": [
    19,
    0,
    0
  ],
  "model_key": [
    8,
    0,
    0
  ],
  "repeat_nesting_layout": [
    13,
    0,
    0
  ],
  "lifecycle_options": [
    9,
    1,
    1
  ],
  "adapters_version_scope": [
    15,
    0,
    0
  ],
  "conceptual_claim_distinctions": [
    7,
    1,
    0
  ]
}
```
Exact envelopes 39/48; zero invalid/runtime outputs; empty false positives 2/8.
Opaque-expression cases 016/018/036 all exact, with no inner API fragments.

Cross-checkpoint differing predictions: ['fresh-flat-001', 'fresh-flat-002', 'fresh-flat-013', 'fresh-flat-027', 'fresh-flat-029', 'fresh-flat-032', 'fresh-flat-046']

All file hashes match these manifests: [('poc/contextual-kb/gliner_feasibility/narrow_contract/fresh_flat/data-freeze.json', 4), ('poc/contextual-kb/gliner_feasibility/narrow_contract/fresh_flat/test-output/run-freeze.json', 144), ('poc/contextual-kb/gliner_feasibility/narrow_contract/challenge_adaptation/test-output/final-freeze.json', 70), ('poc/contextual-kb/gliner_feasibility/narrow_contract/native_decoding/test-output/final-freeze.json', 28)]
Exact overlap independently checked against exposed 98 train + 24 dev + 24 challenge questions: zero. This does not establish semantic disjointness.

## Findings

No remaining actionable evaluation-implementation or gold defect found. Both
models fail the predeclared qualification criteria; this is an experimental
finding, not a request to repair predictions or gold. Both include Markdown
backticks in the 033 API span and classify the wrapper name in 003 as an adapter.
1701 additionally misses two complete compound APIs (validation.messages and
hooks.onInit); 1702 misses validation.messages. Reported compound exact recovery
is 17/19 and 18/19. Quoted name/key/value typed recovery is 17/19 and 18/19;
these deficits are omission/misclassification, not evidence of quote truncation.
All three opaque expressions are recovered intact by both candidates.

## Plan review

The fixed evaluation plan was implemented: 48 new questions, both epoch-8 adapted
checkpoints, flat decoding at 0.5, 96 persisted results, no inference-time gold,
no new training or label repair, and scoring after both raw files exist. The
runner imports existing loader/scorer support within the POC. Static inspection
shows each extract call receives only the original question and shared schema.
The file hashes and unchanged gold hashes match the pre-inference audit. Existing
checkpoint final manifests, base/library run manifest, and both weight receipts
support fixed candidates; receipts record exact checkpoint parameters and
unchanged weights. The reviewer verified file hashes and runner enforcement,
not a second independent parameter load or second inference run.

## Author-claim reconciliation

AUTHOR-NOTES was read only after the independent final recomputation above.

| Author claim | Evidence | Status |
| --- | --- | --- |
| 48 questions, eight families of six, eight empty cases, 100 mentions | Full gold and family audit, independent counters | Confirmed |
| Complete source offsets, opaque expressions and syntactic quotes | Manual annotation review and validator | Confirmed |
| No prior examples or outputs used by author | Author's separate scope and statement; zero exact overlap independently computed | Consistent, historical non-access cannot be proven from data alone |
| No application inspection, answering or ambiguity claims | Question content and explicit protocol limitations | Confirmed |
| Corrections preceded freeze and inference | Reviewer recorded corrected gold hashes before inference; current hashes match | Confirmed |

## Verification performed

Independent standard-library recomputation parsed all 96 raw prediction outputs,
validated all envelopes, asserted uniqueness/coverage, compared every case's exact
TP/FP/FN and exactness with saved scores, and recomputed all per-role/per-family
counts, precision and recall. All agree with scores.json. Raw and accepted scores
are identical because no envelope was rejected. F1 follows the same exact counts.
All 246 entries across the four recorded manifests matched current file hashes
(entries can overlap). No old sealed evaluation content was opened.

## Open questions and residual risks

This is a small authored synthetic clear-case test with eight deliberately empty
questions. Gold is now exposed and cannot remain an unseen test. Zero exact reuse
does not imply semantic independence from training. No ambiguity, relation,
retrieval, answer-quality or production-readiness claim follows. The two
checkpoints disagree on seven questions (41/48 identical predictions); that is
cross-checkpoint stability, not repeated-run determinism. The original raw data
and original scores must remain intact even if future annotation concerns arise.

## Verdict

Ready: the diagnostic evaluation and its evidence are fit to report. Neither
model qualifies under the strict extraction criteria.

1701 precision/recall/F1 = 97.78% / 88.00% / 92.63%; exact envelopes 38/48
(79.17%). Overall recall, API recall (80.77%), registration recall (77.78%), and
adapter precision (88.89%) fail the 90% threshold.

1702 precision/recall/F1 = 94.85% / 92.00% / 93.40%; exact envelopes 39/48
(81.25%). API recall (86.54%), registration recall (88.89%), and adapter precision
(72.73%) fail the per-role threshold. Both also have critical typed compound/name
recovery misses and the backtick boundary error. Zero invalid outputs does not
make the missing or mislabeled mentions correct.

## Recommended next actions

Report both models without selecting or tuning a winner. Include all-case failure
ledger, 0/8 versus 2/8 empty false-positive cases, preserved opaque expressions,
and strict nonqualification. No additional review instance is needed unless the
review target materially changes. This remains review instance 1 of 3.

## Final RESULTS reconciliation (same review instance)

Read RESULTS.md after completing the independent computation. Its model metrics,
all eight family exact counts, six shared failure cases, seed-specific failures,
opaque-expression result and strict nonqualification agree with the evidence.
Independently recomputed 35 questions correct under both, six wrong under both,
and seven mixed; previously verified identical predictions on 41/48. Thus the
stated 42-question oracle union is correct and explicitly not an ensemble result.

The report appropriately excludes representative traffic accuracy, v2 integration,
ambiguity, final-answer quality, service latency and repeat-run determinism claims.
Its suggestion for further bounded improvement is a recommendation, not work
performed or evidence that the next iteration will qualify. No report discrepancy
found. The additional whole-protected-tree audit mentioned at the end is being
completed by the parent; this reviewer previously verified the four listed freeze
manifests, not that additional audit's completion. No inference rerun, gold change,
or new review instance occurred during reconciliation.

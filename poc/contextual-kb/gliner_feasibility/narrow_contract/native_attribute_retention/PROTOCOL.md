# Frozen native-attribute retention/control protocol

Scope: question-layer POC only, GLiNER native span attributes. No change to frozen extractors, A, v2, knowledge/DB, retrieval or answer assembly. Four experimental adapters maximum, no post-fresh tuning, no selected epoch or seed. All historical evaluation remains diagnostic and is never training material.

## Contrast and training

Both arms of each seed start from that seed's identical `native_attribute_training/test-output/{seed}/epoch-6/adapter`, with parameter hashes checked. These precede the failed contrast continuation. Control continues original194 questions/449 negative spans. Treatment uses the exact same seven replay slots per update, replacing the eighth original-replay slot with one of the existing48 training-only contrast questions/85 negatives. These are unchanged annotations: no old probe or test examples are added.

A deterministic seeded cyclic shuffle creates124 updates ×8 examples =992 examples per candidate. Control:992 original examples. Treatment:868 shared original examples plus124 contrast examples. All194 original and48 contrast rows receive exposure; complete per-question and negative-family counts are frozen in exposure.json. Contrast cycling is balanced to within one exposure per question. Shared replay slots, optimizer initialization, seed and update count match exactly.

The native total loss for each original row has coefficient1/8; the contrast row has coefficient0.25/8. There is no renormalization by total weight. Control raw weight sum992; treatment868+31=899. Summed per-update loss coefficients are1 vs0.90625; total coefficients124 vs112.375. This is a bundled sparse, reduced-weight augmentation intervention against continued replay. It does not isolate the individual effects of weighting, substitution, or overall loss scaling. The older contrast run differs in sample budget/distribution and is only a historical comparison, not this controlled contrast.

Both arms use AdamW lr1e-4, weight decay0.01, clipping1, CPUfloat32,4 threads, deterministic algorithms, existing LoRA parameters only. Native boundary-query targets, label descriptions/order, gold injection1, private supplied-span scorer and resolver stay unchanged. Native BCE span supervision must not be described as categorical cross-entropy training. Save/reload checks at updates31 and124 use only original training rows186–193; predictions and parameter hashes must match exactly. Optimizer and RNG are initialized identically for each arm; reload checks restore RNG state. Fixed final checkpoint only.

## Pre-exposure checks

TDD covers matched schedules, budgets, authorized index sets, balanced exposure, deterministic seeds, actual torch gradient scaling without renormalization, abstention semantics and paired superiority. Existing gate tests cover correct-mention preservation, removing prior wrong output, invalid-to-valid wrong and both-seed repair requirements. Native transport compatibility checks both starting adapters over all242 training rows/534 negatives. Review code/tests/protocol first; author rationale separately afterward.

Freeze reviewed source/protocol/training/schedules before reading new fresh data. Then freeze fresh source hashes and prior manifests. Reproduce all336 old original-extractor outputs and starting-candidate outputs exactly, plus all306 old starting-candidate probe predictions. Old starting outputs are available from the contrast experiment's before arm. Fail closed on drift. Never modify prior frozen artifacts.

## Evaluation

Forty independently authored fresh questions plus336 old diagnostic questions =376 operational questions per seed. Original extractor flat-decoded spans supply all operational offsets. Candidate models choose only identical-offset competing roles; partial overlaps, unsupported coordinates, no_entity or confidence≤0.5 retain raw unresolved output. No supplied gold/malformed probes feed the resolver. Safe abstention is not a repaired extraction.

Each arm receives the same fresh supplied-span audit and306 old supplied-span probes (156 native-attribute +150 contrast). Include all complete valid occurrences, semantic malformed spans and separately identified transport-unsupported spans. Correctness requires exact role, not merely acceptance. Learned no_entity rejection requires scored confidence>0.5; low-confidence/unsupported abstention is not rejection. Report total and representable-semantic denominators, rejection precision/recall, valid-role accuracy and valid acceptance. Every gain and loss is retained with confidence.

## Gates, fixed before outcomes

Each arm independently must preserve original correct raw mentions, nonconflicting mentions, per-role accepted precision/recall/F1, and invalid count. Precision/recall/F1 undefined after a previously defined score fails; undefined starting scores impose no numeric lower bound. Zero wrong resolutions and zero invalid-to-valid wrong outputs. Preserve every starting candidate correct raw mention, wholly exact output, and every correctly scored old supplied-span probe across both historical sets. A restored original unresolved invalid output after a starting wrong resolution is safe abstention, not a regression in correctness and not a repair. Each seed needs at least one correct operational repair versus the original extractor. Both seeds must pass for the arm to pass improvement.

Full qualification is separate: zero invalid/runtime/wrong resolutions, every nonempty role precision and recall≥90%, zero critical compound/quoted boundary misses, rejection recall≥90% and zero valid rejected on each fresh/old probe set, both seeds. Unsupported probes remain in total rejection denominator; semantic-only results are additionally reported. Full qualification never overrides failed preservation.

Treatment/control superiority is a third, separate flag: no loss of any correct supplied-span outcome, correct operational mention or wholly exact case anywhere, plus at least one fresh correctness gain per seed. Fresh gains cannot offset old losses. This compares the bundled intervention under matched compute/sample count. Report both arms regardless of outcome. Historical contrast outputs are diagnostic comparisons only; no historical arm selection is permitted.

After all runs: independent same-instance evidence review; protected byte hashes including previous138-file contrast freeze; separate final result report. No retraining or threshold edits based on exposed fresh results.

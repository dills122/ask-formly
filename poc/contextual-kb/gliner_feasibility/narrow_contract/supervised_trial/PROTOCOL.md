# Bounded six-role supervised feasibility

User authorized autonomous work to determine whether question extraction can
improve. All work is inside POC; v2, A, data/DB, prior artifacts, retrieval and
answer layers unchanged. No repair rules or old adapted checkpoint used.

Training: 22 clear envelopes from existing narrow pilot, plus40 newly authored
clear questions. Exclude two ambiguous pilot rows rather than mislabel uncertainty
as absence. Separate24 independently authored clear development questions, author
does not see training content/predictions. Reserved custom names differ. This is
small synthetic development evidence, not a human benchmark or old sealed eval.
Shared library syntax/roles are inevitable; report train/dev similarity and do not
claim perfect semantic family-disjointness. No runtime ambiguous-status learning
or readiness claim from a clear-input-only experiment.

Freeze schema, optimizer, training data and dev hashes before inference/training.
Use same pinned local base and existing described six labels from narrow pilot.
Native explicit span export, all six labels including empty lists. Verify exact
character spans through InputExample roundtrip and native token target mappings
for EVERY training/dev row before optimizing. Entity-only targets; no relations,
classification or request records. No database access.

Two seeds1701/1702, each16epochs, effective batch8 (serial per-example gradient
accumulation), AdamW lr5e-4 weight_decay.01 clip1.0, LoRA rank8 alpha16 dropout0,
targets encoder + extractive_head supported by installed architecture-aware API.
CPUfloat32 fourthreads, deterministic algorithms; local files/offline. Fixed final
epoch16 checkpoint for each seed, no dev-selected best epoch, threshold.5 nested
overlap unchanged. No decoder/source repairs. Up to128updates per seed for62rows.
No tuning after dev results. Training-only loss logs may trigger abort on NaN,
target corruption or save/reload mismatch. Not on weak quality results.

Compare base versus both final adapters on all24 dev, and train separately.
Only question strings enter prediction; explicit training labels never in inference.
Report exact typed raw-span P/R/F1 perrole and overall; accepted nonoverlap contract
metrics separately, exact envelopes, conflicts, no-mention FPs, quote/wholepath
recovery, timing. Same gold for all models. Two seed runs are variability evidence,
not a confidence interval. Never equate train fit with dev generalization.

Worth continuing criterion, frozen before predictions: BOTH final seeds improve
raw dev F1 by >=10 percentage points over base AND accepted dev F1 improves,
without a >5-point drop in any nonempty role's recall. Qualification remains
>=90% P/R overall/everyrole, zero conflicts/errors and no unresolved critical
boundary misses. Failing qualification means no integration even if training helps.
Failure of worth-continuing criterion means don't scale this configuration blindly.

Checkpoint validation: first save after epoch1 and final save before any reload
comparison, compare original-model training-panel predictions to fresh loaded
adapter predictions exactly. Hash trainable and frozen weights before/after;
require some adapter changes and zero frozen changes. Preserve models locally,
optimizer/loss/update receipts and full predictions. No publication.

Independent review examines data, harness and results. Any correctness repair is
recorded separately; preserve failed first evidence. No expanding to broad-frame
training or whole-system redesign.

API evidence: installed gliner2 2.1.0 trainer, lora_targets.py and training/data.py;
official https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/9-training.md
and https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/8-train_data.md .
Installed boundary alias extractive_head maps to boundary_head; no dependency upgrade.

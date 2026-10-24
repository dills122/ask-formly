# Actual v2 outputs into GLiNER2: bounded paired inference

Inputs:30original requests plus all60questions from the first saved v2 run beta1.
No rewritten questions, reasons, global constraints or gold labels enter inference.
H11 produced no focused questions; report it as agent abstention, not GLiNER success.

2models: pinned local unadapted base; final epoch8adapter from completed seed1701.
Epoch8 is fixed final checkpoint, NOT development-selected/best/promoted. Prior
training dataset limitations remain; do not attribute failure to the library alone.
No retraining, threshold sweep, checkpoint search or schema tuning after results.

2schemas per model: unchanged native full frame (5entity types + relations +
interpretation + anchorless request records), and same5entity types alone. Compare
original versus focused within each fixed model/schema. Schema ablation is separate
from input effect. Threshold .5, include spans/confidence, nested overlap, CPUfloat32,
4threads, deterministic algorithms, seed1701; local files only. 360inference calls.

Gold entity annotations are authored blind to predictions with ANNOTATION.md.
Validate exact spans before scoring. Report typed exact-offset precision/recall/F1,
per category and per original parent. Because focused questions repeat context,
also compare recovery of shared unique (type,text) atoms per parent found in both
arms' gold. Do not count repeated context as independent question-level evidence.
Entity precision/recall does not prove condition attachment, correct polarity,
relation correctness, complete frames, searchable requests or final answers.

Full-frame diagnostics: actual number of request records, interpretation labels,
errors and spans. Without full-frame gold do not report frame accuracy. Preserve
all raw outputs/errors. Single warm pass per cell, no latency gate or timing repeats;
record total per-parent extraction time and request times, cold load separately.
Sequential model execution to avoid load contention. A missing/invalid prediction
counts as zero recall plus a reported failure, never excluded.

All writes in this experiment, all code imports within POC or its existing third-
party environment. No DB/search/knowledge/MCP changes; no old sealed evaluation.

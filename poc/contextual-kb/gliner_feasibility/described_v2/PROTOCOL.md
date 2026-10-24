# Description-only ablation on exposed v2 development questions

Fixed inputs: all 60 focused question strings from focused_v2/inputs.json.
No original questions, reasons, global constraints, rewriting or app investigation.
H11 remains upstream abstention and contributes no inference calls.
Reference labels: unchanged focused_v2/gold-1..3.json, 175 entity occurrences.
These agent labels and cases are exposed development material, not held-out evidence.

One candidate: labels.json descriptions with exactly the same five label keys.
Control: bare keys in identical order. No renaming, splitting, filters, regex,
postprocessing, threshold sweep, annotation revision or training.
Base and final epoch8 seed1701 adapter each run both schemas: 240 calls.
Same local pinned model/loader, CPU float32, four threads, seed1701,
deterministic algorithms, threshold .5, nested spans/confidence as prior run.
Alternate schema order by input index to reduce order/timing bias.
No repeated-run stability claim. Compare bare predictions to prior saved results.

Primary outcome: exact typed-offset micro P/R/F1, per-label breakdown, exact-set
question counts and per-parent scores; errors count as empty predictions and are
reported. Paired per-parent unique (type,text) coverage removes repeated context.
Improvement is a descriptive development result. We will not call extraction
fixed unless precision and recall are each >=90% overall and in each nonempty
category, with zero runtime/schema failures. This is an experiment decision gate,
not a production or answer-quality guarantee.
Report gains and losses, not just aggregate improvements.
No label/prompt revisions after inference; follow-ups require separate artifacts.
All writes here. A, v2, pilot, data/DB and earlier evidence remain unchanged.

API evidence: installed gliner2 2.1.0 inference/schema.py Schema.entities accepts
Dict[str,str] descriptions and retains entity_descriptions; official reference:
https://github.com/fastino-ai/GLiNER2/blob/main/gliner2/inference/schema.py
https://github.com/fastino-ai/GLiNER2

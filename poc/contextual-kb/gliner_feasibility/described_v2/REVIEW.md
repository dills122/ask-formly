# Independent review — description-only development ablation

Reviewed 2026-10-22 using the code-review-and-quality skill. Scope: experiment.py, test_experiment.py, labels.json and PROTOCOL.md; checked the focused_v2 scorer and runner, reused loader, and described_v2 saved outputs. No sealed evaluation material was accessed. No implementation, gold, model, training or protected artifact was changed by this review.

Verdict: approve this bounded development experiment. No blocking correctness findings in the reviewed implementation or saved results. This is not approval of extraction quality or deployment.

## Evidence

- `python3 -B -m unittest discover -s poc/contextual-kb/gliner_feasibility/described_v2 -p test_experiment.py`: four tests pass. These cover missing output, malformed output, duplicate predictions, exact spans and parent-level deduplication.
- Independently recomputed every saved score field from the raw outputs using the unchanged focused_v2 span validator and gold. All agree with scores.json: 60 question strings, 175 gold occurrences, four complete 60-row cells, correct model identifiers, no runtime/schema errors.
- Source freeze verification passes. Both saved described schemas contain exactly labels.json, and both controls retain the five bare keys in order. The runtime explicitly asserts retained entity_descriptions before inference.
- Both bare cells match the previous corresponding entity-only output exactly on all 60 questions, including confidence values. This supports the comparability of these saved runs.
- The reused loader fixes CPU float32, four threads, seed 1701 and deterministic schema sampling; this runner enables deterministic algorithms, keeps threshold 0.5 and nested spans, and loads the existing epoch-8 adapter without training. Inference receives only the focused question and selected schema. Gold is used for hashes and scoring, not inference.
- Missing or malformed prediction rows become empty predictions, preserving false negatives and preventing exact-question credit. Duplicate or unknown prediction IDs fail scoring. Strict typed offsets retain boundary errors. Per-parent unique counts deduplicate by (type, text), as stated; they are coverage measures, not exact boundary measures.

## Interpretation and limits

Base F1 rises from 35.49% to 49.09%; adapted F1 rises from 34.46% to 50.26%. False positives rise from 66 to 114 and from 70 to 117 respectively. Exact-question matches fall from 5 to 0 for each model. These losses must accompany any claimed improvement. Neither described cell approaches the protocol's joint 90% precision/recall gate. The protocol correctly identifies exposed development data and disclaims held-out, stability and answer-quality evidence.

The tests are narrow scorer tests; this review validated persisted schema serialization and complete saved records, but did not rerun model inference or independently instrument the library's internal description tokenization. Full integrity manifest checks are reported in the saved integrity.json; this review did not independently traverse its protected inventories.

## Optional hardening

The scorer checks schema names and prediction IDs but does not reject a row whose `model` metadata disagrees with its filename. All current rows have correct model metadata, so this does not affect the reported result. If reused for future experiments, reject mismatched model metadata and add a regression test to prevent accidentally scoring a copied cell under the wrong model name.

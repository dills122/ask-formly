# Preflight preliminary review

Review instance: 2 of 3. Recorded before reading AUTHOR-EXPLANATION.md.

Scope is the new retrieval_integration_v1 directory on dirty main c3091328f49d53de6b41a49c4fe5aa8f1c45e516; unrelated changes excluded. Independent code and test reads covered bridge, extract, retrieve, scoring, the reused integration/assessment and plan validation, and existing PilotIndex/RRF/merge. Graph coverage dated October 16 reports these files not_tracked; direct source fallback used without reindexing.

All 45 gold rows (78 mentions: 28/27/23 by batch), all 36 relevance cases, and all 46 catalog facts inspected. Source strings, offsets, order/nonoverlap, question identities, fact membership and required-group subsets checked mechanically. The method/generic/opaque-object decisions are prospective conventions, including the documented built-in registration-name distinction. R14/R31 remain partial and six empty-gold cases are unsupported-in-catalog, never false-library or hallucination labels.

No material code/label defect identified in the blind pass. Full questions, optional API-only probes, unchanged RRF/merge, top8, read-only SQLite and paired complete-group-loss blocking match the protocol. Extraction records carry timing/error evidence and exact core preservation is checked. No prediction artifacts are present.

Items to reconcile: scoring summaries omit explicit any-hit rate, count-sensitivity calculations, aggregate extractor/projection timing and explicit partial-case labels (underlying rows/raw files retain reconstructible evidence). These reporting obligations must be fulfilled in the completed report. Downstream retrieval/scoring do not themselves verify extraction/retrieval-freeze manifests; immutable-output checks must be part of final orchestration/review. Complete run-freeze is deliberately pending readiness and must include all transitive code, runtime, model and input dependencies before inference. Unit tests and author claim reconciliation remain to run.

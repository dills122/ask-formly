# Contextual supplemental query experiment

Read [FINAL-REPORT.md](FINAL-REPORT.md) for results and the decision, and [COMPLETED-REVIEW.md](COMPLETED-REVIEW.md) for independent verification.

This directory contains a separate, bounded comparison against the unchanged question-layer foundation. It preserves the existing retrieval engine, models and DB. Sealed evaluation was never opened.

- `PROTOCOL.md` and `test-output/design-freeze.json`: prospective criteria and source requests.
- `SUPPLEMENT-CONTRACT.md`: operation-first rewrite instructions.
- `data/records.json`: original first foundation and supplemental outputs.
- `data/cases.json`, `data/semantic-review.json`: independently reviewed relevance and semantic judgments, before retrieval.
- `test-output/retrieval/results.jsonl`: all 72 query/ranking traces.
- `test-output/scores.json`: complete paired metrics, errors and gates.
- `test-output/run-freeze.json`, `results-freeze.json`: immutable code/input/result evidence.
- `test-output/protected-before.json`, `protected-after-run.json`: verification of 45 prior manifests.

The entry point refuses to overwrite its run directory. Do not rerun or tune this experiment in place. New experiments require separate artifacts and fresh prospective cases.

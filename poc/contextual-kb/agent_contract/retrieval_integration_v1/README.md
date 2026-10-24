# Question-plan retrieval comparison

Read [RESULTS.md](RESULTS.md) for the measured results and next experiment proposal, and [COMPLETED-REVIEW.md](COMPLETED-REVIEW.md) for the independent assessment. The accepted foundation and both frozen GLiNER models are unchanged.

This new experiment tests optional API-name queries against full-question retrieval using the existing engine and read-only DB. It does not implement answer generation or open sealed evaluation.

Key evidence:

- PROTOCOL.md and test-output/design-freeze.json: prospective design and original requests.
- ADJUDICATION.md, LABEL-REVIEW.md, data/gold.json, data/cases.json: reviewed labels, before inference.
- PREFLIGHT-REVIEW.md: independent readiness review.
- test-output/run-freeze.json: input/code/model/dependency hashes.
- test-output/extraction/: first predictions, timing and unchanged-parameter receipts.
- test-output/retrieval/:144 first retrieval records, query traces and DB receipt.
- test-output/scores.json and report-metrics.json: exact extraction and retrieval accounting.
- test-output/results-freeze.json: immutable first results/report.
- test-output/protected-before.json and protected-after-run.json:44 prior manifests verified, sealed data hash-only.

The entry points intentionally refuse to overwrite existing outputs. Do not rerun or repair this frozen experiment in place. New candidates require a separate directory and new predeclared development tests. Existing results remain diagnostics.

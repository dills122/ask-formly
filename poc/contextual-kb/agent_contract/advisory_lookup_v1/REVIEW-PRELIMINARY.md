# Preliminary independent review
Review instance: 1 of 3. Recorded before reading AUTHOR-EXPLANATION.md or RESULTS.md.

Scope verified against dirty main HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516; only advisory_lookup_v1 and exact read-only dependencies reviewed. Parent supplied environment-recovery context, but no author rationale/results were read. Coverage checks report new Python files not_tracked in the October 16 graph, so source fallback used.

## Findings
- P1: cli.run performs verify_unchanged on a worker that ProcessExtractor._exchange has already closed after an inference/transport failure. AdvisoryLookup retrieves successfully and marks extraction degraded, but cli.run then raises GLiNER worker unavailable and never returns that packet. Offline mock reproduction retained in test-output/review-failure-reproduction.json. Fix operational verification failure handling without suppressing positive parameter-mismatch or retrieval failures, and exercise this complete CLI run path.
- P2: verify_live.main closes workers only on normal completion. A retrieval, serialization, evidence-save, or verification exception after model creation bypasses close. Persistent subprocesses require try/finally cleanup in the harness as well as the CLI.

## Evidence and pending checks
All 20 unittest cases pass. Tests cover lookup degradation and transport shutdown separately but omit their CLI composition. Static lookup/bridge inspection shows only full-question search_requests enter enhanced=False retrieval; returned records are copied and hints remain advisory. Foundation validator retains conditions and exact full queries.
Pending: complete live-native packets, actual CLI packet, parameter/model/DB hashes, 48 prior protection chains, freeze reconciliation, and author claims. No native inference or retrieval rerun performed.

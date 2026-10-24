# Review 3 preliminary assessment

Saved before reading INTEGRITY-FIX.md, AUTHOR-EXPLANATION.md or RESULTS.md. Bootstrap and prior reviewer findings were visible. Scope is ready-code-freeze on dirty main c3091328f49d53de6b41a49c4fe5aa8f1c45e516; unrelated working-tree changes excluded.

31 unit/fault tests passed independently (test-output/review3-tests.txt). Direct source inspection confirms typed IntegrityError at native checkpoint/load and final verification, serialized worker errors, transport reconstruction, lookup guard against integrate swallowing errors, and CLI rethrow with finally cleanup. Ordinary verification unavailability remains degraded with candidates retained. No native inference or DB retrieval rerun.

Potential blocking P2: reusable AdvisoryLookup retains load_attempted=True after a confirmed startup IntegrityError but does not retain the failure. A second valid lookup on the same instance skips initialization and returns eight candidates with advisory.status=available and no diagnostics. Reproduction retained in test-output/review3-reuse-integrity.json. This violates the known-mismatch boundary for the advertised reusable service; first-call-only tests do not cover it. The CLI itself creates a new service per invocation and propagates the original hard error correctly.

Remaining work: independently audit frozen source/evidence, all 48 preservation chains, both 48-request native panels and latest default CLI; reconcile author explanation after this saved pass. Graph coverage reported all eleven inspected source/test paths untracked in October16 generation; direct full-file source fallback used, no reindex.

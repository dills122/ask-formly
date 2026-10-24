# Independent preliminary review

Review instance: 4 of 4. Recorded before reading author rationale, final status, results, progress or task plan.

Target is dirty main at c3091328f49d53de6b41a49c4fe5aa8f1c45e516, bounded to advisory_lookup_v1. Unrelated dirty files are excluded. Fresh context contains the bootstrap and previous reviewer finding, but no implementation discussion.

No actionable source defect found in the final reuse-state diff so far. Both factory and extraction IntegrityError paths now latch a permanent lookup failure before retrieval. Transport latches remote and local verification mismatches before closing; subsequent exchange checks the latch before checking process availability. Ordinary runtime errors remain degradable. Source and tests confirm validation first, unchanged full-question projection, candidate copy isolation and cleanup. The new four reuse regressions plus surrounding tests all pass: 35 tests, retained in test-output/review4-tests.txt.

Pending: independently hash both final freezes, resolve historical manifest bindings against source archives, verify 48 preservation chains through qualified preserve.snapshot, and reconcile author claims and task plan. No native inference or retrieval rerun.

Graph search returned no POC symbols; coverage reports all 13 relied-on local source/test files not_tracked in generation 2026-10-16. Direct complete source inspection used instead. This is not a graph completeness claim.

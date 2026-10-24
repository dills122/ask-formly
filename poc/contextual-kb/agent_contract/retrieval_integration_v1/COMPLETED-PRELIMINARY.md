# Preliminary completed review

Review instance: 3 of 3. Written before reading RESULTS.md or AUTHOR-EXPLANATION.md.

Scope: retrieval_integration_v1 only, prior artifacts hash-only; no model/retrieval rerun. Bootstrap includes author-supplied scope and parent supplied R06 diagnostic before this note, so complete blindness to those claims was not possible. Numerical reconstruction used saved raw predictions and rankings independently of scoring functions.

Independent verify.py passed for all 45 annotation rows per model, all 144 retrieval rows, top4/top8 all/per-batch aggregates, role counts, exact sets, Wilson intervals, count sensitivity, original foundation-output identity, and full-question preservation. The 5 design, 329 run, 9 extraction, 3 retrieval and 54 result freeze entries match bytes. All 44 prior manifest snapshot results match before/after.

Observed accepted counts: seed1701 66 TP/12 FP/12 FN; seed1702 67/10/11. Neither meets pooled 89.25% precision; seed1701 batch1 also misses 80% recall. No missing extraction rows/errors observed. Boundary errors include invocation parentheses/arguments; role errors include modelChange and numeric key. Foundation annotation zero is inapplicable by design.

Retrieval R06 loses one relevant fact with both models and oracle; R30 top4 loses one relevant fact; oracle additionally loses R04 top4 relevance. All supported requests retain required groups at top8, but these groups deliberately exclude unresolved partial-catalog requirements. Additional queries do not improve aggregate top8 recall. No blocking evidence-integrity problem identified so far. Remaining checks: reconcile written claims, check timing summaries and saved fusion/probe correspondence, and exercise bounded unit tests with disposable fixture directory.

Graph freshness is not tracked for reviewed code; full direct source reads used. No index refresh performed.

# Author explanation

## Intent and scope
Test whether deeper candidate retrieval plus semantic selection can improve bounded eight-slot evidence packets. Four arms identify availability and selection effects; foundation and all prior candidates remain unchanged. This directory alone is new, on dirty main c3091328f49d53de6b41a49c4fe5aa8f1c45e516, not staged or committed. Existing unrelated work is excluded. User explicitly authorized this isolated retrieval/selection experiment despite older steering's question-only boundary.

## Implementation
candidate.py calls frozen PilotIndex.hybrid at8 and20 per original question, retains both pools, and uses existing merge_obligations for rank-only controls. It presents retrieved claims, conditions, limits, version and adapter under hash-ordered opaque handles without ranks or gold. Strict selection validation rejects >8, duplicates, unknown handles, malformed indexes and invalid envelopes; failed selections stay empty and counted. No repair or hidden fallback. account separates whole-envelope failure from invalid individual selections.

assessment.py uses the prior POC relevance metric for comparable precision@k, recall, nDCG, MRR and groups. It adds selected precision/counts, candidate availability, exact fact/group loss and fixed gates. Unsupported requests remain separate. A small floating tolerance on .005 avoids representation errors at the exact boundary, not a relaxed substantive gate.

pipeline.py has separate acquire and score phases. It verifies manifests, uses read-only SQLite, writes exclusive first-save evidence, freezes traces before selector inference, and verifies selection before grading. Gold is validated against catalog IDs but is never passed to acquisition or selection. All rankings are acquired once. Existing engine limit behavior means top20 need not prefix top8; baseline pool is explicitly retained.

preserve.py extends prior byte-only verification with merge_slots_v1 final manifest. Evaluation semantics remain sealed. Local third-party embedding artifacts are copied into this experiment's cache to avoid prior-cache writes; no model downloads/training.

## Verification and plan
Core acquisition/presentation/selection tests and assessment tests were written first, observed failing due to missing modules, then implemented and passed. Exclusive-save/hash safety checks were added to the reused orchestration primitives afterwards. 17 tests pass, including regression/swap detection, no-prefix assumptions, malformed delivery, opaque ordering, empty output and unsupported accounting. No live retrieval has yet run. Generation has36 first-save outputs,59 questions,zero structural failures; prospective semantic review can still find omissions. No claim of semantic perfection from structure.

## Tradeoffs and limits
Native fresh-context selection is a feasibility test with unpinned service configuration. It can judge relevance but does not prove factual answer entailment, application compatibility, deployable latency, repeatability or population ±.75pp accuracy. First-response wall time includes orchestration; report input/output bytes and separate query costs. Hashes verify bytes, not historical independence alone. Fresh wordings remain within a46-fact catalog. Current protocol tests depth20 without query expansion; if facts remain absent the experiment must report it, not tune queries.

## Challenge points
Check fair exact foundation parity, depth-induced rank shifts, no gold leakage to selectors, all per-case losses despite averages, required alternatives vs broad relevance labels, selection failures retained, opaque maps integrity, bounded no-retry evidence, semantic plan errors separate, and all preservation manifests. Review plan and code independently before accepting these claims. No author readiness recommendation is supplied.

# Independent preapply review

Review instance: 1 of 3 (Material select promotion).

## Findings

No actionable findings. Preliminary source/test concerns were recorded separately before the author explanation was read. The dispatch exposed architecture and claimed results, limiting full blindness.

## Plan review

The five-target boundary matches the authorized knowledge-only promotion. Source additions and both DB hashes are constrained, prior knowledge rows remain intact, all five canonical tables reproduce, and protected runtime/model bytes are checked. Snapshot and rollback behavior has meaningful failure and interruption tests. The plan correctly requires stopped serving during apply, reconnect afterward, and journal recovery after an uncatchable crash. Full installed smoke and documentation review are still mandatory before publication.

## Author-claim reconciliation

Confirmed directly: 93 facts/21 documents; exact candidate SHA-256 cc67af9eba6daa5024d671dd306dfd4ada4193e2663e05737d4db2bc39d9d63d; 88 unchanged non-DB runtime pins; 628 unaffected protected files; five target paths; canonical equality across documents, facts, evidence, fact_evidence and fact_links. Runner copies match promotion-v6 and cases match the qualified candidate bytes. Source checks include the promotion fixtures. Claimed historical RED runs were not independently rerun; current GREEN results were independently executed.

## Verification performed

- `python3 -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/promotion-v7 -p 'test_*.py' -v`: 15 passed.
- `python3 -B -m unittest discover -s tools -p test_project.py -v`: 4 passed (mocked suite-wiring checks; not full maintenance).
- `poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v7/promote.py --name review-preflight-1`: passed checked-only; installed files unchanged.
- Direct source/diff/spec/plan review and copy equality checks. Graph path coverage was unavailable/excluded, so Python conclusions rely on direct source inspection.

## Open questions and residual risks

Installation outcomes, all 15 delivered answers and citations, Q20 premise handling, final docs and final allowlisted preservation are pending. Atomicity is per file; the documented crash-recovery limit is real. Candidate quality remains 44/45 with a retained caller-display refusal and does not establish universal accuracy.

## Verdict

Ready for the authorized guarded apply. This is a preapply GO, not final publication readiness. Continue this same review instance against installed smoke, final preservation and current docs before commit/push/PR.

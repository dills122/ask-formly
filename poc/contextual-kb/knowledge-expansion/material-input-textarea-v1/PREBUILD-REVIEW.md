# Independent prebuild review

Review instance: 1 of 3. Scope: new `material-input-textarea-v1` directory on `codex/material-input-textarea`, HEAD `e5027e77c4807636db3ea943ff8edd561065d6cf`. Preliminary judgment was written before reading REVIEW-AUTHOR.md; an author message about crediting baseline evidence arrived during that first pass and is disclosed here. No implementation history was inherited.

## Findings

No blocking defect found in the proposed five facts, applicability, or isolated build path. No implementation changes are requested for this prebuild gate.

## Plan Review

The order is sound: source review, frozen inputs, isolated build and preservation/eligibility checks, runtime wiring freeze, fixed paired MCP comparison, semantic answer review, recommendation only. Claims remain exact Formly 6.3.12 Material. K47 establishes input-kind fallback and both template branches; K51 establishes textarea defaults and CDK bindings. Required is deliberately the renderer's `required` binding. The source does not warrant numeric parsing, disabled/payload equivalence, fixed geometry or hidden-container timing, and the facts and questions preserve those limits.

Ten focused cases plus five controls are appropriate for this bounded admission. Original questions are retained verbatim in both the request and supplied plan. Ninety lookup observations are three repeats of thirty arm/case combinations, not ninety independent caller answers or a planner evaluation. The threshold, all-control requirement and baseline-supported regression gate are explicit. Freeze and run-freeze are future gates, not yet completed evidence.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status | Consequence |
| --- | --- | --- | --- |
| Five source-grounded facts | Draft JSON, K47/K51 complete retained implementation, catalog records and SHA256 comparison | Confirmed | Suitable for exact-version admission testing |
| Exact guide quotes and unchanged source bytes | Five quote membership checks, derived source hash, preservation check | Confirmed | Summary quotes provide provenance; full implementation supports detailed bindings |
| Reused helper design | Direct inspection of candidate, harness, server, results and comparison with choice-controls counterparts | Confirmed | No new production runtime path |
| Eighteen tests pass | Reviewer ran the batch unittest command | Confirmed | Tests cover failure-sensitive bookkeeping and isolation paths, not semantic answer quality |
| Conditions preserved in full questions | Programmatic equality check across all fifteen cases/calls plus call-plan inspection | Confirmed | Paired plans isolate knowledge contribution |
| 321 protected paths and installed baseline preserved | Reviewer invoked `candidate.preserved()` | Confirmed | No drift detected at review time |
| Candidate not built | Candidate output absent | Confirmed | Candidate behavior remains unqualified |

The stated input overlap must be understood broadly: an existing fact's delivered implementation citation can answer a question even when its prose is less specific. Score all delivered evidence fairly; the new expected IDs are coverage labels, not mandatory grading answers.

## Verification Performed

- `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/material-input-textarea-v1 -p 'test_*.py'`: 18 passed.
- Read-only SHA256 checks: retained K47 and K51 match source-verification and canonical evidence catalog; all five guide quotes match the pinned source.
- `candidate.preserved()`: all 321 protected files plus installed DB matched.
- All fifteen case questions equal their initial request and plan question; no candidate-build directory exists.
- Graph search returned no symbols for this new scope; coverage reported the eight inspected Python files untracked. Used direct source inspection for all helper/test conclusions.

No candidate build, installed DB write, sealed evaluation, implementation edit, commit or publish occurred. Full project maintenance is being run by the initiating agent and is not claimed as reviewer-executed here.

## Open Questions And Residual Risks

`results.py:25-60` validates receipts, frozen calls, scope and observed fetch IDs but does not mechanically enforce the two-page/two-fetch limits or sixteen-item caps. The required final semantic reviewer must explicitly inspect those budgets in raw calls as well as unsupported claims. This is a manual audit responsibility rather than evidence of a current violation.

The optional plan-repair language cannot override `results.py:36-38` and `52-54`, which require canonical initial and discovery plans. If a repair becomes necessary, retain the failed attempt separately and explain its disposition; do not silently change frozen comparison inputs or call a repaired run identical.

Exact source hashes and compiler lint do not prove final retrieval or answer quality. Candidate runtime qualification, source/claim freeze contents, wiring freeze, recovery decisions, repeat equality and semantic grading remain to be inspected after execution. Credit baseline source excerpts; do not infer incremental benefit from new fact IDs alone.

## Verdict

**Ready** for freezing the reviewed inputs, one isolated candidate build, and the planned bounded comparison. This verdict does not qualify the candidate for promotion or establish whole-library coverage.

## Recommended Next Actions

Freeze the reviewed claims, source evidence, cases, supplied plans and helpers; build only in the new exclusive candidate directories; pin actual DB wiring before transport. Preserve all initial and recovery outputs, score both arms using their delivered evidence, and obtain the planned independent final-answer audit within the remaining review budget.

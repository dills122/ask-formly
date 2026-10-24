# Final independent review — instance 3 of 3

Verdict: **Not ready for functional POC acceptance.** One bounded integrity-state defect remains in the reusable component. The happy-path CLI and retained native panel are verified. This is not an annotation-accuracy or production-readiness assessment.

## Required finding

### P2 — Retain a known integrity failure across reusable lookup calls

`lookup.py:23–28` sets `load_attempted=True` before invoking the factory, then rethrows `IntegrityError` without retaining that failure. A caller that catches the exception and reuses the documented reusable `AdvisoryLookup` instance skips initialization on the next request. Because `extractor` and `load_error` are both still null, the next call executes retrieval and reports `advisory.status=available`, empty diagnostics, and eight candidates. A positively observed checkpoint mismatch has silently become successful availability.

Reproduced using the test index and factory raising `IntegrityError('checkpoint mismatch')`: first call raises; second call returns eight candidates and available status. See `test-output/review3-reuse-integrity.json` and the runnable `test-output/review3-reuse-reproduce.py`. No native model or real DB operation was involved. Persist a fatal integrity state for the service and reject subsequent model-requiring requests, including failures during extraction; add a regression for repeated use after a known mismatch. Ordinary unavailable-worker behavior must remain degradable.

The CLI constructs a new service for each run and correctly fails on the first integrity error; this finding concerns the explicitly documented reusable service. There is no claim that actual frozen weights changed. A hard exception alone does not make the reusable object unusable in Python, and no documented reset/discard contract prevents this path.

## Review and plan assessment

The implementation follows the intended foundation-plan → advisory extraction → unchanged full-question retrieval architecture. Query projection is the only input passed to `retrieve(..., enhanced=False)`; hints cannot affect query strings, ranking or candidate selection. Input validation precedes extraction, empty questions avoid model loading, candidate facts are copied, and retrieval errors propagate.

The typed-integrity correction closes review 2's immediate CLI defect: native checkpoint and verification mismatches use `IntegrityError`; worker startup and operation responses serialize the error type; transport reconstructs it; the lookup guard recovers integrity exceptions swallowed by the older integration layer; CLI explicitly rethrows them. Transport startup/exchange failures close the worker, and CLI/harness finally blocks close successfully constructed workers. Ordinary final verification unavailability keeps the full candidate packet, adds diagnostics, and reports unknown parameter integrity.

The small local subprocess adapter fits the two existing environments without adding packages or changing models. Contract and scope remain bounded. Five-axis review found no additional concrete blocker in input validation, subprocess command construction, query isolation, cleanup, or the existing timeout/response bound. Dense formatting reduces maintainability, but is not a functional acceptance blocker here. All task-plan boxes remain pending; final acceptance must not be marked complete while the required finding remains.

## Author-claim reconciliation

- Native and transported observed mismatches are hard failures on the failing call: confirmed by source and regression tests.
- Integrity failures remain hard failures for reusable service operation: incomplete; repeated initialization-failure case above contradicts that boundary.
- Ordinary unavailability preserves full-question retrieval: confirmed by composition tests and retained injected-worker CLI evidence.
- Both models preserve the unchanged full-question retrieval path: confirmed from all 144 retained packets, not inferred from summary booleans.
- Current default CLI executes native extraction successfully: confirmed from `cli-ready-native.json` and its matching freeze; two hints, eight facts, integrity true.
- Models, DB and prior evidence preserved: confirmed by offline hashes, historical source mapping and per-parameter receipts.
- Functional parity establishes annotation accuracy or production readiness: neither author nor this review makes that claim.

Preliminary findings were saved before reading INTEGRITY-FIX.md and AUTHOR-EXPLANATION.md. RESULTS.md was absent. Bootstrap claims and prior review findings were visible, but no author rationale preceded the source/test pass.

## Verification

Reviewed target: dirty main HEAD `c3091328f49d53de6b41a49c4fe5aa8f1c45e516`, bounded to new `advisory_lookup_v1`, with ready-code-freeze and ready-cli-freeze matching current bytes. Other working-tree changes are excluded.

- Independently ran `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/advisory_lookup_v1 -p 'test_*.py'`: **31 tests passed**, retained in `test-output/review3-tests.txt`.
- Inspected native runtime, worker, transport, lookup, CLI, live harness and all five test modules directly. Graph coverage reported these paths untracked in the October 16 generation; direct source fallback used, no reindex or graph-completeness claim.
- Offline evidence audit is retained as `test-output/review3-audit.py` and `review3-evidence-audit.json`. It adapts the earlier reviewer's audit after inspecting its assertions, adds final freezes and latest CLI, and executes no inference or retrieval. Its first attempt missed the pre-integrity archive mapping for original run lookup/runtime; corrected mapping passes, with no underlying artifact change.
- **48 prior preservation chains match** their recorded counts and every bound byte; sealed material was hashed only.
- **11 integration freezes match**, with archived pre-fix source for historical run/run-ready/final-code and current source for ready-code. Original failed-environment evidence remains intact.
- All 48 foundation and 48 per-seed native packets preserve exact input plans, query strings/order/count, query logs, final IDs and complete fact records. Each seed has 70 extractions. Seed 1701: 73 hints, including 38 API hints; seed 1702: 71 hints, including 39 API hints. Anchors and advisory-only flags validate; semantic annotation correctness is outside scope.
- All **564 parameter hashes per seed** match before/after and original training receipts. Current DB hash equals native setup hash.
- Latest native CLI has two hints, eight facts and true parameter integrity; injected-failure CLI has matching candidate facts with degraded status and unknown integrity.

No native inference, full panel, DB retrieval, training, annotation, or accuracy rerun was performed. No source/model/data edits were made by this reviewer; only review-3 artifacts were written.

## Decision and remaining work

**Not ready.** Return the reusable integrity-state finding to the author. Review instance budget is exhausted (3 of 3); do not create another review instance or broaden the work. Preserve this assessment and existing evidence. Any subsequent correction must be reported separately and cannot be described as independently approved by this review.

Known limits remain: unpinned foundation-generation revision, historical model-role errors, no certified answerability or abstention behavior, and no universal compatibility, accuracy-target, or production qualification.

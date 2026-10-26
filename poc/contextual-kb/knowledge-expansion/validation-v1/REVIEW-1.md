# Independent prebuild review

Review instance: 1 of 3. Reviewer mode; fresh context, bootstrap/tests/code/draft records inspected before author packets. Target: untracked validation-v1 working tree against HEAD a3240d33bed5ae82aa779a0004f80c8894924a97. No implementation edits, installed build, hosted inference, or sealed evaluation access performed by reviewer.

## Findings

No actionable blocking findings. The nine proposed claims agree with the inspected pinned source, within their stated limits. The code is ready for the isolated build gate; this is not a qualification or promotion verdict.

Preliminary concerns recorded before the author explanation were (1) correspondence between claimed public typing/message surfaces and attached evidence IDs, (2) preservation and exact runtime composition, and (3) whether fresh qualification was separated from development. Subsequent source and implementation checks resolved these concerns.

## Plan Review

The ordered plan is appropriate: freeze inputs, build exclusively under this batch, prove all five accepted tables are retained, verify actual retriever version/adapter eligibility, inspect the resulting artifact, then run the frozen comparison. The candidate count guard requires 79 facts and 17 documents. No runtime redesign or canonical knowledge write is required.

Qualification fixes ten targeted requests plus five unchanged regression/gap controls. Its three repeats use extractor seeds 1701/1702/1701 and counterbalance arm order by repeat/batch. These seeds do not establish deterministic hosted generation. Each repeat must meet 14/15 usability, every control, no critical/delivery failures, and no regression on baseline-supported cases. Matched-plan replay is a separate retrieval diagnostic, not additional final-answer success. These decision gates require final audit; the summarizer alone is not an automatic acceptance verdict.

The batch remains a development qualification set, not a sealed generalization test. No whole-library conclusion follows from it. Deferred exact message precedence, universal routed-error cleanup, production networking policy, and Angular execution remain explicitly out of scope.

## Author-Claim Reconciliation

| Claim | Evidence inspected | Status and consequence |
| --- | --- | --- |
| Nine bounded facts from two unchanged sources | Both draft documents; exact quotes; eight cached pinned upstream files and source-verification.json | Confirmed. Boolean adaptation, typed return contract, six built-ins, length casing, default display, message surfaces, async shapes, and group registration/routing match source. |
| Pinned upstream hashes match retained catalog | Recomputed all eight cached file hashes against recorded hashes; author receipt maps those to catalog; combined compiler lint | Confirmed cached hashes; no upstream tests executed. |
| Typed registration and message configuration have direct source support | K36 lines 30–39 and 62–67; K38 lines 45–77; K04 lines 39–44 and 61–62; K08 lines 97–143 | Confirmed. K36/K38 are supplemental inspected sources, not added fact-evidence IDs. The typed source quote retains its direct pinned typing URL. Existing guide quote supports the bounded message surfaces; no exact precedence is claimed. Do not misdescribe K08/K26 alone as the public type declaration. |
| Both arms use accepted runtime except explicit DB selection | experiment.py; foundation service/capitalization; selected and base backend; current create_server | Confirmed. Accepted lookup/extraction/selection/citation/closure methods remain inherited. Current project/version server context remains in use. |
| Existing evaluation machinery is reused unchanged | Byte comparisons of assess.py, delivery.py, replay.py, summarize.py, both schemas and GRADER.md against extensions-v2 | Confirmed. Delivery failure checks and fixed expected denominators retained. |
| Installed assets preserved | baseline-state.json; recomputation of all 166 protected file hashes | Confirmed before build; recheck after each gate. |
| Qualification is distinct from development | Fifteen qualification cases, five development requests, previous extensions-v2 controls | Confirmed: no identical requests across development/qualification; five controls equal previous cases. |
| Ten isolation fixtures pass | Independent unittest discovery | Confirmed, 10/10. Fixtures do not establish live retrieval or answer quality. |

## Verification Performed

- Verified Git HEAD and status: only validation-v1 untracked in the reviewed scope.
- Ran `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/validation-v1 -p 'test_*.py'`: 10 tests pass.
- Ran existing compiler lint on a temporary combined copy of canonical and draft authored JSON with unchanged evidence catalog: zero errors.
- Recomputed protected-file hashes: 166 matches, no mismatch.
- Read pinned raw K04, K08, K26, E03a, E04a, E04b, K36 and K38 at the recorded ranges; all eight cached byte hashes match source-verification.json. Explicitly observed Bootstrap import in E04b and the fact's core-only scope limitation.
- Checked candidate exclusive directory creation, read-only selected DB, manifest/path/digest checks, five-table superset checks, foreign keys, exact source offsets, count guard, and eligibility call by source inspection.
- Graph coverage reports the new batch code as untracked and current server metadata changed; read all relied-on new Python files and the full current server directly. Existing runtime paths report metadata matches, with normal best-effort caveat. No inference relies on graph absence.

## Open Questions And Residual Risks

Candidate compilation, row-preservation/eligibility results, real transport, live answer quality, repeat stability, and replay completeness are still unexecuted gates. Freeze all batch inputs/code/questions before build. Inspect the candidate manifest and actual built records before starting hosted calls. The final outcome audit must check every failed/critical/delivery case and baseline-supported regression, not just aggregate counts. No installation is approved by this report.

The raw upstream cache was supplied after the initial pass (initial fetching had kept bytes in memory); the reviewer inspected the now-retained cache and verified its hashes before this verdict. This does not change any authored claim.

## Verdict

Ready — prebuild GO for the isolated candidate only. No material fix or new review instance is required for the reviewed inputs. Postbuild and outcome checks may continue in this review instance if implementation and criteria stay frozen.

## Recommended Next Actions

Freeze reviewed batch inputs, build the isolated candidate once, retain its manifest and verification outputs, then return the candidate artifact checks for review before live comparison. Keep the installed 70-fact foundation and all locked assets unchanged.

## Postbuild and gate-evaluator addendum

Same review instance 1 of 3; no changes to the nine claims, candidate implementation or qualification criteria were needed. The added evaluate.py implements the already-declared decision gates; this is a bounded verification addition, not a plan replacement.

Independent read-only SQL/hash checks confirm candidate SHA-256 `226c377ecb4a8a220c5c6db541156c3dcad71045d73b21a5d205fbf164b7715b` and unchanged installed SHA-256 `a5fbfd098fe59b3f80090d3cf1551700542d82cee77aaa7c4ccc2d5023d84929`. All frozen input hashes and all candidate manifest input hashes match. All 166 protected file hashes still match.

| Table | Installed | Candidate | Lost or changed installed rows |
| --- | ---: | ---: | ---: |
| documents | 15 | 17 | 0 |
| facts | 70 | 79 | 0 |
| evidence | 41 | 46 | 0 |
| fact_evidence | 107 | 122 | 0 |
| fact_links | 58 | 70 | 0 |

SQLite integrity_check is `ok`, foreign_key_check is empty, and all fact source hashes/offsets/quotes match their retained sources. Both new documents are Formly6.3.12/core. The actual runtime eligibility check passes. Candidate checked_database verifies the isolated path, candidate hash, and manifest input hashes. No installed build or model load was run by the reviewer.

Read evaluate.py and test_evaluate.py in full after graph coverage reported them untracked. The evaluator checks the six expected arm/repeat combinations, fifteen unique cases per arm, aggregate consistency, delivery/assessment completeness, the candidate threshold, all five controls, critical limit, and paired baseline-supported regressions. Baseline critical errors remain visible diagnostics rather than candidate-quality failures. The frozen zero-delivery-failure policy applies to both arms. Its output still requires independent semantic and preservation audit.

Ran the same unittest-discovery command again after evaluator addition: 16/16 tests pass. Tests cover passing14/15 with a shared noncontrol miss, individual quality gates, missing/duplicate/extra rounds and cases, delivery failure in either arm, missing assessment, inconsistent counts and nonboolean grades. No live inference was performed.

Postbuild verdict: **Ready for the frozen live comparison**, provided the just-reviewed evaluator/harness/questions are included in the final prelive freeze and remain unchanged. Final usability, replay completeness, preservation and outcome review remain pending. No installation approval.

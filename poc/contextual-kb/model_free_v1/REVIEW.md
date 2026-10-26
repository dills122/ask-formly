# Independent architecture-candidate review

Review instance: 1 of 3. Verdict: **Ready**, for retention and use as the isolated feasibility candidate described here. This is not promotion approval or completed answer/harness qualification.

## Findings

No actionable implementation defects found within the frozen candidate scope. The preliminary ledger was written before reading REVIEW-AUTHOR.md. This reviewer had the neutral bootstrap and task summary, but not the implementation conversation or author rationale.

Scope verified against HEAD `8e8d02e82c01e3f0e6e0b74a31b8c7346ca22830`, branch `codex/versioned-knowledge`: untracked `poc/contextual-kb/model_free_v1` only. The two untracked JSON Schema candidate directories were excluded. No source changes, promotion, commits, hosted calls or additional reviewers were made by this review. Review reports are the only intentional edits.

Material limits, rather than defects hidden by this verdict:

- M03 and M04 each lack the predefined `custom-type-recipe-core/public-registration-type` ID. They must remain identity misses, even though delivered examples support the actual registration/use explanations.
- Final citations are display strings with fact IDs followed by source descriptions. They are traceable, but not compliant with a strict bare-ID field requirement. No six-perfect-machine-contract claim is justified.
- Caller repair and live follow-up were not exercised. Current validation raises ordinary errors; absent plans use disclosed raw search. Structured `needs_refinement`, `PLAN_REQUIRED` and a bounded repair loop are prospective changes, not features proved by this review.

## Plan Review

The implementation follows the original bounded plan. `candidate.py:Store` owns read-only SQLite loading, applicability filtering, lexical ranking and full provenance; `Service.lookup` owns plan validation, scope resolution, interleaving and evidence budgets. `server.py:create_server` exposes typed MCP tools and caller instructions. The dependency chain through capitalization, wording normalization, qualification/refinement validation, contract validation, settings and version resolution contains no serving-path inference. Reusing those pure modules and a separate record loader is consistent with keeping model imports out of the candidate.

`Store.search` constructs FTS expressions from tokenized, quoted terms and passes values as SQL parameters. Adapter/applicability eligibility precedes selection. Improved ranking uses stored symbols and fixed AND/OR rank fusion; it adds no authored aliases or facts. Search scans the small fixed corpus, so its repeated scope/provenance queries and hash checks are acceptable here; this review does not establish large-corpus performance.

`Service.lookup` conservatively sums complete fact/citation packets, selects no more than four candidates per question and sixteen distinct facts, and reports omitted IDs/truncation. The byte budget intentionally excludes envelope/plan text. `get_facts` rejects unknown/ineligible requests atomically and rejects oversized complete packets. Facts retain conditions, limits and applicability; citations retain authored quote/offset/hash and evidence references. Scope conflict checks and separate project settings are coherent with the documented contract. The structural validator cannot detect conditions omitted from both the plan question and its ledger; the instructions and response expose this limit.

Tests have meaningful failure sensitivity for late identifiers, OR retrieval despite AND hits, SQL-like input, scope, hash integrity, whole-record omission, condition binding, schema rejection and real stdio. Guard probes actually attempt network, subprocess and model import operations. The wrapper is Python instrumentation, not an OS sandbox. Fresh-machine installation, arbitrary plugin isolation and Kiro/Claude behavior remain outside this acceptance boundary.

The original Kiro/Claude step was explicitly revised by user authorization of an external Codex caller. That supports a Codex feasibility smoke only. The new repair-loop research changes a future interface decision; it does not retroactively fail the frozen raw-fallback contract or authorize silently changing its results.

## Caller Evidence Audit

Reviewed all six actual caller-2 argument plans, returned facts and final answers, using the original requests and saved audit files rather than the summary grades. Replayed all six service calls and reproduced their complete saved packets exactly. Every final citation's fact-ID prefix resolves to its delivered citation record. No follow-up call was necessary to reproduce these six saved packets; the live smoke did not demonstrate follow-up behavior.

| Case | Plan and delivered-answer assessment |
| --- | --- |
| M01 | Two questions preserve version, model retention and the registration distinction. The delivered reset-on-hide-false fact expressly limits control-tree retention; the answer preserves that distinction. |
| M02 | Two questions retain the supplied option-shape premise and local reload condition. Delivered mapping and strict-comparison facts support labelProp/valueProp configuration and distinguish stable scalar identity from object identity. The answer explicitly leaves the recordId type unresolved. |
| M03 | The falsy-model condition applies only to the default question; registration/use remains independent. Delivered defined-value/default-eligibility facts support retention, while the custom-component-use authored quote and E15a/E15b references support the illustrated registration/use. The designated public-registration-type ID remains missing. The answer describes an eligible keyed field, not universal default application. |
| M04 | The plan turns application-specific SSN/OTW wording into library implementation and registration questions without pretending to inspect the app. Delivered Material input K74/K75 excerpts directly show the superclass, bindings, imports and wrapper registration; the custom-component-use example supports selecting a registered alias. The answer marks application placement and SSN validation/masking as unknown. This is a reference pattern, not compiled application code; the designated public-registration-type ID remains missing. |
| M05 | The plan explicitly requests Formly 7. The service returns unsupported_version and no facts; the answer declines compatibility certification. |
| M06 | The plan separately asks about Observable options and external subscription ownership. The delivered observable-consumption fact supports both the stream path and the limit on cleanup guarantees; the answer retains that limit. |

These are six bounded observations, not an exhaustive semantic qualification. `caller-1/INVALID.json` explicitly excludes the earlier expectation-leaking run. The clean prompt lacks required_support/checks fields, and the public_cases regression restricts each caller case to ID and original request. No caller-1 quality evidence was counted.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status and consequence |
| --- | --- | --- |
| No server inference; models/installed knowledge unchanged | Full candidate source, reused import chain, guarded stdio/probe tests, baseline hashes | Confirmed for the inspected serving path and exercised calls. No OS isolation or universal absence-of-side-effects claim. |
| Scope, safe bounded complete delivery, provenance | Store/Service source, fixtures, six replayed caller packets, direct temporary-settings check | Confirmed within current corpus/contract. |
| 12 tests and project maintenance pass | Independently executed both documented commands | Confirmed; existing regression suite emitted a ResourceWarning but exited successfully. |
| 769 pins, installed DB and freeze intact | Rehashed all 769 entries, DB and all 10 freeze entries | Confirmed, no mismatches. |
| Retrieval totals and equal-budget comparison | compare.py, all 45 saved source hashes, independent totals and 135 complete packet replays | Confirmed. Historical hybrid is a saved reference, not rerun inference. |
| Clean external caller produced six answers with traceable citations | Receipt, prompt, all six arguments/packets/answers | Confirmed as saved-run evidence; this reviewer did not rerun the hosted caller or independently compare every raw event frame. |
| No completed repair/follow-up or Kiro/Claude qualification | Contract, tests, saved calls, stated exclusions | Confirmed as limitations; no broader compatibility inferred. |

## Verification Performed

- `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/model_free_v1 -p 'test_*.py'`: 12 tests passed.
- `python3 -B tools/project.py check`: passed local foundation checks without hosted inference or sealed evaluation.
- Independent read-only Python checks: all baseline/freeze hashes match; 45 unique repeat/case rows and every saved source hash match; all 135 basic8/improved8/improved16 packet values reproduce exactly using temporary settings; six caller packets reproduce exactly; citation prefixes resolve.
- Temporary-settings check: saved project core scope persists, excludes Material facts, and mixed valid/unknown follow-up IDs reject atomically.
- Graph status/coverage checked for all relied-on Python paths. Candidate files were not tracked in the 2026-10-25 graph; reused files had changed metadata or lacked records. Full direct-source fallback was used, with no reindex or completeness claim from graph absence.

Recomputed comparison: 45 observations = 15 requests repeated three times; 13 unique requests/39 observations have required IDs, totaling 54 required fact occurrences. Historical: 54/54 and 39/39 complete; basic8: 51/54 and 36/39; improved8 and improved16: 54/54 and 39/39 each. Basic's three misses are S08 `material-select-all/state-and-cache`, one per repeat. Improved8's result rules out a larger global cap as the explanation for this measured gain. Nonrequired candidate changes and repeated known plans prevent inferring semantic parity, statistical independence or unseen accuracy.

## Open Questions And Residual Risks

Structured repair errors, whether to require a plan, and the maximum repair count need a separately frozen revision if pursued. Clean installation and actual Kiro/Claude qualification remain pending. No Angular application was compiled or browser-tested; historical browser failures are unaffected. Citation formatting needs an explicit machine contract if downstream consumers require exact IDs. Semantic relevance and complete decomposition remain the caller's responsibility.

## Verdict

**Ready** as the isolated model-free feasibility candidate with its documented limitations. No heavy architecture pivot or additional review instance is required for the current frozen target. This verdict does not promote it, reopen JSON Schema admission, establish whole-library coverage, certify all answers, or qualify Kiro/Claude.

## Recommended Next Actions

Retain the frozen candidate and honest result denominators. Have the initiating task record acceptance/dispute/defer against this report. If the user proceeds with structured repair, define and test that new contract separately without rewriting these historical results; material changes require a fresh review within the remaining two-instance budget.

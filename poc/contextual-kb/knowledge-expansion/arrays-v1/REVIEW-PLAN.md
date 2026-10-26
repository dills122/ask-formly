# Arrays inventory and initial plan review

Review instance: 1 of 3. Scope: initial inventory and future admission plan only, against commit `39957158b18c040aae87a58a6fa9fcd58ec0a814` on `codex/knowledge-admission-70`. The reviewed arrays preparation files were untracked working-tree additions. This is neither source-admission approval nor a candidate prebuild/qualification review.

## Findings

**P2 — Distinguish development requests from fixed qualification cases before freezing them.** PLAN.md line 11 labels the 15 requests used for the three-repeat decision as “development requests.” The previous validation process separates development cases from fresh fixed qualification cases. If development probes were used to tune facts or selection and then counted toward the 14/15 gate, that would weaken the claimed comparison. Rename this set to fixed visible qualification requests and explicitly keep any development probes separate, freezing cases, criteria, harness and inputs before the build/qualification gate. This does not block retaining the initial inventory; resolve it before the prebuild review.

## Plan Review

The seven pending paragraph decisions reproduce every non-heading paragraph of the frozen arrays guide exactly. Proposed mappings identify the existing array-child cleanup fact and general registration support without admitting duplicates. Implementation, test-source and example provenance are distinguished. The plan correctly excludes unverified cross-version claims, executed upstream tests and a turnkey Material repeater guarantee.

The required next gate is exact pinned-source verification followed by independently reviewed claims, exclusions, candidate inputs and cases. K12, K27, K03 and E01a/b/c currently provide catalog paths, ranges and hashes, not retained upstream excerpts. Their metadata cannot establish add/remove option details, scalar truthiness handling, conditional index keys, default/hide behavior or Material presentation compatibility. All seven decisions must stay pending at this checkpoint.

The candidate must remain isolated and preserve all accepted rows across all five knowledge tables. Model and installed database writes are outside this checkpoint. Promotion remains a separate guarded decision. No fact-count target should drive splitting or duplication.

## Author-Claim Reconciliation

| Claim | Evidence inspected | Status |
| --- | --- | --- |
| Complete initial guide inventory, all pending | Exact paragraph comparison against arrays.md and ledger.json | Confirmed: seven paragraphs, one section, no admitted facts |
| Installed baseline is 79 facts / 17 documents | Read-only SQLite counts and SHA256 compared with baseline.json | Confirmed |
| Source identity unchanged | arrays.md SHA256 compared with ledger and baseline | Confirmed |
| Proposed upstream hashes match frozen catalog | K12/K27/K03/E01a/b/c catalog records | Confirmed as metadata only; source behavior unverified |
| Existing cleanup support should be reused | authored/hiding-and-visibility.json, hide-can-clear-array-children | Confirmed, with existing reset-on-hide and FormArray conditions |
| Candidate built or qualified | No such claim or candidate in review scope | Not performed; expressly outside this review |

The source and installed facts were inspected before the draft plan was ready. No separate author-explanation packet was supplied; the task description and subsequent draft prose supplied rationale, so this was not a fully blind rationale-free review.

## Verification Performed

- Ran the plan's `ledger.py check` command with the arrays manifest, ledger, canonical authored directory and installed database: `ok: true`, `complete: false`, one document and one section.
- Repeated with `--require-complete`: expected failure, `formly.arrays:L1: pending review`.
- Independently compared all seven ledger quotations with the source paragraphs; exact equality passed.
- Independently verified database SHA256 `226c377ecb4a8a220c5c6db541156c3dcad71045d73b21a5d205fbf164b7715b`, source SHA256 `8148916df949ea755be0e7f246e1242a0b68437b47da650444a6c8726a725c5e`, and read-only counts 79/17.
- Checked graph coverage for the source, catalog, existing cleanup document and principal draft files. Draft files were not tracked in the graph; all were read directly. Conclusions rely on file contents, not graph completeness.
- No external fetch, model inference, candidate build, source/catalog mutation, sealed evaluation access, commit or staging was performed by this reviewer. Full maintenance results belong to the parent task; this review does not claim to have run them.

## Open Questions And Residual Risks

Exact upstream bytes and semantics remain unverified in this batch. Candidate fact granularity, full authored records, development/qualification cases, harness pins and runtime eligibility are not yet available. Initial baseline metadata is not a substitute for the full protected-input manifest required at candidate build.

## Verdict

**Ready with non-blocking follow-ups — initial inventory checkpoint only.** The development/qualification terminology must be resolved before freezing cases. This verdict does not authorize candidate build or advance any source decision to admitted. The independent prebuild gate remains pending.

## Recommended Next Actions

Acknowledge the finding and clarify case separation. Then verify pinned upstream bytes, draft bounded claims and exclusions, freeze cases and protected inputs, and submit the concrete candidate source and harness for prebuild review. Preserve this inventory review as the initial checkpoint.

## Same-review correction addendum

Reviewed the revised PLAN.md step 5 in the same review instance (1 of 3). It now calls the scored set fresh visible qualification requests, explicitly excludes development/tuning probes, and requires independent review and freezing of cases, criteria, harness and candidate inputs before qualification. The preceding source-mapping review remains a prerequisite to any candidate build. **P2 closed.** This is a clarification of the existing gate, not a newly executed gate or new review instance.

Updated verdict: **Ready — initial inventory checkpoint only.** No actionable initial-plan findings remain. All source decisions and the independent source-mapping/prebuild gate remain pending; no candidate or qualification approval is implied. Only the revised plan text was checked for this correction; earlier verification results retain their original scope.

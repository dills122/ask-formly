# Prebuild independent review

Review instance: 1 of 3

## Preliminary blind-pass ledger

Recorded before reading REVIEW-PREBUILD-AUTHOR.md. The review target is the untracked public-api-v1 directory at HEAD 250f83da2d93aababf27f169078807ff66f183ee; unrelated dirty/untracked files are excluded. No build or qualification was run.

- Builder guards, baseline hash inventory, eight-table preservation, exact version checks and collision refusal appear sound on direct source inspection. All 35 local unit tests pass.
- P2 candidate finding: audit.py rejects failed recovery before accounting for its attempt; report.py requires zero receipt errors, conflicting with GRADING.md's explicit failed-fetch budget semantics.
- P2 candidate finding: report.py requires all eight preservation cases usable; PLAN/GRADING require no baseline-supported loss. The stricter gate is not predeclared.
- P2 candidate finding: field-get-tree-lookup says an absent descendant returns undefined without restricting numeric inputs. The source uses key.indexOf without scalar-number conversion; source-decisions excludes numeric totality but this limitation is not carried in that fact.
- Pinned cache hashes and aggregate authored copies match. Reviewed getField, reverseDeepMerge, registration/lookup/defaults, preset substitution, builder callback and rendering source support the main claims. K150–153 carry source coordinates rather than inline excerpts; final scoring must credit delivered claim quotes only for their actual content.
- Graph search has no public-api-v1 symbols; coverage reports no recorded scope issues but is older than this batch. Direct reads are the review evidence.
- Awaiting the prospective adjudication artifact before final verdict.

## Findings

No actionable findings remain in the reviewed prebuild state. Three P2 concerns from the blind pass were resolved by the author before freezing/building:

1. **Recovery failure semantics:** `audit.py:33` and `report.py:66` intentionally reject any tool-error run. GRADING now explicitly says a failed fetch consumes an attempt and fails transport qualification; retained packets may inform a separately labeled diagnosis only. This resolves the earlier specification mismatch without relaxing the audit.
2. **Preservation gate:** `report.py:35` requires all eight preservation cases fully supported, in addition to no loss of any baseline-supported case. PLAN/GRADING now explicitly declare both requirements. This resolves the earlier undocumented stricter gate.
3. **Numeric lookup limitation:** `api/test-output/upstream/utils.ts:344` calls `key.indexOf` without converting scalar numbers; `:345` uses the child key's length. A numeric request can throw and numeric child-key prefix traversal need not work. The initial `public-field-api/field-get-tree-lookup` overstated undefined-on-miss. Its revised claim now restricts lookup paths and traversed keyed groups to strings/arrays, carries a numeric traversal limitation, and API-01/API-02 adjudication preserves that limit. The aggregate copy, authored source quote and derived-from hash were rechecked after correction (source-notes SHA-256 `cc431a1f506f3f12ef1d984ce3ad09b2277ac4c18774c855cbd514bbfb018729`).

These are bounded prospective clarification/source-scope corrections within review instance 1, not changes to runtime architecture or historical scores.

## Plan Review

The plan is appropriate for a prebuild admission: source verification, source-independent requests, prospective adjudication, independent review, freeze, isolated compilation, eight-table superset checks, real stdio comparison, then final review. It preserves the 176-fact baseline and installed 124-fact DB separately. Builder inspection confirms exclusive new output creation, source inventory/hash checks, refusal of evidence collisions, foreign-key/source-offset/exact-version checks and retrieval eligibility invocation. No installed output is selected for writing.

Cases and adjudication cover the declared 24 targets, eight preservation cases and eight controls. The finite questions preserve comparisons and negations; the expected answers qualify preset blank values/object shapes, missing pseudo-types, optional names, typing versus runtime and unsupported guarantees. The revised combined gate is at least 22/24 positive targets, all preservation and control cases, no critical unsupported claim and no baseline-supported loss. Package rates remain descriptive.

Freeze and run-freeze artifacts are still future prerequisites. This review does not certify their eventual completeness or the future wiring/calls. No build or scored transport was executed.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status | Review consequence |
| --- | --- | --- | --- |
| Twelve additive facts and seven new evidence IDs | Aggregate authored JSON, extra-evidence, source notes and cached implementation/tests | Confirmed | 188 facts / 35 documents is a prospective build assertion, not an observed output. |
| Correct pinned source mappings | Fifteen cached-file SHA-256 checks; seven new source ranges; K140–142 inline excerpts | Confirmed for inspected cache | Source behavior verified against cached commit-pinned files; no independent network refetch in this review. |
| Existing compiler/baseline preserved | candidate.py accepted_inputs/build/compare_rows; baseline snapshot; tests | Confirmed by code/fixture inspection | Actual candidate superset and eligibility await build. |
| Explicit transport/regression gates | audit.py, report.py, revised PLAN/GRADING | Confirmed after clarification | Failed tool calls cannot be converted into passing qualification. |
| Source-verified adjudication before calls | All 40 adjudication rows, request obligations, inspected sources and existing evidence records | Confirmed as prospective criteria | Delivered packets must still independently supply every credited mechanism. |
| Claimed TDD history and whole-project maintenance pass | Author testimony only; reviewer ran the final local suite | Unverified historical execution | Do not present author command history as independently rerun evidence. |
| No model-backed inference qualification | Plan, harness/server and author limitations | Confirmed | Later model-free results must not be described as model-backed inference qualification. |

## Verification Performed

- `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/public-api-v1 -p 'test*.py'`: **35 tests passed**. Fixtures only; no candidate build.
- Read-only Python checks: all 15 cached source hashes matched; all seven additional evidence ranges fit the cached source; K140/K141/K142 inline excerpts matched exact lines; both aggregate authored copies matched package drafts.
- Read-only Python checks: all 40 cases, lookup calls and adjudication IDs align in order; requests and top-level version/adapter arguments are identical.
- Rechecked corrected lookup claim quote, source hash and aggregate/package copies after the author correction.
- Verified branch `codex/n1-radio-native-promotion`, HEAD `250f83da2d93aababf27f169078807ff66f183ee`, and untracked batch boundary. Unrelated dirty files were excluded.
- Graph discovery returned no batch symbols; exact-path coverage identified batch evidence as untracked. Direct source inspection was used instead. No graph completeness claim is made.

## Open Questions And Residual Risks

- K150–K153 provide source coordinates without inline excerpts. Authored claim quotes can supply their stated mechanisms, but URLs cannot supply additional missing behavior. In particular, expansive expected points must not receive credit merely because the reviewer knows their source location.
- `validate_judgments` validates flags, IDs and citation delivery, not semantic truth or obligation completeness. Manual judgments must apply Full/Partial/Unsupported from GRADING; `usable` must mean Full for target/preservation cases and pass for controls. Final review must inspect those judgments against packets.
- Accepted baseline facts are reused rather than exhaustively re-audited. New source claims and prospective criteria were reviewed; no universal library coverage conclusion follows.
- Runtime transport, output counts, eligibility and success rates remain unobserved until the separately frozen build/comparison. Sealed evaluation and global qualification archives were not opened.

## Verdict

**Ready** for the planned frozen isolated build and bounded comparison. This is prebuild readiness only, not candidate qualification, promotion approval or publication approval.

## Recommended Next Actions

Freeze the corrected claims, criteria, adjudication, plans and implementation before building. Run the predeclared isolated build and comparisons; retain failed attempts. Keep any unsupported obligations partial/unsupported without post-run edits to criteria. Reserve the remaining review instances for material fixes if necessary and the required final review.
